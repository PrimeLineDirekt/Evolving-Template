# Evolving - Personal Knowledge & Innovation System

An AI-powered second brain for knowledge management, idea development, and personal growth with Claude Code.

## What Is Evolving?

Evolving is your **personal knowledge and innovation system** - a comprehensive framework that transforms Claude Code into a powerful second brain. It never forgets, discovers connections, and helps you:

- **Capture ideas** with AI-powered analysis and potential scoring
- **Manage knowledge** extracted from projects and made reusable
- **Find synergies** between different ideas and concepts automatically
- **Build expertise** through documented learnings and patterns
- **Work smarter** with 40+ automated workflows

---

## Quick Start

### Prerequisites

- [Claude Code CLI](https://claude.ai/claude-code) installed
- Clone this repository

### Getting Started

```bash
# Clone the repository
git clone https://github.com/youruser/evolving-template.git my-evolving

# Navigate to the directory
cd my-evolving

# Start Claude Code
claude
```

### Your First Session

1. **Say hello** - Claude automatically loads the system context
2. **Try a command**: `/idea-new My first idea for a SaaS product`
3. **Or use natural language**: "I have an idea for..." (the system detects intent)

### Personalize Your System

1. Open `_ONBOARDING.md` in the root folder
2. Fill in the relevant sections (not everything is required)
3. Tell Claude: "Process the onboarding"
4. The system integrates your profile and deletes the questionnaire

---

## Core Features

### Plain Text Detection

You don't need to memorize commands. Just speak naturally:

| You Say | System Suggests |
|---------|-----------------|
| "I have an idea for..." | "Should I use `/idea-new`?" |
| "Show me my ideas" | "Should I use `/idea-list`?" |
| "Let's brainstorm about..." | "Should I use `/sparring`?" |
| "Search for API patterns" | "Should I use `/knowledge-search`?" |
| "Process the inbox" | "Should I use `/inbox-process`?" |

**How it works:**
- System analyzes your message for intent patterns
- Confidence scoring (1-10) determines the response
- High confidence (9-10): "Should I use /command?"
- Medium confidence (6-8): "Do you mean /command?"
- Low confidence (1-5): Normal response

**NEVER auto-executes** - always asks for confirmation first.

### Multi-Agent System

**30 Specialized Agents** for different workflows (18 internal + 12 external):

| Agent Type | Agents | Purpose |
|------------|--------|---------|
| **Foundation** | context-manager, knowledge-synthesizer, research-analyst | Core knowledge operations |
| **Idea Workflow** | idea-validator, idea-expander, idea-connector | Idea development pipeline |
| **System Builder** | system-analyzer, system-architect, system-generator, system-validator | Generate complete systems |
| **External Analysis** | codebase-analyzer, github-repo-analyzer | Analyze external code |

Agents work together orchestrated by your commands for comprehensive analysis.

### Skills System

**3 Progressive Disclosure Skills** (< 500 lines each for token efficiency):

| Skill | Purpose |
|-------|---------|
| `template-creator` | Generate agents, commands, hooks, skills from templates |
| `prompt-pro-framework` | Advanced prompt engineering with 5-level technique hierarchy |
| `research-orchestrator` | Multi-domain research with confidence scoring |

**Pattern**: Skill.md loads reference.md for details and examples.md for demonstrations.

### Domain Memory

Persistent project state across sessions:

```
_memory/
├── index.json              # Active context pointer
├── projects/               # Per-project state & progress
│   └── {project}.json
├── experiences/            # Learned solutions & patterns
└── workflows/              # Active workflow state
```

**Session Start**: Claude reads memory and announces context:
> "We're working on [Project]. Last progress: [X]. Next step: [Y]. Continue?"

**Session End**: Progress is logged for the next session.

### Experience Memory

Learn from past solutions:

- **Types**: solution, pattern, decision, workaround, gotcha, preference
- **Auto-Suggest**: When errors occur, relevant past solutions are suggested
- **Relevance Scoring**: Experiences are ranked and cleaned automatically

Commands: `/remember`, `/recall`, `/memory-stats`, `/preferences`

### Knowledge Graph

Entity relationships and context routing:

```
_graph/
├── nodes.json              # ~150 entities
├── edges.json              # ~200 relationships
├── taxonomy.json           # Unified keywords
└── cache/context-router.json  # Keyword → nodes mapping
```

When you start a task, the graph routes relevant context automatically.

### Cross-Documentation Sync

**5 Master Files** stay synchronized automatically:

1. `README.md` - System overview & stats
2. `.claude/CONTEXT.md` - Technical context & structure
3. `knowledge/index.md` - Knowledge base index
4. `START.md` - User-facing quick start
5. `.claude/SYSTEM-MAP.md` - Component inventory

When you add a project, pattern, or learning, all 5 files update.

### Session Handoffs

Every session can be documented for continuity:

```
_handoffs/
├── 2025-01-15-feature-implementation.md
├── 2025-01-14-bug-fix-session.md
└── ...
```

Use `/whats-next` to create a handoff before ending your session. The next session can pick up exactly where you left off.

### Plan Archival

Implementation plans are **archived, not deleted**:

```
knowledge/plans/
├── index.md                    # Active plans
├── active-feature-plan.md
└── archive/                    # Completed plans
    ├── 2025-01-implemented-auth.md
    └── ...
```

This builds cumulative knowledge over time.

### Inbox Processing

The fastest way to add content:

1. Drop files in `_inbox/` (markdown, text, PDFs)
2. Say: "Process the inbox" or use `/inbox-process`
3. System analyzes, categorizes, and integrates automatically
4. Asks if original should be deleted

### Scenario System

Context-based project bundles with specialized agents:

```bash
/scenario evolving-dashboard    # Activate a scenario
/scenario-list                  # Show all scenarios
/scenario-create my-app         # Create new scenario
```

Each scenario provides:
- Domain-specific agents
- Custom commands
- Path-specific rules

---

## Command Reference

### Model Switchers (4)

| Command | Model | Use Case |
|---------|-------|----------|
| `/opus` | Opus | Maximum quality, complex tasks |
| `/opus+` | Opus + Ultrathink | Maximum reasoning |
| `/sonnet` | Sonnet | Balanced performance |
| `/haiku` | Haiku | Fast & cheap |

### Idea Management (4)

| Command | Purpose |
|---------|---------|
| `/idea-new` | Capture new idea with AI analysis |
| `/idea-work` | Deep work on an idea (sparring) |
| `/idea-list` | Show all ideas with filters |
| `/idea-connect` | Find synergies between ideas |

### Knowledge Management (2)

| Command | Purpose |
|---------|---------|
| `/knowledge-add` | Add knowledge to the base |
| `/knowledge-search` | Semantic search across knowledge |

### Brainstorming (2)

| Command | Purpose |
|---------|---------|
| `/sparring` | Free brainstorming (7 modes) |
| `/think` | Apply mental models (8 frameworks) |

### Project Tools (3)

| Command | Purpose |
|---------|---------|
| `/project-add` | Document a project |
| `/project-analyze` | Analyze external codebase |
| `/analyze-repo` | Analyze GitHub repository |

### Creation Tools (4)

| Command | Purpose |
|---------|---------|
| `/create-agent` | Create new agent from template |
| `/create-command` | Create new command from template |
| `/create-skill` | Create new skill from template |
| `/create-system` | Generate complete multi-agent system |

### Memory Commands (4)

| Command | Purpose |
|---------|---------|
| `/remember` | Save an experience |
| `/recall` | Search experiences |
| `/memory-stats` | Show memory statistics |
| `/preferences` | Manage user preferences |

### System Tools (3)

| Command | Purpose |
|---------|---------|
| `/system-health` | Run system diagnostics |
| `/whats-next` | Create session handoff |
| `/context` | Load knowledge graph context |

### Scenario Commands (4)

| Command | Purpose |
|---------|---------|
| `/scenario` | Activate a scenario |
| `/scenario-list` | List all scenarios |
| `/scenario-create` | Create new scenario |
| `/scenario-edit` | Edit existing scenario |

---

## Directory Structure

```
evolving/
├── START.md                    # Quick start guide
├── README.md                   # This file
├── CLAUDE.md                   # Claude Code instructions
├── SETUP_MCP.md                # MCP server setup
├── _ONBOARDING.md              # Onboarding questionnaire
│
├── .claude/
│   ├── agents/                 # 13+ specialized agents
│   ├── commands/               # 40+ slash commands
│   ├── skills/                 # 4 progressive skills
│   ├── hooks/                  # Automation hooks
│   ├── rules/                  # Modular behavior rules
│   ├── scenarios/              # Context-based bundles
│   ├── templates/              # Component templates
│   ├── SYSTEM-MAP.md           # Component inventory
│   ├── COMMANDS.md             # Command documentation
│   └── CONTEXT.md              # Technical context
│
├── knowledge/
│   ├── index.md                # Knowledge hub entry
│   ├── projects/               # Project documentation
│   ├── learnings/              # Best practices
│   ├── patterns/               # Reusable patterns
│   ├── prompts/                # Prompt library
│   ├── plans/                  # Implementation plans
│   │   └── archive/            # Completed plans
│   ├── references/             # Tool references
│   └── personal/               # User profile & skills
│
├── ideas/
│   ├── index.json              # Ideas metadata
│   └── {category}/             # Categorized ideas
│
├── _inbox/                     # Drop files for processing
├── _handoffs/                  # Session handoffs
├── _memory/                    # Domain memory
│   ├── index.json              # Active context
│   ├── projects/               # Project-specific state
│   └── experiences/            # Past solutions
│
├── _graph/                     # Knowledge graph
│   ├── nodes.json              # Entities
│   ├── edges.json              # Relationships
│   └── cache/                  # Context router
│
├── workflows/                  # Workflow automation
│   └── definitions/            # YAML workflows
│
├── mcp_server/                 # MCP server for Claude Desktop
└── evolving_core/              # Shared business logic
```

---

## Customization

### Adding New Commands

1. Create file in `.claude/commands/{name}.md`
2. Add trigger patterns to `.claude/workflow-patterns.md`
3. Document in `.claude/COMMANDS.md`

Or use: `/create-command`

### Creating Agents

1. Define in `.claude/agents/{name}-agent.md`
2. Use templates: specialist, research, orchestrator

Or use: `/create-agent`

### Extending Patterns

Add reusable patterns to `knowledge/patterns/`:
- Architecture patterns
- Implementation patterns
- Integration patterns

Use template: `.claude/templates/reusable-pattern.md`

---

## MCP Server Integration

Use Evolving with Claude Desktop (no API key required):

### Setup

1. Copy `.mcp.json` to Claude Desktop config
2. Update the path to your Evolving directory
3. Restart Claude Desktop

See [SETUP_MCP.md](SETUP_MCP.md) for detailed instructions.

### Available Tools

- **Read**: idea_list, knowledge_search, project_list, read_file
- **Write**: idea_create, idea_update, prompt_add, learning_add

---

## System Statistics

| Component | Count |
|-----------|-------|
| Agents | 30 |
| Commands | 43 |
| Skills | 6 |
| Hooks | 4 |
| Rules | 28 |
| Scenarios | 2 |
| Templates | 37 |
| Patterns | 50 |
| Learnings | 28 |
| Blueprints | 7 |

---

## How It Works

### Cumulative Learning

The system builds knowledge over time:

1. **Session work** → Documented in handoffs
2. **Problems solved** → Saved as experiences
3. **Patterns discovered** → Added to patterns library
4. **Plans completed** → Archived for reference
5. **Projects documented** → Connected to learnings

### Automatic Connections

The system finds relationships:
- Ideas ↔ Projects
- Projects ↔ Patterns
- Patterns ↔ Learnings
- Everything ↔ Knowledge Graph

### Evolution

The system grows with you:
- New categories created as needed
- Connections discovered automatically
- Skills tracked and updated
- Prompt library expands with projects

---

## Documentation

| Document | Purpose |
|----------|---------|
| [START.md](START.md) | User quick start |
| [BEGINNER-GUIDE.md](BEGINNER-GUIDE.md) | Step-by-step introduction |
| [START-SMALL.md](START-SMALL.md) | Minimal getting started |
| [SETUP_MCP.md](SETUP_MCP.md) | MCP server setup |
| [.claude/COMMANDS.md](.claude/COMMANDS.md) | Full command reference |
| [.claude/SYSTEM-MAP.md](.claude/SYSTEM-MAP.md) | Component inventory |
| [knowledge/index.md](knowledge/index.md) | Knowledge base entry |

---

## Version

**Version**: 3.1.0
**Created**: 2024-11-22
**Last Updated**: 2026-01-02
**Status**: Production Ready

---

## Philosophy

**AI-First**: Built for Claude, optimized for AI collaboration.

**Sparring over Yes-Saying**: Honest feedback, challenge assumptions.

**80/20 Principle**: Focus on what brings real value.

**Everything Connected**: No isolated knowledge - all linked and findable.

---

## Getting Help

- Start with [BEGINNER-GUIDE.md](BEGINNER-GUIDE.md) for introduction
- Use `/system-health` to diagnose issues
- Check `.claude/COMMANDS.md` for all available commands
- Ask Claude: "What can you help me with?"

---

**License**: MIT
