# Sub-Agent Delegation Pattern

**Kategorie**: Multi-Agent / Context Management
**Confidence**: 95% (Production-validated)
**Source**: Evolving System Rule + Practical Testing (2026-01-01)

---

## Kern-Konzept

Automatische Intent-basierte Delegation von Tasks an spezialisierte Agenten mit eigenem 200K Context Window. Main-Claude erhält nur kompaktes Summary (~500 tokens) zurück, spart massiv Context und ermöglicht parallele Execution.

**Grundidee**:
- EXPLORATIV/Bulk → Agent bekommt volle Autonomie
- KRITISCH/Klein → Direkter Main-Context
- Grenzfälle → Checkpoint-Pattern mit User-Validierung

---

## Die 3 Delegations-Modi

| Modus | Kriterium | Output |
|-------|-----------|--------|
| **FULL DELEGATE** | Explorativ, Bulk, Research | Agent arbeitet autonom, Summary zurück |
| **CHECKPOINT** | Groß UND wichtig | Phase→Report→Entscheidung→Phase |
| **DIRECT** | Kritisch ODER klein | Kein Agent, Main-Context |

---

## Intent Recognition

### CRITICAL-Signale → DIRECT oder CHECKPOINT

```
Keywords: "wichtig", "kritisch", "muss perfekt", "production",
          "security", "auth", "final", "Architektur"
Domains:  security, payment, legal, authentication
```

### EXPLORATIV-Signale → FULL DELEGATE

```
Keywords: "finde", "suche", "zeig mir", "wie viele", "gibt es",
          "schau mal", "check mal", "analysiere [große Menge]"
Intent:   Information Discovery, Bulk Processing
```

### NICHT als Signal werten

```
❌ "lass uns", "wir", "sollen wir"
   = Reine Sprachweise, kein Kritikalitäts-Indikator!
```

---

## Decision Matrix

| Task-Typ | Größe | Kritikalität | Modus |
|----------|-------|--------------|-------|
| Quick fix | 1-2 Files | Niedrig | DIRECT |
| Codebase-Suche | 3+ Files | Niedrig | FULL |
| Web Research | Multi-URL | Niedrig | FULL |
| Multi-File Refactoring | Viele | Mittel-Hoch | CHECKPOINT |
| Architektur-Entscheidung | Klein | Kritisch | DIRECT |
| Security-relevant | Jede | Kritisch | DIRECT |

---

## Wann anwenden?

### Anwenden ✓

- Explorativ Tasks (Suche, Discovery, Analyse)
- Bulk Operations (viele Dateien/URLs)
- Research-fokussiert (Web, Multi-Source)
- Context-Budget kritisch (>70%)
- Parallele Execution gewünscht

### Nicht anwenden ✗

- Kritische Entscheidungen
- Security-relevant
- Small, Quick Fixes (Overhead nicht wert)
- Production Deploys

---

## Fehlerbehandlung

**Kritisch**: Stilles Überspringen ist NICHT akzeptabel!

### Agent-Response Format

```json
{
  "success": true/false,
  "partial": true/false,
  "completed": ["file1", "file2"],
  "failed": [{"path": "file3", "error": "..."}],
  "result": "Analyse basiert auf 2/3 Quellen..."
}
```

### Main-Reaktion

| Situation | Aktion |
|-----------|--------|
| Kritisch + Fehler | RETRY oder SELBST MACHEN |
| Optional + Fehler | Partial akzeptieren + User warnen |
| Unbekannt | User fragen |

---

## Experience Memory Integration

Nach jeder Delegation `delegation_eval` speichern:

```json
{
  "type": "delegation_eval",
  "content": {
    "task_type": "codebase_search",
    "agent": "Explore",
    "mode": "FULL",
    "success": true,
    "user_correction": false,
    "info_loss": false
  }
}
```

**Auto-Auswertung** (alle 20 Delegationen):
- Effectiveness berechnen
- Decision Matrix Schwellwerte anpassen

---

## Praktisches Beispiel

```
User: "Finde alle Stellen mit veralteten Referenzen"

Intent-Analyse:
  Signal: "finde" → EXPLORATIV
  Task: Bulk-Suche
  → FULL DELEGATE zu Explore Agent

Ergebnis:
  - 5 Inkonsistenzen gefunden
  - 0 False Positives
  - ~500 Tokens statt ~5000

Experience: exp-2026-001 (success, effectiveness=100%)
```

---

## Context-Übergabe

### Agent erhält

- Explizite Task-Beschreibung
- Relevanter Projekt-Context aus `_memory/`
- Bekannte Constraints
- Kritische Entscheidungen dieser Session

### Agent erhält NICHT

- Volle Conversation History
- Alle User Preferences
- Unrelated Context

---

## Integration

| Rule | Zusammenspiel |
|------|---------------|
| `context-budget-awareness` | >70% Context → Delegation empfehlen |
| `experience-suggest` | delegation_eval für Verbesserungen |
| `clear-dont-compact` | Agents starten mit frischem Context |

---

## Related

- [Sub-Agent Delegation Rule](../../.claude/rules/sub-agent-delegation.md)
- [Context Budget Awareness](../../.claude/rules/context-budget-awareness.md)
- [Multi-Agent Orchestration Pattern](multi-agent-orchestration-pattern.md)
- [Context Window Ownership Pattern](context-window-ownership-pattern.md)

---

**Validated**: 2026-01-01 (exp-2026-001)
**Status**: Production-Ready
