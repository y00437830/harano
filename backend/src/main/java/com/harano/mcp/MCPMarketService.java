package com.harano.mcp;

import com.harano.SearchUtils;
import org.springframework.stereotype.Service;

import java.util.*;
import java.util.concurrent.ConcurrentHashMap;

/** Marketplace service managing catalog and installation state for MCP servers. */
@Service
public class MCPMarketService {

    private final Map<String, MCPServer> catalog = new ConcurrentHashMap<>();
    private final Map<String, MCPServer> installed = new ConcurrentHashMap<>();

    // ------------------------------------------------------------------
    // Catalog management
    // ------------------------------------------------------------------

    public MCPServer publish(MCPServer server) {
        if (catalog.containsKey(server.getId())) {
            throw new IllegalArgumentException("MCP server '" + server.getId() + "' already exists in catalog.");
        }
        server.setStatus(MCPServerStatus.AVAILABLE);
        catalog.put(server.getId(), server);
        return server;
    }

    public void unpublish(String serverId) {
        if (!catalog.containsKey(serverId)) {
            throw new NoSuchElementException("MCP server not found in catalog: " + serverId);
        }
        installed.remove(serverId);
        catalog.remove(serverId);
    }

    public List<MCPServer> listAvailable() {
        return catalog.values().stream()
                .filter(s -> !installed.containsKey(s.getId()))
                .sorted(Comparator.comparing(MCPServer::getId))
                .toList();
    }

    public List<MCPServer> listAll() {
        return catalog.values().stream()
                .sorted(Comparator.comparing(MCPServer::getId))
                .toList();
    }

    public MCPServer findById(String id) {
        return Optional.ofNullable(catalog.get(id))
                .orElseThrow(() -> new NoSuchElementException("MCP server not found: " + id));
    }

    public List<MCPServer> search(String query) {
        return SearchUtils.search(catalog.values(), query);
    }

    // ------------------------------------------------------------------
    // Installation management
    // ------------------------------------------------------------------

    public MCPServer install(String serverId) {
        if (installed.containsKey(serverId)) {
            throw new IllegalStateException("MCP server '" + serverId + "' is already installed.");
        }
        MCPServer server = findById(serverId);
        MCPServer installedCopy = copyServer(server);
        installedCopy.setStatus(MCPServerStatus.INSTALLED);
        installed.put(serverId, installedCopy);
        return installedCopy;
    }

    public void uninstall(String serverId) {
        if (!installed.containsKey(serverId)) {
            throw new NoSuchElementException("MCP server is not installed: " + serverId);
        }
        installed.remove(serverId);
    }

    public List<MCPServer> listInstalled() {
        return installed.values().stream()
                .sorted(Comparator.comparing(MCPServer::getId))
                .toList();
    }

    public boolean isInstalled(String serverId) {
        return installed.containsKey(serverId);
    }

    public MCPServer getInstalled(String serverId) {
        return Optional.ofNullable(installed.get(serverId))
                .orElseThrow(() -> new NoSuchElementException("MCP server is not installed: " + serverId));
    }

    // ------------------------------------------------------------------
    // Helpers
    // ------------------------------------------------------------------

    private MCPServer copyServer(MCPServer src) {
        MCPServer copy = new MCPServer(src.getId(), src.getName(), src.getVersion(),
                src.getDescription(), src.getAuthor());
        copy.setHomepage(src.getHomepage());
        copy.setTags(new ArrayList<>(src.getTags()));
        copy.setStatus(src.getStatus());
        return copy;
    }
}
