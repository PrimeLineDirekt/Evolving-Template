# Evolving MCP Server

MCP (Model Context Protocol) Server that exposes the Evolving knowledge management system to Claude Desktop.

## Overview

The MCP Server acts as a bridge between Claude Desktop and your Evolving knowledge system, providing **9 tools** for complete idea and knowledge management workflows - **without needing an API key!**

**Key Feature**: Claude Desktop uses its own intelligence to analyze ideas (using your existing subscription), eliminating the need for separate API calls.

---

## Quick Start

### 1. Install Dependencies

```bash
pip3 install mcp anthropic
```

### 2. Configure Claude Desktop

**macOS**: Edit `~/Library/Application Support/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "evolving-knowledge": {
      "command": "python3",
      "args": [
        "/absolute/path/to/your/Evolving/mcp_server/server.py"
      ],
      "env": {
        "PYTHONPATH": "/absolute/path/to/your/Evolving"
      }
    }
  }
}
```

**Note**: No `ANTHROPIC_API_KEY` needed! Claude Desktop provides analysis directly.

### 3. Restart Claude Desktop

Completely quit and restart Claude Desktop. The MCP server will load automatically.

---

## Available Tools (9)

### READ Tools (4)

**`idea_list`** - List all ideas with optional filtering
```
Parameters:
- filter_status: draft|active|paused|completed|archived
- filter_category: Category name
- min_potential: Minimum score 1-10

Example:
"Show me all active ideas"
"List ideas with potential above 7"
```

**`knowledge_search`** - Search entire knowledge base
```
Parameters:
- query: Search keywords
- max_results: Maximum results (default: 10)

Example:
"Search for 'migration' in my knowledge base"
```

**`project_list`** - List all projects
```
Example:
"Show me all my projects"
```

**`read_file`** - Read specific knowledge file
```
Parameters:
- path: Relative path from knowledge/ directory

Example:
"Read the project README"
```

### WRITE Tools (5)

**`idea_create`** - Create new idea with analysis
```
Parameters:
- title: Idea title (required)
- description: Detailed description (required)
- category: e.g., "business/saas" (optional, Claude provides)
- potential: Score 1-10 (optional, Claude provides)
- tags: Array of tags (optional, Claude provides)
- required_skills: Array of skills (optional, Claude provides)
- monetization: direct|indirect|none (optional, Claude provides)
- effort: low|medium|high (optional, Claude provides)
- analysis_text: Analysis (optional, Claude provides)
- next_steps: Array of action items (optional, Claude provides)

Example:
"Create idea: AI Recipe Generator - platform that generates
personalized recipes based on available ingredients"

Claude Desktop automatically analyzes and provides category,
potential score, tags, skills, etc. - no API key needed!
```

**`idea_update`** - Update existing idea
```
Parameters:
- idea_id: ID like "idea-0001" (required)
- status: New status (optional)
- tags: Tags to add (optional)
- related_ideas: Related idea IDs (optional)
- related_projects: Related project names (optional)
- session_note: Session summary (optional)
- session_type: brainstorming|validation|planning|implementation (optional)
- insights: Array of insights (optional)
- decisions: Array of decisions (optional)
- next_steps: Array of action items (optional)

Example:
"Update idea-0001:
- Status: active
- Session note: MVP plan completed
- Insights: Users need visa status tracking
- Next steps: Research APIs, Design schema"
```

**`prompt_add`** - Save prompts from sessions
```
Parameters:
- name: Prompt name (required)
- content: Prompt content (required)
- category: frameworks|research-agents|skills|patterns (required)
- description: What it does (optional)
- tags: Array of tags (optional)

Example:
"Save this prompt as a framework: [your prompt]"
```

**`learning_add`** - Document insights
```
Parameters:
- title: Learning title (required)
- context: Where learned (required)
- insight: The actual insight (required)
- tags: Array of tags (optional)
- confidence: 0-100 (default: 85)

Example:
"Document this learning:
Title: MCP servers auto-start with Claude Desktop
Context: Building Evolving MCP integration
Insight: No manual startup needed, completely automatic"
```

**`resource_add`** - Save links and tools
```
Parameters:
- title: Resource title (required)
- url: Resource URL (required)
- description: What it is (required)
- category: tool|link|inspiration|reference|learning-material (optional)
- tags: Array of tags (optional)

Example:
"Save this resource:
Title: Anthropic MCP Docs
URL: https://modelcontextprotocol.io
Description: Official MCP protocol documentation"
```

---

## Architecture

```
Claude Desktop (Your Subscription)
    ↓
MCP Server (stdio connection)
    ↓
evolving_core/ (Shared Business Logic)
    ├── managers/
    │   ├── IdeaManager - Idea CRUD operations
    │   └── KnowledgeManager - Knowledge base operations
    ├── utils/
    │   ├── FileOps - Safe file operations with backups
    │   ├── JSONDatabase - JSON operations
    │   └── AIClient - Legacy API client (optional)
    └── models/
        └── Idea - Data model
    ↓
Local File System (ideas/, knowledge/)
```

