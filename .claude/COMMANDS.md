# Evolving Command Reference

**Total Commands**: 34
**Last Updated**: 2025-12-22

---

## Quick Reference

| Command | Zweck | Model |
|---------|-------|-------|
| `/opus` | Maximum Quality | opus |
| `/opus+` | Opus + Ultrathink | opus |
| `/sonnet` | Balanced Performance | sonnet |
| `/haiku` | Fast & Cheap | haiku |
| `/idea-new` | Neue Idee erfassen | sonnet |
| `/idea-work` | An Idee arbeiten | opus |
| `/idea-list` | Ideen-Übersicht | haiku |
| `/idea-connect` | Synergien finden | opus |
| `/sparring` | Brainstorming (7 Modi) | opus |
| `/think` | Mental Models (8 Frameworks) | opus |
| `/debug` | Systematisches Debugging | sonnet |
| `/knowledge-add` | Wissen hinzufügen | haiku |
| `/knowledge-search` | KB durchsuchen | haiku |
| `/project-add` | Projekt dokumentieren | sonnet |
| `/project-analyze` | Codebase analysieren | opus |
| `/analyze-repo` | GitHub Repo analysieren | opus |
| `/repo-screen` | Quick Relevanz-Check für Repos | haiku |
| `/inbox-process` | Inbox verarbeiten | haiku |
| `/onboard-process` | Onboarding verarbeiten | sonnet |
| `/whats-next` | Session Handoff | haiku |
| `/system-health` | System-Diagnostik | haiku |
| `/create-agent` | Agent erstellen | haiku |
| `/create-command` | Command erstellen | haiku |
| `/create-hook` | Hook erstellen | haiku |
| `/create-skill` | Skill erstellen | haiku |
| `/create-prompt` | Optimierten Prompt erstellen & speichern | opus |
| `/run-prompt` | Gespeicherte Prompts ausführen | sonnet |
| `/scenario` | Szenario aktivieren | haiku |
| `/scenario-list` | Szenarien anzeigen | haiku |
| `/scenario-create` | Neues Szenario erstellen | sonnet |
| `/scenario-edit` | Szenario bearbeiten | sonnet |
| `/remember` | Experience speichern | haiku |
| `/recall` | Experiences suchen | haiku |
| `/memory-stats` | Experience Memory Statistiken | haiku |
| `/preferences` | User-Praeferenzen anzeigen | haiku |
| `/context` | Knowledge Graph Kontext laden | haiku |
| `/create-system` | Komplettes Multi-Agent System generieren | sonnet |

---

## Commands by Category

### Model Switcher (4)

Wechsle das AI-Modell für optimale Performance/Kosten.

#### `/opus`
**Zweck**: Switch zu Opus (Maximum Quality)
**Model**: opus
**Wann nutzen**: Komplexe Reasoning, wichtige Entscheidungen
```
/opus Erkläre die Architektur von...
```

#### `/opus+`
**Zweck**: Opus mit Extended Thinking (Ultrathink)
**Model**: opus
**Wann nutzen**: Maximales Reasoning, komplexe Analysen
```
/opus+ Entwickle eine Strategie für...
```

#### `/sonnet`
**Zweck**: Switch zu Sonnet (Balanced)
**Model**: sonnet
**Wann nutzen**: Standard-Tasks, gutes Preis-Leistungs-Verhältnis
```
/sonnet Implementiere diese Funktion...
```

#### `/haiku`
**Zweck**: Switch zu Haiku (Fast & Cheap)
**Model**: haiku
**Wann nutzen**: Einfache Tasks, schnelle Antworten
```
/haiku Was ist 2+2?
```

---

### Idea Management (4)

Erfasse, entwickle und vernetze deine Ideen.

#### `/idea-new`
**Zweck**: Neue Idee mit KI-Analyse erfassen
**Model**: sonnet
**Output**: `ideas/{category}/{id}.md`
**Features**:
- Automatische Kategorisierung
- Potential-Score (1-10)
- Markt-Analyse
- Skill-Matching

```
/idea-new SaaS für Freelancer Zeiterfassung
```

