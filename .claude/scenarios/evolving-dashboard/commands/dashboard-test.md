---
description: Führt Tests für das Evolving Dashboard aus
model: haiku
scenario: evolving-dashboard
---

Du führst Tests für das Evolving Dashboard aus.

## Ablauf

### 1. Projekt-Pfad laden
Lade Pfad aus `.claude/scenarios/evolving-dashboard/scenario.json`.

### 2. Test-Modus abfragen
Frage den User:
- **Quick** - Nur Unit Tests (< 30s)
- **Full** - Unit + Integration Tests (< 2min)
- **E2E** - Inklusive Playwright E2E Tests (< 5min)
- **Coverage** - Full + Coverage Report

### 3. Tests ausführen

#### Quick Mode
```bash
cd {project_path}
npm run test -- --watch=false
```

#### Full Mode
```bash
npm run test
npm run test:integration
```

#### E2E Mode
```bash
npm run test
npm run test:integration
npm run test:e2e
```

#### Coverage Mode
```bash
npm run test:coverage
```

### 4. Ergebnisse analysieren

#### Bei Erfolg
```
Tests erfolgreich!

Unit Tests: ✅ {passed}/{total}
Integration: ✅ {passed}/{total}
E2E: ✅ {passed}/{total}

Coverage:
- Statements: {x}%
- Branches: {x}%
- Functions: {x}%
- Lines: {x}%
```

#### Bei Fehlern
- Fehler auflisten
- Betroffene Dateien zeigen
- @dashboard-testing-agent für Hilfe anbieten

### 5. Empfehlungen
- Coverage unter Ziel? → Empfehle Tests
- Flaky Tests? → Markieren und fixen
- Langsame Tests? → Performance-Analyse

## Bei Fehlern

- Test Setup Issues → @dashboard-testing-agent
- Component Fehler → @dashboard-frontend-agent
- API Test Fehler → @dashboard-backend-agent
