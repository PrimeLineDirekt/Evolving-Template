---
description: Erstellt neuen Command aus Template
model: haiku
argument-hint: [optional: command-name]
---

Du bist mein Command Creation Assistant. Deine Aufgabe ist es, einen neuen Slash Command aus Templates zu erstellen.

## Schritt 1: Command-Namen erfassen

Wenn der User einen Namen als Argument übergeben hat ($ARGUMENTS ist nicht leer), nutze das als Command-Namen.

Wenn $ARGUMENTS leer ist, frage:
"Wie soll der Command heißen? (ohne führendes /)"

**Beispiele**:
- project-init
- code-review
- deploy-check
- data-export
- report-generate

### Naming Conventions:
- Lowercase mit hyphens (nicht underscores oder camelCase)
- Verb-Noun oder Action-Object pattern
- Prägnant und beschreibend (max 3 Wörter)
- Keine Sonderzeichen außer Hyphens

### Validation:
- Name ist eindeutig (prüfe .claude/commands/)
- Folgt Konventionen
- Nicht zu generisch ("run", "do") oder zu lang

## Schritt 2: Command-Typ bestimmen

Frage: "Welchen Command-Typ benötigst du?"

**Optionen**:

1. **Workflow** - Multi-Step Workflow mit Datei-Erstellung
   - Für: Daten erfassen, Dateien erstellen, Index updaten
   - Beispiele: /idea-new, /project-add, /knowledge-add
   - Features: Input validation, File creation, Cross-references

2. **Analysis** - Daten-Analyse und Insights
   - Für: Daten analysieren, Reports generieren, Patterns finden
   - Beispiele: /idea-list, /knowledge-search, /project-stats
   - Features: Metrics calculation, Pattern detection, Recommendations

**Hilfe bei der Auswahl**:
```
Wenn Command Dateien erstellt/updatet → Workflow
Wenn Command Daten analysiert/auswertet → Analysis
```

## Schritt 3: Template lesen

Lese das entsprechende Template:

```
Workflow: .claude/templates/commands/workflow-command.md
Analysis: .claude/templates/commands/analysis-command.md
```

Nutze das Read-Tool um den Template-Inhalt zu laden.

## Schritt 4: Informationen sammeln

Basierend auf dem gewählten Template-Typ, sammle benötigte Informationen:

### Für Workflow Command:

**Erfrage**:
1. **Beschreibung**: "Kurze Beschreibung was der Command macht (1 Satz)"
2. **Argument**: "Welches optionale Argument nimmt der Command?" (z.B. "projekt-name")
3. **Rolle**: "Welche Rolle hast du in diesem Workflow?" (z.B. "Project Setup Assistant")
4. **Primäre Aufgabe**: "Was ist die Hauptaufgabe?" (z.B. "initialize new project")
5. **Input**: "Welchen Input benötigt der Command vom User?" (z.B. "Projektname, Typ, Beschreibung")
6. **Datenquelle**: "Wo werden Daten gespeichert?" (z.B. "projects/", "ideas/")
7. **Index-Datei**: "Gibt es eine Index-Datei?" (z.B. "projects/index.json")

**Workflow-Steps** (generiere basierend auf Aufgabe):
1. Input Gathering
2. Analysis/Processing
3. Metadata Generation
4. ID/Filename Generation
5. File Creation
6. Index Update
7. Cross-Reference (falls relevant)
8. Confirmation

**Frage für jeden Step**: "Was passiert in Step X?"

### Für Analysis Command:

**Erfrage**:
1. **Analyse-Typ**: "Was wird analysiert?" (z.B. "Ideas", "Projects", "Knowledge")
2. **Datenquellen**: "Welche Dateien/Ordner?" (z.B. "ideas/", "ideas/index.json")
3. **Default Scope**: "Standard-Umfang?" (z.B. "all", "last-30-days", "active-only")
4. **Metriken**: "Welche Metriken berechnen?" (z.B. "Total count, By category, Potential score avg")
5. **Patterns**: "Welche Patterns erkennen?" (z.B. "High-potential ideas", "Underutilized skills")

**Analysis-Steps** (Standard):
1. Scope Definition
2. Data Collection
3. Metrics Calculation
4. Pattern Identification
5. Analysis Synthesis
6. Recommendations Generation
7. Report Generation
8. Output Delivery

## Schritt 5: Placeholders ersetzen

Ersetze alle `{PLACEHOLDERS}` im Template:

### Universal Placeholders:
- `{BRIEF_DESCRIPTION}` → User's Beschreibung
- `{ARGUMENT_DESCRIPTION}` → Argument-Hint
- `{TIMESTAMP}` → Aktuelles Datum

