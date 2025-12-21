# /memory-stats

Zeige Statistiken ueber das Experience Memory System.

## Model: haiku

## Workflow

### 1. Index laden
Lies `_memory/experiences/index.json`

### 2. Statistiken berechnen

**Counts:**
- Total Experiences
- Pro Typ (solution, pattern, decision, workaround, gotcha, preference)

**Scores:**
- Durchschnittlicher Relevanz-Score
- Hoechster Score
- Niedrigster Score

**Access:**
- Meistgenutzte Experience (hoechster access_count)
- Total Accesses

**Tags:**
- Top 10 Tags mit Count

**Cleanup:**
- Experiences mit Score < threshold
- Experiences aelter als threshold_days mit Score < 50

### 3. Output

```
Experience Memory Stats
=======================

Total: {count} Experiences
  - Solutions: {types.solution}
  - Patterns: {types.pattern}
  - Decisions: {types.decision}
  - Workarounds: {types.workaround}
  - Gotchas: {types.gotcha}
  - Preferences: {types.preference}

Scores:
  - Average: {avg_score}
  - Highest: {max_score} ({max_id})
  - Lowest: {min_score} ({min_id})

Most Accessed:
  - {most_accessed_id} ({access_count}x) - {summary}

Top Tags:
  1. {tag1} ({count1})
  2. {tag2} ({count2})
  ...

Cleanup Pending:
  - {cleanup_count} Experiences mit Score < 30
  - Naechster Cleanup: {next_cleanup_date}
```

## Optionen

`/memory-stats full` - Zeigt zusaetzlich:
- Liste aller Experiences mit Scores
- Tag-Cloud
- Zeitliche Verteilung

## Plain Text Triggers
- "memory statistiken"
- "wie viele experiences"
- "experience uebersicht"
