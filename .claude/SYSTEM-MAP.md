# Evolving System Map

---

## SETUP: Status Line Script (v2 - Context Budget Awareness)

**File:** `~/.claude/statusline.sh`
**Make executable:** `chmod +x ~/.claude/statusline.sh`

**Format:** `145K 72% | dir | Opus | main *3 | ✓ Last → Current`

**Colors:**
- 🟢 Green: < 60% (normal)
- 🟡 Yellow: 60-79% (warning)
- 🔴 Red: ≥ 80% (critical, shows ⚠)

**Features:**
- Context % aus Token-Usage berechnet
- Schreibt % nach `/tmp/claude-context-pct-{session}.txt` für Hooks
- Liest Ledger (`_ledgers/CURRENT.md`) für Continuity-Anzeige
- Git-Status mit Change-Count

```bash
#!/bin/bash
# Claude Code StatusLine with Context Budget Awareness
# Format: 145K 72% | dir | Opus | main *3 | ✓ Last → Current
# Colors: Green (<60%) | Yellow (60-79%) | Red (≥80%)

input=$(cat)
project_dir="${CLAUDE_PROJECT_DIR:-$(pwd)}"

# Context % calculation
input_tokens=$(echo "$input" | jq -r '.context_window.current_usage.input_tokens // 0')
cache_read=$(echo "$input" | jq -r '.context_window.current_usage.cache_read_input_tokens // 0')
cache_creation=$(echo "$input" | jq -r '.context_window.current_usage.cache_creation_input_tokens // 0')
system_overhead=45000
total_tokens=$((input_tokens + cache_read + cache_creation + system_overhead))
context_size=$(echo "$input" | jq -r '.context_window.context_window_size // 200000')
context_pct=$((total_tokens * 100 / context_size))

# Write for hooks
echo "$context_pct" > "/tmp/claude-context-pct-${PPID}.txt"

# Color coding
if [[ "$context_pct" -ge 80 ]]; then
  ctx="\033[31m⚠ ${total_tokens}K ${context_pct}%\033[0m"  # Red
elif [[ "$context_pct" -ge 60 ]]; then
  ctx="\033[33m${total_tokens}K ${context_pct}%\033[0m"    # Yellow
else
  ctx="\033[32m${total_tokens}K ${context_pct}%\033[0m"    # Green
fi

# Model + Git + Ledger (abbreviated - full script in ~/.claude/statusline.sh)
echo -e "$ctx | dir | model | git | continuity"
```

**Vollständiges Script:** Siehe `~/.claude/statusline.sh` (128 Zeilen)

---

# Evolving System Map (continued)

**Letzte Aktualisierung**: 2026-01-05
**Version**: 2.4.0
**Zweck**: Persistente System-Dokumentation für Repository-Analyse und Integration

---

## System-Statistiken

**Aktuelle Zahlen:** `_stats.json` (Single Source of Truth)

Diese Datei enthält das **Detail-Inventar** aller Komponenten mit Beschreibungen, Dependencies und Metadaten.

---

## Knowledge Graph (_graph/)

**NEU in v1.3.0**: Unified Knowledge Graph für automatische Kontextbereitstellung.

| Datei | Inhalt | Beschreibung |
|-------|--------|--------------|
| schema.json | Schema | Graph-Schema Definition |
| nodes.json | ~148 Nodes | Alle Entities im System |
| edges.json | ~187 Edges | Beziehungen zwischen Entities |
| taxonomy.json | ~120 Tags | Unified Keyword-Taxonomie |
| index/by-type.json | Index | Nach Entity-Typ gruppiert |
| index/by-domain.json | Index | Nach Domain/Keywords |
| index/by-project.json | Index | Nach Projekt |
| cache/context-router.json | **28 Routes** | Keyword → Nodes Mapping (v2.3) |

**Zweck**: Bei Erstellung von Agents, Skills, Commands automatisch relevanten Kontext laden.

---

## Blueprints (.claude/blueprints/)

**v1.4.0+**: System-Builder & ML Project Blueprints für automatische Projekt-Generierung.

### System Builder Blueprints (Multi-Agent Systems)

| Blueprint | Typ | Beschreibung | Status |
|-----------|-----|--------------|--------|
| multi-agent-advisory | advisory | Multi-Experten-Beratungssystem (3-5 Agents + Orchestrator) | active |
| autonomous-research | research | Task Decomposition + Parallel Research | active |
| simple-workflow | workflow | Einfache 1-3 Agent Pipelines | active |

