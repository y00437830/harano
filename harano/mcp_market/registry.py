"""Registry for MCP server entries."""

from __future__ import annotations

from typing import Iterator

from harano.mcp_market.models import MCPServer, MCPServerStatus


class MCPRegistry:
    """In-memory registry that holds :class:`~harano.mcp_market.models.MCPServer`
    entries indexed by their unique ``id``.
    """

    def __init__(self) -> None:
        self._servers: dict[str, MCPServer] = {}

    def add(self, server: MCPServer) -> None:
        """Add a new MCP server entry to the registry.

        Args:
            server: The :class:`MCPServer` instance to add.

        Raises:
            ValueError: If an entry with the same ``id`` already exists.
        """
        if server.id in self._servers:
            raise ValueError(f"MCP server {server.id!r} is already in the registry.")
        self._servers[server.id] = server

    def remove(self, server_id: str) -> None:
        """Remove an MCP server entry from the registry.

        Args:
            server_id: The unique id of the server to remove.

        Raises:
            KeyError: If no entry with *server_id* exists.
        """
        if server_id not in self._servers:
            raise KeyError(f"No MCP server with id {server_id!r} in the registry.")
        del self._servers[server_id]

    def get(self, server_id: str) -> MCPServer:
        """Return the MCP server entry for *server_id*.

        Raises:
            KeyError: If no entry with *server_id* exists.
        """
        if server_id not in self._servers:
            raise KeyError(f"No MCP server with id {server_id!r} in the registry.")
        return self._servers[server_id]

    def list_servers(self) -> list[MCPServer]:
        """Return all registered MCP server entries sorted by id."""
        return sorted(self._servers.values(), key=lambda s: s.id)

    def search(self, query: str) -> list[MCPServer]:
        """Return servers whose name, description, or tags contain *query*.

        The search is case-insensitive.

        Args:
            query: A free-text search string.
        """
        q = query.lower()
        return [
            s
            for s in self._servers.values()
            if q in s.name.lower()
            or q in s.description.lower()
            or any(q in tag.lower() for tag in s.tags)
        ]

    def filter_by_tag(self, tag: str) -> list[MCPServer]:
        """Return servers that carry *tag*.

        The match is case-insensitive.

        Args:
            tag: Tag string to filter by.
        """
        tag_lower = tag.lower()
        return [s for s in self._servers.values() if tag_lower in (t.lower() for t in s.tags)]

    def __iter__(self) -> Iterator[MCPServer]:
        return iter(self._servers.values())

    def __len__(self) -> int:
        return len(self._servers)

    def __contains__(self, server_id: str) -> bool:
        return server_id in self._servers
