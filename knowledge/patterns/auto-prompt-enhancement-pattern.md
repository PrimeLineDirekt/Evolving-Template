# Auto-Prompt Enhancement Pattern

**Confidence**: 85%
**Status**: Production
**Created**: 2025-12-14

## Konzept

Automatische Transformation einfacher Prompts in komplexe, kontextreiche Prompts basierend auf:
1. **Komplexitäts-Analyse** - Was braucht der Task wirklich?
2. **Context-Extraktion** - Was wissen wir bereits?
3. **Technique-Injection** - Welche Prompt-Techniken helfen?

## Architektur

```
User Input (Simple)
       │
       ▼
┌──────────────────────────────────────────────────────────┐
│              AUTO-ENHANCEMENT PIPELINE                    │
│                                                          │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐      │
│  │  ANALYZER   │→ │  EXTRACTOR  │→ │  ENHANCER   │      │
│  │ (Complexity)│  │  (Context)  │  │ (Technique) │      │
│  └─────────────┘  └─────────────┘  └─────────────┘      │
│         │                │                │              │
│         ▼                ▼                ▼              │
│    Level 1-5        Relevant         Enhanced            │
│    Assessment       Context          Prompt              │
└──────────────────────────────────────────────────────────┘
       │
       ▼
Enhanced Prompt (Complex)
```

## Komponenten

### 1. Complexity Analyzer

Bestimmt das nötige Enhancement-Level:

| Level | Trigger-Signale | Enhancement |
|-------|-----------------|-------------|
| 1 | Einfache Fakten, "Was ist X?" | Keine - direkt antworten |
| 2 | Analyse, Erklärung, "Wie funktioniert?" | + Struktur, + Beispiele |
| 3 | Multi-Step, "Erstelle", "Implementiere" | + Phasen, + Chaining |
| 4 | Research, Strategie, "Entwickle Plan" | + Extended Thinking, + ToT |
| 5 | Edge Cases, Strict Format | + Prefilling, + Validation |

**Classifier-Heuristiken:**

```python
def classify_complexity(prompt):
    # Level 1 Indicators
    if is_factual_question(prompt):
        return 1

    # Level 2 Indicators
    if needs_explanation(prompt) or needs_examples(prompt):
        return 2

    # Level 3 Indicators
    if is_multi_step(prompt) or is_creation_task(prompt):
        return 3

    # Level 4 Indicators
    if is_research(prompt) or is_strategic(prompt):
        return 4

    # Level 5 Indicators
    if needs_strict_format(prompt) or is_edge_case(prompt):
        return 5

    return 2  # Default: moderate enhancement
```

**Keyword-basierte Detection:**

| Keywords | Level |
|----------|-------|
| "was ist", "definiere", "erkläre kurz" | 1 |
| "erkläre", "wie funktioniert", "vergleiche" | 2 |
| "erstelle", "implementiere", "entwickle" | 3 |
| "recherchiere", "analysiere tief", "strategie" | 4 |
| "exakt format", "validiere strikt" | 5 |

### 2. Context Extractor

Sammelt relevanten Kontext aus verfügbaren Quellen:

**Quellen (Priorität):**

1. **Session Context** (Highest)
   - Letzte 3-5 relevante Messages
   - Aktive Entscheidungen
   - Erwähnte Constraints

2. **Domain Memory**
   - `_memory/projects/{active}.json`
   - Aktuelle Goals & State
   - Known Failures

3. **Knowledge Base**
   - Relevante Patterns
   - Projekt-spezifisches Wissen
   - Learnings

4. **Experience Memory**
   - Ähnliche gelöste Probleme
   - User Preferences

**Extraction Logic:**

```python
def extract_context(prompt, session):
    context = {}

    # 1. Session Context
    context['recent'] = get_relevant_messages(session, limit=5)
    context['decisions'] = get_session_decisions(session)

    # 2. Domain Memory
    active_project = read_memory_index()
    if active_project:
        context['project'] = read_project_memory(active_project)

    # 3. Knowledge Base (keyword-matched)
    keywords = extract_keywords(prompt)
    context['knowledge'] = search_knowledge_base(keywords)

    # 4. Experience Memory
    context['experiences'] = search_experiences(keywords)

    return context
```

### 3. Technique Injector

