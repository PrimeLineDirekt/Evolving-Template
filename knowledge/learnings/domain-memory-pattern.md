---
title: "Domain Memory Pattern"
type: learning
tags: [agents, memory, architecture, long-running, stateful]
topics: [agent-design, memory-systems, workflow-automation]
created: 2025-12-13
source:
  - "YouTube: Anthropic Agent Memory (xNcEgqzlPqs)"
  - "Twitter: @Hesamation (CamelAI)"
  - "Anthropic Blog Post"
completeness: complete
---

# Domain Memory Pattern

## TL;DR

90% von funktionierenden Agents ist das **Memory** - nicht das Model, Framework, oder MCPs. Ein generalisierter Agent ist ein "Amnesiac with a tool belt". Domain Memory transformiert ihn in einen "disciplined engineer".

## Das Problem

### Generalized Agents scheitern

```
User Prompt → Agent + Tools → Output
                ↓
        "Do everything in one manic burst and fail"
        OR
        "Wander around, make partial progress, claim success"
```

**Warum?**
- Jede Session startet ohne Kontext
- Keine Ahnung was vorher passiert ist
- Keine klare Definition von "done"
- Kein Wissen über vergangene Fehler

> "If you loop an LLM with tools, it will give you an infinite sequence of disconnected interns."

### Was NICHT funktioniert

| Ansatz | Problem |
|--------|---------|
| Smarteres Model | Löst nicht das Memory-Problem |
| Mehr Tools | Agent weiß trotzdem nicht wo er ist |
| Vector Database | Unstrukturiert, kein State |
| Längeres Context Window | Irgendwann voll, dann Amnesia |

## Die Lösung: Domain Memory

### Definition

**Domain Memory** = Persistent structured representation of work

Nicht: "Vector DB mit Chunks"
Sondern: "Strukturierter State mit klaren Feldern"

### Was Domain Memory enthält

| Kategorie | Beispiele |
|-----------|-----------|
| **Goals** | Feature List, Requirements, Constraints |
| **State** | Was passed? Was failed? Was tried? Was broke? |
| **Progress** | Log of what each run did |
| **Scaffolding** | How to run, test, extend |
| **Capabilities** | What the agent CAN do |
| **Past Failures** | What went wrong before |

### Formate

```
Domain Memory kann sein:

1. JSON Blob
   {
     "features": [
       {"name": "auth", "status": "passing"},
       {"name": "api", "status": "failing"}
     ]
   }

2. Progress Log (Markdown/Text)
   ## Run 2025-12-13-001
   - Attempted: API integration
   - Result: Failed - missing auth
   - Next: Fix auth first

3. Git History
   - Previous commits
   - What changed when
   - Why it changed
```

## Two-Agent Pattern (Anthropic)

### Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    DOMAIN MEMORY                         │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────┐  │
│  │ Feature List│  │ Progress Log│  │ Test Results    │  │
│  │ (JSON)      │  │ (Markdown)  │  │ (pass/fail)     │  │
│  └─────────────┘  └─────────────┘  └─────────────────┘  │
└─────────────────────────────────────────────────────────┘
         ▲                  ▲                  ▲
         │                  │                  │
    ┌────┴────┐        ┌────┴────┐        ┌────┴────┐
    │ INIT    │        │ WORKER  │        │ WORKER  │
    │ AGENT   │        │ RUN 1   │        │ RUN 2   │
    └─────────┘        └─────────┘        └─────────┘

    Erstellt           Liest → Arbeitet → Schreibt
    Memory             (keine eigene Memory)
