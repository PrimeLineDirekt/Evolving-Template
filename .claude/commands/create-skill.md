---
description: Erstellt neuen Skill aus Template
model: haiku
argument-hint: [optional: skill-name]
---

Du bist mein Skill Creation Assistant. Deine Aufgabe ist es, einen neuen Skill aus Templates zu erstellen.

## Schritt 1: Skill-Namen erfassen

Wenn der User einen Namen als Argument übergeben hat ($ARGUMENTS ist nicht leer), nutze das als Skill-Namen.

Wenn $ARGUMENTS leer ist, frage:
"Wie soll der Skill heißen?"

**Beispiele**:
- pdf-processing
- api-rate-limiting
- seo-optimization
- data-visualization
- code-review-checklist

### Naming Conventions:
- Lowercase mit hyphens (nicht underscores oder camelCase)
- Beschreibend (was macht der Skill?)
- Domain oder Funktion als Name
- Keine Sonderzeichen außer Hyphens
- Singular bevorzugt (nicht plural)

### Validation:
- Name ist eindeutig (prüfe .claude/skills/)
- Folgt Konventionen
- Nicht zu generisch oder zu lang

## Schritt 2: Skill-Komplexität bestimmen

Frage: "Wie komplex ist der Skill?"

**Optionen**:

1. **Simple** - Single-File Skill
   - Für: Style guides, Checklists, Straightforward processes
   - Struktur: Ein SKILL.md File (<500 Zeilen)
   - Beispiele: Code review checklist, Naming conventions, API rate limiting

2. **Progressive** - Multi-File Skill mit Progressive Disclosure
   - Für: Complex domains, Multi-faceted expertise, Advanced workflows
   - Struktur: SKILL.md (entry) + reference.md (details) + examples.md (samples)
   - Beispiele: PDF processing, ML optimization, System architecture

**Hilfe bei der Auswahl**:
```
Simple:
  - Kann in <500 Zeilen erklärt werden
  - Straightforward use case
  - Wenig Sub-Topics
  - Hauptsächlich Guidelines/Rules

Progressive:
  - Komplexer Domain (>500 Zeilen nötig)
  - Multiple Sub-Topics
  - Needs detailed reference
  - Benefits from examples
```

Falls unsicher, empfehle **Simple** und erkläre dass später auf Progressive erweitert werden kann.

## Schritt 3: Template(s) lesen

Basierend auf Komplexität:

**Simple**:
```
.claude/templates/skills/simple-skill/SKILL.md
```

**Progressive**:
```
.claude/templates/skills/progressive-skill/SKILL.md
.claude/templates/skills/progressive-skill/reference.md
.claude/templates/skills/progressive-skill/examples.md
```

Nutze Read-Tool um Template-Inhalt(e) zu laden.

## Schritt 4: Informationen sammeln

### Für Simple Skill:

**Erfrage**:
1. **Purpose**: "Was ist der Hauptzweck des Skills? (1 Satz)"
2. **Use Cases**: "Nenne 2-3 primäre Use-Cases"
3. **Core Principles**: "Welche 2-3 Kern-Prinzipien?" (z.B. "DRY", "KISS", "Fail Fast")
4. **Guideline Categories**: "Welche Hauptkategorien für Guidelines?" (z.B. "Naming", "Structure", "Testing")
5. **Common Patterns**: "Gibt es wiederkehrende Patterns?" (Optional)
6. **Best Practices**: "Wichtigste Do's und Don'ts?"

**Auto-Generate**:
- Workflow-Steps (basierend auf Purpose)
- Quick Reference Tables
- Checklist Items

### Für Progressive Skill:

**SKILL.md (Entry Point)**:
1. **Purpose**: "Was ist der Hauptzweck?" (kurz)
2. **Auto-Detection Trigger**: "Wann soll Skill aktivieren?" (Keywords)
3. **Quick Start Steps**: "3-5 Quick Start Steps"
4. **Tools Needed**: "Welche Tools?" (Read, Write, WebSearch, etc.)

**reference.md (Details)**:
5. **Detailed Sections**: "Welche Detail-Bereiche?" (z.B. "Processing Methods", "Configuration", "API Reference")
6. **Technical Specs**: "Gibt es technische Specs?" (Versions, Formats, etc.)
7. **Advanced Topics**: "Welche Advanced Topics?" (Optional)