Wendet Prompt Pro Framework Techniken an:

| Level | Techniken |
|-------|-----------|
| 1 | Clear & Direct (keine Änderung) |
| 2 | + XML Structure, + Role, + Examples |
| 3 | + Phase Decomposition, + Chaining |
| 4 | + Extended Thinking, + Tree of Thought |
| 5 | + Prefilling, + Validation Rules |

**Enhancement Templates:**

```xml
<!-- Level 2 Enhancement -->
<context>
  {EXTRACTED_CONTEXT}
</context>

<role>
  Du bist ein Experte für {DOMAIN}.
</role>

<task>
  {ORIGINAL_PROMPT}
</task>

<output_format>
  {STRUCTURE_HINT}
</output_format>
```

```xml
<!-- Level 3+ Enhancement -->
<objective>
  {GOAL_FROM_PROMPT}
</objective>

<context>
  {EXTRACTED_CONTEXT}
</context>

<phase_1>
  <name>Analyse</name>
  <task>{DECOMPOSED_STEP_1}</task>
</phase_1>

<phase_2>
  <name>Synthese</name>
  <task>{DECOMPOSED_STEP_2}</task>
</phase_2>

<success_criteria>
  {INFERRED_CRITERIA}
</success_criteria>
```

## Integration Points

### A. Transparent Mode (Default)

Enhancement passiert automatisch im Hintergrund:

```
User: "Hilf mir mit meiner E-Commerce SEO"

System (intern):
  1. Complexity: Level 3 (multi-step task)
  2. Context: Active project = {active-project},
              Known: SEO Patterns, Platform Integration
  3. Enhance: Add structure, inject knowledge

Enhanced Prompt (intern):
  <context>
    Projekt: {project-name}
    Bekannte Patterns: Keyword Research, Title Structure
    Ziel: Listing-Optimierung
  </context>

  <task>
    Unterstütze bei E-Commerce SEO Optimierung
  </task>

  <phases>
    1. Keyword-Analyse
    2. Title-Optimierung
    3. Tag-Strategie
  </phases>

User sieht: Strukturierte, fundierte Antwort
```

### B. Explicit Mode (`--enhance`)

User triggert explizit:

```
/run-prompt 004 --enhance

oder

/create-prompt --auto "Analysiere meinen Markt"
```

### C. Threshold Mode

Enhancement nur wenn sinnvoll:

```python
ENHANCEMENT_THRESHOLD = 2  # Nur Level 2+ enhancen

if complexity >= ENHANCEMENT_THRESHOLD:
    enhance(prompt)
else:
    execute_directly(prompt)
```

## Implementierung

### Command: `/enhance`

Schnelle Prompt-Enhancement ohne Speichern:

```markdown
/enhance [prompt]

→ Analysiert Komplexität
→ Extrahiert Kontext
→ Zeigt enhanced Prompt
→ Fragt: "Ausführen?"
```

### Auto-Mode in `/create-prompt`

```markdown
/create-prompt --auto [task]

→ Alles automatisch
→ Optimales Level wählen
→ Kontext injizieren
→ Als Datei speichern
→ Optional direkt ausführen
```

### Integration in Task Tool

Bei jedem Task-Aufruf optional:

```python
Task(
    prompt=prompt,
    auto_enhance=True,  # NEU
    subagent_type="general-purpose"
)
```

## Best Practices

1. **Nicht über-enhancen**
   - Level 1 Fragen brauchen keine Enhancement
   - Manchmal ist einfach besser

2. **Kontext-Relevanz**
   - Nur relevanten Kontext injizieren
   - Zu viel Kontext = Noise

3. **Transparenz**
   - User sollte wissen dass Enhancement passiert
   - Optional: Enhanced Prompt zeigen

4. **Feedback-Loop**
   - Wenn Enhancement nicht hilft → Learning speichern
   - Classifier verbessern

## Limitations

- Complexity Classification ist heuristisch
- Kontext-Extraktion kann irrelevantes einschließen
- Overhead bei einfachen Fragen

## Related

- `@prompt-pro-framework` - Basis-Techniken
- `/create-prompt` - Explizite Prompt-Erstellung
- `/run-prompt` - Prompt-Ausführung
- `_memory/` - Kontext-Quelle
- `_graph/cache/context-router.json` - Knowledge Routing
