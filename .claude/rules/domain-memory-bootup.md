# Domain Memory Bootup Ritual

**Priorität**: KRITISCH
**Trigger**: Session-Start, Projekt-Wechsel, nach längerer Pause

## Konzept

Domain Memory macht den Unterschied zwischen:
- **Ohne**: "6yo dumb kid" / "Amnesiac with tool belt"
- **Mit**: "Disciplined engineer"

## Session-Start Ritual

### 1. READ MEMORY (Immer zuerst!)

```
Lies in dieser Reihenfolge:

1. _memory/index.json
   → Welches Projekt ist aktiv?
   → Welcher Workflow läuft?

2. _memory/projects/{active}.json
   → Goals & Features
   → Current State
   → Recent Progress
   → Known Failures

3. _memory/workflows/active.json (falls vorhanden)
   → Current Step
   → Checklist Status
```

### 2. ORIENT

Beantworte für dich selbst:
- Was war der letzte Progress?
- Was sind die aktuellen Goals?
- Was sind bekannte Failures/Blockers?
- Was wurde als nächster Schritt vorgeschlagen?

### 3. ANNOUNCE

Teile dem User den Context mit:
```
"Ich sehe wir arbeiten an [Projekt].
 Letzter Stand: [Progress].
 Nächster Schritt wäre: [Next].
 Soll ich damit weitermachen?"
```

### 4. PICK ONE

- Wähle EINEN Task
- Nicht mehrere gleichzeitig
- Atomic Progress

## Session-Ende Ritual

### 1. LOG PROGRESS

Update `_memory/projects/{project}.json`:
```json
{
  "date": "YYYY-MM-DD",
  "action": "Was wurde getan",
  "result": "Ergebnis",
  "next": "Vorgeschlagener nächster Schritt"
}
```

### 2. UPDATE STATE

- Feature-Status ändern (passing/failing)
- Current Phase aktualisieren
- Blocking Issues updaten

### 3. LOG FAILURES (wenn applicable)

```json
{
  "date": "YYYY-MM-DD",
  "what": "Was ging schief",
  "why": "Root Cause",
  "learned": "Lesson Learned"
}
```

## Wann Memory updaten?

| Event | Action |
|-------|--------|
| Task abgeschlossen | Progress Entry |
| Feature fertig | Feature Status → passing |
| Fehler aufgetreten | Failure Entry |
| Phase gewechselt | State.current_phase |
| Session Ende | Progress + Next Step |

## Memory-Pfade

```
_memory/
├── index.json              # Aktiver Context
├── projects/
│   ├── {project-name}.json
│   └── ...
├── workflows/
│   └── active.json         # Laufender Workflow
└── sessions/
    └── context.json        # Session-spezifisch
```

## Knowledge Graph Integration

Der Knowledge Graph (`_graph/`) ergänzt Domain Memory mit Entity-Vernetzung.

### Bei Task-Start: Context Router nutzen

Wenn ein spezifischer Task beginnt (z.B. "Agent erstellen"):
1. Lies `_graph/cache/context-router.json`
2. Finde passende Route für die Keywords
3. Lade Primary Nodes für sofortigen Kontext
4. Secondary Nodes bei Bedarf

### Graph-Dateien

```
_graph/
├── nodes.json              # Alle Entities (~150)
├── edges.json              # Beziehungen (~200)
├── taxonomy.json           # Unified Keywords
├── index/
│   ├── by-type.json        # Nach Entity-Typ
│   ├── by-domain.json      # Nach Domain/Tag
│   └── by-project.json     # Nach Projekt
└── cache/
    └── context-router.json # Keyword → Nodes
```

### Wann Graph nutzen?

| Situation | Aktion |
|-----------|--------|
| Agent/Skill/Command erstellen | Context Router → Templates & Patterns |
| Verbindungen suchen | edges.json lesen |
| Entity finden | by-type.json oder by-domain.json |
| Projekt-Kontext | by-project.json |

## Beispiel Bootup

```
[Session Start]

Claude liest _memory/index.json:
  → active_context.project = "evolving-system"

Claude liest _memory/projects/evolving-system.json:
  → current_phase = "Domain Memory Implementation"
  → last_progress = "Schema erstellt"
  → next = "Workflows anpassen"

Claude sagt:
  "Wir arbeiten am Evolving System.
   Letzter Stand: Domain Memory Schema erstellt.
   Features: 6/8 passing, Domain Memory in_progress.
   Nächster Schritt: Workflows für Memory-Integration anpassen.
   Soll ich damit weitermachen?"
```

## Nicht vergessen!

- **Jede Session**: Memory lesen
- **Jeder Task-Abschluss**: Progress loggen
- **Jeder Fehler**: Failure dokumentieren
- **Session-Ende**: Next Step vorschlagen

> "The agent is just a policy that transforms one memory state into another."
