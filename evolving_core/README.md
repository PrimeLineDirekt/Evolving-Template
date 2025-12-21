# Evolving Core - Shared Business Logic

Shared business logic package used by both Claude Code slash commands and MCP Server.

## Purpose

This package provides the **single source of truth** for all knowledge management operations, ensuring consistency across different interfaces:

- **Claude Code** (`.claude/commands/*.md`) - Slash command interface
- **Claude Desktop** (`mcp_server/server.py`) - MCP tool interface

Both interfaces use the exact same business logic, ensuring consistent behavior and data integrity.

---

## Architecture

```
evolving_core/
├── managers/          # Domain-specific business logic
│   ├── idea_manager.py        # Idea CRUD operations ✅
│   └── knowledge_manager.py   # Knowledge base operations ✅
│
├── utils/             # Shared utilities
│   ├── file_ops.py    # Safe file operations with backups ✅
│   ├── json_db.py     # JSON database operations ✅
│   └── ai_client.py   # Claude API client (optional) ✅
│
└── models/            # Data models
    └── idea.py        # Idea data model ✅
```

---

## Design Principles

### 1. Safety First

All write operations use:
- **Atomic writes** - Write to temp file, then rename (prevents corruption)
- **Automatic backups** - Timestamped backups before modifications
- **Validation** - Data validation before writes
- **Path validation** - Prevents directory traversal attacks

### 2. Backward Compatibility

Supports both index.json formats:
- Legacy: `[{idea}, {idea}]` (array)
- Current: `{"ideas": [{idea}], "stats": {...}}` (object with metadata)

### 3. Clear Separation of Concerns

- **Managers** - Business logic, orchestration, validation
- **Utils** - Reusable low-level operations
- **Models** - Data structures and serialization

### 4. Optional AI Integration

- **No API key required** - Claude Desktop provides analysis directly
- **AIClient optional** - Only for legacy API-based analysis
- **Graceful degradation** - Works without AI client

---

## Usage

### IdeaManager

```python
from evolving_core.managers.idea_manager import IdeaManager
from pathlib import Path

manager = IdeaManager(Path('/path/to/Evolving'), ai_client=None)

# List all ideas
ideas = manager.list()

# Filter ideas
active_ideas = manager.list(filter_status="active")
high_potential = manager.list(min_potential=8)
business_ideas = manager.list(filter_category="business/saas")

# Get specific idea
idea = manager.get("idea-0001")

# Get statistics
stats = manager.count()
# {'total': 10, 'draft': 3, 'active': 5, 'paused': 1, 'completed': 1, 'archived': 0}

# Get categories
categories = manager.get_categories()
# ['business/saas', 'tech/automation', 'content/creator']

# Create idea (with external analysis from Claude Desktop)
idea = manager.create(
    title="AI Recipe Generator",
    description="Platform that generates personalized recipes...",
    category="business/saas",           # Provided by Claude
    potential=8,                        # Provided by Claude
    tags=["ai", "food", "personalization"],  # Provided by Claude
    required_skills=["Python", "API Development"],
    monetization="direct",
    effort="medium",
    analysis_text="Strong market need...",
    next_steps=["Research APIs", "Design schema"]
)

# Update idea
idea = manager.update(
    idea_id="idea-0001",
    status="active",
    session_note="Completed MVP planning",
    session_type="planning",
    insights=["Users need real-time tracking"],
    decisions=["Use PostgreSQL for data storage"],
    next_steps=["Build API", "Design frontend"]
)
```

### KnowledgeManager

```python
from evolving_core.managers.knowledge_manager import KnowledgeManager
from pathlib import Path

manager = KnowledgeManager(Path('.'))

# Search knowledge base
results = manager.search("migration", max_results=10)
for result in results:
    print(f"{result['title']} ({result['score']} matches)")
    print(f"  Path: {result['path']}")
    print(f"  Type: {result['type']}")
    for excerpt in result['excerpts']:
        print(f"  ...{excerpt}...")

# List projects
projects = manager.list_projects()
for project in projects:
    print(f"{project['name']}: {project.get('title', 'No title')}")

# Read specific file
file_data = manager.read_file("projects/your-project/README.md")
print(file_data['content'])

# Add prompt
result = manager.add_prompt(
    name="API Response Parser",
    content="You are an expert at parsing API responses...",
    category="skills",
    tags=["api", "parsing", "json"],
    description="Parses and validates API responses"
)

# Add learning
result = manager.add_learning(
    title="MCP servers are stateless",
    context="Building Evolving MCP integration",
    insight="Each tool call is independent, no session state",
    tags=["mcp", "architecture"],
    confidence=95
)

# Add resource
result = manager.add_resource(
    title="Anthropic MCP Docs",
    url="https://modelcontextprotocol.io",
    description="Official MCP protocol documentation",
    category="reference",
    tags=["mcp", "documentation"]
)
```

### File Operations

```python
from evolving_core.utils.file_ops import FileOps
from pathlib import Path

file_ops = FileOps(Path('.'))

# Read file
content = file_ops.read_file("ideas/category/idea-001.md")

# Write file (with automatic backup)
file_ops.write_file("ideas/category/idea-001.md", content, backup=True)
# Creates backup: ideas/category/idea-001.md.backup.YYYYMMDD_HHMMSS

# Check existence
exists = file_ops.file_exists("ideas/index.json")

# Ensure directory
path = file_ops.ensure_dir("ideas/new-category")
```

