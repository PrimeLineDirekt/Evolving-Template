# Token Sustainability

**Priorität**: HOCH
**Trigger**: Bei JEDEM Task automatisch evaluieren

---

## Prinzip

> Mehr Autonomie = Mehr Sub-Agents = Sauberer Main Context

Sub-Agents haben eigene 200K Context Windows. Jede Delegation entlastet den Main Agent.

---

## Architektur

```
┌─────────────────────────────────────────────────────┐
│              MAIN AGENT                              │
│              Context: 200K                           │
│              Aufgabe: Koordinieren, Entscheiden      │
│              NICHT: Alles selbst machen              │
└────────────────────┬────────────────────────────────┘
                     │
    ┌────────────────┼────────────────┬───────────────┐
    ▼                ▼                ▼               ▼
┌────────┐    ┌────────────┐    ┌─────────┐    ┌──────────┐
│ Explore │    │ debugger   │    │ Plan    │    │ general  │
│ Agent   │    │ Agent      │    │ Agent   │    │ purpose  │
│ 200K    │    │ 200K       │    │ 200K    │    │ 200K     │
└────┬────┘    └─────┬──────┘    └────┬────┘    └────┬─────┘
     │               │                │              │
     └───────────────┴────────────────┴──────────────┘
                           │
                     Summary zurück
                     (~500 Tokens)
```

---

## Aggressive Delegation Rule

```
WENN Task > 3 Dateien betrifft
ODER Task > 10 Tool-Calls braucht
ODER Recherche nötig ist
ODER Debugging komplex ist
→ IMMER an Sub-Agent delegieren
→ NICHT im Main Context machen
```

---

## Agent-Zuordnung

| Task-Typ | Agent | Warum |
|----------|-------|-------|
| Codebase durchsuchen | `Explore` | Schnell, focused |
| Fehler debuggen | `debugger` | Spezialisiert auf Errors |
| Komplexe Planung | `Plan` | Architektur-Fokus |
| Web Research | `general-purpose` | WebFetch + Analyse |
| Multi-File Änderungen | Mehrere parallel | Maximale Effizienz |

---

## Parallel Agent Dispatch

Bei großen Tasks mehrere Agents parallel spawnen:

```
Task: "Analysiere die gesamte Codebase"

Dispatch:
  Agent 1: Explore → src/components/
  Agent 2: Explore → src/lib/
  Agent 3: Explore → src/app/

Sammeln:
  3 Summaries → Main aggregiert
```

---

## Context Thresholds

| Context % | Verhalten |
|-----------|-----------|
| < 60% | Normal arbeiten |
| 60-69% | Mehr delegieren |
| 70-79% | Aggressive Delegation, Handoff erwägen |
| 80-89% | Nur noch delegieren, Handoff vorbereiten |
| ≥ 90% | STOPP, /whats-next, /clear |

---

## Was NICHT delegieren

- Kritische Entscheidungen (braucht User-Interaktion)
- Finale Bestätigungen
- Kurze, schnelle Fixes (< 3 Tool Calls)
- User-Kommunikation

---

## Summary-Format von Agents

Agents sollen kompakte Summaries zurückgeben:

```json
{
  "success": true,
  "files_analyzed": 15,
  "key_findings": [
    "Pattern X in 5 Dateien gefunden",
    "Issue Y in component Z"
  ],
  "recommendations": [
    "Empfehlung 1",
    "Empfehlung 2"
  ]
}
```

**Nicht:** 50 Zeilen Detail-Output
**Sondern:** Kompakte, actionable Summary

---

## Integration

- `context-warning.sh` Hook warnt bei hohem Context
- `autonomy-classifier.md` bestimmt Delegation-Modus
- `sub-agent-delegation.md` (besteht) für Details

---

## Beispiel

```
User: "Finde alle API Endpoints im Projekt"

SCHLECHT (Main Context füllen):
  - Main liest Datei 1
  - Main liest Datei 2
  - ... (20 Dateien)
  → Main Context: +40K Tokens

GUT (Delegation):
  - Main spawnt Explore Agent
  - Agent liest alle Dateien
  - Agent gibt Summary zurück
  → Main Context: +500 Tokens
```

---

## Metriken

Track in `_stats.json`:
- `delegation_count`: Wie oft delegiert
- `context_saved`: Geschätzte Token-Ersparnis
- `agent_success_rate`: Wie oft Agent erfolgreich
