"""Tests for the MCP upload module."""

import json
import os
import tempfile
import unittest
from http.server import BaseHTTPRequestHandler, HTTPServer
from threading import Thread
from unittest.mock import patch

from mcp.upload import MCPConfig, MCPUploadError, MCPUploader


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _valid_config_dict() -> dict:
    """Return a minimal valid MCP configuration dictionary."""
    return {
        "name": "test-mcp-server",
        "version": "1.0.0",
        "description": "A test MCP server",
        "tools": [
            {"name": "tool_a", "description": "First tool"},
        ],
    }


class _MockHandler(BaseHTTPRequestHandler):
    """Tiny HTTP handler used by the upload integration tests."""

    def do_POST(self):  # noqa: N802
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length)
        data = json.loads(body)

        # Echo back with a status field
        response = {"status": "ok", "name": data.get("name")}
        payload = json.dumps(response).encode("utf-8")

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def log_message(self, format, *args):  # noqa: A002
        # Suppress log output during tests
        pass


# ---------------------------------------------------------------------------
# MCPConfig tests
# ---------------------------------------------------------------------------

class TestMCPConfigFromDict(unittest.TestCase):
    """Tests for MCPConfig.from_dict."""

    def test_valid_dict(self):
        cfg = MCPConfig.from_dict(_valid_config_dict())
        self.assertIsInstance(cfg, MCPConfig)

    def test_non_dict_raises(self):
        with self.assertRaises(MCPUploadError):
            MCPConfig.from_dict("not a dict")

    def test_none_raises(self):
        with self.assertRaises(MCPUploadError):
            MCPConfig.from_dict(None)


class TestMCPConfigFromFile(unittest.TestCase):
    """Tests for MCPConfig.from_file."""

    def test_valid_file(self):
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False
        ) as tmp:
            json.dump(_valid_config_dict(), tmp)
            tmp_path = tmp.name
        try:
            cfg = MCPConfig.from_file(tmp_path)
            self.assertIsInstance(cfg, MCPConfig)
        finally:
            os.unlink(tmp_path)

    def test_missing_file_raises(self):
        with self.assertRaises(MCPUploadError) as ctx:
            MCPConfig.from_file("/nonexistent/path.json")
        self.assertIn("not found", str(ctx.exception))

    def test_invalid_json_raises(self):
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False
        ) as tmp:
            tmp.write("{bad json")
            tmp_path = tmp.name
        try:
            with self.assertRaises(MCPUploadError) as ctx:
                MCPConfig.from_file(tmp_path)
            self.assertIn("Invalid JSON", str(ctx.exception))
        finally:
            os.unlink(tmp_path)


class TestMCPConfigValidation(unittest.TestCase):
    """Tests for MCPConfig.validate."""

    def test_valid_config(self):
        cfg = MCPConfig.from_dict(_valid_config_dict())
        self.assertTrue(cfg.validate())

    def test_missing_name(self):
        d = _valid_config_dict()
        del d["name"]
        cfg = MCPConfig.from_dict(d)
        with self.assertRaises(MCPUploadError) as ctx:
            cfg.validate()
        self.assertIn("name", str(ctx.exception))

    def test_missing_version(self):
        d = _valid_config_dict()
        del d["version"]
        cfg = MCPConfig.from_dict(d)
        with self.assertRaises(MCPUploadError) as ctx:
            cfg.validate()
        self.assertIn("version", str(ctx.exception))

    def test_missing_description(self):
        d = _valid_config_dict()
        del d["description"]
        cfg = MCPConfig.from_dict(d)
        with self.assertRaises(MCPUploadError) as ctx:
            cfg.validate()
        self.assertIn("description", str(ctx.exception))

    def test_missing_tools(self):
        d = _valid_config_dict()
        del d["tools"]
        cfg = MCPConfig.from_dict(d)
        with self.assertRaises(MCPUploadError) as ctx:
            cfg.validate()
        self.assertIn("tools", str(ctx.exception))

    def test_tools_not_list(self):
        d = _valid_config_dict()
        d["tools"] = "not a list"
        cfg = MCPConfig.from_dict(d)
        with self.assertRaises(MCPUploadError) as ctx:
            cfg.validate()
        self.assertIn("must be a list", str(ctx.exception))

    def test_tools_empty_list(self):
        d = _valid_config_dict()
        d["tools"] = []
        cfg = MCPConfig.from_dict(d)
        with self.assertRaises(MCPUploadError) as ctx:
            cfg.validate()
        self.assertIn("at least one tool", str(ctx.exception))

    def test_tool_not_dict(self):
        d = _valid_config_dict()
        d["tools"] = ["bad"]
        cfg = MCPConfig.from_dict(d)
        with self.assertRaises(MCPUploadError) as ctx:
            cfg.validate()
        self.assertIn("must be a dictionary", str(ctx.exception))

    def test_tool_missing_name(self):
        d = _valid_config_dict()
        d["tools"] = [{"description": "no name"}]
        cfg = MCPConfig.from_dict(d)
        with self.assertRaises(MCPUploadError) as ctx:
            cfg.validate()
        self.assertIn("missing 'name'", str(ctx.exception))

    def test_multiple_valid_tools(self):
        d = _valid_config_dict()
        d["tools"].append({"name": "tool_b"})
        cfg = MCPConfig.from_dict(d)
        self.assertTrue(cfg.validate())