#### `/idea-work`
**Zweck**: An bestehender Idee arbeiten (Sparring)
**Model**: opus
**Agents**: idea-validator, idea-expander, idea-connector
**Features**:
- Multi-Agent Orchestration
- Tiefe Analyse
- Expansion & Validation

```
/idea-work
/idea-work idea-2024-001
```

#### `/idea-list`
**Zweck**: Übersicht aller Ideen mit Filtern
**Model**: haiku
**Filter**: status, category, potential

```
/idea-list
/idea-list status:active
/idea-list potential:8+
```

#### `/idea-connect`
**Zweck**: Synergien zwischen Ideen finden
**Model**: opus
**Features**:
- Cross-Idea Analysis
- Shared Resources
- Combination Opportunities

```
/idea-connect
/idea-connect idea-001 idea-002
```

---

### Thinking & Brainstorming (3)

Strukturiertes Denken und kreative Exploration.

#### `/sparring`
**Zweck**: Freies Brainstorming mit 7 Modi
**Model**: opus
**Modi**:
1. `brainstorm` - Ideen erweitern
2. `problem-solving` - Lösungen finden
3. `strategy` - Pläne entwickeln
4. `devils-advocate` - Kritisch hinterfragen
5. `explore` - Thema erkunden
6. `decide` - Entscheidung treffen
7. `reflect` - Rückblick

```
/sparring
/sparring problem-solving Wie skaliere ich...
```

#### `/think`
**Zweck**: Mental Models anwenden
**Model**: opus
**Frameworks**:
| Framework | Trigger | Best For |
|-----------|---------|----------|
| 80/20 | `pareto` | Prioritization |
| First Principles | `fp` | Innovation |
| Inversion | `inv` | Risk Analysis |
| SWOT | `swot` | Strategy |
| Eisenhower | `matrix` | Time Management |
| Pre-Mortem | `pm` | Risk Prevention |
| Second Order | `so` | Consequences |
| Opportunity Cost | `oc` | Decisions |

```
/think 80/20 Meine täglichen Tasks
/think swot Mein Business
/think premortem Product Launch
```

#### `/debug`
**Zweck**: Systematisches Debugging
**Model**: sonnet
**Process**:
1. Problem-Definition
2. Hypothesen bilden
3. Evidence Gathering
4. Root Cause Analysis
5. Fix entwickeln

```
/debug API gibt 500 Error
/debug Tests failen nach Update
```

---

### Knowledge Management (2)

Wissen speichern und wiederfinden.

#### `/knowledge-add`
**Zweck**: Wissen zur Knowledge Base hinzufügen
**Model**: haiku
**Categories**: learnings, patterns, prompts, resources

```
/knowledge-add
/knowledge-add learning
```

#### `/knowledge-search`
**Zweck**: Knowledge Base durchsuchen
**Model**: haiku
**Search**: Semantisch über alle Kategorien

```
/knowledge-search API Best Practices
/knowledge-search SEO Optimierung
```

---

### Project Management (4)

Projekte dokumentieren und analysieren.

#### `/project-add`
**Zweck**: Projekt in Knowledge Base dokumentieren
**Model**: sonnet
**Output**: `knowledge/projects/{name}/README.md`
**Extracts**: Tech Stack, Learnings, Patterns

```
/project-add
/project-add ~/code/my-project
```

#### `/project-analyze`
**Zweck**: Externe Codebase analysieren
**Model**: opus
**Agents**: codebase-analyzer, n8n-expert
**Features**:
- Architecture Mapping
- Dependency Analysis
- n8n Workflow Detection
- Context Persistence

```
/project-analyze ~/code/external-project
```

#### `/analyze-repo`
**Zweck**: GitHub Repository analysieren mit System-Mapping
**Model**: opus
**Agent**: github-repo-analyzer
**Features**:
- Dual-System Analysis (Repo vs. Evolving)
- Finding Kategorisierung (NEU/BESSER/ANDERS/REDUNDANT)
- Integration Roadmap
- SYSTEM-MAP Update

```
/analyze-repo https://github.com/owner/repo
/analyze-repo /path/to/local/repo
```

#### `/repo-screen`
**Zweck**: Quick Relevanz-Check für GitHub Repos (Phase 1 vor Deep Analysis)
**Model**: haiku
**Features**:
- Batch-fähig (mehrere URLs)
- README + Struktur-Check
- Relevanz: JA/NEIN + Kurze Begründung

