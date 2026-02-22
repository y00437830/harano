# harano

**harano** is a Python library that provides two core building blocks for AI agent platforms:

1. **Skill system** – a typed, registry-backed framework for defining and executing reusable AI capabilities.
2. **MCP Market** – a lightweight marketplace for managing [Model Context Protocol (MCP)](https://modelcontextprotocol.io) servers.

---

## Installation

```bash
pip install harano
```

---

## Skill system

A **Skill** is a self-contained, named unit of computation.  Each skill declares its input parameters via `SkillMetadata` and carries out work in `execute()`.

```python
from harano.skill import Skill, SkillMetadata, SkillParameter, SkillRegistry
from harano.skill.models import ParameterType

# 1. Define a skill
class GreetSkill(Skill):
    metadata = SkillMetadata(
        name="greet",
        description="Returns a greeting message.",
        parameters=[
            SkillParameter(name="name", type=ParameterType.STRING),
        ],
    )

    def execute(self, **kwargs):
        return f"Hello, {kwargs['name']}!"

# 2. Register it
registry = SkillRegistry()
registry.register(GreetSkill)   # or use as a decorator: @registry.register

# 3. Look up and run
skill = registry.get("greet")()
print(skill.execute(name="World"))   # Hello, World!
```

### SkillRegistry API

| Method | Description |
|---|---|
| `register(skill_class)` | Register a `Skill` subclass (usable as a decorator). |
| `get(name)` | Return the class registered under `name`. |
| `unregister(name)` | Remove a skill from the registry. |
| `list_skills()` | Sorted list of registered skill names. |

---

## MCP Market

The MCP Market lets you publish, browse, install, and uninstall MCP servers.

```python
from harano.mcp_market import MCPMarket, MCPServer

market = MCPMarket()

# Publish servers to the catalog
market.publish(MCPServer(id="weather", name="Weather API", tags=["weather", "api"]))
market.publish(MCPServer(id="code-fmt", name="Code Formatter", tags=["dev"]))

# Browse
print([s.id for s in market.list_available()])   # ['code-fmt', 'weather']
print([s.id for s in market.search("weather")])  # ['weather']

# Install
market.install("weather")
print(market.is_installed("weather"))             # True

# Uninstall
market.uninstall("weather")
```

### MCPMarket API

| Method | Description |
|---|---|
| `publish(server)` | Add a server to the marketplace catalog. |
| `unpublish(server_id)` | Remove a server (also uninstalls if installed). |
| `list_available()` | All catalog entries not yet installed. |
| `search(query)` | Free-text search across name, description, and tags. |
| `install(server_id)` | Install a catalog server locally. |
| `uninstall(server_id)` | Uninstall a previously installed server. |
| `list_installed()` | All currently installed servers. |
| `is_installed(server_id)` | Check installation status. |
| `get_installed(server_id)` | Get the installed `MCPServer` entry. |

---

## Development

```bash
pip install -e ".[dev]"
pytest
```
