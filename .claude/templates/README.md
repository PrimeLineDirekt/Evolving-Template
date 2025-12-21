# Evolving Template System

The Template System provides production-ready, reusable structures for rapidly building agents, commands, hooks, skills, patterns, and learnings in your Personal Knowledge & Innovation System.

## Quick Start

1. **Choose a template category** based on what you want to create
2. **Copy the template** to your target location
3. **Replace placeholders** with your specific values
4. **Customize** as needed for your use case

```bash
# Example: Creating a new agent
cp .claude/templates/agents/specialist-agent.md .claude/agents/my-new-agent.md

# Replace {DOMAIN}, {DESCRIPTION}, etc. with your values
# Customize the agent's expertise and tools
```

## Template Categories

### Agents (`agents/`)
Pre-built agent architectures for different roles:
- **Specialist Agent**: Domain-expert agents (tax, legal, research, etc.)
- **Research Agent**: Multi-source research and validation
- **Orchestrator Agent**: Coordinates multiple agents in workflows

**When to use**: Building AI agents with specific expertise or coordination roles.

### Commands (`commands/`)
Workflow templates for slash commands:
- **Workflow Command**: Step-by-step user workflows
- **Analysis Command**: Data analysis and reporting

**When to use**: Creating new `/command` functionality in `.claude/commands/`.

### Hooks (`hooks/`)
Event-driven automation templates:
- **Post-Tool-Use Hook**: Trigger actions after tool usage
- **Stop Hook**: Session summary and file creation

**When to use**: Automating cross-referencing, logging, or session summaries.

### Skills (`skills/`)
Reusable skill patterns:
- **Progressive Skill**: Large skills with reference docs (SKILL.md + reference.md + examples.md)
- **Simple Skill**: Single-file skills for straightforward use cases

**When to use**: Building complex, reusable capabilities for Claude.

### Patterns (`patterns/`)
Architectural and design patterns:
- **Reusable Pattern**: Problem → Solution → Example format

**When to use**: Documenting repeatable solutions to common problems.

### Learnings (`learnings/`)
Project learnings templates:
- **Project Learning**: Capture key insights from projects

**When to use**: Documenting insights after completing projects or experiments.

## Placeholder Reference

All templates use consistent placeholders. Replace these when using templates:

| Placeholder | Description | Example |
|------------|-------------|---------|
| `{PROJECT_NAME}` | Name of project or component | "tax-optimizer" |
| `{DESCRIPTION}` | Brief description | "Optimizes tax structure for expats" |
| `{CATEGORY}` | Category or domain | "finance/tax" |
| `{TIMESTAMP}` | ISO date | "2024-11-26" |
| `{DOMAIN}` | Domain/expertise area | "international-tax" |
| `{TOOLS}` | Available tools list | "WebSearch, Read, Bash" |
| `{INPUT_FORMAT}` | Expected input structure | "JSON profile object" |
| `{OUTPUT_FORMAT}` | Expected output structure | "Markdown report" |

## Best Practices

### 1. Start with Templates, Don't Start from Scratch
Templates encode proven patterns. Customize them rather than building from zero.

### 2. Replace ALL Placeholders
Missing placeholders will break your implementation. Use search/replace.

### 3. Keep Templates Updated
When you discover improvements, update the templates for future use.

### 4. Version Your Templates
Templates have frontmatter `template_version`. Track changes for maintainability.

### 5. Progressive Disclosure for Complex Skills
Large skills (>500 lines) should use progressive-skill pattern:
- SKILL.md: Entry point, core functionality
- reference.md: Detailed documentation
- examples.md: Usage examples

### 6. AI-First Design
Templates are optimized for Claude, not humans:
- Precise, structured, no fluff
- Clear input/output contracts
- Explicit tool usage instructions

### 7. READMEs are Human-Friendly
READMEs in each category explain usage for developers, not AI.

## Template Structure

Each template includes:

```yaml
---
template_version: "1.0"
template_type: {agent|command|hook|skill|pattern|learning}
template_name: "{Name}"
description: "{Brief description}"
use_cases: [use-case1, use-case2]
complexity: {low|medium|high}
created: 2024-11-26
---
```

This frontmatter helps track versions and understand template purpose.

## Examples

### Creating a Specialist Agent

```bash
# 1. Copy template
cp .claude/templates/agents/specialist-agent.md .claude/agents/seo-specialist.md

# 2. Replace placeholders
# {DOMAIN} → "seo-optimization"
# {DESCRIPTION} → "SEO analysis and optimization recommendations"
# {TOOLS} → "WebSearch, Read, Grep"

# 3. Customize expertise section
# Add specific SEO knowledge, frameworks, tools
```

### Creating a Workflow Command

```bash
# 1. Copy template
cp .claude/templates/commands/workflow-command.md .claude/commands/project-init.md

# 2. Define workflow steps
# Step 1: Gather project requirements
# Step 2: Create directory structure
# Step 3: Initialize git repository
# Step 4: Create README and documentation

# 3. Add tool usage
# Use Write for files, Bash for git commands
```

### Creating a Pattern

```bash
# 1. Copy template
cp .claude/templates/patterns/reusable-pattern.md knowledge/patterns/api-rate-limiting.md

# 2. Document problem
# Problem: API rate limits cause failures in high-volume scenarios

# 3. Document solution
# Solution: Exponential backoff with jitter and circuit breaker

# 4. Add example
# Example: Implementation in TypeScript with retry logic
```

## Troubleshooting

### Template Not Working?

**Check placeholders**: Ensure all `{PLACEHOLDERS}` are replaced with actual values.

**Check frontmatter**: YAML frontmatter must be valid. Use a YAML validator.

**Check file location**: Templates must be in correct directories (commands in `.claude/commands/`, etc.).

### Agent Not Responding Correctly?

**Check tool configuration**: Ensure agent has access to required tools.

**Check input format**: Verify input matches expected structure in template.

**Check output format**: Ensure agent produces expected output format.

### Skill Not Loading?

**Check SKILL.md**: Progressive skills must have SKILL.md as entry point.

**Check file size**: Skills >500 lines should use progressive pattern.

**Check references**: Verify reference.md and examples.md exist if referenced.

## Contributing Templates

When you create effective patterns, add them as templates:

1. Create template in appropriate category
2. Add frontmatter with version and metadata
3. Use placeholders for customization points
4. Document in category README
5. Add example usage to this master README

## Related Documentation

- **Agents**: See `knowledge/prompts/patterns/` for advanced agent examples
- **Commands**: See `.claude/commands/` for production command examples
- **Patterns**: See `knowledge/patterns/` for architectural patterns
- **Learnings**: See `knowledge/learnings/` for project insights

## Template System Philosophy

**90% AI-Optimized**: Templates are designed for Claude to execute efficiently.

**10% Human-Friendly**: READMEs provide context and guidance for developers.

**Production-Ready**: Templates encode battle-tested patterns from real projects.

**Evolvable**: Templates improve as you discover better patterns.

---

**Version**: 1.0.0
**Created**: 2024-11-26
**Maintained by**: Evolving Template System
