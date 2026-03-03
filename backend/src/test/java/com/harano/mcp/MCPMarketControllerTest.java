package com.harano.mcp;

import com.fasterxml.jackson.databind.ObjectMapper;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.http.MediaType;
import org.springframework.test.annotation.DirtiesContext;
import org.springframework.test.web.servlet.MockMvc;

import java.util.List;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

@SpringBootTest
@AutoConfigureMockMvc
@DirtiesContext(classMode = DirtiesContext.ClassMode.AFTER_EACH_TEST_METHOD)
class MCPMarketControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @Autowired
    private ObjectMapper objectMapper;

    private MCPServer makeServer(String id, String name) {
        return new MCPServer(id, name, "1.0.0", "A test server", "author");
    }

    // ------------------------------------------------------------------
    // Publish (upload) endpoint tests
    // ------------------------------------------------------------------

    @Test
    void publishServer_returns201WithServer() throws Exception {
        MCPServer server = makeServer("weather", "Weather API");
        server.setTags(List.of("weather", "api"));

        mockMvc.perform(post("/api/mcp")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(server)))
                .andExpect(status().isCreated())
                .andExpect(jsonPath("$.id").value("weather"))
                .andExpect(jsonPath("$.name").value("Weather API"))
                .andExpect(jsonPath("$.version").value("1.0.0"))
                .andExpect(jsonPath("$.description").value("A test server"))
                .andExpect(jsonPath("$.author").value("author"))
                .andExpect(jsonPath("$.status").value("AVAILABLE"))
                .andExpect(jsonPath("$.tags[0]").value("weather"))
                .andExpect(jsonPath("$.tags[1]").value("api"));
    }

    @Test
    void publishServer_withFullPayload_returns201() throws Exception {
        MCPServer server = new MCPServer("code-linter", "Code Linter", "2.1.0",
                "Lint your code", "alice");
        server.setHomepage("https://example.com");
        server.setTags(List.of("linting", "code-quality"));

        mockMvc.perform(post("/api/mcp")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(server)))
                .andExpect(status().isCreated())
                .andExpect(jsonPath("$.id").value("code-linter"))
                .andExpect(jsonPath("$.homepage").value("https://example.com"))
                .andExpect(jsonPath("$.tags").isArray())
                .andExpect(jsonPath("$.tags.length()").value(2));
    }

    @Test
    void publishServer_duplicate_returns409() throws Exception {
        MCPServer server = makeServer("weather", "Weather API");
        String json = objectMapper.writeValueAsString(server);

        mockMvc.perform(post("/api/mcp")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(json))
                .andExpect(status().isCreated());

        mockMvc.perform(post("/api/mcp")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(json))
                .andExpect(status().isConflict());
    }

    @Test
    void publishServer_thenGetById_returnsPublished() throws Exception {
        MCPServer server = makeServer("weather", "Weather API");

        mockMvc.perform(post("/api/mcp")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(server)))
                .andExpect(status().isCreated());

        mockMvc.perform(get("/api/mcp/weather"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.id").value("weather"))
                .andExpect(jsonPath("$.name").value("Weather API"));
    }

    @Test
    void publishServer_thenListAll_includesPublished() throws Exception {
        MCPServer server = makeServer("weather", "Weather API");

        mockMvc.perform(post("/api/mcp")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(server)))
                .andExpect(status().isCreated());

        mockMvc.perform(get("/api/mcp"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.length()").value(1))
                .andExpect(jsonPath("$[0].id").value("weather"));
    }

    @Test
    void publishServer_multipleServers_allListed() throws Exception {
        mockMvc.perform(post("/api/mcp")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(makeServer("a", "Server A"))))
                .andExpect(status().isCreated());

        mockMvc.perform(post("/api/mcp")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(makeServer("b", "Server B"))))
                .andExpect(status().isCreated());

        mockMvc.perform(get("/api/mcp"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.length()").value(2));
    }

    @Test
    void publishServer_thenSearch_findsIt() throws Exception {
        MCPServer server = makeServer("weather", "Weather API");
        server.setTags(List.of("weather"));

        mockMvc.perform(post("/api/mcp")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(server)))
                .andExpect(status().isCreated());

        mockMvc.perform(get("/api/mcp").param("q", "Weather"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.length()").value(1))
                .andExpect(jsonPath("$[0].id").value("weather"));
    }

    @Test
    void publishServer_thenUnpublish_removesFromCatalog() throws Exception {
        MCPServer server = makeServer("weather", "Weather API");

        mockMvc.perform(post("/api/mcp")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(server)))
                .andExpect(status().isCreated());

        mockMvc.perform(delete("/api/mcp/weather"))
                .andExpect(status().isNoContent());

        mockMvc.perform(get("/api/mcp/weather"))
                .andExpect(status().isNotFound());
    }

    @Test
    void getServer_notFound_returns404() throws Exception {
        mockMvc.perform(get("/api/mcp/nonexistent"))
                .andExpect(status().isNotFound());
    }

    @Test
    void unpublishServer_notFound_returns404() throws Exception {
        mockMvc.perform(delete("/api/mcp/nonexistent"))
                .andExpect(status().isNotFound());
    }
}
