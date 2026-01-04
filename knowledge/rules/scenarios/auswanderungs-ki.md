---
paths:
  - {HOME}/Buisiness/{PROJECT}-v2/**/*
---

# {PROJECT} v2 Rules

Path-spezifische Regeln für Arbeit am {PROJECT} v2 Projekt.

## Tech Stack

- **Backend**: Python 3.11+, LangGraph, FastAPI
- **Database**: ChromaDB (Vector Store)
- **LLM**: Claude Opus/Sonnet/Haiku (3-Tier)

## Architektur

- 17 Specialist Agents
- Resilient Orchestrator mit Checkpoint Recovery
- Knowledge Base mit Tax Documents (72 Docs, 621k Wörter)

## Model Tiers

| Tier | Model | Use Case |
|------|-------|----------|
| 1 | Opus | Kritische Analyse (Steuer, DBA) |
| 2 | Sonnet | Standard-Analyse (Default) |
| 3 | Haiku | Strukturierte Tasks (Checklisten) |

## Key Patterns

- **BaseAgent** mit standardisiertem Interface
- **Confidence Scoring** (3-Tier: Primary/Secondary/Tertiary)
- **Risk Zone Classification** (🟢🟡🟠)
- **HITL Trigger** bei Confidence < 0.75

## Dokumentation

- Projekt-Docs: @knowledge/projects/{PROJECT_ID}/
- Analysis Context: @knowledge/external-projects/{PROJECT_ID}/
- Agent Patterns: @knowledge/prompts/patterns/{PROJECT_ID}-agents/

## Codebase

```
{HOME}/Buisiness/{PROJECT}-v2/
├── src/
│   ├── agents/          # 17 Specialist Agents
│   ├── orchestrator/    # Resilient Orchestrator
│   ├── knowledge/       # KB Retriever & Cache
│   └── models/          # Pydantic Models
├── knowledge-base/      # Tax Documents (72 Docs)
└── config/              # Settings
```
