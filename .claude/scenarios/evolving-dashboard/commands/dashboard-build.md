---
description: Erstellt einen Production Build des Evolving Dashboards
model: haiku
scenario: evolving-dashboard
---

Du erstellst einen Production Build des Evolving Dashboards.

## Ablauf

### 1. Projekt-Pfad laden
Lade Pfad aus `.claude/scenarios/evolving-dashboard/scenario.json`.

### 2. Pre-Build Checks
```bash
cd {project_path}

# TypeScript Check
npm run type-check

# Lint
npm run lint
```

Falls Fehler → Stoppen und User informieren.

### 3. Build ausführen
```bash
npm run build
```

### 4. Build-Analyse
Nach erfolgreichem Build:
- Bundle Size prüfen
- Warnungen auflisten
- Empfehlungen geben

### 5. Status ausgeben
```
Production Build erfolgreich!

Bundle-Analyse:
- First Load JS: {size}
- Largest Chunks: {list}

Nächste Schritte:
- /dashboard-test - Tests vor Deploy
- /dashboard-deploy - Zu Railway deployen
```

## Bei Fehlern

- TypeScript Fehler → @dashboard-frontend-agent oder @dashboard-backend-agent
- Build Fehler → @dashboard-codebase-agent
- Performance Issues → @dashboard-codebase-agent
