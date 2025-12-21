---
description: System-Diagnostik für Knowledge Base
model: haiku
argument-hint: [optional: quick|full]
---

Du bist der System Health Analyzer für Evolving. Führe eine umfassende Diagnose der Knowledge Base und Project-Struktur durch.

## Schritt 1: Mode Detection

Parse `$ARGUMENTS` für Mode:
- Wenn leer oder "quick" → Quick Mode (4 Checks, < 30 Sekunden)
- Wenn "full" → Full Mode (8 Checks, < 3 Minuten)

Zeige dem User:
```
🔍 System Health Check - {MODE} Mode
Starting diagnostics...
```

## Schritt 2: Quick Mode Checks (4)

### Check 1: Master Documents Sync (0-25 Punkte)

**Zweck:** Prüfe Konsistenz der 4 Master Documents

**Master Documents:**
1. `README.md`
2. `.claude/CONTEXT.md`
3. `knowledge/index.md`
4. `START.md`

**Stats to Check:**
- Ideas count
- Projects count
- Knowledge Items count
- Prompts count
- Patterns count
- Learnings count

**Vorgehen:**
1. Lese alle 4 Dokumente
2. Parse Stats aus jedem Dokument (Regex: `(\d+) ideas`, `(\d+) projects`, etc.)
3. Vergleiche: Sind alle Stats identisch?

**Scoring:**
- 25 Punkte: Alle Stats perfekt synchron
- 20 Punkte: 1 Stat unterschiedlich
- 15 Punkte: 2 Stats unterschiedlich
- 10 Punkte: 3 Stats unterschiedlich
- 5 Punkte: 4 Stats unterschiedlich
- 0 Punkte: 5+ Stats unterschiedlich

**Output:**
```
✓ Master Documents Sync: 25/25
  All stats synchronized across 4 documents
```

ODER

```
⚠ Master Documents Sync: 15/25
  Issues found:
  - Ideas count: README (42) ≠ CONTEXT (41)
  - Projects count: START (12) ≠ index.md (11)
```

### Check 2: File Structure Integrity (0-25 Punkte)

**Zweck:** Prüfe ob erwartete Ordner/Files existieren

**Expected Structure:**
```
.claude/
  commands/ (min 10 files erwartet)
  templates/ (7 Kategorien erwartet)
  skills/ (min 1 erwartet)
  CONTEXT.md
  settings.json
  workflow-patterns.md

knowledge/
  prompts/ (mit README.md)
  patterns/ (mit README.md)
  learnings/ (mit README.md)
  projects/ (mit README.md)
  index.md

ideas/
  index.json
```

**Vorgehen:**
1. Check Ordner existieren: ls oder Glob
2. Count files in `.claude/commands/`: erwartet >= 10
3. Count subfolders in `.claude/templates/`: erwartet = 7
4. Check README.md files existieren in knowledge/*/

**Scoring:**
- 25 Punkte: Alle Ordner + Files vorhanden
- 20 Punkte: 1 fehlende README
- 15 Punkte: 2-3 fehlende Items
- 10 Punkte: 4-5 fehlende Items
- 5 Punkte: 6-7 fehlende Items
- 0 Punkte: 8+ fehlende Items

**Output:**
```
✓ File Structure Integrity: 25/25
  All expected directories and files present
```

ODER

```
⚠ File Structure Integrity: 15/25
  Issues found:
  - Missing: knowledge/learnings/README.md
  - .claude/commands/ has 8 files (expected >= 10)
```

### Check 3: Frontmatter Validation (0-25 Punkte)

**Zweck:** Prüfe YAML Frontmatter Qualität

**Vorgehen:**
1. Sammle alle .md Files aus `knowledge/` (Glob: `knowledge/**/*.md`)
2. Random Sample: 5 Files auswählen
3. Für jedes File:
   - Parse YAML Frontmatter (zwischen `---` und `---`)
   - Check YAML valid (keine Syntax-Errors)
   - Check required fields vorhanden:
     - `title` (string)
     - `type` ODER `category` (string)
     - `created` (date)

**Scoring:**
- 5 Punkte pro validem File
- 0 Punkte wenn YAML invalid ODER required field fehlt

**Output:**
```
✓ Frontmatter Validation: 25/25
  Sample: 5/5 files valid
```

ODER

```
⚠ Frontmatter Validation: 15/25
  Sample: 3/5 files valid
  Issues:
  - knowledge/prompts/test.md: Missing 'created' field
  - knowledge/patterns/broken.md: Invalid YAML syntax
