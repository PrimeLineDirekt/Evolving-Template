---
description: {BRIEF_DESCRIPTION_OF_COMMAND}
argument-hint: [optional: {ARGUMENT_DESCRIPTION}]
template_version: "1.0"
template_type: command
template_name: "Workflow Command"
use_cases: [user-workflow, data-capture, multi-step-process]
complexity: low
created: 2024-11-26
---

You are my {ROLE_DESCRIPTION}. Your task is to {PRIMARY_TASK_DESCRIPTION}.

## Step 1: {INPUT_GATHERING_STEP}

If the user provided an argument ($ARGUMENTS is not empty), use that as {INPUT_NAME}.

If $ARGUMENTS is empty, ask:
"{PROMPT_FOR_USER_INPUT}"

### Input Validation:
- Check if input meets {CRITERIA_1}
- Validate {CRITERIA_2}
- Ensure {CRITERIA_3}

## Step 2: {ANALYSIS_OR_PROCESSING_STEP}

Analyze the input and determine:

### A) {ANALYSIS_DIMENSION_1}
{DESCRIPTION_OF_WHAT_TO_ANALYZE}

Examples:
- {EXAMPLE_1}
- {EXAMPLE_2}
- {EXAMPLE_3}

Check existing data in `{DATA_SOURCE}` for similar items. If found, use existing categories/patterns. If not, suggest new ones.

### B) {ANALYSIS_DIMENSION_2}
{DESCRIPTION_OF_SCORING_OR_EVALUATION}

Evaluate based on:
- **{CRITERION_1}**: {DESCRIPTION}
- **{CRITERION_2}**: {DESCRIPTION}
- **{CRITERION_3}**: {DESCRIPTION}

Provide a score and rationale.

### C) {ANALYSIS_DIMENSION_3}
{DESCRIPTION_OF_CLASSIFICATION}

Options: `{OPTION_1}`, `{OPTION_2}`, `{OPTION_3}`

### D) {ANALYSIS_DIMENSION_4}
{DESCRIPTION_OF_CONNECTIONS}

Search `{RELATED_DATA_SOURCE}` for connections.
List related items and explain relationships.

## Step 3: {METADATA_GENERATION_STEP}

Generate:
- **{METADATA_1}**: {HOW_TO_GENERATE}
- **{METADATA_2}**: {HOW_TO_GENERATE}
- **{METADATA_3}**: {HOW_TO_GENERATE}

If not explicitly provided, create based on {GENERATION_LOGIC}.

## Step 4: {ID_OR_FILENAME_GENERATION}

Read `{INDEX_FILE}` to get the next ID/sequence number.

Generate: `{ID_FORMAT}` (e.g., `item-2024-001`)

Ensure uniqueness and proper formatting.

## Step 5: {FILE_CREATION_STEP}

Create a new file at `{FILE_PATH}/{CATEGORY}/{ID}.md` with this structure:

```markdown
---
{FRONTMATTER_FIELD_1}: {VALUE}
{FRONTMATTER_FIELD_2}: {VALUE}
{FRONTMATTER_FIELD_3}: {VALUE}
{FRONTMATTER_FIELD_4}: {VALUE}
created: {CURRENT_DATE}
updated: {CURRENT_DATE}
---

# {TITLE}

## {SECTION_1}

{CONTENT_FROM_USER_INPUT}

## {SECTION_2}

{ANALYSIS_RESULTS}

## {SECTION_3}

{RELATED_ITEMS_OR_CONNECTIONS}

## {SECTION_4}

- [ ] {NEXT_STEP_1}
- [ ] {NEXT_STEP_2}
- [ ] {NEXT_STEP_3}

## {SECTION_5}

_To be filled as work progresses_
```

**Important**: Create the category directory if it doesn't exist.

## Step 6: {INDEX_UPDATE_STEP}

Read `{INDEX_FILE}` and update:
- Add new item to `{ARRAY_NAME}`
- Increment `{COUNTER_NAME}`
- Update `stats.{STAT_NAME}`
- Add category to `categories` if new

Ensure JSON validity.

## Step 7: {CROSS_REFERENCE_STEP}

If connections to existing items were found:
- Update those items to reference this new item
- Maintain bidirectional links
- Keep `related_{TYPE}` arrays synchronized

## Step 8: {CONFIRMATION_STEP}

Show the user:

```
✓ {ITEM_TYPE} created: {TITLE}
  ID: {ID}
  {KEY_METRIC_1}: {VALUE}
  {KEY_METRIC_2}: {VALUE}

{BRIEF_SUMMARY_OF_ANALYSIS}

Next steps:
- /{RELATED_COMMAND_1} {ID} - {DESCRIPTION}
- /{RELATED_COMMAND_2} - {DESCRIPTION}
```

---

## Tool Usage Guidelines

**Required Tools**:
- `Read`: Read existing files and indices
- `Write`: Create new files
- `Edit`: Update existing files (for cross-references)
- `Grep/Glob`: Search for related items (if needed)

**Tool Usage Pattern**:
```
1. Read index/related files
2. Analyze and generate metadata
3. Write new file
4. Edit index file
5. Edit related files (cross-references)
```

---

## Error Handling

### Missing Input
```
IF no_input_provided AND no_arguments:
  Prompt user with clear question
  Wait for response
  Validate before proceeding
```

### Invalid Data
```
IF input_invalid:
  Explain what's wrong
  Ask for correction
  Retry validation
```

### File Conflicts
```
IF file_already_exists:
  Check if it's truly a duplicate
  If duplicate: Inform user
  If not: Generate unique ID/filename
```

---

## Validation Checklist

Before confirming completion:
- [ ] All required fields populated
- [ ] File created in correct location
- [ ] Index updated correctly
- [ ] Cross-references created (if applicable)
- [ ] Category directory exists
- [ ] JSON is valid (if updating JSON)
- [ ] User receives clear confirmation

---

## Important Notes

**Best Practices**:
- Always read before writing/editing
- Create directories before files
- Validate JSON after updates
- Keep cross-references bidirectional
- Use absolute paths, not relative

**Common Pitfalls**:
- Forgetting to create category directory
- Not incrementing counters in index
- Breaking JSON with invalid syntax
- Missing cross-references
- Unclear confirmation messages

**Related Commands**:
- `/{RELATED_COMMAND_1}` - {DESCRIPTION}
- `/{RELATED_COMMAND_2}` - {DESCRIPTION}

---

**Template Customization Notes**:
- Replace all `{PLACEHOLDERS}` with actual values
- Customize frontmatter fields for your data model
- Adjust analysis dimensions for your use case
- Define validation criteria specific to your domain
- Configure cross-reference logic based on relationships
