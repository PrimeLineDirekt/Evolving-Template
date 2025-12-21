---
description: Analysiere externes Repository mit Dual-System Mapping
model: opus
argument-hint: [GitHub-URL oder lokaler Pfad]
---

Du analysierst externe Repositories und mappst Findings gegen unser Evolving-System. Jedes Finding wird kontextualisiert und mit konkreten Integrations-Vorschlägen versehen.

## Plain Text Detection

**Dieser Workflow wird ausgelöst durch**:
- `/analyze-repo https://github.com/owner/repo`
- `/analyze-repo /path/to/local/repo`
- "Analysiere dieses Repo: ..."
- "Schau dir mal ... an"
- "Was können wir von ... lernen?"
- "Untersuche das Repository ..."

**Bei Plain Text ohne Slash Command**:
1. Erkenne Intent (Repository analysieren)
2. Extrahiere URL/Pfad aus User-Message
3. Frage: "Soll ich `/analyze-repo` mit `{url/path}` ausführen?"
4. Bei "Ja" → Starte Analyse

---

## Schritt 1: Input validieren

### URL/Pfad parsen

**$ARGUMENTS Format**:
- GitHub URL: `https://github.com/owner/repo`
- Lokaler Pfad: `/path/to/repo`

**Erkennung**:
```python
def detect_source_type(input):
    if input.startswith("https://github.com/"):
        return "remote", parse_github_url(input)
    elif os.path.exists(input):
        return "local", os.path.abspath(input)
    else:
        return "invalid", None
```

**Bei Fehler**: "Repository nicht gefunden. Bitte gib eine gültige GitHub-URL oder einen lokalen Pfad an."

---

## Schritt 2: SYSTEM-MAP laden (Phase 1)

**KRITISCH**: Vor der Repo-Analyse MUSS die SYSTEM-MAP gelesen werden!

```python
system_map_path = ".claude/SYSTEM-MAP.md"

if not os.path.exists(system_map_path):
    print("""
    ⚠️ SYSTEM-MAP.md nicht gefunden!

    Die SYSTEM-MAP ist erforderlich für kontextualisierte Findings.

    Soll ich sie jetzt erstellen? (Dauert ca. 2 Minuten)
    """)
    # If yes: Run system scan and create SYSTEM-MAP.md
else:
    system_context = Read(system_map_path)
    print(f"""
    ✅ SYSTEM-MAP geladen

    Unser System:
    - {count_agents} Agents
    - {count_skills} Skills
    - {count_commands} Commands
    - {count_patterns} Patterns

    Starte Repository-Analyse...
    """)
```

---

## Schritt 3: Repository analysieren (Phase 2)

### Für Remote Repos (GitHub)

```python
def analyze_remote(github_url):
    owner, repo = parse_url(github_url)
    base_raw = f"https://raw.githubusercontent.com/{owner}/{repo}/main"

    # Core files
    readme = WebFetch(f"{base_raw}/README.md",
                      prompt="Extrahiere: Purpose, Features, Tech Stack, Architecture, Key Patterns")

    # Config files (try multiple)
    for config in ["package.json", "pyproject.toml", "Cargo.toml", "go.mod"]:
        try:
            config_content = WebFetch(f"{base_raw}/{config}",
                                      prompt="Extrahiere: Dependencies, Scripts, Metadata")
            break
        except:
            continue

    # Structure via GitHub page
    structure = WebFetch(github_url,
                         prompt="Extrahiere: Ordnerstruktur, Key Files, Patterns")

    # Additional key files based on structure
    for important_file in identify_key_files(structure):
        WebFetch(f"{base_raw}/{important_file}")

    return findings
```

### Für Lokale Repos

```python
def analyze_local(repo_path):
    # Structure
    all_files = Glob(f"{repo_path}/**/*")

    # Core files
    readme = Read(f"{repo_path}/README.md")
    config = Read(f"{repo_path}/package.json")  # or equivalent

    # Pattern search
    patterns = Grep(pattern="class |function |export |def ", path=repo_path)

    # Git info
    commits = Bash(f"cd {repo_path} && git log --oneline -20")
    remote = Bash(f"cd {repo_path} && git remote -v")

    return findings
```

---

## Schritt 4: Findings gegen System mappen (Phase 3)

**Für JEDES Finding**:

```python
def categorize_finding(finding, system_context):
    # Check our system for equivalent
    equivalent = find_in_system(finding.type, system_context)

    if not equivalent:
        return {
            "category": "NEU",
            "emoji": "🟢",
            "action": f"Add to {suggest_location(finding)}",
            "effort": estimate_effort(finding)
        }

    comparison = compare(finding, equivalent)

    if comparison.is_better:
        return {
            "category": "BESSER",
            "emoji": "🟡",
            "our_version": equivalent,
            "improvement": comparison.improvements,
            "action": f"Upgrade {equivalent.name}",
            "effort": estimate_effort(finding)
        }

    if comparison.is_different:
        return {
            "category": "ANDERS",
            "emoji": "🔵",
            "our_approach": equivalent.approach,
            "their_approach": finding.approach,
            "recommendation": evaluate_approaches(finding, equivalent),
            "action": "Evaluate and decide"
        }

    return {
        "category": "REDUNDANT",
        "emoji": "⚪",
        "our_equivalent": equivalent,
        "action": "Document only"
    }
```

