# Claude Code Rules

## Tiered Structure (Token-optimiert)

```
rules/
├── core-principles.md        # CORE: Arbeitsweise
├── workflow-detection.md     # CORE: Command-Erkennung
├── domain-memory-bootup.md   # CORE: Session-Start
├── on-demand/                # Kontextabhängig geladen
│   ├── debugging/            # observe-before-editing, evidence-before-claims
│   ├── memory/               # experience-suggest, memory-decay
│   ├── creation/             # command-creation, ultrathink
│   └── ...                   # 20+ weitere Rules
└── scenarios/
    ├── evolving-dashboard.md
    └── auswanderungs-ki.md
```

## Loading-Verhalten

| Ordner | Auto-Load | Wann |
|--------|-----------|------|
| `rules/*.md` | JA | Session-Start |
| `rules/on-demand/` | NEIN | Via Context Router |
| `rules/scenarios/` | NEIN | Bei Path-Match |

## On-Demand Rules laden

Context Router in `_graph/cache/context-router.json` bestimmt welche Rules bei welchen Keywords geladen werden.

## Neue Regel

1. Datei in `on-demand/` erstellen (NICHT root!)
2. Nur echte Core-Rules gehören in root
