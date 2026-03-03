package com.harano.mcp;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import java.util.List;
import java.util.NoSuchElementException;

import static org.junit.jupiter.api.Assertions.*;

class MCPMarketServiceTest {

    private MCPMarketService service;

    @BeforeEach
    void setUp() {
        service = new MCPMarketService();
    }

    private MCPServer makeServer(String id, String name) {
        return new MCPServer(id, name, "1.0.0", "A test server", "author");
    }

    @Test
    void publish_and_findById() {
        service.publish(makeServer("s1", "S1"));
        MCPServer found = service.findById("s1");
        assertEquals("s1", found.getId());
        assertEquals(MCPServerStatus.AVAILABLE, found.getStatus());
    }

    @Test
    void publish_duplicate_throws() {
        service.publish(makeServer("s1", "S1"));
        assertThrows(IllegalArgumentException.class, () -> service.publish(makeServer("s1", "S1b")));
    }

    @Test
    void publish_preservesAllFields() {
        MCPServer server = new MCPServer("s1", "My Server", "2.0.0", "desc", "alice");
        server.setHomepage("https://example.com");
        server.setTags(List.of("ai", "ml"));
        MCPServer published = service.publish(server);
        assertEquals("s1", published.getId());
        assertEquals("My Server", published.getName());
        assertEquals("2.0.0", published.getVersion());
        assertEquals("desc", published.getDescription());
        assertEquals("alice", published.getAuthor());
        assertEquals("https://example.com", published.getHomepage());
        assertEquals(List.of("ai", "ml"), published.getTags());
        assertEquals(MCPServerStatus.AVAILABLE, published.getStatus());
    }

    @Test
    void publish_returnsServerWithAvailableStatus() {
        MCPServer server = makeServer("s1", "S1");
        server.setStatus(MCPServerStatus.INSTALLED);
        MCPServer published = service.publish(server);
        assertEquals(MCPServerStatus.AVAILABLE, published.getStatus());
    }

    @Test
    void publish_appearsInListAll() {
        service.publish(makeServer("s1", "S1"));
        List<MCPServer> all = service.listAll();
        assertEquals(1, all.size());
        assertEquals("s1", all.get(0).getId());
    }

    @Test
    void publish_multipleServers() {
        service.publish(makeServer("s1", "Server One"));
        service.publish(makeServer("s2", "Server Two"));
        service.publish(makeServer("s3", "Server Three"));
        assertEquals(3, service.listAll().size());
    }

    @Test
    void publish_thenSearchByTag() {
        MCPServer server = makeServer("s1", "S1");
        server.setTags(List.of("data", "weather"));
        service.publish(server);
        List<MCPServer> results = service.search("weather");
        assertEquals(1, results.size());
        assertEquals("s1", results.get(0).getId());
    }

    @Test
    void publish_thenSearchByDescription() {
        service.publish(makeServer("s1", "S1"));
        List<MCPServer> results = service.search("test server");
        assertEquals(1, results.size());
    }

    @Test
    void unpublish_unknown_throws() {
        assertThrows(NoSuchElementException.class, () -> service.unpublish("nonexistent"));
    }

    @Test
    void findById_unknown_throws() {
        assertThrows(NoSuchElementException.class, () -> service.findById("x"));
    }

    @Test
    void listAvailable_excludesInstalled() {
        service.publish(makeServer("s1", "S1"));
        service.publish(makeServer("s2", "S2"));
        service.install("s1");
        List<MCPServer> available = service.listAvailable();
        assertEquals(1, available.size());
        assertEquals("s2", available.get(0).getId());
    }

    @Test
    void listAll_sorted() {
        service.publish(makeServer("b", "B"));
        service.publish(makeServer("a", "A"));
        List<String> ids = service.listAll().stream().map(MCPServer::getId).toList();
        assertEquals(List.of("a", "b"), ids);
    }

    @Test
    void install_setsStatusInstalled() {
        service.publish(makeServer("s1", "S1"));
        MCPServer installed = service.install("s1");
        assertEquals(MCPServerStatus.INSTALLED, installed.getStatus());
        assertTrue(service.isInstalled("s1"));
    }

    @Test
    void install_unknown_throws() {
        assertThrows(NoSuchElementException.class, () -> service.install("x"));
    }

    @Test
    void install_twice_throws() {
        service.publish(makeServer("s1", "S1"));
        service.install("s1");
        assertThrows(IllegalStateException.class, () -> service.install("s1"));
    }

    @Test
    void uninstall() {
        service.publish(makeServer("s1", "S1"));
        service.install("s1");
        service.uninstall("s1");
        assertFalse(service.isInstalled("s1"));
    }

    @Test
    void uninstall_notInstalled_throws() {
        service.publish(makeServer("s1", "S1"));
        assertThrows(NoSuchElementException.class, () -> service.uninstall("s1"));
    }

    @Test
    void listInstalled_sorted() {
        service.publish(makeServer("b", "B"));
        service.publish(makeServer("a", "A"));
        service.install("b");
        service.install("a");
        List<String> ids = service.listInstalled().stream().map(MCPServer::getId).toList();
        assertEquals(List.of("a", "b"), ids);
    }

    @Test
    void unpublish_alsoUninstalls() {
        service.publish(makeServer("s1", "S1"));
        service.install("s1");
        service.unpublish("s1");
        assertFalse(service.isInstalled("s1"));
        assertThrows(NoSuchElementException.class, () -> service.findById("s1"));
    }

    @Test
    void search_byName() {
        service.publish(makeServer("weather", "Weather API"));
        service.publish(makeServer("code", "Code Linter"));
        List<MCPServer> results = service.search("weather");
        assertEquals(1, results.size());
        assertEquals("weather", results.get(0).getId());
    }

    @Test
    void search_caseInsensitive() {
        service.publish(makeServer("weather", "Weather API"));
        assertEquals(1, service.search("WEATHER").size());
    }

    @Test
    void getInstalled_unknown_throws() {
        assertThrows(NoSuchElementException.class, () -> service.getInstalled("x"));
    }
}
