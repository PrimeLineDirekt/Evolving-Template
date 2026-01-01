# Evolving System Map

---

## SETUP: Status Line Script

**File:** `~/.claude/statusline.sh`
**Make executable:** `chmod +x ~/.claude/statusline.sh`

```bash
#!/bin/bash
# Claude Code Auto-Updating Status Line
# Displays: directory | model | git-status
# Auto-refreshes between commands (no manual refresh needed)

input=$(cat)
cwd=$(echo "$input" | jq -r '.workspace.current_dir // .cwd // "~"')
model=$(echo "$input" | jq -r '.model.display_name // "Claude"')
dir=$(basename "$cwd")

if [[ "$model" =~ Opus ]]; then
  m="Opus"
elif [[ "$model" =~ Sonnet ]]; then
  m="Sonnet"
elif [[ "$model" =~ Haiku ]]; then
  m="Haiku"
else
  m="${model%% *}"
fi

git_info=""
if git -C "$cwd" rev-parse --git-dir &>/dev/null 2>&1; then
  branch=$(git -C "$cwd" --no-optional-locks branch --show-current 2>/dev/null)
  [[ -z "$branch" ]] && branch="detached"

  if git -C "$cwd" --no-optional-locks status --porcelain 2>/dev/null | grep -q .; then
    status="*"
  else
    status="✓"
  fi

  git_info=" | $branch $status"
fi

printf "\033[38;5;6m%s | %s\033[0m%s" "$dir" "$m" "$git_info"
```

---

# Evolving System Map (continued)

**Last Updated**: 2026-01-02
**Version**: 3.1.0
**Purpose**: Persistent system documentation for repository analysis and integration

---

## System Statistics

| Component | Count | Location |
|-----------|-------|----------|
| **Agents** | 30 | .claude/agents/ |
| **Skills** | 6 | .claude/skills/ |
| **Commands** | 43 | .claude/commands/ |
| **Hooks** | 4 | .claude/hooks/ |
| **Rules** | 28 | .claude/rules/ |
| **Scenarios** | 2 | .claude/scenarios/ |
| **Blueprints** | 7 | .claude/blueprints/ |
| **Templates** | 37 | .claude/templates/ |
| **Patterns** | 50 | knowledge/patterns/ |
| **Learnings** | 28 | knowledge/learnings/ |
| **Prompts** | 24 | knowledge/prompts/ |
| **MCP Servers** | 3 | .mcp.json |
| **Domain Memory** | 1 | _memory/ |

---

## Knowledge Graph (_graph/)

**NEW in v1.3.0**: Unified Knowledge Graph for automatic context provisioning.

| File | Content | Description |
|------|---------|-------------|
| schema.json | Schema | Graph schema definition |
| nodes.json | ~148 Nodes | All entities in system |
| edges.json | ~187 Edges | Relationships between entities |
| taxonomy.json | ~120 Tags | Unified keyword taxonomy |
| index/by-type.json | Index | Grouped by entity type |
| index/by-domain.json | Index | Grouped by domain/keywords |
| index/by-project.json | Index | Grouped by project |
| cache/context-router.json | Router | Keyword → Nodes mapping |

**Purpose**: Automatically load relevant context when creating Agents, Skills, Commands.

---

## Blueprints (.claude/blueprints/)

**NEW in v1.4.0**: System-Builder blueprints for automatic project generation.

| Blueprint | Type | Description | Status |
|-----------|------|-------------|--------|
| multi-agent-advisory | advisory | Multi-expert advisory system (3-5 Agents + Orchestrator) | active |

**Planned Blueprints:**
- autonomous-research (Research-focused)
- simple-workflow (Simple automation)

**Purpose**: Blueprints enable generation of complete project systems with:
- Specialized Agents
- Domain-specific Commands
- Knowledge injection from Evolving
- Pre-configured model tiers

---

## Component Inventory

### Agents (.claude/agents/)

