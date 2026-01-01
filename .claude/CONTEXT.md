# System Context for Claude Code Sessions

**Purpose**: This file provides technical context for Claude Code sessions. Referenced when user uses `@START.md` or `@.claude/CONTEXT.md` in new sessions.

---

## User Profile

**Name**: [Your Name]
**Location**: [Your Location]

**Important**: → Full profile in `knowledge/personal/about-me.md`
**System Instructions**: → `knowledge/personal/system-instructions.md`

**AI-First Approach**:
- Creates almost everything WITH AI - not a traditional programmer
- **Core Competency**: Orchestrating AI tools effectively, designing systems, writing prompts
- **What I create WITH AI**: Full-Stack SaaS, Multi-Agent Systems, Python Automation
- **Independent Skills**: System Architecture, Research Methodology, Product Conceptualization

**Working Style**:
- Learning by doing
- Visual, systematic, pattern recognition
- **Sparring over Yes-Saying** - needs radical honesty, no politeness phrases
- Chain of Thought first - sketch steps, then implement

**Current Focus**:
- **Personal Knowledge System "Evolving"** (this system!)
- [Your Projects - will be filled through onboarding]

**Skills**: → `knowledge/personal/skills.md` (AI-Orchestration, Prompt Engineering, Multi-Agent Systems)

**Goals**:
- [Your Goals - will be filled through onboarding]

---

## System Architecture

### Folder Structure

```
evolving/
├── START.md                      # User-facing Quick Start
├── README.md                     # System Documentation
├── CLAUDE.md                     # Claude Code Instructions
├── .gitignore                    # Git ignore rules
│
├── _inbox/                       # IMPORTANT: Document Processing
│   └── [User drops files here]
│
├── _handoffs/                    # Session Handoffs
│   └── [Auto-generated session docs]
│
├── _memory/                      # Domain Memory (Persistent State)
│   ├── index.json               # Active context
│   ├── projects/                # Per-project state
│   └── experiences/             # Past solutions
│
├── _graph/                       # Knowledge Graph
│   ├── nodes.json               # Entities
│   ├── edges.json               # Relationships
│   └── cache/                   # Context router
│
├── ideas/                        # Idea Management
│   ├── index.json               # Metadata of all ideas
│   └── {category}/              # Auto-generated categories
│       └── {id}.md              # Individual ideas
│
├── workflows/                    # Workflow Automation Engine
│   ├── definitions/             # YAML Workflow Definitions (4)
│   │   ├── morning-briefing.yaml
│   │   ├── weekly-review.yaml
│   │   ├── inbox-processing.yaml
│   │   └── idea-forge-full.yaml
│   ├── permissions/             # Permission Profiles (3)
│   ├── preferences/             # User Preferences (1)
│   ├── schema/                  # JSON Schemas (3)
│   ├── engine/                  # Python Engine
│   └── README.md
│
├── dashboard/                    # Knowledge Hub Web Dashboard
│   ├── src/app/                 # Next.js App Router
│   ├── src/components/          # React Components
│   ├── src/data/                # Learning content
│   └── package.json             # npm run dev → localhost:3000
│
├── knowledge/                    # Knowledge Base
│   ├── index.md                 # Knowledge Index (ALWAYS READ!)
│   ├── projects/                # Project Documentation
│   ├── prompts/                 # Prompt Library
│   │   ├── README.md           # MASTER INDEX of library
│   │   ├── frameworks/         # Meta-Level Prompt Engineering
│   │   ├── research-agents/    # Research & Data Collection
│   │   ├── skills/             # Specialized Workflows
│   │   └── patterns/           # Production-Proven Agent Prompts
│   ├── personal/                # User Profile (3 docs)
│   │   ├── about-me.md         # IMPORTANT: Full profile
│   │   ├── skills.md           # IMPORTANT: AI-First Skills
│   │   └── system-instructions.md
│   ├── learnings/               # Extracted Learnings
│   ├── patterns/                # Reusable Patterns
│   ├── plans/                   # Implementation Plans
│   │   ├── index.md
│   │   └── archive/            # Completed plans
│   ├── sessions/                # Sparring Sessions (auto-generated)
│   ├── resources/               # External Resources & Tools
│   └── external-projects/       # External Codebase Analysis
│
└── .claude/                      # Claude Code Config
    ├── CONTEXT.md               # This file
    ├── COMMANDS.md              # Workflow Documentation
    ├── SYSTEM-MAP.md            # Component Inventory
    ├── workflow-patterns.md     # Auto-Detection Patterns
    ├── settings.json            # Hook Configuration
    ├── commands/                # Slash Commands (43)
    ├── agents/                  # Multi-Agent Orchestration (30)
    ├── scenarios/               # Context-based Project Bundles (2)
    ├── tests/                   # Scenario Testing Framework
    ├── skills/                  # Progressive Disclosure (6)
    ├── hooks/                   # Automation (4)
    ├── rules/                   # Modular Behavior Rules (28)
    └── templates/               # Template System (37 files)
```