**examples.md (Practical)**:
8. **Example Scenarios**: "3-5 praktische Beispiele?"
9. **Step-by-Step Walkthroughs**: "Detailed Walkthroughs nötig?"

## Schritt 5: Placeholders ersetzen

Ersetze alle `{PLACEHOLDERS}` in Template(s):

### Simple Skill Placeholders:

- `{SKILL_NAME}` → Skill Name (Title Case)
- `{BRIEF_DESCRIPTION_OF_SKILL_PURPOSE}` → Purpose
- `{USE_CASE_1-3}` → Use Cases
- `{PRINCIPLE_1-3}` → Core Principles
- `{GUIDELINE_CATEGORY_1-2}` → Guideline Categories
- `{PATTERN_NAME}` → Pattern Names
- `{PRACTICE_X}` → Best Practices
- `{ANTI_PATTERN_X}` → Anti-Patterns
- `{VERSION}` → Version (Default: "1.0")
- `{DATE}` → Current Date
- `{MAINTAINER}` → "Meta-Agent System" oder User

### Progressive Skill Placeholders:

**SKILL.md**:
- `{SKILL_NAME}` → Skill Name
- `{BRIEF_PURPOSE}` → Short purpose
- `{TRIGGER_PATTERN_X}` → Auto-detection patterns
- `{QUICK_START_STEP_X}` → Quick start steps
- `{TOOL_X}` → Required tools

**reference.md**:
- `{DETAILED_SECTION_X}` → Detailed sections
- `{SPECIFICATION_X}` → Technical specs
- `{ADVANCED_TOPIC_X}` → Advanced topics

**examples.md**:
- `{EXAMPLE_SCENARIO_X}` → Example scenarios
- `{STEP_BY_STEP_X}` → Walkthroughs

### Frontmatter (beide Typen):

```yaml
---
name: {skill-name}  # lowercase-with-hyphens
description: "{DESCRIPTION mit Trigger-Hints}"
allowed-tools: {TOOL_1}, {TOOL_2}, {TOOL_3}
---
```

**Description für Auto-Detection**:
Sollte Trigger-Keywords enthalten, z.B.:
```
"PDF Processing Skill. Aktiviert bei 'analyze pdf', 'extract from pdf'.
Supports text extraction, table analysis, metadata extraction."
```

## Schritt 6: Validierung

Vor dem Schreiben prüfe:

- [ ] Alle Placeholders ersetzt
- [ ] Frontmatter YAML ist valide
- [ ] Skill-Name folgt Konventionen
- [ ] Directory `.claude/skills/{name}/` existiert oder wird erstellt
- [ ] Keine Konflikte mit bestehenden Skills
- [ ] (Progressive) Alle 3 Files vorbereitet
- [ ] Description enthält Trigger-Keywords (für Auto-Detection)

Falls Skill bereits existiert, frage:
"Der Skill `.claude/skills/{name}/` existiert bereits. Überschreiben? (Y/N)"

## Schritt 7: Dateien erstellen

### Simple Skill:

**Pfad**: `.claude/skills/{name}/SKILL.md`

1. Erstelle Directory: `.claude/skills/{name}/`
2. Write SKILL.md File

### Progressive Skill:

**Pfad**: `.claude/skills/{name}/`

1. Erstelle Directory: `.claude/skills/{name}/`
2. Write SKILL.md (Entry Point)
3. Write reference.md (Detailed Docs)
4. Write examples.md (Practical Examples)

**Wichtig**: Alle 3 Files müssen erstellt werden für Progressive Skills.

## Schritt 8: Auto-Detection Pattern dokumentieren (Optional)

Falls Skill Auto-Detection haben soll, dokumentiere Pattern:

**In SKILL.md Frontmatter** (bereits gemacht in Step 5):
```yaml
description: "{Description MIT Trigger-Keywords}"
```

**Optional - In workflow-patterns.md erwähnen**:
Frage: "Soll ich den Skill in workflow-patterns.md dokumentieren?"

Falls ja:
1. Read `.claude/workflow-patterns.md`
2. Prüfe ob Skill-Sektion existiert
3. Füge Skill-Pattern hinzu (ähnlich wie Commands)
4. Edit die Datei

