# Claude Skills Generator

**Quelle**: claude-skills-generator Repository
**Extrahiert**: 2026-01-01
**Kategorie**: reference

---

## Übersicht

Template-basiertes System zur Erstellung von Claude Code Skills. Nutzt VibeShip Orchestrator für AI-powered Development mit State Management und Task Queuing.

## Skill Schema (skill.schema.json)

### Required Fields

| Feld | Typ | Constraints |
|------|-----|-------------|
| `name` | string | 1-50 chars, pattern: `^[a-z][a-z0-9-]*$` |
| `description` | string | 10-200 chars |

### Optional Fields

| Feld | Typ | Beschreibung |
|------|-----|--------------|
| `version` | string | Semver pattern: `^\d+\.\d+\.\d+$` |
| `author` | string | Max 100 chars |
| `mcps` | object | `required[]` und `optional[]` MCP Server Arrays |
| `triggers` | array | Activation keywords/phrases |
| `tags` | array | Categorization tags |

### MCP Configuration

```yaml
mcps:
  required:
    - filesystem     # Always needed
    - sequential-thinking  # For complex reasoning
  optional:
    - github         # If repo operations
    - puppeteer      # If browser needed
```

---

## Template: World-Class Specialist

**Datei**: `skills/world-class-specialist.md`

### Struktur

```markdown
---
name: {{name}}
description: Use when {{condition}} - {{what_it_does_and_why}}
version: 1.0.0
author: {{author}}
mcps:
  required: [{{mcp1}}, {{mcp2}}]
  optional: [{{mcp3}}]
triggers:
  - "{{trigger_phrase_1}}"
  - "{{trigger_phrase_2}}"
tags: [{{tag1}}, {{tag2}}, {{tag3}}]
---

# {{Name}} Skill

## Iron Law
> "{{Core principle that must never be violated}}"

## When to Use
- {{Use case 1}}
- {{Use case 2}}

## Process

### Phase 1: {{Phase Name}}
1. {{Step 1}}
2. {{Step 2}}

### Phase 2: {{Phase Name}}
1. {{Step 1}}
2. {{Step 2}}

## Patterns

### {{Pattern 1 Name}}
**When**: {{Situation}}
**Do**: {{Action}}
**Example**:
```{{language}}
{{code example}}
```

### {{Pattern 2 Name}}
...

## Anti-Patterns

### {{Anti-Pattern 1}}
**Problem**: {{What goes wrong}}
**Instead**: {{What to do}}

## Red Flags
- {{Warning sign 1}}
- {{Warning sign 2}}

## Gotchas
- {{Common mistake 1}}
- {{Common mistake 2}}

## Verification Checklist
- [ ] {{Check 1}}
- [ ] {{Check 2}}
- [ ] {{Check 3}}
```

---

## Template: Debugging Skill

**Datei**: `skills/debugging.md`

### Struktur

```markdown
---
name: {{domain}}-debugging
description: Debug {{domain}} issues using systematic investigation
version: 1.0.0
mcps:
  required:
    - filesystem
  optional:
    - sequential-thinking
triggers:
  - "debug {{domain}}"
  - "{{domain}} error"
  - "fix {{domain}} issue"
tags: [debugging, {{domain}}, troubleshooting]
---

# {{Domain}} Debugging Skill

## Iron Law
> "Observe before assuming. Evidence before changes."

## 3-Phase Process

### Phase 1: Gather Information
**Goal**: Understand what's happening before changing anything

1. **Reproduce the issue**
   - Exact steps to trigger
   - Environment details
   - Error messages (full text)

2. **Check logs**
   - Application logs
   - System logs
   - Network logs (if applicable)

3. **Identify recent changes**
   - Git history
   - Config changes
   - Dependency updates

### Phase 2: Systematic Investigation
**Goal**: Narrow down root cause

1. **Binary search the problem space**
   - Disable half the components
   - Does issue persist?
   - Repeat until isolated

2. **Form hypotheses**
   - Based on evidence, not assumptions
   - List top 3 most likely causes
   - Test each systematically

3. **Use debugging tools**
   - Debugger breakpoints
   - Print statements (strategic)
   - Profilers if performance issue

### Phase 3: Fix and Verify
**Goal**: Implement solution and confirm fix

1. **Minimal fix first**
   - Smallest change that fixes issue
   - Avoid "while I'm here" changes

2. **Verify fix works**
   - Reproduce steps now pass
   - No regression in related areas

3. **Document for future**
   - What was the root cause?
   - How was it found?
   - How to prevent recurrence?

## Common {{Domain}} Issues

### {{Issue Type 1}}
**Symptoms**: {{What you see}}
**Cause**: {{Why it happens}}
**Fix**: {{How to resolve}}

### {{Issue Type 2}}
...

## Debugging Anti-Patterns

### Shotgun Debugging
**Problem**: Random changes hoping something works
**Instead**: Systematic hypothesis testing

### Assumption Blindness
**Problem**: "It can't be X because..."
**Instead**: Verify every assumption

### Log Overload
**Problem**: Adding logs everywhere
**Instead**: Strategic logging at key points

## Verification Checklist
- [ ] Issue is reproducible
- [ ] Root cause identified (not just symptom)
- [ ] Fix tested in isolation
- [ ] No regression introduced
- [ ] Documentation updated
```

