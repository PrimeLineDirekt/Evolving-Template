---
description: Automatische Model-Auswahl basierend auf Task-Komplexität
model: haiku
argument-hint: [task description]
---

# Auto Model Selection

Analysiere die Task-Beschreibung und empfehle das optimale Model.

## Input

**Task**: $ARGUMENTS

## Self-Assessment

Führe Metacognitive Analyse durch:

```xml
<task_analysis>
  <complexity_indicators>
    Multi-step erforderlich: [ja/nein]
    Domain-Expertise nötig: [keine/etwas/tief]
    Reasoning-Tiefe: [flach/mittel/tief]
    Output-Komplexität: [einfach/strukturiert/umfassend]
    Ambiguität: [klar/mittel/hoch]
  </complexity_indicators>

  <requirements_check>
    □ Code-Generierung
    □ Research/Recherche
    □ Kreative Ideation
    □ Risiko-Bewertung
    □ Multi-Perspektiven
    □ Strategische Planung
  </requirements_check>
</task_analysis>
```

## Scoring

| Complexity Score | Model |
|------------------|-------|
| 1-3 | **Haiku** - Schnell, günstig, ausreichend |
| 4-6 | **Sonnet** - Balanced, gute Qualität |
| 7-10 | **Opus** - Maximum Quality für komplexe Tasks |

## Entscheidung

Basierend auf der Analyse:

```
Complexity Score: {X}/10
Empfohlenes Model: {haiku|sonnet|opus}
Confidence: {high|medium|low}

Begründung: {Warum dieses Model}
```

## Quick-Use

Falls Confidence HIGH:
→ Zeige Empfehlung und frage: "Soll ich mit {Model} fortfahren?"

Falls Confidence MEDIUM:
→ Zeige Alternativen: "Haiku für schnelle Antwort, Opus für tiefe Analyse - was bevorzugst du?"

Falls Confidence LOW:
→ Frage nach Klarstellung: "Könntest du den Task genauer beschreiben?"

---

**Hinweis**: Nutze `/opus`, `/sonnet`, oder `/haiku` für direkten Model-Wechsel.
