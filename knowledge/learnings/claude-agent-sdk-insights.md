# Claude Agent SDK Insights

**Source**: GitHub Issues (anthropics/claude-agent-sdk-typescript)
**Type**: Technical Learning
**Confidence**: 85%
**Date**: 2025-12-10

---

## Overview

Key Learnings aus der Analyse von 49 offenen Issues im Claude Agent SDK Repository. Relevant für zukünftige SDK-Nutzung und Verständnis der Architektur-Entscheidungen.

---

## Critical Insight: Declarative Session Hooks

### Problem (Issue #83)

Session Hooks können **NICHT** programmatisch zur Laufzeit hinzugefügt werden.

```typescript
// ❌ FUNKTIONIERT NICHT
const session = new Session({
  hooks: {
    onToolCall: (tool) => console.log(tool)
  }
});
```

### Lösung

Hooks müssen **DECLARATIVE** in `settings.json` definiert werden:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": ["bash:.claude/hooks/pre-edit.sh"]
      }
    ],
    "PostToolUse": [
      {
        "matcher": ".*",
        "hooks": ["bash:.claude/hooks/post-tool.sh"]
      }
    ]
  }
}
```

### Implikation

- Hooks sind **Config**, nicht Code
- Änderungen erfordern Settings-Update, nicht Code-Deployment
- Passt zur 12-Factor Methodology (Config separate from Code)

---

## Cache Control Issues (Issue #89)

### Problem

Prompt Caching funktioniert nicht korrekt mit Subagents.

```
Main Agent (cached) → spawns → Subagent (NOT cached)
                                    ↓
                              Full API cost
```

### Workaround

- Cache-Control Headers manuell setzen
- Subagent-Kontext minimieren
- Kritische Context-Teile in Main Agent halten

### Status

Offenes Issue, kein Fix verfügbar (Stand: Dezember 2025)

---

## OpenTelemetry Integration (Issue #82)

### Problem

Kein automatisches Tracing/Telemetry Support.

### Lösung

Manuelle Hook-Integration erforderlich:

```bash
# .claude/hooks/telemetry-hook.sh
#!/bin/bash
# Log tool calls to external system
curl -X POST https://your-telemetry.com/events \
  -H "Content-Type: application/json" \
  -d "{\"tool\": \"$TOOL_NAME\", \"timestamp\": \"$(date -u +%Y-%m-%dT%H:%M:%SZ)\"}"
```

### Alternative

- Langfuse Integration (externe Lösung)
- Custom Logging in Hooks
- Wrapper um SDK Calls

---

## Weitere Issues (Zusammenfassung)

| Issue | Problem | Status |
|-------|---------|--------|
| #83 | Declarative Hooks Only | By Design |
| #89 | Cache Control + Subagents | Open |
| #82 | No Auto-Telemetry | Open |
| #76 | Memory Leaks bei langen Sessions | Open |
| #71 | Rate Limiting nicht transparent | Open |

---

## Relevanz für Evolving

### Aktuell

| Bereich | Impact |
|---------|--------|
| **Hooks** | ✅ Bereits declarative in settings |
| **Subagents** | ⚠️ Cache-Bewusstsein bei Task Tool |
| **Telemetry** | ⚠️ Manuell wenn nötig |

### Zukünftig (wenn Agent SDK genutzt)

1. **Hooks-Design**: Von Anfang an declarative planen
2. **Caching-Strategie**: Main Agent Context maximieren
3. **Observability**: Eigene Telemetry-Hooks vorbereiten

---

## Key Takeaways

1. **Declarative > Programmatic**: SDK erzwingt Config-basierte Hooks
2. **Caching-Limitierungen**: Subagents haben separate Cache-Contexts
3. **Telemetry selbst bauen**: Kein Auto-Support, aber Hooks ermöglichen es
4. **SDK ist jung**: Viele Features noch in Entwicklung

---

## Related

- [Anthropic Advanced Tool Use](anthropic-advanced-tool-use.md) - Tool Use Features
- [12-Factor Agents Framework](12-factor-agents-framework.md) - Config vs Code Prinzip

---

**Navigation**: [← Learnings](README.md) | [Knowledge Index](../index.md)
