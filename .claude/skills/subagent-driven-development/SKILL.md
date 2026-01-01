---
name: subagent-driven-development
description: Use when executing a detailed implementation plan with multiple independent tasks that need systematic review
---

# Subagent-Driven Development

Execute implementation plans by dispatching independent subagents for each task, with mandatory two-stage review cycles.

## Core Principle

> "Fresh subagent per task + two-stage review (spec then quality) = high quality, fast iteration."

## When to Use

- Detailed implementation plan already exists
- Tasks are largely independent
- Work should remain in current session
- Fresh context per task prevents accumulated confusion

## Workflow

```
For each task in plan:
    ↓
1. Dispatch Implementer Subagent
    - Give full task description
    - Provide context
    - Allow clarifying questions
    - Execute implementation
    ↓
2. Dispatch Spec Reviewer
    - Verify: built what was requested?
    - Nothing more, nothing less
    - If issues → Implementer fixes → Re-review
    ↓
3. Dispatch Quality Reviewer
    - Verify: well-built?
    - Clean, tested, maintainable
    - If issues → Implementer fixes → Re-review
    ↓
4. Mark Task Complete
    ↓
Next Task
```

## Subagent Prompts

See reference.md for full prompts:
- `implementer-prompt.md`
- `spec-reviewer-prompt.md`
- `code-quality-reviewer-prompt.md`

## Red Flags

- Skipping reviews (even for "simple" changes)
- Accepting "close enough" spec compliance
- Advancing with unresolved feedback
- Not answering subagent questions thoroughly

## Key Benefits

1. **Fresh Context**: Each subagent starts clean
2. **Separation of Concerns**: Spec vs Quality reviews
3. **Systematic Progress**: Clear completion criteria
4. **Quality Gates**: No shortcuts allowed

---

**Source**: https://github.com/obra/superpowers
**Integrated**: 2025-12-30
