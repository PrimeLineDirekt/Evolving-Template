# Skill Templates

Skill templates provide structures for building reusable, complex capabilities for Claude.

## What are Skill Templates?

Skills are specialized capabilities that Claude can invoke for complex tasks. They're similar to "super-prompts" with structured knowledge, examples, and reference documentation.

## When to Use Skill Templates

- Building complex, reusable capabilities
- Creating domain-specific expertise modules
- Packaging workflows with extensive documentation
- Progressive disclosure for large knowledge bases

## Available Templates

### 1. Progressive Skill (`progressive-skill/`)

**Use for**: Large, complex skills requiring extensive documentation.

**Structure**:
```
progressive-skill/
├── SKILL.md          # Entry point (<500 lines)
├── reference.md      # Detailed documentation
└── examples.md       # Usage examples
```

**Complexity**: High

**Examples**:
- API integration frameworks
- Complex analysis methodologies
- Multi-step technical processes

**Key Features**:
- Progressive disclosure pattern
- Main entry point stays concise
- Deep reference when needed
- Practical examples

### 2. Simple Skill (`simple-skill/SKILL.md`)

**Use for**: Straightforward, single-file skills.

**Structure**:
```
simple-skill/
└── SKILL.md          # All-in-one file
```

**Complexity**: Low-Medium

**Examples**:
- Code formatting rules
- Writing style guides
- Simple calculation methods

**Key Features**:
- Single-file simplicity
- Quick to create and use
- All content in one place

## Quick Start

### Creating a Progressive Skill

```bash
# 1. Create skill directory
mkdir -p .claude/skills/my-complex-skill

# 2. Copy templates
cp .claude/templates/skills/progressive-skill/* .claude/skills/my-complex-skill/

# 3. Edit SKILL.md (main entry point)
# - Define skill purpose
# - Core concepts
# - Quick reference
# - Link to reference.md and examples.md

# 4. Edit reference.md (detailed docs)
# - Comprehensive documentation
# - Technical details
# - Advanced usage

# 5. Edit examples.md (practical usage)
# - Real-world examples
# - Common scenarios
# - Troubleshooting
```

### Creating a Simple Skill

```bash
# 1. Create skill directory
mkdir -p .claude/skills/my-simple-skill

# 2. Copy template
cp .claude/templates/skills/simple-skill/SKILL.md .claude/skills/my-simple-skill/

# 3. Edit SKILL.md
# - Define skill purpose
# - Provide instructions
# - Add examples
# - Include best practices
```

## Progressive Disclosure Pattern

Large skills use progressive disclosure to manage complexity:

**Level 1 - SKILL.md**: Core concepts and quick start (read first)
↓
**Level 2 - reference.md**: Detailed documentation (when needed)
↓
**Level 3 - examples.md**: Practical examples (for implementation)

Benefits:
- Claude loads minimal content initially
- Deep dive available when needed
- Faster initial response
- Comprehensive when required

## Best Practices

### 1. Keep SKILL.md Under 500 Lines
If main entry exceeds 500 lines, use progressive pattern.

### 2. Structure for Skimming
Use clear headers, bullet points, code blocks for quick scanning.

### 3. Provide Examples
Real examples are more valuable than abstract descriptions.

### 4. Version Your Skills
Track skill versions in frontmatter for maintainability.

### 5. Link References Explicitly
Progressive skills should clearly reference supporting docs:

```markdown
For detailed API documentation, see [reference.md](reference.md)

For integration examples, see [examples.md](examples.md)
```

## Skill Invocation

Skills are invoked with the `Skill` tool:

```
User: "Help me with API integration"
Claude: *invokes Skill tool with skill="api-integration"*
```

Skills automatically expand and provide context to Claude.

## Examples

### Progressive Skill: API Integration

```
api-integration/
├── SKILL.md          # Core concepts, quick start
├── reference.md      # Full API docs, parameters, errors
└── examples.md       # REST, GraphQL, WebSocket examples
```

**SKILL.md** (400 lines):
- What is this skill?
- Core principles
- Quick start guide
- Common patterns
- Links to reference and examples

**reference.md** (1500 lines):
- Complete API specification
- All parameters and options
- Error handling details
- Rate limiting and quotas
- Authentication methods

**examples.md** (800 lines):
- Basic REST example
- Advanced GraphQL example
- WebSocket streaming
- Error handling patterns
- Rate limit management

### Simple Skill: Code Style

```
code-style/
└── SKILL.md          # All style rules in one file
```

**SKILL.md** (300 lines):
- Naming conventions
- Formatting rules
- Comment guidelines
- Best practices
- Examples

## Troubleshooting

### Skill Not Loading?

**Check directory structure**: Progressive skills need SKILL.md as entry point

**Check file names**: Must be exactly `SKILL.md`, `reference.md`, `examples.md`

**Check skill name**: Skill directory name is how it's invoked

### Skill Too Large?

**Split into progressive**: Use progressive-skill pattern

**Extract examples**: Move examples to examples.md

**Link external docs**: Reference external resources instead of duplicating

### Skill Not Useful?

**Add examples**: Abstract skills need practical examples

**Improve structure**: Use clear headers and formatting

**Simplify language**: Be precise, avoid verbosity

## Advanced Topics

### Skill Composition
Skills can reference other skills for modular design.

### Dynamic Skills
Skills can include conditionals for different scenarios.

### Skill Updates
Version skills in frontmatter and track changes.

## Related Documentation

- **Progressive Disclosure Pattern**: See templates for structure
- **Claude Skills**: Official documentation
- **Best Practices**: Writing effective prompts

---

**Navigation**: [← Templates](./../README.md)
