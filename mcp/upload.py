"""MCP Upload Module.

Provides functionality to upload MCP (Model Context Protocol) server
configurations to a remote registry or endpoint.
"""

import json
import os
import urllib.request
import urllib.error


class MCPUploadError(Exception):
    """Raised when an MCP upload operation fails."""


class MCPConfig:
    """Represents an MCP server configuration."""

    REQUIRED_FIELDS = {"name", "version", "description", "tools"}

    def __init__(self, config: dict):
        self._config = config

    @classmethod
    def from_file(cls, path: str) -> "MCPConfig":
        """Load an MCP configuration from a JSON file.

        Args:
            path: Path to the JSON configuration file.

        Returns:
            An MCPConfig instance.

        Raises:
            MCPUploadError: If the file cannot be read or parsed.
        """
        if not os.path.isfile(path):
            raise MCPUploadError(f"Configuration file not found: {path}")
        try:
            with open(path, "r", encoding="utf-8") as fh:
                data = json.load(fh)
        except json.JSONDecodeError as exc:
            raise MCPUploadError(f"Invalid JSON in {path}: {exc}") from exc
        return cls(data)

    @classmethod
    def from_dict(cls, data: dict) -> "MCPConfig":
        """Create an MCPConfig from a dictionary.

        Args:
            data: Configuration dictionary.

        Returns:
            An MCPConfig instance.
        """
        if not isinstance(data, dict):
            raise MCPUploadError("Configuration must be a dictionary")
        return cls(data)

    def validate(self) -> bool:
        """Validate that the configuration contains all required fields.

        Returns:
            True if valid.

        Raises:
            MCPUploadError: If required fields are missing or tools is invalid.
        """
        missing = self.REQUIRED_FIELDS - set(self._config.keys())
        if missing:
            raise MCPUploadError(f"Missing required fields: {', '.join(sorted(missing))}")

        if not isinstance(self._config["tools"], list):
            raise MCPUploadError("'tools' must be a list")

        if len(self._config["tools"]) == 0:
            raise MCPUploadError("'tools' must contain at least one tool")

        for i, tool in enumerate(self._config["tools"]):
            if not isinstance(tool, dict):
                raise MCPUploadError(f"Tool at index {i} must be a dictionary")
            if "name" not in tool:
                raise MCPUploadError(f"Tool at index {i} is missing 'name'")

        return True

    def to_dict(self) -> dict:
        """Return the configuration as a dictionary."""
        return dict(self._config)

    def to_json(self) -> str:
        """Return the configuration as a JSON string."""
        return json.dumps(self._config, ensure_ascii=False)


class MCPUploader:
    """Handles uploading MCP configurations to a remote endpoint."""

    def __init__(self, endpoint: str, token: str | None = None):
        """Initialize the uploader.

        Args:
            endpoint: The URL of the upload endpoint.
            token: Optional authentication token.
        """
        if not endpoint:
            raise MCPUploadError("Endpoint URL must not be empty")
        self._endpoint = endpoint.rstrip("/")
        self._token = token

    @property
    def endpoint(self) -> str:
        return self._endpoint

    def _build_request(self, config: MCPConfig) -> urllib.request.Request:
        """Build an HTTP request for uploading.

        Args:
            config: The MCP configuration to upload.

        Returns:
            A configured urllib Request object.
        """
        data = config.to_json().encode("utf-8")
        headers = {"Content-Type": "application/json"}
        if self._token:
            headers["Authorization"] = f"Bearer {self._token}"
        return urllib.request.Request(
            f"{self._endpoint}/mcp/upload",
            data=data,
            headers=headers,
            method="POST",
        )

    def upload(self, config: MCPConfig) -> dict:
        """Upload an MCP configuration.

        Args:
            config: A validated MCPConfig instance.

        Returns:
            A dict with upload result info.

        Raises:
            MCPUploadError: If validation or upload fails.
        """
        config.validate()
        request = self._build_request(config)
        try:
            with urllib.request.urlopen(request, timeout=30) as resp:
                body = resp.read().decode("utf-8")
                return json.loads(body)
        except urllib.error.HTTPError as exc:
            raise MCPUploadError(
                f"Upload failed with HTTP {exc.code}: {exc.reason}"
            ) from exc
        except urllib.error.URLError as exc:
            raise MCPUploadError(f"Upload failed: {exc.reason}") from exc
        except Exception as exc:
            raise MCPUploadError(f"Upload failed: {exc}") from exc
