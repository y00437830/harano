package com.harano.mcp;

import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.NoSuchElementException;

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
    public ResponseEntity<MCPServer> getServer(@PathVariable String id) {
        try {
            return ResponseEntity.ok(mcpMarketService.findById(id));
        } catch (NoSuchElementException e) {
            return ResponseEntity.notFound().build();
        }
    }

    @PostMapping
    public ResponseEntity<MCPServer> publishServer(@RequestBody MCPServer server) {
        try {
            return ResponseEntity.status(HttpStatus.CREATED).body(mcpMarketService.publish(server));
        } catch (IllegalArgumentException e) {
            return ResponseEntity.status(HttpStatus.CONFLICT).build();
        }
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> unpublishServer(@PathVariable String id) {
        try {
            mcpMarketService.unpublish(id);
            return ResponseEntity.noContent().build();
        } catch (NoSuchElementException e) {
            return ResponseEntity.notFound().build();
        }
    }

    // ------------------------------------------------------------------
    // Installation endpoints
    // ------------------------------------------------------------------

    @GetMapping("/installed")
    public List<MCPServer> listInstalled() {
        return mcpMarketService.listInstalled();
    }

    @PostMapping("/{id}/install")
    public ResponseEntity<MCPServer> installServer(@PathVariable String id) {
        try {
            return ResponseEntity.ok(mcpMarketService.install(id));
        } catch (NoSuchElementException e) {
            return ResponseEntity.notFound().build();
        } catch (IllegalStateException e) {
            return ResponseEntity.status(HttpStatus.CONFLICT).build();
        }
    }

    @DeleteMapping("/{id}/install")
    public ResponseEntity<Void> uninstallServer(@PathVariable String id) {
        try {
            mcpMarketService.uninstall(id);
            return ResponseEntity.noContent().build();
        } catch (NoSuchElementException e) {
            return ResponseEntity.notFound().build();
        }
    }
}
