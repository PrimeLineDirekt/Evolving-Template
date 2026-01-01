# Meta-Component Creation Pattern

**Quelle**: davila7/claude-code-templates
**Extrahiert**: 2025-12-28
**Typ**: System Pattern

---

## Konzept

Framework für die Erstellung von Claude Code Komponenten (Agents, Commands, MCPs, Hooks).

---

## 1. Agent Creation Framework

### Standard Agent Format

```markdown
---
name: {domain}-{role}
description: Use this agent when [specific trigger]. Specializes in [2-3 areas]. Examples: <example>Context: [situation] user: '[request]' assistant: '[response]' <commentary>[reasoning]</commentary></example>
color: {color}
---

You are a {Domain} specialist focusing on {specific expertise}.

Your core expertise areas:
- **{Area 1}**: {capabilities}
- **{Area 2}**: {capabilities}
- **{Area 3}**: {capabilities}

## When to Use This Agent

Use this agent for:
- {Use case 1}
- {Use case 2}
- {Use case 3}

## {Domain}-Specific Sections

### {Category 1}
{Implementation guidance, code examples}

### {Category 2}
{Best practices, patterns}

Always provide {specific deliverables} when working in this domain.
```

### Agent Type Categories

| Typ | Beispiele | Color |
|-----|-----------|-------|
| **Technical** | Frontend, Backend, DevOps | blue, green, gray |
| **Domain** | Security, Performance, Testing | red, yellow, purple |
| **Industry** | E-Commerce, Healthcare, FinTech | custom |
| **Workflow** | Code Review, Architecture, Docs | varies |

### Color Coding System

| Domain | Colors |
|--------|--------|
| Frontend | blue, cyan, teal |
| Backend | green, emerald, lime |
| Security | red, crimson, rose |
| Performance | yellow, amber, orange |
| Testing | purple, violet, indigo |
| DevOps | gray, slate, stone |

---

## 2. Command Creation Framework

### Standard Command Format

```markdown
# {Action} {Target}

{Brief description} for $ARGUMENTS following {standards}.

## Task

I'll {action} including:
1. {Step 1}
2. {Step 2}
3. {Step 3}
4. {Step 4}

## Process

I'll follow these steps:
1. {Detailed step 1}
2. {Detailed step 2}
3. {Final step}

## {Category-Specific Sections}

### {Section 1}
- {Feature 1}
- {Feature 2}

## Best Practices

### {Practice Category}
- {Best practice 1}
- {Best practice 2}

I'll adapt to your project's {tools/framework}.
```

### Command Types

| Typ | Verben | Beispiele |
|-----|--------|-----------|
| **Generation** | generate, create, setup | `/generate-tests`, `/setup-ci` |
| **Analysis** | analyze, audit, check | `/analyze-security`, `/check-deps` |
| **Optimization** | optimize, improve, fix | `/optimize-bundle`, `/fix-imports` |
| **Automation** | run, deploy, migrate | `/run-tests`, `/deploy-staging` |

### Argument Handling

```markdown
## Configuration Options

- **--config**: Custom configuration file path
- **--output**: Output directory or format
- **--verbose**: Enable detailed logging
- **--dry-run**: Preview without execution
- **--force**: Override safety checks
```

---

## 3. MCP Integration Framework

### Standard MCP Format

```json
{
  "mcpServers": {
    "{Service} MCP": {
      "command": "npx",
      "args": [
        "-y",
        "mcp-{service}@latest"
      ],
      "env": {
        "API_KEY": "{required}",
        "BASE_URL": "https://api.service.com/v1",
        "TIMEOUT": "30000"
      }
    }
  }
}
```

### MCP Categories

| Typ | Beispiele | Key Env Vars |
|-----|-----------|--------------|
| **Database** | PostgreSQL, MySQL, Supabase | DATABASE_URL, MAX_CONNECTIONS |
| **API** | GitHub, Stripe, Slack | API_TOKEN, BASE_URL |
| **FileSystem** | Local, S3, GCS | ALLOWED_PATHS, MAX_FILE_SIZE |
| **Development** | CI/CD, Testing | varies |

### Database MCP Template

```json
{
  "mcpServers": {
    "PostgreSQL MCP": {
      "command": "npx",
      "args": ["-y", "postgresql-mcp@latest"],
      "env": {
        "DATABASE_URL": "postgresql://user:pass@host:5432/db",
        "MAX_CONNECTIONS": "10",
        "ENABLE_SSL": "true"
      }
    }
  }
}
```

### API MCP Template

```json
{
  "mcpServers": {
    "{Service} API MCP": {
      "command": "npx",
      "args": ["-y", "{service}-mcp@latest"],
      "env": {
        "API_TOKEN": "{token}",
        "RATE_LIMIT_REQUESTS": "5000",
        "RATE_LIMIT_WINDOW": "3600"
      }
    }
  }
}
```

---

## 4. Quality Checklist

### Agent Creation

- [ ] Expertise boundaries clearly defined
- [ ] 2-3 realistic examples in description
- [ ] Practical code examples included
- [ ] Limitations documented
- [ ] Color matches domain

### Command Creation

- [ ] Uses $ARGUMENTS placeholder
- [ ] Process steps clearly defined
- [ ] Error handling documented
- [ ] Best practices included
- [ ] Adapts to project context

### MCP Creation

- [ ] Security best practices (env vars)
- [ ] Rate limiting configured
- [ ] Connection handling defined
- [ ] Error scenarios documented

---

## 5. Naming Conventions

| Component | Format | Beispiel |
|-----------|--------|----------|
| Agent | `{domain}-{role}.md` | `security-auditor.md` |
| Command | `{action}-{target}.md` | `generate-tests.md` |
| MCP | `{service}-integration.json` | `github-integration.json` |
| Hook | `{trigger}-{action}.sh` | `pre-commit-validation.sh` |

---

## Integration mit Evolving

Unser `template-creator` Skill nutzt ähnliche Patterns. Dieses Framework ergänzt mit:

1. **Color Coding** für visuelle Agent-Kategorisierung
2. **Description Examples** in Frontmatter
3. **MCP Templates** für Service-Integrationen

---

## Related

- [template-creator Skill](.claude/skills/template-creator/)
- [Agent Templates](.claude/templates/agents/)
- [Hook Patterns](hook-patterns-library.md)
