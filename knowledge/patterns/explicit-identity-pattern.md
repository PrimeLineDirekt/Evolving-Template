# Explicit Identity Pattern

**Source**: continuous-claude
**Extracted**: 2025-12-28
**Tags**: multi-agent, async, concurrency, identifiers

---

## Konzept

> "Never rely on 'latest' or 'current' when crossing process or async boundaries."

Explicit IDs durch die gesamte Pipeline durchreichen. "Most recent" ist eine Race Condition.

---

## Das Problem

```
FALSCH: Race Condition

Main Agent → Spawn Worker("process latest session")
                    ↓
             Worker starts
                    ↓
    [NEW SESSION STARTS]
                    ↓
             Worker queries "latest"
                    ↓
             Gets WRONG session!
```

---

## Die Lösung

```
RICHTIG: Explicit IDs

Main Agent → Spawn Worker("process session-abc123")
                    ↓
             Worker starts
                    ↓
    [NEW SESSION STARTS - irrelevant]
                    ↓
             Worker uses session-abc123
                    ↓
             Correct result!
```

---

## DO

| Technik | Beispiel |
|---------|----------|
| Pass explicit IDs | `--session-id $ID` |
| Store IDs in state | `state.session_id = id` |
| Use full identifiers | UUID v4, nicht partielle |
| Keep ID types separate | session_id != span_id |

## DON'T

| Anti-Pattern | Problem |
|--------------|---------|
| Query "most recent" | Race condition |
| Assume context persists | Await/spawn changes context |
| Collapse ID types | Confusion zwischen Konzepten |
| Use "latest" in queries | Unstable reference |

---

## Implementation

### Bad: Race Condition

```python
# DON'T - race at session boundaries
spawn_agent('analyzer', ['--learn'])  # defaults to "most recent"
```

### Good: Explicit ID

```python
# DO - explicit identity
spawn_agent('analyzer', [
    '--learn',
    '--session-id', context.session_id
])
```

### State File Pattern

```python
def save_state(session_id: str, data: dict):
    state_file = f"state/{session_id}.json"
    write_json(state_file, {
        'session_id': session_id,
        'data': data,
        'timestamp': now()
    })

def load_state(session_id: str):
    # Explicit ID, no "latest" query
    state_file = f"state/{session_id}.json"
    return read_json(state_file)
```

---

## ID Type Separation

Verschiedene IDs für verschiedene Konzepte:

| ID Type | Purpose | Example |
|---------|---------|---------|
| `session_id` | Claude Code Session (human-facing) | `session-2025-001` |
| `root_span_id` | Trace ID (query key) | `span-abc123` |
| `turn_span_id` | Turn within session | `turn-xyz789` |
| `task_id` | Background task | `task-def456` |

**Nicht kollabieren!** Jeder ID-Typ hat unterschiedliche Semantik.

---

## Wann anwenden?

| Situation | Explicit ID nötig? |
|-----------|-------------------|
| Agent spawnen | JA |
| Async operation starten | JA |
| State für später speichern | JA |
| DB-Query in anderem Prozess | JA |
| Synchroner, lokaler Code | Optional |

---

## Checkliste

```
□ Wird ein Prozess/Agent gestartet?
  → ID explizit durchreichen

□ Gibt es await/async Boundaries?
  → ID vorher speichern, nicht nach await queryen

□ Werden mehrere ID-Typen verwendet?
  → Klar trennen, nicht mischen

□ Wird "latest" oder "current" queryed?
  → Durch explizite ID ersetzen
```

---

## Related

- `knowledge/patterns/idempotent-redundancy-pattern.md` - Safe retries
- `.claude/rules/domain-memory-bootup.md` - Session ID handling
