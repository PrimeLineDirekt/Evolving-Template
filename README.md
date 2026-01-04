# Evolving - AI-Powered Second Brain & Development System

A highly optimized system for **AI-First Development** that transforms Claude Code into an expert with persistent memory, automatic context loading, and continuous learning.

![System Blueprint](assets/system-blueprint.png)

---

## What Makes This System Special?

### The Problem

Claude Code starts every session as an "Amnesiac with Tool Belt" - brilliant reasoning, but zero memory of past sessions, learned lessons, or project context.

### The Solution

**Evolving** transforms Claude into a **Disciplined Engineer** with:

| Feature | Effect |
|---------|--------|
| **Domain Memory** | Persistent project state across sessions |
| **Experience Memory** | Learns from past failures & successes |
| **Context Router** | Automatically loads relevant knowledge (20+ routes) |
| **Tiered Architecture** | 67% token reduction through on-demand loading |
| **Knowledge Graph** | Connected knowledge with entity relationships |
| **Plain Text Detection** | Natural language triggers for 40+ commands |

---

## Efficiency: 67% Token Savings

### Tiered Context Architecture

Instead of 34K+ tokens at session start:

```
WITHOUT Evolving:
┌─────────────────────────────────────────────────┐
│ Everything loaded: 34K+ Tokens                  │
│ CLAUDE.md + all Rules + all Patterns + ...      │
│ → Context Degradation, Lost-in-the-Middle       │
└─────────────────────────────────────────────────┘

WITH Evolving (Tiered Architecture):
┌─────────────────────────────────────────────────┐
│ CORE (~5K Tokens): Always loaded                │
│ ├─ CLAUDE.md (compact)                          │
│ ├─ core-principles.md                           │
│ ├─ workflow-detection.md                        │
│ └─ domain-memory-bootup.md                      │
├─────────────────────────────────────────────────┤
│ ON-DEMAND: Context Router loads when needed     │
│ ├─ debugging/   → only on error keywords        │
│ ├─ memory/      → only on memory work           │
│ └─ creation/    → only on agent/skill creation  │
└─────────────────────────────────────────────────┘

Result: ~5K instead of 34K+ Tokens = 67% savings
```

### How It Works

```
User Input: "I have a TypeScript error"
                    │
                    ▼
┌───────────────────────────────────────┐
│ Context Scout analyzes keywords       │
│ → "error" → Route: debugging          │
└──────────────────┬────────────────────┘
                   │
                   ▼
┌───────────────────────────────────────┐
│ Context Router loads automatically:   │
│ ├─ pattern-systematic-debugging       │
│ ├─ rule-observe-before-editing        │
│ ├─ rule-evidence-before-claims        │
│ └─ agent-debugger (if needed)         │
└──────────────────┬────────────────────┘
                   │
                   ▼
      Claude has precise context
      (instead of irrelevant mass)
```

---

## The 5 Intelligence Layers

### 1. Domain Memory - Persistent Project State

```json
// _memory/projects/{your-project}.json
{
  "name": "Your Project",
  "state": {
    "current_phase": "Feature Implementation",
    "last_session": "2026-01-04"
  },
  "progress": [
    {"d": "01-04", "a": "API endpoints created", "r": "5 routes"}
  ],
  "failures": [
    {"what": "Auth middleware", "why": "Token expired", "learned": "Add refresh logic"}
  ]
}
```

**Effect**: Session starts with: *"Project: Your Project | Phase: Feature Implementation | Last Session: Yesterday, API endpoints created"*

### 2. Experience Memory - Learning from Experience

6 experience types with automatic decay:

| Type | Description | Example |
|------|-------------|---------|
| `solution` | Problem + Fix | "Build error → Extend interface" |
| `pattern` | Reusable approach | "ICS Framework for image generation" |
| `decision` | Architecture decision | "LangGraph instead of n8n" |
| `workaround` | Temporary fix | "API timeout → Retry with backoff" |
| `gotcha` | Known pitfall | "FAL.ai Edit: image_urls is Array!" |
| `preference` | User preference | "English preferred, sparring style" |

**Automatic Decay**: Unused experiences lose relevance over time. Active access boosts score.

### 3. Context Router - Intelligent Routes

Automatic context loading based on keywords:

```
"I want to create a new agent"
       │
       ▼
Route: agent-creation
       │
       ├─ Primary (load immediately):
       │   ├─ template-specialist-agent
       │   ├─ template-research-agent
       │   └─ skill-template-creator
       │
       └─ Secondary (on demand):
           ├─ pattern-progressive-disclosure
           ├─ pattern-multi-agent-orchestration
           └─ learning-12-factor-agents
```

### 4. Knowledge Graph - Connected Knowledge

```
~150 Nodes │ ~200 Edges │ Unified Taxonomy

Example connections:
┌────────────────────┐       uses        ┌──────────────────────┐
│ agent-idea-        │──────────────────▶│ pattern-research-    │
│ validator          │                   │ confidence-scoring   │
└────────────────────┘                   └──────────────────────┘
        │                                          │
        │ part_of                                  │ documented_in
        ▼                                          ▼
┌────────────────────┐                   ┌──────────────────────┐
│ scenario-          │                   │ learning-agentic-    │
│ idea-management    │                   │ architectures        │
└────────────────────┘                   └──────────────────────┘
```

### 5. Progressive Disclosure - Knowledge on Demand

```
Level 1: Summary (300 Tokens)
         ↓ when needed
Level 2: Reference (1000 Tokens)
         ↓ for deep-dive
Level 3: Full Documentation (3000+ Tokens)

90% of the time Level 1 is enough!
```

