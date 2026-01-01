# Ralph Wiggum Loop Pattern

**Quelle**: anthropics/claude-plugins-official/ralph-wiggum
**Kategorie**: automation, self-improvement, hooks
**Status**: Official Anthropic Pattern
**Erstellt**: 2025-12-29

---

## Problem

Komplexe Tasks erfordern oft mehrere Iterationen. Manuelles Re-Prompting ist zeitaufwändig und unterbricht den Flow.

## Lösung

Self-Referential Loop via Stop Hook: Intercepte Exit-Versuche und füttere den gleichen Prompt zurück bis eine Completion-Promise erfüllt ist.

## Pattern

### Architektur

```
┌─────────────────────────────────────────────────────┐
│                  Ralph Loop                          │
│                                                      │
│  /ralph-loop "Task" --completion-promise "DONE"     │
│                         │                            │
│                         ▼                            │
│               ┌─────────────────┐                   │
│               │  Claude Works   │◄──────────────┐   │
│               │   on Task       │               │   │
│               └────────┬────────┘               │   │
│                        │                         │   │
│                        ▼                         │   │
│               ┌─────────────────┐               │   │
│               │  Tries to Exit  │               │   │
│               └────────┬────────┘               │   │
│                        │                         │   │
│                        ▼                         │   │
│               ┌─────────────────┐               │   │
│               │   Stop Hook     │               │   │
│               │   Intercepts    │               │   │
│               └────────┬────────┘               │   │
│                        │                         │   │
│           ┌────────────┴────────────┐           │   │
│           ▼                         ▼           │   │
│   ┌──────────────┐         ┌──────────────┐    │   │
│   │ Promise Found │         │ No Promise   │────┘   │
│   │ (COMPLETE)    │         │ Re-prompt    │        │
│   └──────┬───────┘         └──────────────┘        │
│          │                                          │
│          ▼                                          │
│   ┌──────────────┐                                 │
│   │  Exit Loop   │                                 │
│   │  Task Done   │                                 │
│   └──────────────┘                                 │
└─────────────────────────────────────────────────────┘
```

### Komponenten

| Komponente | Zweck |
|------------|-------|
| **ralph-loop Command** | Startet Loop mit Prompt + Completion-Promise |
| **stop-hook.sh** | Intercepted Exit, prüft Promise, re-prompts |
| **State File** | `.claude/ralph-loop.local.md` mit Iteration Counter |
| **Completion Promise** | `<promise>DONE</promise>` Tag im Output |

### Command Syntax

```bash
/ralph-loop "PROMPT" --completion-promise "TEXT" --max-iterations N
```

### Stop Hook Logic (Pseudocode)

```bash
# 1. Check if loop active
if [ ! -f ".claude/ralph-loop.local.md" ]; then
  exit 0  # No loop, allow exit
fi

# 2. Extract completion promise from state
completion_promise=$(get_frontmatter "completion_promise")

# 3. Check last message for promise
last_message=$(extract_last_assistant_message)
if echo "$last_message" | grep -q "<promise>$completion_promise</promise>"; then
  rm ".claude/ralph-loop.local.md"
  exit 0  # Promise found, allow exit
fi

# 4. Increment iteration, re-prompt
iteration=$((iteration + 1))
if [ $iteration -gt $max_iterations ]; then
  exit 0  # Safety limit reached
fi

# 5. Block exit, return re-prompt
echo '{"decision": "block", "reason": "ORIGINAL_PROMPT"}'
```

### Best Practices für Prompts

1. **Klare Completion-Kriterien**: Exakt definieren wann fertig
2. **Inkrementelle Ziele**: Task in Phasen aufteilen
3. **Self-Correction einbauen**: Test-Driven Development Loops
4. **Escape Hatch**: IMMER `--max-iterations` setzen

### Beispiel

```bash
/ralph-loop "Build a REST API for todos. Requirements:
- CRUD operations
- Input validation
- Unit tests with >80% coverage
- Documentation

When ALL requirements are met and tests pass,
output <promise>COMPLETE</promise>" \
  --completion-promise "COMPLETE" \
  --max-iterations 50
```

## Wann anwenden?

✅ **Gut für:**
- Well-defined Tasks mit klaren Kriterien
- Iteration-heavy Work (TDD Loops)
- Greenfield Projects
- Tasks mit automatischer Verifikation (Tests, Lints)

❌ **Nicht gut für:**
- Tasks die Human Judgment brauchen
- One-Shot Operations
- Unklare Kriterien
- Production Debugging

## Real-World Results (aus Doku)

- 6 Repositories overnight generiert (YC Hackathon)
- $50k Contract für $297 API Costs abgeschlossen
- Komplette Programming Language über 3 Monate entwickelt

## Design Philosophy

> "Iteration > Perfection"
> "Failures Are Data"
> "Persistence Wins"

## Integration mit Evolving

Könnte als Hook implementiert werden für:
- Automatische Test-Fix-Loops
- Iterative Dokumentation
- Self-Improving Workflows

**Vorsicht**: Benötigt klare Completion-Kriterien und Safety Limits!

## Related

- `safety-hooks-framework-pattern.md` - Hook Safety Best Practices
- `hook-development-reference.md` - Hook Implementation Guide
- `session-evaluation.md` Rule - Für Loop-Qualitätsbewertung
