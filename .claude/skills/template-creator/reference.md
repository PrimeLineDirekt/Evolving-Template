# Template Creator - Reference Documentation

Complete reference for all template types, placeholders, and advanced usage.

---

## Table of Contents

1. [Template Specifications](#template-specifications)
2. [Complete Placeholder Reference](#complete-placeholder-reference)
3. [Frontmatter Specifications](#frontmatter-specifications)
4. [Template Locations](#template-locations)
5. [Advanced Usage](#advanced-usage)
6. [Troubleshooting](#troubleshooting)

---

## Template Specifications

### Agent Templates

#### specialist-agent.md

**Purpose**: Domain expert with specialized knowledge and analytical capabilities.

**Structure**:
```markdown
---
template_version: "1.0"
template_type: agent
template_name: "Specialist Agent"
---

# {DOMAIN} Specialist Agent

## Agent Role & Expertise
## Input Processing
## Analysis Framework
## Output Format
## Tool Usage
## Error Handling
## Success Criteria
## Related Agents
```

**Required Placeholders**:
- `{DOMAIN}`: Domain name (e.g., "SEO", "Legal", "Finance")
- `{DESCRIPTION}`: One-line description of expertise
- `{EXPERTISE_AREA_1-5}`: 3-5 specific areas of expertise
- `{INPUT_FIELD_1-4}`: Expected input fields
- `{TOOL_1-3}`: Tools the agent needs

**Optional Placeholders**:
- `{CRITERION_X}`: Assessment criteria
- `{METRIC_X}`: Measurement metrics
- `{RISK_X}`: Risk categories

**Output Location**: `.claude/agents/{domain}-agent.md`

---

#### research-agent.md

**Purpose**: Multi-source research with confidence scoring and validation.

**Structure**:
```markdown
---
template_version: "1.0"
template_type: agent
template_name: "Research Agent"
---

# {DOMAIN} Research Agent

## Agent Role & Expertise
## Input Processing
## Research Framework
## Output Format
## Tool Usage
## Validation Rules
## Error Handling
## Success Criteria
```

**Required Placeholders**:
- `{DOMAIN}`: Research domain (e.g., "Market", "Technical", "Competitive")
- `{RESEARCH_DOMAIN_1-3}`: Specific research areas
- `{TOPIC}`: Research topic/query

**Optional Placeholders**:
- `{DEPTH}`: Research depth (surface|standard|deep)
- `{FINDING_X}`: Key findings
- `{SOURCE_X}`: Information sources

**Output Location**: `.claude/agents/{domain}-research-agent.md`

---

### Command Templates

#### workflow-command.md

**Purpose**: Multi-step workflow for data capture and file creation.

**Structure**:
```markdown
---
description: {BRIEF_DESCRIPTION}
argument-hint: [optional: {ARGUMENT_DESCRIPTION}]
template_version: "1.0"
template_type: command
---

You are my {ROLE_DESCRIPTION}.

## Step 1: {INPUT_GATHERING_STEP}
## Step 2: {ANALYSIS_OR_PROCESSING_STEP}
## Step 3: {METADATA_GENERATION_STEP}
## Step 4: {ID_OR_FILENAME_GENERATION}
## Step 5: {FILE_CREATION_STEP}
## Step 6: {INDEX_UPDATE_STEP}
## Step 7: {CROSS_REFERENCE_STEP}
## Step 8: {CONFIRMATION_STEP}

## Tool Usage Guidelines
## Error Handling
## Validation Checklist
```

**Required Placeholders**:
- `{BRIEF_DESCRIPTION}`: Short command description
- `{ARGUMENT_DESCRIPTION}`: What argument command accepts
- `{ROLE_DESCRIPTION}`: Agent role for this command
- `{PRIMARY_TASK_DESCRIPTION}`: What the command does
- `{INPUT_NAME}`: Name of primary input
- `{DATA_SOURCE}`: Where data is stored
- `{FILE_PATH}`: Output directory
- `{INDEX_FILE}`: Index file to update

**Step-Specific Placeholders**:
- `{INPUT_GATHERING_STEP}`: Name of input step
- `{ANALYSIS_DIMENSION_1-4}`: Analysis aspects
- `{METADATA_1-3}`: Metadata fields to generate
- `{ID_FORMAT}`: ID generation pattern
- `{FRONTMATTER_FIELD_X}`: Frontmatter fields

**Output Location**: `.claude/commands/{name}.md`

---

#### analysis-command.md

**Purpose**: Data analysis, metrics calculation, and insights generation.

**Structure**:
```markdown
---
description: {BRIEF_DESCRIPTION_OF_ANALYSIS}
argument-hint: [optional: {FILTER_OR_SCOPE}]
template_version: "1.0"
template_type: command
---

You are my {DOMAIN} Analyst.

## Step 1: {SCOPE_DEFINITION_STEP}
## Step 2: {DATA_COLLECTION_STEP}
## Step 3: {METRICS_CALCULATION_STEP}
## Step 4: {PATTERN_IDENTIFICATION_STEP}
## Step 5: {ANALYSIS_SYNTHESIS_STEP}
## Step 6: {RECOMMENDATIONS_GENERATION_STEP}
## Step 7: {REPORT_GENERATION_STEP}
## Step 8: {OUTPUT_DELIVERY_STEP}

## Tool Usage
## Error Handling
## Validation Checklist
```

**Required Placeholders**:
- `{DOMAIN}`: Analysis domain
- `{DATA_SOURCE}`: Primary data source
- `{DEFAULT_SCOPE}`: Default analysis scope
- `{METRIC_1-3}`: Key metrics to calculate
- `{ANALYSIS_TYPE}`: Type of analysis

**Optional Placeholders**:
- `{PATTERN_X}`: Patterns to detect
- `{INSIGHT_X}`: Expected insights
- `{RECOMMENDATION_X}`: Recommendations to generate

**Output Location**: `.claude/commands/{name}.md`

---

### Hook Templates

#### post-tool-use.sh

**Purpose**: Event-driven automation triggered after tool usage.

**Structure**:
```bash
#!/bin/bash
# Template metadata in comments

# Configuration
# Helper Functions
# Processing Functions
# Automation Logic
# Main Processing Logic
# Execution
```

**Required Placeholders**:
- `{PATH_PATTERN_1-2}`: Paths to monitor
- `{CUSTOM_WRITE_LOGIC}`: Write event handling
- `{CUSTOM_EDIT_LOGIC}`: Edit event handling
- `{CROSS_REFERENCE_LOGIC}`: Cross-reference logic
- `{INDEX_UPDATE_LOGIC}`: Index update logic

**Configuration Options**:
- `MONITORED_TOOLS`: Array of tools to process
- `MONITORED_PATHS`: Array of path patterns
- `LOG_FILE`: Log file location
- `DEBUG`: Debug mode flag

**Output Location**: `.claude/hooks/{name}.sh`
**Permissions**: Must be executable (`chmod +x`)

---

#### stop-hook.sh

**Purpose**: Session summary generation on conversation end.

**Structure**:
```bash
#!/bin/bash
# Template metadata in comments

# Configuration
# Helper Functions
# Summary Generation
# Main Logic
# Execution
```

**Required Placeholders**:
- `{SUMMARY_OUTPUT_PATH}`: Where to save summaries
- `{markdown|json|text}`: Summary format
- `{SESSION_DESCRIPTION}`: Session overview
- `{CUSTOM_TOPIC_DETECTION}`: Topic identification logic

**Configuration Options**:
- `SUMMARY_DIR`: Output directory
- `SUMMARY_FORMAT`: Output format
- `INCLUDE_TIMESTAMP`: Include timestamps
- `INCLUDE_TOOLS_USED`: Track tool usage
- `INCLUDE_FILES_MODIFIED`: Track file modifications
- `INCLUDE_TOPICS`: Identify session topics

**Output Location**: `.claude/hooks/{name}.sh`
**Permissions**: Must be executable (`chmod +x`)

---

### Skill Templates

#### simple-skill/SKILL.md

**Purpose**: Single-file skill for straightforward use cases.

**Structure**:
```markdown
---
template_version: "1.0"
template_type: skill
template_name: "Simple Skill"
---

# {SKILL_NAME}

## Purpose
## Core Principles
## Guidelines
## Workflow
## Examples
## Common Patterns
## Best Practices
## Quick Reference
## Troubleshooting
## Checklist
## Related Skills
```

**Required Placeholders**:
- `{SKILL_NAME}`: Skill name
- `{BRIEF_DESCRIPTION_OF_SKILL_PURPOSE}`: One-line purpose
- `{USE_CASE_1-3}`: Primary use cases
- `{PRINCIPLE_1-3}`: Core principles
- `{GUIDELINE_CATEGORY_1-2}`: Guideline categories

**Optional Placeholders**:
- `{PATTERN_X}`: Common patterns
- `{PRACTICE_X}`: Best practices
- `{ANTI_PATTERN_X}`: Anti-patterns

**Output Location**: `.claude/skills/{name}/SKILL.md`

---

#### progressive-skill/

**Purpose**: Three-file skill structure with progressive disclosure.

**Files**:
1. `SKILL.md`: Entry point (<500 lines)
2. `reference.md`: Detailed documentation
3. `examples.md`: Practical examples

**SKILL.md Placeholders**:
- `{SKILL_NAME}`: Skill name
- `{BRIEF_PURPOSE}`: Short purpose statement
- `{TRIGGER_PATTERN_X}`: Auto-detection patterns
- `{QUICK_START_STEP_X}`: Quick start steps

**reference.md Placeholders**:
- `{DETAILED_SECTION_X}`: Detailed sections
- `{SPECIFICATION_X}`: Technical specifications
- `{ADVANCED_TOPIC_X}`: Advanced topics

**examples.md Placeholders**:
- `{EXAMPLE_SCENARIO_X}`: Example scenarios
- `{STEP_BY_STEP_X}`: Walkthroughs

**Output Location**: `.claude/skills/{name}/` (directory with 3 files)

---

## Complete Placeholder Reference

### Universal Placeholders

| Placeholder | Type | Description | Example |
|------------|------|-------------|---------|
| `{DOMAIN}` | String | Domain/specialization | "SEO", "Legal" |
| `{DESCRIPTION}` | String | Brief description | "Search engine optimization expert" |
| `{TIMESTAMP}` | Date | Current date | "2024-11-26" |
| `{VERSION}` | String | Version number | "1.0" |
| `{PROJECT_NAME}` | String | Project/command name | "idea-tracker" |

### Agent-Specific Placeholders

| Placeholder | Type | Description | Required |
|------------|------|-------------|----------|
| `{EXPERTISE_AREA_X}` | String | Area of expertise | Yes (3-5) |
| `{INPUT_FIELD_X}` | String | Expected input field | Yes (2-4) |
| `{TOOL_X}` | String | Tool name | Yes (1-3) |
| `{CRITERION_X}` | String | Assessment criterion | Optional |
| `{METRIC_X}` | String | Measurement metric | Optional |
| `{RISK_X}` | String | Risk category | Optional |
| `{RESEARCH_DOMAIN_X}` | String | Research area | Research agents |
| `{FINDING_X}` | String | Key finding | Research agents |

### Command-Specific Placeholders

| Placeholder | Type | Description | Required |
|------------|------|-------------|----------|
| `{BRIEF_DESCRIPTION}` | String | Command description | Yes |
| `{ARGUMENT_DESCRIPTION}` | String | Argument hint | Yes |
| `{ROLE_DESCRIPTION}` | String | Agent role | Yes |
| `{PRIMARY_TASK_DESCRIPTION}` | String | Main task | Yes |
| `{INPUT_NAME}` | String | Input field name | Yes |
| `{DATA_SOURCE}` | Path | Data location | Yes |
| `{FILE_PATH}` | Path | Output directory | Yes |
| `{INDEX_FILE}` | Path | Index file path | Yes |
| `{STEP_NAME}` | String | Workflow step name | Yes (per step) |
| `{ANALYSIS_DIMENSION_X}` | String | Analysis aspect | Workflow (2-4) |
| `{METADATA_X}` | String | Metadata field | Workflow (1-3) |
| `{ID_FORMAT}` | String | ID pattern | Workflow |
| `{FRONTMATTER_FIELD_X}` | String | Frontmatter field | Workflow |
| `{DEFAULT_SCOPE}` | String | Default scope | Analysis |
| `{METRIC_X}` | String | Metric to calculate | Analysis (1-3) |

### Hook-Specific Placeholders

| Placeholder | Type | Description | Required |
|------------|------|-------------|----------|
| `{PATH_PATTERN_X}` | String | Path to monitor | Yes (1-2) |
| `{CUSTOM_WRITE_LOGIC}` | Code | Write handler | Optional |
| `{CUSTOM_EDIT_LOGIC}` | Code | Edit handler | Optional |
| `{CROSS_REFERENCE_LOGIC}` | Code | Cross-ref logic | Optional |
| `{INDEX_UPDATE_LOGIC}` | Code | Index update | Optional |
| `{SUMMARY_OUTPUT_PATH}` | Path | Summary directory | Stop hook |
| `{SESSION_DESCRIPTION}` | String | Session overview | Stop hook |
| `{CUSTOM_TOPIC_DETECTION}` | Code | Topic detection | Stop hook |

### Skill-Specific Placeholders

| Placeholder | Type | Description | Required |
|------------|------|-------------|----------|
| `{SKILL_NAME}` | String | Skill name | Yes |
| `{BRIEF_DESCRIPTION_OF_SKILL_PURPOSE}` | String | Purpose | Yes |
| `{USE_CASE_X}` | String | Use case | Yes (2-3) |
| `{PRINCIPLE_X}` | String | Core principle | Yes (2-3) |
| `{GUIDELINE_CATEGORY_X}` | String | Guideline category | Yes (1-2) |
| `{PATTERN_X}` | String | Common pattern | Optional |
| `{PRACTICE_X}` | String | Best practice | Optional |
| `{ANTI_PATTERN_X}` | String | Anti-pattern | Optional |
| `{TRIGGER_PATTERN_X}` | String | Auto-detection pattern | Progressive |

---

## Frontmatter Specifications

### Agent Frontmatter

```yaml
---
template_version: "1.0"
template_type: agent
template_name: "{Template Name}"
description: "{Brief description}"
use_cases: [use-case-1, use-case-2]
complexity: {low|medium|medium-high|high}
created: YYYY-MM-DD
---
```

### Command Frontmatter

```yaml
---
description: {Brief command description}
argument-hint: [optional: {argument description}]
template_version: "1.0"
template_type: command
template_name: "{Template Name}"
use_cases: [use-case-1, use-case-2]
complexity: {low|medium|high}
created: YYYY-MM-DD
---
```

### Hook Frontmatter (in comments)

```bash
# ---
# template_version: "1.0"
# template_type: hook
# template_name: "{Template Name}"
# description: "{Brief description}"
# use_cases: [use-case-1, use-case-2]
# complexity: {low|medium|high}
# created: YYYY-MM-DD
# ---
```

### Skill Frontmatter

```yaml
---
name: {skill-name}
description: "{Brief description with auto-detection hints}"
allowed-tools: Tool1, Tool2, Tool3
template_version: "1.0"
template_type: skill
template_name: "{Template Name}"
use_cases: [use-case-1, use-case-2]
complexity: {low|medium|high}
created: YYYY-MM-DD
---
```

---

## Template Locations

### Directory Structure

```
.claude/
├── templates/
│   ├── agents/
│   │   ├── specialist-agent.md
│   │   └── research-agent.md
│   ├── commands/
│   │   ├── workflow-command.md
│   │   └── analysis-command.md
│   ├── hooks/
│   │   ├── post-tool-use.sh
│   │   └── stop-hook.sh
│   └── skills/
│       ├── simple-skill/
│       │   └── SKILL.md
│       └── progressive-skill/
│           ├── SKILL.md
│           ├── reference.md
│           └── examples.md
```

### Output Locations

```
.claude/
├── agents/
│   └── {domain}-agent.md
├── commands/
│   └── {name}.md
├── hooks/
│   └── {name}.sh
└── skills/
    └── {name}/
        ├── SKILL.md
        ├── reference.md (optional)
        └── examples.md (optional)
```

---

## Advanced Usage

### Combining Templates

For complex workflows, combine multiple templates:

**Example**: Research + Analysis workflow
1. Create research agent for data collection
2. Create analysis command for insights
3. Create hook for auto-triggering analysis after research

### Custom Placeholder Logic

For domain-specific placeholders:

```python
def generate_custom_placeholder(domain, placeholder_name):
    if placeholder_name == "EXPERTISE_AREA_1":
        # Generate based on domain
        expertise_map = {
            "SEO": ["On-page SEO", "Technical SEO", "Content Strategy"],
            "Legal": ["Contract Law", "IP Rights", "Compliance"],
            "Finance": ["Financial Analysis", "Risk Assessment", "Forecasting"]
        }
        return expertise_map.get(domain, ["General Expertise"])

    # Add more custom logic as needed
```

### Template Inheritance

Create specialized templates by extending base templates:

1. Start with base template
2. Add domain-specific sections
3. Override default placeholders
4. Save as new template variant

### Batch Creation

Create multiple related components:

```
User: "Create an SEO system"

Process:
1. Create seo-specialist-agent.md
2. Create seo-analysis-command.md
3. Create seo-report-hook.sh
4. Cross-reference all components
```

---

## Troubleshooting

### Issue: Placeholder Not Replaced

**Symptom**: Output contains `{PLACEHOLDER_NAME}`

**Causes**:
1. Typo in placeholder name
2. Missing from replacement logic
3. Conditional placeholder not triggered

**Solution**:
1. Verify placeholder name matches template exactly
2. Add to replacement mapping
3. Check conditional logic

---

### Issue: Invalid Frontmatter

**Symptom**: YAML parsing error

**Causes**:
1. Unquoted special characters
2. Incorrect indentation
3. Missing closing `---`

**Solution**:
1. Quote strings with special characters
2. Use 2-space indentation
3. Verify frontmatter structure

---

### Issue: File Permission Error (Hooks)

**Symptom**: Hook not executing

**Causes**:
1. Missing execute permissions
2. Wrong shebang line
3. Path issues

**Solution**:
```bash
chmod +x .claude/hooks/{name}.sh
# Verify shebang
head -1 .claude/hooks/{name}.sh  # Should be #!/bin/bash
```

---

### Issue: Template Not Found

**Symptom**: Read tool fails

**Causes**:
1. Wrong template path
2. Template doesn't exist
3. Typo in filename

**Solution**:
1. List available templates:
```bash
ls -la .claude/templates/**/*
```
2. Verify path matches expected location
3. Check for typos

---

### Issue: Duplicate Component

**Symptom**: File already exists error

**Causes**:
1. Component with same name exists
2. User forgot existing component

**Solution**:
1. List existing components
2. Ask user to rename or overwrite
3. If overwrite, backup original first

---

## Validation Rules

### Pre-Creation Validation

```python
def validate_before_creation(template_type, placeholders, output_path):
    errors = []

    # 1. Check all required placeholders provided
    required = get_required_placeholders(template_type)
    for req in required:
        if req not in placeholders:
            errors.append(f"Missing required placeholder: {req}")

    # 2. Validate placeholder values
    for key, value in placeholders.items():
        if not validate_value(key, value):
            errors.append(f"Invalid value for {key}: {value}")

    # 3. Check output path
    if file_exists(output_path):
        errors.append(f"File already exists: {output_path}")

    # 4. Verify parent directory exists
    if not dir_exists(parent_dir(output_path)):
        errors.append(f"Parent directory missing: {parent_dir(output_path)}")

    return errors
```

### Post-Creation Validation

```python
def validate_after_creation(file_path, template_type):
    checks = []

    # 1. File exists
    checks.append(("File created", file_exists(file_path)))

    # 2. No placeholders remain
    content = read_file(file_path)
    remaining = find_placeholders(content)
    checks.append(("All placeholders replaced", len(remaining) == 0))

    # 3. Valid frontmatter (if applicable)
    if has_frontmatter(template_type):
        checks.append(("Valid frontmatter", validate_frontmatter(file_path)))

    # 4. Executable (for hooks)
    if template_type == "hook":
        checks.append(("Executable", is_executable(file_path)))

    return checks
```

---

## Version History

**v1.0** (2024-11-26)
- Initial release
- 6 template types
- Complete placeholder system
- Progressive disclosure support

---

**Last Updated**: 2024-11-26
**Maintained by**: Meta-Agent System