### ML & Project Blueprints (Extracted from KalyanM45/AI-Project-Gallery)

| Blueprint | Typ | Quelle | Beschreibung | Status |
|-----------|-----|--------|--------------|--------|
| end-to-end-ml-project | regression | Airbnb, Flight Fare, Gold Price | Umfassender ML-Projekt-Template mit DVC, MLFlow, Flask, Docker | active |
| web-scraping-project | data-collection | Article Web Scraper | API-basierter Web Scraping mit Beautiful Soup, Rate-Limiting, Persistence | active |
| timeseries-prediction-project | forecasting | Flight Fare, Gold Price | Time-Series Forecasting mit Stationarity Testing, Lag Features, Seasonal Patterns | active |
| business-intelligence-project | analytics | E-Commerce Data Analysis | BI Dashboard Template mit Power BI, EDA, Customer Segmentation, KPI Definitions | active |

**Zweck der Blueprints**:
- Automatische Projekt-Generierung mit `/create-system` Command
- Spezialisierte Architekturen für verschiedene Datentypen
- Vorkonfigurierte Best Practices und Patterns
- Knowledge Injection aus Evolving System
- Production-ready Strukturen

---

## Komponenten-Inventar

### Agents (.claude/agents/)

| Name | Typ | Domain | Zweck | Dependencies |
|------|-----|--------|-------|--------------|
| model-selector-agent | specialist | model-selection | Metacognitive Self-Assessment für Model-Auswahl | - |
| context-manager-agent | specialist | context-management | Context sharing, persistence, coordination | upstream: knowledge-synthesizer, research-analyst |
| idea-validator-agent | specialist | idea-validation | Feasibility, market, technical assessment | upstream: context-manager, research-analyst |
| idea-expander-agent | specialist | idea-expansion | Opportunity discovery, feature generation | upstream: idea-validator, research-analyst |
| idea-connector-agent | specialist | idea-connection | Cross-idea synergy discovery | upstream: knowledge-synthesizer, idea-validator |
| knowledge-synthesizer-agent | specialist | knowledge-synthesis | Multi-source integration, pattern recognition | upstream: research-analyst, context-manager |
| research-analyst-agent | research | multi-domain-research | Multi-source research with confidence scoring | upstream: context-manager |
| codebase-analyzer-agent | specialist | codebase-analysis | External codebase analysis, n8n detection | orchestrates: n8n-expert-agent |
| n8n-expert-agent | specialist | n8n-workflows | n8n workflow analysis, optimization | triggered by: codebase-analyzer |
| pitch-document-analyzer-agent | specialist | pitch-systems | Technische Dokumentation analysieren (dokumentbasiert) | - |
| pitch-content-categorizer-agent | specialist | pitch-systems | KB-Kategorisierung (dokumentbasiert) | upstream: pitch-document-analyzer |
| pitch-style-extractor-agent | specialist | pitch-systems | Stil-Extraktion aus PPTX (dokumentbasiert) | upstream: pitch-document-analyzer |
| system-analyzer-agent | specialist | system-building | Requirements Analysis, Blueprint Matching | - |
| system-architect-agent | specialist | system-building | Architecture Design, Agent Roles, Model Tiers | upstream: system-analyzer |
| system-generator-agent | specialist | system-building | File Generation, Template Instantiation | upstream: system-architect |
| system-validator-agent | specialist | system-building | Structure Validation, Quality Gates | upstream: system-generator |
| github-repo-analyzer-agent | specialist | codebase-analysis | GitHub Repo Analysis, Deep Dive Extraktion | - |
| dashboard-features-agent | specialist | dashboard | Feature Ideas Generation, UX/UI Assessment | upstream: dashboard-codebase-agent |
| fal-image-generator-agent | specialist | image-generation | FAL.ai Nano Banana Pro Elite Agent, ICS Framework, 20 Style-Kategorien | - |
| macro-data-collector-agent | orchestrator | market-analysis | Parallel Data Collection (7 Sources) | upstream: research-analyst |
| meta-analyst-agent | specialist | market-analysis | Hidden Patterns, Cui Bono, Narrative Detection | upstream: macro-data-collector, knowledge-synthesizer |
| pattern-recognizer-agent | specialist | market-analysis | Historical Patterns, Contrarian Signals | upstream: knowledge-synthesizer |
| forecast-synthesizer-agent | specialist | market-analysis | Scenario Modeling, Probability Forecasts | upstream: meta-analyst, pattern-recognizer, macro-economist |
| learning-optimizer-agent | specialist | market-analysis | Prediction Tracking, Model Refinement | upstream: forecast-synthesizer |
| market-technical-analyst-agent | specialist | market-analysis | Technical Indicators, Chart Analysis | - |
| macro-economist-agent | specialist | market-analysis | Liquidity Cycles, CPI Lag, Fed Policy | - |
| macro-orchestrator-agent | orchestrator | market-analysis | Agent Coordination, Report Synthesis | orchestrates: all macro-agents |

