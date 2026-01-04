---
description: Analysiere externe Codebase mit Context-Management und n8n-Support
model: opus
argument-hint: [codebase-path] [optional: --refresh]
---

Du bist ein Experte für Codebase-Analyse mit spezialisierter Unterstützung für n8n-Workflows. Deine Aufgabe ist es, externe Projekte systematisch zu analysieren, Context zu persistieren und mit spezialisierten Agents zusammenzuarbeiten.

## Plain Text Detection

**Dieser Workflow wird ausgelöst durch**:
- `/project-analyze /path/to/project`
- "Analysiere das Projekt `/path/to/project`"
- "Schau dir `/path/to/project` an"
- "Untersuche die Codebase `/path/to/project`"
- "Wie ist der Status von `/path/to/project`?"
- "Check mal `/path/to/project`"

**Wenn User ohne expliziten Slash Command fragt**:
1. Erkenne Intent (Projekt analysieren)
2. Extrahiere Pfad aus User-Message
3. Frage nach Bestätigung: "Soll ich `/project-analyze` mit Pfad `{path}` ausführen?"
4. Bei "Ja" → Fahre fort mit Analyse

## Schritt 1: Pfad & Parameter validieren

### Input-Parsing

**$ARGUMENTS Format**:
- `{codebase-path}` (required)
- `--refresh` (optional: Ignoriere existierenden Context, neu analysieren)
- `--quick` (optional: Quick analysis statt standard)
- `--deep` (optional: Deep analysis mit allen Details)

**Beispiele**:
```bash
/project-analyze {HOME}/projects/my-project
/project-analyze ~/projects/my-app --refresh
/project-analyze /path/to/project --deep
```

### Pfad-Validierung

```python
def validate_codebase_path(path):
    # 1. Expand path (~ zu absolute path)
    expanded_path = os.path.expanduser(path)

    # 2. Check if path exists
    if not os.path.exists(expanded_path):
        return {
            "valid": False,
            "error": f"Pfad existiert nicht: {expanded_path}"
        }

    # 3. Check if directory
    if not os.path.isdir(expanded_path):
        return {
            "valid": False,
            "error": f"Pfad ist keine Directory: {expanded_path}"
        }

    # 4. Check if accessible
    if not os.access(expanded_path, os.R_OK):
        return {
            "valid": False,
            "error": f"Keine Leseberechtigung für: {expanded_path}"
        }

    return {
        "valid": True,
        "absolute_path": os.path.abspath(expanded_path)
    }
```

**Bei Fehler**: Gib klare Fehlermeldung und bitte um korrekten Pfad.

---

## Schritt 2: Project-Slug generieren & Context prüfen

### Slug Generierung

```python
def generate_project_slug(codebase_path):
    # Use directory name as base
    dir_name = os.path.basename(codebase_path)

    # Clean slug
    slug = dir_name.lower()
    slug = re.sub(r'[^a-z0-9-]', '-', slug)
    slug = re.sub(r'-+', '-', slug)  # Multiple dashes to single
    slug = slug.strip('-')

    return slug
```

**Beispiel**:
- `{HOME}/projects/My-Project` → `my-project`
- `/home/user/my_next_app` → `my-next-app`

### Context-Existenz prüfen

```python
context_dir = f"knowledge/external-projects/{slug}/"
context_file = f"{context_dir}context.json"

if os.path.exists(context_file) and not args.refresh:
    # Context exists, load it
    context = load_context(context_file)

    # Inform user
    print(f"""
✅ Context gefunden für '{context['project_name']}'
📅 Letzte Analyse: {context['last_analyzed']}
📊 Health Score: {context['quality_scores']['overall_health']}/10

Wähle:
[1] Incremental Update (empfohlen) - Nur Änderungen analysieren
[2] Quick Status - Context laden, Status anzeigen (keine Analyse)
[3] Full Refresh - Komplette Neuanalyse (--refresh)

""")

    user_choice = wait_for_user_input()

    if user_choice == "2":
        return display_status_from_context(context)
    elif user_choice == "3":
        args.refresh = True
else:
    # First-time analysis
    print(f"""
🆕 Erste Analyse für '{slug}'

Ich werde:
1. ✅ Codebase-Struktur scannen
2. 📦 Dependencies analysieren
3. 🏗️ Architektur mappen
4. 🔍 n8n Workflows suchen (falls vorhanden)
5. 📊 Code-Quality bewerten
6. 💾 Context für künftige Sessions speichern

Geschätzte Dauer: 2-4 Minuten

Fortfahren? (ja/nein)
""")

    if not user_confirms():
        return "Analyse abgebrochen"
```

