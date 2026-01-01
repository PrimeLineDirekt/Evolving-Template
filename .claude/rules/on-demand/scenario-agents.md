# Szenario-Agent-Nutzung

**Priorität**: KRITISCH

Regeln für die Nutzung von Agents innerhalb aktiver Szenarien.

## Wann gilt diese Regel?

- Ein Szenario ist explizit aktiviert (`/scenario {name}`)
- Arbeit findet in einem Szenario-Projekt statt (z.B. `dashboard/`)

## VOR Code-Arbeit: Agent lesen

| Aufgabe | Agent |
|---------|-------|
| Frontend-Arbeit | `{scenario}/agents/frontend-agent.md` |
| Backend-Arbeit | `{scenario}/agents/backend-agent.md` |
| Architektur | `{scenario}/agents/codebase-agent.md` |
| Tests | `{scenario}/agents/testing-agent.md` |
| Deployment | `{scenario}/agents/deployment-agent.md` |

## Agent-Patterns anwenden

1. Code nach Agent-Best-Practices schreiben
2. Agent-Checklisten durchgehen
3. Agent-Output-Formate nutzen

## NACH Code-Arbeit: Review

- Codebase-Agent Architektur-Checklist durchgehen
- Code-Qualität prüfen
- Verbesserungen vorschlagen

## Workflow-Beispiel

```
User: "Erstelle Terminal Component"
  ↓
Claude:
  1. Lies frontend-agent.md
  2. Nutze Agent-Patterns (xterm.js Setup, etc.)
  3. Implementiere nach Best Practices
  4. Review mit codebase-agent Checklist
```

## Merksatz

**Agents sind Experten - nutze sie!**