```

### Initializer Agent (Stage Manager)

**Aufgabe:** Bootstrap Domain Memory from User Prompt

1. Expandiert User Prompt → Detailed Feature List
2. Setzt alle Features initial auf "failing"
3. Erstellt Progress Log Struktur
4. Definiert "Rules of Engagement"
5. Definiert Test-Kriterien

**Hat KEINE persistent Memory nötig** - transformiert nur Prompt → Artifacts

### Worker Agent (Actor)

**Aufgabe:** Transform one memory state into another

Jeder Run:
1. **Read** - Progress, Git History, Feature List
2. **Pick** - Single failing feature
3. **Implement** - Work on that one thing
4. **Test** - End-to-end
5. **Update** - Feature status (pass/fail)
6. **Log** - Write progress note
7. **Commit** - Git commit
8. **Exit** - Disappear (no memory retained)

> "The agent is now just a policy that transforms one consistent memory state into another."

## Key Insight

### Memory > Model

| Component | Importance |
|-----------|------------|
| Memory/Context | 90% |
| Model | ~5% |
| Framework | ~3% |
| MCPs | ~2% |

### Context macht den Unterschied

> "The context can make an agent a 6yo dumb kid, or a disciplined engineer."

Gleicher Agent, gleiche Tools:
- **Ohne Domain Memory:** Amnesiac intern
- **Mit Domain Memory:** Disciplined engineer

## Design Principles

### 1. Externalize Goals
```
❌ "Do X"
✅ Machine-readable backlog with pass/fail criteria
```

### 2. Make Progress Atomic & Observable
```
❌ "Work on the project"
✅ Pick ONE item → Work → Update shared state
```

### 3. Leave Campsite Cleaner
```
Every run ends with:
- Clean test passing state
- Human-readable documentation
- Machine-readable state update
```

### 4. Standardize Bootup Ritual
```
EVERY run:
1. Read memory
2. Run basic checks
3. THEN act
```

### 5. Tests Close to Memory
```
pass/fail = Source of truth for domain state
If not tied to tests → Will drift
```

## Beyond Coding

### Das Pattern ist generalisierbar

| Domain | Memory Schema |
|--------|---------------|
| **Coding** | Feature list, test results, git history |
| **Research** | Hypothesis backlog, experiment registry, evidence log |
| **Operations** | Runbook, incident timeline, ticket queue, SLA |
| **Content** | Topic backlog, draft status, publish criteria |
| **Ideas** | Idea list, validation status, next actions |

### Workflow Memory (CamelAI)

Gleicher Begriff, andere Formulierung:
- **Spezialisierung** - Was kann der Agent?
- **Task-spezifisches Memory** - Nicht Session Memory!
- **Long-term Memory** - Kritische Insights die in Zukunft wichtig sind

## Strategic Implications

### Der echte Moat

> "The moat isn't a smarter AI agent. The moat is your domain memory and your harness."

**Wird commoditized:**
- Models
- Frameworks
- APIs

**Wird NICHT commoditized:**
- Deine Schemas für Arbeit
- Deine Harnesses für durable progress
- Deine Testing Loops

### Fantasy vs. Reality

| Fantasy | Reality |
|---------|---------|
| "Drop an agent on your company" | Braucht domain-specific memory |
| "Universal enterprise agent" | Ohne schemas = thrash |
| "Plug model into Slack = Agent" | Ohne struktur = chaos |

## Prompting Connection

> "So much of what we do with prompting is being that initializer agent."

**Prompting = Setting the Stage**

Gutes Prompting:
- Setzt Context
- Definiert Structure
- Ermöglicht erfolgreiche Activity

Das ist exakt was der Initializer Agent tut - nur manuell.

## Implementation Checklist

Für jede Domain/Workflow:

- [ ] **Goals definiert** - Machine-readable backlog
- [ ] **State trackbar** - Was passed/failed/tried
- [ ] **Progress loggbar** - Was jeder Run tat
- [ ] **Tests definiert** - Pass/fail criteria
- [ ] **Bootup Ritual** - Standard read-check-act
- [ ] **Atomic Progress** - One thing per run

## Related

- [Context Window Ownership Pattern](../patterns/context-window-ownership-pattern.md)
- [Compact Errors Pattern](../patterns/compact-errors-pattern.md)
- [12-Factor Agents Framework](12-factor-agents-framework.md)
- [Checkpoint Validation Pattern](../patterns/checkpoint-validation-pattern.md)

## Sources

1. **YouTube Video** (xNcEgqzlPqs) - "Anthropic Agent Memory"
2. **Twitter @Hesamation** - CamelAI Workflow Memory
3. **Anthropic Blog Post** - Referenced in video

---

**Key Quote:**
> "The mystery of agents is memory. And this is how you solve it."
