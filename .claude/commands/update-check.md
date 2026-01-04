# /update-check

Prüft auf neue Anthropic/Claude Code Features und integriert relevante Updates.

## Trigger-Patterns
- "check for updates"
- "neue features"
- "anthropic updates"
- "claude code changelog"

## Model: haiku (für Search) + sonnet (für Analyse)

## Workflow

### 1. State laden

```
Lies _memory/system-updates.json
→ known_features
→ last_check
→ update_history
```

### 2. WebSearch ausführen

```
Queries (max 3):
1. "Claude Code changelog 2026 new features"
2. "MCP protocol updates 2026"
3. "Anthropic Claude model updates 2026"
```

### 3. Diff analysieren

```
Für jeden Fund:
  - Ist das Feature bereits in known_features?
  - Ist es neu?
  - Ist es relevant für unser System?
```

### 4. Updates integrieren

```
Bei neuen relevanten Features:
  1. Learning erstellen in knowledge/learnings/
  2. known_features aktualisieren
  3. update_history erweitern
```

### 5. Report ausgeben

```markdown
## Update Check Report

**Letzte Prüfung**: 2026-01-03
**Neue Features gefunden**: 2
**Integriert**: 1
**Übersprungen**: 1 (nicht relevant)

### Neu integriert
- **Claude Code Hooks v2**: Neue Hook-Typen für ...
  → Learning erstellt: claude-code-hooks-v2.md

### Übersprungen
- **Feature X**: Nicht relevant für unser Use Case
```

## Parameter

| Flag | Beschreibung |
|------|--------------|
| `--force` | Ignoriert Intervall, prüft sofort |
| `--dry-run` | Zeigt nur, erstellt keine Learnings |
| `--category=X` | Nur bestimmte Kategorie prüfen |

## Beispiele

```
/update-check
→ Standard-Check, nur wenn > 7 Tage

/update-check --force
→ Sofortiger Check

/update-check --category=claude-code
→ Nur Claude Code Updates
```

## Token-Budget

Max 2K Tokens für:
- 3 WebSearch Queries
- Analyse + Diff
- 1 Learning erstellen

Bei hohem Context (>70%): Warnung ausgeben, optional abbrechen.

## State nach Check

`_memory/system-updates.json` wird aktualisiert:
- `last_check` = jetzt
- `known_features` erweitert
- `update_history` ergänzt

## Related

- `update-monitor.md` Rule - Automatische Checks
- `knowledge-refresh.md` Command - Bestehende Learnings validieren
- `_memory/system-updates.json` - State