**Agent Type Distribution:**
- Specialist Agents: 22 (84.6%)
- Orchestrator Agents: 2 (7.7%)
- Research Agents: 1 (3.8%)
- System Builder Agents: 4 (orchestrated pipeline)

---

### Skills (.claude/skills/)

| Name | Typ | Zweck | Invocation |
|------|-----|-------|------------|
| template-creator | production | Template Creation für Agents, Commands, Hooks, Skills | `@template-creator` oder "erstelle einen agent" |
| prompt-pro-framework | production | 5-Level Prompt Engineering System | `@prompt-pro-framework` oder "erstelle prompt für" |
| research-orchestrator | production | Multi-domain Research mit Confidence Scoring | `@research-orchestrator` oder "research {topic}" |
| etsy-poster-creator | production | Viral-optimierte Etsy Listings mit SEO | `@etsy-poster-creator` oder "create etsy listing" |

**Skill Pattern:** Alle Skills nutzen Progressive Disclosure (reference.md + examples.md)

---

### Commands (.claude/commands/)

| Command | Zweck | Model | Agent/Skill |
|---------|-------|-------|-------------|
| `/opus` | Switch to Opus (maximum quality) | opus | - |
| `/opus+` | Opus + Ultrathink (maximum reasoning) | opus | - |
| `/sonnet` | Switch to Sonnet (balanced) | sonnet | - |
| `/haiku` | Switch to Haiku (fast & cheap) | haiku | - |
| `/idea-new` | Neue Idee mit KI-Analyse | sonnet | - |
| `/idea-work` | An Idee arbeiten (Sparring) | opus | idea-validator, idea-expander, idea-connector |
| `/idea-list` | Ideen-Übersicht mit Filtern | haiku | - |
| `/idea-connect` | Synergien zwischen Ideen finden | opus | - |
| `/sparring` | Freies Brainstorming (7 Modi) | opus | - |
| `/knowledge-add` | Wissen zur KB hinzufügen | haiku | - |
| `/knowledge-search` | Semantische KB-Suche | haiku | - |
| `/project-add` | Projekt dokumentieren | sonnet | - |
| `/project-analyze` | Codebase analysieren | opus | codebase-analyzer, n8n-expert |
| `/inbox-process` | Inbox automatisch verarbeiten | haiku | - |
| `/onboard-process` | Onboarding-Fragebogen verarbeiten | sonnet | - |
| `/create-agent` | Agent aus Template erstellen | haiku | template-creator |
| `/create-command` | Command aus Template erstellen | haiku | template-creator |
| `/create-hook` | Hook aus Template erstellen | haiku | template-creator |
| `/create-skill` | Skill aus Template erstellen | haiku | template-creator |
| `/compose-agent` | Dynamischer Agent aus Trait-System (480 Kombinationen) | sonnet | agent-factory |
| `/system-health` | System-Diagnostik | haiku | - |
| `/scenario` | Szenario aktivieren | haiku | - |
| `/scenario-list` | Szenarien anzeigen | haiku | - |
| `/scenario-create` | Neues Szenario erstellen | sonnet | - |
| `/scenario-edit` | Szenario bearbeiten | sonnet | - |
| `/analyze-pitch-docs` | Pitch-Dokumente analysieren | sonnet | pitch-document-analyzer, pitch-content-categorizer, pitch-style-extractor |
| `/create-system` | Komplettes Projekt-System generieren | sonnet | system-analyzer, system-architect, system-generator, system-validator |
| `/auto-model` | Automatische Model-Auswahl | haiku | model-selector-agent |
| `/pattern-scan` | Historical Pattern Matching | sonnet | pattern-recognizer-agent |
| `/learning-review` | Accuracy Metrics & Model Refinement | sonnet | learning-optimizer-agent |
| `/analyze-batch` | Batch Document Analysis | sonnet | - |
| `/security-review` | Security Code Review | opus | - |
| `/interview-plan` | Interview vor Implementation | opus | - |
| `/run-workflow` | Workflow ausführen | sonnet | - |
| `/macro-forecast` | 30-Tage Probability Forecast | opus | forecast-synthesizer-agent |
| `/market-analysis` | Deep Market Analysis | opus | macro-orchestrator-agent |

