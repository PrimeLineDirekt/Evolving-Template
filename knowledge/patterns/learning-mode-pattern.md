# Learning Mode Pattern

> **Source**: Piebald-AI/claude-code-system-prompts (system-prompt-learning-mode.md)
> **Type**: Interactive Learning / Pair Programming Pattern
> **Purpose**: Balance zwischen Task-Erledigung und Lernzielen

## Konzept

Statt Code komplett zu generieren, werden User an bedeutsamen Stellen herausgefordert, selbst zu implementieren. "Learn by Doing" mit AI-Unterstützung.

## Kern-Mechanismus: TODO(human)

```python
def process_data(items):
    validated = []
    for item in items:
        # TODO(human): Implement validation logic
        # Consider: type checking, range validation, required fields
        pass
    return validated
```

Der User soll den `TODO(human)` Teil selbst implementieren.

## Wann Learning Mode aktivieren?

| Trigger | Beispiel |
|---------|----------|
| Komplexe Logik (20+ Zeilen) | Algorithmus, Business Rules |
| Fehlerbehandlung | Try/Catch Strategien |
| Datenstrukturen | Custom Classes, State Management |
| Architektur-Entscheidungen | Design Patterns |
| Debugging | Root Cause Analysis |

## Format: Learn-by-Doing Block

```markdown
## Learning Challenge

**Context:**
{Was der Code tut und warum diese Stelle wichtig ist}

**Your Task:**
Implementiere {spezifische Aufgabe} in 2-10 Zeilen.

**Guidance:**
- Bedenke: {Hinweis 1}
- Achte auf: {Hinweis 2}
- Vermeide: {Anti-Pattern}

**Code Location:**
```{language}
// ... existing code ...

// TODO(human): Your implementation here
// Expected: {was erwartet wird}

// ... existing code ...
```

**When you're done:**
Teile deinen Code und ich gebe dir Feedback.
```

## Regeln

### 1. Ein TODO(human) pro Code-Block
```
✗ Mehrere TODOs → User überfordert
✓ Ein fokussierter TODO → Klares Lernziel
```

### 2. TODO VOR der Anfrage setzen
```
Erst TODO platzieren, dann auf User warten.
Nicht: Code generieren und dann TODO erwähnen.
```

### 3. Nach User-Input: Insight Message
```
User implementiert → Claude gibt Feedback:
- Was gut war
- Was verbessert werden könnte
- Alternative Ansätze
- Warum die Lösung funktioniert
```

### 4. Scope begrenzen: 2-10 Zeilen
```
Zu wenig (1 Zeile) → Trivial, kein Lerneffekt
Zu viel (20+ Zeilen) → Überfordernd
Sweet Spot: 2-10 Zeilen mit klarem Fokus
```

## Beispiele

### Beispiel 1: Ganze Funktion

```markdown
## Learning Challenge: Input Validation

**Context:**
Wir bauen eine User-Registration. Die Validierung ist kritisch für Security.

**Your Task:**
Implementiere `validate_email()` die prüft ob eine Email gültig ist.

**Guidance:**
- Nutze Regex oder String-Methoden
- Prüfe: @ vorhanden, Domain vorhanden, keine Leerzeichen
- Return: True/False

**Code:**
```python
def validate_email(email: str) -> bool:
    # TODO(human): Implement email validation
    # Expected: Return True if valid, False otherwise
    pass
```
```

### Beispiel 2: Teil einer Funktion

```markdown
## Learning Challenge: Error Handling

**Context:**
Die API-Funktion braucht robustes Error Handling.

**Your Task:**
Füge try/except hinzu für den API-Call.

**Guidance:**
- Fange spezifische Exceptions (nicht bare except)
- Logge den Fehler
- Gib sinnvollen Fallback zurück

**Code:**
```python
def fetch_user_data(user_id: int) -> dict:
    url = f"https://api.example.com/users/{user_id}"

    # TODO(human): Add error handling around this request
    response = requests.get(url)
    data = response.json()

    return data
```
```

### Beispiel 3: Debugging

```markdown
## Learning Challenge: Debug This

**Context:**
Der folgende Code hat einen Bug. Users berichten dass die Summe falsch ist.

**Your Task:**
Finde und fixe den Bug.

**Guidance:**
- Trace durch mit Beispiel-Input
- Achte auf Edge Cases
- Prüfe Loop-Bedingungen

**Code:**
```python
def calculate_total(items):
    total = 0
    for i in range(len(items)):
        total += items[i].price
        i += 1  # Bug ist hier!
    return total
```

**Hint:** Was passiert mit `i` in einer for-loop?
```

## Insight Message Format

Nach User-Implementierung:

```markdown
## Feedback

**Was du gut gemacht hast:**
- {Positives 1}
- {Positives 2}

**Verbesserungsvorschläge:**
- {Suggestion 1}
- {Suggestion 2}

**Warum das funktioniert:**
{Erklärung des Konzepts}

**Alternative Ansätze:**
```{language}
# Option 2: Mit {anderer Technik}
{alternativer Code}
```

**Weiterführend:**
- {Link oder Konzept zum Vertiefen}
```

## Integration mit Evolving

### Möglicher Command: `/learn`

```markdown
/learn {topic}

Aktiviert Learning Mode für das Thema.
Generiert Challenges statt fertigem Code.
```

### Möglicher Agent: `learning-coach-agent`

- Erkennt Lern-Opportunities im Code
- Generiert passende Challenges
- Gibt strukturiertes Feedback

### Wann Learning Mode vorschlagen?

```
User fragt: "Implementiere X für mich"
Claude erkennt: Komplexe Logik, gute Lern-Opportunity

Claude: "Das ist eine gute Gelegenheit zum Lernen!
        Soll ich dir eine Challenge stellen statt
        den Code direkt zu generieren?"
```

## Best Practices

1. **Adaptiv sein**: Wenn User struggled, mehr Guidance geben
2. **Nicht frustrieren**: Nach 2 Versuchen Lösung anbieten
3. **Kontext behalten**: Vorheriges Wissen des Users berücksichtigen
4. **Feiern**: Erfolge anerkennen, Motivation aufbauen

---

## Related

- [Pair Programming Pattern](pair-programming-pattern.md) (falls vorhanden)
- System Instructions: Learning Style "Learning by Doing"
