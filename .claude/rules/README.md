# Claude Code Rules

Modulare Regeln für das Evolving System.

## Struktur

```
rules/
├── README.md                  # Diese Datei
├── core-principles.md         # AI-First, Sparring, 80/20
├── cross-reference-sync.md    # KRITISCH: 5 Dateien synchron
├── domain-memory-bootup.md    # KRITISCH: Memory Read/Write Ritual
├── auto-enhancement.md        # NEU: Automatisches Prompt-Enhancement
├── plan-archival.md           # Plan-Archivierung Workflow
├── workflow-detection.md      # Confidence-basierte Trigger
├── command-creation.md        # KRITISCH: Neue Commands
├── scenario-agents.md         # KRITISCH: Agent-Nutzung
├── knowledge-linking.md       # Proaktive Wissensvernetzung
├── experience-suggest.md      # Experience Memory Auto-Suggest
├── ultrathink.md              # Qualitätsprinzipien (Foundation, SSOT, Composition, Naming, Roadmap)
└── scenarios/
    └── evolving-dashboard.md  # Path: dashboard/**/* (Beispiel)
```

## Regel-Typen

### Core Rules (immer aktiv)
- `core-principles.md` - Grundlegende Arbeitsweise
- `cross-reference-sync.md` - Dokumenten-Synchronisation
- `domain-memory-bootup.md` - Memory Read/Write bei Session-Start
- `auto-enhancement.md` - **NEU**: Automatisches Prompt-Enhancement (Level 1-5)
- `plan-archival.md` - Plan-Management
- `workflow-detection.md` - Slash-Command Erkennung
- `command-creation.md` - Neue Commands erstellen
- `scenario-agents.md` - Agent-Nutzung in Szenarien
- `knowledge-linking.md` - Wissensvernetzung
- `experience-suggest.md` - Experience Memory Auto-Suggest
- `ultrathink.md` - Qualitätsprinzipien (5 Prinzipien + Roadmap)

### Path-Specific Rules (nur bei bestimmten Dateien)
- `scenarios/evolving-dashboard.md` - Gilt für `dashboard/**/*` (Beispiel)

## Path-Specific Syntax

```markdown
---
paths: dashboard/**/*
---

# Rule Content
...
```

Unterstützte Glob-Patterns:
- `**/*.ts` - Alle TypeScript Dateien
- `src/**/*` - Alles unter src/
- `{src,lib}/**/*.ts` - Multiple Patterns

## Neue Regel hinzufügen

1. Datei erstellen: `.claude/rules/{name}.md`
2. Optional: Path-Filter im Frontmatter
3. Diese README aktualisieren

## Priorität

1. Enterprise Policy (falls vorhanden)
2. Project Rules (`.claude/rules/`)
3. User Rules (`~/.claude/rules/`)
4. CLAUDE.md

Project Rules überschreiben User Rules.
