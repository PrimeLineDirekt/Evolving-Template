# Clear, Don't Compact

**Priorität**: HOCH
**Quelle**: Continuous-Claude
**Trigger**: Bei Context-Problemen, vor /clear

---

## Das Problem

```
Compaction = Lossy Summarization

Session Start: Full context, high signal
    ↓ work, work, work
Compaction 1: Some detail lost
    ↓ work, work, work
Compaction 2: Context getting murky
    ↓ work, work, work
Compaction 3: Working with compressed noise
    ↓ Halluzinationen, vergessener Kontext
```

**Jede Compaction ist verlustbehaftet.** Nach mehreren Compactions arbeitet man mit einem "Summary of a Summary of a Summary".

---

## Die Lösung

**Save state → /clear → Resume fresh**

```
Session Start: Fresh context + ledger loaded
    ↓ focused work
Complete task → Update ledger
    ↓ /clear
Fresh context + ledger loaded
    ↓ continue with full signal
```

---

## Wann /clear nutzen?

| Signal | Aktion |
|--------|--------|
| Context fühlt sich "murky" an | Ledger updaten → /clear |
| Halluzinationen über vorherige Arbeit | Ledger updaten → /clear |
| Große Task abgeschlossen | Ledger updaten → /clear |
| Projekt-Wechsel | Ledger updaten → /clear |
| Nach ~2-3 Stunden Arbeit | Ledger updaten → /clear |

---

## Ledger Required Sections

Ein vollständiges Ledger enthält diese Sektionen:

```markdown
# Session: {name}
Updated: {ISO timestamp}

## Goal
{Success criteria - what does "done" look like?}

## Constraints
{Tech requirements, patterns to follow, things to avoid}

## Key Decisions
{Choices made with brief rationale}
- Decision 1: Chose X over Y because...
- Decision 2: ...

## State
- Done: {completed items}
- Now: {current focus - ONE thing only}
- Next: {queued items in priority order}

## Open Questions
- UNCONFIRMED: {things needing verification after clear}
- UNCONFIRMED: {assumptions that should be validated}

## Working Set
{Active files, branch, test commands}
- Branch: `feature/xyz`
- Key files: `src/auth/`, `tests/auth/`
- Test cmd: `npm test -- --grep auth`
```

---

## Checkbox States (für Multi-Phase Work)

Für komplexe Implementierungen mit mehreren Phasen:

```markdown
## State
- Done:
  - [x] Phase 1: Setup database schema
  - [x] Phase 2: Create API endpoints
- Now: [→] Phase 3: Add validation logic
- Next: Phase 4: Frontend components
- Remaining:
  - [ ] Phase 5: Wire up API calls
  - [ ] Phase 6: Write tests
```

| Symbol | Bedeutung |
|--------|-----------|
| `[x]` | Completed |
| `[→]` | In progress (current) |
| `[ ]` | Pending |

**Warum Checkboxes in Files?** TodoWrite überlebt Compaction, aber das *Verständnis* degradiert. File-based checkboxes werden nie komprimiert.

---

## UNCONFIRMED Prefix

Für unsichere Items nach /clear:

```markdown
## Open Questions
- UNCONFIRMED: Does the auth middleware need updating?
- UNCONFIRMED: Is the API rate limit sufficient?
```

Nach Resume diese Items explizit verifizieren!

---

## Tool-Vergleich

| Tool | Scope | Fidelity |
|------|-------|----------|
| CLAUDE.md | Project | Always fresh, stable patterns |
| TodoWrite | Turn | Survives compaction, understanding degrades |
| Ledger (CURRENT.md) | Session | External file - never compressed, full fidelity |
| Handoffs | Cross-session | External file - detailed context for new session |
| Domain Memory | Persistent | Project state across all sessions |

---

## Workflow

### Vor /clear

1. **Ledger aktualisieren**:
   ```
   Lies _ledgers/CURRENT.md
   Aktualisiere:
   - State Section (Done/Now/Next mit Checkboxes)
   - Key Decisions (neue Entscheidungen)
   - Open Questions (UNCONFIRMED für Unsicheres)
   - Working Set (aktuelle Dateien)
   ```

2. **Domain Memory updaten** (falls Progress):
   ```
   Update _memory/projects/{active}.json
   ```

3. **Erst dann**: `/clear`

### Nach /clear

1. **Ledger laden**: `_ledgers/CURRENT.md` lesen
2. **Find `[→]`** um aktuelle Phase zu finden
3. **UNCONFIRMED Items** verifizieren
4. **Weiterarbeiten** mit frischem Context

---

## Automatische Unterstützung

### Ledger Auto-Save Hook

Bei Session-Ende wird automatisch:
- Session-Aktivität (Commits, Modified Files) zum Ledger hinzugefügt
- Projekt aus Domain Memory referenziert

### Session-Summary Hook

Erstellt zusätzlich:
- `knowledge/sessions/session-YYYY-MM-DD-HHMMSS.md`
- Git Activity
- Uncommitted Changes

---

## Merksätze

> "Ledgers are lossless - you control what's saved"

> "Fresh context = full signal"

> "Agents spawn with clean context, not degraded summaries"

---

## Anti-Pattern

**NICHT** machen:
- Compaction einfach akzeptieren und weiterarbeiten
- Wichtige Entscheidungen nur im Chat-Kontext behalten
- Ohne Ledger-Update /clear ausführen

---

## Ledger-Pfade

| Datei | Zweck |
|-------|-------|
| `_ledgers/CURRENT.md` | Aktives Session-Ledger |
| `_ledgers/archive/` | Abgeschlossene Ledgers |
| `_handoffs/` | Detaillierte Session-Handoffs |
| `_memory/` | Persistenter Projekt-State |

---

## Integration

Diese Rule arbeitet zusammen mit:
- `domain-memory-bootup.md` - Memory beim Start laden
- `ledger-auto-save.sh` Hook - Automatisches Speichern
- `/whats-next` Command - Detaillierter Handoff
