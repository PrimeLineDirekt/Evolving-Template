# Command Templates

Command templates provide structures for creating slash commands (e.g., `/idea-new`, `/knowledge-add`) in `.claude/commands/`.

## What are Command Templates?

Commands are user-facing workflows triggered by typing `/command-name` in the Claude interface. They guide multi-step processes with clear instructions for both the user and Claude.

## When to Use Command Templates

- Creating user workflows (idea capture, knowledge addition, project init)
- Building analysis commands (system health, performance review)
- Implementing automation triggers (batch processing, cleanup)
- Standardizing repetitive tasks

## Available Templates

### 1. Workflow Command (`workflow-command.md`)

**Use for**: Step-by-step user workflows with tool usage.

**Complexity**: Low-Medium

**Examples**:
- `/idea-new` - Capture and analyze ideas
- `/knowledge-add` - Add knowledge to database
- `/project-init` - Initialize new project

**Key Features**:
- Clear step progression
- User input handling
- Tool integration
- Validation and confirmation

### 2. Analysis Command (`analysis-command.md`)

**Use for**: Data analysis and report generation.

**Complexity**: Medium

**Examples**:
- `/system-health` - Analyze system status
- `/idea-connections` - Find idea synergies
- `/performance-review` - Generate performance reports

**Key Features**:
- Data collection
- Analysis framework
- Report generation
- Actionable insights

## Quick Start

### Creating a Workflow Command

```bash
# 1. Copy template
cp .claude/templates/commands/workflow-command.md .claude/commands/my-workflow.md

# 2. Define frontmatter
description: "What this command does"
argument-hint: "[optional: argument description]"

# 3. Define steps
## Step 1: Gather input
## Step 2: Process data
## Step 3: Generate output
## Step 4: Confirm completion

# 4. Test command
# Type /my-workflow in Claude interface
```

### Creating an Analysis Command

```bash
# 1. Copy template
cp .claude/templates/commands/analysis-command.md .claude/commands/analyze-x.md

# 2. Define analysis scope
# What data sources to analyze
# What metrics to calculate
# What insights to generate

# 3. Configure output format
# Charts, tables, summaries
# Recommendations and next steps

# 4. Test and iterate
```

## Command Structure

All commands follow this structure:

```markdown
---
description: Brief description of what the command does
argument-hint: [optional: hint about arguments]
---

Introduction explaining command purpose

## Step 1: {First Step}
Clear instructions for what to do

## Step 2: {Second Step}
More instructions

## Step N: {Final Step}
Completion and confirmation

---

**Important notes**:
- Best practices
- Common pitfalls
- Related commands
```

## Best Practices

### 1. Clear Step Progression
Users should understand what happens in each step.

### 2. Handle Optional Arguments
Support both direct arguments (`/command arg`) and interactive prompts.

```markdown
## Step 1: Get Input

If $ARGUMENTS is provided, use it.
Otherwise, ask user: "Please provide {input}."
```

### 3. Use Appropriate Tools
- `Read` for reading files
- `Write` for creating new files
- `Edit` for modifying existing files
- `Grep/Glob` for searching
- `Bash` for system commands

### 4. Validate and Confirm
Always confirm completion with summary:

```markdown
✓ {Action} completed: {Summary}

Next steps:
- {Related action 1}
- {Related action 2}
```

### 5. Error Handling
Anticipate and handle common errors:

```markdown
**Important**:
- Check if file exists before writing
- Validate input format
- Handle missing dependencies
```

## Command Patterns

### Pattern 1: Input → Process → Output

```
Step 1: Gather input (interactive or argument)
Step 2: Validate input
Step 3: Process data
Step 4: Generate output
Step 5: Confirm and suggest next steps
```

**Use for**: Most workflow commands

### Pattern 2: Collect → Analyze → Report

```
Step 1: Identify data sources
Step 2: Collect data (Read, Grep, Bash)
Step 3: Analyze and calculate metrics
Step 4: Generate insights
Step 5: Format report
Step 6: Provide recommendations
```

**Use for**: Analysis commands

### Pattern 3: Batch Processing

```
Step 1: Identify items to process
Step 2: For each item:
  - Validate
  - Process
  - Log result
Step 3: Summary report
```

**Use for**: Automation commands

## Examples from Production

### `/idea-new` (Workflow Command)
```
Step 1: Get idea (argument or prompt)
Step 2: Analyze idea (category, potential, skills)
Step 3: Generate ID
Step 4: Create markdown file
Step 5: Update index.json
Step 6: Confirm with summary
```

### `/knowledge-add` (Workflow Command)
```
Step 1: Determine knowledge type
Step 2: Get content (file or input)
Step 3: Analyze content (insights, tags, connections)
Step 4: Generate filename and metadata
Step 5: Create structured file
Step 6: Update skills and index
Step 7: Create cross-references
Step 8: Confirm with summary
```

## Troubleshooting

### Command Not Appearing?

**Check file location**: Must be in `.claude/commands/`

**Check filename**: Use lowercase with hyphens: `my-command.md`

**Check frontmatter**: Must have valid YAML frontmatter with `description`

### Command Not Working as Expected?

**Check tool usage**: Ensure tools are used correctly (Read before Edit, etc.)

**Check file paths**: Use absolute paths, not relative

**Check error handling**: Add validation for edge cases

### User Confused by Command?

**Add clearer descriptions**: Explain what each step does

**Add examples**: Show example inputs and outputs

**Improve confirmation**: Better summary of what was accomplished

## Advanced Topics

### Conditional Logic
Use IF/ELSE for different user scenarios:

```markdown
## Step 2: Route Based on Type

If type is "prompt":
  - Do X
  - Format as Y

If type is "learning":
  - Do A
  - Format as B
```

### Cross-Command Integration
Commands can suggest related commands:

```markdown
Next steps:
- /idea-work {id} - Work on this idea
- /idea-list - View all ideas
```

### State Management
Commands can read/write state files for persistence:

```markdown
## Step 3: Update Index

Read `ideas/index.json`
Update stats and categories
Write updated index
```

## Related Documentation

- **Production Commands**: See `.claude/commands/` for working examples
- **Tool Documentation**: See Claude documentation for tool usage
- **Workflows**: See `knowledge/patterns/` for workflow patterns

---

**Navigation**: [← Templates](./../README.md)