---

## Schritt 5: Report generieren (Phase 4)

### Output Format

```markdown
# 📊 Repository Analysis: {REPO_NAME}

## Executive Summary

| Metric | Value |
|--------|-------|
| **Repository** | {url or path} |
| **Purpose** | {1-sentence} |
| **Tech Stack** | {technologies} |
| **Relevance** | {X}/10 |
| **Actionable Findings** | {count} |

---

## Evolving System Context

SYSTEM-MAP.md loaded:
- Agents: {count}
- Skills: {count}
- Commands: {count}
- Patterns: {count}

---

## Repository Overview

### Purpose
{Description}

### Tech Stack
{Technologies}

### Key Features
1. {Feature 1}
2. {Feature 2}
3. {Feature 3}

---

## 🎯 Mapping & Findings

### 🟢 NEU - We Don't Have This

| Finding | Description | Integration Point | Effort |
|---------|-------------|-------------------|--------|
| {name} | {desc} | {where} | {estimate} |

### 🟡 BESSER - Upgrade Potential

| Finding | Our Current | Improvement | Action |
|---------|-------------|-------------|--------|
| {name} | {our version} | {what's better} | {action} |

### 🔵 ANDERS - Alternative Approaches

| Finding | Our Way | Their Way | Recommendation |
|---------|---------|-----------|----------------|
| {name} | {ours} | {theirs} | {recommendation} |

### ⚪ REDUNDANT - Already Have

| Finding | Our Equivalent |
|---------|----------------|
| {name} | {our version} |

---

## 📋 Integration Roadmap

### Quick Wins (< 1h)
- [ ] {Action} → {Location}

### Medium Effort (1-4h)
- [ ] {Action}
  - Create: {files}
  - Modify: {files}

### Larger Projects (> 4h)
- [ ] {Action}
  - Scope: {description}

---

## SYSTEM-MAP Update

Add to `.claude/SYSTEM-MAP.md` Changelog:

| Datum | Quelle | Finding | Integration | Status |
|-------|--------|---------|-------------|--------|
| {today} | {repo} | {finding} | {action} | Pending |

---

## Next Steps

1. Review findings above
2. Approve integrations you want
3. I'll update SYSTEM-MAP after implementation

**Sage einfach**: "Integriere {finding}" oder "Zeig mir mehr zu {finding}"
```

---

## Schritt 6: User-Interaktion

### Nach Report

**Optionen anbieten**:
```
📊 Analyse abgeschlossen!

Was möchtest du tun?

1. **Details zu Finding** - "Zeig mir mehr zu {finding}"
2. **Integration starten** - "Integriere {finding}"
3. **Alles Quick Wins** - "Mach alle Quick Wins"
4. **Später** - "Speicher für später"

Oder frag mich etwas Spezifisches!
```

### Bei Integration

**Vor jeder Änderung**:
```
⚠️ Integration: {FINDING_NAME}

Ich werde:
- Erstellen: {files}
- Ändern: {files}

Fortfahren? (ja/nein)
```

**Nach Integration**:
- SYSTEM-MAP.md Changelog updaten
- Betroffene Statistiken aktualisieren

---

## Error Handling

### Repository nicht erreichbar
```
❌ Repository nicht erreichbar

URL: {url}

Mögliche Gründe:
- Privates Repository
- URL fehlerhaft
- Netzwerkproblem

Alternativen:
1. Repository lokal klonen: `git clone {url}`
2. Dann: `/analyze-repo /path/to/cloned/repo`
```

### SYSTEM-MAP fehlt
```
⚠️ SYSTEM-MAP.md nicht gefunden

Für kontextualisierte Findings brauche ich die SYSTEM-MAP.

Soll ich sie jetzt erstellen? (Dauert ~2 Min)
```

### Keine relevanten Findings
```
✅ Analyse abgeschlossen

Ergebnis: Keine neuen Findings für Evolving.

Das Repository {name} bietet nichts, was wir nicht schon haben.

Alle {count} Findings wurden als REDUNDANT kategorisiert.
Details: {kurze Auflistung}
```

---

## Success Criteria

- ✅ SYSTEM-MAP.md wurde gelesen (Phase 1)
- ✅ Repository vollständig analysiert (Phase 2)
- ✅ ALLE Findings kategorisiert (NEU/BESSER/ANDERS/REDUNDANT)
- ✅ Konkrete Integration Points für actionable Findings
- ✅ SYSTEM-MAP Changelog vorbereitet

---

## Related

**Reads**:
- `.claude/SYSTEM-MAP.md` (immer)

**Updates** (nach Integration):
- `.claude/SYSTEM-MAP.md` (Changelog)
- Betroffene Komponenten

**Invokes**:
- `@github-repo-analyzer-agent` (intern)

---

**Command Philosophy**: Keine isolierten Findings! Alles wird gegen unser System gemappt. Konkrete Integrations-Vorschläge statt abstrakter Empfehlungen.