### Key Design Decisions

**1. Claude Desktop Provides Analysis**
- Claude Desktop analyzes ideas directly using its own intelligence
- No separate API calls needed
- Uses your existing Claude Desktop subscription
- Faster and more cost-effective

**2. Shared Core Logic**
- `evolving_core/` package used by both:
  - Claude Code (slash commands)
  - Claude Desktop (MCP tools)
- Single source of truth for all operations
- Consistent behavior across interfaces

**3. Safe Operations**
- Atomic writes (temp file → rename)
- Automatic backups with timestamps
- Path validation (no directory traversal)
- Duplicate prevention

---

## Testing

### Local Server Test

```bash
cd /path/to/your/Evolving
python3 mcp_server/server.py
```

Should start without errors. Press Ctrl+C to stop.

### Test IdeaManager

```bash
python3 -c "
from evolving_core.managers.idea_manager import IdeaManager
from pathlib import Path

# No API key needed!
manager = IdeaManager(Path('.'), ai_client=None)
print(f'Ideas: {manager.count()}')
print(f'Categories: {manager.get_categories()}')
"
```

### Test in Claude Desktop

After restarting Claude Desktop:

```
"Show me all my ideas"
"Create idea: Test Idea - just testing the MCP server"
"Update idea-0001 with status: active"
```

---

## Troubleshooting

### Server doesn't appear in Claude Desktop

**Check 1: Config File Location**
```bash
cat ~/Library/Application\ Support/Claude/claude_desktop_config.json
```

macOS uses `~/Library/Application Support/Claude/`, NOT `~/.config/Claude/`

**Check 2: Restart Required**
After changing config, completely quit Claude Desktop (Cmd+Q) and restart.

**Check 3: Server Status**
Look for 🔌 icon in Claude Desktop (bottom right) - should show connected.

**Check 4: Python Dependencies**
```bash
pip3 list | grep mcp
```

Should show `mcp >= 0.9.0`

### Import Errors

```bash
# Ensure PYTHONPATH is set
export PYTHONPATH=/path/to/your/Evolving
python3 -c "from evolving_core.managers.idea_manager import IdeaManager; print('OK')"
```

### Permission Errors

```bash
chmod +x /path/to/your/Evolving/mcp_server/server.py
```

---

## Development Status

**Version**: 2.0.0
**Status**: ✅ Production Ready

### Completed Phases

- ✅ Phase 1: MCP Server Setup & idea_list
- ✅ Phase 2: Read Operations (knowledge_search, project_list, read_file)
- ✅ Phase 2.5: Write Operations (prompt_add, learning_add, resource_add)
- ✅ Phase 3: idea_update - Complete workflow cycle
- ✅ API Key Removal - Claude Desktop provides analysis

### All 9 Tools Implemented

- **READ**: idea_list, knowledge_search, project_list, read_file
- **WRITE**: idea_create, idea_update, prompt_add, learning_add, resource_add

---

## Usage Examples

### Complete Idea Lifecycle

```
1. CREATE
"Create idea: AI Recipe Generator
Description: Platform that generates personalized recipes..."

→ Claude Desktop analyzes and provides category, potential, tags, etc.
→ Idea saved as idea-0001

2. UPDATE (Session 1)
"Update idea-0001:
- Status: active
- Session note: Researched recipe APIs
- Insights: AllRecipes API has good coverage
- Next steps: Design database schema"

3. UPDATE (Session 2)
"Update idea-0001:
- Session note: Built MVP prototype
- Decisions: Use PostgreSQL for recipe storage
- Next steps: Add user authentication, Deploy to Vercel"

4. COMPLETE
"Update idea-0001 with status: completed"
```

### Knowledge Management

```
"Save this prompt I developed as a framework: [your prompt]"

"Document this learning:
I discovered that MCP servers are stateless - each tool call
is independent"

"Save this resource:
Title: Recipe API Docs
URL: https://example.com/api
Description: Comprehensive recipe database API"
```

---

## Links

**Setup Guide**: [../SETUP_MCP.md](../SETUP_MCP.md)
**Workflow Guide**: [../knowledge/personal/mcp-workflow.md](../knowledge/personal/mcp-workflow.md)
**Core Logic**: [../evolving_core/README.md](../evolving_core/README.md)
**Main README**: [../README.md](../README.md)

---

## Version History

**2.0.0** (2025-11-22)
- All 9 tools implemented
- API key removed - Claude Desktop provides analysis
- Complete idea lifecycle support
- Production ready

**1.0.0** (2024-11-22)
- Initial proof of concept
- idea_list tool only
