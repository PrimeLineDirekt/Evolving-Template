# 12-Factor Agents Framework

**Type**: External Learning / Reference Framework
**Confidence**: 90%
**Date**: 2025-12-10

---

## Overview

Production-Prinzipien für LLM-powered Agents, inspiriert von der 12-Factor App Methodologie für Cloud-native Applications.

---

## Die 12 Factors

### 1. Natural Language to Tool Calls
Konvertiere User Intent in strukturierte Function Calls, die deterministischer Code ausführen kann.

**Evolving**: ✅ Workflow Detection + Slash Commands

---

### 2. Own Your Prompts
Behalte volle Kontrolle über Prompts statt Framework-Defaults zu vertrauen.

**Evolving**: ✅ `knowledge/prompts/` + Agent-spezifische System Prompts

---

### 3. Own Your Context Window
Aktives Context Engineering statt Standard Message-Formate.

**Evolving**: ✅ Dokumentiert als [Context Window Ownership Pattern](../patterns/context-window-ownership-pattern.md)

**Key Insight**: XML-Tags und YAML sind token-effizienter als JSON. Custom Structures > Framework Defaults.

---

### 4. Tools Are Just Structured Outputs
Behandle Tool Calls als eine Form von Structured Output Generation.

**Evolving**: ✅ Verstanden, kein explizites Pattern nötig

**Mental Model**: LLM generiert JSON → Code führt aus → Ergebnis zurück

---

### 5. Unify Execution State and Business State
Halte Agent Execution State synchron mit Business Logic State.

**Evolving**: ✅ Multi-Agent Orchestrator synchronisiert Session State

**Beispiel**: Checkpoint speichert sowohl Agent-Results als auch User-Profile Updates

---

### 6. Launch/Pause/Resume with Simple APIs
Design Agents mit einfachen Interfaces für Start, Pause, Resume.

**Evolving**: ✅ Checkpoint Recovery in production systems

```python
# Resume from checkpoint
orchestrator.resume_session(session_id)
```

---

### 7. Contact Humans with Tool Calls
Nutze den gleichen Tool-Calling Mechanismus für Human-in-the-Loop.

**Evolving**: ✅ `AskUserQuestion` Tool in Claude Code

**Pattern**: Human Approval als Tool Call, nicht als separate Logik

---

### 8. Own Your Control Flow
Explizite Entscheidungslogik statt LLM alle Pfade bestimmen zu lassen.

**Evolving**: ✅ Orchestrator Pattern mit expliziten Agent-Sequenzen

**Anti-Pattern**: "Figure out what to do next" als einziger Prompt

---

### 9. Compact Errors into Context
Strukturierte Error-Darstellung mit Limits und Escalation.

**Evolving**: ✅ Dokumentiert als [Compact Errors Pattern](../patterns/compact-errors-pattern.md)

**Key Insight**: Max 3 consecutive errors per tool, dann Human Escalation

---

### 10. Small, Focused Agents
Spezialisierte Agents mit engen Responsibilities statt monolithische Systeme.

**Evolving**: ✅ Multiple Specialist Agents in production systems

**Beispiele**: idea-validator, research-analyst, context-manager, codebase-analyzer, etc.

---

### 11. Trigger from Anywhere, Meet Users Where They Are
Agents von verschiedenen Sources aktivierbar, Multi-Channel Integration.

**Evolving**: ✅ Workflow Detection + Plain Text Triggers + Slash Commands

**Beispiel**: "Ich habe eine Idee..." → `/idea-new` vorgeschlagen

---

### 12. Make Your Agent a Stateless Reducer
Agents als Pure Functions: Input State → Output State

**Evolving**: ✅ Checkpoint Pattern ermöglicht Stateless Execution

```
Agent(previous_state, new_input) → new_state
```

**Benefit**: Reproducibility, Testability, Crash Recovery

---

## Evolving System Coverage

| Factor | Status | Implementation |
|--------|--------|----------------|
| 1. NL → Tool Calls | ✅ | Workflow Detection |
| 2. Own Your Prompts | ✅ | knowledge/prompts/ |
| 3. Own Your Context Window | ✅ | Pattern dokumentiert |
| 4. Tools = Structured Outputs | ✅ | Mental Model |
| 5. Unify State | ✅ | Session + Checkpoint |
| 6. Launch/Pause/Resume | ✅ | Checkpoint Recovery |
| 7. Contact Humans | ✅ | AskUserQuestion |
| 8. Own Control Flow | ✅ | Orchestrator Pattern |
| 9. Compact Errors | ✅ | Pattern dokumentiert |
| 10. Small Agents | ✅ | 17 Specialists |
| 11. Trigger Anywhere | ✅ | Multi-Trigger Detection |
| 12. Stateless Reducer | ✅ | Checkpoint Pattern |

**Coverage**: 12/12 (100%)

---

## Key Takeaways

1. **Framework als Checkliste**: Nützlich um Agent-Architekturen zu validieren
2. **Factors 3 + 9 als Patterns**: Detailliert genug für eigenständige Dokumentation
3. **Unsere Architektur ist solid**: 100% Coverage zeigt gutes Design

---

## Related

- [Context Window Ownership Pattern](../patterns/context-window-ownership-pattern.md)
- [Compact Errors Pattern](../patterns/compact-errors-pattern.md)
- [Checkpoint Validation Pattern](../patterns/checkpoint-validation-pattern.md)
- [Multi-Agent Orchestration Pattern](../patterns/multi-agent-orchestration.md)

---

**Navigation**: [← Learnings](README.md) | [Knowledge Index](../index.md)