| Name | Type | Domain | Purpose | Dependencies |
|------|------|--------|---------|--------------|
| model-selector-agent | specialist | model-selection | Metacognitive self-assessment for model selection | - |
| context-manager-agent | specialist | context-management | Context sharing, persistence, coordination | upstream: knowledge-synthesizer, research-analyst |
| idea-validator-agent | specialist | idea-validation | Feasibility, market, technical assessment | upstream: context-manager, research-analyst |
| idea-expander-agent | specialist | idea-expansion | Opportunity discovery, feature generation | upstream: idea-validator, research-analyst |
| idea-connector-agent | specialist | idea-connection | Cross-idea synergy discovery | upstream: knowledge-synthesizer, idea-validator |
| knowledge-synthesizer-agent | specialist | knowledge-synthesis | Multi-source integration, pattern recognition | upstream: research-analyst, context-manager |
| research-analyst-agent | research | multi-domain-research | Multi-source research with confidence scoring | upstream: context-manager |
| codebase-analyzer-agent | specialist | codebase-analysis | External codebase analysis, workflow detection | orchestrates: n8n-expert-agent |
| n8n-expert-agent | specialist | n8n-workflows | n8n workflow analysis, optimization | triggered by: codebase-analyzer |
| system-analyzer-agent | specialist | system-building | Requirements analysis, blueprint matching | - |
| system-architect-agent | specialist | system-building | Architecture design, agent roles, model tiers | upstream: system-analyzer |
| system-generator-agent | specialist | system-building | File generation, template instantiation | upstream: system-architect |
| system-validator-agent | specialist | system-building | Structure validation, quality gates | upstream: system-generator |

**Agent Type Distribution:**
- Specialist Agents: 12 (92.3%)
- Research Agents: 1 (7.7%)
- System Builder Agents: 4 (orchestrated pipeline)

---

### Skills (.claude/skills/)

| Name | Type | Purpose | Invocation |
|------|------|---------|------------|
| template-creator | production | Template creation for Agents, Commands, Hooks, Skills | `@template-creator` or "create an agent" |
| prompt-pro-framework | production | 5-Level Prompt Engineering System | `@prompt-pro-framework` or "create prompt for" |
| research-orchestrator | production | Multi-domain research with confidence scoring | `@research-orchestrator` or "research {topic}" |

**Skill Pattern:** All skills use Progressive Disclosure (reference.md + examples.md)

---

### Commands (.claude/commands/)

| Command | Purpose | Model | Agent/Skill |
|---------|---------|-------|-------------|
| `/opus` | Switch to Opus (maximum quality) | opus | - |
| `/opus+` | Opus + Ultrathink (maximum reasoning) | opus | - |
| `/sonnet` | Switch to Sonnet (balanced) | sonnet | - |
| `/haiku` | Switch to Haiku (fast & cheap) | haiku | - |
| `/idea-new` | New idea with AI analysis | sonnet | - |
| `/idea-work` | Work on idea (sparring) | opus | idea-validator, idea-expander, idea-connector |
| `/idea-list` | Idea overview with filters | haiku | - |
| `/idea-connect` | Find synergies between ideas | opus | - |
| `/sparring` | Free brainstorming (7 modes) | opus | - |
| `/knowledge-add` | Add knowledge to KB | haiku | - |
| `/knowledge-search` | Semantic KB search | haiku | - |
| `/project-add` | Document project | sonnet | - |
| `/project-analyze` | Analyze codebase | opus | codebase-analyzer, n8n-expert |
| `/inbox-process` | Automatically process inbox | haiku | - |
| `/onboard-process` | Process onboarding questionnaire | sonnet | - |
| `/create-agent` | Create agent from template | haiku | template-creator |
| `/create-command` | Create command from template | haiku | template-creator |
| `/create-hook` | Create hook from template | haiku | template-creator |
| `/create-skill` | Create skill from template | haiku | template-creator |
| `/system-health` | System diagnostics | haiku | - |
| `/scenario` | Activate scenario | haiku | - |
| `/scenario-list` | Show scenarios | haiku | - |
| `/scenario-create` | Create new scenario | sonnet | - |
| `/scenario-edit` | Edit scenario | sonnet | - |
| `/create-system` | Generate complete project system | sonnet | system-analyzer, system-architect, system-generator, system-validator |

**Command Categories:**
- Model Switchers: 4
- Idea Management: 4
- Knowledge Management: 2
- Project Management: 2
- Scenario Management: 4
- Creation Tools: 4
- System Building: 1
- System Utilities: 3
- Brainstorming: 1

---

### Hooks (.claude/hooks/)

| Hook | Type | Trigger | Purpose |
|------|------|---------|---------|
| context-monitor.sh | StatusLine | Permanent | Display session cost & duration |
| auto-cross-reference.sh | PostToolUse | Write/Edit | Synchronize master documents |
| session-summary.sh | Stop | Session end | Create session documentation |
| graph-update.sh | PostToolUse | Write/Edit | Update knowledge graph (placeholder) |