---

## Model Selection Strategy

### Quick Model Switcher

**4 Commands for quick model switching:**

- **`/opus`** - Opus (maximum quality for complex reasoning)
- **`/opus+`** - Opus with Ultrathink (maximum extended thinking)
- **`/sonnet`** - Sonnet (balanced performance)
- **`/haiku`** - Haiku (fast & cost-effective)

**Usage**: `/opus What's the best architecture for...` or `/opus` then ask question

### Auto-Optimization per Command

**All workflows automatically use optimal models:**

**Opus (complex tasks):**
- `/sparring` - Deep brainstorming
- `/idea-connect` - Recognize synergies
- `/project-analyze` - External codebase analysis

**Sonnet (balanced):**
- `/idea-new` - Idea analysis
- `/project-add` - Knowledge extraction
- `/onboard-process` - Onboarding analysis

**Haiku (fast & cheap):**
- `/idea-list`, `/knowledge-search`, `/knowledge-add`
- `/inbox-process`, `/create-*`, `/system-health`

**Cost Optimization**: ~70% Haiku, ~20% Sonnet, ~10% Opus

---

## Workflows (Slash Commands)

### Core Workflows

| Command | Purpose | Model |
|---------|---------|-------|
| `/idea-new` | Capture idea with AI analysis | Sonnet |
| `/idea-work` | Deep work on idea (sparring) | Opus |
| `/idea-list` | Show ideas with filters | Haiku |
| `/idea-connect` | Find synergies | Opus |
| `/knowledge-add` | Add to knowledge base | Haiku |
| `/knowledge-search` | Semantic search | Haiku |
| `/project-add` | Document project | Sonnet |
| `/project-analyze` | Analyze external codebase | Opus |
| `/inbox-process` | Process inbox files | Haiku |
| `/sparring` | Free brainstorming | Opus |
| `/whats-next` | Session handoff | Haiku |
| `/remember` | Save experience | Haiku |
| `/recall` | Search experiences | Haiku |

See `.claude/COMMANDS.md` for complete reference.

---

## Workflow Auto-Detection

**Status**: ACTIVE

**Pattern Recognition**:
- Analyze user text for trigger patterns
- On match → **Ask**: "Should I use `/{workflow}`?"
- User confirms → Execute
- **NEVER** trigger automatically without asking

**Patterns**: See `.claude/workflow-patterns.md`

**Confidence Levels**:
- High (9-10): Trigger + ask
- Medium (6-8): Carefully ask
- Low (1-5): Ignore

**Examples**:
- "I have an idea..." → `/idea-new`
- "Show me my ideas" → `/idea-list`
- "Search for API" → `/knowledge-search`
- "Process inbox" → `/inbox-process`

---

## Current System Status

**Last Updated**: 2026-01-02