**Pattern-Template**:
```markdown
### Skills: {SKILL_NAME}

**Trigger-Keywords**:
- {KEYWORD_1}
- {KEYWORD_2}

**Auto-Activation**: {WHEN_TO_ACTIVATE}
```

## Schritt 9: Bestätigung

Zeige dem User:

```
✓ {SKILL_NAME} Skill erfolgreich erstellt!

{Simple}
Datei: .claude/skills/{name}/SKILL.md

{Progressive}
Dateien:
  .claude/skills/{name}/SKILL.md
  .claude/skills/{name}/reference.md
  .claude/skills/{name}/examples.md

Typ: {Simple|Progressive} Skill
Complexity: {Low|Medium|High}
Tools: {LIST_OF_TOOLS}

Auto-Activation Triggers:
→ {TRIGGER_1}
→ {TRIGGER_2}

Nächste Schritte:
→ Skill aktiviert sich automatisch bei {TRIGGER_CONTEXT}
→ Teste mit: {EXAMPLE_PROMPT}
→ {SIMPLE: "Erweitere mit mehr Patterns/Examples"}
→ {PROGRESSIVE: "Review reference.md für Details, examples.md für Walkthroughs"}

{Falls Progressive}
Progressive Disclosure:
→ SKILL.md: Entry point (<500 Zeilen)
→ reference.md: Detailed documentation
→ examples.md: Practical examples

Related Skills: {RELATED_SKILLS}
```

**Beispiel Simple**:
```
✓ API Rate Limiting Skill erfolgreich erstellt!

Datei: .claude/skills/api-rate-limiting/SKILL.md

Typ: Simple Skill
Complexity: Low
Tools: Read, Write, WebFetch

Auto-Activation Triggers:
→ "api integration"
→ "rate limit"
→ "api quota"

Nächste Schritte:
→ Skill aktiviert sich automatisch bei API-bezogenen Tasks
→ Teste mit: "Implement rate limiting for Twitter API"
→ Erweitere mit mehr Patterns/Examples für spezifische APIs

Related Skills: web-scraping, api-design
```

**Beispiel Progressive**:
```
✓ PDF Processing Skill erfolgreich erstellt!

Dateien:
  .claude/skills/pdf-processing/SKILL.md
  .claude/skills/pdf-processing/reference.md
  .claude/skills/pdf-processing/examples.md

Typ: Progressive Skill
Complexity: Medium-High
Tools: Read, Write, mcp__pdf-tools

Auto-Activation Triggers:
→ "analyze pdf"
→ "extract from pdf"
→ "pdf summary"

Nächste Schritte:
→ Skill aktiviert sich automatisch bei PDF-bezogenen Tasks
→ Teste mit: "Extract text from /path/to/document.pdf"
→ Review reference.md für Technical Details
→ Review examples.md für Step-by-Step Walkthroughs

Progressive Disclosure:
→ SKILL.md: Entry point (<500 Zeilen)
→ reference.md: Processing methods, APIs, configurations
→ examples.md: Text extraction, table analysis, summary generation

Related Skills: document-analysis, ocr-processing
```

---

## Tool Usage

**Required Tools**:
- `Read`: Template(s) einlesen
- `Write`: Skill-File(s) erstellen
- `Bash`: Directory erstellen (mkdir -p)
- `Edit`: workflow-patterns updaten (optional)

**Tool Pattern Simple**:
```
1. Read template file
2. Replace all placeholders
3. Validate
4. Bash: mkdir -p .claude/skills/{name}
5. Write SKILL.md
6. Confirm to user
```

**Tool Pattern Progressive**:
```
1. Read 3 template files
2. Replace placeholders in all 3
3. Validate
4. Bash: mkdir -p .claude/skills/{name}
5. Write SKILL.md
6. Write reference.md
7. Write examples.md
8. Confirm to user
```

---

## Error Handling

### Template nicht gefunden

```
IF template_not_found:
  Liste verfügbare Skill-Templates
  Frage User welcher Template
  Retry
```

### Skill existiert bereits

```
IF skill_exists:
  Frage: "Skill existiert bereits. Überschreiben? (Y/N)"
  IF no: Frage nach alternativem Namen
  IF yes: Backup erstellen (optional), dann überschreiben
```

### Directory-Erstellung fehlschlägt

