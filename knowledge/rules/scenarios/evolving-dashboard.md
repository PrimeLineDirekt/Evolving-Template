---
paths: dashboard/**/*
---

# Evolving Dashboard Rules

Path-spezifische Regeln für Arbeit im Dashboard-Verzeichnis.

## Tech Stack

- **Frontend**: Next.js 15, React 19, TypeScript, Tailwind CSS
- **Terminal**: xterm.js, node-pty, WebSocket
- **Backend**: Next.js Custom Server

## Agents nutzen

| Aufgabe | Agent |
|---------|-------|
| React Components | @.claude/scenarios/evolving-dashboard/agents/dashboard-frontend-agent.md |
| API/WebSocket | @.claude/scenarios/evolving-dashboard/agents/dashboard-backend-agent.md |
| Tests | @.claude/scenarios/evolving-dashboard/agents/dashboard-testing-agent.md |
| Architektur | @.claude/scenarios/evolving-dashboard/agents/dashboard-codebase-agent.md |

## Commands

- `/dashboard-dev` - Development Server starten
- `/dashboard-build` - Production Build
- `/dashboard-test` - Tests ausführen

## Wichtige Patterns

1. **TileGrid-Guide** (75% der UI)
   - 48 Features in 10 Kategorien
   - Klickbare Tiles für Actions

2. **Chat Panel** (25% der UI)
   - Toggle & Resize
   - Claude Code Integration

## Sicherheit

**Nur lokal nutzbar!** Terminal-Zugriff = zu hohes Risiko für Online-Deployment.

## Projekt-Pfad

```
{EVOLVING_PATH}/dashboard/
```
