package com.harano.mcp;

import java.util.ArrayList;
import java.util.List;

/** Describes a single MCP server available in the marketplace. */
public class MCPServer {

    private String id;
    private String name;
    private String version;
    private String description;
    private String author;
    private String homepage;
    private List<String> tags = new ArrayList<>();
    private MCPServerStatus status = MCPServerStatus.AVAILABLE;

    public MCPServer() {}

    public MCPServer(String id, String name, String version, String description, String author) {
        this.id = id;
        this.name = name;
        this.version = version;
        this.description = description;
        this.author = author;
    }

    public boolean isInstalled() {
        return MCPServerStatus.INSTALLED.equals(this.status);
    }

    public String getId() { return id; }
    public void setId(String id) { this.id = id; }

    public String getName() { return name; }
    public void setName(String name) { this.name = name; }

    public String getVersion() { return version; }
    public void setVersion(String version) { this.version = version; }

    public String getDescription() { return description; }
    public void setDescription(String description) { this.description = description; }

    public String getAuthor() { return author; }
    public void setAuthor(String author) { this.author = author; }

    public String getHomepage() { return homepage; }
    public void setHomepage(String homepage) { this.homepage = homepage; }

    public List<String> getTags() { return tags; }
    public void setTags(List<String> tags) { this.tags = tags; }

    public MCPServerStatus getStatus() { return status; }
    public void setStatus(MCPServerStatus status) { this.status = status; }
}
