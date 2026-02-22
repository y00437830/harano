"""Tests for the MCP marketplace."""

import pytest

from harano.mcp_market.market import MCPMarket
from harano.mcp_market.models import MCPServer, MCPServerStatus
from harano.mcp_market.registry import MCPRegistry


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def make_server(server_id: str = "server-1", **kwargs) -> MCPServer:
    return MCPServer(
        id=server_id,
        name=kwargs.get("name", f"Server {server_id}"),
        description=kwargs.get("description", ""),
        tags=kwargs.get("tags", []),
    )


# ---------------------------------------------------------------------------
# MCPServer model
# ---------------------------------------------------------------------------


class TestMCPServer:
    def test_defaults(self):
        server = MCPServer(id="s1", name="S1")
        assert server.version == "0.1.0"
        assert server.status == MCPServerStatus.AVAILABLE
        assert server.is_installed() is False

    def test_is_installed_when_status_installed(self):
        server = MCPServer(id="s1", name="S1", status=MCPServerStatus.INSTALLED)
        assert server.is_installed() is True

    def test_deprecated_not_installed(self):
        server = MCPServer(id="s1", name="S1", status=MCPServerStatus.DEPRECATED)
        assert server.is_installed() is False


# ---------------------------------------------------------------------------
# MCPRegistry
# ---------------------------------------------------------------------------


class TestMCPRegistry:
    def test_add_and_get(self):
        registry = MCPRegistry()
        server = make_server("s1")
        registry.add(server)
        assert registry.get("s1") is server

    def test_add_duplicate_raises(self):
        registry = MCPRegistry()
        registry.add(make_server("s1"))
        with pytest.raises(ValueError, match="already in the registry"):
            registry.add(make_server("s1"))

    def test_get_unknown_raises(self):
        registry = MCPRegistry()
        with pytest.raises(KeyError):
            registry.get("nonexistent")

    def test_remove(self):
        registry = MCPRegistry()
        registry.add(make_server("s1"))
        registry.remove("s1")
        assert "s1" not in registry

    def test_remove_unknown_raises(self):
        registry = MCPRegistry()
        with pytest.raises(KeyError):
            registry.remove("nonexistent")

    def test_list_servers_sorted(self):
        registry = MCPRegistry()
        registry.add(make_server("b"))
        registry.add(make_server("a"))
        ids = [s.id for s in registry.list_servers()]
        assert ids == ["a", "b"]

    def test_search_by_name(self):
        registry = MCPRegistry()
        registry.add(make_server("s1", name="Weather Tool"))
        registry.add(make_server("s2", name="Code Formatter"))
        results = registry.search("weather")
        assert len(results) == 1
        assert results[0].id == "s1"

    def test_search_by_description(self):
        registry = MCPRegistry()
        registry.add(make_server("s1", description="Fetches weather data"))
        results = registry.search("weather")
        assert len(results) == 1

    def test_search_by_tag(self):
        registry = MCPRegistry()
        registry.add(make_server("s1", tags=["weather", "api"]))
        registry.add(make_server("s2", tags=["code"]))
        results = registry.search("api")
        assert len(results) == 1
        assert results[0].id == "s1"

    def test_search_case_insensitive(self):
        registry = MCPRegistry()
        registry.add(make_server("s1", name="Weather Tool"))
        assert len(registry.search("WEATHER")) == 1

    def test_filter_by_tag(self):
        registry = MCPRegistry()
        registry.add(make_server("s1", tags=["nlp", "api"]))
        registry.add(make_server("s2", tags=["vision"]))
        results = registry.filter_by_tag("nlp")
        assert len(results) == 1
        assert results[0].id == "s1"

    def test_contains(self):
        registry = MCPRegistry()
        registry.add(make_server("s1"))
        assert "s1" in registry
        assert "s2" not in registry

    def test_len(self):
        registry = MCPRegistry()
        assert len(registry) == 0
        registry.add(make_server("s1"))
        assert len(registry) == 1

    def test_iter(self):
        registry = MCPRegistry()
        server = make_server("s1")
        registry.add(server)
        assert server in list(registry)


# ---------------------------------------------------------------------------
# MCPMarket
# ---------------------------------------------------------------------------


class TestMCPMarket:
    def test_publish_and_list_available(self):
        market = MCPMarket()
        market.publish(make_server("s1"))
        available = market.list_available()
        assert len(available) == 1
        assert available[0].id == "s1"

    def test_publish_duplicate_raises(self):
        market = MCPMarket()
        market.publish(make_server("s1"))
        with pytest.raises(ValueError):
            market.publish(make_server("s1"))

    def test_install(self):
        market = MCPMarket()
        market.publish(make_server("s1"))
        installed = market.install("s1")
        assert installed.status == MCPServerStatus.INSTALLED
        assert market.is_installed("s1")

    def test_install_unknown_raises(self):
        market = MCPMarket()
        with pytest.raises(KeyError):
            market.install("nonexistent")

    def test_install_twice_raises(self):
        market = MCPMarket()
        market.publish(make_server("s1"))
        market.install("s1")
        with pytest.raises(ValueError, match="already installed"):
            market.install("s1")

    def test_uninstall(self):
        market = MCPMarket()
        market.publish(make_server("s1"))
        market.install("s1")
        market.uninstall("s1")
        assert not market.is_installed("s1")

    def test_uninstall_not_installed_raises(self):
        market = MCPMarket()
        market.publish(make_server("s1"))
        with pytest.raises(KeyError):
            market.uninstall("s1")

    def test_list_installed(self):
        market = MCPMarket()
        market.publish(make_server("b"))
        market.publish(make_server("a"))
        market.install("b")
        market.install("a")
        ids = [s.id for s in market.list_installed()]
        assert ids == ["a", "b"]

    def test_installed_not_in_available(self):
        market = MCPMarket()
        market.publish(make_server("s1"))
        market.install("s1")
        available_ids = [s.id for s in market.list_available()]
        assert "s1" not in available_ids

    def test_unpublish_removes_from_catalog(self):
        market = MCPMarket()
        market.publish(make_server("s1"))
        market.unpublish("s1")
        assert market.list_available() == []

    def test_unpublish_also_uninstalls(self):
        market = MCPMarket()
        market.publish(make_server("s1"))
        market.install("s1")
        market.unpublish("s1")
        assert not market.is_installed("s1")

    def test_search(self):
        market = MCPMarket()
        market.publish(make_server("s1", name="Weather API"))
        market.publish(make_server("s2", name="Code Linter"))
        results = market.search("weather")
        assert len(results) == 1
        assert results[0].id == "s1"

    def test_get_installed(self):
        market = MCPMarket()
        market.publish(make_server("s1"))
        market.install("s1")
        server = market.get_installed("s1")
        assert server.id == "s1"
        assert server.status == MCPServerStatus.INSTALLED

    def test_get_installed_unknown_raises(self):
        market = MCPMarket()
        with pytest.raises(KeyError):
            market.get_installed("nonexistent")
