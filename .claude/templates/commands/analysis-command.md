---
description: {BRIEF_DESCRIPTION_OF_ANALYSIS}
argument-hint: [optional: {FILTER_OR_SCOPE}]
template_version: "1.0"
template_type: command
template_name: "Analysis Command"
use_cases: [data-analysis, reporting, insights-generation]
complexity: medium
created: 2024-11-26
---

You are my {DOMAIN} Analyst. Your task is to analyze {DATA_SOURCE} and generate actionable insights.

## Step 1: {SCOPE_DEFINITION_STEP}

Determine analysis scope:

If $ARGUMENTS provided:
- Parse filter/scope from arguments
- Example: `/analyze {SCOPE}` where scope could be category, date range, or specific item

If no arguments:
- Default to {DEFAULT_SCOPE}
- Or ask: "What would you like to analyze? Options: {OPTION_1}, {OPTION_2}, {OPTION_3}"

### Scope Parameters:
- **Time Range**: {DEFAULT_OR_SPECIFIED}
- **Category**: {DEFAULT_OR_SPECIFIED}
- **Filters**: {ANY_ADDITIONAL_FILTERS}

## Step 2: {DATA_COLLECTION_STEP}

Collect data from:

### Primary Sources:
- `{DATA_SOURCE_1}` - {DESCRIPTION}
- `{DATA_SOURCE_2}` - {DESCRIPTION}
- `{DATA_SOURCE_3}` - {DESCRIPTION}

### Collection Strategy:
```python
data = {
    "{CATEGORY_1}": [],
    "{CATEGORY_2}": [],
    "{CATEGORY_3}": []
}

# Read index or directory
items = read_items_from("{DATA_SOURCE}")

# Apply filters
filtered = apply_scope_filter(items, scope)

# Categorize
for item in filtered:
    category = determine_category(item)
    data[category].append(item)

return data
```

### Data Validation:
- Check for completeness
- Identify missing or corrupted data
- Log data quality issues

## Step 3: {METRICS_CALCULATION_STEP}

Calculate key metrics:

### Quantitative Metrics:
- **{METRIC_1}**: {CALCULATION_FORMULA}
- **{METRIC_2}**: {CALCULATION_FORMULA}
- **{METRIC_3}**: {CALCULATION_FORMULA}

Example calculation:
```python
{METRIC_NAME} = {FORMULA}
```

### Qualitative Assessments:
- **{ASSESSMENT_1}**: {CRITERIA}
- **{ASSESSMENT_2}**: {CRITERIA}

### Trend Analysis (if temporal data):
- Compare current vs. previous period
- Calculate growth/decline rates
- Identify trend direction

## Step 4: {PATTERN_IDENTIFICATION_STEP}

Identify patterns and insights:

### Pattern Detection:
```python
patterns = {
    "clusters": identify_clusters(data),
    "correlations": find_correlations(data),
    "anomalies": detect_anomalies(data),
    "trends": analyze_trends(data)
}
```

### Insight Generation:
For each pattern:
1. Describe the pattern
2. Explain significance
3. Suggest implications
4. Recommend actions

### Examples:
- **High-performing items**: Items with {CRITERIA}
- **Underutilized items**: Items with {CRITERIA}
- **Emerging patterns**: {DESCRIPTION}

## Step 5: {ANALYSIS_SYNTHESIS_STEP}

Synthesize findings:

### Top Insights:
Identify 3-5 most important insights:
1. {INSIGHT_TYPE} - {DESCRIPTION}
2. {INSIGHT_TYPE} - {DESCRIPTION}
3. {INSIGHT_TYPE} - {DESCRIPTION}

### Cross-Category Analysis:
- Connections between {CATEGORY_1} and {CATEGORY_2}
- Synergies and conflicts
- Optimization opportunities

### Gap Analysis:
- What's missing from the data
- Underrepresented areas
- Opportunities for expansion

## Step 6: {RECOMMENDATIONS_GENERATION_STEP}

Generate actionable recommendations:

### Immediate Actions (High Priority):
1. **{ACTION_1}**
   - **Rationale**: {WHY}
   - **Impact**: {EXPECTED_BENEFIT}
   - **Effort**: {LOW|MEDIUM|HIGH}

2. **{ACTION_2}**
   - **Rationale**: {WHY}
   - **Impact**: {EXPECTED_BENEFIT}
   - **Effort**: {LOW|MEDIUM|HIGH}

### Short-term Optimizations:
- {RECOMMENDATION_1}
- {RECOMMENDATION_2}

### Long-term Strategic:
- {RECOMMENDATION_3}
- {RECOMMENDATION_4}

## Step 7: {REPORT_GENERATION_STEP}

Generate comprehensive report:

