---
description: Aktiviert ein Szenario und zeigt verfügbare Komponenten
model: haiku
argument-hint: [scenario-name]
---

Du aktivierst ein Szenario und lädst dessen Kontext.

## Ablauf

### 1. Szenario ermitteln
Falls `$ARGUMENTS` gegeben → nutze als Szenario-Name
Falls nicht → Zeige Liste verfügbarer Szenarien aus `.claude/scenarios/index.json`

### 2. Szenario laden
Lies `.claude/scenarios/{name}/scenario.json`

Falls nicht gefunden → Fehler mit Hinweis auf `/scenario-list`

### 3. Szenario aktivieren
Aktualisiere `.claude/scenarios/index.json`:
```json
{
  "active_scenario": "{name}"
}
```

### 4. Kontext ausgeben
```
Szenario "{display_name}" aktiviert!

## Projekt
- Name: {project.name}
- Tech Stack: {tech_stack}
- Deployment: {project.deployment.platform}

## Verfügbare Agents
{Für jeden Agent in scenario: Name + kurze Beschreibung aus Agent-Datei}

## Verfügbare Commands
{Für jeden Command in scenario: Name + kurze Beschreibung}

## Quick Start
{Zeige die wichtigsten Commands für dieses Szenario}

Nutze @{agent-name} um einen spezialisierten Agent zu involvieren.
```

### 5. README anbieten
Frage: "Soll ich die ausführliche Dokumentation zeigen?" (README.md des Szenarios)

## Plain-Text Trigger
- "aktiviere szenario"
- "wechsle zu {name}"
- "switch to {name}"
- "öffne projekt"
