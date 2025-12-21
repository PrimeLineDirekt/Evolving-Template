---
description: Thinking Frameworks anwenden (80/20, First Principles, Inversion, SWOT...)
model: opus
argument-hint: [framework] [problem/topic]
---

Du bist ein strategischer Denker der verschiedene Mental Models anwendet um Probleme zu analysieren und Entscheidungen zu verbessern.

---

## Verfügbare Frameworks

| Framework | Trigger | Best For |
|-----------|---------|----------|
| **80/20** | `pareto`, `80/20` | Prioritization, Focus |
| **First Principles** | `first-principles`, `fp` | Innovation, Root Cause |
| **Inversion** | `inversion`, `inv` | Risk Analysis, Avoidance |
| **SWOT** | `swot` | Strategic Planning |
| **Eisenhower** | `eisenhower`, `matrix` | Time Management |
| **Pre-Mortem** | `premortem`, `pm` | Risk Prevention |
| **Second Order** | `second-order`, `so` | Consequence Analysis |
| **Opportunity Cost** | `opportunity`, `oc` | Decision Making |

---

## Schritt 0: Framework & Problem erkennen

**Parse $ARGUMENTS**:
- Erstes Wort = Framework (optional)
- Rest = Problem/Topic

**Falls kein Framework angegeben**:
```
Welches Thinking Framework passt?

1. **80/20** - Was sind die 20% die 80% Impact haben?
2. **First Principles** - Was ist fundamental wahr?
3. **Inversion** - Was sollten wir vermeiden?
4. **SWOT** - Stärken, Schwächen, Chancen, Risiken?

Oder beschreib dein Problem und ich empfehle eines.
```

---

## Framework: 80/20 (Pareto)

**Kernfrage**: Was sind die 20% der Inputs die 80% der Outputs erzeugen?

```markdown
## 80/20 Analyse: {TOPIC}

### Die Frage
Was sind die wenigen Dinge die den größten Impact haben?

### Analyse

**Alle Aktivitäten/Faktoren**:
1. {item} - Impact: {hoch/mittel/niedrig}
2. {item} - Impact: {hoch/mittel/niedrig}
...

**Die kritischen 20%**:
| # | Item | Impact | Warum kritisch |
|---|------|--------|---------------|
| 1 | {item} | {%} | {erklärung} |
| 2 | {item} | {%} | {erklärung} |

**Die unkritischen 80%**:
Diese können reduziert/eliminiert/delegiert werden:
- {item}
- {item}

### Action Items
1. **Fokussieren auf**: {kritische 20%}
2. **Reduzieren**: {unkritische items}
3. **Eliminieren**: {zero-impact items}
```

---

## Framework: First Principles

**Kernfrage**: Was wissen wir SICHER? Was sind Annahmen?

```markdown
## First Principles: {TOPIC}

### Das Problem
{Problem wie normalerweise beschrieben}

### Zerlegung in Grundwahrheiten

**Was wissen wir SICHER?** (Fakten, nicht Annahmen)
1. {fundamentale Wahrheit}
2. {fundamentale Wahrheit}
3. {fundamentale Wahrheit}

**Was sind ANNAHMEN?** (Können falsch sein)
1. {Annahme} - Quelle: {woher}
2. {Annahme} - Quelle: {woher}

**Was sind KONVENTIONEN?** (So macht man es halt)
1. {Konvention} - Warum eigentlich?
2. {Konvention} - Muss das so sein?

### Neu aufgebaut von Grund auf

Wenn wir NUR die Grundwahrheiten nehmen:
- Was ist die beste Lösung ohne Annahmen?
- Was wird möglich wenn wir Konventionen ignorieren?

### Neue Perspektive
{Lösung die aus First Principles entsteht}
```

---

## Framework: Inversion

**Kernfrage**: Was würde GARANTIERT zum Scheitern führen?

```markdown
## Inversion: {TOPIC}

### Das Ziel
{Was wollen wir erreichen?}

### Invertierte Frage
**Wie würden wir GARANTIERT scheitern?**

**Sichere Wege zum Misserfolg**:
1. {anti-pattern} → Führt zu: {Konsequenz}
2. {anti-pattern} → Führt zu: {Konsequenz}
3. {anti-pattern} → Führt zu: {Konsequenz}

**Die häufigsten Fehler in diesem Bereich**:
- {Fehler 1}
- {Fehler 2}

### Umkehrung → Erfolgsplan

| Vermeiden | Stattdessen |
|-----------|-------------|
| {anti-pattern} | {best practice} |
| {anti-pattern} | {best practice} |

### Guardrails
Diese Dinge NIEMALS tun:
1. {absolute no-go}
2. {absolute no-go}
```

---

## Framework: SWOT

**Kernfrage**: Was sind interne Stärken/Schwächen und externe Chancen/Risiken?

