# Sub-Agent Delegation

**Priorität**: HOCH
**Trigger**: Bei JEDER Anfrage (Vor-Analyse)
**Quelle**: Context Architecture Best Practice

---

## Konzept

Jeder Sub-Agent hat ein eigenes 200K Context Window. Main bekommt nur Summary zurück (~500 tokens).

```
Input analysieren (automatisch)
         │
    ┌────┴────┬────────────┐
    ▼         ▼            ▼
CRITICAL?  EXPLORATIV?  STANDARD
    │         │            │
    ▼         ▼            ▼
 DIRECT    FULL        HYBRID
   oder   DELEGATE    (fragen)
CHECKPOINT
```

---

## 3 Delegations-Modi

| Modus | Wann | Wie |
|-------|------|-----|
| **FULL DELEGATE** | Exploration, Bulk, Research | Agent arbeitet komplett, Summary zurück |
| **CHECKPOINT** | Wichtig + Groß | Agent: Phase→Report→Phase→Report |
| **DIRECT** | Kritisch, Entscheidungen, Klein | Kein Agent, Main Context |

### CHECKPOINT Pattern

```
Agent Phase 1: Verstehen
    ↓ [Checkpoint: "Gefunden: X, Y, Z. Weiter?"]
Agent Phase 2: Analysieren
    ↓ [Checkpoint: "Empfehlung: A. Einverstanden?"]
Agent Phase 3: Ausführen
    ↓ [Result]
```

---

## Automatische Intent-Erkennung

### CRITICAL Signale → DIRECT oder CHECKPOINT

- "wichtig", "kritisch", "muss perfekt"
- "production", "live", "deploy"
- "sicher", "security", "auth"
- "final", "letzte Version"
- "Architektur", "Design-Entscheidung"
- Domain: security, payment, legal

### EXPLORATIV Signale → FULL DELEGATE

- "finde", "suche", "zeig mir"
- "wie viele", "gibt es", "wo ist"
- "schau mal", "check mal"
- "analysiere [große Menge]"

### NICHT als Signal werten (nur Sprachstil)

- ~~"lass uns"~~ → User-Sprachstil
- ~~"wir"~~ → User-Sprachstil
- ~~"sollen wir"~~ → User-Sprachstil

Diese Phrasen sind **kein Indikator** für Kollaboration oder Kritikalität!

---

## Decision Matrix

| Task-Typ | Modus | Agent |
|----------|-------|-------|
| Quick fix (1-2 Files) | DIRECT | - |
| Code lesen (3+ Files) | FULL | Explore |
| Research (Web + Files) | FULL | Research |
| Multi-File Refactoring | CHECKPOINT | Explore/Plan |
| Debugging | FULL | debugger |
| Codebase Analysis | FULL/CHECKPOINT | Explore |
| Architektur-Entscheidung | DIRECT | - |
| Security-relevant | DIRECT | - |

---

## Hybrid-Verhalten bei Grenzfällen

| Situation | Verhalten |
|-----------|-----------|
| **Klar explorativ** | Automatisch FULL DELEGATE |
| **Klar kritisch** | Automatisch DIRECT |
| **Grenzfall** | Fragen: "Groß aber wichtig - Checkpoints oder direkt?" |

---

## Context-Übergabe an Agents

### Agent erhält IMMER

- Task-Beschreibung (explizit formuliert)
- Relevanter Projekt-Kontext (aktives Projekt aus `_memory/`)
- Bekannte Constraints (aus aktueller Conversation)
- Kritische Entscheidungen dieser Session

### Agent erhält NICHT

- Volle Conversation History (zu lang, irrelevant)
- Alle User Preferences (nur task-relevante)
- Unrelated Context (andere Projekte etc.)

---

## Agent-Fehlerbehandlung

**KRITISCH**: Stilles Überspringen von Files/URLs ist NICHT akzeptabel.

### Fehler-Typen

| Fehler | Handling |
|--------|----------|
| File nicht lesbar | MELDEN + Task fehlgeschlagen |
| URL fetch failed | RETRY 1x, dann MELDEN |
| Timeout | MELDEN + Partial Results kennzeichnen |
| Permission denied | MELDEN + Alternativen vorschlagen |

### Agent MUSS zurückmelden

