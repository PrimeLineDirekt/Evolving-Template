# /recall [query] [--type TYPE] [--project PROJECT] [--recent DAYS]

Durchsuche das Experience Memory nach relevanten Erfahrungen.

## Model: haiku

## Arguments
- `query`: Suchbegriffe (optional)
- `--type`: Filter nach Typ (solution, pattern, decision, workaround, gotcha, preference)
- `--project`: Filter nach Projekt
- `--recent`: Nur Experiences der letzten N Tage

## Workflow

### 1. Index laden
Lies `_memory/experiences/index.json`

### 2. Suche durchfuehren

**Ohne Query:**
- Zeige alle Experiences sortiert nach relevance_score

**Mit Query:**
- Suche in: summary, tags, error_pattern (falls vorhanden)
- Matching-Strategien:
  1. Exact Match in Tags
  2. Partial Match in Summary
  3. Regex Match in Error-Pattern
  4. Keyword Match

### 3. Filter anwenden
- `--type`: Nur Experiences dieses Typs
- `--project`: Nur Experiences mit diesem Projekt-Tag
- `--recent N`: created innerhalb der letzten N Tage

### 4. Ergebnisse sortieren
Nach Relevanz-Score (absteigend)

### 5. Ergebnisse anzeigen
```
{count} Experiences gefunden:

[{type}] {id} ({relevance_score}) - {summary}
  Tags: {tags}
  Created: {created}

[{type}] {id} ({relevance_score}) - {summary}
  Tags: {tags}
  Created: {created}

...
```

### 6. Detail-Ansicht (optional)
Falls User eine ID nennt oder "mehr zu {id}":
- Lies `_memory/experiences/{id}.json`
- Zeige vollstaendigen Content
- Inkrementiere access_count
- Update last_accessed

## Beispiele

```
/recall typescript error
→ 5 Experiences gefunden:
  [solution] exp-2025-001 (85) - TypeScript Property Error Fix
  [gotcha] exp-2025-012 (78) - useEffect async Trap
  ...

/recall --type solution
→ Alle Solutions sortiert nach Score

/recall --project dashboard --recent 7d
→ Dashboard-Experiences der letzten Woche

/recall react hooks
→ Alle Experiences zu React Hooks
```

## Plain Text Triggers
- "was wissen wir ueber..."
- "hatten wir das schon mal"
- "such mal nach"
- "recall"
