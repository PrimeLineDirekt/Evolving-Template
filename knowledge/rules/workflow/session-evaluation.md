# Session Evaluation Rule

**Priorität**: NIEDRIG (Optional, bei Session-Start)
**Trigger**: Session-Start, wenn unbewertete Sessions existieren
**Quelle**: Mark Kashef - Self-Improving AI Systems Package

---

## Konzept

Sessions werden nach dem 5-Kriterien Rubric bewertet. Bei niedrigem Score wird Learning-Extraktion angeboten.

```
Session-Ende (Hook)
    ↓
Session-Summary erstellt
    ↓
[Nächste Session-Start]
    ↓
Unbewertete Sessions erkennen
    ↓
Rubric-Evaluation anbieten
    ↓
Score speichern (Experience Memory)
    ↓
Score < 3.5? → Learning-Extraktion anbieten
```

---

## Wann triggern?

Bei Session-Start prüfen:

1. Existieren Session-Summaries in `knowledge/sessions/`?
2. Haben diese Sessions noch keine Evaluation? (Marker: `Status: Pending`)
3. Sind sie von den letzten **30 Tagen**?

**Limits**:
- Maximal **3 Sessions** pro Evaluation-Angebot (nicht alle auf einmal)
- Älteste zuerst (FIFO)
- Einmal pro Session anbieten (nicht aufdringlich)

```
"Ich sehe 3 unbewertete Sessions (älteste: 15.12.).
 Soll ich eine kurze Qualitäts-Evaluation machen? (30 Sek pro Session)"
```

---

## Rubric (5 Kriterien)

| Kriterium | Gewicht | Frage |
|-----------|---------|-------|
| **Completeness** | 20% | Wurden alle Aufgaben erledigt? |
| **Depth** | 25% | War die Arbeit gründlich? |
| **Tone** | 15% | Passte die Kommunikation? |
| **Scope** | 20% | Fokussiert geblieben? |
| **Missed Opportunities** | 20% | Hätte mehr gemacht werden können? |

### Scoring Scale

| Score | Label | Bedeutung |
|-------|-------|-----------|
| 5 | Excellent | Übertroffen |
| 4 | Good | Solide Arbeit |
| 3 | Acceptable | Ausreichend |
| 2 | Below Average | Lücken |
| 1 | Poor | Verfehlt |

---

## Evaluation durchführen

### Input: Session-Summary lesen

```
knowledge/sessions/session-YYYY-MM-DD-HHMMSS.md
```

Analysiere:
- Git Commits: Was wurde tatsächlich committed?
- Uncommitted Changes: Wurde Arbeit nicht abgeschlossen?
- Handoff: Wurde dokumentiert?
- Projekt: Welcher Kontext?

### Bewertung

Für jedes Kriterium Score vergeben, dann gewichteter Durchschnitt:

```
overall = (completeness * 0.20) +
          (depth * 0.25) +
          (tone * 0.15) +
          (scope * 0.20) +
          (missed_opportunities * 0.20)
```

### Output: Experience speichern

```json
{
  "type": "session_eval",
  "content": {
    "session_file": "session-2025-12-23-143000.md",
    "scores": {
      "completeness": 4,
      "depth": 4,
      "tone": 5,
      "scope": 3,
      "missed_opportunities": 4
    },
    "overall": 3.95,
    "strengths": ["Gute Commits", "Klare Dokumentation"],
    "weaknesses": ["Scope etwas breit"],
    "action_taken": "none"
  }
}
```

---

## Decision Framework

| Score | Action |
|-------|--------|
| **4.0 - 5.0** | Nur loggen, keine Aktion |
| **3.0 - 3.9** | Fragen: "Soll ich ein Learning extrahieren?" |
| **< 3.0** | Proaktiv: "Diese Session hatte Schwächen. Learning erstellen?" |

---

## Learning-Extraktion (bei Score < 4.0)

Wenn User zustimmt:

1. Session-Summary + Kontext analysieren
2. Kern-Erkenntnis identifizieren
3. Learning erstellen in `knowledge/learnings/`
4. Oder Pattern in `knowledge/patterns/`

Template:
```markdown
# {Titel}

**Quelle**: Session {DATUM}
**Kontext**: {Projekt/Situation}
**Session Score**: {overall}/5

## Was lief nicht optimal?

{Schwächen aus Evaluation}

## Key Insight

{Die Kern-Erkenntnis}

## Für die Zukunft

- {Actionable Takeaway 1}
- {Actionable Takeaway 2}
```

---

## Session-Summary Marker

Nach Evaluation wird dem Session-Summary hinzugefügt:

```markdown
---

## Evaluation

**Score**: 3.95/5 (Good)
**Bewertet**: 2025-12-24

| Kriterium | Score |
|-----------|-------|
| Completeness | 4 |
| Depth | 4 |
| Tone | 5 |
| Scope | 3 |
| Missed Opps | 4 |

**Stärken**: Gute Commits, Klare Dokumentation
**Schwächen**: Scope etwas breit
```

---

## Nicht aufdringlich sein!

- Maximal 1x pro Session anbieten
- Maximal 3 Sessions pro Angebot
- User kann ablehnen: "Nein, nicht nötig"
- Kein Evaluation-Spam bei vielen alten Sessions
- Sessions älter als 30 Tage ignorieren
- Bei "wo waren wir" → Memory Bootup hat Priorität

---

## Integration

Diese Rule ergänzt:
- `domain-memory-bootup.md` - Memory hat Vorrang
- `experience-suggest.md` - session_eval als neuer Type
- `/whats-next` - Erstellt Session-Summary für Evaluation

---

## Beispiel-Flow

```
[Session Start]

Claude: "Willkommen zurück! Projekt: Evolving System.

         Ich sehe 1 unbewertete Session von gestern.
         Kurze Qualitäts-Evaluation? (Dauert 30 Sek)"

User: "Ja"

Claude: [Liest Session-Summary, bewertet]

         "Session vom 23.12.2025:
          - Completeness: 4/5 (alle Tasks erledigt)
          - Depth: 4/5 (gründliche Analyse)
          - Tone: 5/5 (passend)
          - Scope: 3/5 (etwas breit geworden)
          - Missed Opportunities: 4/5 (gut)

          Overall: 3.95/5 (Good)

          Score ist solide. Kein Learning nötig.
          Experience gespeichert."
```

---

## Related

- [Self-Assessment Rubric Pattern](../../knowledge/patterns/self-assessment-rubric-pattern.md)
- [Self-Improving Feedback Loop](../../knowledge/learnings/self-improving-feedback-loop.md)
- [Experience Schema](../../_memory/experiences/SCHEMA.md)