```json
{
  "success": false,
  "partial": true,
  "completed": ["file1.md", "file2.md"],
  "failed": [
    {"path": "file3.md", "error": "Permission denied"},
    {"url": "https://...", "error": "Timeout after retry"}
  ],
  "result": "Partial analysis based on 2/3 files..."
}
```

### Main-Reaktion auf Fehler

```
Agent meldet Fehler
        │
   ┌────┴────┐
   ▼         ▼
KRITISCH?  OPTIONAL?
   │         │
   ▼         ▼
RETRY     Akzeptiere
 oder     Partial +
SELBST    Warnung
 MACHEN   an User
```

### Beispiel-Meldung an User

```
"Agent konnte 2/5 URLs nicht laden:
 - example.com/api (Timeout)
 - internal.site/doc (403 Forbidden)

 Ergebnis basiert auf 3 Quellen. Reicht das oder soll ich
 die fehlenden manuell versuchen?"
```

---

## Ergebnis-Validierung

Nach Agent-Return:

1. **Fehler-Check**: Gab es failed items? → Entscheiden ob akzeptabel
2. **Vollständigkeits-Check**: Wurde alles bearbeitet was angefragt war?
3. **Plausibilitäts-Check**: Macht das Ergebnis Sinn?
4. **Bei Partial Results**: User informieren, Entscheidung überlassen

---

## Kosten-Bewusstsein

**User hat Max Plan** → Kosten irrelevant, Qualität priorisieren.

- Agents frei nutzen wenn sinnvoll
- Keine Sparmaßnahmen bei Model-Wahl
- Lieber mehr Agents parallel als sequentiell warten

---

## Feedback-System

### Experience-Typ: `delegation_eval`

Nach jeder Delegation speichern:

```json
{
  "type": "delegation_eval",
  "task_type": "codebase_search",
  "agent": "Explore",
  "mode": "FULL",
  "success": true,
  "user_correction": false,
  "info_loss": false,
  "notes": "Schnell, vollständig"
}
```

### Tracking-Felder

| Feld | Beschreibung |
|------|--------------|
| `task_type` | explore, analyze, research, debug, ... |
| `agent` | Explore, debugger, Plan, ... |
| `mode` | FULL, CHECKPOINT, DIRECT |
| `success` | true/false |
| `user_correction` | Musste User korrigieren? |
| `info_loss` | Wurde Info-Verlust bemerkt? |

### Auto-Auswertung

- **Trigger**: Alle 20 Delegationen ODER bei `/memory-stats`
- **Output**: "Delegation-Effectiveness: 85%. Explore-Agent funktioniert gut. CHECKPOINT bei Refactoring empfohlen (2x User-Korrektur)."
- **Anpassung**: Decision Matrix Schwellwerte justieren

---

## Integration

Diese Rule arbeitet zusammen mit:

| Rule | Bezug |
|------|-------|
| `context-budget-awareness.md` | Threshold-basierte Empfehlung bei hohem Context |
| `experience-suggest.md` | Nutzt delegation_eval für Verbesserungen |
| `clear-dont-compact.md` | Agents starten mit frischem Context |

---

## Beispiele

### Explorativ → FULL DELEGATE

```
User: "Finde alle API endpoints"

Claude (intern):
  Signal: "finde" → EXPLORATIV
  Aktion: FULL DELEGATE an Explore Agent

Claude: [spawnt Agent, erhält Summary]
  "Gefunden: 23 API Endpoints in 5 Dateien..."
```

### Kritisch → DIRECT

```
User: "Wichtige Architektur-Entscheidung für Auth"

Claude (intern):
  Signal: "wichtig", "Architektur" → CRITICAL
  Aktion: DIRECT (kein Agent)

Claude: [arbeitet direkt im Main Context]
```

### Grenzfall → CHECKPOINT

```
User: "Analysiere dieses große Repo gründlich"

Claude (intern):
  Signal: "analysiere" → EXPLORATIV
  Signal: "gründlich" → möglicherweise CRITICAL
  Entscheidung: CHECKPOINT (groß + wichtig)

Claude: "Das ist ein großes Repo. Ich schlage vor:
  - Phase 1: Struktur-Overview
  - Phase 2: Detailanalyse der Kernkomponenten
  - Checkpoint nach jeder Phase
  Einverstanden?"
```