```markdown
# {ANALYSIS_TYPE} Analysis Report

**Generated**: {TIMESTAMP}
**Scope**: {SCOPE_DESCRIPTION}
**Data Sources**: {SOURCES}

## Executive Summary

**Key Finding**: {PRIMARY_INSIGHT}

**Top Metrics**:
- {METRIC_1}: {VALUE}
- {METRIC_2}: {VALUE}
- {METRIC_3}: {VALUE}

**Recommended Action**: {PRIMARY_RECOMMENDATION}

## 1. Overview

### Scope & Methodology:
- **Analysis Period**: {TIME_RANGE}
- **Items Analyzed**: {COUNT}
- **Categories**: {LIST}

### Data Quality:
- Completeness: {PERCENTAGE}%
- Issues Found: {COUNT}

## 2. Quantitative Analysis

### Key Metrics:

| Metric | Value | Change | Trend |
|--------|-------|--------|-------|
| {METRIC_1} | {VALUE} | {CHANGE} | {↑/↓/→} |
| {METRIC_2} | {VALUE} | {CHANGE} | {↑/↓/→} |
| {METRIC_3} | {VALUE} | {CHANGE} | {↑/↓/→} |

### Distribution Analysis:
{DESCRIBE_DATA_DISTRIBUTION}

## 3. Patterns & Insights

### Pattern 1: {PATTERN_NAME}
**Description**: {WHAT_IS_THE_PATTERN}
**Significance**: {WHY_IT_MATTERS}
**Examples**: {SPECIFIC_INSTANCES}
**Recommendation**: {WHAT_TO_DO}

### Pattern 2: {PATTERN_NAME}
{SAME_STRUCTURE}

### Pattern 3: {PATTERN_NAME}
{SAME_STRUCTURE}

## 4. Top Performers

### {CATEGORY_1} Leaders:
1. **{ITEM_1}** - {SCORE} - {REASON}
2. **{ITEM_2}** - {SCORE} - {REASON}
3. **{ITEM_3}** - {SCORE} - {REASON}

### {CATEGORY_2} Standouts:
{SIMILAR_LIST}

## 5. Areas for Improvement

### Underperforming Items:
- {ITEM_1}: {ISSUE_AND_SUGGESTION}
- {ITEM_2}: {ISSUE_AND_SUGGESTION}

### Gaps & Opportunities:
- {GAP_1}: {OPPORTUNITY}
- {GAP_2}: {OPPORTUNITY}

## 6. Cross-Category Insights

### Connections:
- {ITEM_A} ↔ {ITEM_B}: {SYNERGY_DESCRIPTION}
- {ITEM_C} ↔ {ITEM_D}: {SYNERGY_DESCRIPTION}

### Conflicts:
- {CONFLICT_DESCRIPTION_AND_RESOLUTION}

## 7. Recommendations

### High Priority (Immediate):
1. {ACTION_WITH_DETAILS}
2. {ACTION_WITH_DETAILS}

### Medium Priority (Short-term):
- {ACTION}
- {ACTION}

### Low Priority (Long-term):
- {ACTION}
- {ACTION}

## 8. Next Steps

### Immediate Actions:
- [ ] {ACTION_1}
- [ ] {ACTION_2}

### Follow-up Analysis:
- [ ] {FUTURE_ANALYSIS_1}
- [ ] {FUTURE_ANALYSIS_2}

### Monitoring:
- Track {METRIC} monthly
- Review {CATEGORY} quarterly

---

**Analysis Confidence**: {HIGH|MEDIUM|LOW}
**Data Quality**: {SCORE}/10
**Recommendations Priority**: {CRITICAL|HIGH|MEDIUM}
```

## Step 8: {OUTPUT_DELIVERY_STEP}

Present report to user:

### Console Summary:
```
{ANALYSIS_TYPE} Analysis Complete

Key Findings:
✓ {FINDING_1}
✓ {FINDING_2}
✓ {FINDING_3}

Top Recommendations:
→ {RECOMMENDATION_1}
→ {RECOMMENDATION_2}

Full report: {FILE_PATH} (if saved)
```

### Optional: Save Report
Ask user: "Save detailed report to file? (Y/N)"

If yes:
- Create file at `{REPORTS_PATH}/{ANALYSIS_TYPE}-{TIMESTAMP}.md`
- Confirm file location

---

## Tool Usage

**Required Tools**:
- `Read`: Read data sources
- `Grep/Glob`: Search and filter data
- `Write`: Save report (optional)

**Tool Usage Pattern**:
```
1. Glob to find all relevant files
2. Read files and extract data
3. Grep for specific patterns (if needed)
4. Process data in memory
5. Write report (if requested)
```

---

## Error Handling

### No Data Found
```
IF no_data_in_scope:
  Inform user: "No items found matching {SCOPE}"
  Suggest: "Try different scope or check data sources"
  Exit gracefully
```

### Insufficient Data
```
IF data_count < minimum_threshold:
  Warn: "Limited data ({COUNT} items) - analysis may be preliminary"
  Proceed with caveats
  Flag low confidence
```

### Data Quality Issues
```
IF data_quality_problems:
  Log issues in report
  Proceed with available data
  Recommend data cleanup
```

---

## Validation Checklist

Before delivering report:
- [ ] All metrics calculated correctly
- [ ] Patterns identified and explained
- [ ] Recommendations are actionable
- [ ] Data quality assessed
- [ ] Report is well-formatted
- [ ] User receives clear summary

---

## Important Notes

**Best Practices**:
- Start with broad overview, then drill down
- Quantify whenever possible
- Provide context for metrics
- Make recommendations specific and actionable
- Highlight both strengths and weaknesses

**Common Pitfalls**:
- Analysis paralysis - focus on top insights
- Vague recommendations - be specific
- Ignoring data quality issues
- Overwhelming user with too much detail

**Related Commands**:
- `/{DETAIL_COMMAND}` - Drill into specific items
- `/{UPDATE_COMMAND}` - Act on recommendations

---

**Template Customization Notes**:
- Replace `{PLACEHOLDERS}` with domain-specific values
- Define relevant metrics for your data type
- Customize pattern detection for your use case
- Adjust recommendation categories as needed
- Configure report format for your audience