### Workflow-Specific:
- `{ROLE_DESCRIPTION}` → User's Rolle
- `{PRIMARY_TASK_DESCRIPTION}` → Hauptaufgabe
- `{INPUT_NAME}` → Input-Bezeichnung
- `{DATA_SOURCE}` → Datenquelle-Pfad
- `{FILE_PATH}` → Output-Verzeichnis
- `{INDEX_FILE}` → Index-Datei-Pfad
- `{INPUT_GATHERING_STEP}` → "Input Collection"
- `{ANALYSIS_OR_PROCESSING_STEP}` → "Data Processing"
- `{METADATA_GENERATION_STEP}` → "Metadata Generation"
- `{ID_OR_FILENAME_GENERATION}` → "ID Generation"
- `{FILE_CREATION_STEP}` → "File Creation"
- `{INDEX_UPDATE_STEP}` → "Index Update"
- `{CROSS_REFERENCE_STEP}` → "Cross-Referencing"
- `{CONFIRMATION_STEP}` → "Confirmation"
- `{ANALYSIS_DIMENSION_1-4}` → Analyse-Aspekte
- `{FRONTMATTER_FIELD_X}` → Frontmatter-Felder

### Analysis-Specific:
- `{DOMAIN}` → Analyse-Domain
- `{DATA_SOURCE}` → Datenquellen
- `{DEFAULT_SCOPE}` → Standard-Scope
- `{METRIC_1-3}` → Metriken
- `{ANALYSIS_TYPE}` → Analyse-Typ
- `{SCOPE_DEFINITION_STEP}` → "Scope Definition"
- `{DATA_COLLECTION_STEP}` → "Data Collection"
- `{METRICS_CALCULATION_STEP}` → "Metrics Calculation"
- Etc.

**Wichtig**: Alle `{PLACEHOLDERS}` müssen ersetzt werden.

## Schritt 6: Workflow-Patterns Update (Optional)

Frage: "Soll ich ein Auto-Detection Pattern für diesen Command in workflow-patterns.md hinzufügen?"

Falls ja:
1. Frage nach Trigger-Keywords (z.B. für /project-init: "neues projekt", "projekt erstellen")
2. Frage nach Anti-Patterns (was NICHT triggern soll)
3. Bestimme Confidence Level (High: 9-10, Medium: 7-8, Low: 5-6)

**Pattern-Template**:
```markdown
### /{COMMAND_NAME}

**Trigger-Keywords**:
- {KEYWORD_1}
- {KEYWORD_2}
- {KEYWORD_3}

**Pattern-Beispiele**:
```
✓ "{EXAMPLE_1}"
✓ "{EXAMPLE_2}"
```

**Anti-Patterns**:
```
✗ "{ANTI_EXAMPLE_1}"
✗ "{ANTI_EXAMPLE_2}"
```

**Confirmation Template**:
"Ich erkenne dass du {intent}. Soll ich `/{COMMAND_NAME}` nutzen?"
```

## Schritt 7: Validierung

Vor dem Schreiben prüfe:

- [ ] Alle Placeholders ersetzt
- [ ] Frontmatter YAML ist valide
- [ ] Command-Name folgt Konventionen (lowercase-with-hyphens)
- [ ] Datei existiert noch nicht (oder User hat Überschreiben bestätigt)
- [ ] Directory `.claude/commands/` existiert
- [ ] Steps sind logisch geordnet
- [ ] Tool-Usage ist definiert

Falls Datei bereits existiert, frage:
"Der Command `.claude/commands/{name}.md` existiert bereits. Überschreiben? (Y/N)"

## Schritt 8: Dateien erstellen

### Command-Datei erstellen

**Pfad**: `.claude/commands/{name}.md`

Nutze Write-Tool mit vollständig ausgefülltem Template.

### Workflow-Patterns updaten (falls User zugestimmt hat)

Wenn Pattern hinzugefügt werden soll:
1. Read `.claude/workflow-patterns.md`
2. Füge neues Pattern am Ende (vor "## Maintenance") hinzu
3. Edit die Datei mit dem neuen Pattern
4. Update "Last Updated" Datum

## Schritt 9: Bestätigung

Zeige dem User:

```
✓ Command erfolgreich erstellt!

Datei: .claude/commands/{name}.md
Typ: {Workflow|Analysis} Command
Purpose: {BRIEF_DESCRIPTION}

{Falls Pattern hinzugefügt}
Auto-Detection Pattern hinzugefügt zu workflow-patterns.md
Trigger-Keywords: {LIST}

Nächste Schritte:
→ Teste mit: /{name} {example-argument}
→ {SPECIFIC_NEXT_STEP_1}
→ {SPECIFIC_NEXT_STEP_2}

Related: {RELATED_COMMANDS}
```

