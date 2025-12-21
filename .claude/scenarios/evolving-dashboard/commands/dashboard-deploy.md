---
description: Deployed das Evolving Dashboard zu Railway.app
model: sonnet
scenario: evolving-dashboard
---

Du deployest das Evolving Dashboard zu Railway.app.

## Ablauf

### 1. Projekt-Pfad laden
Lade Pfad aus `.claude/scenarios/evolving-dashboard/scenario.json`.

### 2. Pre-Deploy Checks
```bash
cd {project_path}

# Git Status prüfen
git status

# Uncommitted Changes?
```

Falls uncommitted Changes → User fragen ob committen.

### 3. Railway CLI prüfen
```bash
railway --version
```

Falls nicht installiert:
```bash
npm install -g @railway/cli
railway login
```

### 4. Railway Projekt prüfen
```bash
railway status
```

Falls kein Projekt verlinkt:
- Frage User: Neues Projekt oder bestehendes?
- `railway init` oder `railway link`

### 5. Environment Variables prüfen
Stelle sicher dass kritische Variables gesetzt sind:
- `NODE_ENV=production`
- Weitere projekt-spezifische Variables

### 6. Deploy
```bash
railway up
```

### 7. Post-Deploy Checks
- Health Check aufrufen
- WebSocket-Verbindung testen
- URL ausgeben

### 8. Status ausgeben
```
Deployment erfolgreich!

URL: {railway_url}
Health: ✅ OK
WebSocket: ✅ Connected

Dashboard ist live!
```

## Bei Fehlern

- Railway CLI Issues → @railway-expert-agent
- Build Fehler → @dashboard-codebase-agent
- WebSocket Issues → @dashboard-backend-agent + @railway-expert-agent

## Rollback

Falls Deployment fehlschlägt:
```bash
railway rollback
```
