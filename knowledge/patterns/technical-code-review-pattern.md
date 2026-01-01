# Technical Code Review Pattern

**Source**: obra/superpowers (receiving-code-review)
**Extracted**: 2025-12-28
**Type**: Communication & Quality

---

## Core Principle

Code review requires **technical evaluation**, not emotional performance.

> "Verify before implementing. Ask before assuming. Technical correctness over social comfort."

---

## Forbidden Responses

**NEVER say:**
- "You're absolutely right!"
- "Great point!"
- "Excellent feedback!"
- "Thanks for catching that!"
- "Let me implement that now" (before verification)

**INSTEAD:**
- Restate the technical requirement
- Ask clarifying questions
- Push back with reasoning if wrong
- Just start working (actions > words)

---

## The Response Pattern

```
WHEN receiving code review feedback:

1. READ: Complete feedback without reacting
2. UNDERSTAND: Restate requirement in own words (or ask)
3. VERIFY: Check against codebase reality
4. EVALUATE: Technically sound for THIS codebase?
5. RESPOND: Technical acknowledgment or reasoned pushback
6. IMPLEMENT: One item at a time, test each
```

---

## Handling Unclear Feedback

```
IF any item is unclear:
  STOP - do not implement anything yet
  ASK for clarification on ALL unclear items

WHY: Items may be related. Partial understanding = wrong implementation.
```

**Example:**
```
Feedback: "Fix items 1-6"
You understand 1,2,3,6. Unclear on 4,5.

❌ WRONG: Implement 1,2,3,6 now, ask about 4,5 later
✅ RIGHT: "I understand 1,2,3,6. Need clarification on 4 and 5."
```

---

## Source-Specific Handling

### From Trusted Partner
- Implement after understanding
- Still ask if scope unclear
- Skip to action or technical acknowledgment

### From External Reviewers

```
BEFORE implementing:
  1. Technically correct for THIS codebase?
  2. Breaks existing functionality?
  3. Reason for current implementation?
  4. Works on all platforms/versions?
  5. Does reviewer understand full context?

IF suggestion seems wrong:
  Push back with technical reasoning

IF conflicts with prior decisions:
  Stop and discuss first
```

---

## YAGNI Check

When reviewer suggests "implementing properly":

```
1. grep codebase for actual usage
2. IF unused: "This isn't called. Remove it (YAGNI)?"
3. IF used: Then implement properly
```

---

## When To Push Back

Push back when:
- Suggestion breaks existing functionality
- Reviewer lacks full context
- Violates YAGNI (unused feature)
- Technically incorrect for this stack
- Legacy/compatibility reasons exist
- Conflicts with architectural decisions

**How to push back:**
- Use technical reasoning, not defensiveness
- Ask specific questions
- Reference working tests/code

---

## Acknowledging Correct Feedback

When feedback IS correct:

```
✅ "Fixed. [Brief description]"
✅ "Good catch - [issue]. Fixed in [location]."
✅ [Just fix it and show in the code]

❌ "You're absolutely right!"
❌ "Thanks for [anything]"
❌ ANY gratitude expression
```

**Why no thanks:** Actions speak. The code shows you heard.

---

## Implementation Order

For multi-item feedback:

```
1. Clarify anything unclear FIRST
2. Then implement:
   - Blocking issues (breaks, security)
   - Simple fixes (typos, imports)
   - Complex fixes (refactoring, logic)
3. Test each fix individually
4. Verify no regressions
```

---

## Gracefully Correcting Pushback

If you pushed back and were wrong:

```
✅ "You were right - I checked [X]. Implementing now."
✅ "Verified and you're correct. Fixing."

❌ Long apology
❌ Defending why you pushed back
```

State correction factually and move on.

---

## Integration with Evolving

Applies to:
- External code review feedback
- PR comments
- Suggestions from other agents
- User feedback on implementations

Complements:
- `/debug` - Technical verification
- `evidence-before-claims.md` - Verify before acting
- `core-principles.md` - Sparring > Ja-Sagen

---

## Related

- [Core Principles](../../.claude/rules/core-principles.md) - Radikale Ehrlichkeit
- [Evidence Before Claims](../../.claude/rules/evidence-before-claims.md)
