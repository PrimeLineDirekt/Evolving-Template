# Skill Creation with TDD Methodology

**Source**: obra/superpowers (writing-skills)
**Extracted**: 2025-12-28
**Type**: Meta-Learning

---

## Key Insight

Skills should be developed with the same rigor as code: Test-Driven Development applied to documentation.

```
Code TDD:
  Write failing test → Write code → Verify pass

Skill TDD:
  Define pressure scenario → Write skill → Test with subagent
```

---

## The Pressure Scenario Pattern

A "test case" for a skill is a **pressure scenario**: a real situation where the skill should trigger and guide behavior.

### Creating Pressure Scenarios

```markdown
## Test: {Scenario Name}

**Setup**: {Context that should trigger skill}
**Pressure**: {What makes this hard without the skill}
**Expected**: {Behavior the skill should produce}
**Failure Mode**: {What happens without skill}
```

### Example

```markdown
## Test: Bug in Unfamiliar Code

**Setup**: User reports bug in module I haven't seen before
**Pressure**: Urge to "just try something"
**Expected**: Follow 4-phase debugging, resist quick fixes
**Failure Mode**: Random changes, hours wasted, bug remains
```

---

## Skill Structure Best Practices

### SKILL.md Frontmatter

Only two fields allowed:
```yaml
---
name: skill-name
description: What it does and when to use it
---
```

**Frontmatter Requirements** (Official Anthropic):
- `name`: Max 64 chars, lowercase + numbers + hyphens only
- `description`: Max 1024 chars, non-empty
- **ALWAYS third person** ("Processes files" not "I help you")

**CRITICAL**: Description should include WHAT + WHEN, not workflow summary!

**Naming Convention**: Gerund form recommended:
- `processing-pdfs` (good)
- `analyzing-spreadsheets` (good)
- `helper`, `utils` (avoid)

```yaml
# WRONG:
description: Use for debugging. Follows 4-phase process with root cause analysis.

# RIGHT:
description: Use when debugging issues before attempting fixes
```

### Claude Search Optimization (CSO)

Skills are found by keyword matching. Optimize for discovery:

```markdown
## Keywords to Include

- Synonyms: "debug", "fix", "troubleshoot", "investigate"
- User phrases: "not working", "broken", "error", "failing"
- Actions: "find the bug", "figure out why"
```

---

## Token Efficiency

| Skill Type | Target Size | Reason |
|------------|-------------|--------|
| Frequently-loaded | <200 words | Loaded often, minimize overhead |
| Reference skills | <500 words | Comprehensive but focused |
| Full workflows | <1000 words | Complete process documentation |

---

## Skill Types

### Technique Skills
Step-by-step process that must be followed exactly.
- TDD, Debugging, Verification
- Rigid: don't adapt away discipline

### Pattern Skills
Principles to apply with judgment.
- Orchestration, Review patterns
- Flexible: adapt to context

### Reference Skills
Information to consult when needed.
- API references, checklists
- Lookup: use as reference

---

## Testing Skills with Subagents

Before finalizing a skill:

```
1. Create fresh subagent (no prior context)
2. Give it the pressure scenario
3. Observe: Does it find and use the skill?
4. Observe: Does the skill guide correct behavior?
5. Iterate until skill passes
```

### The RED-GREEN-REFACTOR Cycle for Skills

```
RED Phase:
  → Run scenarios WITHOUT the skill
  → Document agent failures and rationalizations verbatim
  → These become your prevention targets

GREEN Phase:
  → Create skill addressing documented failures
  → Test with pressure scenarios
  → Verify correct behavior under pressure

REFACTOR Phase:
  → Watch for new rationalizations
  → Add explicit counters in skill
  → Update description, add red flags
```

> "If you didn't watch an agent fail without the skill, you don't know if the skill prevents the right failures."

### Combined Pressure Testing

Best tests combine 3+ pressures:

| Pressure Type | Example |
|---------------|---------|
| Time constraint | "We need this shipped today" |
| Sunk cost | "We already spent hours on this approach" |
| Authority | "The senior dev said to do it this way" |
| Exhaustion | "This is the 5th attempt" |
| Social | "Everyone else does it this way" |

### Multi-Model Testing

Skills perform differently across models. Test with:
- **Haiku**: Fast, may skip steps
- **Sonnet**: Balanced, standard behavior
- **Opus**: Thorough, may over-elaborate

---

## Anti-Rationalization Techniques

When agents try to skip skill guidance:

| Rationalization | Counter in Skill |
|-----------------|------------------|
| "This is a simple case" | "Even for 'simple' cases, follow full process" |
| "I already know the answer" | "Verify assumptions before acting" |
| "This would take too long" | "Shortcuts cost more time in debugging" |
| "The user wants speed" | "Quality prevents rework" |

Add explicit negations:
```markdown
## Red Flags

- Starting without full context loaded
- Skipping verification "because it's obvious"
- Citing time pressure to skip steps
```

---

## Anti-Patterns in Skill Creation

| Anti-Pattern | Problem | Fix |
|--------------|---------|-----|
| Workflow in description | Pollutes skill discovery | Description = trigger only |
| Too long | Token waste, skimming | Strict word limits |
| No pressure scenarios | Can't verify effectiveness | Write tests first |
| Rigid when should be flexible | Over-constrains agent | Mark skill type clearly |

---

## Application to Evolving

When creating new skills with `/create-skill`:

1. **Before writing**: Define 2-3 pressure scenarios
2. **Description**: Only triggering conditions
3. **Body**: Progressive disclosure (reference.md pattern)
4. **Test**: Verify with fresh agent context

---

## Related

- [/create-skill Command](../../.claude/commands/create-skill.md)
- [Template Creator Skill](../../.claude/skills/template-creator/)
- [Skill Anti-Patterns Structure](./skill-anti-patterns-structure.md)
- [Anthropic Skill Best Practices](../references/anthropic-skill-best-practices.md) - Official Docs