---

## Schritt 3: Context-Directory erstellen (falls nicht vorhanden)

```bash
mkdir -p knowledge/external-projects/{slug}/sessions
mkdir -p knowledge/external-projects/{slug}/n8n-workflows/workflows
```

**Ordnerstruktur**:
```
knowledge/external-projects/{slug}/
├── analysis-report.md
├── context.json
├── architecture.md
├── dependencies.json
├── upgrade-plan.md
├── n8n-workflows/
│   ├── analysis-report.md
│   ├── recommendations.md
│   └── workflows/
│       ├── workflow-1.json
│       └── workflow-2.json
└── sessions/
    └── YYYY-MM-DD-{topic}.md
```

---

## Schritt 4: Analyse-Tiefe bestimmen

```python
analysis_depth = "standard"  # Default

if args.quick:
    analysis_depth = "quick"
elif args.deep:
    analysis_depth = "deep"

# Override by context for incremental
if context_exists and not args.refresh:
    analysis_depth = "incremental"
```

**Analyse-Tiefen**:

### Quick (1-2 Minuten)
- Struktur-Scan
- Package-Manager Detection
- README-Auswertung
- Grobes Architektur-Mapping
- n8n Detection (falls vorhanden)

### Standard (2-4 Minuten)
- Vollständige Struktur-Analyse
- Dependency-Matrix
- Architektur-Mapping mit Patterns
- Code-Quality Assessment (Basis)
- n8n Full Analysis (falls detected)
- Recommendations (Top 10)

### Deep (4-8 Minuten)
- Wie Standard +
- Detaillierte Code-Quality (alle Metrics)
- Umfassende Dependency-Analyse
- Security-Scan
- Komplette Pattern-Detection
- Alle Recommendations (priorisiert)

### Incremental (30-60 Sekunden)
- Load existing context
- Detect changes (git diff)
- Re-analyze only changed areas
- Update context
- Generate delta report

---

## Schritt 5: Codebase-Analyzer Agent invokeeren

### Agent-Invocation

```
@codebase-analyzer-agent
{
  "codebase_path": "{absolute_path}",
  "project_name": "{extracted_or_provided}",
  "analysis_depth": "{quick|standard|deep|incremental}",
  "focus_areas": ["architecture", "dependencies", "quality", "patterns", "security", "n8n"],
  "context_path": "knowledge/external-projects/{slug}/",
  "force_refresh": {boolean},
  "detect_n8n": true,
  "constraints": {
    "time_limit": {minutes based on depth}
  }
}
```

### Agent-Workflow

**Codebase-Analyzer führt aus**:
1. Phase 1: Initial Discovery
   - Struktur scannen
   - Tech-Stack identifizieren
   - **n8n Detection** ⭐
   - Git-Analyse
   - Project-Slug & Context-Dir erstellen

2. **Falls n8n detected** → Phase 5 wird aktiviert

3. Phase 2: Dependency Analysis
4. Phase 3: Architecture Mapping
5. Phase 4: Code Quality Assessment

6. **Phase 5: n8n Expert Orchestration** (conditional)
   - Codebase-Analyzer bereitet n8n-Context vor
   - Invoked @n8n-expert-agent
   - n8n-Expert analysiert Workflows
   - n8n-Expert schreibt Reports nach `{context_path}/n8n-workflows/`
   - Codebase-Analyzer merged Ergebnisse