---

## VibeShip Orchestrator Integration

### State Files

| File | Purpose |
|------|---------|
| `state.json` | Current phase, decisions, assumptions |
| `task_queue.json` | All tasks and status |
| `docs/PRD.md` | Generated requirements |
| `docs/ARCHITECTURE.md` | Technical decisions |
| `docs/PROJECT_LOG.md` | Progress narrative |

### Session Start Protocol

```
1. Read state.json
   → Check current phase
   → Check custom_skills_needed

2. If custom_skills_needed has items:
   → Generate those skills first

3. Based on phase:
   - discovery → Load planner.md
   - planning → Load planner.md
   - building → Read task_queue.json
   - review → Show summary

4. Resume from checkpoint if set
```

### Commands

| Command | Action |
|---------|--------|
| `status` | Show phase, completed tasks, next steps |
| `continue` | Resume from checkpoint |
| `replan` | Go back to planning phase |
| `assumptions` | Show/edit assumptions |
| `skip [task]` | Skip specific task |
| `pause` | Save state and stop |

### Status Indicators

| Symbol | Meaning |
|--------|---------|
| `>` | Active/processing |
| `+` | Completed |
| `!` | Warning |
| `*` | Needs human input |
| `x` | Error |

---

## Behaviors

Das System folgt diesen Behaviors:

| Behavior | Beschreibung |
|----------|--------------|
| `verify-before-complete` | Validierung vor Abschluss |
| `follow-architecture` | Architektur-Konformität |
| `one-task-at-a-time` | Fokussierte Ausführung |
| `maintainable-code` | Wartbarer Code |
| `secure-code` | Sicherheits-First |
| `tdd-mode` | Test-Driven Development |
| `commit-per-task` | Atomic Commits |
| `explain-as-you-go` | Transparente Kommunikation |

---

## Frontmatter Validation

### Name Pattern
```regex
^[a-z][a-z0-9-]*$
```
- Startet mit Kleinbuchstabe
- Nur lowercase, Zahlen, Bindestriche
- 1-50 Zeichen

### Version Pattern (Semver)
```regex
^\d+\.\d+\.\d+$
```
- Format: `MAJOR.MINOR.PATCH`
- Beispiel: `1.0.0`, `2.3.1`

### Description
- 10-200 Zeichen
- Sollte beschreiben: WANN nutzen + WAS es tut

---

## Lokaler Pfad

```
{EVOLVING_PATH}/_archive/repos/2026-01-01-deep-dive/claude-skills-generator/
├── CLAUDE.md                    # Orchestrator Instructions
├── state.json                   # Current State
├── task_queue.json              # Task Management
├── skills/
│   ├── planner.md               # Planning Skill
│   ├── world-class-specialist.md   # Universal Template
│   ├── debugging.md             # Debugging Template
│   └── skill.schema.json        # Validation Schema
└── docs/
    ├── PRD.md
    ├── ARCHITECTURE.md
    └── PROJECT_LOG.md
```

---

## Key Takeaways

1. **Schema-First**: Frontmatter muss Schema entsprechen
2. **Iron Law zentral**: Jeder Skill braucht ein unverletzbares Prinzip
3. **Patterns + Anti-Patterns**: Beide dokumentieren
4. **Verification Checklist**: Immer am Ende
5. **State Management**: VibeShip Orchestrator tracked Progress

---

## Related

- [vibeship-spawner-skills.md](vibeship-spawner-skills.md) - 462 fertige Skills
- [vibeship-content-ops.md](vibeship-content-ops.md) - Content Pipeline
- [.claude/skills/template-creator/](../../.claude/skills/template-creator/) - Evolving Skill Creator