### JSON Database

```python
from evolving_core.utils.json_db import JSONDatabase
from pathlib import Path

db = JSONDatabase(Path('.'))

# Read JSON with default
data = db.read_json("ideas/index.json", default={"ideas": []})

# Write JSON (with backup)
db.write_json("ideas/index.json", data, backup=True)
```

### AI Client (Optional)

```python
from evolving_core.utils.ai_client import AIClient

# Only needed for legacy API-based analysis
# Claude Desktop provides analysis directly, so this is optional

try:
    ai_client = AIClient()  # Requires ANTHROPIC_API_KEY env var
    analysis = ai_client.analyze_idea(
        title="AI Recipe Generator",
        description="Platform for personalized recipes...",
        existing_categories=["business/saas", "tech/automation"]
    )
    # Returns: category, potential, tags, skills, monetization, effort, analysis_text, next_steps
except ValueError:
    # No API key - use Claude Desktop for analysis instead
    ai_client = None
```

---

## Implementation Details

### IdeaManager.create()

**Supports three modes:**

1. **With external analysis** (Claude Desktop provides)
```python
idea = manager.create(
    title="...",
    description="...",
    category="business/saas",  # Claude provides
    potential=8,               # Claude provides
    # ... other analysis fields
    use_ai_analysis=False      # Default
)
```

2. **With AI API analysis** (Legacy, requires API key)
```python
idea = manager.create(
    title="...",
    description="...",
    use_ai_analysis=True  # Makes API call
)
```

3. **With defaults** (No analysis)
```python
idea = manager.create(
    title="...",
    description="...",
    use_ai_analysis=False  # No AI, uses defaults
)
```

### IdeaManager.update()

**Flexible parameter-based updates:**

```python
idea = manager.update(
    idea_id="idea-0001",

    # Optional: Metadata updates
    status="active",
    tags=["new-tag"],  # Appends to existing
    related_ideas=["idea-0002"],
    related_projects=[],

    # Optional: Session documentation
    session_note="Summary of work done",
    session_type="brainstorming",
    insights=["Key insight 1", "Key insight 2"],
    decisions=["Decision 1", "Decision 2"],
    next_steps=["Step 1", "Step 2"]
)
```

**What it does:**
- Updates frontmatter fields
- Appends timestamped session entry to Fortschritt section
- Updates `updated` field automatically
- Synchronizes index.json
- Creates automatic backup

---

## Development Status

**Version**: 2.0.0
**Status**: ✅ Production Ready

### Completed

- [x] Package structure
- [x] FileOps utility (atomic writes, backups)
- [x] JSONDatabase utility
- [x] Idea data model
- [x] IdeaManager (list, get, count, get_categories, create, update)
- [x] KnowledgeManager (search, list_projects, read_file, add_prompt, add_learning, add_resource)
- [x] AIClient (optional, for legacy API analysis)
- [x] Complete MCP integration
- [x] API-key-free operation (Claude Desktop provides analysis)

### Future Enhancements (Optional)

- [ ] ConnectionEngine - Automatic synergy detection between ideas
- [ ] InboxProcessor - Batch processing automation
- [ ] SessionManager - Stateful multi-turn workflows
- [ ] SearchEngine - Semantic search with embeddings
- [ ] Complete test coverage (pytest)

---

## Testing

### Quick Functionality Test

```bash
python3 -c "
from evolving_core.managers.idea_manager import IdeaManager
from evolving_core.managers.knowledge_manager import KnowledgeManager
from pathlib import Path

# No API key needed!
idea_mgr = IdeaManager(Path('.'), ai_client=None)
know_mgr = KnowledgeManager(Path('.'))

print(f'Ideas: {idea_mgr.count()}')
print(f'Categories: {idea_mgr.get_categories()}')
print(f'Projects: {len(know_mgr.list_projects())}')
"
```

### Test IdeaManager.create()

```bash
python3 -c "
from evolving_core.managers.idea_manager import IdeaManager
from pathlib import Path

manager = IdeaManager(Path('.'), ai_client=None)

# Create with analysis data (Claude Desktop mode)
idea = manager.create(
    title='Test Idea',
    description='Testing create() method',
    category='test/validation',
    potential=7,
    tags=['test'],
    use_ai_analysis=False
)

print(f'Created: {idea.id} in {idea.category}')
"
```

### Test IdeaManager.update()

```bash
python3 -c "
from evolving_core.managers.idea_manager import IdeaManager
from pathlib import Path

manager = IdeaManager(Path('.'), ai_client=None)

# Update with session info
idea = manager.update(
    idea_id='idea-0001',
    status='active',
    session_note='Testing update() method',
    insights=['Update works correctly']
)

print(f'Updated: {idea.id} - Status: {idea.status}')
"
```

---

## Version History

**2.0.0** (2025-11-22)
- Added IdeaManager.update() with session tracking
- Added KnowledgeManager with full CRUD operations
- Added AIClient (optional)
- Removed API key requirement (Claude Desktop provides analysis)
- Complete MCP Server integration
- Production ready

**1.0.0** (2024-11-22)
- Initial implementation
- IdeaManager with list, get, count operations
- FileOps and JSONDatabase utilities
- Idea data model

---

## Links

**MCP Server**: [../mcp_server/README.md](../mcp_server/README.md)
**Main README**: [../README.md](../README.md)
**Setup Guide**: [../SETUP_MCP.md](../SETUP_MCP.md)