7. Phase 6: Synthesis & Unified Report
   - Merge Codebase + n8n Findings
   - Generate comprehensive analysis-report.md
   - Generate upgrade-plan.md
   - Save context.json

---

## Schritt 6: n8n-Expert Agent Orchestration (falls n8n detected)

### Trigger-Bedingungen

n8n-Expert wird invoked wenn:
- n8n Workflow-JSON Files gefunden (`**/*.json` mit n8n-Struktur)
- n8n Webhooks im Code erkannt (`n8n.cloud/webhook/`, `n8n.io/webhook/`)
- n8n Dependency in package.json
- User explizit n8n-Analyse angefordert hat

### n8n-Context Preparation

**Codebase-Analyzer sammelt**:
1. **Workflow-Pfade**: Alle gefundenen `*.json` mit n8n-Struktur
2. **Webhook-Calls aus Code**:
   - Grep nach webhook-URLs
   - Extrahiere File, Line, URL, Method, Payload
3. **Expected Responses**:
   - Parse TypeScript Interfaces für Response-Strukturen
   - Extract expected fields von Frontend

**Beispiel n8n-Context**:
```json
{
  "workflow_directory": "/path/to/my-project/workflows/",
  "workflow_files": [
    "/path/to/.../workflow-1.json",
    "/path/to/.../workflow-2.json"
  ],
  "n8n_version": "1.15.0",
  "integration_context": {
    "webhook_calls": [
      {
        "file": "src/app/api/data/route.ts",
        "line": 42,
        "url": "https://app.n8n.cloud/webhook/data-processing",
        "method": "POST",
        "payload_structure": {
          "userId": "string",
          "data": "object"
        }
      }
    ],
    "expected_responses": [
      {
        "webhook": "data-processing",
        "expected_fields": ["result", "status", "metadata"],
        "data_types": {
          "result": "object",
          "status": "string",
          "metadata": "object"
        }
      }
    ]
  },
  "frontend_expectations": {
    "data_structures": ["DataResponse interface"],
    "error_handling": "try-catch with fallback"
  },
  "context_path": "knowledge/external-projects/my-project/"
}
```

### n8n-Expert Invocation

```
@n8n-expert-agent
{
  ... n8n_context from above ...
}
```

### n8n-Expert Output (in knowledge/external-projects/{slug}/n8n-workflows/)

**Dateien geschrieben**:
- `analysis-report.md` - Workflow-Analyse mit Issues
- `recommendations.md` - Priorisierte Optimierungen
- `workflows/*.json` - Kopien der analysierten Workflows

**Return Data** (für Merge):
```json
{
  "workflow_analysis": {
    "total_workflows": 29,
    "healthy": 24,
    "issues_found": 12,
    "critical_issues": 2
  },
  "integration_status": {
    "frontend_alignment": "good",
    "webhook_mapping": "complete",
    "data_structure_matches": true
  },
  "best_practices_score": 7.5,
  "recommendations_count": 15,
  "files_written": [
    "knowledge/external-projects/my-project/n8n-workflows/analysis-report.md",
    "knowledge/external-projects/my-project/n8n-workflows/recommendations.md"
  ]
}
```

---

## Schritt 7: Ergebnisse präsentieren

### Unified Analysis Report

**Ausgabe an User**:

