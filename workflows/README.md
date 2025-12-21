# Workflow Automation Engine

AI-nativer, deklarativer Workflow-Orchestrator für das Evolving-System.

## Quick Start

```bash
# Workflow ausführen (CLI)
/run-workflow morning-briefing

# Mit Variablen
/run-workflow idea-forge-full --variables '{"idea_input": "SaaS für X"}'

# Dry-Run (Simulation)
/run-workflow weekly-review --dry-run
```

## Struktur

```
workflows/
├── definitions/          # Workflow YAML-Dateien
│   ├── morning-briefing.yaml
│   ├── weekly-review.yaml
│   ├── inbox-processing.yaml
│   └── idea-forge-full.yaml
├── permissions/          # Berechtigungs-Profile
│   ├── default.yaml
│   ├── automation.yaml
│   └── idea-forge.yaml
├── preferences/          # User-Präferenzen
│   └── default.yaml
├── templates/            # Workflow-Templates
│   └── basic-workflow.yaml
├── schema/               # JSON Schemas
│   ├── workflow.schema.json
│   ├── permissions.schema.json
│   └── preferences.schema.json
├── logs/                 # Execution Logs
├── engine/               # Python Engine
│   └── __init__.py
└── README.md
```

## Verfügbare Workflows

| Workflow | Trigger | Beschreibung |
|----------|---------|--------------|
| `morning-briefing` | Cron 8:00 | Tägliche Übersicht |
| `weekly-review` | Cron Mo 9:00 | Ideen-Hygiene |
| `inbox-processing` | Watch `_inbox/` | Auto-Klassifizierung |
| `idea-forge-full` | Manual | Komplette Ideenentwicklung |

## YAML-Syntax

### Trigger

```yaml
trigger:
  type: manual    # Manuell ausführen
  type: cron      # Zeitgesteuert
  cron: "0 8 * * *"
  type: watch     # Datei-basiert
  watch: "_inbox/*"
  type: event     # Event-basiert
  event: "idea.created"
```

### Steps

```yaml
steps:
  # Prompt Step
  - name: Analysiere
    prompt: "..."
    model: sonnet
    store_as: result

  # Command Step
  - name: Liste Ideen
    command: /idea-list --format json
    store_as: ideas

  # Bash Step
  - name: Check Files
    bash: "ls -la"
    store_as: files

  # Agent Step
  - name: Validiere
    agent: idea-validator-agent
    prompt: "..."
    store_as: validation

  # Output Step
  - name: Speichern
    output: "_handoffs/{{date}}.md"
    template: "# Result\n{{result}}"
```

### Flow Control

```yaml
# Bedingung
- name: Nur wenn
  condition: "{{count}} > 0"
  prompt: "..."

# Loop
- name: Für jede Idee
  loop: "{{ideas}}"
  loop_as: idea
  steps:
    - prompt: "Check {{idea.title}}"

# Branch
- name: Verzweigung
  branch:
    - condition: "{{type}} == 'idea'"
      steps: [...]
    - condition: "{{type}} == 'learning'"
      steps: [...]
```

## Permissions

```yaml
# permissions/default.yaml
tools:
  always_allow: [Read, Glob, Grep]
  allow_with_constraints:
    - tool: Write
      paths: ["ideas/**"]
  never_allow:
    - tool: Bash
      patterns: ["rm -rf"]

file_access:
  readable: "**/*"
  writable: ["ideas/**"]
  protected: [".git/**"]
```

## Status

- [x] Schema Design
- [ ] Core Engine
- [ ] Knowledge Integration
- [ ] Safety & Control
- [ ] CLI & Dashboard
- [ ] Idea Forge Automation
- [ ] Advanced Triggers
- [ ] Analytics
