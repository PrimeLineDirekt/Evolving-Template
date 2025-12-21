---
description: Erstellt ein neues Szenario mit Agents, Commands und Konfiguration
model: sonnet
argument-hint: [scenario-name]
---

Du erstellst ein neues Szenario mit Agents, Commands und Konfiguration.

## Ablauf

### 1. Name ermitteln
Falls `$ARGUMENTS` gegeben → nutze als Szenario-Name (kebab-case)
Falls nicht → Frage nach Name

### 2. Basis-Infos sammeln
Frage den User:
1. **Display Name** - Wie soll das Szenario heißen?
2. **Beschreibung** - Was ist der Zweck?
3. **Tech Stack** - Welche Technologien? (Frontend, Backend, Deployment)
4. **Welche Agents** - Welche Expertise wird benötigt?

### 3. Verzeichnis erstellen
```bash
mkdir -p .claude/scenarios/{name}/{commands,agents,skills,knowledge}
```

### 4. scenario.json erstellen
Erstelle `.claude/scenarios/{name}/scenario.json` mit:
- Gesammelten Infos
- Leeren Component-Arrays (werden gefüllt)
- Status: "draft"

### 5. README.md erstellen
Erstelle `.claude/scenarios/{name}/README.md` mit:
- Projekt-Beschreibung
- Tech Stack
- Architektur-Skizze (ASCII)
- Agent-Übersicht (Platzhalter)
- Command-Übersicht (Platzhalter)

### 6. Agents erstellen
Für jeden gewünschten Agent:
- Nutze Template-Struktur aus bestehenden Agents
- Passe an Domain/Expertise an
- Speichere in `.claude/scenarios/{name}/agents/`
- Aktualisiere scenario.json components.agents

### 7. Basis-Commands erstellen
Erstelle Standard-Commands:
- `{name}-dev.md` - Development Server
- `{name}-build.md` - Build
- `{name}-deploy.md` - Deployment
- `{name}-test.md` - Testing

### 8. Registry aktualisieren
Füge Szenario zu `.claude/scenarios/index.json` hinzu.

### 9. Workflow-Patterns erweitern
Füge Plain-Text Trigger für neue Commands zu `.claude/workflow-patterns.md` hinzu.

### 10. Bestätigung
```
Szenario "{name}" erstellt!

## Erstellt
- scenario.json
- README.md
- {x} Agents: {liste}
- {x} Commands: {liste}

## Nächste Schritte
1. /scenario {name} - Szenario aktivieren
2. Projekt-Pfad in scenario.json setzen
3. Agents nach Bedarf anpassen
4. Mit Development starten

Soll ich das Szenario jetzt aktivieren?
```

## Plain-Text Trigger
- "neues szenario"
- "szenario erstellen"
- "create scenario"
