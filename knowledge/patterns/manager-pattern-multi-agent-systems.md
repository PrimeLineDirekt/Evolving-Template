# Manager Pattern für Multi-Agent Systems

**Typ**: Infrastructure Pattern
**Domain**: Multi-Agent Systems, MCP Servers, System Architecture
**Quelle**: MCP Server v3.0.0 Implementation (2025-12-16)
**Complexity Score**: 6/10

---

## Problem

Bei Multi-Agent/Multi-Manager Systemen entsteht schnell Chaos:
- Jeder Manager hat eigene API-Konventionen
- Kein konsistentes Error Handling
- Schwierig zu testen (jede API anders)
- MCP Protocol Integration wird komplex (45+ Tools mit unterschiedlichen Interfaces)

**Beispiel-Symptome**:
- `AgentManager.list()` vs `GraphManager.get_all()` vs `SkillManager.fetch_skills()`
- Inkonsistente Return-Typen (dict vs Model vs JSON string)
- Unterschiedliches Error Handling (Exception vs None vs Error dict)

---

## Lösung

**Standardisiertes Manager Interface** mit klaren Konventionen:

### Core Interface

```python
class BaseManager:
    def __init__(self, base_path: Path):
        self.base_path = Path(base_path)
        self.db = JSONDatabase(base_path)  # JSON operations
        self.file_ops = FileOps(base_path)  # Atomic writes

    def list(self, filters: Optional[Dict] = None) -> List[Model]:
        """List all items, optionally filtered"""
        pass

    def get(self, id: str) -> Optional[Model]:
        """Get single item by ID"""
        pass

    def create(self, data: Dict[str, Any]) -> Model:
        """Create new item with atomic write + backup"""
        pass

    def update(self, id: str, updates: Dict[str, Any]) -> Model:
        """Update existing item with atomic write + backup"""
        pass

    def delete(self, id: str) -> bool:
        """Delete item (optional)"""
        pass
```

### Begleitende Model-Klasse

```python
@dataclass
class Model:
    field1: str
    field2: int
    # ... fields

    @classmethod
    def from_dict(cls, data: dict) -> 'Model':
        """Deserialize from JSON"""
        return cls(**data)

    def to_dict(self) -> dict:
        """Serialize to JSON"""
        return asdict(self)
```

### Shared Utilities

```python
class FileOps:
    """Atomic writes with automatic backups"""
    def write_json_atomic(self, path: Path, data: dict):
        temp = path.with_suffix('.tmp')
        temp.write_text(json.dumps(data, indent=2))
        if path.exists():
            shutil.copy(path, path.with_suffix('.backup'))
        temp.rename(path)  # Atomic!

class JSONDatabase:
    """Read-only JSON operations with caching"""
    def read(self, path: Path) -> dict:
        return json.loads(path.read_text())
```

---

## Implementation

### 1. Define Base Manager (Optional aber empfohlen)

```python
# evolving_core/managers/base_manager.py
class BaseManager:
    """Base class für alle Managers"""
    def __init__(self, base_path: Path):
        self.base_path = Path(base_path)
        self.db = JSONDatabase(base_path)
        self.file_ops = FileOps(base_path)
```

### 2. Implement Concrete Managers

```python
# evolving_core/managers/agent_manager.py
class AgentManager(BaseManager):
    def __init__(self, base_path: Path):
        super().__init__(base_path)
        self.agents_dir = base_path / ".claude" / "agents"
        self._agents_cache = None  # Lazy loading

    def list(self, filter_by_type: Optional[str] = None) -> List[Agent]:
        """List all agents, optionally filtered by type"""
        if self._agents_cache is None:
            self._load_agents()

        agents = list(self._agents_cache.values())
        if filter_by_type:
            agents = [a for a in agents if a.agent_type == filter_by_type]
        return agents

    def get(self, agent_name: str) -> Optional[Agent]:
        """Get agent by name (fuzzy matching)"""
        # Implementation with fuzzy matching
        pass

    # Keine create/update/delete - Agents sind file-based
```

### 3. MCP Protocol Integration wird trivial

```python
# mcp_server/server.py
Tool(
    name="agent_list",
    inputSchema={
        "type": "object",
        "properties": {
            "filter_by_type": {"type": "string", "enum": ["specialist", "research"]}
        }
    }
)

async def _handle_agent_list(self, arguments: dict):
    agents = self.agent_manager.list(
        filter_by_type=arguments.get("filter_by_type")
    )
    return [TextContent(
        type="text",
        text=json.dumps([a.to_dict() for a in agents], indent=2)
    )]
```

**Gleiche Struktur für alle 45 Tools** → Copy-Paste-freundlich!

---

## Benefits

