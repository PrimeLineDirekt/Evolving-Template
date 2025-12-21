# /remember [type]

Speichere eine Erfahrung im Experience Memory System.

## Model: haiku

## Argument
- `type` (optional): solution, pattern, decision, workaround, gotcha, preference

## Workflow

### 1. Typ bestimmen
Falls kein Typ angegeben, frage:
```
Was moechtest du speichern?
1. solution - Fehler + Fix
2. pattern - Erfolgreicher Ansatz
3. decision - Architektur-Entscheidung
4. workaround - Temporaerer Fix
5. gotcha - Stolperfalle
6. preference - User-Praeferenz
```

### 2. Typ-spezifische Fragen

**Solution:**
- Was war das Problem/der Fehler?
- Was war die Root Cause?
- Was ist die Loesung?
- Was hat NICHT funktioniert? (optional)

**Pattern:**
- Name des Patterns?
- Wann anwenden?
- Wie implementieren?
- Beispiel-Datei? (optional)

**Decision:**
- Welche Frage wurde entschieden?
- Was wurde entschieden?
- Warum? (Reasoning)
- Was wurde verworfen?
- Wann revisiten?

**Workaround:**
- Was ist das Issue?
- Was ist der Workaround?
- Wann kommt der permanente Fix?
- Ablaufdatum? (optional)

**Gotcha:**
- Was ist die Stolperfalle?
- Warum ist es problematisch?
- Was ist der korrekte Ansatz?

**Preference:**
- Kategorie (code-style, architecture, workflow, communication)?
- Was ist die Praeferenz?
- Woher kommt sie?

### 3. Auto-Tags generieren
Basierend auf:
- Aktuellem Projekt (falls bekannt)
- Tech-Stack aus Kontext
- Keywords aus der Beschreibung

### 4. Relevanz-Score berechnen
Initiale Faktoren:
- Attempts (falls bekannt): 0-30 Punkte
- Complexity: 0-25 Punkte (basierend auf Beschreibung)
- Reusability: 0-25 Punkte (generische Tags = hoeher)
- Base: 20 Punkte

### 5. Experience speichern

1. Lies `_memory/experiences/index.json`
2. Generiere ID: `exp-{YYYY}-{NNN}` (next_id)
3. Erstelle `_memory/experiences/exp-{YYYY}-{NNN}.json`
4. Update Index:
   - count++
   - next_id++
   - types[type]++
   - experiences.push({id, summary, relevance_score, tags, type})
5. Update `_graph/cache/experience-router.json` mit neuen Trigger-Patterns

### 6. Bestaetigung
```
Experience gespeichert!
ID: exp-2025-001
Typ: {type}
Score: {relevance_score}
Tags: {tags}
```

## Shortcuts
- `/remember solution` - Direkt zur Solution
- `/remember decision` - Direkt zur Decision
- `/remember gotcha` - Direkt zur Gotcha

## Plain Text Triggers
- "speichere diese loesung"
- "merk dir das"
- "das sollten wir uns merken"
- "remember this"
