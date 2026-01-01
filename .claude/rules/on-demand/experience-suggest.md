# Experience Auto-Suggest Rule

**Prioritaet**: HOCH
**Trigger**: Bei Fehlern, Architektur-Fragen, Code-Style-Fragen

## Konzept

Das Experience Memory System speichert Erfahrungen (Solutions, Patterns, Decisions, etc.).
Diese Rule definiert WANN und WIE automatisch relevante Experiences vorgeschlagen werden.

## Wann Auto-Suggest?

### 1. Bei Fehlern (Hoechste Prioritaet)

Wenn ein Fehler auftritt:

```
1. Error-Message extrahieren
2. _graph/cache/experience-router.json laden
3. Error-Patterns matchen
4. Falls Match: Relevante Experiences aus _memory/experiences/ laden
5. Vorschlagen:
   "Das hatten wir schon! Loesung war: {summary}"
   "Root Cause: {root_cause}"
   "Was NICHT funktioniert hat: {failed_approaches}"
```

### 2. Bei Architektur-Fragen (Mittlere Prioritaet)

Wenn User fragt "sollen wir X oder Y", "wie strukturieren wir", "welcher Ansatz":

```
1. Keywords extrahieren
2. experience-router.json → architecture-decision Route
3. Relevante Decisions anzeigen:
   "Wir haben uns frueher fuer X entschieden, weil: {reasoning}"
```

### 3. Bei Code-Style-Fragen (Niedrigere Prioritaet)

Wenn User nach Formatierung, Naming, Conventions fragt:

```
1. Keywords extrahieren
2. experience-router.json → code-style Route
3. Preferences anzeigen:
   "Deine Praeferenz: {preference} (Confidence: {confidence}%)"
```

### 4. Bei Projekt-Start (Kontext-basiert)

Wenn in einem bekannten Projekt gearbeitet wird:

```
1. Projekt-Tags aus Kontext extrahieren
2. Relevante Patterns und Gotchas fuer dieses Projekt laden
3. Proaktiv warnen bei bekannten Stolperfallen
```

## Wie vorschlagen?

### Format bei Fehlern

```
Relevante Erfahrung gefunden!

[solution] exp-2025-001: {summary}
Root Cause: {root_cause}
Loesung: {solution}
Was NICHT funktioniert hat: {failed_approaches}

Soll ich die vollstaendigen Details zeigen?
```

### Format bei Decisions

```
Zu diesem Thema gibt es eine fruehere Entscheidung:

[decision] exp-2025-005: {question}
Entscheidung: {decision}
Begruendung: {reasoning}
Revisit wenn: {revisit_if}
```

### Format bei Patterns

```
Passendes Pattern gefunden:

[pattern] exp-2025-010: {name}
Wann nutzen: {when_to_use}
Beispiel: {example_file}
```

### Format bei Gotchas

```
ACHTUNG - Bekannte Stolperfalle!

[gotcha] exp-2025-015: {trap}
Warum problematisch: {why_problematic}
Korrekter Ansatz: {correct_approach}
```

## NICHT vorschlagen wenn:

- User explizit "ohne Memory" oder "fresh start" sagt
- Experience-Score < 30 (zu niedrig)
- Experience aelter als 180 Tage UND Score < 50
- Bereits in dieser Session vorgeschlagen

## Access-Tracking

Bei jedem Vorschlag:
1. `access_count++` in der Experience
2. `last_accessed` updaten
3. Falls User die Loesung nutzt: `relevance_score += 5`

## Beispiel-Flow

```
User: "npm run build gibt einen Type Error"

Claude:
1. Erkennt: Build-Fehler + TypeScript
2. Laedt experience-router.json
3. Matched: typescript-error Route
4. Findet: exp-2025-001 mit aehnlichem Error-Pattern
5. Zeigt:
   "Das hatten wir schon!
    [solution] TypeScript Property Error
    Root Cause: Interface nicht erweitert
    Loesung: Interface um Property ergaenzen"
```

## Integration mit Commands

- `/recall` nutzt experience-router.json fuer Suche
- `/remember` aktualisiert experience-router.json bei neuen Experiences
- `/preferences` zeigt preference-type Experiences