---

### Rules (.claude/rules/)

| Rule | Type | Purpose |
|------|------|---------|
| core-principles.md | Core | AI-First, Sparring, 80/20, Chain of Thought |
| cross-reference-sync.md | Core (CRITICAL) | Keep 5 master documents synchronized |
| domain-memory-bootup.md | Core (CRITICAL) | Memory read/write ritual |
| auto-enhancement.md | Core | Automatic prompt enhancement |
| plan-archival.md | Core | Plan archival workflow |
| workflow-detection.md | Core | Confidence-based slash-command detection |
| command-creation.md | Core (CRITICAL) | Create new commands correctly |
| scenario-agents.md | Core (CRITICAL) | Agent usage in scenarios |
| knowledge-linking.md | Core | Proactive knowledge linking |
| experience-suggest.md | Core | Experience memory auto-suggest |
| ultrathink.md | Core | Quality principles (5 principles) |
| scenarios/evolving-dashboard.md | Path-Specific | Rules for dashboard/**/* (example) |

**Rule Types:**
- Core Rules: 11 (always active)
- Path-Specific Rules: 1 (only for specific files)

---

### Scenarios (.claude/scenarios/)

| Scenario | Description | Agents | Commands | Status |
|----------|-------------|--------|----------|--------|
| evolving-dashboard | TileGrid-Guide (48 features) + Chat Panel with Toggle & Resize (v2.0.0) | 5 | 3 | active |
| workflow-engine | Claude Agent SDK Implementation | 5 | 4 | active |

**Evolving Dashboard Agents:**
- dashboard-frontend-agent (Next.js, React, xterm.js)
- dashboard-backend-agent (API, WebSocket, node-pty)
- railway-expert-agent (Railway.app Deployment)
- dashboard-testing-agent (Jest, Playwright)
- dashboard-codebase-agent (Architecture, Code Quality)

**Evolving Dashboard Commands:**
- /dashboard-dev - Development server
- /dashboard-build - Production build
- /dashboard-deploy - Railway deployment
- /dashboard-test - Run tests

**Workflow Engine Agents:**
- sdk-architect-agent (System Design, Architecture)
- python-engineer-agent (Backend Implementation)
- dashboard-engineer-agent (Frontend, React)
- qa-agent (Testing, Quality Assurance)
- code-reviewer-agent (Code Review, Best Practices)

**Workflow Engine Commands:**
- /workflow-design - Plan architecture
- /workflow-implement - Implementation
- /workflow-test - Run tests
- /workflow-review - Code review

---

### Templates (.claude/templates/)

| Type | Files | Purpose |
|------|-------|---------|
| **Agents** | specialist-agent.md, research-agent.md, orchestrator-agent.md | Agent creation |
| **Commands** | workflow-command.md, analysis-command.md | Command creation |
| **Hooks** | post-tool-use.sh, stop-hook.sh | Hook creation |
| **Skills** | progressive-skill/, simple-skill/ | Skill creation |
| **Scenarios** | autonomous-research/, multi-agent-advisory/ | Scenario creation (Task Decomposition, Multi-Agent Advisory) |
| **Generated-System** | CLAUDE.md.template, README.md.template, scenario.json.template, memory-index.json.template | System generation |
| **Patterns** | reusable-pattern.md | Pattern documentation |
| **Learnings** | project-learning.md | Learning capture |

---

### Knowledge Base (knowledge/)

