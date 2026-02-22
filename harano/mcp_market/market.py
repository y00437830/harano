"""High-level MCP marketplace operations."""

from __future__ import annotations

from harano.mcp_market.models import MCPServer, MCPServerStatus
from harano.mcp_market.registry import MCPRegistry


class MCPMarket:
    """Facade for marketplace operations on top of a :class:`MCPRegistry`.

    The market maintains two separate registries:

    * **catalog** – all servers published to the marketplace.
    * **installed** – servers that have been installed locally.

    Example::

        market = MCPMarket()
        market.publish(MCPServer(id="my-server", name="My Server"))
        market.install("my-server")
        assert market.is_installed("my-server")
    """

    def __init__(self) -> None:
        self._catalog = MCPRegistry()
        self._installed: dict[str, MCPServer] = {}

    # ------------------------------------------------------------------
    # Catalog management
    # ------------------------------------------------------------------

    def publish(self, server: MCPServer) -> None:
        """Add a server to the marketplace catalog.

        Args:
            server: The :class:`MCPServer` to publish.

        Raises:
            ValueError: If a server with the same ``id`` already exists in the catalog.
        """
        self._catalog.add(server)

    def unpublish(self, server_id: str) -> None:
        """Remove a server from the marketplace catalog.

        The server is also uninstalled if it was previously installed.

        Args:
            server_id: The unique id of the server to remove.

        Raises:
            KeyError: If no server with *server_id* exists in the catalog.
        """
        if self.is_installed(server_id):
            self.uninstall(server_id)
        self._catalog.remove(server_id)

    def list_available(self) -> list[MCPServer]:
        """Return all catalog entries that are not yet installed, sorted by id."""
        return sorted(
            (s for s in self._catalog if not self.is_installed(s.id)),
            key=lambda s: s.id,
        )

    def search(self, query: str) -> list[MCPServer]:
        """Search the catalog by free-text query.

        Args:
            query: Case-insensitive search string matched against name,
                description, and tags.
        """
        return self._catalog.search(query)

    # ------------------------------------------------------------------
    # Installation management
    # ------------------------------------------------------------------

    def install(self, server_id: str) -> MCPServer:
        """Install a server from the catalog.

        Sets the server's :attr:`status` to ``INSTALLED`` and tracks it in
        the installed set.

        Args:
            server_id: The unique id of the catalog server to install.

        Raises:
            KeyError: If *server_id* is not found in the catalog.
            ValueError: If the server is already installed.
        """
        if self.is_installed(server_id):
            raise ValueError(f"MCP server {server_id!r} is already installed.")
        server = self._catalog.get(server_id)
        installed = server.model_copy(update={"status": MCPServerStatus.INSTALLED})
        self._installed[server_id] = installed
        return installed

    def uninstall(self, server_id: str) -> None:
        """Uninstall a previously installed server.

        Args:
            server_id: The unique id of the server to uninstall.

        Raises:
            KeyError: If *server_id* is not currently installed.
        """
        if server_id not in self._installed:
            raise KeyError(f"MCP server {server_id!r} is not installed.")
        del self._installed[server_id]

    def list_installed(self) -> list[MCPServer]:
        """Return all installed servers sorted by id."""
        return sorted(self._installed.values(), key=lambda s: s.id)

    def is_installed(self, server_id: str) -> bool:
        """Return ``True`` if *server_id* is currently installed."""
        return server_id in self._installed

    def get_installed(self, server_id: str) -> MCPServer:
        """Return the installed MCPServer for *server_id*.

        Raises:
            KeyError: If *server_id* is not installed.
        """
        if server_id not in self._installed:
            raise KeyError(f"MCP server {server_id!r} is not installed.")
        return self._installed[server_id]