---

## Plain Text Detection

You don't need to memorize commands. Just speak naturally:

| You say... | System detects... |
|------------|-------------------|
| "I have a new idea" | `/idea-new` (Confidence: 9/10) |
| "Process the inbox" | `/inbox-process` |
| "What's next?" | `/whats-next` |
| "Analyze this repo" | `/analyze-repo` |
| "Debug this error" | `/debug` |

**Important**: System ALWAYS asks for confirmation, never executes blindly.

---

## Components Overview

| Component | Count | Location |
|-----------|-------|----------|
| **Commands** | 43 | `.claude/commands/` |
| **Agents** | 30 | `.claude/agents/` |
| **Skills** | 6 | `.claude/skills/` |
| **Patterns** | 50 | `knowledge/patterns/` |
| **Learnings** | 28 | `knowledge/learnings/` |
| **Rules** | 28 | `.claude/rules/` |
| **Blueprints** | 7 | `.claude/blueprints/` |
| **Scenarios** | 2 | `.claude/scenarios/` |
| **Templates** | 37 | `.claude/templates/` |

---

## Quick Start

### Prerequisites

- Claude Code CLI installed
- Clone this repository

### Getting Started

```bash
# Clone the repository
git clone https://github.com/YourUsername/Evolving.git my-evolving
cd my-evolving

# Start Claude Code
claude
```

### Your First Session

Claude automatically reads:
1. `_memory/index.json` → Active project
2. `_memory/projects/{active}.json` → Status, progress, failures
3. Announces: "Project X | Phase Y | Last progress Z"

### Personalize Your System

1. Open `_ONBOARDING.md` and fill in your details
2. Tell Claude: "Process the onboarding"
3. System integrates your profile

---

## Key Commands

| What you want | Command |
|---------------|---------|
| Develop an idea | `/idea-new`, `/idea-work` |
| Add knowledge | `/knowledge-add` |
| Analyze project | `/project-analyze` |
| Debug | `/debug` |
| End session | `/whats-next` |
| System health | `/system-health` |

---

## Session Handoffs

```
Session 1: Working on Feature X
    │
    ▼
/whats-next creates handoff:
    ├─ What was achieved
    ├─ Open tasks
    ├─ Key decisions
    └─ Next steps
    │
    ▼
Session 2: Starts with full context
    "Last session: Feature X 80% done.
     Next step: Write tests.
     Known blocker: API timeout on large requests."
```

---

## Multi-Agent Orchestration

```
Complex Task
      │
      ▼
┌─────────────────────────────────────────────────┐
│ Main Agent coordinates:                         │
│                                                 │
│   ┌──────────────┐   ┌──────────────┐          │
│   │ Explore      │   │ Research     │          │
│   │ Agent        │   │ Agent        │          │
│   │ (Codebase)   │   │ (Web)        │          │
│   └──────┬───────┘   └──────┬───────┘          │
│          │                   │                  │
│          └─────────┬─────────┘                  │
│                    ▼                            │
│            Summary back                         │
│            (~500 tokens instead of 10K)         │
└─────────────────────────────────────────────────┘
```

**Benefit**: Each sub-agent has its own 200K context window. Main stays lean.

---

## Architecture

```
evolving/
├── START.md                 # User Entry Point
├── CLAUDE.md                # Compact System Context
│
├── .claude/                 # Claude Code Integration
│   ├── commands/            # 43 Slash Commands
│   ├── agents/              # 30 Specialized Agents
│   ├── skills/              # 6 Progressive Skills
│   ├── rules/               # 28 Modular Rules
│   ├── blueprints/          # 7 System Templates
│   ├── scenarios/           # Context Bundles
│   └── templates/           # Component Templates
│
├── _memory/                 # Persistent State
│   ├── index.json           # Active Context
│   ├── projects/            # Project Memory
│   ├── experiences/         # Learning Memory
│   └── preferences/         # User Preferences
│
├── _graph/                  # Knowledge Graph
│   ├── nodes.json           # Entities
│   ├── edges.json           # Relationships
│   └── cache/
│       └── context-router.json  # Auto-Routes
│
├── _handoffs/               # Session State
│
├── knowledge/               # Knowledge Base
│   ├── patterns/            # Reusable Patterns
│   ├── learnings/           # Documented Insights
│   ├── prompts/             # Prompt Templates
│   ├── references/          # Tool References
│   └── personal/            # Your Profile
│
└── mcp_server/              # Claude Desktop Integration
```

---

## System Philosophy

### AI-First

- **For Claude**: Structured JSON, graph connections, keyword routes
- **For User**: START.md, natural language, simple commands

### Sparring > Yes-Saying

System challenges assumptions, offers alternatives, is radically honest.

### 80/20 Focus

What brings real value? No over-engineering.

### Single Source of Truth

One source per concept, no duplication.

---

## Documentation

| Entry Point | Description |
|-------------|-------------|
| [START.md](START.md) | User Quick Start |
| [BEGINNER-GUIDE.md](BEGINNER-GUIDE.md) | Step-by-step intro |
| [.claude/COMMANDS.md](.claude/COMMANDS.md) | All commands |
| [.claude/SYSTEM-MAP.md](.claude/SYSTEM-MAP.md) | Component inventory |
| [knowledge/index.md](knowledge/index.md) | Knowledge Base Index |

---

## Version

**Version**: 3.1.0
**Last Updated**: 2026-01-04
**Status**: Production Ready

---

> *"The agent is just a policy that transforms one memory state into another."*
> *— This system makes that transformation intelligent.*

---

**License**: MIT
