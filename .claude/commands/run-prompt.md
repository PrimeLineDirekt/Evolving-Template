---
description: Führe gespeicherte Prompts in frischem Sub-Agent Kontext aus
model: sonnet
argument-hint: [Nummer oder Name] [--parallel|--sequential]
---

Du führst gespeicherte Prompts aus dem `prompts/` Ordner aus. Der Hauptvorteil: Ausführung in einem **frischen Sub-Agent Kontext** ohne Context-Bleeding vom Planning.

---

## Schritt 0: Arguments parsen

### Input-Formate

```
/run-prompt              → Letzten/neuesten Prompt
/run-prompt 004          → Prompt Nummer 004
/run-prompt seo          → Prompt mit "seo" im Namen
/run-prompt 004 005 006  → Mehrere Prompts
/run-prompt 004 005 --parallel   → Parallel ausführen
/run-prompt 004 005 --sequential → Sequentiell ausführen
```

### Parsing

```python
args = parse($ARGUMENTS)

if args.empty:
    mode = "latest"
    prompts = [get_latest_prompt()]

elif args.is_single_number:
    mode = "single"
    prompts = [resolve_by_number(args[0])]

elif args.is_single_text:
    mode = "single"
    prompts = [resolve_by_name(args[0])]

elif args.is_multiple:
    mode = "parallel" if "--parallel" in args else "sequential"
    prompts = [resolve(x) for x in args if not x.startswith("--")]
```

---

## Schritt 1: Prompts auflösen

### Glob für Prompt-Dateien

```python
all_prompts = Glob("prompts/*.md")

# Sortiert nach Nummer
# prompts/001-xxx.md
# prompts/002-xxx.md
# ...
```

### Auflösung

**By Number** (z.B. "004"):
```python
def resolve_by_number(num):
    pattern = f"prompts/{num.zfill(3)}-*.md"
    matches = Glob(pattern)
    if len(matches) == 1:
        return matches[0]
    elif len(matches) == 0:
        error(f"Kein Prompt mit Nummer {num} gefunden")
    else:
        error(f"Mehrere Matches - bitte spezifischer")
```

**By Name** (z.B. "seo"):
```python
def resolve_by_name(name):
    matches = [p for p in all_prompts if name.lower() in p.lower()]
    if len(matches) == 1:
        return matches[0]
    elif len(matches) == 0:
        error(f"Kein Prompt mit '{name}' gefunden")
    else:
        show_options(matches)
        ask("Welchen meinst du?")
```

### Bei Mehrdeutigkeit

```
Mehrere Prompts gefunden für "analysis":

1. prompts/002-competitor-analysis.md
2. prompts/005-market-analysis.md
3. prompts/008-data-analysis.md

Welchen möchtest du ausführen? (Nummer oder genauerer Name)
```

---

## Schritt 2: Prompt laden & validieren

### Datei lesen

```python
prompt_content = Read(prompt_path)
```

### Metadata extrahieren

```yaml
---
created: 2025-12-01
type: research
level: 3
model: opus
status: ready
---
```

### Validierung

```python
if metadata.status != "ready":
    warn(f"Prompt Status: {metadata.status}")
    ask("Trotzdem ausführen?")

if metadata.model != current_model:
    info(f"Empfohlenes Model: {metadata.model}")
    ask("Mit empfohlenem Model ausführen?")
```

---

## Schritt 3: Ausführung

### Single Prompt

```python
def execute_single(prompt_path):
    prompt = Read(prompt_path)

    # Nutze Task Tool für Sub-Agent Kontext
    result = Task(
        prompt=prompt,
        subagent_type="general-purpose",
        model=metadata.model or "sonnet"
    )

    return result
```

**Wichtig**: Der Task-Aufruf erstellt einen **frischen Kontext**:
- Kein Bleeding vom create-prompt Planning
- Nur der Prompt selbst ist im Kontext
- Saubere Ausführung

### Parallel Execution

```python
def execute_parallel(prompts):
    # ALLE Task-Calls in EINER Message
    # Das ist kritisch für echte Parallelität

    results = []
    for prompt in prompts:
        # Diese werden parallel gestartet
        Task(prompt=Read(prompt), subagent_type="general-purpose")

    # Warte auf alle
    return aggregate_results(results)
```

**User-Info**:
```
Starte parallele Ausführung:

🔄 prompts/004-market-research.md
🔄 prompts/005-competitor-analysis.md
🔄 prompts/006-trend-research.md

[Alle laufen gleichzeitig...]
```

### Sequential Execution

