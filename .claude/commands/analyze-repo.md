---
description: 5-Phasen Repository-Analyse mit Rel-Extraktion + Tpl-Abstraktion
model: opus
argument-hint: [GitHub-URL]
---

## Plain Text Trigger (PFLICHT!)

**Natürliche Sprache funktioniert:**
- "Analysiere dieses Repo: {url}"
- "Schau dir mal {url} an"
- "Was können wir von {url} lernen?"
- "Check das Repo {url}"
- "Deep Dive auf {url}"
- "Untersuche {url}"
- "Ist {url} relevant für uns?"

---

## 5-Phasen Architektur

```
P1: Relevanz-Check (Remote)
├── README.md via WebFetch
├── Struktur via GitHub Page
├── Relevanz-Score (0-10)
└── Output: RELEVANT / NICHT RELEVANT
     │
     ▼ (Wenn RELEVANT + User OK)
P2: Deep Dive (Local Clone)
├── git clone → /tmp/{repo}
├── Glob/Read/Grep auf echtem Code
├── Funktionssignaturen extrahieren
└── Mapping gegen Evolving
     │
     ▼
P3: REL-EXTRAKTION (Kernlogik!)
├── Rel? → .claude/*/external/{repo}/
├── Interessant? → .claude/templates/{tpl}.md
└── Irrelevant? → Skip-Notes
     │
     ▼
P4: Archivierung
└── /tmp/{repo} → _archive/repos/{date}-{name}/
     │
     ▼
P5: Integration
└── Findings → knowledge/, .claude/SYSTEM-MAP.md
```

---

## Phase 1: Relevanz-Check

### 1.1 Remote-Analyse

```python
# README + Struktur fetchen
readme = WebFetch(f"{raw_url}/README.md")
structure = WebFetch(github_url, prompt="Ordnerstruktur")
```

### 1.2 Relevanz-Indikatoren

| Indikator | Gewicht | Check |
|-----------|---------|-------|
| Claude Code Integration | +3 | `.claude/`, CLAUDE.md |
| MCP Server/Tools | +2 | mcp, tools, server |
| Agent Patterns | +2 | agents, multi-agent |
| Skills/Commands | +2 | skills, commands, workflows |
| Memory/Persistence | +1 | memory, persistence, state |
| Prompt Engineering | +1 | prompts, templates |

### 1.3 Relevanz-Score berechnen

```
Score < 4  → NICHT RELEVANT (Report + Ende)
Score 4-5  → GRENZWERTIG (User entscheiden lassen)
Score >= 6 → RELEVANT (Deep Dive anbieten)
```

### 1.4 Phase 1 Output

```markdown
## Phase 1: Relevanz-Check

| Metric | Value |
|--------|-------|
| Repo | {name} |
| Score | {X}/10 |
| Indikatoren | {liste} |

**Fazit**: {RELEVANT/NICHT RELEVANT}

{Wenn RELEVANT}:
Für Code-Level Analyse muss ich clonen.
Soll ich Deep Dive starten?
```

---

## Phase 2: Deep Dive

### 2.1 Clone

```bash
git clone {url} /tmp/{repo-name}
```

### 2.2 Tech-Stack Detection

