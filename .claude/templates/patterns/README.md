# Pattern Templates

Pattern templates provide structures for documenting reusable architectural and design patterns.

## What are Pattern Templates?

Patterns are proven solutions to recurring problems. They document the problem, solution, trade-offs, and when to apply the pattern.

## When to Use Pattern Templates

- Documenting repeatable solutions
- Capturing architectural decisions
- Sharing design knowledge
- Building pattern libraries

## Available Templates

### 1. Reusable Pattern (`reusable-pattern.md`)

**Structure**: Problem → Solution → Example → Trade-offs

**Use for**: Any repeatable solution pattern

**Examples**:
- Multi-agent orchestration
- API rate limiting strategies
- Data validation patterns
- Error handling approaches

**Key Features**:
- Clear problem statement
- Concrete solution
- Real-world example
- Honest trade-offs
- When to use / not use

## Quick Start

```bash
# 1. Copy template
cp .claude/templates/patterns/reusable-pattern.md knowledge/patterns/my-pattern.md

# 2. Define problem
# What problem does this pattern solve?

# 3. Document solution
# How does this pattern solve it?

# 4. Provide example
# Real implementation from your projects

# 5. Analyze trade-offs
# Pros, cons, when to use, when not to use
```

## Pattern Structure

All patterns follow this structure:

```markdown
---
title: "Pattern Name"
type: pattern
category: {architecture|design|workflow}
created: {DATE}
confidence: {%}
tags: [tag1, tag2]
---

# Pattern Name

## Problem
Clear problem statement

## Solution
How to solve it

## Example
Real-world implementation

## Trade-offs
Pros, cons, when to use

## Related
Links to related patterns
```

## Best Practices

### 1. Clear Problem Statement
State the problem clearly before jumping to solution.

### 2. Concrete Examples
Use real code/implementations, not abstract descriptions.

### 3. Honest Trade-offs
Document both pros and cons. No silver bullets.

### 4. When (Not) to Use
Explicitly state when to use and when NOT to use.

### 5. Confidence Level
Rate your confidence in the pattern based on experience.

## Examples from Evolving

### Multi-Agent Orchestration Pattern

**Problem**: Single AI agents too slow for complex tasks (8-12 min)

**Solution**: Master orchestrator + specialized agents in parallel

**Example**: Multi-domain advisory system (15+ agents)

**Result**: 70% faster (8-12 min → 45 sec)

**Trade-offs**:
- Pros: Dramatically faster, better specialization
- Cons: More complexity, dependency management
- Use when: Complex multi-domain tasks >3 min
- Don't use when: Simple tasks <60 sec

See: `knowledge/patterns/multi-agent-orchestration.md`

## Troubleshooting

### Pattern Too Abstract?

**Add concrete example**: Real code beats abstract description

**Show before/after**: Demonstrate the transformation

**Quantify benefits**: Metrics prove the pattern works

### Pattern Not Reusable?

**Generalize**: Extract core principles from specific case

**Identify variations**: Document pattern variants

**Define boundaries**: When does pattern not apply?

## Related Documentation

- **Production Patterns**: See `knowledge/patterns/`
- **Learnings**: See `knowledge/learnings/`
- **Agent Patterns**: See `knowledge/prompts/patterns/`

---

**Navigation**: [← Templates](./../README.md)
