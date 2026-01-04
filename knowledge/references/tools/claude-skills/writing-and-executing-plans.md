---
title: "Writing and Executing Plans"
type: reference
category: claude-skill
domain: [planning, execution, workflow, collaboration]
source: obra/superpowers
source_date: 2025-12-13
completeness: complete
tags: [planning, execution, tasks, batches, checkpoints, implementation]
---

# Writing and Executing Plans

## TL;DR

Two complementary skills: **Writing Plans** creates 2-5 minute atomic tasks with exact paths and code. **Executing Plans** runs in batches of 3 with checkpoint reviews. Together they transform designs into working code systematically.

---

# Part 1: Writing Plans

## When to Use

- After brainstorming/design phase
- Before implementation begins
- When multiple developers will work on feature
- When work spans multiple sessions

## Core Principle

Plans assume developers have **strong technical skills but minimal domain knowledge**. Every task must be self-contained with exact paths and complete code.

## Task Granularity

Each step = ONE 2-5 minute action.

```markdown
## Good Task Decomposition

### Task 1: Create failing test for email validation
File: `tests/validation.test.ts`
```typescript
test('rejects invalid email format', () => {
  expect(validate('notanemail')).toBe(false);
});
```
Run: `npm test -- --grep "rejects invalid email"`
Expect: FAIL - validate is not defined

### Task 2: Implement minimal validation
File: `src/validation.ts`
```typescript
export function validate(email: string): boolean {
  return email.includes('@');
}
```
Run: `npm test -- --grep "rejects invalid email"`
Expect: PASS

### Task 3: Commit progress
Run: `git add . && git commit -m "feat: add basic email validation"`
Expect: Clean commit with passing tests
```

## Plan Structure

```markdown
# Implementation Plan: [Feature Name]

## Goal
[One sentence describing what we're building]

## Architecture Summary
[2-3 sentences explaining approach]

## Tech Stack
- [Framework/Library 1]
- [Framework/Library 2]

## Execution
Use `executing-plans` skill with batch size 3

---

## Section 1: [Component Name]

### Task 1.1: [Description]
**Files:**
- Create: `path/to/new/file.ts`
- Modify: `path/to/existing/file.ts`
- Test: `tests/file.test.ts`

**Code:**
```typescript
// Complete, copy-paste-ready code
```

**Verification:**
```bash
npm test -- --grep "test name"
# Expected: PASS
```

### Task 1.2: [Description]
...

---

## Section 2: [Component Name]
...
```

## File Location

Save plans to: `docs/plans/YYYY-MM-DD-<feature-name>.md`

---

# Part 2: Executing Plans

## When to Use

- When you have a written plan
- For systematic implementation
- When you need checkpoint reviews
- For batched execution with validation

## The Batch Model

```
┌─────────────────────────────────────────────────────────────┐
│                    EXECUTION CYCLE                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Load Plan → Review → Execute Batch → Report → Feedback    │
│       │                     │              │        │       │
│       ▼                     ▼              ▼        ▼       │
│  Raise Issues         3 Tasks Each    Summarize   Modify   │
│  If Needed           With Verify      Changes     If Asked │
│                                                             │
│                    [Repeat Until Complete]                  │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Step-by-Step Process

### Step 1: Load and Review Plan

```markdown
## Plan Review Checklist

- [ ] Read entire plan
- [ ] Identify potential issues
- [ ] Verify all paths exist or can be created
- [ ] Confirm dependencies are available
- [ ] Raise concerns BEFORE starting

If issues found:
"Before we start, I have concerns about:
1. [Issue 1]
2. [Issue 2]
Should we address these first?"
```

### Step 2: Execute Batch (Default: 3 Tasks)

```markdown
## Batch Execution

### Task 1: [Description]
Status: in_progress → completed
Steps executed:
- Created file at path/to/file.ts
- Added 24 lines of code
- Verification: `npm test` → PASS

### Task 2: [Description]
Status: in_progress → completed
Steps executed:
- Modified existing file
- Added validation logic
- Verification: `npm test` → PASS

### Task 3: [Description]
Status: in_progress → completed
Steps executed:
- Added integration test
- Verification: All 12 tests passing
```

### Step 3: Report and Pause

```markdown
## Batch 1 Complete