```
/repo-screen https://github.com/owner/repo
/repo-screen [liste von URLs]
```

**Workflow**:
1. README fetchen
2. Relevanz-Indikatoren checken (Claude Code, MCP, Agents, etc.)
3. JA/NEIN + Grund ausgeben
4. Bei JA → `/analyze-repo` für Details

---

### Workflow Automation (3)

Automatisierte Verarbeitung.

#### `/inbox-process`
**Zweck**: Dateien aus _inbox/ verarbeiten
**Model**: haiku
**Process**:
1. Dateien scannen
2. Typ erkennen (Prompt, Learning, Project...)
3. Kategorisieren
4. Einpflegen
5. Original löschen (mit Bestätigung)

```
/inbox-process
```

#### `/onboard-process`
**Zweck**: Onboarding-Fragebogen verarbeiten
**Model**: sonnet
**Input**: `_ONBOARDING.md`
**Updates**: personal/, projects/, ideas/

```
/onboard-process
```

#### `/whats-next`
**Zweck**: Session-Handoff erstellen
**Model**: haiku
**Output**: `_handoffs/YYYY-MM-DD-{topic}.md`
**Features**:
- Was wurde erreicht
- Was ist offen
- Nächste Schritte
- Quick Summary für neue Session

```
/whats-next
```

---

### System & Creation (5)

System-Verwaltung und Komponenten-Erstellung.

#### `/system-health`
**Zweck**: System-Diagnostik
**Model**: haiku
**Checks**:
- Datei-Struktur
- Index-Konsistenz
- Broken Links
- Stats

```
/system-health
/system-health full
```

#### `/create-agent`
**Zweck**: Neuen Agent aus Template erstellen
**Model**: haiku
**Templates**: specialist, research, orchestrator
**Output**: `.claude/agents/{name}-agent.md`

```
/create-agent
/create-agent api-tester
```

#### `/create-command`
**Zweck**: Neuen Command aus Template erstellen
**Model**: haiku
**Templates**: workflow, analysis
**Output**: `.claude/commands/{name}.md`

```
/create-command
/create-command review-pr
```

#### `/create-hook`
**Zweck**: Neuen Hook aus Template erstellen
**Model**: haiku
**Templates**: post-tool-use, stop
**Output**: `.claude/hooks/{name}.sh`

```
/create-hook
/create-hook pre-commit
```

#### `/create-skill`
**Zweck**: Neuen Skill aus Template erstellen
**Model**: haiku
**Templates**: progressive, simple
**Output**: `.claude/skills/{name}/`

```
/create-skill
/create-skill data-analyzer
```

---

### Meta-Prompting (2)

Prompts erstellen, speichern und in frischem Kontext ausführen.

#### `/create-prompt`
**Zweck**: Optimierten Prompt erstellen und speichern
**Model**: opus
**Framework**: Prompt Pro (5-Level Hierarchy)
**Output**: `prompts/{NNN}-{name}.md`
**Features**:
- Deep Analysis (Complexity, Domain, Type)
- Technique Selection (Level 1-5)
- XML-strukturierte Prompts
- Quality Checklist

```
/create-prompt Analysiere meine Content-Strategie
/create-prompt Entwickle Marketing-Plan
```

#### `/run-prompt`
**Zweck**: Gespeicherte Prompts in Sub-Agent ausführen
**Model**: sonnet (oder wie im Prompt definiert)
**Features**:
- Frischer Kontext (kein Context-Bleeding)
- Single, Parallel, oder Sequential Execution
- Auto-Archive nach Ausführung

```
/run-prompt 004
/run-prompt seo
/run-prompt 004 005 006 --parallel
/run-prompt 004 005 006 --sequential
```

---

### Scenario Management (4)

Kontext-basierte Projekt-Bundles mit spezialisierten Agents.

#### `/scenario`
**Zweck**: Szenario aktivieren und Kontext laden
**Model**: haiku
**Features**:
- Lädt szenario-spezifische Agents
- Zeigt verfügbare Commands
- Aktiviert Plain-Text Trigger

```
/scenario evolving-dashboard
/scenario
```

