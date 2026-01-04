# Auto-Enhancement Thinking Pattern

**Priorität**: STANDARD
**Trigger**: Bei JEDER Anfrage automatisch im Denken anwenden

## Konzept

Bessere Ergebnisse ohne extra Schritte durch automatisches Prompt-Enhancement in meinem Thinking-Prozess.

```
User Request → [Auto-Enhancement] → Bessere Antwort
```

Der User sieht nur die verbesserte Antwort, nicht den Enhancement-Prozess.

---

## Schritt 1: Complexity Assessment

**Bei JEDER Anfrage** klassifiziere ich intern die Komplexität:

| Level | Signale | Beispiel | Enhancement |
|-------|---------|----------|-------------|
| 1 | Fakten-Frage | "Was ist X?", "Definiere..." | Keine |
| 2 | Erklärung nötig | "Erkläre...", "Wie funktioniert..." | + Struktur |
| 3 | Multi-Step Task | "Erstelle...", "Implementiere..." | + Phasen |
| 4 | Research/Strategie | "Analysiere...", "Plane...", "Entwickle..." | + Multi-Perspektive |
| 5 | Strict/Edge Case | "Validiere exakt...", "Prüfe strikt..." | + Validation |

**Keyword-Heuristiken:**

```
Level 1: "was ist", "definiere", "wann", "wo", "wer"
Level 2: "erkläre", "wie", "warum", "vergleiche", "beschreibe"
Level 3: "erstelle", "implementiere", "baue", "entwickle feature"
Level 4: "recherchiere", "analysiere tief", "strategie", "plane"
Level 5: "validiere", "prüfe strikt", "exaktes format"
```

---

## Schritt 2: Context Extraction (Level 2+)

Falls Komplexität ≥ Level 2, sammle automatisch relevanten Kontext:

### 2.1 Session Context (Höchste Priorität)
- Was wurde in dieser Session besprochen?
- Welche Entscheidungen wurden getroffen?
- Welche Constraints wurden erwähnt?

### 2.2 Domain Memory
```
Lies _memory/index.json → Aktives Projekt
Lies _memory/projects/{active}.json → Goals, State, Progress
```

### 2.3 Knowledge Base (Keyword-matched)
- Relevante Patterns aus `knowledge/patterns/`
- Relevante Learnings aus `knowledge/learnings/`
- Projekt-spezifisches Wissen

### 2.4 Experience Memory
- Ähnliche gelöste Probleme aus `_memory/experiences/`
- User-Präferenzen

---

## Schritt 3: Intern Prompt verbessern (Level 2+)

Formuliere in meinem Denken einen reichhaltigeren Prompt:

### Level 2 Enhancement
```
Original + Struktur + Kontext + Beispiele

"Erkläre mir React Hooks"
→ "Erkläre React Hooks im Kontext von {aktuellem Projekt},
   strukturiert nach: Konzept, Wichtige Hooks, Best Practices,
   Häufige Fehler, Code-Beispiele"
```

### Level 3 Enhancement
```
Original + Phasen + Erfolgskriterien + Kontext

"Erstelle einen API Endpoint"
→ "Erstelle API Endpoint für {Projekt} mit:
   Phase 1: Design (Endpoints, Models)
   Phase 2: Security (Auth, Validation)
   Phase 3: Implementation
   Erfolg: Sichere Passwörter, JWT, Error Handling"
```

### Level 4 Enhancement
```
Original + Multi-Perspektive + Confidence + Deep Analysis

"Analysiere meinen Markt"
→ "Analysiere Markt für {Produkt/Projekt}:
   - Perspektive 1: Kundensicht
   - Perspektive 2: Wettbewerb
   - Perspektive 3: Trends
   Confidence-Score für jede Aussage
   Quellen validieren"
```

### Level 5 Enhancement
```
Original + Strict Validation + Format + Prefill

"Validiere diese Config"
→ "Validiere {Config} strikt gegen Schema:
   - Pflichtfelder prüfen
   - Typen validieren
   - Constraints einhalten
   Output exakt im Format: {Schema}"
```