### Ideas
- **Total**: 0 (will be populated through `/idea-new` or onboarding)

### Projects
- **Total**: 0 (will be populated through `/project-add` or onboarding)

### Knowledge Items
- **Agents**: 30 (18 internal + 12 external)
- **Skills**: 6 (4 internal + 2 external)
- **Commands**: 43 workflows available
- **Templates**: 37 files
- **Patterns**: 50
- **Learnings**: 28
- **Rules**: 28 (3 core + 25 on-demand)
- **Blueprints**: 7

---

## Interaction Guidelines

### At Session Start

1. **Read Context**:
   - This file (CONTEXT.md)
   - `knowledge/personal/about-me.md`
   - `_memory/index.json` (active project)
   - `ideas/index.json` (quick overview)

2. **Ready for**:
   - Execute workflows
   - Plain text detection
   - Inbox processing

### Workflow Detection (Plain Text)

**ALWAYS**:
1. Analyze text for patterns
2. On match: Ask "Should I use `/{workflow}`?"
3. Wait for confirmation
4. Then execute

**NEVER** execute automatically without asking!

### Domain Memory Bootup

**At session start**:
1. Read `_memory/index.json` → Active project
2. Read `_memory/projects/{active}.json` → State, progress
3. Announce: "Working on [X]. Last progress: [Y]. Continue?"

### Knowledge Base Usage

**ALWAYS**:
- Use existing knowledge for context
- Link ideas/projects/knowledge
- Actively find connections
- Update skills after projects

### CRITICAL: Cross-Reference Synchronization

**For EVERY new change:**

When adding something new, it MUST be synchronized in ALL relevant documents:

**Master Documents (ALWAYS keep in sync)**:
1. `README.md` - System Overview & Stats
2. `.claude/CONTEXT.md` - Technical Context (this file!)
3. `knowledge/index.md` - Knowledge Base Index
4. `START.md` - User Stats
5. `.claude/SYSTEM-MAP.md` - Component Inventory

**Example: New Pattern**
✅ Update in: patterns/{name}.md, patterns/README.md, knowledge/index.md, README.md, CONTEXT.md
❌ Only pattern file = INCONSISTENT!

**Rule**: NO half measures - fully synchronized or not at all!

---

## File Formats & Standards

### Idea Format
```markdown
---
id: idea-2024-001
title: "{Title}"
category: {main/sub}
tags: [tag1, tag2]
status: draft|active|paused|completed|archived
potential: {1-10}
created: YYYY-MM-DD
updated: YYYY-MM-DD
---

# {Title}
## Description
## Analysis
## Progress
## Next Steps
```

### Project Format
```markdown
---
project_name: "{Name}"
status: in_development|live|paused|completed
started: YYYY-MM
tech_stack: [techs]
---

# {Name}
## Overview
## Features
## Tech Stack
## Learnings
```

---

## Quick Reference

### File Locations
- Ideas: `ideas/{category}/{id}.md`
- Projects: `knowledge/projects/{name}/README.md`
- Prompts: `knowledge/prompts/{category}/{name}.md`
- Personal: `knowledge/personal/`
- Learnings: `knowledge/learnings/{name}.md`
- Patterns: `knowledge/patterns/{name}.md`
- Plans: `knowledge/plans/` (active) / `knowledge/plans/archive/` (completed)
- Handoffs: `_handoffs/`
- Memory: `_memory/`

### Index Files
- Ideas Index: `ideas/index.json`
- Knowledge Index: `knowledge/index.md`
- Memory Index: `_memory/index.json`

### Important Files
- User Profile: `knowledge/personal/about-me.md`
- Skills: `knowledge/personal/skills.md`
- Workflow Patterns: `.claude/workflow-patterns.md`

---

## Version

- **Current**: 3.1.0
- **Created**: 2024-11-22
- **Last Updated**: 2026-01-02

---

**Ready**: System is fully operational!