**Command Categories:**
- Model Switchers: 4
- Idea Management: 4
- Knowledge Management: 2
- Project Management: 4
- Scenario Management: 4
- Creation Tools: 5
- System Building: 1
- System Utilities: 3
- Brainstorming: 1
- Macro-Analyse: 5
- Development Tools: 3
- Workflow Execution: 1
- Experience Memory: 4
- External Projects: 1 (Schulung Pitch)

---

### Hooks (.claude/hooks/)

| Hook | Typ | Trigger | Zweck |
|------|-----|---------|-------|
| context-monitor.sh | StatusLine | Permanent | Session-Kosten & Dauer anzeigen |
| auto-cross-reference.sh | PostToolUse | Write/Edit | Master-Dokumente synchronisieren |
| session-summary.sh | Stop | Session-Ende | Session-Dokumentation erstellen |
| graph-update.sh | PostToolUse | Write/Edit | Knowledge Graph aktualisieren (Placeholder) |

---

### Rules (.claude/rules/)

| Rule | Typ | Zweck |
|------|-----|-------|
| core-principles.md | Core | AI-First, Sparring, 80/20, Chain of Thought |
| cross-reference-sync.md | Core (KRITISCH) | 5 Master-Dokumente synchron halten |
| proactive-doc-sync.md | Core (NEU) | Automatische Doc-Aktualisierung nach strukturellen Änderungen |
| plan-archival.md | Core | Plan-Archivierung Workflow |
| workflow-detection.md | Core | Confidence-basierte Slash-Command Erkennung |
| command-creation.md | Core (KRITISCH) | Neue Commands korrekt erstellen |
| scenario-agents.md | Core (KRITISCH) | Agent-Nutzung in Szenarien |
| knowledge-linking.md | Core | Proaktive Wissensvernetzung |
| observe-before-editing.md | Core | Outputs prüfen vor Code-Edits (Debugging-First) |
| index-at-creation.md | Core | Artifacts sofort indexieren, nicht Batch |
| context-budget-awareness.md | Core (NEU) | v3 Emergent Behavior: Parallelisierung bei High Context |
| explicit-identity.md | Core (NEU) | IDs durch Process-Boundaries durchreichen |
| idempotent-redundancy.md | Core (NEU) | Redundanz nur wenn idempotent |
| sub-agent-delegation.md | Core (NEU) | 3-Modi Delegation (FULL/CHECKPOINT/DIRECT) |
| scenarios/evolving-dashboard.md | Path-Specific | Regeln für dashboard/**/* |
| scenarios/auswanderungs-ki.md | Path-Specific | Regeln für Auswanderungs-KI-v2/**/* |

**Rule Types:**
- Core Rules: 28 (immer aktiv)
- Path-Specific Rules: 2 (nur bei bestimmten Dateien)

---

### Scenarios (.claude/scenarios/)

| Szenario | Beschreibung | Agents | Commands | Status |
|----------|--------------|--------|----------|--------|
| evolving-dashboard | TileGrid-Guide (48 Features) + Chat Panel mit Toggle & Resize (v2.0.0) | 5 | 3 | active |
| steuererklaerung-2024 | Experten-Team für Steuererklärung 2024 | 4 | 2 | active |
| workflow-engine | ARCHIVED - Over-Engineering, SDK reicht | 5 | 4 | archived |
| nhien-bistro | QR-Order System für NHIÊN Bistro, Da Nang | 3 | 3 | active |
| macro-analyse | WZRD Signals Market Analysis Dashboard | 7 | 5 | active |
| didit-medical-care | Medizinische Koordination Lombok → Jakarta | 3 | 2 | active |
| auswanderungs-ki | Python/LangGraph Multi-Agent System | - | - | active |

**Steuererklärung 2024 Agents:**
- steuerberater-agent (Optimierung, Werbungskosten, Sonderausgaben)
- steueranwalt-agent (Rechtssicherheit, Risiko-Ampel)
- software-experte-agent (SteuerSparErklärung Bedienung)
- steuer-koordinator-agent (Team-Orchestrierung)

