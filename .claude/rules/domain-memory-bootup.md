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
│   ├── evolving-system.json
│   ├── auswanderungs-ki-v2.json
│   └── thrive-vibes-art.json
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

## Hydrate Pattern (Single-Call Context Loading)

**Quelle**: QuixiAI/agi-memory, vectorize-io/hindsight

Statt sequentieller Reads ein optimierter Single-Call für alle Memory-Typen.

### Hydrate-Prozess

```
HYDRATE bei Session-Start:
                    ┌─────────────┐
                    │   Session   │
                    │    Start    │
                    └──────┬──────┘
                           │
           ┌───────────────┼───────────────┐
           ▼               ▼               ▼
    ┌─────────────┐ ┌─────────────┐ ┌─────────────┐
    │   DOMAIN    │ │ EXPERIENCE  │ │    GRAPH    │
    │   MEMORY    │ │   MEMORY    │ │   CONTEXT   │
    └──────┬──────┘ └──────┬──────┘ └──────┬──────┘
           │               │               │
           ▼               ▼               ▼
    _memory/index    Decay-Filtered    context-router
    + project.json   Experiences       Primary Nodes
           │               │               │
           └───────────────┼───────────────┘
                           ▼
                  ┌─────────────────┐
                  │  MERGED CONTEXT │
                  │  für Session    │
                  └─────────────────┘
```

### Type-Aware Retrieval

| Memory-Typ | Retrieval-Strategie | Filter |
|------------|---------------------|--------|
| **Domain Memory** | Direct Read | Aktives Projekt |
| **Experience Memory** | Decay-Aware Query | effective_relevance > 30 |
| **Graph Context** | Keyword-Match | Context Router |
| **Workflow State** | Direct Read | Falls aktiv |

### Decay-Aware Experience Loading

Bei Hydrate nur Experiences laden mit:
```
effective_relevance = base * decay_factor * trust_level
WHERE effective_relevance > 30
  AND (valid_until IS NULL OR valid_until > NOW())
```

**Filter-Kriterien:**
- `effective_relevance > 30` (Standard-Threshold)
- `valid_until` nicht abgelaufen (Temporal Validity)
- Projekt-Match (falls projekt-spezifischer Kontext)

### Optimierte Bootup-Sequenz

```
1. PARALLEL HYDRATE (Single-Call-Konzept):
   │
   ├─ _memory/index.json
   │   └─ Extrahiere: active_project, active_workflow
   │
   ├─ _memory/projects/{active}.json
   │   └─ Extrahiere: goals, state, progress, failures
   │
   ├─ _memory/experiences/ (decay-filtered)
   │   └─ Relevante Solutions, Patterns, Decisions
   │   └─ Filter: project-match OR high-relevance
   │
   └─ _graph/cache/context-router.json
       └─ Extrahiere: Routes für aktiven Projekt-Domain

2. MERGE & PRIORITIZE:
   │
   ├─ Domain Memory → Höchste Priorität (aktueller State)
   ├─ Recent Failures → Warnung bei bekannten Issues
   ├─ High-Trust Experiences → Relevante Lösungen
   └─ Graph Nodes → Verfügbare Patterns/Templates

3. ANNOUNCE (wie gehabt):
   "Projekt: {name} | Phase: {phase}
    Letzter Stand: {progress}
    Bekannte Issues: {failures count}
    Relevante Erfahrungen: {experiences count}
    Nächster Schritt: {next}"
```

### Wann Full Hydrate vs. Partial?

| Situation | Hydrate-Level |
|-----------|---------------|
| Neue Session | Full Hydrate (alle Typen) |
| Gleiche Session, neuer Task | Partial (nur Experience + Graph) |
| Fehler aufgetreten | Experience-fokussiert (Solutions) |
| Projekt-Wechsel | Full Hydrate für neues Projekt |

---

## Phase 3: Context-Scout (bei JEDER Anfrage)

**NACH Memory-Bootup, VOR User-Response.**

### Scout-Prozess

```
User-Input empfangen
         │
         ▼
┌────────────────────────┐
│ 1. KEYWORDS EXTRAHIEREN │
│    (aus User-Anfrage)   │
└──────────┬─────────────┘
           │
           ▼
┌────────────────────────────────┐
│ 2. COMMAND-DETECTION           │
│    .claude/detection-index.json │
│    → Match? Confidence?         │
└──────────┬─────────────────────┘
           │
           ▼
┌────────────────────────────────┐
│ 3. CONTEXT-ROUTER MATCH        │
│    _graph/cache/context-router  │
│    → Relevante Patterns/Rules   │
└──────────┬─────────────────────┘
           │
           ▼
┌────────────────────────────────┐
│ 4. SUMMARY-LAYER CHECK         │
│    .claude/summaries/{type}/    │
│    → Kompakte JSON statt MD     │
└──────────┬─────────────────────┘
           │
           ▼
      CONFIDENCE?
      /    |    \
    HIGH  MED   LOW
     │     │     │
     ▼     ▼     ▼
   LOAD  FRAGEN  SKIP
```