| Folder | Files | Description |
|--------|-------|-------------|
| **projects/** | - | Project documentation (populated via /project-add) |
| **plans/** | 0 | Parked implementation plans |
| **learnings/** | 13 | Project insights |
| **patterns/** | 24 | Reusable patterns (4 core, 8 agent, 1 infra, 3 business, 1 system-gen, 3 claude-code, 2 token-efficiency, 2 research) |
| **references/** | 6 | Self-contained tool references (claude-skills, mcp-servers, agent-templates, claude-flow, document-skills, claude-code-system-prompts) |
| **prompts/** | 24 | Prompt library & frameworks |
| **personal/** | 4 | User profile, skills, instructions |
| **external-projects/** | - | Context-persistent codebase analysis |
| **_sources/** | 2 | Source tracking & archived externals |

**Key Knowledge Assets:**
- Projects: Populated through onboarding and /project-add
- 2 Frameworks: Prompt Pro 2.0, Idea Forge
- 24+ Production Patterns (Multi-Agent, Reflection, PEV, Blackboard, Metacognitive, Context Window, Compact Errors, 8-Block Profile, Content Pipeline, System-Generation, Security Review, Swarm/Team Coordination, Learning Mode, Observation Compression, Progressive Disclosure, Recursive Research, LOCK Methodology)
- 13+ Learnings (12-Factor Agents, Claude SDK Insights, System-Builder, Claude-Mem Persistent Memory, Prompt Coach Methodology, AgentFS Storage, etc.)
- **7 Tool References** (obra/superpowers 19 Skills, MCP Servers, Agent Mega-Template, Claude-Flow Patterns, Document Skills, Claude Code System Prompts, Awesome Claude Resources)

---

### MCP Configuration

| Status | Details |
|--------|---------|
| **Available** | Yes (.mcp.json) |
| **Servers** | github, sequential-thinking, context7 |
| **Tools** | GitHub API, Sequential Thinking, Context7 |

---

## Architecture Patterns

### Implemented Patterns

| Pattern | Description | Used In |
|---------|-------------|---------|
| **Multi-Agent Orchestration** | Agents coordinate via dependencies | codebase-analyzer → n8n-expert |
| **Research Agent Pattern** | Multi-source + confidence scoring | research-analyst-agent |
| **Progressive Disclosure** | Skills with reference.md + examples.md | All 3 skills |
| **Specialist Agent Pattern** | Domain-focused agents | 12 of 13 agents |
| **Cross-Reference Sync** | Automatic document synchronization | auto-cross-reference.sh hook |
| **Model Selection Strategy** | Optimal model per task | /opus, /sonnet, /haiku commands |
| **Reflection Pattern** | Generator → Critic → Refiner loop | Output quality improvement |
| **PEV Pattern** | Plan-Execute-Verify with self-correction | Complex multi-step tasks |
| **Blackboard Pattern** | Shared memory + controller coordination | Multi-agent coordination |
| **Metacognitive Pattern** | Self-assessment before actions | Model selection, error prevention |

### Agent Execution Patterns

```
Sequential: Agent A → Agent B → Agent C
Parallel:   [Agent A, Agent B] → Aggregator
Conditional: IF condition → Agent A ELSE Agent B
Orchestrated: codebase-analyzer → (detects n8n) → n8n-expert
```

---

## Integration Points

| What to Add? | Where? | Template? |
|--------------|--------|-----------|
| New Agent | .claude/agents/{name}-agent.md | specialist/research/orchestrator-agent.md |
| New Command | .claude/commands/{name}.md | workflow/analysis-command.md |
| New Hook | .claude/hooks/{name}.sh | post-tool-use/stop-hook.sh |
| New Skill | .claude/skills/{name}/ | progressive/simple-skill/ |
| New Pattern | knowledge/patterns/{name}.md | reusable-pattern.md |
| New Learning | knowledge/learnings/{name}.md | project-learning.md |
| New Prompt | knowledge/prompts/{name}.md | - |
| New System | /create-system {path} | .claude/blueprints/ + templates/generated-system/ |
| New Blueprint | .claude/blueprints/{name}.json | multi-agent-advisory.json |

---

## Naming Conventions

| Component | Format | Example |
|-----------|--------|---------|
| Agent | {domain}-agent.md | idea-validator-agent.md |
| Command | {action}.md (lowercase) | idea-new.md |
| Hook | {purpose}.sh | context-monitor.sh |
| Skill | {name}/ (folder) | template-creator/ |
| Pattern | {name}.md (kebab-case) | multi-agent-orchestration.md |

---

## Changelog (Integrated Findings)

| Date | Source | Finding | Integration | Status |
|------|--------|---------|-------------|--------|
| 2025-12-01 | Initial | System scan | SYSTEM-MAP.md created | Done |
| 2025-12-01 | langwatch/better-agents | MCP Configuration | `.mcp.json` created | Done |
| 2025-12-01 | langwatch/better-agents | Scenario Testing | `.claude/tests/` framework created | Done |
| 2025-12-01 | langwatch/better-agents | Prompt Registry | `knowledge/prompts/index.json` (prompts.json pattern) | Done |
| 2025-12-01 | langwatch/better-agents | YAML Prompt Format | Evaluate: model/temperature/messages structure | Backlog |
| 2025-12-01 | langwatch/better-agents | Evaluation Notebooks | `.claude/tests/evaluations/` (Jupyter) | Backlog |
| 2025-12-01 | langwatch/better-agents | AGENTS.md Pattern | knowledge/learnings/better-agents-patterns.md | Done |
| 2025-12-01 | langwatch/better-agents | Observability | Pattern for later | Backlog |
| 2025-12-01 | taches-cc-resources | Intake Gate Pattern | knowledge/patterns/intake-gate-pattern.md | Done |
| 2025-12-01 | taches-cc-resources | /whats-next Command | .claude/commands/whats-next.md | Done |
| 2025-12-01 | taches-cc-resources | /debug Command | .claude/commands/debug.md | Done |
| 2025-12-01 | taches-cc-resources | /think Command (8 Frameworks) | .claude/commands/think.md | Done |
| 2025-12-01 | taches-cc-resources | COMMANDS.md Documentation | .claude/COMMANDS.md | Done |
| 2025-12-01 | taches-cc-resources | Meta-Prompting System | /create-prompt + /run-prompt + prompts/ | Done |
| 2025-12-01 | prompt-pro-framework | reference.md + examples.md | .claude/skills/prompt-pro-framework/ | Done |
| 2025-12-09 | ucbepic/docetl | Gleaning Config | Reflection pattern extended | Done |
| 2025-12-09 | ucbepic/docetl | Checkpoint Validation | knowledge/patterns/checkpoint-validation-pattern.md | Done |
| 2025-12-09 | ucbepic/docetl | Auto-Optimizer Pattern | Evaluated - not adopted (different use case) | Skipped |
| 2025-12-09 | ucbepic/docetl | YAML Pipeline DSL | Evaluated - keeping JSON scenarios | Skipped |
| 2025-12-10 | Claude Code Docs | .claude/rules/ System | CLAUDE.md refactored, 8 modular rules | Done |
| 2025-12-10 | Claude Code Docs | Path-Specific Rules | scenarios/evolving-dashboard.md (example) | Done |
| 2025-12-10 | Claude Code Docs | @import Syntax | CLAUDE.md now uses @imports | Done |
| 2025-12-10 | humanlayer/12-factor-agents | Context Window Ownership | knowledge/patterns/context-window-ownership-pattern.md | Done |
| 2025-12-10 | humanlayer/12-factor-agents | Compact Errors Pattern | knowledge/patterns/compact-errors-pattern.md | Done |
| 2025-12-12 | memodb-io/Acontext | Automatic Skill Distillation | knowledge/learnings/acontext-automatic-skill-distillation.md | Done |
| 2025-12-12 | memodb-io/Acontext | Complexity Scoring | /whats-next extended with learning extraction | Done |
| 2025-12-12 | System Audit | Stats Correction | Commands: 34→33, Scenarios: 2→3, MCP: No→Yes | Done |
| 2025-12-13 | Anthropic Video | Domain Memory Pattern | _memory/ system, domain-memory-bootup.md rule | Done |
| 2025-12-14 | Knowledge Graph Design | Unified Knowledge Graph | _graph/ with ~148 nodes, ~187 edges, context router | Done |
| 2025-12-14 | Knowledge Graph | /context Command | .claude/commands/context.md | Done |
| 2025-12-14 | Knowledge Graph | graph-update.sh Hook | .claude/hooks/graph-update.sh (placeholder) | Done |
| 2025-12-12 | System Audit | Model Fix | idea-work.md: opusplan→opus | Done |
| 2025-12-12 | System Audit | workflow-engine Scenario | SYSTEM-MAP.md: Agents & commands documented | Done |
| 2025-12-14 | Experience Memory | Experience Memory System | _memory/experiences/, 4 commands, auto-suggest rule | Done |
| 2025-12-14 | Experience Memory | experience-suggest.md Rule | .claude/rules/experience-suggest.md | Done |
| 2025-12-14 | Experience Memory | experience-router.json | _graph/cache/experience-router.json | Done |
| 2025-12-14 | System Builder | Blueprint Infrastructure | .claude/blueprints/ with index.json + multi-agent-advisory.json | Done |
| 2025-12-14 | System Builder | 4 System-Builder Agents | system-analyzer, system-architect, system-generator, system-validator | Done |
| 2025-12-14 | System Builder | /create-system Command | .claude/commands/create-system.md | Done |
| 2025-12-14 | System Builder | Generation Templates | .claude/templates/generated-system/ (4 templates) | Done |
| 2025-12-14 | System Builder | Context Router Update | system-creation route for knowledge injection | Done |
| 2025-12-14 | System Builder | System-Generation Pattern | knowledge/patterns/system-generation-pattern.md | Done |
| 2025-12-14 | System Builder | System-Builder Learnings | knowledge/learnings/system-builder-learnings.md | Done |
| 2025-12-16 | Blueprints | autonomous-research Blueprint | .claude/blueprints/autonomous-research.json | Done |
| 2025-12-16 | Blueprints | simple-workflow Blueprint | .claude/blueprints/simple-workflow.json | Done |
| 2025-12-16 | Code Cleanup | BaseManager Abstract Class | evolving_core/managers/base_manager.py | Done |
| 2025-12-16 | Code Cleanup | Manager __init__.py Exports | evolving_core/managers/__init__.py | Done |
| 2025-12-16 | Code Cleanup | Idea Model Schema Fix | evolving_core/models/idea.py | Done |
| 2025-12-16 | Code Cleanup | Agents Frontmatter Fix | model-selector agent | Done |
| 2025-12-16 | Piebald-AI/claude-code-system-prompts | /repo-screen Command | .claude/commands/repo-screen.md (2-phase repo check) | Done |
| 2025-12-16 | Piebald-AI/claude-code-system-prompts | Session Notes Template | .claude/templates/session-notes-template.md (10-section enhanced) | Done |
| 2025-12-16 | Piebald-AI/claude-code-system-prompts | Security Review Pattern | knowledge/patterns/security-review-pattern.md (3-phase, 80%+ confidence) | Done |
| 2025-12-16 | Piebald-AI/claude-code-system-prompts | Swarm/Team Coordination Pattern | knowledge/patterns/swarm-team-coordination-pattern.md (multi-agent) | Done |
| 2025-12-16 | Piebald-AI/claude-code-system-prompts | Learning Mode Pattern | knowledge/patterns/learning-mode-pattern.md (TODO(human)) | Done |
| 2025-12-16 | Piebald-AI/claude-code-system-prompts | System Prompts Reference | knowledge/references/claude-code-system-prompts.md (59 prompts) | Done |
| 2025-12-16 | Piebald-AI/claude-code-system-prompts | /whats-next Enhanced | --detailed flag for 10-section template | Done |
| 2025-12-16 | Piebald-AI/claude-code-system-prompts | /security-review Command | .claude/commands/security-review.md (Opus, OWASP Top 10) | Done |
| 2025-12-16 | thedotmack/claude-mem | Persistent Memory Learning | knowledge/learnings/claude-mem-persistent-memory.md (5-hook architecture) | Done |
| 2025-12-16 | thedotmack/claude-mem | Observation Compression Pattern | knowledge/patterns/observation-compression-pattern.md (75-95% token reduction) | Done |
| 2025-12-16 | thedotmack/claude-mem | Progressive Disclosure Pattern | knowledge/patterns/progressive-disclosure-pattern.md (4-step workflow) | Done |
| 2025-12-16 | Cranot/deep-research | Recursive Research Pattern | knowledge/patterns/recursive-research-pattern.md (Agent DNA, 6-dimensional) | Done |
| 2025-12-16 | hancengiz/claude-code-prompt-coach-skill | Prompt Analysis Methodology | knowledge/learnings/prompt-coach-analysis-methodology.md (8-dimensional, golden rule) | Done |
| 2025-12-16 | tursodatabase/agentfs | Unified Agent Storage | knowledge/learnings/agentfs-unified-storage.md (3-layer SQLite, audit trail) | Done |
| 2025-12-16 | Nebulock-Inc/agentic-threat-hunting-framework | LOCK Methodology Pattern | knowledge/patterns/lock-methodology-pattern.md (Learn-Observe-Check-Keep) | Done |
| 2025-12-16 | alvinunreal/awesome-claude | Awesome Claude Resources | knowledge/references/awesome-claude-resources.md (curated resource list) | Done |
| 2025-12-22 | English Translation | Root Documentation | All root MD files translated to English | Done |

---

## Files to Synchronize

When making changes to the system, the following files must be updated:

1. **README.md** - System overview & stats
2. **.claude/CONTEXT.md** - Technical context & structure
3. **knowledge/index.md** - Knowledge base index
4. **START.md** - User stats
5. **.claude/SYSTEM-MAP.md** - This file (component inventory)

---

**Generated by:** github-repo-analyzer-agent
**Next Update:** After integration of repo findings