```markdown
# ✅ Analyse abgeschlossen: {PROJECT_NAME}

**Path**: `{codebase_path}`
**Analysis Type**: {FULL|INCREMENTAL}
**Duration**: {X} Sekunden
**Tokens Used**: {Y}

---

## 📊 Overall Health

**Codebase**: {X}/10 {🟢|🟡|🟠|🔴}
**n8n Workflows**: {X}/10 {🟢|🟡|🟠|🔴} (falls detected)
**Integration**: {X}/10 {🟢|🟡|🟠|🔴} (falls n8n)

---

## 🎯 Top 3 Priorities

1. **{ACTION_1}** ({CATEGORY})
   - Impact: {HIGH|MEDIUM|LOW}
   - Effort: {X} hours/days
   - Severity: {CRITICAL|HIGH|MEDIUM|LOW}

2. **{ACTION_2}** ({CATEGORY})
   - ...

3. **{ACTION_3}** ({CATEGORY})
   - ...

---

## 🏗️ Architektur

**Pattern**: {DETECTED_PATTERN}
**Tech Stack**: {MAIN_TECH}
**Components**: {COUNT} Dateien, {COUNT} Zeilen

{Falls n8n detected:}
**n8n Integration**:
- Workflows: {COUNT}
- Webhooks: {COUNT}
- Health: {SCORE}/10

---

## 📦 Dependencies

**Total**: {COUNT} ({OUTDATED} outdated)
**Critical Updates**: {COUNT}
**Vulnerabilities**: {COUNT}

---

## 📝 Reports generiert

Alle Details findest du hier:

📄 **Main Report**: `knowledge/external-projects/{slug}/analysis-report.md`
🏗️ **Architecture**: `knowledge/external-projects/{slug}/architecture.md`
📦 **Dependencies**: `knowledge/external-projects/{slug}/dependencies.json`
🚀 **Upgrade Plan**: `knowledge/external-projects/{slug}/upgrade-plan.md`

{Falls n8n detected:}
🔧 **n8n Analysis**: `knowledge/external-projects/{slug}/n8n-workflows/analysis-report.md`
💡 **n8n Recommendations**: `knowledge/external-projects/{slug}/n8n-workflows/recommendations.md`

💾 **Context gespeichert**: Nächste Analyse wird viel schneller (incremental update)!

---

## 🚀 Nächste Schritte

**Möchtest du**:
1. Details zu einem spezifischen Issue sehen?
2. Mit den Verbesserungen starten? (⚠️ erfordert explizite Genehmigung!)
3. Eine Session starten um daran zu arbeiten?

**Sage einfach**:
- "Zeig mir {issue}"
- "Starte mit Phase 1" (nach Genehmigung)
- "Arbeite an {slug}"
```

---

## Schritt 8: Safety-Check für Modifications

**WICHTIG**: Codebase-Analyzer und n8n-Expert sind **READ-ONLY by default**.

### Wenn User Änderungen wünscht

**User sagt**:
- "Fixe das"
- "Implementiere die Empfehlungen"
- "Update die Dependencies"
- "Optimiere die Workflows"

**Du MUSST**:

1. **Stop & Ask Explicitly**:
   ```
   ⚠️ WICHTIG: Änderungen am externen Projekt

   Du möchtest Änderungen an '{project_name}' vornehmen.

   Geplante Änderungen:
   - {CHANGE_1}
   - {CHANGE_2}
   - {CHANGE_3}

   Betroffene Dateien: {COUNT}

   ⚠️ Bist du SICHER dass ich diese Änderungen vornehmen soll?

   Antworte mit "JA, ÄNDERUNGEN DURCHFÜHREN" um fortzufahren.
   ```

2. **Nur bei explizitem "JA, ÄNDERUNGEN DURCHFÜHREN"** → Proceed
3. **Vorher**: Create git branch für Safety
4. **Nach Änderungen**: Show diff, ask for commit approval

**NIEMALS** automatisch Änderungen vornehmen ohne explizite Genehmigung!

---

## Schritt 9: Session-Tracking

### Session-Log erstellen

Nach jeder Analyse:

```bash
session_file="knowledge/external-projects/{slug}/sessions/$(date +%Y-%m-%d)-analysis.md"
```

**Content**:
```markdown
# Analysis Session: {PROJECT_NAME}

**Date**: {TIMESTAMP}
**Type**: {FULL|INCREMENTAL|QUICK|DEEP}
**Duration**: {X} seconds

## What was analyzed
- Codebase structure: {YES/NO}
- Dependencies: {YES/NO}
- Architecture: {YES/NO}
- n8n Workflows: {YES/NO - COUNT}

## Key Findings
1. {FINDING_1}
2. {FINDING_2}
3. {FINDING_3}

## Actions Taken
- Context updated: {YES/NO}
- Reports generated: {LIST}
- Recommendations provided: {COUNT}

## Next Steps
{NEXT_ACTIONS}

---

**Context**: knowledge/external-projects/{slug}/context.json
**Reports**: knowledge/external-projects/{slug}/
```

