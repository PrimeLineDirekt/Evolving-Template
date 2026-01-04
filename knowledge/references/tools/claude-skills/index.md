---
title: "Claude Skills Index"
type: reference
category: index
domain: [skills, claude, methodology]
source: obra/superpowers
source_date: 2025-12-13
completeness: complete
tags: [skills, index, methodology, development, debugging, testing]
---

# Claude Skills Reference

Comprehensive skill library from [obra/superpowers](https://github.com/obra/superpowers) for Claude Code.

## Quick Lookup

| Skill | Purpose | Status |
|-------|---------|--------|
| [systematic-debugging](systematic-debugging.md) | 4-Phase Root Cause Analysis | Complete |
| [test-driven-development](test-driven-development.md) | RED-GREEN-REFACTOR | Complete |
| [brainstorming](brainstorming.md) | Interactive Design Refinement | Complete |
| [writing-and-executing-plans](writing-and-executing-plans.md) | Plan Creation & Batch Execution | Complete |
| root-cause-tracing | Backward Data Flow Analysis | Summary |
| verification-before-completion | Confirm Fixes Work | Summary |
| defense-in-depth | Multi-Layer Validation | Summary |
| condition-based-waiting | Async Test Patterns | Summary |
| testing-anti-patterns | What to Avoid | Summary |
| requesting-code-review | Pre-Review Checklist | Summary |
| receiving-code-review | Respond to Feedback | Summary |
| using-git-worktrees | Isolated Workspaces | Summary |
| finishing-a-development-branch | Merge/PR Decisions | Summary |
| subagent-driven-development | Fast Iteration with Quality | Summary |
| writing-skills | Create New Skills | Summary |
| testing-skills-with-subagents | Validate Skill Quality | Summary |
| using-superpowers | Orientation to System | Summary |

---

## Category: Testing

### test-driven-development
**Full Reference:** [test-driven-development.md](test-driven-development.md)

RED-GREEN-REFACTOR cycle. Write failing test → Minimal code → Refactor.

### condition-based-waiting
Handle asynchronous test patterns:
```typescript
// Wait for condition instead of arbitrary timeout
await waitFor(() => expect(element).toBeVisible());

// Use test retries for flaky tests
jest.retryTimes(3);
```

### testing-anti-patterns
**Avoid these patterns:**
- Testing implementation instead of behavior
- Flaky tests with arbitrary waits
- Tests that depend on order
- Mock overuse hiding real bugs
- Testing private methods

---

## Category: Debugging

### systematic-debugging
**Full Reference:** [systematic-debugging.md](systematic-debugging.md)

4-Phase: Investigation → Pattern Analysis → Hypothesis → Implementation

### root-cause-tracing
Trace data flow backward from symptom:
```
Error: "Invalid token"
  ↑
API received: { token: null }
  ↑
Storage returned: null
  ↑
Key mismatch: "auth_token" vs "authToken"  ← ROOT CAUSE
```

### verification-before-completion
Ensure fix actually works:
```markdown
## Verification Checklist
- [ ] Original error no longer occurs
- [ ] Related tests pass
- [ ] No new errors introduced
- [ ] Tested with real data (not just test data)
- [ ] Verified in environment where bug occurred
```

### defense-in-depth
Multiple validation layers:
```typescript
// Layer 1: Input validation
validateInput(data);

// Layer 2: Business logic validation
validateBusinessRules(data);

// Layer 3: Database constraints
await db.insert(data);  // Will fail if constraints violated

// Layer 4: Output validation
validateOutput(result);
```

---

## Category: Collaboration

### brainstorming
**Full Reference:** [brainstorming.md](brainstorming.md)

Interactive design with Socratic questioning.

### writing-and-executing-plans
**Full Reference:** [writing-and-executing-plans.md](writing-and-executing-plans.md)

Create 2-5 min atomic tasks, execute in batches of 3.

### requesting-code-review
Pre-review checklist by severity:
```markdown
## Pre-Review Report

### Blocking Issues (Must Fix)
- [ ] Security vulnerability in auth.ts:45
- [ ] Breaking API change without migration

### Major Issues (Should Fix)
- [ ] Missing error handling in api.ts
- [ ] No tests for edge case

### Minor Issues (Nice to Fix)
- [ ] Inconsistent naming
- [ ] Could extract helper function
```

### receiving-code-review
Respond to feedback systematically:
```markdown
## Review Response

### Accepted Changes
1. Fixed null check in auth.ts ✓
2. Added error handling ✓

### Clarification Needed
3. "Consider caching" - Do you mean Redis or in-memory?

### Respectfully Declined
4. "Rename function" - Current name matches API docs
```

---

## Category: Git Workflow

### using-git-worktrees
Create isolated workspace:
```bash
# Create worktree on new branch
git worktree add ../feature-auth -b feature/auth

# Work in isolation
cd ../feature-auth

# Clean baseline - all tests should pass
npm test

# When done
git worktree remove ../feature-auth
```

### finishing-a-development-branch
Completion checklist:
```markdown
## Branch Completion

### Pre-Merge Checks
- [ ] All tests pass
- [ ] No merge conflicts
- [ ] Code reviewed
- [ ] Documentation updated

### Decision
- [ ] MERGE: Ready for main
- [ ] PR: Needs team review
- [ ] KEEP: More work needed
- [ ] DISCARD: Approach didn't work

### Cleanup
- [ ] Delete branch if merged
- [ ] Remove worktree if used
- [ ] Update related issues
```

---

## Category: Subagent Patterns

### subagent-driven-development
Fast iteration with quality gates:
```markdown
## Subagent Workflow

1. Dispatch fresh subagent for task
2. Subagent completes isolated work
3. Code review before integration
4. Repeat for next task

Benefits:
- Fresh context per task
- No context pollution
- Built-in review checkpoint
```

### dispatching-parallel-agents
*Covered in [writing-and-executing-plans.md](writing-and-executing-plans.md)*

Concurrent subagents for independent problems.

---

## Category: Meta Skills

### writing-skills
Framework for creating new skills:
```markdown
## Skill Structure

/skills/skill-name/
├── SKILL.md       # Main definition
├── EXAMPLES.md    # Usage examples
└── ANTI-PATTERNS.md  # What to avoid

## Skill Template
- Clear activation phrase
- Step-by-step process
- Verification criteria
- Related skills
```

### testing-skills-with-subagents
Validate skill quality:
```markdown
## Skill Testing Process

1. Create test scenario
2. Dispatch subagent with skill
3. Evaluate output quality
4. Iterate on skill definition
```

### using-superpowers
Orientation to system:
```markdown
## Quick Start

1. Announce skill: "I'm using the X skill"
2. Follow skill methodology
3. Reference related skills when needed
4. Verify completion criteria met

## Available Skills
[List of all skills with one-line descriptions]
```

---

## Usage Pattern

Announce when using a skill:
```
"I'm using the systematic-debugging skill to investigate this issue."
```

This ensures:
- Structured methodology applied
- Expectations are clear
- Related skills can be referenced

---

## Skill Combinations

### Bug Fix Workflow
1. `systematic-debugging` - Find root cause
2. `test-driven-development` - Create failing test
3. `verification-before-completion` - Confirm fix

### Feature Development
1. `brainstorming` - Design the feature
2. `writing-plans` - Create implementation plan
3. `executing-plans` - Build in batches
4. `finishing-a-development-branch` - Complete and merge

### Code Review
1. `requesting-code-review` - Pre-review checklist
2. `receiving-code-review` - Respond to feedback
3. `verification-before-completion` - Confirm all addressed

---

## Navigation

**Full Reference Files:**
- [systematic-debugging.md](systematic-debugging.md)
- [test-driven-development.md](test-driven-development.md)
- [brainstorming.md](brainstorming.md)
- [writing-and-executing-plans.md](writing-and-executing-plans.md)

**Up:** [← Tools](../index.md) | [← References](../../index.md) | [← Knowledge Base](../../../index.md)

---

**Source:** obra/superpowers
**Last Updated:** 2025-12-13
