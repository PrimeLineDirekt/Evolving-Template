# Evolving - Your Second Brain

**New here?** Read `START-SMALL.md` first for a 5-minute quick start!

## Welcome!

**For new Claude Code sessions:**
Just say: `@START.md - New session` and I'll understand the context immediately!

---

## Knowledge Hub Dashboard

**Interactive learning portal** for AI fundamentals directly in your browser:

```bash
cd dashboard && npm run dev
```

Open: http://localhost:3000

**Features:**
- 35 Learning cards (Beginner → Advanced → Expert)
- YouTube videos for each topic
- Progress tracking (LocalStorage)
- Full-text search & filters
- 7 Categories (Fundamentals, Prompting, Models, Tools, Agents, Ethics, Future)

---

## New Here? Start with Onboarding!

**First time?** Fill out the onboarding questionnaire:

1. Open `_ONBOARDING.md` in the root folder
2. Fill in the relevant sections (not everything is required!)
3. Tell me: *"Process the onboarding"*
4. I'll integrate everything and delete the questionnaire

**This gives the system information about:**
- You (skills, background, goals)
- Your projects
- Your ideas
- Your prompts & learnings

The more the system knows about you, the better it can support you!

---

## What Is This?

Evolving is your **Personal Knowledge & Innovation System** - an AI-powered second brain that:
- Captures, analyzes and connects all your ideas
- Extracts knowledge from projects and makes it reusable
- Automatically finds connections between different topics
- Supports you in developing ideas (sparring)
- Never forgets anything

---

## Quick Start

### Quick Model Switching

**Switch AI model for optimal performance:**

```
/opus   → Opus (Maximum quality for complex tasks)
/opus+  → Opus with Ultrathink (Maximum reasoning)
/sonnet → Sonnet (Balanced performance)
/haiku  → Haiku (Fast & cheap)
```

**Example:**
```
/opus Design a complex architecture for...
/haiku What is 2+2?
```

**Tip**: Most workflows automatically select the optimal model!

---

### Idea Management

**Capture new idea:**
```
/idea-new
```
Or just write: *"I have an idea for..."*

**Work on idea:**
```
/idea-work
```
Or: *"Let's work on {idea}"*

**Overview:**
```
/idea-list
```
Or: *"Show me my ideas"*

**Find synergies:**
```
/idea-connect
```
Or: *"Find connections between my ideas"*

---

### Adding Knowledge

**Process files (recommended):**
1. Drop files in `_inbox/`
2. Say: *"Process the inbox"* or use `/inbox-process`
3. I'll automatically categorize and integrate

**Add knowledge directly:**
```
/knowledge-add
```
Or: *"I've learned that..."*

**Document project:**
```
/project-add
```
Or: *"I want to document my {project}"*

---

### Search & Discover

**Search knowledge:**
```
/knowledge-search {topic}
```
Or: *"What do I know about API integration?"*

**Find connections:**
```
/idea-connect
```
Automatically finds synergies between your ideas

---

### Brainstorming & Sparring

**Free thinking:**
```
/sparring
```
Or: *"Let's brainstorm about {topic}"*

Different modes:
- Brainstorming - Expand ideas
- Problem-Solving - Find solutions
- Strategy - Develop plans
- Devil's Advocate - Critical questioning

---

## Your Current Status

<!-- Auto-updated after activities -->

**Ideas:** 0
**Projects:** 0

_Start with onboarding to populate your system!_

**System components (ready):**
- Agents: 13+ (Multi-Agent Orchestration System)
- Skills: 3 (Progressive Disclosure Pattern)
- Templates: 37 (Agents, Commands, Hooks, Skills)
- Commands: 40+ workflows available

---

## How It Works

### Plain Text vs. Slash Commands

You can use **both**:

**Slash Commands** (explicit):
```
/idea-new
/knowledge-search API
```

**Plain Text** (I detect automatically):
```
"I have an idea for..."
→ I ask: "Should I use /idea-new?"

"Search for API best practices"
→ I ask: "Should I use /knowledge-search?"
```

I suggest, you confirm. Simple!

---

## Inbox System

The **fastest** and **most convenient** system:

1. **Drop files** in `_inbox/`:
   - Project READMEs
   - Prompts you want to save
   - Ideas as markdown
   - Notes & learnings

2. **Let me know**:
   - "Process the inbox"
   - Or: `/inbox-process`

3. **I do the rest**:
   - Analyze & categorize
   - Integrate into the right system
   - Ask if original can be deleted

**Perfect for:**
- Project READMEs and documentation
- Prompts you've created
- Quick idea capture

---

## Folder Structure

```
Evolving/
├── START.md              ← You are here!
├── README.md             ← System documentation
│
├── _inbox/               ← Drop files here
│
├── ideas/                ← All your ideas
│   ├── index.json        ← Metadata
│   └── {category}/       ← Categorized
│
├── knowledge/            ← Your knowledge base
│   ├── index.md          ← Knowledge index (start here!)
│   ├── projects/         ← Project documentation
│   ├── prompts/          ← Prompt library
│   ├── plans/            ← Implementation plans
│   │   └── archive/      ← Completed plans
│   └── personal/         ← About you, skills
│
├── _memory/              ← Domain memory (persistent state)
├── _handoffs/            ← Session handoffs
│
└── .claude/commands/     ← All workflows
```