```python
def execute_sequential(prompts):
    results = []

    for i, prompt in enumerate(prompts):
        info(f"Schritt {i+1}/{len(prompts)}: {prompt}")

        # Vorherige Ergebnisse als Kontext
        context = results[-1] if results else None

        result = Task(
            prompt=Read(prompt),
            context=context,
            subagent_type="general-purpose"
        )

        results.append(result)

    return results
```

**User-Info**:
```
Starte sequentielle Ausführung:

✅ 1/3: prompts/004-research.md (fertig)
🔄 2/3: prompts/005-analysis.md (läuft...)
⏳ 3/3: prompts/006-strategy.md (wartet)
```

---

## Schritt 4: Ergebnis verarbeiten

### Single Result

```
## Ergebnis: {PROMPT_NAME}

{RESULT_CONTENT}

---

**Prompt**: prompts/{NNN}-{name}.md
**Model**: {model}
**Dauer**: ~{sekunden}s
```

### Multiple Results

```
## Ergebnisse

### 1. {PROMPT_1_NAME}
{RESULT_1}

### 2. {PROMPT_2_NAME}
{RESULT_2}

---

**Ausführung**: {parallel|sequential}
**Prompts**: {anzahl}
**Gesamt-Dauer**: ~{sekunden}s
```

---

## Schritt 5: Archivierung (Optional)

Nach erfolgreicher Ausführung:

```
Prompt erfolgreich ausgeführt!

Optionen:
1. **Archive** → Nach prompts/archive/ verschieben
2. **Keep** → Für spätere Wiederverwendung behalten
3. **Delete** → Prompt löschen
```

### Archive-Struktur

```
prompts/
├── 001-active-prompt.md
├── 002-another-prompt.md
└── archive/
    ├── 2025-12-01/
    │   ├── 001-old-prompt.md
    │   └── 002-another-old.md
    └── 2025-12-02/
        └── ...
```

---

## Schritt 6: Git Commit (Optional)

Falls Änderungen gemacht wurden:

```
Änderungen durch Prompt-Ausführung:

Modified:
- src/components/Header.tsx
- src/styles/main.css

Created:
- src/components/NewFeature.tsx

Git commit erstellen?
```

**Commit Format**:
```
[prompt]: {kurze beschreibung}

Executed: prompts/{NNN}-{name}.md
Type: {research|creative|strategy|technical}
```

---

## Error Handling

### Prompt nicht gefunden

```
❌ Prompt nicht gefunden

Gesucht: {input}
Verfügbare Prompts:
- 001-seo-optimization.md
- 002-competitor-analysis.md
- 003-pricing-strategy.md

Tipp: Nutze Nummer oder Teil des Namens
```

### Execution Error

```
❌ Fehler bei Ausführung

Prompt: prompts/{NNN}-{name}.md
Error: {error_message}

Optionen:
1. **Retry** - Nochmal versuchen
2. **Edit** - Prompt anpassen
3. **Abort** - Abbrechen
```

### Partial Failure (Multiple)

```
⚠️ Teilweise erfolgreich

✅ prompts/004-research.md - OK
❌ prompts/005-analysis.md - Error: {reason}
✅ prompts/006-strategy.md - OK

Fehlgeschlagenen Prompt erneut versuchen?
```

---

## Beispiele

### Einfach

```
/run-prompt 004

→ Lädt prompts/004-competitor-analysis.md
→ Führt in Sub-Agent aus
→ Zeigt Ergebnis
```

### Mit Name

```
/run-prompt seo

→ Findet prompts/001-seo-optimization.md
→ Führt aus
→ Zeigt Ergebnis
```

### Parallel

```
/run-prompt 004 005 006 --parallel

→ Startet alle drei gleichzeitig
→ Wartet auf alle
→ Zeigt aggregierte Ergebnisse
```

### Sequential

```
/run-prompt 004 005 006 --sequential

→ Führt 004 aus
→ Nutzt Ergebnis als Kontext für 005
→ Nutzt Ergebnis als Kontext für 006
→ Zeigt finale Ergebnisse
```

---

## Quick Reference

| Command | Aktion |
|---------|--------|
| `/run-prompt` | Neuesten Prompt |
| `/run-prompt 4` | Prompt #004 |
| `/run-prompt seo` | Prompt mit "seo" |
| `/run-prompt 4 5 6` | Sequential (default) |
| `/run-prompt 4 5 6 --parallel` | Parallel |
| `/run-prompt 4 5 6 --sequential` | Explizit sequential |

---

## Success Criteria

- ✅ Prompt korrekt aufgelöst
- ✅ In Sub-Agent Kontext ausgeführt
- ✅ Ergebnis angezeigt
- ✅ Archivierungs-Option angeboten

---

## Related

- `/create-prompt` - Prompts erstellen
- `@prompt-pro-framework` - Framework Referenz
- `prompts/` - Prompt Storage