**Steuererklärung 2024 Commands:**
- /steuer-beratung - Umfassende Team-Beratung
- /steuer-check - Schnelle Absetzbarkeits-Prüfung

**Evolving Dashboard Agents:**
- dashboard-frontend-agent (Next.js, React, xterm.js)
- dashboard-backend-agent (API, WebSocket, node-pty)
- railway-expert-agent (Railway.app Deployment)
- dashboard-testing-agent (Jest, Playwright)
- dashboard-codebase-agent (Architektur, Code-Qualität)

**Evolving Dashboard Commands:**
- /dashboard-dev - Development Server
- /dashboard-build - Production Build
- /dashboard-deploy - Railway Deployment
- /dashboard-test - Tests ausführen

**Workflow Engine Agents:**
- sdk-architect-agent (System Design, Architecture)
- python-engineer-agent (Backend Implementation)
- dashboard-engineer-agent (Frontend, React)
- qa-agent (Testing, Quality Assurance)
- code-reviewer-agent (Code Review, Best Practices)

**Workflow Engine Commands:**
- /workflow-design - Architektur planen
- /workflow-implement - Implementierung
- /workflow-test - Tests ausführen
- /workflow-review - Code Review

**Macro-Analyse Agents:**
- macro-data-collector-agent (7 API Sources parallel)
- market-technical-analyst-agent (Technical Indicators)
- macro-economist-agent (Liquidity, CPI, Fed)
- meta-analyst-agent (Hidden Drivers, Cui Bono)
- pattern-recognizer-agent (Historical Patterns)
- forecast-synthesizer-agent (Scenario Modeling)
- learning-optimizer-agent (Self-Improvement)
- macro-orchestrator-agent (Agent Coordination)

**Macro-Analyse Commands:**
- /market-analysis - Deep Analysis mit allen Agents
- /macro-forecast - 30-Tage Probability Forecast
- /pattern-scan - Historical Pattern Matching
- /learning-review - Accuracy Metrics
- /analyze-batch - Batch Document Analysis

**Didit Medical Care Agents:**
- medical-coordinator-agent (Krankenhaus-Kommunikation, OP-Planung)
- transport-coordinator-agent (Air Ambulance, Ground Transport)
- logistics-coordinator-agent (Unterkunft, Budget-Tracking)

**Didit Medical Care Commands:**
- /didit-status - Aktueller Projektstand
- /didit-next - Nächste Schritte

---

### Templates (.claude/templates/)

| Typ | Dateien | Zweck |
|-----|---------|-------|
| **Agents (8)** | specialist, research, orchestrator, advisor, system-builder, validator, creative, automation, dynamic | Agent-Erstellung + Trait-basierte Composition |
| **Commands** | workflow-command.md, analysis-command.md | Command-Erstellung |
| **Hooks** | post-tool-use.sh, stop-hook.sh | Hook-Erstellung |
| **Skills** | progressive-skill/, simple-skill/ | Skill-Erstellung |
| **Scenarios** | autonomous-research/, multi-agent-advisory/ | Szenario-Erstellung (Task Decomposition, Multi-Agent Advisory) |
| **Generated-System** | CLAUDE.md.template, README.md.template, scenario.json.template, memory-index.json.template | System-Generierung |
| **Patterns** | reusable-pattern.md | Pattern-Dokumentation |
| **Learnings** | project-learning.md | Learning-Erfassung |
| **Data-Aggregation** | multi-source-aggregator/ (6 files) | News Feeds, Trend Tracking, Knowledge Aggregation (Source: replicate/hype) |

---

### Agent Trait System (knowledge/agents/) 🆕

| Datei | Beschreibung |
|-------|--------------|
| trait-taxonomy.json | 10 Expertise × 8 Personality × 6 Approach = **480 Kombinationen** |
| voice-mappings.json | Personality → Voice Characteristics (Tone, Markers, Avoids) |
| disclaimers.json | Domain-spezifische Disclaimers (legal, security, medical) |

**Expertise (10)**: researcher, architect, engineer, analyst, strategist, legal*, creative, security*, communications, medical*

**Personality (8)**: precise, creative, cautious, direct, thorough, contrarian, empathetic, skeptical

**Approach (6)**: systematic, exploratory, iterative, parallel, adversarial, consultative

