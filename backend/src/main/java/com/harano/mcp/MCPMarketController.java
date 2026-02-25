package com.harano.mcp;

import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

/** REST controller for the MCP marketplace. */
@RestController
@RequestMapping("/api/mcp")
@CrossOrigin(origins = "*")
public class MCPMarketController {

    private final MCPMarketService mcpMarketService;

    public MCPMarketController(MCPMarketService mcpMarketService) {
        this.mcpMarketService = mcpMarketService;
    }

    // ------------------------------------------------------------------
    // Catalog endpoints
    // ------------------------------------------------------------------

    @GetMapping
    public List<MCPServer> listServers(
            @RequestParam(required = false) String q,
            @RequestParam(required = false, defaultValue = "false") boolean availableOnly) {
        if (q != null && !q.isBlank()) {
            return mcpMarketService.search(q);
        }
        return availableOnly ? mcpMarketService.listAvailable() : mcpMarketService.listAll();
    }

    @GetMapping("/{id}")
    public MCPServer getServer(@PathVariable String id) {
        return mcpMarketService.findById(id);
    }

    @PostMapping
    public ResponseEntity<MCPServer> publishServer(@RequestBody MCPServer server) {
        return ResponseEntity.status(HttpStatus.CREATED).body(mcpMarketService.publish(server));
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> unpublishServer(@PathVariable String id) {
        mcpMarketService.unpublish(id);
        return ResponseEntity.noContent().build();
    }

    // ------------------------------------------------------------------
    // Installation endpoints
    // ------------------------------------------------------------------

    @GetMapping("/installed")
    public List<MCPServer> listInstalled() {
        return mcpMarketService.listInstalled();
    }

    @PostMapping("/{id}/install")
    public MCPServer installServer(@PathVariable String id) {
        return mcpMarketService.install(id);
    }

    @DeleteMapping("/{id}/install")
    public ResponseEntity<Void> uninstallServer(@PathVariable String id) {
        mcpMarketService.uninstall(id);
        return ResponseEntity.noContent().build();
    }
}
