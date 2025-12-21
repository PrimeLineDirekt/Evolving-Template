# Template Creator - Practical Examples

Real-world examples for creating each template type.

---

## Table of Contents

1. [Example 1: SEO Specialist Agent](#example-1-seo-specialist-agent)
2. [Example 2: Project Init Command](#example-2-project-init-command)
3. [Example 3: Pre-Commit Hook](#example-3-pre-commit-hook)
4. [Example 4: PDF Processing Skill](#example-4-pdf-processing-skill)
5. [Example 5: Rate Limiting Pattern](#example-5-rate-limiting-pattern)
6. [Example 6: ML Project Learning](#example-6-ml-project-learning)

---

## Example 1: SEO Specialist Agent

### User Request

```
User: "Erstelle einen SEO-Spezialisten Agent der Websites analysieren kann."
```

### Detection & Type Selection

```
Confidence: 10/10 (Clear agent creation intent)
Type: Agent (Specialist)
Template: specialist-agent.md
```

### Information Gathering

**Questions Asked**:
1. "Welche SEO-Bereiche soll der Agent abdecken?"
2. "Welche Tools benötigt der Agent?"

**User Responses**:
- Bereiche: On-page, Technical, Content, Link Building, Analytics
- Tools: WebSearch, WebFetch, Read

### Placeholder Mapping

```yaml
{DOMAIN}: "SEO"
{DESCRIPTION}: "Search Engine Optimization expert specializing in website analysis and optimization"
{EXPERTISE_AREA_1}: "On-page SEO optimization"
{EXPERTISE_AREA_2}: "Technical SEO and site performance"
{EXPERTISE_AREA_3}: "Content strategy and optimization"
{EXPERTISE_AREA_4}: "Link building and backlink analysis"
{EXPERTISE_AREA_5}: "SEO analytics and reporting"
{INPUT_FIELD_1}: "url"
{INPUT_FIELD_2}: "analysis_type"
{INPUT_FIELD_3}: "competitor_urls"
{INPUT_FIELD_4}: "target_keywords"
{TOOL_1}: "WebSearch: Research keywords and competitors"
{TOOL_2}: "WebFetch: Analyze website content and structure"
{TOOL_3}: "Read: Access local SEO knowledge base"
{CRITERION_1}: "Technical Health"
{CRITERION_2}: "Content Quality"
{CRITERION_3}: "Link Profile"
```

### Template Before Replacement

```markdown
# {DOMAIN} Specialist Agent

## Agent Role & Expertise

You are a highly specialized **{DOMAIN} Agent** with deep expertise in {DESCRIPTION}.

**Specialization**:
- {EXPERTISE_AREA_1}
- {EXPERTISE_AREA_2}
- {EXPERTISE_AREA_3}
...
```

### Template After Replacement

```markdown
# SEO Specialist Agent

## Agent Role & Expertise

You are a highly specialized **SEO Agent** with deep expertise in Search Engine Optimization expert specializing in website analysis and optimization.

**Specialization**:
- On-page SEO optimization
- Technical SEO and site performance
- Content strategy and optimization
- Link building and backlink analysis
- SEO analytics and reporting
...
```

### Output File

**Location**: `.claude/agents/seo-agent.md`

**Confirmation Message**:
```
✓ SEO Specialist Agent erfolgreich erstellt!

Datei: .claude/agents/seo-agent.md
Typ: Specialist Agent
Domain: SEO
Tools: WebSearch, WebFetch, Read

Nächste Schritte:
→ Aktiviere den Agent mit @seo-agent in deinen Prompts
→ Teste mit: "Analysiere https://example.com auf SEO-Optimierung"
→ Passe Expertise-Bereiche an falls nötig

Dokumentation: Siehe .claude/templates/agents/specialist-agent.md
```

---

## Example 2: Project Init Command

### User Request

```
User: "Ich brauche einen Command der neue Projekte initialisiert"
```

### Detection & Type Selection

```
Confidence: 9/10 (Command creation intent)
Type: Command (Workflow)
Template: workflow-command.md
```

### Information Gathering

**Questions Asked**:
1. "Was soll der Command genau tun?"
2. "Welche Informationen werden vom User benötigt?"
3. "Wo sollen Projekt-Dateien gespeichert werden?"

**User Responses**:
- Erstellt Projektstruktur mit README, docs, src Ordnern
- User gibt Projektnamen, Typ (web/cli/library), Beschreibung
- Speichern in `projects/{projekt-name}/`

### Placeholder Mapping

```yaml
{BRIEF_DESCRIPTION}: "Initialisiert neue Projekte mit Standardstruktur"
{ARGUMENT_DESCRIPTION}: "optional: projekt-name"
{ROLE_DESCRIPTION}: "Project Setup Assistant"
{PRIMARY_TASK_DESCRIPTION}: "initialize a new project with standard structure and documentation"
{INPUT_GATHERING_STEP}: "Project Information Collection"
{INPUT_NAME}: "project name"
{PROMPT_FOR_USER_INPUT}: "Wie soll dein Projekt heißen?"
{ANALYSIS_OR_PROCESSING_STEP}: "Project Configuration"
{ANALYSIS_DIMENSION_1}: "Project Type"
{EXAMPLE_1}: "web - Web application"
{EXAMPLE_2}: "cli - Command-line tool"
{EXAMPLE_3}: "library - Reusable library"
{ANALYSIS_DIMENSION_2}: "Tech Stack"
{ANALYSIS_DIMENSION_3}: "License Type"
{METADATA_GENERATION_STEP}: "Directory Structure Planning"
{FILE_CREATION_STEP}: "Project Files Creation"
{FILE_PATH}: "projects"
{CONFIRMATION_STEP}: "Confirmation & Next Steps"
```

### Output File

**Location**: `.claude/commands/project-init.md`

**Key Sections**:
```markdown
---
description: Initialisiert neue Projekte mit Standardstruktur
argument-hint: [optional: projekt-name]
---

You are my Project Setup Assistant. Your task is to initialize a new project with standard structure and documentation.

## Step 1: Project Information Collection

If the user provided an argument ($ARGUMENTS is not empty), use that as project name.

If $ARGUMENTS is empty, ask:
"Wie soll dein Projekt heißen?"

### Input Validation:
- Check if name is valid (alphanumeric, hyphens, underscores)
- Validate project doesn't already exist
- Ensure name follows conventions
...
```

### Confirmation Message

```
✓ Command erfolgreich erstellt!

Datei: .claude/commands/project-init.md
Typ: Workflow Command
Purpose: Initialisiert neue Projekte mit Standardstruktur

Nächste Schritte:
→ Teste mit: /project-init test-project
→ Passe Directory-Struktur an falls nötig
→ Erweitere Validation-Logic in Step 1

Related: /project-add zum Dokumentieren bestehender Projekte
```

---

## Example 3: Pre-Commit Hook

### User Request

```
User: "Create a hook that validates markdown files before they're committed"
```

### Detection & Type Selection

```
Confidence: 8/10 (Hook creation, but "pre-commit" might mean Git hook)
Type: Hook (Post-Tool-Use - adapted for validation)
Template: post-tool-use.sh
```

### Clarification

```
Assistant: "Meinst du einen Git pre-commit hook oder einen Claude hook der nach Edit/Write triggert?"
User: "Claude hook, der nach Write triggert und Markdown validiert"
```

### Information Gathering

**Questions Asked**:
1. "Welche Markdown-Dateien sollen validiert werden?"
2. "Was soll bei Validation-Fehlern passieren?"

**User Responses**:
- Alle .md Dateien in ideas/, knowledge/, projects/
- Log errors, optional: auto-fix common issues

### Placeholder Mapping

```yaml
{PATH_PATTERN_1}: "ideas/.*\\.md"
{PATH_PATTERN_2}: "knowledge/.*\\.md"
{CUSTOM_WRITE_LOGIC}: "validate_markdown \"$file_path\""
{CUSTOM_EDIT_LOGIC}: "validate_markdown \"$file_path\""
```

### Custom Logic Added

```bash
# Markdown validation function
validate_markdown() {
  local file_path="$1"
  local errors=0

  # Check frontmatter
  if ! has_valid_frontmatter "$file_path"; then
    info_log "Invalid frontmatter in $file_path"
    ((errors++))
  fi

  # Check for broken links
  if has_broken_links "$file_path"; then
    info_log "Broken links in $file_path"
    ((errors++))
  fi

  # Check heading structure
  if ! has_valid_headings "$file_path"; then
    info_log "Invalid heading structure in $file_path"
    ((errors++))
  fi

  if [[ $errors -gt 0 ]]; then
    info_log "Validation failed: $file_path ($errors issues)"
  else
    debug_log "Validation passed: $file_path"
  fi
}
```

### Output File

**Location**: `.claude/hooks/markdown-validator.sh`

**Post-Creation Steps**:
```bash
chmod +x .claude/hooks/markdown-validator.sh
```

### Confirmation Message

```
✓ Hook erfolgreich erstellt!

Datei: .claude/hooks/markdown-validator.sh
Typ: Post-Tool-Use Hook
Triggers: Write, Edit on .md files
Monitored Paths: ideas/, knowledge/, projects/

Nächste Schritte:
→ Hook ist bereits executable (chmod +x applied)
→ Teste durch Bearbeiten einer .md Datei
→ Check logs in .claude/hooks/logs/post-tool-use.log
→ Optional: Konfiguriere in .claude/settings.json

Testing: Edit eine .md Datei und prüfe ob Validation läuft
```

---

## Example 4: PDF Processing Skill

### User Request

```
User: "Neuer Skill für PDF-Verarbeitung und Analyse"
```

### Detection & Type Selection

```
Confidence: 9/10 (Skill creation intent)
Type: Skill (Progressive - complex domain)
Template: progressive-skill/
```

### Information Gathering

**Questions Asked**:
1. "Welche PDF-Operationen soll der Skill abdecken?"
2. "Gibt es spezielle Anforderungen?"

**User Responses**:
- Text extraction, Table extraction, Metadata analysis, Summary generation
- Support für multi-page PDFs, OCR falls nötig

### Placeholder Mapping

**SKILL.md**:
```yaml
{SKILL_NAME}: "PDF Processing"
{BRIEF_PURPOSE}: "Extract, analyze, and summarize PDF documents"
{TRIGGER_PATTERN_1}: "analyze pdf"
{TRIGGER_PATTERN_2}: "extract from pdf"
{TRIGGER_PATTERN_3}: "pdf summary"
{QUICK_START_STEP_1}: "Detect PDF file path"
{QUICK_START_STEP_2}: "Determine operation type"
{QUICK_START_STEP_3}: "Execute and return results"
```

**reference.md**:
```yaml
{DETAILED_SECTION_1}: "PDF Structure & Parsing"
{DETAILED_SECTION_2}: "Text Extraction Methods"
{DETAILED_SECTION_3}: "Table Detection & Extraction"
{SPECIFICATION_1}: "Supported PDF versions"
{SPECIFICATION_2}: "OCR integration"
{ADVANCED_TOPIC_1}: "Multi-page handling strategies"
```

**examples.md**:
```yaml
{EXAMPLE_SCENARIO_1}: "Extracting text from research paper"
{EXAMPLE_SCENARIO_2}: "Analyzing financial report tables"
{EXAMPLE_SCENARIO_3}: "Generating executive summary"
```

### Output Structure

```
.claude/skills/pdf-processing/
├── SKILL.md          (Entry point, <500 lines)
├── reference.md      (Technical details)
└── examples.md       (Practical examples)
```

### SKILL.md Excerpt

```markdown
---
name: pdf-processing
description: "PDF Processing Skill. Aktiviert bei 'analyze pdf', 'extract from pdf', 'pdf summary'. Supports text extraction, table analysis, metadata extraction, and summary generation. Progressive Disclosure: reference.md für Details, examples.md für Beispiele."
allowed-tools: Read, Write, mcp__pdf-tools
---

# PDF Processing

## Purpose

Extract, analyze, and summarize PDF documents with support for text, tables, metadata, and multi-page documents.

**Use this skill for**:
- Text extraction from PDFs
- Table detection and extraction
- Metadata analysis
- Summary generation
- OCR-based text recovery

## Quick Start

### Step 1: Detect PDF File Path
Identify PDF file from user input or file path.

### Step 2: Determine Operation Type
- Text extraction
- Table extraction
- Metadata analysis
- Summary generation

### Step 3: Execute and Return Results
Process PDF and return formatted results.

**See reference.md for detailed processing methods**
**See examples.md for practical walkthroughs**
...
```

### Confirmation Message

```
✓ PDF Processing Skill erfolgreich erstellt!

Dateien:
  .claude/skills/pdf-processing/SKILL.md
  .claude/skills/pdf-processing/reference.md
  .claude/skills/pdf-processing/examples.md

Typ: Progressive Skill
Complexity: Medium-High
Tools: Read, Write, mcp__pdf-tools

Nächste Schritte:
→ Skill aktiviert sich bei: "analyze pdf", "extract from pdf", "pdf summary"
→ Teste mit: "Extract text from /path/to/document.pdf"
→ Erweitere reference.md mit spezifischen PDF-Tools
→ Füge mehr Beispiele in examples.md hinzu

Documentation: Progressive structure mit 3 Dateien für optimale Disclosure
```

---

## Example 5: Rate Limiting Pattern

### User Request

```
User: "Dokumentiere das Rate Limiting Pattern für API Calls"
```

### Detection & Type Selection

```
Confidence: 7/10 (Pattern documentation - could be knowledge or skill)
Type: Skill (Simple - straightforward pattern)
Template: simple-skill/SKILL.md
```

### Clarification

```
Assistant: "Soll das als Skill dokumentiert werden (wiederverwendbares Pattern) oder in die Knowledge Base (einmaliges Wissen)?"
User: "Als Skill, damit es bei API-bezogenen Tasks automatisch aktiviert wird"
```

### Placeholder Mapping

```yaml
{SKILL_NAME}: "API Rate Limiting"
{BRIEF_DESCRIPTION_OF_SKILL_PURPOSE}: "Apply rate limiting patterns to API integrations"
{USE_CASE_1}: "External API integrations"
{USE_CASE_2}: "Preventing API quota exhaustion"
{USE_CASE_3}: "Graceful degradation under limits"
{PRINCIPLE_1}: "Respect API Limits"
{PRINCIPLE_2}: "Implement Exponential Backoff"
{PRINCIPLE_3}: "Cache Aggressively"
{GUIDELINE_CATEGORY_1}: "Rate Limit Detection"
{GUIDELINE_CATEGORY_2}: "Retry Strategies"
{PATTERN_1}: "Token Bucket"
{PATTERN_2}: "Sliding Window"
```

### Output File

**Location**: `.claude/skills/api-rate-limiting/SKILL.md`

**Key Sections**:
```markdown
---
name: api-rate-limiting
description: "Rate limiting patterns for API integrations. Auto-activates for API-related tasks. Covers token bucket, sliding window, exponential backoff, and caching strategies."
allowed-tools: Read, Write, WebFetch
---

# API Rate Limiting

## Purpose

Apply proven rate limiting patterns to API integrations to prevent quota exhaustion and ensure reliable operation.

**Use this skill for**:
- External API integrations
- Preventing API quota exhaustion
- Graceful degradation under limits

## Core Principles

### 1. Respect API Limits
Always stay within documented rate limits. Budget for 80% of limit to allow headroom.

### 2. Implement Exponential Backoff
When rate limited, wait progressively longer before retrying.

### 3. Cache Aggressively
Cache responses to minimize API calls.

## Guidelines

### Rate Limit Detection

**Rule 1**: Check response headers
- **Good**: `if response.headers['X-RateLimit-Remaining'] < 10: sleep()`
- **Bad**: `while True: api_call()  # No limit checking`

**Rule 2**: Parse error responses
- **Good**: `if response.status == 429: backoff()`
- **Bad**: `Ignore 429 errors`

### Retry Strategies

**Rule 1**: Exponential backoff
- Example: `wait_time = base_delay * (2 ** attempt)`

**Rule 2**: Max retry limit
- Example: `max_retries = 3`

## Common Patterns

### Pattern 1: Token Bucket

**When to use**: Smoothing burst traffic

**How to apply**:
```python
class TokenBucket:
    def __init__(self, rate, capacity):
        self.rate = rate
        self.capacity = capacity
        self.tokens = capacity
        self.last_update = time.time()

    def consume(self, tokens=1):
        self._refill()
        if self.tokens >= tokens:
            self.tokens -= tokens
            return True
        return False

    def _refill(self):
        now = time.time()
        elapsed = now - self.last_update
        self.tokens = min(
            self.capacity,
            self.tokens + elapsed * self.rate
        )
        self.last_update = now
```
...
```

### Confirmation Message

```
✓ API Rate Limiting Skill erfolgreich erstellt!

Datei: .claude/skills/api-rate-limiting/SKILL.md
Typ: Simple Skill
Complexity: Low
Auto-Activation: API-related tasks

Nächste Schritte:
→ Skill aktiviert sich bei API-Integration Tasks
→ Review patterns: Token Bucket, Sliding Window
→ Erweitere mit domain-specific limits (Twitter, OpenAI, etc.)

Related Skills: web-scraping, api-integration
```

---

## Example 6: ML Project Learning

### User Request

```
User: "Create a research agent for machine learning trends"
```

### Detection & Type Selection

```
Confidence: 10/10 (Clear agent creation intent)
Type: Agent (Research)
Template: research-agent.md
```

### Information Gathering

**Questions Asked**:
1. "Welche ML-Bereiche sollen erforscht werden?"
2. "Wie tief soll die Recherche sein (surface/standard/deep)?"
3. "Welche Quellen sollen priorisiert werden?"

**User Responses**:
- Bereiche: Deep Learning, NLP, Computer Vision, MLOps
- Standard depth (5-10 sources)
- Priorisiere: Academic papers, Industry blogs, GitHub repos

### Placeholder Mapping

```yaml
{DOMAIN}: "Machine Learning"
{RESEARCH_DOMAIN_1}: "Deep Learning architectures and techniques"
{RESEARCH_DOMAIN_2}: "Natural Language Processing advances"
{RESEARCH_DOMAIN_3}: "Computer Vision applications"
{TOPIC}: "Machine learning trends and innovations"
```

### Output File

**Location**: `.claude/agents/ml-research-agent.md`

**Key Sections**:
```markdown
# Machine Learning Research Agent

## Agent Role & Expertise

You are a specialized **Machine Learning Research Agent** with expertise in multi-source data collection, validation, and synthesis in the ML domain.

**Research Domains**:
- Deep Learning architectures and techniques
- Natural Language Processing advances
- Computer Vision applications

## Research Framework

### 1. Research Planning

**Research Strategy**:
Standard depth:
- Sources: 5-10
- Validation: Multi-source validation
- Time: 15-30 minutes

**Priority Sources**:
1. ArXiv (academic papers)
2. Papers with Code
3. Industry ML blogs (Google AI, OpenAI, etc.)
4. GitHub trending (ML repositories)

### 2. Data Collection

**Source Types**:
- **Primary**: Research papers, official documentation
- **Secondary**: Technical blog posts, conference talks
- **Tertiary**: News articles, aggregators

### 3. Validation & Confidence Scoring

**Confidence Levels**:
- 90-100%: Multiple academic sources + implementation
- 70-89%: Academic source + industry validation
- 50-69%: Single academic source or multiple blogs
- 30-49%: Blog posts only
- 0-29%: Unverified claims
...
```

### Confirmation Message

```
✓ Machine Learning Research Agent erfolgreich erstellt!

Datei: .claude/agents/ml-research-agent.md
Typ: Research Agent
Domain: Machine Learning
Research Depth: Standard (5-10 sources)
Priority Sources: Academic, Industry, GitHub

Nächste Schritte:
→ Aktiviere mit @ml-research-agent
→ Teste mit: "Research latest advances in transformer architectures"
→ Review confidence scoring logic
→ Customize source priorities if needed

Tools: WebSearch, WebFetch, Read
Output: Multi-source validated research reports with confidence scores
```

---

## Common Patterns Across Examples

### Pattern 1: Progressive Questioning

Start with essential information, ask follow-ups as needed:

```
1. Detect intent and type
2. Ask for required placeholders only
3. Infer optional placeholders from context
4. Confirm before creation
```

### Pattern 2: Validation Before Writing

Always validate before creating files:

```
1. Check all required placeholders filled
2. Verify output path valid
3. Ensure no file conflicts
4. Validate placeholder values
5. Confirm with user
6. Write files
```

### Pattern 3: Clear Confirmation

Every creation ends with structured confirmation:

```
✓ {TYPE} erfolgreich erstellt!

Datei: {PATH}
Typ: {TEMPLATE_TYPE}
{KEY_DETAILS}

Nächste Schritte:
→ {ACTION_1}
→ {ACTION_2}
→ {ACTION_3}

{RELATED_INFO}
```

### Pattern 4: Context-Aware Defaults

Use intelligent defaults when possible:

```python
# If user says "create SEO agent"
domain = "SEO"
expertise_areas = infer_from_domain(domain)
# ["On-page SEO", "Technical SEO", "Content Strategy", ...]

# If user says "create hook for ideas"
monitored_paths = ["ideas/"]
# Infer from context
```

---

## Tips for Successful Template Creation

### 1. Understand User Intent

- Listen for keywords: "create", "new", "make", "generate"
- Clarify ambiguity: "Meinst du einen Agent oder einen Command?"
- Confirm before proceeding: "Soll ich einen {TYPE} erstellen?"

### 2. Ask Smart Questions

- Start with type (if unclear)
- Ask for domain/purpose
- Only ask for non-inferrable placeholders
- Provide examples in questions

### 3. Validate Thoroughly

- Check all required fields
- Verify paths and filenames
- Test for conflicts
- Confirm frontmatter validity

### 4. Provide Clear Output

- Show file location
- Explain how to use
- Suggest next steps
- Link to documentation

### 5. Handle Errors Gracefully

- Explain what went wrong
- Suggest fixes
- Offer alternatives
- Never leave user stuck

---

**Last Updated**: 2024-11-26
**Maintained by**: Meta-Agent System
