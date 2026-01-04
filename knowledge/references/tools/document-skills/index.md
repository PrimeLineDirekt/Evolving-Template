---
title: "Document Skills Reference"
type: reference
category: skills
domain: [documents, excel, powerpoint, pdf, word]
source: anthropic-cookbook/skills
source_date: 2025-12-13
completeness: complete
tags: [xlsx, pptx, pdf, docx, documents, skills, generation]
---

# Document Skills Reference

Built-in Claude skills for generating Office documents and PDFs.

## TL;DR

Four document skills enable Claude to generate professional documents: **xlsx** (Excel with formulas/charts), **pptx** (PowerPoint presentations), **pdf** (formatted PDFs), **docx** (Word documents). Invoke with `@skill-name` or natural language.

---

## Quick Reference

| Skill | Output | Best For |
|-------|--------|----------|
| [xlsx](#xlsx---excel-generation) | Excel (.xlsx) | Data, calculations, charts |
| [pptx](#pptx---powerpoint-generation) | PowerPoint (.pptx) | Presentations, slides |
| [pdf](#pdf---pdf-generation) | PDF (.pdf) | Reports, formatted docs |
| [docx](#docx---word-generation) | Word (.docx) | Long-form documents |

---

## xlsx - Excel Generation

**Invocation**: `@xlsx` or "create an Excel spreadsheet"

### Capabilities

- Create workbooks with multiple sheets
- Add formulas and functions
- Generate charts (bar, line, pie, etc.)
- Apply formatting (colors, borders, fonts)
- Create tables with headers
- Data validation rules

### Example Prompts

```
"Create an Excel budget tracker with income, expenses, and savings calculations"

"Generate a sales dashboard with monthly data and a trend chart"

"Make a project timeline spreadsheet with Gantt-style visualization"
```

### Output Structure

```typescript
interface ExcelOutput {
  workbook: {
    sheets: Sheet[];
    properties: WorkbookProperties;
  };
}

interface Sheet {
  name: string;
  cells: Cell[][];
  charts?: Chart[];
  tables?: Table[];
}

interface Cell {
  value: string | number | null;
  formula?: string;  // e.g., "=SUM(A1:A10)"
  format?: CellFormat;
}
```

### Best Practices

1. **Structure first**: Define columns and data types before populating
2. **Use named ranges**: For complex formulas
3. **Separate data/calculations**: Keep raw data separate from computed values
4. **Chart appropriately**: Match chart type to data relationship

### Example: Budget Tracker

```
Prompt: "Create a monthly budget tracker with categories,
         planned vs actual spending, and variance calculations"

Output:
- Sheet 1: "Budget"
  - Columns: Category | Planned | Actual | Variance | % Spent
  - Rows: Housing, Food, Transport, Utilities, etc.
  - Formulas: Variance = Actual - Planned
  - Conditional formatting: Red if over budget

- Sheet 2: "Charts"
  - Pie chart: Spending by category
  - Bar chart: Planned vs Actual comparison
```

---

## pptx - PowerPoint Generation

**Invocation**: `@pptx` or "create a PowerPoint presentation"

### Capabilities

- Create slide decks with various layouts
- Add text, images, shapes
- Include charts and tables
- Apply themes and styling
- Add speaker notes
- Create transitions

### Slide Layouts

| Layout | Use Case |
|--------|----------|
| Title Slide | Opening, section breaks |
| Title + Content | Standard content slides |
| Two Column | Comparisons, pros/cons |
| Title Only | Full visual slides |
| Blank | Custom layouts |

### Example Prompts

```
"Create a 10-slide pitch deck for a SaaS product"

"Generate a quarterly business review presentation"

"Make a training presentation on data security"
```

### Output Structure

```typescript
interface PowerPointOutput {
  presentation: {
    slides: Slide[];
    theme?: Theme;
    properties: PresentationProperties;
  };
}

interface Slide {
  layout: SlideLayout;
  title?: string;
  content: SlideContent[];
  notes?: string;
  transition?: Transition;
}

interface SlideContent {
  type: 'text' | 'image' | 'chart' | 'table' | 'shape';
  position: Position;
  data: any;
}
```

### Best Practices

1. **6x6 rule**: Max 6 bullets, 6 words each
2. **Visual hierarchy**: One main point per slide
3. **Consistent styling**: Use theme colors
4. **Speaker notes**: Add context for presenter

### Example: Pitch Deck

```
Prompt: "Create a startup pitch deck for a food delivery app"

Output:
1. Title Slide: Company name, tagline
2. Problem: Market pain point
3. Solution: How app solves it
4. Market Size: TAM, SAM, SOM
5. Product: Screenshots, features
6. Business Model: Revenue streams
7. Traction: Metrics, growth
8. Competition: Positioning matrix
9. Team: Founders, advisors
10. Ask: Funding, use of funds
```

---

## pdf - PDF Generation

**Invocation**: `@pdf` or "create a PDF document"

### Capabilities

- Generate formatted PDFs
- Include text, images, tables
- Apply headers/footers
- Create table of contents
- Add page numbers
- Support multi-column layouts

### Example Prompts

```
"Create a PDF report summarizing the quarterly sales data"

"Generate a PDF invoice template"

"Make a PDF user manual for the application"
```

### Output Structure

```typescript
interface PDFOutput {
  document: {
    pages: Page[];
    metadata: PDFMetadata;
    tableOfContents?: TOC;
  };
}

interface Page {
  content: PageContent[];
  header?: HeaderFooter;
  footer?: HeaderFooter;
  pageNumber?: number;
}

interface PageContent {
  type: 'heading' | 'paragraph' | 'table' | 'image' | 'list';
  data: any;
  style?: ContentStyle;
}
```

### Best Practices

1. **Clear hierarchy**: Use heading levels consistently
2. **White space**: Don't overcrowd pages
3. **Consistent margins**: Professional appearance
4. **Page breaks**: Control content flow

### Example: Report

```
Prompt: "Create a quarterly business report PDF"

Output:
- Cover page: Title, date, company logo
- Table of Contents
- Executive Summary
- Financial Overview (with charts)
- Department Highlights
- Challenges & Risks
- Next Quarter Goals
- Appendix: Detailed data tables
```

---

## docx - Word Generation

**Invocation**: `@docx` or "create a Word document"

### Capabilities

- Rich text formatting
- Headers and footers
- Tables and lists
- Styles and themes
- Track changes
- Comments
- Table of contents

### Example Prompts

```
"Create a project proposal document"

"Generate a technical specification document"

"Make a meeting minutes template"
```

### Output Structure

```typescript
interface WordOutput {
  document: {
    sections: Section[];
    styles: StyleDefinition[];
    properties: DocumentProperties;
  };
}

interface Section {
  content: SectionContent[];
  header?: HeaderFooter;
  footer?: HeaderFooter;
  columns?: number;
}

interface SectionContent {
  type: 'heading' | 'paragraph' | 'table' | 'list' | 'image';
  style?: string;  // Reference to style name
  data: any;
}
```

### Best Practices

1. **Use styles**: Consistent formatting via styles, not manual
2. **Heading hierarchy**: Proper H1, H2, H3 structure
3. **Templates**: Create reusable document templates
4. **Metadata**: Include author, date, version

### Example: Proposal

```
Prompt: "Create a project proposal document"

Output:
- Title Page
- Executive Summary
- Problem Statement
- Proposed Solution
- Scope & Deliverables
- Timeline (table)
- Budget (table)
- Team & Resources
- Risk Assessment
- Terms & Conditions
- Appendices
```

---

## Integration with Evolving

### Report Generation Pipeline

```typescript
// Example: Generate analysis report
async function generateAnalysisReport(
  data: AnalysisData,
  format: 'pdf' | 'docx'
): Promise<Document> {
  // 1. Structure content
  const content = structureReport(data);

  // 2. Select skill based on format
  const skill = format === 'pdf' ? 'pdf' : 'docx';

  // 3. Generate document
  return await invokeSkill(skill, {
    template: 'analysis-report',
    content,
    styling: 'professional'
  });
}
```

### Presentation from Analysis

```typescript
// Example: Convert analysis to presentation
async function analysisToSlides(
  analysis: Analysis
): Promise<Presentation> {
  // 1. Extract key points
  const keyPoints = extractKeyPoints(analysis);

  // 2. Map to slide structure
  const slideStructure = mapToSlides(keyPoints);

  // 3. Generate presentation
  return await invokeSkill('pptx', {
    slides: slideStructure,
    theme: 'professional-dark'
  });
}
```

### Data Export to Excel

```typescript
// Example: Export data with analysis
async function exportDataWithAnalysis(
  data: DataSet,
  analysis: Analysis
): Promise<Workbook> {
  return await invokeSkill('xlsx', {
    sheets: [
      { name: 'Raw Data', data: data.rows },
      { name: 'Summary', data: analysis.summary },
      {
        name: 'Charts',
        charts: [
          { type: 'line', data: analysis.trends },
          { type: 'pie', data: analysis.distribution }
        ]
      }
    ]
  });
}
```

---

## Use Cases for Evolving

| Scenario | Skill | Output |
|----------|-------|--------|
| Pitch analysis report | pdf | Formatted analysis PDF |
| Data export | xlsx | Excel with calculations |
| Project presentation | pptx | Slide deck |
| Documentation | docx | Word document |
| Financial tracking | xlsx | Budget spreadsheet |
| Quarterly review | pptx + pdf | Slides + handout |

---

## Skill Invocation

### Direct Invocation

```
@xlsx Create a budget tracker with income categories
@pptx Create a 5-slide product overview
@pdf Create a one-page executive summary
@docx Create a meeting agenda template
```

### Natural Language

```
"Generate an Excel spreadsheet for tracking expenses"
"Create a PowerPoint about our Q4 results"
"Make a PDF report from this analysis"
"Write a Word document proposal"
```

### Chained Generation

```
"Analyze the sales data, then:
 1. Create an Excel summary with pivot tables
 2. Generate a PowerPoint with key insights
 3. Export a PDF report for stakeholders"
```

---

## Related

- [Claude Skills](../claude-skills/index.md)
- [AI Content Generation Pipeline](../../../../patterns/ai-content-generation-pipeline.md)
- [Agent Templates](../agent-templates/mega-template.md)

---

**Source**: anthropic-cookbook/skills
**Last Updated**: 2025-12-13