---

## All Workflows Overview

| Command | Purpose | Plain Text Trigger |
|---------|---------|-------------------|
| `/onboard-process` | Process onboarding questionnaire | "Process onboarding" |
| `/idea-new` | New idea with AI analysis | "I have an idea..." |
| `/idea-work` | Work on idea (sparring) | "Work on {idea}" |
| `/idea-list` | Overview & filters | "Show my ideas" |
| `/idea-connect` | Find synergies | "Find connections" |
| `/knowledge-add` | Add knowledge | "I've learned..." |
| `/knowledge-search` | Semantic search | "Search for {topic}" |
| `/project-add` | Document project | "Document project" |
| `/inbox-process` | Process inbox | "Process inbox" |
| `/sparring` | Free brainstorming | "Let's brainstorm" |
| `/scenario` | Activate scenario | "Activate scenario" |
| `/scenario-list` | Show scenarios | "Show scenarios" |
| `/scenario-create` | New scenario | "Create new scenario" |
| `/scenario-edit` | Edit scenario | "Edit scenario" |
| `/whats-next` | Session handoff | "What's next" |
| `/remember` | Save experience | "Remember this" |
| `/recall` | Search experiences | "What do we know about..." |

---

## Typical Workflows

### Scenario 1: New Idea
```
You: "I have an idea for a tool that helps developers"

Me: "Should I use /idea-new?"

You: "Yes"

Me: [Captures idea, analyzes potential, finds connections]
    "Idea captured! Potential: 8/10. Fits your
     background. Should I find synergies with
     your other ideas?"
```

### Scenario 2: Document Project
```
You: [Drop project-readme.md in _inbox/]
     "Process the inbox"

Me: "File recognized as project README.
    Project: {Your Project}
    Should I run /project-add?"

You: "Yes"

Me: [Documents project, extracts skills,
    finds connections to ideas]
    "Project documented! 3 new skills extracted,
     2 connections to ideas found.
     Delete original?"
```

### Scenario 3: Search Knowledge
```
You: "What do I know about API design?"

Me: "Should I use /knowledge-search?"

You: "Yes"

Me: [Searches knowledge base]
    "3 results found:
     - API Best Practices (from project)
     - API Design Prompt (saved)
     - Learning: REST vs GraphQL (from project)"
```

---

## Next Steps

### If you're just starting:

1. **Complete onboarding**:
   - Fill out `_ONBOARDING.md`
   - Say: "Process the onboarding"

2. **Document projects**:
   - Drop your project READMEs in `_inbox/`
   - Say: "Process the inbox"

3. **Save prompts**:
   - Drop your created prompts in `_inbox/`
   - I'll categorize them automatically

4. **Capture first idea**:
   - `/idea-new` or "I have an idea..."

---

## Tips & Tricks

### Work efficiently
- Use **Inbox** for everything you want to save
- **Plain text** when you're in a hurry
- **Slash commands** when you want to be specific

### System grows with you
- Categories created as needed
- Connections discovered automatically
- Skills are tracked

### Having problems?
- Check `.claude/README.md` for details
- Just ask me!

---

## For New Sessions

When you restart Claude Code:

```
@START.md - New session
```

I'll read this file + `.claude/CONTEXT.md` and immediately understand:
- Who you are
- What the system is
- Which workflows are available
- Your current status

**Alternatively** just start writing - I'll detect your intents automatically!

---

## Session Continuity

### Session Handoffs

Before ending a session, use `/whats-next` to create a handoff document:

```
_handoffs/
├── 2025-01-15-feature-work.md
├── 2025-01-14-bug-fixes.md
└── ...
```

The next session can pick up exactly where you left off.

### Domain Memory

Your project state persists across sessions:

```
_memory/
├── index.json          ← Active context
├── projects/           ← Per-project state
└── experiences/        ← Past solutions
```

At session start, I'll announce: "We're working on [X]. Last progress: [Y]. Continue?"

---

## IMPORTANT for Claude Sessions: Cross-Reference Rule

**When adding new content (projects, patterns, learnings, prompts):**

ALWAYS update in ALL relevant documents:
1. `README.md` - System overview & stats
2. `.claude/CONTEXT.md` - Technical context & structure
3. `knowledge/index.md` - Knowledge base index
4. `START.md` - User stats (numbers only)
5. `.claude/SYSTEM-MAP.md` - Component inventory

**No half measures** - either fully synchronized or not at all!

See [README.md](README.md) for details.

---

## Good luck!

This system grows with you. The more you use it, the more valuable it becomes.

**Questions?** Just ask me!

**Ready to go?** Tell me what you want to do or use one of the workflows.

---

**Version**: 3.0.0
**Created**: 2024-11-22
**Last Updated**: 2025-12-22
**Status**: Ready to use
