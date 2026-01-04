# /knowledge-refresh

Validiert und aktualisiert bestehende Learnings und Patterns.

## Trigger-Patterns
- "knowledge refresh"
- "learnings validieren"
- "wissen aktualisieren"
- "stale learnings"

## Model: haiku (für Search) + sonnet (für Analyse)

## Workflow

### 1. Learnings sammeln

```
Lade alle Learnings aus knowledge/learnings/
Filter nach:
  - refresh_category (wenn --category)
  - last_validated > Intervall
  - valid_until nicht abgelaufen
```

### 2. Validierung durchführen

```
Für jedes Learning (max 5 pro Session):
  1. Prüfe Aktualität via WebSearch
  2. Vergleiche mit aktuellem Stand
  3. Klassifiziere: aktuell | geändert | deprecated
```

### 3. Updates anwenden

```
aktuell:
  → last_validated = heute

geändert:
  → Inhalt aktualisieren
  → last_validated = heute
  → change_history erweitern

deprecated:
  → valid_until = heute
  → deprecation_reason setzen
  → Alternative dokumentieren
```

### 4. Report ausgeben

```markdown
## Knowledge Refresh Report

**Geprüft**: 5 Learnings
**Aktuell**: 4
**Aktualisiert**: 1
**Deprecated**: 0

### Aktualisiert
- **claude-code-hooks**: Neue Hook-Typen hinzugefügt
  - Alt: 3 Hook-Typen
  - Neu: 5 Hook-Typen

### Nächste Refresh-Kandidaten
- react-server-components (in 5 Tagen fällig)
- typescript-5-features (in 12 Tagen fällig)
```

## Parameter

| Flag | Beschreibung |
|------|--------------|
| `--all` | Alle Kategorien prüfen |
| `--category=X` | Nur bestimmte Kategorie |
| `--stale` | Nur abgelaufene Learnings |
| `--dry-run` | Nur Report, keine Änderungen |
| `--limit=N` | Max N Learnings prüfen |

## Kategorien

| Kategorie | Intervall | Beispiele |
|-----------|-----------|-----------|
| claude-code | 30 Tage | Claude Code Features, MCP |
| api | 60 Tage | Claude API, Third-Party |
| framework | 90 Tage | React, Next.js, Python |
| general | 180 Tage | Best Practices, Patterns |

## Beispiele

```
/knowledge-refresh
→ Prüft stale Learnings (Standard: 5)

/knowledge-refresh --category=claude-code
→ Nur Claude Code Learnings

/knowledge-refresh --all --limit=10
→ Alle Kategorien, max 10 Learnings
```

## Learning-Metadata-Format

```yaml
---
title: Feature X Learnings
created: 2026-01-01
last_validated: 2026-01-03
valid_until: null
refresh_category: claude-code
confidence: 85
change_history:
  - "2026-01-03: Feature Y hinzugefügt"
---
```

## Token-Budget

- Max 5 Learnings pro Session (default)
- Pro Learning: 1 WebSearch + kurze Analyse
- Bei hohem Context: Limit auf 3 reduzieren

## Related

- `update-check.md` Command - Neue Features finden
- `knowledge-refresh-cycle.md` Rule - Refresh-Logik
- `memory-decay.md` Rule - Experience Decay