---

## Schritt 4: Antwort geben

**Wichtig**: Der User sieht NUR die bessere Antwort.

- Kein "Ich habe deinen Prompt verbessert"
- Kein "Ich wende Auto-Enhancement an"
- Einfach bessere, strukturiertere, fundiertere Qualität

---

## Wann NICHT enhancen?

| Situation | Verhalten |
|-----------|-----------|
| Level 1 Fragen | Direkt antworten |
| User sagt "kurz" / "schnell" | Kein Enhancement |
| Triviale Tasks | Direkt antworten |
| User fragt nach raw/unenhanced | Kein Enhancement |

---

## Context Degradation Awareness

**Quelle**: Agent-Skills-for-Context-Engineering Deep Dive

### Das Problem

Context Extraction kann zu Degradation führen:
- Zu viel Memory geladen → Lost-in-the-Middle
- Irrelevante Patterns → Context Poisoning
- Alle Experiences → Context Distraction

### Lösung: SELECT before EXTRACT

Bei Context Extraction (Schritt 2) das 4-Bucket Framework anwenden:

```
NICHT: Lade ALLES was relevant sein könnte
SONDERN: Selektiere die TOP-3 relevantesten Quellen

1. Session Context → Immer (bereits im Context)
2. Domain Memory → Nur aktives Projekt, kompakt
3. Knowledge Base → Max 2 relevante Patterns
4. Experiences → Nur Top-1 mit Score > 50
```

### Relevanz-Heuristik

| Kontext-Typ | Wann laden? | Max Token Budget |
|-------------|-------------|------------------|
| Session Context | Immer | (bereits da) |
| Domain Memory | Wenn Projekt-relevant | ~2K tokens |
| Patterns | Wenn Task matcht | ~1K tokens |
| Experiences | Wenn Fehler/Decision | ~500 tokens |

### Counterintuitive Rule

> "Ein einzelner irrelevanter Kontext-Chunk triggert bereits Degradation!"

Lieber zu WENIG Kontext als zu VIEL.

Bei Unsicherheit: Nur Session Context + Domain Memory, keine Patterns/Experiences.

---

## Beispiel-Flow

### Ohne Enhancement (Level 1):
```
User: "Was ist TypeScript?"
Claude: [Direkte, prägnante Antwort]
```

### Mit Enhancement (Level 3):
```
User: "Hilf mir mit meiner Etsy SEO"

Claude (intern):
  Complexity: Level 3 (Multi-Step Task)
  Context:
    - Projekt: {PROJECT}
    - Bekannt: Etsy SEO Patterns, Pinterest Integration
    - Learnings: Title-Optimierung wichtig

  Enhanced Prompt:
    "Unterstütze bei Etsy SEO für {PROJECT}:
     Phase 1: Keyword-Analyse (mit bekannten Tools)
     Phase 2: Title-Optimierung (Learning anwenden)
     Phase 3: Tag-Strategie
     Phase 4: Pinterest-Integration
     Erfolg: Bessere Rankings, mehr Traffic"

Claude (extern):
  [Strukturierte, fundierte Antwort mit Projekt-Bezug,
   aufgeteilt in klare Phasen, mit konkreten Empfehlungen]
```

---

## Integration mit anderen Rules

Diese Rule arbeitet zusammen mit:
- `domain-memory-bootup.md` - Memory-Kontext laden
- `experience-suggest.md` - Erfahrungen einbeziehen
- `workflow-detection.md` - Komplexe Tasks erkennen
- `context-optimization.md` - 4-Bucket Framework, Degradation Prevention

---

## Metriken (für Selbst-Evaluation)

Nach Antworten mental prüfen:
- War der Kontext hilfreich?
- Hätte weniger Enhancement gereicht?
- War die Struktur angemessen?

Bei Feedback anpassen.