```
IF mkdir_fails:
  Prüfe Permissions
  Versuche Parent-Directory zu erstellen
  Falls persistent fehlschlägt: Error an User mit Anleitung
```

### Multi-File Write fehlschlägt (Progressive)

```
IF one_file_fails:
  Rollback bereits geschriebene Files
  Oder: Frage User ob partial creation ok ist
  Log welche Files erfolgreich erstellt wurden
```

---

## Validation Checklist

Vor Bestätigung prüfe:

- [ ] Template(s) erfolgreich gelesen
- [ ] Alle User-Inputs erhalten
- [ ] Alle Placeholders ersetzt
- [ ] Frontmatter valide
- [ ] Skill-Name valide
- [ ] Directory erstellt
- [ ] File(s) geschrieben
- [ ] (Progressive) Alle 3 Files vorhanden
- [ ] Description hat Trigger-Keywords
- [ ] User erhält klare Next Steps

---

## Best Practices

**Do's**:
- Wähle richtigen Komplexitäts-Level (Simple vs. Progressive)
- Include Trigger-Keywords in Description
- Gib konkrete Beispiele in Fragen
- Validiere vor dem Schreiben
- Für Progressive: Achte auf gute Separation (Entry/Details/Examples)
- Dokumentiere related Skills

**Don'ts**:
- Erstelle keinen Skill ohne User-Bestätigung
- Überkompliziere nicht (Simple reicht oft)
- Lasse keine Placeholders im Output
- Vergiss nicht Directory zu erstellen
- (Progressive) Erstelle nicht nur 1 oder 2 Files - alle 3 oder Simple wählen

---

## Progressive Skill Guidelines

### Wann Progressive wählen?

Progressive Skill macht Sinn wenn:
- Content >500 Zeilen
- Multiple komplexe Sub-Topics
- Braucht detailed reference documentation
- Benefits von Beispielen/Walkthroughs
- Advanced topics existieren

### SKILL.md (Entry) Guidelines:

- **Ziel**: User schnell orientieren
- **Length**: <500 Zeilen
- **Content**:
  - Purpose (kurz)
  - Quick Start (3-5 Steps)
  - When to use
  - Auto-Detection Trigger
  - Progressive Disclosure Hints ("See reference.md for...")

### reference.md Guidelines:

- **Ziel**: Comprehensive documentation
- **Content**:
  - Detailed explanations
  - Technical specifications
  - API references
  - Configuration options
  - Advanced topics
  - Troubleshooting

### examples.md Guidelines:

- **Ziel**: Practical learning
- **Content**:
  - Real-world scenarios
  - Step-by-step walkthroughs
  - Before/after examples
  - Common patterns
  - Edge cases

---

## Examples

### Simple Skill Beispiel

```
User: /create-skill api-rate-limiting

Komplexität: Simple
Purpose: "Apply rate limiting patterns to API integrations"
Use Cases: External APIs, Quota prevention, Graceful degradation
Principles: Respect limits, Exponential backoff, Cache aggressively
Categories: Rate Limit Detection, Retry Strategies

→ Erstellt: .claude/skills/api-rate-limiting/SKILL.md
→ Triggers: "api integration", "rate limit"
```

### Progressive Skill Beispiel

```
User: /create-skill pdf-processing

Komplexität: Progressive
Purpose: "Extract, analyze, and summarize PDF documents"
Triggers: "analyze pdf", "extract from pdf", "pdf summary"
Tools: Read, Write, mcp__pdf-tools

SKILL.md: Entry point, Quick Start
reference.md: PDF structure, Extraction methods, OCR, Table detection
examples.md: Research paper extraction, Financial report tables, Summary generation

→ Erstellt: 3 Files in .claude/skills/pdf-processing/
→ Progressive Disclosure optimiert
```

---

## Related Commands

- `/create-agent` - Agent erstellen
- `/create-command` - Command erstellen
- `/create-hook` - Hook erstellen

**Template-Creator Skill**: Dieser Command kann auch durch den `template-creator` Skill getriggert werden.

---

**Wichtig**:
- Wähle richtige Komplexität (Simple vs. Progressive)
- Include Trigger-Keywords in Description
- Für Progressive: Erstelle ALLE 3 Files
- Nutze Progressive Disclosure richtig
- Dokumentiere Auto-Activation Pattern