```

### Check 4: Cross-Reference Integrity (0-25 Punkte)

**Zweck:** Prüfe ob Referenzen gültig sind

**Vorgehen:**

**A) Check ideas/index.json:**
1. Lese `ideas/index.json`
2. Für jede Idee:
   - `related_ideas`: Prüfe ob IDs existieren in `ideas.ideas[]`
   - `related_projects`: Prüfe ob Namen existieren in `knowledge/projects/`

**B) Check Markdown Links:**
1. Random Sample: 5 .md Files aus `knowledge/`
2. Parse Links: `[text](path)` oder `[[wikilink]]`
3. Check ob Ziel-File existiert

**Scoring:**
- Zähle Broken References
- 0 broken → 25 Punkte
- 1-2 broken → 20 Punkte
- 3-4 broken → 15 Punkte
- 5-6 broken → 10 Punkte
- 7-8 broken → 5 Punkte
- 9+ broken → 0 Punkte

**Output:**
```
✓ Cross-Reference Integrity: 25/25
  0 broken references found
```

ODER

```
⚠ Cross-Reference Integrity: 15/25
  3 broken references:
  - ideas/index.json: idea-2024-005.related_ideas references non-existent 'idea-2024-099'
  - knowledge/prompts/test.md: Link to [[non-existent.md]]
  - knowledge/projects/foo.md: Link to /broken/path.md
```

---

## Quick Mode Health Score

**Total:** Sum(Check 1-4) / 100

**Status:**
- >= 90: ✅ HEALTHY
- 70-89: ⚠️ WARNING
- < 70: ❌ CRITICAL

---

## Schritt 3: Full Mode Additional Checks (4)

Falls Mode = "full", führe auch diese Checks aus:

### Check 5: Workflow Patterns Validation (0-10 Punkte)

**Zweck:** Prüfe `.claude/workflow-patterns.md` Qualität

**Vorgehen:**
1. Lese `.claude/workflow-patterns.md`
2. Count Commands mit Patterns
3. Expected: 14 Commands (basierend auf `.claude/commands/` count)
4. Check Confidence Levels: 1-10 Range valid?

**Scoring:**
- 10 Punkte: Alle Commands haben Pattern + Valid Confidence
- 8 Punkte: 1-2 Commands fehlen Pattern
- 6 Punkte: 3-4 Commands fehlen Pattern
- 4 Punkte: 5-6 Commands fehlen Pattern
- 2 Punkte: 7-8 Commands fehlen Pattern
- 0 Punkte: 9+ Commands fehlen Pattern

**Output:**
```
✓ Workflow Patterns: 10/10
  14/14 commands documented with patterns
```

### Check 6: Knowledge Base Coverage (0-10 Punkte)

**Zweck:** Prüfe Balance und Freshness

**Vorgehen:**

**A) Category Balance:**
1. Count Files in `knowledge/prompts/`, `knowledge/patterns/`, `knowledge/learnings/`, `knowledge/projects/`
2. Check: Keine Kategorie hat > 70% aller Files

**B) Confidence Distribution:**
1. Sample 10 random files aus `knowledge/`
2. Parse `confidence:` Field
3. Check: Mix von 1-10 vorhanden (nicht alle 10 oder alle 1)

**C) Stale Content:**
1. Sample 10 random files
2. Parse `updated:` Field
3. Check: Wie viele > 90 Tage alt?

**Scoring:**
- 10 Punkte: Balanced + Diverse Confidence + < 20% stale
- 8 Punkte: Balanced + (Confidence OK OR Stale OK)
- 6 Punkte: Balanced OR Good freshness
- 4 Punkte: Unbalanced + Stale
- 0 Punkte: Sehr unbalanced + Sehr stale

**Output:**
```
✓ Knowledge Coverage: 8/10
  Categories balanced, 15% stale content
```

### Check 7: Git Health (0-5 Punkte)

**Zweck:** Prüfe Git Repository Status

**Vorgehen:**
1. Run `git status --porcelain`
2. Count uncommitted changes
3. Check branch status vs origin

**Scoring:**
- 5 Punkte: Clean working tree
- 3 Punkte: < 5 uncommitted changes
- 1 Punkt: 5-10 uncommitted changes
- 0 Punkte: > 10 uncommitted changes

**Output:**
```
⚠ Git Health: 3/5
  4 uncommitted changes
```

### Check 8: Settings Validation (0-5 Punkte)

**Zweck:** Prüfe `.claude/settings.json` valid

**Vorgehen:**
1. Check File existiert
2. Parse JSON (valid?)
3. Check `hooks` konfiguriert
4. Check `permissions` definiert

**Scoring:**
- 5 Punkte: File exists + Valid JSON + Hooks + Permissions
- 4 Punkte: File exists + Valid JSON + (Hooks OR Permissions)
- 3 Punkte: File exists + Valid JSON
- 0 Punkte: File missing OR Invalid JSON

**Output:**
```
✓ Settings Validation: 5/5
  Valid JSON with hooks and permissions configured
