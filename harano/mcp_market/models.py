"""Data models for the MCP marketplace."""

from __future__ import annotations

from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field, HttpUrl


class MCPServerStatus(str, Enum):
    """Lifecycle status of an MCP server entry."""

    AVAILABLE = "available"
    INSTALLED = "installed"
    DEPRECATED = "deprecated"


class MCPServer(BaseModel):
    """Describes a single MCP server available in the marketplace."""

    id: str = Field(..., description="Unique identifier for the MCP server.")
    name: str = Field(..., description="Human-readable display name.")
    version: str = Field(default="0.1.0", description="Semantic version.")
    description: str = Field(default="", description="What the server provides.")
    author: str = Field(default="", description="Author or organisation name.")
    homepage: Optional[str] = Field(
        default=None, description="URL to the server's homepage or repository."
    )
    tags: list[str] = Field(default_factory=list, description="Categorisation tags.")
    status: MCPServerStatus = Field(
        default=MCPServerStatus.AVAILABLE,
        description="Current status of this server entry.",
    )

    def is_installed(self) -> bool:
        """Return ``True`` if the server has been installed locally."""
        return self.status == MCPServerStatus.INSTALLED
