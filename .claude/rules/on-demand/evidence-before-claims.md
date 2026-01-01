# Evidence Before Claims

**Priority**: HOCH
**Source**: obra/superpowers (verification-before-completion)
**Trigger**: Before ANY completion claim

---

## Iron Law

> "Evidence before claims, always."

NEVER claim something is done, working, fixed, or complete without fresh verification output.

---

## The Gate Function

Before making ANY claim about completion:

```
1. IDENTIFY: What command proves this claim?
2. RUN: Execute the FULL command
3. READ: Full output, check exit code
4. VERIFY: Does output confirm the claim?
5. ONLY THEN: Make the claim
```

---

## Forbidden Claims Without Evidence

| Claim | Required Evidence |
|-------|-------------------|
| "Tests pass" | Fresh `npm test` / `pytest` output |
| "Build works" | Fresh `npm run build` output |
| "Fixed the bug" | Reproduction steps now succeed |
| "Feature complete" | All acceptance criteria verified |
| "No errors" | Actual error-free run output |

---

## Common Traps

### The Memory Trap

```
❌ "Tests passed earlier, so they still pass"
✅ Run tests NOW, show output NOW
```

### The Partial Trap

```
❌ Run quick check, claim full verification
✅ Run FULL test suite
```

### The Assumption Trap

```
❌ "This should work based on my changes"
✅ Actually run it and show the result
```

---

## Verification Template

When completing a task, ALWAYS include:

```markdown
## Verification

Command: `{exact command run}`
Output:
```
{actual output}
```
Exit code: {0 or error}

✅ Verified: {what was confirmed}
```

---

## Integration

This rule complements:
- `systematic-debugging-pattern.md` - Verify fixes
- `/debug` command - Evidence gathering
- Task completion - Verification step

---

## The Bottom Line

**No output? No claim.**

Run the command. Show the result. Then—and only then—claim completion.
