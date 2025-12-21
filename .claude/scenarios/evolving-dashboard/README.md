# Evolving Dashboard

Web-basiertes Dashboard für das Evolving Knowledge System mit integriertem Claude Code Terminal.

## Konzept

```
┌─────────────────────────────────────────────────────────┐
│  EVOLVING DASHBOARD                              [─][□][×]│
├─────────────────────────┬───────────────────────────────┤
│                         │                               │
│  📦 COMMANDS            │   $ claude                    │
│  ┌─────────────────┐    │   > Bereit für Aufgaben      │
│  │ /idea-new       │    │   _                           │
│  │ Neue Idee       │    │                               │
│  └─────────────────┘    │                               │
│  ┌─────────────────┐    │                               │
│  │ /knowledge-add  │    │                               │
│  │ Wissen hinzu    │    │                               │
│  └─────────────────┘    │                               │
│                         │                               │
│  🤖 AGENTS              │                               │
│  ┌─────────────────┐    │                               │
│  │ idea-validator  │    │                               │
│  │ Ideen prüfen    │    │                               │
│  └─────────────────┘    │                               │
│                         │                               │
│  KACHELN (Guide)        │   TERMINAL (Claude Code)      │
└─────────────────────────┴───────────────────────────────┘
```

## Tech Stack

- **Frontend**: Next.js 15, React 19, TypeScript, Tailwind CSS
- **Terminal**: xterm.js + WebSocket + node-pty
- **Deployment**: Railway.app

## Features

### Terminal (Rechts)
- Echtes Terminal im Browser via xterm.js
- WebSocket-Verbindung zum Backend
- Claude Code direkt nutzbar
- Volle Shell-Funktionalität

### Kachel-System (Links)
- Übersicht aller Commands mit Beschreibung
- Übersicht aller Agents mit Beschreibung
- Übersicht aller Skills
- Klickbar → Command/Info wird ins Terminal eingefügt

## Agents

| Agent | Expertise |
|-------|-----------|
| `dashboard-frontend-agent` | Next.js, React, xterm.js, Tailwind |
| `dashboard-backend-agent` | API Routes, WebSocket, node-pty |
| `railway-expert-agent` | Railway.app Deployment, Config, Domains |
| `dashboard-testing-agent` | Jest, Playwright, E2E Tests |
| `dashboard-codebase-agent` | Projekt-Struktur, Architektur, Code Review |

## Commands

| Command | Zweck |
|---------|-------|
| `/dashboard-dev` | Development Server starten |
| `/dashboard-build` | Production Build erstellen |
| `/dashboard-deploy` | Zu Railway deployen |
| `/dashboard-test` | Tests ausführen |

## Architektur

```
evolving-dashboard/
├── app/                    # Next.js App Router
│   ├── page.tsx           # Dashboard Hauptseite
│   ├── layout.tsx         # Root Layout
│   └── api/
│       └── terminal/      # WebSocket Endpoint
├── components/
│   ├── Terminal/          # xterm.js Wrapper
│   ├── TileGrid/          # Kachel-System
│   └── Sidebar/           # Navigation
├── lib/
│   ├── terminal.ts        # Terminal Logic
│   └── evolving.ts        # Evolving System Integration
└── public/
```

## Deployment

1. Railway.app Projekt erstellen
2. GitHub Repo verbinden
3. Environment Variables setzen
4. Deploy
