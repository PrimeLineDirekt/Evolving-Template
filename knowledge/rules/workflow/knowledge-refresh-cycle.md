# Knowledge Refresh Cycle

**Priorität**: NIEDRIG
**Trigger**: `/knowledge-refresh` Command, periodisch (monatlich)

---

## Konzept

Learnings und Patterns werden über Zeit potenziell outdated. Diese Rule definiert wie Knowledge validiert und aktualisiert wird.

---

## Refresh-Kategorien

| Kategorie | Refresh-Intervall | Beispiele |
|-----------|-------------------|-----------|
| claude-code | 30 Tage | Hooks, MCP, API Changes |
| api | 60 Tage | Claude API, Third-Party APIs |
| framework | 90 Tage | React, Next.js, Python Libs |
| general | 180 Tage | Best Practices, Patterns |

---

## Refresh-Flow

```
/knowledge-refresh [kategorie]
    │
    ▼
Lade Learnings mit refresh_category = kategorie
    │
    ▼
Für jedes Learning:
    │
    ├─ last_validated < Intervall?
    │       │
    │       └─ Skip (noch aktuell)
    │
    └─ Validierung nötig?
            │
            ▼
        WebSearch: "{topic} 2026 changes"
            │
            ├─ Keine Änderungen → last_validated updaten
            ├─ Änderungen → Learning updaten + History
            └─ Deprecated → valid_until setzen
```

---

## Learning-Metadata

Jedes Learning sollte enthalten:

```yaml
---
title: Feature X
created: 2026-01-01
last_validated: 2026-01-01
valid_until: null  # oder Datum wenn deprecated
refresh_category: claude-code | api | framework | general
confidence: 85
---
```

---

## Validierungs-Aktionen

### Aktuell (keine Änderungen)

```
- last_validated = heute
- Nichts weiter
```

### Geändert

```
- Inhalt aktualisieren
- last_validated = heute
- confidence ggf. anpassen
- change_history: "2026-01-03: Feature X jetzt mit Y"
```

### Deprecated

```
- valid_until = heute
- deprecation_reason = "Ersetzt durch Z"
- Alternatives dokumentieren
- Experience mit type=gotcha erstellen
```

---

## Batch-Mode

```
/knowledge-refresh --all
→ Alle Kategorien prüfen (Zeit-intensiv!)

/knowledge-refresh --category=claude-code
→ Nur Claude Code Learnings

/knowledge-refresh --stale
→ Nur abgelaufene (> Intervall)
```

---

## Output-Format

```
## Knowledge Refresh Report

**Geprüft**: 12 Learnings
**Aktuell**: 10
**Aktualisiert**: 1
**Deprecated**: 1

### Aktualisiert
- [claude-code-hooks] Feature X jetzt mit Y

### Deprecated
- [old-api-pattern] Ersetzt durch neue API
```

---

## Token-Effizienz

- Max 5 Learnings pro Refresh-Session
- WebSearch nur wenn wirklich nötig
- Bei hohem Context: Skip oder minimieren

---

## Related

- `update-monitor.md` - Proaktive Updates
- `memory-decay.md` - Experience Decay
- `/knowledge-refresh` Command