#### `/scenario-list`
**Zweck**: Alle verfügbaren Szenarien anzeigen
**Model**: haiku

```
/scenario-list
```

#### `/scenario-create`
**Zweck**: Neues Szenario mit Agents und Commands erstellen
**Model**: sonnet
**Output**: `.claude/scenarios/{name}/`
**Features**:
- Interaktive Erstellung
- Agent-Templates nutzen
- Automatische workflow-patterns.md Updates

```
/scenario-create mobile-app
/scenario-create
```

#### `/scenario-edit`
**Zweck**: Bestehendes Szenario bearbeiten
**Model**: sonnet
**Features**:
- Agents hinzufügen/entfernen
- Commands hinzufügen/entfernen
- Konfiguration anpassen

```
/scenario-edit evolving-dashboard
```

---

## Model Distribution

```
Opus (7 commands - 27%):
  Complex reasoning, strategic thinking
  - /opus+, /sparring, /think, /idea-work,
  - /idea-connect, /project-analyze, /analyze-repo
  - /create-prompt

Sonnet (5 commands - 19%):
  Balanced tasks
  - /sonnet, /idea-new, /project-add,
  - /onboard-process, /debug, /run-prompt

Haiku (14 commands - 54%):
  Fast, simple tasks
  - All others
```

---

## Plain Text Triggers

Diese Commands können auch durch natürliche Sprache ausgelöst werden:

| Phrase | Command |
|--------|---------|
| "Ich habe eine Idee..." | `/idea-new` |
| "Lass uns an {Idee} arbeiten" | `/idea-work` |
| "Zeig meine Ideen" | `/idea-list` |
| "Finde Verbindungen" | `/idea-connect` |
| "Lass uns brainstormen" | `/sparring` |
| "Suche nach {topic}" | `/knowledge-search` |
| "Verarbeite die Inbox" | `/inbox-process` |
| "Analysiere {repo}" | `/analyze-repo` |
| "Check diese Repos" | `/repo-screen` |
| "Sind diese Repos relevant" | `/repo-screen` |
| "Erstelle ein System für..." | `/create-system` |
| "Generiere ein Multi-Agent System" | `/create-system` |

---

## Best Practices

### Intake Gate Pattern
Komplexe Commands sollten vor Ausführung validieren:
1. Input prüfen
2. Bei Bedarf nachfragen (AskUserQuestion)
3. Bestätigung einholen
4. Dann erst ausführen

→ Siehe `knowledge/patterns/intake-gate-pattern.md`

### Model Selection
- **Opus**: Wenn Qualität > Speed
- **Sonnet**: Standard für die meisten Tasks
- **Haiku**: Schnelle Queries, einfache Tasks

### Command Chaining
Commands können kombiniert werden:
```
/inbox-process
→ findet neues Projekt
→ "Soll ich /project-add ausführen?"

/analyze-repo github.com/...
→ findet Patterns
→ "Integriere {pattern}"
→ nutzt /create-* Commands
```

---

## Adding New Commands

1. Template nutzen: `/create-command`
2. In `.claude/commands/{name}.md` speichern
3. COMMANDS.md aktualisieren
4. SYSTEM-MAP.md aktualisieren
5. Claude Code neu starten

---

### System Building (1)

Generiere komplette Multi-Agent Systeme.

#### `/create-system`
**Zweck**: Generiert ein vollständiges Multi-Agent System in einem Ziel-Ordner
**Model**: sonnet (orchestriert opus/sonnet/haiku Agents)
**Agents**: system-analyzer, system-architect, system-generator, system-validator
**Blueprint**: multi-agent-advisory (weitere geplant)

**Features**:
- Automatische Blueprint-Erkennung basierend auf Beschreibung
- Knowledge Injection aus Evolving (Patterns, Learnings)
- Architektur-Design mit Model-Tiering
- Validierung des generierten Systems

```
/create-system ~/projects/advisory-system
/create-system ~/projects/legal-advisor --blueprint multi-agent-advisory
/create-system ~/projects/quick-test --dry-run
```

**Workflow**:
1. Analysiert Anforderung → Blueprint-Match
2. Customization → Agent-Rollen definieren
3. Architektur-Design → Model-Tiering
4. Generation → Alle Dateien erstellen
5. Validation → Struktur prüfen

