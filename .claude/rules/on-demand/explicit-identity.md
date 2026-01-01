# Explicit Identity Across Boundaries

**Priorität**: MITTEL
**Trigger**: Agent-Spawning, Async Operations, Session-Handoffs
**Quelle**: continuous-claude

---

## Das Prinzip

> "Pass explicit identifiers through the entire pipeline. 'Most recent' is a race condition."

Niemals auf "latest" oder "current" verlassen wenn Prozess- oder Async-Grenzen überschritten werden.

---

## DO

- Pass `--session-id $ID` beim Spawnen von Prozessen
- IDs in State Files speichern für spätere Korrelation
- Volle UUIDs verwenden, nicht partielle Matches
- Verschiedene ID-Typen getrennt halten

## DON'T

- "Most recent session" zur Ausführungszeit abfragen
- Annehmen dass aktueller Kontext nach await/spawn noch gilt
- ID-Typen kollabieren (verschiedene Konzepte!)

---

## ID-Typen in Evolving

| ID-Typ | Zweck | Speicherort |
|--------|-------|-------------|
| `session_id` | Claude Code Session | `_ledgers/CURRENT.md` |
| `project_id` | Domain Memory Projekt | `_memory/index.json` |
| `experience_id` | Experience Entry | `_memory/experiences/exp-*.json` |
| `handoff_id` | Session Handoff | `_handoffs/*.md` |

---

## Pattern

```typescript
// SCHLECHT: Race Condition an Session-Grenzen
spawn('agent', ['--analyze'])  // defaults to "most recent"

// GUT: Explizite Identität
spawn('agent', ['--analyze', '--session-id', input.session_id])
```

---

## Beispiel: Agent-Spawning

```bash
# SCHLECHT
Task("Analysiere die letzte Session")

# GUT
Task("Analysiere Session {session_id} aus _ledgers/CURRENT.md")
```

---

## Wann kritisch?

| Situation | Risiko | Mitigation |
|-----------|--------|------------|
| Agent spawnt Agent | ID-Verlust | Session-ID durchreichen |
| After /clear | Kontext weg | Ledger hat IDs |
| Async Operations | Race Condition | Explizite IDs in Files |
| Multi-Step Workflows | Drift | ID pro Step speichern |

---

## Integration

Diese Rule arbeitet zusammen mit:
- `clear-dont-compact.md` - Ledger hat Session-IDs
- `domain-memory-bootup.md` - Project-IDs aus Memory
- `index-at-creation.md` - IDs bei Erstellung setzen
