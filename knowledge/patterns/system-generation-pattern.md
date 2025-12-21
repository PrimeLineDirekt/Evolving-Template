# System Generation Pattern

**Confidence**: 90%
**Status**: Production
**Created**: 2025-12-14

## Konzept

Automatische Generierung kompletter Multi-Agent Systeme aus Blueprints mit Knowledge Injection.

## Architektur

```
User Request
    │
    ▼
┌─────────────────────────────────────────────────────────────┐
│                    SYSTEM BUILDER                            │
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │   ANALYZER   │→ │  ARCHITECT   │→ │  GENERATOR   │       │
│  │   (Sonnet)   │  │   (Opus)     │  │   (Sonnet)   │       │
│  └──────────────┘  └──────────────┘  └──────────────┘       │
│         │                 │                 │                │
│         ▼                 ▼                 ▼                │
│    Blueprint          Architecture      File                 │
│    Matching           Design            Creation             │
│                                              │                │
│                                              ▼                │
│                                    ┌──────────────┐          │
│                                    │  VALIDATOR   │          │
│                                    │   (Haiku)    │          │
│                                    └──────────────┘          │
└─────────────────────────────────────────────────────────────┘
    │
    ▼
Generated System
├── CLAUDE.md
├── .claude/agents/
├── .claude/commands/
├── knowledge/patterns/
└── _memory/
```

## Komponenten

### 1. System Analyzer Agent
- **Model**: Sonnet
- **Input**: User-Beschreibung, verfügbare Blueprints
- **Output**: Blueprint-Match mit Confidence Score
- **Aufgabe**: Versteht Anforderung, findet passenden Blueprint

### 2. System Architect Agent
- **Model**: Opus
- **Input**: Blueprint, Domain, Customization
- **Output**: Architektur-Spezifikation
- **Aufgabe**: Designt Agent-Rollen, Model-Tiers, Dependencies

### 3. System Generator Agent
- **Model**: Sonnet
- **Input**: Architektur-Spec, Templates
- **Output**: Generierte Dateien
- **Aufgabe**: Instantiiert Templates, injiziert Knowledge

### 4. System Validator Agent
- **Model**: Haiku
- **Input**: Generierte Dateien, Architektur-Spec
- **Output**: Validation Report
- **Aufgabe**: Prüft Struktur, Referenzen, Vollständigkeit

## Blueprints

Blueprints sind erweiterte Scenarios mit:
- Detection Patterns (Keywords für Auto-Match)
- Generation Config (Struktur, Required Files)
- Knowledge Injection (welche Patterns/Learnings)
- Model Tiers (welcher Agent bekommt welches Model)

### Blueprint-Schema

```json
{
  "blueprint": {
    "id": "blueprint-id",
    "type": "advisory|research|workflow",
    "detection_patterns": {
      "keywords": ["keyword1", "keyword2"]
    }
  },
  "components": {
    "agents": [
      {"role": "specialist", "template": "specialist-agent.md"}
    ],
    "commands": [
      {"name": "main-command", "template": "workflow-command.md"}
    ]
  },
  "knowledge_injection": {
    "patterns": ["pattern-1", "pattern-2"],
    "learnings": ["relevant-learning"]
  },
  "generation": {
    "target_structure": ["agents/", "commands/", "knowledge/"]
  }
}
```

## Knowledge Injection

Das System injiziert automatisch relevantes Wissen:

1. **Patterns** - Wiederverwendbare Architektur-Patterns
2. **Learnings** - Best Practices aus anderen Projekten
3. **References** - Tool-Dokumentation

### Injection-Prozess

```python
def inject_knowledge(architecture, blueprint):
    patterns = blueprint.knowledge_injection.patterns

    for pattern in patterns:
        source = f"knowledge/patterns/{pattern}.md"
        target = f"{target_path}/knowledge/patterns/{pattern}.md"

        # Kopiere Pattern (trimmed version)
        copy_and_trim(source, target)
```

## Template Instantiation

Templates verwenden Placeholders:

| Placeholder | Beschreibung |
|-------------|--------------|
| `{PROJECT_NAME}` | Projekt-Name |
| `{DOMAIN}` | Domain (z.B. "steuer") |
| `{DATE}` | Generierungsdatum |
| `{AGENT_COUNT}` | Anzahl Agents |
| `{COMMAND_LIST}` | Liste der Commands |

## Validation Rules

| Check | Beschreibung | Severity |
|-------|--------------|----------|
| Structure | Alle Ordner vorhanden | Critical |
| Required Files | CLAUDE.md, README.md, scenario.json | Critical |
| Placeholders | Keine {PLACEHOLDER} verbleibend | Critical |
| References | Alle referenzierten Dateien existieren | Warning |
| Quality | CLAUDE.md > 100 Zeilen | Info |

## Best Practices

1. **Blueprint-First**: Immer mit Blueprint starten, Custom als Fallback
2. **Schrittweise Bestätigung**: User bei jedem Schritt informieren
3. **Knowledge Trimming**: Nur essentielle Teile der Patterns injizieren
4. **Validation vor Commit**: Immer validieren vor "fertig" melden
5. **Standalone Systems**: Generierte Systeme haben keine Runtime-Dependency

## Limitations

- Blueprints sind Shortcuts, nicht Limitierungen
- Custom Systems ohne Blueprint möglich (mehr Aufwand)
- Knowledge Injection nur für dokumentierte Patterns
- Kein automatisches Testing der generierten Systeme

## Related

- `.claude/blueprints/` - Blueprint-Definitionen
- `.claude/agents/system-*-agent.md` - Builder-Agents
- `.claude/templates/generated-system/` - Generation Templates
- `.claude/commands/create-system.md` - Command-Dokumentation