| Stack | Erkennungsdateien | Key-Patterns |
|-------|-------------------|--------------|
| Python | pyproject.toml, setup.py, *.py | `^(class\|def\|@dataclass)` |
| TypeScript | package.json, tsconfig.json, *.ts | `^(export\|interface\|type\|class)` |
| Claude Code | .claude/*, CLAUDE.md | agents, commands, skills |
| Go | go.mod, *.go | `^(func\|type\|package)` |

### 2.3 Code-Level Extraktion

**Für Python:**
```bash
Grep "^(class |def |@dataclass)" **/*.py
Read pyproject.toml, requirements.txt
```

Extrahiere:
- Klassen mit Methoden-Signaturen
- Dataclass/Pydantic Felder
- Dependencies

**Für TypeScript:**
```bash
Grep "^(export |interface |type )" **/*.ts
Read package.json
```

Extrahiere:
- Interface Definitionen
- Type Aliases
- Exported Functions

**Für Claude Code (.claude/):**
```bash
Glob .claude/agents/*.md
Glob .claude/commands/*.md
Glob .claude/skills/*
```

Extrahiere:
- Agent-Definitionen (Typ, Domain)
- Command-Workflows
- Skill-Strukturen
- Hooks, Rules

### 2.4 Mapping gegen Evolving

Für JEDES Finding:

| Kategorie | Bedeutung | Aktion |
|-----------|-----------|--------|
| 🟢 NEU | Haben wir nicht | → patterns/ oder learnings/ |
| 🟡 BESSER | Ihre Version überlegen | → Upgrade unsere |
| 🔵 ANDERS | Andere Herangehensweise | → Evaluieren |
| ⚪ REDUNDANT | Haben wir schon | → Nur dokumentieren |

### 2.5 Automatisches Tagging

Neue Findings werden getaggt aus `_graph/taxonomy.json`:

```markdown
---
tags: [memory, persistence, context-management]
---
# {Finding Title}
```

---

## Phase 3: REL-EXTRAKTION (Kernlogik!)

**Regel**: Lies `.claude/rules/relevance-extraction.md`

### 3.1 Entscheidungsbaum

Für JEDE Komponente (A, S, C, H, R, P):

```
Komponente gefunden
       │
       ▼
┌──────────────────┐
│ Für UNS nutzbar? │
└────────┬─────────┘
    Ja   │   Nein
    ▼    │    ▼
   EXT   │  ┌──────────────────┐
         │  │ Framework        │
         │  │ interessant?     │
         │  └────────┬─────────┘
         │      Ja   │   Nein
         │      ▼    │    ▼
         │    TPL    │  SKIP
```

### 3.2 EXT → external/

Direkt nutzbare Komponenten:

```
.claude/{type}/external/{repo}/
├── {komponente}.md          # Vollständiger Inhalt
└── _index.json              # Tags + Beschreibungen
```

**_index.json Format:**
```json
{
  "source": "{github-url}",
  "extracted": "{date}",
  "components": [
    {
      "name": "{name}",
      "type": "agent|skill|command|hook",
      "tags": ["tag1", "tag2"],
      "status": "extracted|adapted|integrated"
    }
  ]
}
```

### 3.3 TPL → templates/

Interessantes Framework, aber irrelevanter Use-Case:

```
.claude/templates/{abstrahierter-name}.md
```

**Abstraktion:**
- Themen-Referenzen → Platzhalter
- "kubernetes" → "{domain}"
- "deployment" → "{task}"
- Framework/Struktur behalten

### 3.4 SKIP → Skip-Notes

Irrelevante Komponenten dokumentieren:

```
knowledge/learnings/{repo}-skip-notes.md
```

**Format:**
```markdown
# {Repo} Skip Notes

| Komponente | Grund |
|------------|-------|
| discord-bot | Discord-spezifisch |
| aws-lambda | AWS, kein neues Framework |
```

### 3.5 Rel-Extraktion Output

```markdown
## Phase 3: Rel-Extraktion

| Komponente | Entscheidung | Aktion |
|------------|--------------|--------|
| context-mgr-agent | EXT | → agents/external/{repo}/ |
| k8s-validator | TPL | → templates/validation-checklist.md |
| discord-bot | SKIP | → {repo}-skip-notes.md |

Extrahiert: {X} | Templates: {Y} | Skipped: {Z}
```

---

## Phase 4: Archivierung

Nach Rel-Extraktion:

```bash
# Verschieben
mv /tmp/{repo-name} _archive/repos/{YYYY-MM-DD}-{repo-name}/

# Summary erstellen
Write _archive/repos/{date}-{repo-name}/_analysis.md
```

---

## Phase 5: Integration (WICHTIG!)

**Archivieren reicht NICHT!** Relevante Findings müssen ins System:

### 5.1 Für jedes 🟢 NEU Finding

```
1. Pattern/Learning erstellen:
   → knowledge/patterns/{name}-pattern.md
   → knowledge/learnings/{name}.md

2. Mit Tags aus taxonomy.json versehen

3. SYSTEM-MAP.md Changelog updaten
```

### 5.2 Für jedes 🟡 BESSER Finding

```
1. Bestehende Datei identifizieren
2. Verbesserung einarbeiten
3. Quelle im Dokument vermerken
```

### 5.3 Integration-Checkliste

Nach jedem Deep Dive FRAGEN:

```markdown
## Integration

Ich habe folgende Findings identifiziert:

| # | Finding | Kategorie | Integrieren? |
|---|---------|-----------|--------------|
| 1 | {name} | 🟢 NEU | ☐ |
| 2 | {name} | 🟡 BESSER | ☐ |
| 3 | {name} | 🔵 ANDERS | ☐ Evaluieren |

Welche soll ich jetzt integrieren?
- Alle NEU
- Alle NEU + BESSER
- Spezifische (Nummern nennen)
- Keine (nur archivieren)
```

### 5.4 Nach Integration

```markdown
## Integriert

| Finding | Location | Done |
|---------|----------|------|
| {name} | knowledge/patterns/{file}.md | ✓ |
| {name} | knowledge/learnings/{file}.md | ✓ |

SYSTEM-MAP.md Changelog aktualisiert.
```

---

**_analysis.md Format:**
```markdown
# {Repo} Analysis

**Datum**: {date}
**URL**: {url}
**Score**: {X}/10

## Extrahierte Patterns

| Pattern | Code | Integration |
|---------|------|-------------|
| {name} | `{signature}` | patterns/{file} |

## Integration Status

| Finding | Integriert | Location |
|---------|------------|----------|
| {name} | ✓/✗ | {path} |

## Quick Access

`cd _archive/repos/{date}-{name}/`
```

---

## Output: Deep Dive Report

```markdown
# {REPO_NAME} Deep Dive

## Summary

| Metric | Value |
|--------|-------|
| Score | {X}/10 |
| Tech Stack | {stack} |
| Code Files | {count} |
| Extrahierte Patterns | {count} |

## 🟢 NEU (Code-Level)

### Pattern: {name}
**Datei**: `{path}`
**Code**:
```{lang}
{extracted_code}
```
**Integration**: → knowledge/patterns/{name}.md
**Tags**: {auto-tags}

## 🟡 BESSER (vs. unsere Version)

| Finding | Unser Code | Ihr Code | Verbesserung |
|---------|-----------|----------|--------------|
| {name} | {ours} | {theirs} | {improvement} |

## 🔵 ANDERS

{alternative approaches}

## Archiv

Repo archiviert: `_archive/repos/{date}-{name}/`
Für Details: Dort reinschauen.

## SYSTEM-MAP Update

| Datum | Finding | Integration | Status |
|-------|---------|-------------|--------|
| {date} | {finding} | {location} | Pending |
```

---

## Beispiel-Flow

```
User: "Schau dir mal https://github.com/some/claude-tools an"

Claude:
## Phase 1: Relevanz-Check

| Metric | Value |
|--------|-------|
| Repo | claude-tools |
| Score | 8/10 |
| Indikatoren | .claude/ ✓, MCP ✓, Hooks ✓ |

**Fazit**: RELEVANT

Für Code-Level Analyse muss ich clonen.
Deep Dive starten?

User: Ja

Claude:
Cloning...
Analysiere Code...
Extrahiere Patterns...

[Deep Dive Report mit Code-Level Details]

✓ Archiviert: _archive/repos/2025-12-27-claude-tools/
```

---

## KRITISCH: Nicht überspringen!

**Wenn eine Datei/Seite nicht gelesen werden kann:**

1. **NIEMALS stillschweigend überspringen**
2. **User informieren**: "Konnte {datei} nicht lesen"
3. **Alternativen versuchen**:
   - Raw GitHub URL statt Page
   - Lokaler Clone falls Remote fehlschlägt
   - Andere Dateien im gleichen Ordner
4. **Explizit fragen**: "Soll ich anders vorgehen?"

**Warum?** Nicht lesbare Dateien können die wichtigsten Findings enthalten!

**Beispiel:**
```
⚠ Konnte docs/architecture.md nicht lesen (404)

Das könnte relevante Patterns enthalten.
Alternativen:
1. Lokal clonen und dann lesen
2. Ähnliche Dateien suchen (docs/*.md)
3. Überspringen (mit Vermerk im Report)

Wie soll ich vorgehen?
```

**Im Report dokumentieren:**
```markdown
## Nicht gelesene Dateien

| Datei | Grund | Potentielle Relevanz |
|-------|-------|---------------------|
| docs/architecture.md | 404 | Hoch (Architecture Patterns) |
| src/internal/ | Private | Mittel |
```

---

## Error Handling

### Nicht erreichbar
```
❌ Repo nicht erreichbar

Optionen:
1. Lokal klonen: git clone {url}
2. Dann: "Analysiere /path/to/repo"
```

### Score zu niedrig
```
Score: 2/10

Keine Claude Code Relevanz erkannt.
Analyse beenden.
```

### Datei nicht lesbar
```
⚠ {datei} nicht lesbar

Nicht überspringen! Alternativen versuchen oder User fragen.
```

---

## Reads

- `.claude/SYSTEM-MAP.md` (für Mapping)
- `_graph/taxonomy.json` (für Auto-Tagging)
- `.claude/rules/relevance-extraction.md` (Rel-Check + Tpl Framework)
- `.claude/rules/no-reference-only.md` (Kein URL-only!)

## Creates/Updates

- `.claude/{type}/external/{repo}/` (EXT-Komponenten)
- `.claude/{type}/external/{repo}/_index.json` (Index + Tags)
- `.claude/templates/{name}.md` (TPL-Abstraktionen)
- `knowledge/learnings/{repo}-skip-notes.md` (SKIP-Dok)
- `_archive/repos/{date}-{name}/` (nach Archivierung)
- `.claude/SYSTEM-MAP.md` Changelog (nach Integration)
- `knowledge/patterns/` oder `knowledge/learnings/` (bei Integration)

---

**Philosophie**: README-Level reicht nicht. Echte Deep Dives extrahieren Code, Signaturen, Schemas. Implementierbare Details statt Beschreibungen.
