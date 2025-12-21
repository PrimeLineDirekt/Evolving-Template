---
description: Zeigt alle verfügbaren Szenarien
model: haiku
---

Du zeigst alle verfügbaren Szenarien an.

## Ablauf

### 1. Szenarien laden
Lies `.claude/scenarios/index.json` für die Liste aller Szenarien.

### 2. Details sammeln
Für jedes Szenario, lies `scenario.json` für Details:
- display_name
- description
- status
- tech_stack (gekürzt)
- Anzahl components (agents, commands)

### 3. Übersicht ausgeben
```
## Verfügbare Szenarien

| Szenario | Beschreibung | Status | Agents | Commands |
|----------|--------------|--------|--------|----------|
| evolving-dashboard | Web Dashboard mit Terminal | active | 5 | 4 |
| ... | ... | ... | ... | ... |

**Aktives Szenario**: {active_scenario oder "Keins"}

## Commands
- /scenario {name} - Szenario aktivieren
- /scenario-create {name} - Neues Szenario erstellen
- /scenario-edit {name} - Szenario bearbeiten
```

### 4. Falls keine Szenarien
```
Keine Szenarien gefunden.

Erstelle ein neues Szenario mit:
/scenario-create {name}
```

## Plain-Text Trigger
- "zeig mir szenarien"
- "welche szenarien"
- "alle szenarien"
