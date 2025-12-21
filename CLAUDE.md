# Evolving

## Your Profile

→ Populated through onboarding: `_ONBOARDING.md`
→ Result: `knowledge/personal/about-me.md` and `knowledge/personal/skills.md`

**Working Rules:**
- AI-First: Create with AI, not classical programming
- Sparring > Yes-Saying: Honest feedback, challenge assumptions
- Chain of Thought: Sketch steps first, then implement
- 80/20: What brings real value?
- Task-Tracking: TodoWrite for 3+ steps

---

## System Structure

```
.claude/
├── agents/           # Specialist Agents (idea-*, codebase-analyzer, etc.)
├── commands/         # Workflows (/idea-*, /knowledge-*, /scenario-*, etc.)
├── skills/           # Skills (template-creator, prompt-pro, research-orchestrator)
├── hooks/            # Auto-Hooks (context-monitor, auto-cross-reference, session-summary)
├── scenarios/        # Scenario System (context-based project bundles)
├── templates/        # Templates for Agents, Commands, Skills, Patterns
├── rules/            # Modular behavior rules
├── SYSTEM-MAP.md     # Component inventory
├── COMMANDS.md       # Workflow documentation
└── CONTEXT.md        # Technical details

knowledge/
├── index.md          # Knowledge Base Index
├── projects/         # Project documentation
├── learnings/        # Best practices & insights
├── patterns/         # Reusable patterns
├── prompts/          # Prompt library
├── plans/            # Implementation plans
│   └── archive/      # Completed plans
└── personal/         # User profile & skills

ideas/                # Idea management
└── index.json        # All ideas with status

_inbox/               # Content input for processing
_handoffs/            # Session handoffs for context switching
_memory/              # Domain memory (persistent state)
_graph/               # Knowledge graph (entity relationships)
```

**References:**
→ Quick start: START-SMALL.md
→ Beginner guide: BEGINNER-GUIDE.md
→ All features: START.md
→ System inventory: .claude/SYSTEM-MAP.md
→ All commands: .claude/COMMANDS.md

---

## Projects

_No projects documented yet._

Use `/project-add` to add your first project.

---

## Automatic Rules

### Cross-Reference Sync (CRITICAL)
When changing projects/patterns/learnings/prompts → 5 files stay in sync:
README.md | .claude/CONTEXT.md | knowledge/index.md | START.md | .claude/SYSTEM-MAP.md

### Plan Archival
After implementing all features from `knowledge/plans/`:
1. Set status "Archived" + archival date in file
2. **MOVE** (mv, NOT copy!) to `archive/`
3. Update `index.md` (remove from active, add to archive)

### Workflow Detection
→ All workflows & triggers: .claude/COMMANDS.md
→ Trigger patterns: .claude/workflow-patterns.md

**Confidence-based detection:**
- **9-10 (High)**: Trigger detected → Ask "Should I use /workflow?"
- **6-8 (Medium)**: Carefully ask "Do you mean /workflow?"
- **1-5 (Low)**: Ignore, respond normally

**Rules:**
- NEVER auto-execute without confirmation
- On multi-match: Ask user which workflow fits
- Conservative: Better not trigger than trigger wrong

### Command Creation (CRITICAL)
For EVERY new command ALWAYS:
1. Create command file in `.claude/commands/`
2. Add plain-text trigger in `.claude/workflow-patterns.md`
3. Update COMMANDS.md

**No commands without plain-text detection!**

### Scenario Agent Usage
**When a scenario is active or working in a scenario project:**

1. **BEFORE code work**: Read relevant agent
2. **Apply agent patterns**: Write code following best practices
3. **AFTER code work**: Codebase agent for review

**Agents are experts - use them!**

### Proactive Knowledge Linking
**Find connections proactively:**
- For new ideas → Check synergies with existing ideas
- For projects → Find relevant patterns
- For learnings → Link with affected projects

### Domain Memory Bootup
**At session start:**
1. Read `_memory/index.json` → Active project
2. Read `_memory/projects/{active}.json` → State, progress, failures
3. Announce: "Working on [X]. Last progress: [Y]. Continue?"

### Experience Memory
**When errors occur:**
1. Check `_memory/experiences/` for similar solutions
2. Auto-suggest relevant past fixes
3. Use `/remember` to save new solutions

---

## Load Context When Needed

| When | What to Load |
|------|--------------|
| Idea work | ideas/index.json |
| Parked plans | knowledge/plans/index.md |
| Previous session | _handoffs/ (newest) |
| Deep-dive | .claude/CONTEXT.md |
| Workflow help | .claude/COMMANDS.md |
| Scenario work | `.claude/scenarios/{name}/` |
| Project state | `_memory/projects/{name}.json` |
| Past solutions | `_memory/experiences/` |