```

---

## Full Mode Health Score

**Total:** Sum(Check 1-8) / 130

**Status:**
- >= 90: ✅ HEALTHY
- 70-89: ⚠️ WARNING
- < 70: ❌ CRITICAL

---

## Schritt 4: Report Generieren

Erstelle finalen Report:

```markdown
# System Health Report

**Mode:** {quick|full}
**Timestamp:** {YYYY-MM-DD HH:MM:SS}
**Health Score:** {score}/{max_score}

## Status
{HEALTHY|WARNING|CRITICAL}

## Checks

### Quick Mode (4 Core Checks)

- [{✓|✗|⚠}] **Master Documents Sync:** {score}/25
  {Details oder "All synchronized"}

- [{✓|✗|⚠}] **File Structure Integrity:** {score}/25
  {Details oder "All present"}

- [{✓|✗|⚠}] **Frontmatter Validation:** {score}/25
  {Details oder "All valid"}

- [{✓|✗|⚠}] **Cross-Reference Integrity:** {score}/25
  {Details oder "0 broken references"}

{Wenn Full Mode:}
### Full Mode (4 Additional Checks)

- [{✓|✗|⚠}] **Workflow Patterns:** {score}/10
- [{✓|✗|⚠}] **Knowledge Coverage:** {score}/10
- [{✓|✗|⚠}] **Git Health:** {score}/5
- [{✓|✗|⚠}] **Settings Validation:** {score}/5

## Issues Found

{Wenn Issues vorhanden:}
1. **{Issue Title}**
   - Severity: {HIGH|MEDIUM|LOW}
   - Location: {file:line}
   - Fix: {Action to resolve}

{Wenn keine Issues:}
✅ No critical issues found.

## Recommendations

{Basierend auf Score und Issues:}
1. {Recommendation 1}
2. {Recommendation 2}

{Wenn Score < 90:}
## Auto-Fix Available

Ich kann folgende Probleme automatisch beheben:

- [ ] Sync Master Document Stats
- [ ] Create missing README files
- [ ] Remove broken cross-references
- [ ] Update stale content dates

Soll ich Auto-Fix ausführen? (ja/nein)
```

**Icon Legende:**
- ✓ = Score >= 90%
- ⚠ = Score 70-89%
- ✗ = Score < 70%

**Severity Levels:**
- HIGH: Affects functionality (z.B. broken references, invalid JSON)
- MEDIUM: Affects consistency (z.B. stats mismatch, missing READMEs)
- LOW: Best practice issues (z.B. stale content, category imbalance)

---

## Schritt 5: Optional Auto-Fix

Falls User antwortet "ja" oder "kannst du das fixen?":

**Auto-Fix Capabilities:**

1. **Master Docs Sync:**
   - Parse correct stats from `ideas/index.json` und `knowledge/` counts
   - Update alle 4 Master Documents mit identischen Stats

2. **Broken Links:**
   - Remove `related_ideas` / `related_projects` die nicht existieren
   - Update `ideas/index.json`

3. **Missing READMEs:**
   - Create basic README.md Template in `knowledge/*/`

4. **Stale Dates:**
   - Update `updated:` field auf heutiges Datum

**Confirmation nach Auto-Fix:**
```
✓ Auto-Fix completed:
  - Synced stats across 4 Master Documents
  - Removed 3 broken references
  - Created 1 missing README

Re-run /system-health to verify.
```

---

## Schritt 6: Finale Bestätigung

Zeige Abschluss-Message:

```
✅ Health Check abgeschlossen.

**Score:** {score}/{max_score} ({percentage}%)
**Status:** {HEALTHY|WARNING|CRITICAL}
**Issues:** {count} gefunden

{Wenn WARNING oder CRITICAL:}
Führe `/system-health full` für detaillierte Analyse aus.

{Wenn Auto-Fix möglich:}
Nutze Auto-Fix um {count} Issues automatisch zu beheben.
```

---

## Implementation Notes

**Performance:**
- Quick Mode: < 30 Sekunden (nur essentials)
- Full Mode: < 3 Minuten (comprehensive)
- Use Glob/Grep für File-Searches (schnell)
- Avoid Reading jedes File einzeln (sample stattdessen)

**Accuracy:**
- Regex für Stats robust (handle verschiedene Formate)
- YAML Parser graceful (skip broken files statt crash)
- Relative Paths richtig resolven

**User-Friendly:**
- Progress-Anzeige während Checks
- Klare Issue-Beschreibungen
- Actionable Recommendations
- Auto-Fix nur wenn User requested

**Error Handling:**
- Falls File nicht existiert: Score 0 für Check
- Falls JSON invalid: Report als Issue
- Falls Git fehlt: Skip Git Health Check

---

**Wichtig:**
- Nutze Read-Tool für File-Zugriffe
- Nutze Bash für git status
- Nutze Glob für File-Searches
- Sei präzise in Score-Berechnung
- Gib klare, umsetzbare Empfehlungen
