# Update Monitor

**Priorität**: MITTEL
**Trigger**: Session-Start (wenn > 7 Tage seit letztem Check), `/update-check` Command

---

## Konzept

Das System prüft regelmäßig auf neue Anthropic/Claude Code Features und integriert relevante Updates automatisch in die Knowledge Base.

---

## Automatischer Check-Flow

```
Session-Start
    │
    ▼
Lese _memory/system-updates.json
    │
    ├─ last_check < 7 Tage? → Skip
    │
    └─ last_check >= 7 Tage?
        │
        ▼
    WebSearch (max 3 Queries):
    - "Claude Code changelog 2026"
    - "MCP protocol updates 2026"
    - "Anthropic model updates 2026"
        │
        ▼
    Diff gegen known_features
        │
        ├─ Neue Features → Learning erstellen
        ├─ Geänderte Features → Learning updaten
        └─ Deprecations → Als stale markieren
        │
        ▼
    Timestamp aktualisieren
```

---

## Was gecheckt wird

| Kategorie | Quellen | Beispiel-Features |
|-----------|---------|-------------------|
| Claude Code | GitHub Releases, Changelog | Neue Hooks, Skills-Updates, MCP-Änderungen |
| MCP Protocol | modelcontextprotocol.io | Neue Tool-Typen, Resource-Updates |
| Claude Models | Anthropic Changelog | Neue Modelle, Capabilities |

---

## Token-Budget

**Maximal 2K Tokens** für Update-Check:
- 3 WebSearch Queries
- Kurze Analyse
- Optional: 1 Learning erstellen

Bei hohem Session-Context: Check überspringen.

---

## Update-Integration

### Bei neuen Features

```
1. Feature identifizieren
2. Relevanz für System prüfen:
   - Direkt nutzbar? → Learning + Implementation
   - Interessant? → Learning nur
   - Irrelevant? → Skip
3. Learning in knowledge/learnings/ erstellen
4. known_features in system-updates.json aktualisieren
```

### Bei Deprecations

```
1. Deprecation in existing Learnings markieren
2. valid_until setzen
3. Alternative dokumentieren
```

---

## Manueller Check: `/update-check`

Forciert Update-Check unabhängig vom Intervall:

```
/update-check
→ Sucht aktuelle Updates
→ Zeigt Diff zu known_features
→ Bietet Integration an
```

---

## State Management

`_memory/system-updates.json`:

```json
{
  "last_check": "2026-01-03T12:00:00Z",
  "known_features": { ... },
  "pending_updates": [],
  "update_history": [
    {
      "date": "2026-01-03",
      "type": "new_feature",
      "category": "claude-code",
      "feature": "hooks-v2",
      "action": "learning_created",
      "learning_id": "claude-code-hooks-v2"
    }
  ]
}
```

---

## Integration mit Session-Start

In `domain-memory-bootup.md` eingebaut:
- Nach Memory-Load
- Vor User-Interaktion
- Nur wenn Context < 60%

---

## Nicht vergessen

- Max 7-Tage-Intervall (nicht öfter)
- Token-Budget einhalten
- Nur relevante Updates integrieren
- History für Audit-Trail

---

## Related

- `domain-memory-bootup.md` - Session-Start Integration
- `/update-check` Command - Manueller Check
- `_memory/system-updates.json` - State
