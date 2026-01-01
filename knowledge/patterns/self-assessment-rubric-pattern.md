# Self-Assessment Rubric Pattern

**Quelle**: Mark Kashef - Self-Improving AI Systems Package
**Typ**: Evaluation Pattern
**Anwendung**: Output-Qualitätsbewertung, Agent-Evaluation, Experience-Scoring

---

## Konzept

AI-Outputs systematisch nach 5 gewichteten Kriterien bewerten.
Ermöglicht: Selbst-Evaluation, Quality Gates, automatische Verbesserungen.

---

## Die 5 Kriterien

| Kriterium | Gewicht | Frage |
|-----------|---------|-------|
| **Completeness** | 20% | Wurde alles beantwortet? (explizit + implizit) |
| **Depth** | 25% | Genug Detail und Insight? (nicht nur Oberfläche) |
| **Tone** | 15% | Kommunikationsstil passend? (Level-Match) |
| **Scope** | 20% | Fokussiert geblieben? (nicht off-topic) |
| **Missed Opportunities** | 20% | Was wurde übersehen? (Proaktivität) |

---

## Scoring Scale (1-5)

| Score | Label | Beschreibung |
|-------|-------|--------------|
| **5** | Excellent | Übertrifft Erwartungen, keine Verbesserung möglich |
| **4** | Good | Erfüllt Erwartungen, kleine Verbesserungsbereiche |
| **3** | Acceptable | Ausreichend, aber klar verbesserbar |
| **2** | Below Average | Merkliche Lücken, beeinträchtigt Nützlichkeit |
| **1** | Poor | Verfehlt grundlegende Erwartungen |

---

## Detaillierte Kriterien-Definitionen

### 1. Completeness (20%)

**Prüfe:**
- Alle expliziten Fragen beantwortet
- Alle impliziten Fragen adressiert
- Keine Key-Points übersprungen
- Logischer Fluss von Frage zu Antwort

**Common Failures:**
- Nur Teil einer Multi-Part-Frage beantwortet
- "Why" ignoriert wenn "What and Why" gefragt
- Antwort ohne nötigen Kontext

### 2. Depth (25%)

**Prüfe:**
- Reasoning erklärt, nicht nur Conclusionen
- Spezifische Beispiele wo angebracht
- Edge Cases/Nuancen erwähnt
- Technische Genauigkeit auf richtigem Level

**Common Failures:**
- Generische Antworten die auf alles passen
- Optionen listen ohne Entscheidungshilfe
- Offensichtliches sagen ohne Mehrwert

### 3. Tone (15%)

**Prüfe:**
- Match zum Expertise-Level des Users
- Angemessene Formalität
- Hilfreich ohne herablassend
- Confident ohne dismissive

**Common Failures:**
- Over-Explaining für Experten
- Zu knapp für Anfänger
- Unnötiges Hedging
- Roboterhaft/formelhaft

### 4. Scope (20%)

**Prüfe:**
- Direkt relevant zur Frage
- Keine unnötigen Tangenten
- Richtige Menge Kontext
- Klar was essentiell vs. supplementär

**Common Failures:**
- Ungefragte Information inkludieren
- Tangenten die User nicht helfen
- Textbook-Antwort wenn Quick-Answer gebraucht
- Fehlender Kontext der Antwort nützlich macht

### 5. Missed Opportunities (20%)

**Prüfe:**
- Follow-Up Fragen die helfen würden
- Related Information die User wahrscheinlich braucht
- Warnungen/Considerations nicht erwähnt
- Alternative Ansätze nicht angeboten

**Common Failures:**
- Nächste Frage nicht antizipiert
- Offensichtliche Pitfalls nicht gewarnt
- Kein besseres Problem-Framing angeboten
- Breiteren Kontext nicht verbunden

---

## Decision Framework

```
Score berechnen (gewichteter Durchschnitt)
           │
           ▼
    ┌──────────────┐
    │ Score >= 4.0 │───Yes──▶ ACTION: NONE (nur loggen)
    └──────────────┘
           │ No
           ▼
    ┌──────────────┐
    │ Score >= 3.0 │───Yes──▶ ACTION: SUGGESTION (Human Review)
    └──────────────┘
           │ No
           ▼
    ┌──────────────┐
    │ Score >= 2.0 │───Yes──▶ ACTION: AUTO-UPDATE (automatisch verbessern)
    └──────────────┘
           │ No
           ▼
    ACTION: ESCALATE (Sofortige Aufmerksamkeit)
```

| Action | Score Range | Was passiert |
|--------|-------------|--------------|
| **None** | 4.0 - 5.0 | Log the reflection, keine Änderungen |
| **Suggestion** | 3.0 - 3.9 | Vorschlag für Human Review |
| **Auto-Update** | 2.0 - 2.9 | Automatisch verbesserten Output generieren |
| **Escalate** | 1.0 - 1.9 | Sofortige Aufmerksamkeit, Auto-Updates pausieren |