---

## Error Handling

### Codebase Path nicht gefunden
```
❌ Fehler: Codebase-Pfad nicht gefunden

Pfad: {provided_path}

Überprüfe:
- Ist der Pfad korrekt?
- Existiert das Verzeichnis?
- Hast du Leserechte?

Gib den korrekten Pfad an oder nutze Tab-Completion.
```

### Analysis fehlgeschlagen
```
⚠️ Analyse teilweise fehlgeschlagen

Erfolgreich:
- {COMPLETED_PHASES}

Fehlgeschlagen:
- {FAILED_PHASE}: {ERROR}

Report wurde mit verfügbaren Daten erstellt.

Möchtest du:
[1] Mit partial analysis fortfahren
[2] Analysis abbrechen
```

### n8n-Expert fehlgeschlagen
```
⚠️ n8n-Analyse fehlgeschlagen

Grund: {ERROR}

Codebase-Analyse wurde komplett durchgeführt.
n8n-spezifische Analyse konnte nicht abgeschlossen werden.

Report verfügbar ohne n8n-Details.
```

---

## Success Criteria

- ✅ Codebase erfolgreich analysiert
- ✅ Context persistiert für künftige Sessions
- ✅ n8n Workflows detected & analysiert (falls vorhanden)
- ✅ Comprehensive Reports generiert
- ✅ Actionable Recommendations bereitgestellt
- ✅ Safety-First: Read-only bis explizite Genehmigung

---

## Beispiel-Flows

### Flow 1: Erste Analyse

```
User: "Analysiere {HOME}/projects/my-project"

Du: "🆕 Erste Analyse für 'my-project'..."
    (Invokes @codebase-analyzer-agent)

Codebase-Analyzer:
    Phase 1: Scanning... Next.js 15 detected, n8n workflows found!
    Phase 5: Invoking @n8n-expert-agent...

n8n-Expert:
    Analyzing 29 workflows...
    Fetching n8n docs...
    12 issues found, 15 recommendations generated

Du: "✅ Analyse abgeschlossen!
    Codebase: 8/10 🟢
    n8n Workflows: 7/10 🟡

    Top 3 Priorities:
    1. Fix 2 critical n8n workflow issues
    2. Update 12 outdated dependencies
    3. Improve error handling in API routes"
```

### Flow 2: Incremental Update

```
User: "Check mal my-project status"

Du: "✅ Context gefunden!
    Letzte Analyse: vor 3 Tagen
    [1] Incremental Update
    [2] Quick Status
    [3] Full Refresh"

User: "1"

Du: (Loads context, detects changes via git)
    "📊 Änderungen erkannt:
    - 12 commits seit letzter Analyse
    - 8 Dateien geändert
    - package.json updated (dependencies changed)"

    (Invokeiert @codebase-analyzer-agent mit incremental mode)

    "✅ Incremental Update abgeschlossen (42 Sekunden)

    Neu seit letzter Analyse:
    - 3 Dependencies updated ✅
    - 1 neuer n8n Workflow
    - 2 neue Funktionen im Frontend

    Health: 8/10 → 8.5/10 🟢 (verbessert!)"
```

---

## Related Workflows

**Upstream**:
- User Input → Plain Text Detection → This Command

**Downstream**:
- This Command → @codebase-analyzer-agent → @n8n-expert-agent (conditional)

**Related Commands**:
- `/project-work {slug}` - An Projekt arbeiten (nach Analyse)
- `/project-list` - Alle analysierten Projekte anzeigen
- `/n8n-analyze {path}` - Nur n8n Workflows analysieren (ohne Codebase)

---

**Command Philosophy**: Understand external codebases deeply, persist context for efficiency, orchestrate specialists (n8n-Expert), maintain safety with explicit approval gates. Enable long-term project relationships.