**Beispiel**:
```
✓ Command erfolgreich erstellt!

Datei: .claude/commands/project-init.md
Typ: Workflow Command
Purpose: Initialisiert neue Projekte mit Standardstruktur

Auto-Detection Pattern hinzugefügt zu workflow-patterns.md
Trigger-Keywords: "neues projekt", "projekt erstellen", "initialize project"

Nächste Schritte:
→ Teste mit: /project-init my-new-project
→ Passe Directory-Struktur an falls nötig
→ Erweitere Validation-Logic in Step 1

Related: /project-add (für bestehende Projekte)
```

---

## Tool Usage

**Required Tools**:
- `Read`: Template einlesen, workflow-patterns lesen
- `Write`: Command-Datei erstellen
- `Edit`: workflow-patterns updaten (optional)
- `Grep/Glob`: Prüfen ob Command existiert

**Tool Pattern**:
```
1. Read template file
2. Replace all placeholders
3. Validate output
4. Write command file
5. (Optional) Read workflow-patterns
6. (Optional) Edit workflow-patterns
7. Confirm to user
```

---

## Error Handling

### Template nicht gefunden

```
IF template_not_found:
  Liste verfügbare Templates
  Frage User welcher Template
  Retry mit korrektem Pfad
```

### Command existiert bereits

```
IF command_exists:
  Frage: "Command existiert bereits. Überschreiben? (Y/N)"
  IF no: Frage nach alternativem Namen
  IF yes: Backup erstellen (optional), dann überschreiben
```

### Ungültiger Name

```
IF name_invalid:
  Erkläre Naming-Konventionen
  Gib Beispiele
  Frage nach korrektem Namen
```

### Workflow-Patterns Update fehlschlägt

```
IF pattern_update_fails:
  Warne User
  Command wurde trotzdem erstellt
  User kann Pattern manuell hinzufügen
  Gib Anleitung
```

---

## Validation Checklist

Vor Bestätigung prüfe:

- [ ] Template erfolgreich gelesen
- [ ] Alle User-Inputs erhalten
- [ ] Alle Placeholders ersetzt
- [ ] Frontmatter valide (YAML korrekt)
- [ ] Command-Name valide
- [ ] Steps logisch und vollständig
- [ ] Tool-Usage definiert
- [ ] Error-Handling vorhanden
- [ ] Keine Konflikte mit bestehenden Commands
- [ ] User erhält klare Next Steps

---

## Best Practices

**Do's**:
- Folge Naming-Konventionen strikt
- Frage nur nach essentiellen Infos
- Generiere sinnvolle Defaults
- Validiere vor dem Schreiben
- Biete Auto-Detection Pattern an
- Gib konkrete Beispiele

**Don'ts**:
- Erstelle keinen Command ohne User-Bestätigung
- Lasse keine Placeholders im Output
- Verwende keine generischen Namen
- Überspringe keine Validation-Steps
- Vergiss nicht Tool-Usage zu definieren

---

## Examples

### Workflow Command Beispiel

```
User: /create-command project-init

Typ: Workflow
Beschreibung: "Initialisiert neue Projekte mit Standardstruktur"
Argument: "optional: projekt-name"
Input: Projektname, Typ (web/cli/library), Beschreibung
Datenquelle: projects/
Index: projects/index.json

→ Erstellt: .claude/commands/project-init.md
→ Pattern: "neues projekt", "projekt erstellen"
```

### Analysis Command Beispiel

```
User: /create-command idea-stats

Typ: Analysis
Analyse-Typ: Ideas
Datenquellen: ideas/, ideas/index.json
Metriken: Total, By Category, Avg Potential, Status Distribution
Patterns: High-potential ideas, Underutilized skills

→ Erstellt: .claude/commands/idea-stats.md
→ Pattern: "ideen statistik", "analyse ideen"
```

---

## Related Commands

- `/create-agent` - Agent erstellen
- `/create-hook` - Hook erstellen
- `/create-skill` - Skill erstellen

**Template-Creator Skill**: Dieser Command kann auch durch den `template-creator` Skill getriggert werden.

---

**Wichtig**:
- Nutze Read/Write/Edit Tools korrekt
- Erstelle commands/ Directory falls nötig
- Präzises Placeholder-Replacement
- Validiere gründlich
- Biete Pattern-Integration an
