---
title: "MCP Server Reference"
type: reference
category: index
domain: [mcp, tools, integrations]
source: modelcontextprotocol/servers + awesome-claude
source_date: 2025-12-13
completeness: complete
tags: [mcp, servers, tools, integrations, automation]
---

# MCP Server Reference

Model Context Protocol (MCP) servers extend Claude Code with external tools and data sources.

## Quick Setup

### Configuration Location

```
~/.mcp.json           # User-level (all projects)
.mcp.json             # Project-level (repo-specific)
```

### Configuration Format

```json
{
  "mcpServers": {
    "server-name": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-name"],
      "env": {
        "API_KEY": "your-key"
      }
    }
  }
}
```

---

## Priority 1: Essential Servers

| Server | Purpose | Evolving Use Case |
|--------|---------|-------------------|
| [github](#github) | GitHub API integration | Repo management, PR automation |
| [filesystem](#filesystem) | Enhanced file operations | Large file handling, batch ops |
| [sequential-thinking](#sequential-thinking) | Structured reasoning | Complex analysis chains |
| [fetch](#fetch) | Web content extraction | Research, data gathering |
| [memory](#memory) | Persistent knowledge graph | Cross-session context |

---

## Priority 2: Development Servers

| Server | Purpose | Use Case |
|--------|---------|----------|
| [postgres](#postgres) | Database access | Direct DB queries |
| [git](#git) | Git operations | Advanced version control |
| [docker](#docker) | Container management | Dev environments |
| [firebase](#firebase) | Firebase platform | Backend operations |

---

## Priority 3: Specialized Servers

| Server | Purpose | Use Case |
|--------|---------|----------|
| [brave-search](#brave-search) | Web search | Research alternative |
| [slack](#slack) | Communication | Notifications |
| [notion](#notion) | External KB | Note sync |

---

## Server Details

### github

**Status**: Configured in `.mcp.json`

GitHub API integration for repository management.

**Installation**:
```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "<your-token>"
      }
    }
  }
}
```

**Capabilities**:
- Create/manage repositories
- Create/review pull requests
- Search code and issues
- Manage branches and releases
- Read repository contents

**Token Permissions** (minimum):
- `repo` - Full repository access
- `read:org` - Organization membership (optional)

**Example Usage**:
```
"Search for authentication implementations in my repos"
"Create a PR from feature/auth to main"
"List open issues with 'bug' label"
```

---

### filesystem

**Purpose**: Enhanced file operations beyond standard Read/Write tools.

**Installation**:
```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/allowed/path"]
    }
  }
}
```

**Capabilities**:
- Read/write files
- Create/list directories
- Move/copy files
- Search files by pattern
- Get file metadata

**Security**: Paths must be explicitly allowed in args.

**Use Cases**:
- Batch file operations
- Large file handling
- Cross-directory operations

---

### sequential-thinking

**Status**: Configured in `.mcp.json`

Dynamic problem-solving through structured thought sequences.

**Installation**:
```json
{
  "mcpServers": {
    "sequential-thinking": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-sequential-thinking"]
    }
  }
}
```

**Capabilities**:
- Break complex problems into steps
- Track reasoning chains
- Revise thoughts based on new info
- Branch exploration paths

**Use Cases**:
- Complex debugging
- Architecture decisions
- Multi-step analysis
- Research synthesis

---

### fetch

**Purpose**: Web content extraction optimized for LLM consumption.

**Installation**:
```json
{
  "mcpServers": {
    "fetch": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-fetch"]
    }
  }
}
```

**Capabilities**:
- Fetch web pages
- Convert HTML to markdown
- Extract structured data
- Handle redirects

**Use Cases**:
- Documentation research
- API exploration
- Content aggregation

---

### memory

**Purpose**: Knowledge graph-based persistent memory.

**Installation**:
```json
{
  "mcpServers": {
    "memory": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-memory"]
    }
  }
}
```

**Capabilities**:
- Store entities with observations
- Create relations between entities
- Query by entity or relation type
- Persistent across sessions

**Schema**:
```
Entity: { name, entityType, observations[] }
Relation: { from, to, relationType }
```

**Use Cases**:
- Project context persistence
- Relationship tracking
- Cross-session memory

---

### postgres

**Purpose**: Read-only PostgreSQL database access.

**Installation**:
```json
{
  "mcpServers": {
    "postgres": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-postgres",
        "postgresql://user:pass@host:5432/db"
      ]
    }
  }
}
```

**Capabilities**:
- Execute read-only queries
- Inspect schema
- List tables and columns
- Query relationships

**Security**: Read-only by design. Use restricted DB user.

---

### git

**Purpose**: Advanced Git repository operations.

**Installation**:
```json
{
  "mcpServers": {
    "git": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-git", "--repository", "/path/to/repo"]
    }
  }
}
```

**Capabilities**:
- Read repository state
- Search commits
- Analyze diffs
- Browse history

---

### brave-search

**Purpose**: Web search via Brave Search API.

**Installation**:
```json
{
  "mcpServers": {
    "brave-search": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-brave-search"],
      "env": {
        "BRAVE_API_KEY": "<your-key>"
      }
    }
  }
}
```

**Capabilities**:
- Web search
- News search
- Local search (optional)


---

## Current Evolving Configuration

File: `.mcp.json`

```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "<token>"
      }
    },
    "sequential-thinking": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-sequential-thinking"]
    },
    "context7": {
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp"]
    }
  }
}
```

---

## Adding New Servers

1. **Find server** on awesome-mcp-servers
2. **Install**: Usually `npx -y @scope/server-name`
3. **Configure** in `.mcp.json`
4. **Restart** Claude Code to load

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Server not loading | Check `claude mcp list` for errors |
| Permission denied | Verify API keys and tokens |
| Tool not available | Restart Claude Code after config change |
| Timeout errors | Increase timeout in server config |

---

## Related

- [claude-flow Patterns](../claude-flow/index.md)
- [Agent Templates](../agent-templates/mega-template.md)
- [Claude Skills](../claude-skills/index.md)

---

**Source**: modelcontextprotocol/servers, awesome-mcp-servers
**Last Updated**: 2025-12-13
