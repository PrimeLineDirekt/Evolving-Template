# Learning Templates

Learning templates provide structures for capturing key insights and learnings from projects and experiences.

## What are Learning Templates?

Learnings document insights gained from projects, experiments, or experiences. They capture what worked, what didn't, and what you'd do differently.

## When to Use Learning Templates

- After completing a project
- After experimenting with new approaches
- After encountering significant challenges
- To capture insights for future reference

## Available Templates

### 1. Project Learning (`project-learning.md`)

**Structure**: Context → Learnings → Challenges → Reusable Insights

**Use for**: Post-project insights and retrospectives

**Examples**:
- SaaS project learnings
- Technical experiment insights
- Process improvement learnings

**Key Features**:
- Project context
- Top learnings (1-5 key insights)
- Challenges and solutions
- Reusable knowledge for future projects
- Related patterns and resources

## Quick Start

```bash
# 1. Copy template
cp .claude/templates/learnings/project-learning.md knowledge/learnings/my-project-learnings.md

# 2. Document context
# What was the project? What was the goal?

# 3. Identify top learnings
# 3-5 most important insights (be specific!)

# 4. Document challenges
# What problems did you face? How did you solve them?

# 5. Extract reusable insights
# What applies to future projects?

# 6. Link related patterns
# Connect to patterns you discovered
```

## Learning Structure

All learnings follow this structure:

```markdown
---
title: "Project Name - Learnings"
source: {PROJECT_NAME}
type: project-learnings
created: {DATE}
confidence: {%}
tags: [tag1, tag2]
---

# Project Name - Learnings

## Context
Project description and goals

## Top Learnings
3-5 key insights with specifics

## Challenges & Solutions
Problems faced and how solved

## Reusable Insights
What applies to future projects

## Related
Links to patterns, resources
```

## Best Practices

### 1. Be Specific
Vague: "API integration is important"
Specific: "OAuth2 flow requires state parameter for security - implement PKCE for mobile apps"

### 2. Quantify When Possible
Vague: "Performance improved"
Specific: "Multi-agent parallelization: 70% faster (8-12 min → 45 sec)"

### 3. Document What Didn't Work
Failures are valuable learning. Document what you tried but didn't work.

### 4. Extract Reusable Patterns
Connect learnings to reusable patterns. Create pattern files if needed.

### 5. Rate Confidence
Be honest about confidence levels based on experience.

## Example Learning Structure

**Context**: Complex multi-agent system project

**Top Learnings**:
1. **Multi-Agent 70% Faster**: Parallel execution vs. sequential
2. **GDPR-First Saves Time**: Compliance from start, not retrofit
3. **Profile-Based Agent Selection**: Efficiency without feature loss
4. **Premium AI Justifies Premium Pricing**: Higher quality = value
5. **Freemium Needs Real Value**: Not just demo, actual usefulness

**Challenges**:
- API limitations → Solution implementation
- Multi-context handling → Dynamic adaptation
- Compliance complexity → Dedicated specialist agents

**Reusable**:
- Compliance-first approach for regulated projects
- Progressive disclosure for complex onboarding
- Multi-agent orchestration for complex tasks

## Troubleshooting

### Learnings Too Vague?

**Add specifics**: Numbers, examples, code snippets

**Show before/after**: Demonstrate the change

**Explain why**: Not just what, but why it matters

### Too Many Learnings?

**Prioritize**: Focus on top 3-5 most impactful

**Group related**: Combine similar insights

**Create separate docs**: Split if covering multiple domains

### Hard to Extract Reusable Insights?

**Ask**: "What would I tell my past self?"

**Generalize**: Remove project-specific details

**Create patterns**: If insight is reusable, make it a pattern

## Related Documentation

- **Production Learnings**: See `knowledge/learnings/`
- **Patterns**: See `knowledge/patterns/`
- **Projects**: See `knowledge/projects/`

---

**Navigation**: [← Templates](./../README.md)