### Confidence-Levels

| Level | Score | Aktion |
|-------|-------|--------|
| **HIGH** | 80-100% | Automatisch laden (Primary Items) |
| **MEDIUM** | 50-79% | User fragen: "Meinst du /command?" |
| **LOW** | 0-49% | Ignorieren, normal antworten |

### Scout-Output (intern)

```json
{
  "match_type": "exact|fuzzy|fallback",
  "confidence": 85,
  "primary_route": "debugging",
  "secondary_routes": [{"route": "testing", "conf": 45}],
  "load_items": {
    "patterns": ["systematic-debugging"],
    "rules": ["observe-before-editing"],
    "commands": ["/debug"]
  },
  "suggested_command": "/debug",
  "full_docs_needed": false
}
```

### Laden aus Summaries (schnell!)

```
Bei HIGH Confidence:
1. Lies .claude/summaries/{type}/{name}.json (300 Tokens)
2. Verstehe key_points, when_to_use, related
3. NUR bei Bedarf: Volle MD laden (3000 Tokens)

Effekt: ~90% Token-Ersparnis durch Summary-Layer
```

### Fallback-Strategie

```
IF no_route_match OR confidence < 50:
   │
   ├─ Fallback 1: detection-index.json Keywords prüfen
   │   → Vielleicht Command-Match ohne Route?
   │
   ├─ Fallback 2: User fragen
   │   "Ich bin nicht sicher was du meinst.
   │    Meinst du X, Y, oder Z?"
   │
   └─ Max-Depth: 1
       → KEIN rekursives Fallback!
       → Lieber fragen als raten
```

### Wann NICHT scouten?

| Input | Verhalten |
|-------|-----------|
| "ja", "nein", "ok" | Direkt verarbeiten |
| "weiter", "mach mal" | Vorherigen Task fortsetzen |
| < 3 Wörter ohne Keywords | Direkt antworten |
| Expliziter /command | Command ausführen (kein Scout) |

---

## Context Budget Awareness

**Quelle**: Agent-Skills-for-Context-Engineering Deep Dive

### Model-Specific Thresholds

| Model | Degradation Onset | Severe Degradation |
|-------|-------------------|-------------------|
| Claude Opus 4.5 | ~100K tokens | ~180K tokens |
| Claude Sonnet 4.5 | ~80K tokens | ~150K tokens |

**Regel**: Bei ~80% des Thresholds proaktiv komprimieren!

### Hydrate mit Context Budget

```
HYDRATE mit Budget-Awareness:

1. ESTIMATE Session-Komplexität:
   - Einfacher Task → Budget: 50K tokens
   - Komplexer Task → Budget: 100K tokens
   - Multi-Step → Budget: 150K tokens

2. BUDGET für Memory reservieren:
   - Domain Memory: max 5K tokens (kompakt halten!)
   - Experiences: max 3K tokens (nur Top-3 relevant)
   - Graph Context: max 2K tokens (Primary Nodes only)
   - REST für Task-Arbeit!

3. Bei BUDGET-Überschreitung:
   - Nur NEUESTE Failures laden (nicht alle)
   - Experiences auf Top-1 reduzieren
   - Graph-Kontext skippen
```

### Degradation-Prävention bei Bootup

| Symptom | Prävention |
|---------|------------|
| Zu viel Memory geladen | SELECT: Nur aktives Projekt |
| Alte Experiences | COMPRESS: Decay-Filter strikt |
| Langes Projekt-JSON | WRITE: Progress auf letzte 5 Entries kürzen |
| Viele Graph-Nodes | SELECT: Nur Primary, keine Secondary |

### Kompakte Memory-Formate

**Progress-Entries** (statt verbose):
```json
// SCHLECHT (zu lang):
{"date": "2025-12-27", "action": "Ich habe das Feature X implementiert mit den folgenden Schritten...", "result": "Das Feature funktioniert jetzt komplett..."}

// GUT (kompakt):
{"d": "12-27", "a": "Feature X impl", "r": "OK", "n": "Tests"}
```

**Experience-Loading**:
```
// SCHLECHT: Alle 50 Experiences laden
// GUT: Top-3 nach effective_relevance, projekt-gefiltert
```

---

## Nicht vergessen!

- **Jede Session**: Memory lesen (Hydrate Pattern)
- **Jeder Task-Abschluss**: Progress loggen
- **Jeder Fehler**: Failure dokumentieren + Experience checken
- **Session-Ende**: Next Step vorschlagen

> "The agent is just a policy that transforms one memory state into another."

---

## Related

- [Experience Schema](_memory/experiences/SCHEMA.md) - Decay & Trust Level
- [Memory Decay Rule](.claude/rules/memory-decay.md) - Decay-Aware Filtering
- [Multi-Strategy Retrieval](knowledge/patterns/multi-strategy-retrieval-pattern.md) - 4-Way Retrieval
- [Context Window Ownership](knowledge/patterns/context-window-ownership-pattern.md) - Token Management
