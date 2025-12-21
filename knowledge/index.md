# Knowledge Base Index

## Overview
This is your personal knowledge management system. All knowledge, projects, prompts, learnings, patterns, and resources are stored and interconnected here.

## Structure

### Projects (`knowledge/projects/`)
Documentation for all your active and past projects.

### Prompts (`knowledge/prompts/`)
Production-ready prompt library with frameworks, research agents, and patterns.

### Personal (`knowledge/personal/`)
Information about you, your skills, interests, and development.

### Learnings (`knowledge/learnings/`)
Extracted lessons learned from projects, experiments, and experiences.

### Patterns (`knowledge/patterns/`)
Reusable patterns and best practices from your projects.

### Sessions (`knowledge/sessions/`)
Documented sparring and brainstorming sessions.

### Plans (`knowledge/plans/`)
Parked implementation plans for later execution.

#### Example: Technical Architecture Session
Sample sparring session for technical architecture - API strategy, infrastructure planning, database design, cost modeling.
**Type**: Business Planning | **Format**: Session documentation

### Resources (`knowledge/resources/`)
External tools, links, references, and learning materials.

**Resources**:
- External tools, links, and references for your work

## Quick Links
- [About Me](personal/about-me.md)
- [Skills](personal/skills.md)
- [System Instructions](personal/system-instructions.md)
- [Prompt Library](prompts/README.md)
- [Patterns](patterns/README.md)
- [Learnings](learnings/README.md)
- **Knowledge Hub Dashboard**: `cd dashboard && npm run dev` → http://localhost:3000

### Knowledge Hub Dashboard
Interactive web learning portal for AI fundamentals:
- **35 Learning Cards** (Beginner → Advanced → Expert)
- **25 YouTube Videos** (verified & functional)
- **7 Categories**: Fundamentals, Prompting, Models, Tools, Agents, Ethics, Future
- **Features**: Level filter, search, progress tracking (LocalStorage)
- **Tech**: Next.js 16, React, TypeScript, Tailwind CSS

## System Features

### Model Selection Strategy

Intelligent model selection for optimal performance & cost efficiency.

**Quick Model Switcher:**
- `/opus` - Opus (maximum quality for complex reasoning)
- `/opus+` - Opus with Ultrathink (maximum extended thinking)
- `/sonnet` - Sonnet (balanced performance)
- `/haiku` - Haiku (fast & cost-effective)

**Auto-Optimization:** All 34+ workflows automatically use optimal models:
- **70% Haiku** - Fast tasks (search, list, create, inbox)
- **20% Sonnet** - Balanced tasks (idea-new, project-add)
- **10% Opus** - Complex tasks (sparring, idea-connect, project-analyze)

**Cost Optimization:** Automatic distribution significantly reduces API costs while maintaining maximum quality for complex tasks.