### Summary
- Created EmailValidator class
- Added 3 validation methods
- Implemented 4 tests (all passing)

### Verification Results
```
✓ 12 tests passing
✓ No TypeScript errors
✓ Lint clean
```

### Files Changed
- Created: `src/validators/email.ts`
- Created: `tests/validators/email.test.ts`
- Modified: `src/index.ts` (added export)

**Ready for feedback.**
```

### Step 4: Continue Based on Feedback

After receiving feedback:
1. Incorporate any requested changes
2. Execute next batch
3. Repeat cycle until complete

### Step 5: Finish Development

When all tasks done:
```markdown
## All Tasks Complete

### Final Summary
- 9 tasks completed across 3 batches
- 24 tests passing
- 3 new files, 2 modified files

### Ready for Branch Completion
Invoking `finishing-a-development-branch` skill...
```

## Stop Conditions

**Immediately halt and ask if:**

| Situation | Action |
|-----------|--------|
| Dependency missing | "Task 4 requires library X which isn't installed. Should I add it?" |
| Test fails mid-batch | "Task 2 verification failed. Error: [details]. Should I investigate?" |
| Plan has gaps | "Task 6 references file that doesn't exist. Options: A) Create it, B) Skip" |
| Instruction unclear | "Task 3 says 'add validation' but doesn't specify which fields. Clarify?" |
| Repeated failures | "This is the 3rd attempt. Should we reconsider the approach?" |

**Principle:** "Ask for clarification rather than guessing."

---

# Part 3: Parallel Agent Dispatch

## When to Use

- 3+ unrelated failures across different files
- Independent problems that don't share state
- Investigations that won't interfere

## NOT for

- Causally related failures
- Problems requiring full system context
- Overlapping code sections

## Process

```markdown
## Parallel Dispatch Setup

### Domain Identification
Group failures by component:
1. Agent 1: auth.test.ts (3 failures) - Token expiry logic
2. Agent 2: api.test.ts (2 failures) - Response parsing
3. Agent 3: cache.test.ts (1 failure) - TTL calculation

### Verify Independence
- [ ] No shared state between domains
- [ ] Fixes won't conflict
- [ ] Each can be understood alone

### Dispatch Prompt Template

For each agent:
```
Fix the failing tests in [specific file]:
- Test: [name] - expects [behavior]
- Test: [name] - expects [behavior]

Error messages:
[paste relevant errors]

Your task:
1. Identify root cause
2. Implement minimal fix
3. Verify tests pass

Constraints:
- Do NOT modify code outside this file
- Do NOT change test expectations

Return: Summary of findings and changes
```
```

## Integration After Dispatch

```markdown
## Integration Checklist

- [ ] Review each agent's summary
- [ ] Check for conflicting changes
- [ ] Run full test suite
- [ ] Verify no systematic errors

If conflicts:
"Agent 1 and Agent 2 both modified utils.ts.
Agent 1 change: [description]
Agent 2 change: [description]
How should we reconcile?"
```

---

## Quick Reference

### Writing Plans Checklist
```markdown
- [ ] One sentence goal
- [ ] 2-3 sentence architecture
- [ ] Each task is 2-5 minutes
- [ ] Exact file paths provided
- [ ] Complete code blocks (copy-paste ready)
- [ ] Verification commands included
- [ ] Expected outputs specified
- [ ] Saved to docs/plans/YYYY-MM-DD-name.md
```

### Executing Plans Checklist
```markdown
- [ ] Read entire plan first
- [ ] Raise concerns before starting
- [ ] Execute in batches of 3
- [ ] Verify after each task
- [ ] Report after each batch
- [ ] Wait for feedback
- [ ] Stop when blocked
- [ ] Finish with branch completion skill
```

### Parallel Dispatch Checklist
```markdown
- [ ] 3+ independent failures
- [ ] Domains don't overlap
- [ ] Prompts have specific scope
- [ ] Constraints clearly stated
- [ ] Verify no conflicts after
- [ ] Run full test suite
```

---

## Related Skills

- **brainstorming** - Design phase before planning
- **finishing-a-development-branch** - After execution complete
- **systematic-debugging** - When tasks fail
- **test-driven-development** - For test-first tasks

---

**Source:** obra/superpowers
**Navigation:** [← Claude Skills](index.md) | [← References](../../index.md)
