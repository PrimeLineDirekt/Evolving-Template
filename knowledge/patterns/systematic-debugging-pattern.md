# Systematic Debugging Pattern

**Source**: obra/superpowers
**Extracted**: 2025-12-28
**Type**: Development Workflow

---

## Iron Law

> "NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST"

The urge to "just try something" is the enemy. Every fix without understanding is a coin flip that compounds complexity.

---

## The 4 Phases

### Phase 1: Root Cause Investigation

**DO NOT touch any code yet.**

```
1. READ error messages completely
2. REPRODUCE the issue (get exact steps)
3. CHECK recent changes (git diff, git log)
4. GATHER evidence (logs, stack traces, state)
```

**Questions to answer:**
- What exactly is failing?
- When did it start failing?
- What changed recently?

### Phase 2: Pattern Analysis

**Find working examples to compare.**

```
1. FIND similar working code in codebase
2. COMPARE broken vs working
3. IDENTIFY the key differences
4. UNDERSTAND why working code works
```

**The insight**: Working code is your best teacher.

### Phase 3: Hypothesis Testing

**One hypothesis at a time.**

```
1. FORM a single, testable hypothesis
2. PREDICT what you'll see if hypothesis is correct
3. TEST with minimal change
4. VERIFY - was prediction correct?
```

**If hypothesis wrong**: Go back to Phase 1 with new evidence.

### Phase 4: Implementation

**Only after root cause is understood.**

```
1. WRITE failing test that captures the bug
2. MAKE single, focused fix
3. VERIFY test passes
4. CHECK no regressions
```

**After 3+ failures in same area**: Question the architecture, not just the fix.

---

## Common Rationalizations (Red Flags)

| Thought | Reality |
|---------|---------|
| "I'll just try this one thing" | Coin flip. Compounds complexity. |
| "The fix is obvious" | Obvious fixes often miss root cause. |
| "I don't have time to investigate" | Shortcuts take longer. |
| "This worked before" | Something changed. Find what. |

---

## Integration with /debug Command

This pattern extends the existing `/debug` command with:

1. **Stricter Phase Discipline**: No jumping between phases
2. **Pattern Analysis Phase**: Explicit step to find working examples
3. **Hypothesis Testing**: Scientific method applied
4. **Architecture Questioning**: After repeated failures

---

## Checklist

Before fixing:
- [ ] Error message fully understood?
- [ ] Issue reproducible?
- [ ] Recent changes reviewed?
- [ ] Working example found?
- [ ] Single hypothesis formed?
- [ ] Failing test written?

---

## Related

- [/debug Command](../../.claude/commands/debug.md)
- [Verification Before Completion](./verification-before-completion-pattern.md)