→ See [.claude/README.md - Model Selection Strategy](../.claude/README.md#model-selection-strategy) for details

---

## Projects

_No projects documented yet._

Use `/project-add` to document your first project.

## Agents (Multi-Agent Orchestration)

### Foundation Agents (3)

#### [Context Manager](../.claude/agents/context-manager-agent.md)
Context sharing, persistence & coordination across multi-agent systems. Manages session state and knowledge base references.
**Type**: Specialist | **Complexity**: High

#### [Knowledge Synthesizer](../.claude/agents/knowledge-synthesizer-agent.md)
Knowledge extraction, synthesis & integration from multiple sources. Pattern recognition and cross-domain connections.
**Type**: Specialist | **Complexity**: High

#### [Research Analyst](../.claude/agents/research-analyst-agent.md)
Multi-source research with confidence scoring (0-100%). Market, technical, and user research capabilities.
**Type**: Research | **Complexity**: High

### Idea Workflow Agents (3)

#### [Idea Validator](../.claude/agents/idea-validator-agent.md)
Comprehensive validation with feasibility, market, and technical assessment. Risk identification and mitigation planning.
**Type**: Specialist | **Complexity**: High

#### [Idea Expander](../.claude/agents/idea-expander-agent.md)
Systematic idea expansion through opportunity discovery and feature generation. Market expansion and use case identification.
**Type**: Specialist | **Complexity**: Medium-High

#### [Idea Connector](../.claude/agents/idea-connector-agent.md)
Cross-idea synergy discovery and connection pattern identification. Resource sharing and integration opportunities.
**Type**: Specialist | **Complexity**: High

### External Project Analysis Agents (3)

#### [Codebase Analyzer](../.claude/agents/codebase-analyzer-agent.md)
External codebase analysis with context persistence. Architecture mapping, dependency analysis, code quality assessment, and automatic workflow detection. Orchestrates specialized experts when workflows detected.
**Type**: Specialist | **Complexity**: High

#### [n8n Expert](../.claude/agents/n8n-expert-agent.md)
n8n workflow analysis, optimization, and validation. Automatically fetches latest n8n documentation, detects errors, validates integration with frontend, and provides best-practice recommendations.
**Type**: Specialist | **Complexity**: High

#### [GitHub Repo Analyzer](../.claude/agents/github-repo-analyzer-agent.md)
Dual-system analysis for GitHub repositories. Maps external repo findings against SYSTEM-MAP.md, categorizes as NEW/BETTER/DIFFERENT/REDUNDANT, generates integration roadmap with effort estimates.
**Type**: Research | **Complexity**: High

**Integration**:
- Idea workflows: 6 agents orchestrated in `/idea-work` (3-5 per session)
- External projects: codebase-analyzer + n8n-expert (conditional) in `/project-analyze`
- Repository analysis: github-repo-analyzer in `/analyze-repo`

## Skills (Progressive Disclosure)

### [Template Creator](../.claude/skills/template-creator/SKILL.md)
Meta-agent for component generation (Agents, Commands, Hooks, Skills). Hybrid approach with auto-detection and explicit commands.
**Lines**: 439 | **Pattern**: Progressive Disclosure

### [Prompt Pro Framework](../.claude/skills/prompt-pro-framework/SKILL.md)
Advanced prompt engineering with 5-level technique hierarchy. Adaptive expert transformation and performance-driven design.
**Lines**: 249 | **Source**: Prompt Pro 2.0 (condensed 41%)

### [Research Orchestrator](../.claude/skills/research-orchestrator/SKILL.md)
Elite research coordination for multi-domain systematic research. Confidence scoring and actionable output generation.
**Lines**: 316 | **Source**: Research Orchestrator prompt (condensed 9%)

### Example: E-commerce Skill
E-commerce workflow automation with SEO optimization, social media integration, and research tools.
**Pattern**: Progressive Disclosure | **Lines**: < 500

**Pattern**: All skills < 500 lines with reference.md for complete documentation and examples.md for demonstrations.

## Prompts

### Frameworks

#### [Prompt Pro 2.0](prompts/frameworks/prompt-pro-2.0.md)
Advanced prompt engineering framework with 5-level technique hierarchy, XML structure optimization, and Claude-specific best practices.
**Model**: Opus 4, Sonnet 4.5 | **Type**: Meta-Prompt Framework | **Confidence**: 95%

#### [Idea Forge](prompts/frameworks/idea-forge.md)
Adaptive ideation system with multi-phase process: Divergence → Convergence → Roadmap.
**Type**: Idea Development Framework | **Confidence**: 90%

### Research Agents

#### [Research Orchestrator](prompts/research-agents/research-orchestrator.md)
Elite research coordinator with confidence scoring and multi-domain research workflows.
**Model**: Opus | **Domain**: Multi-Domain Research

### Pattern Library

#### Example: Multi-Agent Patterns
Production-ready specialized agent prompts from orchestration systems. Includes domain-specific and synthesis agents.
**Status**: Production-Proven | **Use Case**: Multi-Agent Inspiration

### Skills

_Example skills demonstrate the Progressive Disclosure pattern with reference documentation and examples._

## Learnings

### Example: Project Learnings
Key learnings extracted from your projects - Multi-Agent Systems, Architecture Patterns, Integration Strategies.
**Pattern**: Confidence-scored insights from real implementations

### [Anthropic Advanced Tool Use](learnings/anthropic-advanced-tool-use.md)
Three beta features for intelligent tool management: Tool Search Tool (85% token reduction), Programmatic Tool Calling (37% token reduction), Tool Use Examples (72%→90% accuracy).
**Source**: Anthropic Engineering Blog | **Type**: Technical Learning | **Confidence**: 95%

### [AITMPL Platform - Key Findings](learnings/aitmpl-findings.md)
Comprehensive analysis of AITMPL template library - Specialization patterns, progressive disclosure, hooks automation, hybrid approaches, template systems.
**Source**: aitmpl.com | **Type**: External Learning | **Confidence**: 85%

## Patterns

### Completed (4)
1. [Research Confidence Scoring](patterns/research-confidence-scoring.md) - 95% Confidence
2. [Multi-Agent Orchestration](patterns/multi-agent-orchestration.md) - 95% Confidence
3. [Bilingual SEO System](patterns/bilingual-seo-system.md) - 92% Confidence
4. [Freemium SaaS Gates](patterns/freemium-saas-gates.md) - 88% Confidence

### TODO Placeholders (3)
5. [8-Block Profile System](patterns/8-block-profile-system.md) - 90% Confidence
6. [GDPR-Compliant SaaS](patterns/gdpr-compliant-saas.md) - 95% Confidence
7. [AI Content Generation Pipeline](patterns/ai-content-generation-pipeline.md) - 92% Confidence

## Scenarios (Context-based Project Bundles)

### [Evolving Dashboard](../.claude/scenarios/evolving-dashboard/README.md)
Web Dashboard with Terminal for Evolving System. Tile-based guide system on left, Claude Code Terminal on right.
**Status**: Active | **Tech**: Next.js 15, React 19, xterm.js, WebSocket, Railway.app
**Agents**: 5 (Frontend, Backend, Railway, Testing, Codebase)

### [Workflow Engine](../.claude/scenarios/workflow-engine/scenario.json)
AI-native workflow orchestrator with YAML definitions, permission engine, and Claude Code SDK integration.
**Status**: In Development | **Tech**: Python, FastAPI, Claude Code SDK
**Agents**: 5 (SDK-Architect, Python-Engineer, Dashboard-Engineer, QA-Engineer, Code-Reviewer)
**Commands**: 4 (dev, build, deploy, test)

→ Activate: `/scenario evolving-dashboard`

## Workflows (Automation Engine)

Declarative YAML-based workflow automation with permission engine and user preferences.

### Available Workflows
| Workflow | Trigger | Description |
|----------|---------|-------------|
| `morning-briefing` | Cron 8:00 | Daily overview |
| `weekly-review` | Cron Mon 9:00 | Idea hygiene |
| `inbox-processing` | Watch `_inbox/` | Auto-classification |
| `idea-forge-full` | Manual | Complete idea development |

→ Documentation: [workflows/README.md](../workflows/README.md)

## Statistics
<!-- Auto-updated by workflows -->
- **Total Projects**: 0
- **Total Scenarios**: 2 (evolving-dashboard, workflow-engine)
- **Total Workflows**: 4 (morning-briefing, weekly-review, inbox-processing, idea-forge-full)
- **Total Prompts**: 4+ files (2 Frameworks, 1 Research Agent, examples)
- **Total Learnings**: 13+ (technical learnings, external findings)
- **Total Patterns**: 24 (4 complete, 20+ production)
- **Total Personal Docs**: 3 (to be filled via onboarding)
- **Total Resources**: Variable
- **Total Sessions**: Variable
- **Total Ideas**: 0
- **Total External Projects**: 0
- **Total Plans**: 0
- **Last Updated**: 2025-12-22