**Output**: Vollständiges `.claude/` Setup mit Agents, Commands, CLAUDE.md

---

### Experience Memory (4)

Persistentes "Fake Memory" fuer Erfahrungen ueber Sessions hinweg.

#### `/remember`
**Zweck**: Experience speichern (Solution, Pattern, Decision, Workaround, Gotcha, Preference)
**Model**: haiku
**Output**: `_memory/experiences/exp-YYYY-NNN.json`
**Experience Types**:
- `solution` - Fehler + Fix mit Root Cause
- `pattern` - Erfolgreicher Ansatz
- `decision` - Architektur-Entscheidung
- `workaround` - Temporaerer Fix
- `gotcha` - Stolperfalle
- `preference` - User-Praeferenz

```
/remember
/remember solution
/remember decision
```

#### `/recall`
**Zweck**: Experiences suchen mit Filtern
**Model**: haiku
**Features**:
- Keyword-Suche
- Type-Filter (--type solution)
- Project-Filter (--project dashboard)
- Recent-Filter (--recent 7d)
- Auto-Suggest bei Fehlern

```
/recall typescript error
/recall --type solution api
/recall --project dashboard --recent 7d
```

#### `/memory-stats`
**Zweck**: Experience Memory Statistiken anzeigen
**Model**: haiku
**Features**:
- Counts pro Type
- Score-Verteilung
- Top Tags
- Cleanup-Pending

```
/memory-stats
/memory-stats full
```

#### `/preferences`
**Zweck**: User-Praeferenzen anzeigen und verwalten
**Model**: haiku
**Features**:
- Nach Kategorie gruppiert (workflow, code_style, architecture)
- Confidence-Tracking
- Add/Edit/Remove

```
/preferences
/preferences show code_style
/preferences add
```

**Plain Text Trigger**:
- "Merk dir das"
- "Was wissen wir ueber..."
- "Zeig meine Praeferenzen"

---

## Native Claude Code Commands (Nützlich für Evolving)

Diese sind **native Commands** von Claude Code selbst - keine Evolving-eigenen Workflows.

### Session Management

| Command | Zweck | Beispiel |
|---------|-------|----------|
| `/rename <name>` | Session benennen | `/rename project-work` |
| `/resume <name>` | Benannte Session fortsetzen | `/resume project-work` |
| `claude --resume <name>` | Von Terminal aus fortsetzen | `claude --resume my-project` |

**Use Case**: Projekt-spezifische Sessions mit persistentem Kontext.

### Browser & Tools

| Command | Zweck | Status |
|---------|-------|--------|
| `/chrome` | Browser-Kontrolle via Extension | Beta - [Setup](https://claude.ai/chrome) |
| `/stats` | Nutzungsstatistiken (Model, Streak) | Verfügbar |
| `/config` | Settings anpassen | Verfügbar |
| `/permissions` | Permission-Regeln verwalten | Verfügbar |

### Shortcuts

| Shortcut | Zweck |
|----------|-------|
| `Option + P` (macOS) | Model-Wechsel während Tippen |
| `Alt + P` (Linux/Win) | Model-Wechsel während Tippen |
| `Alt + T` | Thinking Mode Toggle |
| `Tab` | Prompt-Suggestion akzeptieren |
| `Ctrl + R` | History Search (bash-style) |
| `Alt + Y` | Yank-pop (kill ring cycle) |

### CLI Flags

```bash
claude --agent research-analyst     # Mit spezifischem Agent starten
claude --session-id my-session      # Custom Session ID
claude --resume project-work        # Session fortsetzen
```

**Tipp**: Kombiniere Named Sessions mit Domain Memory für maximale Persistenz.

---

## Related Documentation

- `START.md` - User Quick Start
- `.claude/CONTEXT.md` - Technical Context
- `.claude/SYSTEM-MAP.md` - System Inventory
- `knowledge/patterns/intake-gate-pattern.md` - Command Design Pattern
- `knowledge/learnings/claude-code-dec-2025-features.md` - Aktuelle Features

---

**Version**: 1.5
**Commands**: 34 (Evolving) + Native Claude Code Commands
**Categories**: 10
**Last Updated**: 2025-12-22