### 1. Konsistenz
- **Developer Experience**: Einmal lernen, überall anwenden
- **Code Review**: Abweichungen fallen sofort auf
- **Testing**: Gleiche Test-Patterns für alle Managers

### 2. Maintainability
- **Refactoring**: Änderung am Interface propagiert automatisch
- **Documentation**: Ein Pattern zu dokumentieren, nicht 9
- **Onboarding**: Neuer Manager in <30min implementiert

### 3. Testability
```python
# Gleicher Test-Pattern für alle Managers
class TestAgentManager:
    def test_list(self, manager):
        agents = manager.list()
        assert isinstance(agents, list)
        assert all(isinstance(a, Agent) for a in agents)

    def test_get(self, manager):
        agent = manager.get("some-agent")
        assert agent is None or isinstance(agent, Agent)
```

### 4. Performance Optimization Points
- **Lazy Loading**: `_cache = None` → Load on first access
- **LRU Caching**: `@lru_cache(maxsize=100)` für hot paths
- **Indexes**: Separate Index-Dateien für schnelle Lookups

---

## When to Use

✅ **Use this pattern when:**
- Multi-Manager System (3+ Managers)
- MCP Server oder API mit vielen Endpoints
- Team mit mehreren Entwicklern
- Langfristiges Projekt (6+ Monate)

❌ **Skip this pattern when:**
- Single Manager System
- Proof-of-Concept / Throwaway Code
- Sehr unterschiedliche Datenquellen (SQL vs NoSQL vs API)

---

## Real-World Example: MCP Server v3.0.0

**9 Managers** alle mit identischem Interface:
1. `IdeaManager` - Ideas CRUD
2. `KnowledgeManager` - Knowledge Base
3. `DomainMemoryManager` - Project State
4. `ExperienceMemoryManager` - Solutions/Patterns
5. `GraphManager` - Knowledge Graph
6. `AgentManager` - 17 Agents
7. `ScenarioManager` - 3 Scenarios
8. `SkillManager` - 4 Skills
9. `BlueprintManager` - System Generation

**Result**:
- 45 MCP Tools in 8 Stunden implementiert
- 0 Interface-Fehler
- 39/39 Tests passing (alle Test-Fehler waren API-Mismatches im Test, nicht im Code)

**Code Reuse**:
```python
# Gleicher Handler-Pattern für ALLE Tools
async def _handle_X_list(self, arguments: dict):
    items = self.X_manager.list(arguments.get("filters"))
    return [TextContent(type="text", text=json.dumps(...))]
```

---

## Anti-Patterns

### ❌ Manager-Spezifische APIs
```python
# DON'T: Jeder Manager eigene Methoden
class AgentManager:
    def fetch_all_agents(self): ...
    def find_agent_by_name(self): ...

class SkillManager:
    def get_skills_list(self): ...
    def lookup_skill(self): ...
```

### ❌ Inkonsistente Return Types
```python
# DON'T: Mixed return types
def list(self) -> dict:  # Manager A
def list(self) -> List[dict]:  # Manager B
def list(self) -> str:  # Manager C (JSON string)
```

### ❌ Kein Error Handling Standard
```python
# DON'T: Unterschiedliches Error Handling
def get(self, id):
    if not found:
        raise ValueError  # Manager A
        return None  # Manager B
        return {"error": "..."}  # Manager C
```

---

## Variations

### File-Based Managers (kein create/update/delete)
Wenn Daten file-based sind (z.B. Agents in `.md` Files):
- `list()` + `get()` implementieren
- Keine `create()`/`update()`/`delete()`
- Dokumentieren: "Read-only Manager"

### Read-Only Managers
Wenn keine Writes erlaubt:
- Nur `list()` + `get()`
- `ValidationManager`, `MetadataManager`, etc.

### Async Managers
Bei I/O-bound Operations:
```python
class AsyncManager:
    async def list(self) -> List[Model]:
        data = await self.db.read_async(...)
        return [Model.from_dict(d) for d in data]
```

---

## Related Patterns

- Repository Pattern - Similar concept for DB access
- [Atomic Operations Pattern](atomic-operations-pattern.md) - Für write safety
- [Lazy Loading Pattern](lazy-loading-pattern.md) - Performance optimization
- [Dataclass Pattern](dataclass-serialization-pattern.md) - Model serialization

---

## References

- MCP Server v3.0.0 Implementation: 9 Managers, 45 Tools
- `evolving_core/managers/` - Reference Implementations
- `tests/integration/test_mcp_server_full.py` - Test Patterns

---

**Created**: 2025-12-16
**Category**: Infrastructure
**Tags**: #architecture #patterns #multi-agent #mcp #managers
