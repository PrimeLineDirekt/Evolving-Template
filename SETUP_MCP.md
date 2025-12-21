# MCP Server Setup Guide

## No API Key Required!

**Important:** You don't need a separate Anthropic API key!

Claude Desktop uses your existing subscription and analyzes ideas directly.
No extra costs, no double payment.

### Activate Claude Desktop

**1. Restart Claude Desktop completely**
- Quit Claude Desktop fully
- Restart
- The MCP server loads automatically on startup

**2. Test the MCP Tool**

In Claude Desktop you can now ask:
```
"Show me all my ideas"
"List all ideas with high potential"
"What categories do I have?"
"Show me active ideas"
```

**3. Check Server Status**

Claude Desktop shows at the bottom right (plug symbol) if MCP servers are connected.

---

## Setup

### 1. Configure Claude Desktop

Edit Claude Desktop config:

**macOS:**
```bash
nano ~/Library/Application\ Support/Claude/claude_desktop_config.json
```

**Windows:**
```
%APPDATA%\Claude\claude_desktop_config.json
```

### 2. Add MCP Server Configuration

```json
{
  "mcpServers": {
    "evolving-knowledge": {
      "command": "python3",
      "args": ["/path/to/your/evolving/mcp_server/server.py"],
      "env": {
        "PYTHONPATH": "/path/to/your/evolving"
      }
    }
  }
}
```

Replace `/path/to/your/evolving` with your actual Evolving directory path.

**No ANTHROPIC_API_KEY required!** Claude Desktop uses your subscription.

### 3. Install Python Dependencies

```bash
cd /path/to/your/evolving
pip3 install -r requirements.txt
```

Or install individually:
```bash
pip3 install mcp>=0.9.0
```

---

## Troubleshooting

### Server not appearing in Claude Desktop

**Check 1: Config File**
```bash
cat ~/Library/Application\ Support/Claude/claude_desktop_config.json
```

Should show:
```json
{
  "mcpServers": {
    "evolving-knowledge": {
      "command": "python3",
      "args": ["/path/to/your/evolving/mcp_server/server.py"],
      "env": {
        "PYTHONPATH": "/path/to/your/evolving"
      }
    }
  }
}
```

**Check 2: Python Dependencies**
```bash
pip3 list | grep mcp
```

Should show:
- mcp >= 0.9.0

**Note:** The `anthropic` package is only needed for legacy AI-API calls (optional).

**Check 3: Test Server Manually**
```bash
cd /path/to/your/evolving
python3 mcp_server/server.py
```

If errors: See error message and fix imports/dependencies.

**Check 4: Claude Desktop Logs**

Find logs (macOS):
```bash
# Claude Desktop logs location varies
# Check Console.app → Filter: "Claude"
```

### Import Errors

```bash
# Make sure PYTHONPATH is correct
export PYTHONPATH=/path/to/your/evolving
python3 -c "from evolving_core.managers.idea_manager import IdeaManager; print('OK')"
```

### Permission Errors

```bash
chmod +x /path/to/your/evolving/mcp_server/server.py
```

---

## Local Testing (Optional)

If you want to test the MCP server outside of Claude Desktop:

**Test IdeaManager**
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

---

## Security Notes

### No API Keys in Repo

- **No API keys required!** Claude Desktop uses your subscription
- **.env files**: In .gitignore (are NOT committed)
- **Backups**: Automatically created with timestamps
- **Config**: Outside of Git repo

### NEVER commit:

- credentials.json
- *.key, *.pem files
- Personal data

All these patterns are in `.gitignore` and are automatically ignored.

---

## Available Tools

**Read Operations (4):**
- `idea_list` - List ideas with filters
- `knowledge_search` - Search knowledge base
- `project_list` - List all projects
- `read_file` - Read specific files

**Write Operations (5):**
- `idea_create` - Create new idea (Claude analyzes directly!)
- `idea_update` - Update idea, document sessions
- `prompt_add` - Save prompts from sessions
- `learning_add` - Document insights
- `resource_add` - Save links & tools

---

## Status: Complete!

**All phases completed:**
- Phase 1: MCP Server Setup
- Phase 2: Read Operations
- Phase 2.5: Write Operations
- Phase 3: idea_update - Complete workflow
- API Key Removal - Uses Claude Desktop subscription

**Next**: Restart Claude Desktop & Test the tools!