**Verwendung**: `/compose-agent <expertise> [personality] [approach]`

---

### Knowledge Base (knowledge/)

| Ordner | Dateien | Beschreibung |
|--------|---------|--------------|
| **projects/** | 37 | Projekt-Dokumentation (8 Projekte - siehe Key Knowledge Assets) |
| **plans/** | 1 | Geparkte Implementierungspläne |
| **learnings/** | 30 | Projekt-Erkenntnisse (inkl. Context Degradation, Skill Anti-Patterns, Notebook Audit Methodology) |
| **patterns/** | 46 | Wiederverwendbare Patterns (inkl. Research Orchestration, Systematic Debugging, Technical Code Review, Parallel Agent Dispatch) |
| **references/** | 6 | Self-Contained Tool References (claude-skills, mcp-servers, agent-templates, claude-flow, document-skills, claude-code-system-prompts) |
| **prompts/** | 24 | Prompt Library & Frameworks |
| **personal/** | 4 | User Profile, Skills, Instructions |
| **external-projects/** | 1 | Context-persistent Codebase Analysis (auswanderungs-ki-v2) |
| **_sources/** | 2 | Source Tracking & Archived externals |

**Key Knowledge Assets:**
- **8 Projekte:**
  - AI Poster Creation Hub (Live, Etsy/Midjourney/Pinterest)
  - KI Auswanderungs-Berater v1 (n8n, Phase 4)
  - Auswanderungs-KI v2.1 (Python/LangGraph, Production-Ready)
  - Macro-Analyse (FastAPI/Next.js, WZRD Signals Dashboard)
  - Document Dashboard (Next.js, RAG/ChromaDB)
  - Didit Medical Care (MVP)
  - Gold Price Prediction (ML Pipeline)
  - Schulung Pitch (Windenergie, wartet auf Samples)
- **Auswanderungs-KI v2.1 Tax KB**: 72 Dokumente, 621.326 Wörter, Phase 1-5 KOMPLETT
- 2 Frameworks: Prompt Pro 2.0, Idea Forge
- 18 Auswanderungs-KI Agent Patterns
- 48 Production Patterns (inkl. Research Orchestration, Systematic Debugging, Technical Code Review, Parallel Agent Dispatch, Resume Strategies, Safety Hooks, Four-Bucket Context, Hook Development Reference, Idempotent Redundancy, Explicit Identity, Multi-Agent Ultrathink, Ralph Wiggum Loop)
- 30 Learnings (inkl. Notebook Audit Methodology, Skill Creation TDD, Context Degradation Deep Dive, Skill Anti-Patterns Structure, Memory Decay, Agent Observability/LangSmith)
- **9 Tool References** (obra/superpowers 19 Skills, MCP Servers, Agent Mega-Template, Claude-Flow Patterns, Document Skills, Claude Code System Prompts, Awesome Claude Resources, CC-WF-Studio, just-bash)

---

### MCP Configuration

| Status | Details |
|--------|---------|
| **Vorhanden** | Ja (.mcp.json) |
| **Server** | github, sequential-thinking, context7 |
| **Tools** | GitHub API, Sequential Thinking, Context7 |

---

## Architektur-Patterns

### Implementierte Patterns

| Pattern | Beschreibung | Verwendet in |
|---------|--------------|--------------|
| **Multi-Agent Orchestration** | Agents koordinieren über Dependencies | codebase-analyzer → n8n-expert |
| **Research Agent Pattern** | Multi-Source + Confidence Scoring | research-analyst-agent |
| **Progressive Disclosure** | Skills mit reference.md + examples.md | Alle 4 Skills |
| **Specialist Agent Pattern** | Domain-fokussierte Agents | 7 von 8 Agents |
| **Cross-Reference Sync** | Automatische Dokument-Synchronisation | auto-cross-reference.sh Hook |
| **Model Selection Strategy** | Optimales Modell pro Task | /opus, /sonnet, /haiku Commands |
| **Reflection Pattern** | Generator → Critic → Refiner Loop | Output-Qualitätsverbesserung |
| **PEV Pattern** | Plan-Execute-Verify mit Self-Correction | Komplexe Multi-Step Tasks |
| **Blackboard Pattern** | Shared Memory + Controller Coordination | Multi-Agent Koordination |
| **Metacognitive Pattern** | Self-Assessment vor Aktionen | Model Selection, Error Prevention |
| **Temporal Knowledge Graph** | Edges mit valid_from/valid_until für Time-Travel Queries | _graph/schema.json |
| **Memory Architecture Pattern** | 5-Layer Memory (Working→Entity→Temporal KG) | knowledge/patterns/memory-architecture-pattern.md |

### Agent Execution Patterns

```
Sequential: Agent A → Agent B → Agent C
Parallel:   [Agent A, Agent B] → Aggregator
Conditional: IF condition → Agent A ELSE Agent B
Orchestrated: codebase-analyzer → (detects n8n) → n8n-expert
```

---

## Integration Points

| Was hinzufügen? | Wo? | Template? |
|-----------------|-----|-----------|
| Neuer Agent | .claude/agents/{name}-agent.md | specialist/research/orchestrator-agent.md |
| Neuer Command | .claude/commands/{name}.md | workflow/analysis-command.md |
| Neuer Hook | .claude/hooks/{name}.sh | post-tool-use/stop-hook.sh |
| Neuer Skill | .claude/skills/{name}/ | progressive/simple-skill/ |
| Neues Pattern | knowledge/patterns/{name}.md | reusable-pattern.md |
| Neues Learning | knowledge/learnings/{name}.md | project-learning.md |
| Neuer Prompt | knowledge/prompts/{name}.md | - |
| Neues System | /create-system {path} | .claude/blueprints/ + templates/generated-system/ |
| Neuer Blueprint | .claude/blueprints/{name}.json | multi-agent-advisory.json |

---

## Naming Conventions

| Komponente | Format | Beispiel |
|------------|--------|----------|
| Agent | {domain}-agent.md | idea-validator-agent.md |
| Command | {action}.md (lowercase) | idea-new.md |
| Hook | {purpose}.sh | context-monitor.sh |
| Skill | {name}/ (Ordner) | template-creator/ |
| Pattern | {name}.md (kebab-case) | multi-agent-orchestration.md |

---

## Changelog (Integrierte Findings)

**159 Einträge** (2025-12-01 bis 2025-12-30)

→ Vollständiger Changelog: [_archive/changelog-system-map.md](../../_archive/changelog-system-map.md)

**Letzte Einträge:**
| Datum | Finding | Integration |
|-------|---------|-------------|
| 2026-01-05 | Agent Template System | +8 Templates (advisor, system-builder, validator, creative, automation, dynamic), +1 Command (/compose-agent), +3 JSON (trait-taxonomy, voice-mappings, disclaimers), 480 Agent-Kombinationen |
| 2026-01-01 | System-Vollständigkeits-Audit | +7 Commands (auto-model, pattern-scan, learning-review, analyze-batch, security-review, interview-plan, run-workflow, macro-forecast, market-analysis), +10 Agents dokumentiert, +2 Scenarios (macro-analyse, didit-medical-care) |
| 2025-12-30 | replicate/hype | 1 Pattern (multi-source-aggregation), 1 Template (multi-source-aggregator/), Context Router Route |
| 2025-12-30 | robzolkos gist | 1 Command (interview-plan), 1 Pattern |
| 2025-12-30 | obra/superpowers Deep Dive | 1 Skill (subagent-driven-development), 1 Ext Agent (code-reviewer), 2 Pattern Updates |
| 2025-12-30 | Claude Docs (Official) | 1 Reference (anthropic-skill-best-practices), 1 Learning Update |
| 2025-12-29 | awesome-claude-code-plugins | 4 Ext Agents, 1 Ext Command, 2 Templates, 1 Pattern |
| 2025-12-29 | cc-wf-studio, just-bash | 2 Tool References |
| 2025-12-29 | ralph-wiggum | 1 Pattern (Self-Improvement Loop) |
| 2025-12-29 | Continuous Claude v2 | 3 Rules: context-budget-awareness, explicit-identity, idempotent-redundancy |

---

## Zu synchronisierende Dateien

Bei Änderungen am System müssen folgende Dateien aktualisiert werden:

1. **README.md** - System Overview & Stats
2. **.claude/CONTEXT.md** - Technical Context & Structure
3. **knowledge/index.md** - Knowledge Base Index
4. **START.md** - User Stats
5. **.claude/SYSTEM-MAP.md** - Diese Datei (Komponenten-Inventar)

---

**Generiert von:** github-repo-analyzer-agent
**Nächste Aktualisierung:** Nach Integration von Repo-Findings