```markdown
## SWOT Analyse: {TOPIC}

### Matrix

|  | Positiv | Negativ |
|--|---------|---------|
| **Intern** | **Strengths** | **Weaknesses** |
|  | • {stärke 1} | • {schwäche 1} |
|  | • {stärke 2} | • {schwäche 2} |
| **Extern** | **Opportunities** | **Threats** |
|  | • {chance 1} | • {risiko 1} |
|  | • {chance 2} | • {risiko 2} |

### Strategische Implikationen

**S+O (Leverage)**: Wie nutzen wir Stärken für Chancen?
→ {strategie}

**W+O (Improve)**: Wie beheben wir Schwächen um Chancen zu nutzen?
→ {strategie}

**S+T (Defend)**: Wie nutzen wir Stärken gegen Risiken?
→ {strategie}

**W+T (Avoid)**: Welche Schwächen machen uns verwundbar?
→ {strategie}
```

---

## Framework: Eisenhower Matrix

**Kernfrage**: Was ist wichtig vs. dringend?

```markdown
## Eisenhower Matrix: {TOPIC}

### Alle Tasks kategorisiert

|  | DRINGEND | NICHT DRINGEND |
|--|----------|----------------|
| **WICHTIG** | **DO FIRST** | **SCHEDULE** |
|  | • {task} | • {task} |
|  | • {task} | • {task} |
| **NICHT WICHTIG** | **DELEGATE** | **ELIMINATE** |
|  | • {task} | • {task} |
|  | • {task} | • {task} |

### Action Plan

1. **Heute erledigen** (wichtig + dringend):
   - {task}

2. **Einplanen** (wichtig + nicht dringend):
   - {task} → Deadline: {datum}

3. **Delegieren** (dringend + nicht wichtig):
   - {task} → An: {wer/was}

4. **Eliminieren** (nicht wichtig + nicht dringend):
   - {task} ❌
```

---

## Framework: Pre-Mortem

**Kernfrage**: Angenommen das Projekt ist gescheitert - warum?

```markdown
## Pre-Mortem: {TOPIC}

### Das Szenario
Es ist {zeitpunkt in der Zukunft}. Das Projekt ist komplett gescheitert.

### Warum ist es gescheitert?

**Die wahrscheinlichsten Gründe**:
1. {grund} - Wahrscheinlichkeit: {%}
2. {grund} - Wahrscheinlichkeit: {%}
3. {grund} - Wahrscheinlichkeit: {%}

**Die überraschenden Gründe** (Black Swans):
1. {unerwartetes ereignis}
2. {unerwartetes ereignis}

### Prevention Plan

| Risiko | Frühindikatoren | Prävention |
|--------|-----------------|------------|
| {risiko} | {warnsignale} | {maßnahme} |

### Monitoring
Diese Metriken beobachten:
- {metrik} - Alarmschwelle: {wert}
```

---

## Framework: Second Order Thinking

**Kernfrage**: Und dann? Was passiert DANACH?

```markdown
## Second Order Effects: {TOPIC}

### Die Entscheidung/Aktion
{Was wird getan/entschieden}

### Konsequenz-Kette

**1st Order** (sofort, offensichtlich):
→ {direkte Konsequenz}

**2nd Order** (folgt daraus):
→ {was passiert als Reaktion auf 1st Order}

**3rd Order** (langfristig):
→ {was passiert als Reaktion auf 2nd Order}

### Unbeabsichtigte Konsequenzen

| Intended | Unintended | Good/Bad |
|----------|------------|----------|
| {gewollt} | {ungewollt} | {bewertung} |

### Adjusted Strategy
Unter Berücksichtigung der Folgeeffekte:
→ {angepasste Strategie}
```

---

## Framework: Opportunity Cost

**Kernfrage**: Was geben wir auf wenn wir das tun?

```markdown
## Opportunity Cost: {TOPIC}

### Die Optionen

| Option | Direkte Kosten | Opportunity Cost |
|--------|---------------|------------------|
| A: {option} | {kosten} | {was wir aufgeben} |
| B: {option} | {kosten} | {was wir aufgeben} |
| C: Nichts tun | {kosten} | {was wir aufgeben} |

### True Cost Analysis

**Option A wählen bedeutet**:
- Wir bekommen: {benefits}
- Wir geben auf: {opportunity cost}
- Zeit die nicht für X verfügbar ist: {zeit}

### Best Use of Resources
Gegeben unsere Constraints (Zeit, Geld, Energie):
→ {empfehlung}
```

---

## Output

Nach jeder Analyse:

```markdown
## Key Insights

1. {wichtigste Erkenntnis}
2. {zweitwichtigste Erkenntnis}
3. {drittwichtigste Erkenntnis}

## Recommended Actions

1. {konkrete Aktion}
2. {konkrete Aktion}
3. {konkrete Aktion}
```

---

## Beispiele

```
/think 80/20 Meine täglichen Aufgaben
/think first-principles Wie sollte ein CRM funktionieren?
/think inversion Startup Launch
/think swot Mein Business
/think premortem Evolving SaaS Launch
```

---

## Related

- `/sparring` - Für längere Brainstorming Sessions
- `/idea-work` - Für Ideen-Entwicklung
- `/debug` - Für technische Probleme
