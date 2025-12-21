---
description: Startet den Development Server für das Evolving Dashboard
model: haiku
scenario: evolving-dashboard
---

Du startest den Development Server für das Evolving Dashboard.

## Ablauf

### 1. Projekt-Pfad prüfen
Prüfe ob der Projekt-Pfad in `.claude/scenarios/evolving-dashboard/scenario.json` gesetzt ist.

Falls nicht gesetzt:
- Frage den User nach dem Pfad
- Aktualisiere `scenario.json` mit dem Pfad

### 2. Dependencies prüfen
```bash
cd {project_path}
npm install  # Falls node_modules fehlt
```

### 3. Development Server starten
```bash
npm run dev
```

### 4. Status ausgeben
```
Dashboard Development Server gestartet!

URL: http://localhost:3000
Terminal WebSocket: ws://localhost:3000/api/terminal

Verfügbare Agents:
- @dashboard-frontend-agent
- @dashboard-backend-agent
- @dashboard-testing-agent
- @dashboard-codebase-agent

Commands:
- /dashboard-build - Production Build
- /dashboard-deploy - Deploy zu Railway
- /dashboard-test - Tests ausführen
```

## Bei Fehlern

Nutze @dashboard-codebase-agent für Dependency-Issues oder @dashboard-backend-agent für Server-Probleme.
