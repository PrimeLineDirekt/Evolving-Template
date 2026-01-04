# Anthropic Skill Best Practices Reference

**Type**: Official Documentation
**Extracted**: 2025-12-30

---

## Core Principles

### 1. Concise is Key

> "The context window is a public good."

- Only add context Claude doesn't already have
- Default assumption: Claude is already very smart
- Challenge each piece: "Does Claude really need this?"

### 2. Degrees of Freedom

| Level | Use When | Example |
|-------|----------|---------|
| **High** | Multiple approaches valid | Code review process |
| **Medium** | Preferred pattern exists | Report templates |
| **Low** | Operations are fragile | Database migrations |

**Analogy:**
- Narrow bridge with cliffs → Low freedom (exact instructions)
- Open field → High freedom (general direction)

### 3. Test with All Models

| Model | Consideration |
|-------|--------------|
| **Haiku** | Does Skill provide enough guidance? |
| **Sonnet** | Is Skill clear and efficient? |
| **Opus** | Does Skill avoid over-explaining? |

---

## YAML Frontmatter Requirements

```yaml
---
name: skill-name
description: What it does and when to use it
---
```

**Name:**
- Max 64 characters
- Lowercase letters, numbers, hyphens only
- No XML tags
- No reserved words: "anthropic", "claude"

**Description:**
- Max 1024 characters
- Non-empty
- No XML tags
- **ALWAYS third person** (not "I can help you...")

---

## Naming Conventions

**Recommended: Gerund form (verb + -ing)**
- `processing-pdfs`
- `analyzing-spreadsheets`
- `managing-databases`

**Avoid:**
- Vague: `helper`, `utils`, `tools`
- Generic: `documents`, `data`, `files`

---

## Description Best Practices

**Include both WHAT and WHEN:**

```yaml
# Good
description: Extract text and tables from PDF files. Use when working with PDF files or when user mentions document extraction.

# Bad
description: Helps with documents
```

**Always third person:**
- Good: "Processes Excel files and generates reports"
- Bad: "I can help you process Excel files"

---

## Progressive Disclosure Patterns

### Pattern 1: High-level guide with references

```markdown
# PDF Processing

## Quick start
[Basic example]

## Advanced features
**Form filling**: See [FORMS.md](FORMS.md)
**API reference**: See [REFERENCE.md](REFERENCE.md)
```

### Pattern 2: Domain-specific organization

```
bigquery-skill/
├── SKILL.md
└── reference/
    ├── finance.md
    ├── sales.md
    └── product.md
```

### Pattern 3: Conditional details

```markdown
## Basic content here

**For tracked changes**: See [REDLINING.md](REDLINING.md)
```

---

## Critical Rules

### Keep References One Level Deep

```
BAD (too deep):
SKILL.md → advanced.md → details.md

GOOD (one level):
SKILL.md → advanced.md
SKILL.md → reference.md
SKILL.md → examples.md
```

### SKILL.md Size Limit

- Keep body under **500 lines**
- If exceeding, split into separate files

### Structure Long Files with TOC

For reference files > 100 lines:
```markdown
# API Reference

## Contents
- Authentication and setup
- Core methods
- Advanced features
- Error handling
```

---

## Workflow Patterns

### Checklist Pattern

```markdown
Copy this checklist and track progress:

```
- [ ] Step 1: Read documents
- [ ] Step 2: Identify themes
- [ ] Step 3: Cross-reference
- [ ] Step 4: Create summary
```
```

### Feedback Loop Pattern

```
1. Make edits
2. Validate immediately
3. If fails → Fix → Validate again
4. Only proceed when validation passes
```

---

## Evaluation-Driven Development

**Create evaluations BEFORE writing documentation!**

1. Identify gaps (run without Skill)
2. Create 3+ test scenarios
3. Establish baseline
4. Write minimal instructions
5. Iterate

### Evaluation Structure

```json
{
  "skills": ["pdf-processing"],
  "query": "Extract text from PDF",
  "files": ["test.pdf"],
  "expected_behavior": [
    "Successfully reads PDF",
    "Extracts text from all pages",
    "Saves to output.txt"
  ]
}
```

---

## Iterative Development with Claude

**Two-Claude Pattern:**
- **Claude A**: Author (helps design Skill)
- **Claude B**: User (tests Skill in real tasks)

**Process:**
1. Complete task with Claude A (normal prompting)
2. Identify reusable pattern
3. Ask Claude A to create Skill
4. Review for conciseness
5. Test with Claude B on similar tasks
6. Iterate based on observation

---

## Anti-Patterns

| Anti-Pattern | Fix |
|--------------|-----|
| Windows paths (`\`) | Use forward slashes (`/`) |
| Too many options | Provide sensible default |
| Magic constants | Document why each value |
| Time-sensitive info | Use "old patterns" section |
| Inconsistent terminology | Choose one term, use everywhere |
| Deeply nested references | Keep one level deep |
| Vague names | Use descriptive names |

---

## Advanced: Executable Code

### Solve, Don't Punt

```python
# GOOD: Handle errors explicitly
def process_file(path):
    try:
        with open(path) as f:
            return f.read()
    except FileNotFoundError:
        print(f"Creating {path}")
        with open(path, 'w') as f:
            f.write('')
        return ''

# BAD: Let it fail
def process_file(path):
    return open(path).read()
```

### Document Constants

```python
# GOOD: Self-documenting
REQUEST_TIMEOUT = 30  # HTTP requests typically complete within 30s

# BAD: Magic number
TIMEOUT = 47  # Why 47?
```

### Plan-Validate-Execute Pattern

For complex/batch operations:

```
1. Analyze
2. Create plan file (changes.json)
3. Validate plan (script)
4. Execute
5. Verify
```

### MCP Tool References

Always use fully qualified names:
```markdown
Use the BigQuery:bigquery_schema tool...
Use the GitHub:create_issue tool...
```

---

## Checklist

### Core Quality
- [ ] Description includes WHAT + WHEN
- [ ] SKILL.md under 500 lines
- [ ] References one level deep
- [ ] No time-sensitive info
- [ ] Consistent terminology
- [ ] Concrete examples
- [ ] Workflows have clear steps

### Code
- [ ] Scripts solve, don't punt
- [ ] Explicit error handling
- [ ] No magic constants
- [ ] Packages listed and verified
- [ ] No Windows-style paths
- [ ] Validation for critical ops

### Testing
- [ ] 3+ evaluations created
- [ ] Tested with Haiku, Sonnet, Opus
- [ ] Tested with real scenarios

---

**Official Source**: platform.claude.com/docs
