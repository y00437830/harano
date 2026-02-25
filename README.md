# harano

**harano** is a Skill and MCP (Model Context Protocol) marketplace platform.

- **Backend** – Java 17 / Spring Boot 3 REST API
- **Frontend** – TypeScript / React (Vite)

---

## Project structure

```
harano/
├── backend/          # Java Spring Boot REST API
│   ├── pom.xml
│   └── src/
│       ├── main/java/com/harano/
│       │   ├── HaranoApplication.java
│       │   ├── GlobalExceptionHandler.java   # Centralised error handling
│       │   ├── skill/          # Skill CRUD + registry
│       │   │   ├── Skill.java
│       │   │   ├── SkillParameter.java
│       │   │   ├── SkillService.java
│       │   │   └── SkillController.java
│       │   └── mcp/            # MCP marketplace
│       │       ├── MCPServer.java
│       │       ├── MCPServerStatus.java
│       │       ├── MCPMarketService.java
│       │       └── MCPMarketController.java
│       └── test/java/com/harano/
│           ├── skill/SkillServiceTest.java
│           └── mcp/MCPMarketServiceTest.java
└── frontend/         # TypeScript / React (Vite)
    ├── package.json
    ├── vite.config.ts
    └── src/
        ├── types/        # skill.ts, mcp.ts
        ├── api/          # skillApi.ts, mcpApi.ts
        ├── utils/        # errorUtils.ts (shared error handling)
        ├── components/   # SkillList.tsx, MCPMarket.tsx
        ├── App.tsx
        └── main.tsx
```

---

## Backend

### Run

```bash
cd backend
mvn spring-boot:run
# API available at http://localhost:8080
```

### Test

```bash
cd backend
mvn test
```

### REST API

#### Skills  `GET /api/skills`

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/skills` | List all skills (optional `?q=` search) |
| GET | `/api/skills/{id}` | Get skill by id |
| POST | `/api/skills` | Register a new skill |
| PUT | `/api/skills/{id}` | Update a skill |
| DELETE | `/api/skills/{id}` | Delete a skill |

#### MCP Market  `GET /api/mcp`

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/mcp` | List all servers (optional `?q=` search, `?availableOnly=true`) |
| GET | `/api/mcp/{id}` | Get server by id |
| POST | `/api/mcp` | Publish a server |
| DELETE | `/api/mcp/{id}` | Unpublish a server |
| GET | `/api/mcp/installed` | List installed servers |
| POST | `/api/mcp/{id}/install` | Install a server |
| DELETE | `/api/mcp/{id}/install` | Uninstall a server |

---

## Frontend

### Run (development)

```bash
cd frontend
npm install
npm run dev
# UI available at http://localhost:5173
```

The Vite dev server proxies `/api/*` requests to the Spring Boot backend at `http://localhost:8080`.

### Test

```bash
cd frontend
npm test
```

### Build

```bash
cd frontend
npm run build
```