---

## Override Conditions

Auch bei akzeptablen Scores Aktion triggern wenn:

```javascript
const OVERRIDE_CONDITIONS = {
  // Einzelnes Kriterium sehr niedrig
  anyCriterionBelow2: (scores) =>
    Object.values(scores).some(s => s < 2),

  // Konsistenter Abwärtstrend
  decliningTrend: (current, lastThree) =>
    lastThree.every(s => s > current),

  // Hohe Varianz in einem Kriterium
  inconsistentPerformance: (recent) =>
    standardDeviation(recent) > 1.0,

  // Wiederholte spezifische Schwäche
  repeatedWeakness: (reflections) =>
    reflections.filter(r =>
      r.weaknesses.includes('shallow responses')).length >= 3
};
```

---

## Ruthless Critic Variation

Für Stress-Testing oder wenn Scores zu hoch scheinen.

**Mindset:**
- Score 5 ist nahezu unmöglich
- "Pretty good" = Score 3, nicht 4
- Spezifische Schwäche finden, nicht vage loben

**Scoring Adjustment:**
| Normal Assessment | Ruthless Score |
|-------------------|----------------|
| "Excellent" | 4 (max) |
| "Good" | 3 |
| "Okay" | 2 |
| "Has problems" | 1 |

**Red Flags (auto -1 Punkt):**

*Completeness:*
- "Let me know if you want more details"
- User müsste Follow-Up fragen um nützlich zu sein

*Depth:*
- Statement das auf alles passen könnte
- What ohne Why erklären

*Tone:*
- Unnötiges Hedging ("I think maybe...")
- Formulaic phrases ("Great question!")

*Scope:*
- >20% der Antwort ist Context-Setting
- Frage zurück wiederholen

*Missed Opportunities:*
- Offensichtliches Follow-Up nicht antizipiert
- Relevant Warning nicht erwähnt

**Wann nutzen:**
- System scheint zu zufrieden (Scores immer 4+)
- Neuen Prompt vor Deployment testen
- Untersuchen warum User unzufrieden scheinen

---

## Gewichtung nach Use-Case

| Use Case | Betonen | De-betonen |
|----------|---------|------------|
| **Customer Support** | Completeness, Tone | Depth |
| **Technical Docs** | Depth, Completeness | Tone |
| **Sales/Marketing** | Tone, Missed Opportunities | Scope |
| **Code Review** | Depth, Scope | Tone |
| **Sparring/Ideation** | Missed Opportunities, Depth | Completeness |

---

## Reflection Output Format

```json
{
  "overall_score": 4.2,
  "action_taken": "none",
  "scores": {
    "completeness": 4,
    "depth": 4,
    "tone": 5,
    "scope": 4,
    "missed_opportunities": 4
  },
  "strengths": [
    "Clear recommendation with reasoning",
    "Actionable steps provided"
  ],
  "weaknesses": [
    "Could mention middleware setup",
    "Security considerations not addressed"
  ],
  "patterns_noticed": [],
  "suggested_improvements": null
}
```

---

## Integration in Evolving

### Für Experience Memory
Ersetze einfachen `relevance_score` durch strukturierten Rubric-Score.

### Für Agent-Outputs
Nach Agent-Ausführung optional evaluieren:
```
Agent Output → Self-Assessment → Score < 4? → Refinement Loop
```

### Für Session-End
Session-Qualität mit Rubric bewerten → Learnings extrahieren.

### Für `/sparring`
Ruthless Critic Mode für Devil's Advocate aktivieren.

---

## Beispiel: Passing vs. Failing

**Passing (Score 4.2):**
> "For Next.js 14, I'd recommend NextAuth.js. Here's why:
> - Built for Next.js with App Router support
> - Handles OAuth providers out of the box
> Quick setup: 1. npm install... 2. Create route... 3. Configure...
> Alternative: Clerk or Supabase Auth if you need more control.
> Want me to walk through implementation?"

**Failing (Score 2.1):**
> "There are several ways to handle authentication. You could use
> NextAuth.js, Clerk, Auth0, or implement your own. Each has pros
> and cons depending on your needs. Let me know if you want details!"

**Warum Failing:**
- Listet ohne zu empfehlen
- "Pros and cons depending on needs" = leere Aussage
- "Let me know" = Deflection statt Engagement
- Keine actionable Information

---

## Related

- [Reflection Pattern](reflection-pattern.md) - Generator → Critic → Refiner
- [Experience Memory](_memory/experiences/SCHEMA.md) - Score-basiertes Filtering
- [Metacognitive Pattern](metacognitive-self-assessment-pattern.md) - Self-Assessment

---

**Erstellt**: 2025-12-23
**Quelle**: Mark Kashef - Self-Improving AI Systems Package