class TestMCPConfigSerialization(unittest.TestCase):
    """Tests for MCPConfig.to_dict and to_json."""

    def test_to_dict(self):
        d = _valid_config_dict()
        cfg = MCPConfig.from_dict(d)
        self.assertEqual(cfg.to_dict(), d)

    def test_to_json(self):
        d = _valid_config_dict()
        cfg = MCPConfig.from_dict(d)
        result = json.loads(cfg.to_json())
        self.assertEqual(result, d)


# ---------------------------------------------------------------------------
# MCPUploader tests
# ---------------------------------------------------------------------------

class TestMCPUploaderInit(unittest.TestCase):
    """Tests for MCPUploader initialization."""

    def test_valid_init(self):
        uploader = MCPUploader("https://example.com", token="abc")
        self.assertEqual(uploader.endpoint, "https://example.com")

    def test_trailing_slash_stripped(self):
        uploader = MCPUploader("https://example.com/")
        self.assertEqual(uploader.endpoint, "https://example.com")

    def test_empty_endpoint_raises(self):
        with self.assertRaises(MCPUploadError):
            MCPUploader("")

    def test_none_token_allowed(self):
        uploader = MCPUploader("https://example.com")
        self.assertIsNotNone(uploader)


class TestMCPUploaderBuildRequest(unittest.TestCase):
    """Tests for MCPUploader._build_request."""

    def test_request_url(self):
        uploader = MCPUploader("https://example.com")
        cfg = MCPConfig.from_dict(_valid_config_dict())
        req = uploader._build_request(cfg)
        self.assertEqual(req.full_url, "https://example.com/mcp/upload")

    def test_request_method(self):
        uploader = MCPUploader("https://example.com")
        cfg = MCPConfig.from_dict(_valid_config_dict())
        req = uploader._build_request(cfg)
        self.assertEqual(req.method, "POST")

    def test_content_type_header(self):
        uploader = MCPUploader("https://example.com")
        cfg = MCPConfig.from_dict(_valid_config_dict())
        req = uploader._build_request(cfg)
        self.assertEqual(req.get_header("Content-type"), "application/json")

    def test_auth_header_present(self):
        uploader = MCPUploader("https://example.com", token="secret")
        cfg = MCPConfig.from_dict(_valid_config_dict())
        req = uploader._build_request(cfg)
        self.assertEqual(req.get_header("Authorization"), "Bearer secret")

    def test_auth_header_absent(self):
        uploader = MCPUploader("https://example.com")
        cfg = MCPConfig.from_dict(_valid_config_dict())
        req = uploader._build_request(cfg)
        self.assertIsNone(req.get_header("Authorization"))

    def test_request_body(self):
        uploader = MCPUploader("https://example.com")
        d = _valid_config_dict()
        cfg = MCPConfig.from_dict(d)
        req = uploader._build_request(cfg)
        self.assertEqual(json.loads(req.data.decode("utf-8")), d)


class TestMCPUploaderUploadValidation(unittest.TestCase):
    """Tests that upload validates the config before sending."""

    def test_upload_rejects_invalid_config(self):
        uploader = MCPUploader("https://example.com")
        cfg = MCPConfig.from_dict({"name": "incomplete"})
        with self.assertRaises(MCPUploadError):
            uploader.upload(cfg)


class TestMCPUploaderUploadNetwork(unittest.TestCase):
    """Integration tests that use a local HTTP server."""

    @classmethod
    def setUpClass(cls):
        cls.server = HTTPServer(("127.0.0.1", 0), _MockHandler)
        cls.port = cls.server.server_address[1]
        cls.thread = Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()

    def test_successful_upload(self):
        uploader = MCPUploader(f"http://127.0.0.1:{self.port}")
        cfg = MCPConfig.from_dict(_valid_config_dict())
        result = uploader.upload(cfg)
        self.assertEqual(result["status"], "ok")
        self.assertEqual(result["name"], "test-mcp-server")

    def test_upload_with_token(self):
        uploader = MCPUploader(
            f"http://127.0.0.1:{self.port}", token="my-token"
        )
        cfg = MCPConfig.from_dict(_valid_config_dict())
        result = uploader.upload(cfg)
        self.assertEqual(result["status"], "ok")

    def test_upload_connection_refused(self):
        uploader = MCPUploader("http://127.0.0.1:1")
        cfg = MCPConfig.from_dict(_valid_config_dict())
        with self.assertRaises(MCPUploadError) as ctx:
            uploader.upload(cfg)
        self.assertIn("Upload failed", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()
