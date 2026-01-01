# Self-Improving Feedback Loop Architecture

**Quelle**: Mark Kashef - Self-Improving AI Systems Package
**Typ**: Architecture Learning
**Relevanz**: Evolving System Enhancement

---

## Kernkonzept: Der Paradigmenwechsel

### Linear (Alt)
```
User Input → LLM → Response → Done
```
**Probleme:**
- Qualität degradiert über Zeit
- Human Bottleneck für Verbesserungen
- Kein institutionelles Gedächtnis
- Gleiche Fehler wiederholt

### Self-Improving Loop (Neu)
```
User Input → LLM → Response
                ↓
         Store in Database
                ↓
         Periodic Reflection ←────────┐
                ↓                     │
         Evaluation (AI-as-Judge)     │
                ↓                     │
         Score < Threshold?           │
                ↓ Yes                 │
         Generate Improvement         │
                ↓                     │
         Update System Prompt         │
                ↓                     │
         Better Future Responses ─────┘
```

**Key Insight**: AI evaluiert eigene Outputs, identifiziert Schwächen, schreibt eigene Instructions um. Human setzt Kriterien, System optimiert.

---

## Feedback Loop Flow (4 Schritte)

### Step 1: Chat
```
User Message → Chat Handler → Response mit active prompt v3
                    ↓
         Store beide Messages mit prompt_version: 3
```

**Kritisch**: Jede Message wird mit `prompt_version` getaggt für spätere A/B Analyse.

### Step 2: Reflection (Trigger: Zeit oder Volumen)
```
Reflection Loop triggered
        ↓
Query: Get last 20 conversations (24h window)
        ↓
EVALUATOR AI (Claude as Judge)
  Input:
    - 20 conversations
    - Current system prompt
    - Evaluation rubric
  Output:
    - Scores (Completeness, Depth, Tone, Scope, Missed Opps)
    - Overall Score
    - Weaknesses identified
        ↓
DECISION LOGIC
  if (overall >= 4.0) → NONE
  if (overall >= 3.0) → SUGGESTION (human review)
  if (overall < 3.0)  → AUTO_UPDATE
```

### Step 3: Prompt Update (wenn triggered)
```
Prompt Updater
  Input:
    - Current prompt (v3)
    - Weaknesses: ["shallow", "no follow-ups"]
  Output:
    - New prompt (v4) mit Verbesserungen
        ↓
DATABASE UPDATE
  - Deactivate v3
  - Insert v4 as active
```

### Step 4: Improved Responses
```
Next user message uses prompt v4
Response quality improves
Cycle continues...
```

---

## Safety Nets (KRITISCH)

### 1. Cooldown Period
**Problem**: Zu häufige Updates → Instabilität

```javascript
const COOLDOWN_HOURS = 6;

async function canRunReflection() {
  const lastLog = await getLastReflection();
  if (!lastLog) return true;

  const hoursSince = (Date.now() - lastLog.created_at) / (1000 * 60 * 60);
  return hoursSince >= COOLDOWN_HOURS;
}
```

### 2. Update Thresholds
**Problem**: Minor Fluctuations → Unnötige Changes

```javascript
const THRESHOLDS = {
  autoUpdate: 2.5,    // Below: auto-update
  suggestion: 3.5,    // Below: create suggestion
  acceptableMin: 4.0, // Below: log for monitoring
};

function decideAction(scores) {
  if (scores.overall < THRESHOLDS.autoUpdate) return 'prompt_update';
  if (scores.overall < THRESHOLDS.suggestion) return 'suggestion';
  if (scores.overall < THRESHOLDS.acceptableMin) return 'log_only';
  return 'none';
}
```

### 3. Maximum Update Frequency
**Problem**: Rapid consecutive updates = Instabilität

```javascript
const MAX_UPDATES_PER_DAY = 3;

async function hasReachedUpdateLimit() {
  const count = await getUpdatesLast24h();
  return count >= MAX_UPDATES_PER_DAY;
}
```

### 4. Version Control & Rollback
**Problem**: Bad prompt update → alle Responses degradieren

```javascript
async function rollbackPrompt(targetVersion) {
  // 1. Deactivate current
  await deactivateCurrentPrompt();

  // 2. Activate target version
  await activatePrompt(targetVersion);

  // 3. Log the rollback
  await logAction('rollback', targetVersion);
}
```

### 5. Human Override (Locked Prompts)
```sql
ALTER TABLE system_prompts ADD COLUMN locked BOOLEAN DEFAULT false;

-- Locked prompts can't be auto-deactivated
-- Reflection loop checks: WHERE is_active = true AND locked = false
```

**Humans können immer:**
- Auto-updates temporär deaktivieren
- Alle Updates manuell approven
- Spezifische Prompt-Version erzwingen
- Pending Suggestions reviewen

---

## Reflection Trigger Optionen

| Trigger | Beschreibung | Empfehlung |
|---------|--------------|------------|
| **Time-based** | Cron job every 6-24h | Stabil, vorhersehbar |
| **Volume-based** | After every N messages | Responsive, aber variable |
| **Manual** | Admin endpoint | Für Testing |

**Start**: Every 12 hours mit minimum 10 conversations.

---

## Score Interpretation

| Score | Label | Action |
|-------|-------|--------|
| 4.5 - 5.0 | Excellent | None - system performs well |
| 3.5 - 4.4 | Good | Log patterns, consider suggestions |
| 2.5 - 3.4 | Needs Improvement | Generate suggestion for review |
| 1.0 - 2.4 | Poor | Auto-update prompt if enabled |

---

## Integration in Evolving

### Was wir schon haben (ähnlich):
- `_memory/` - Domain Memory (Session-Persistenz)
- `_memory/experiences/` - Experience Memory
- `_handoffs/` - Session-Übergaben
- `.claude/rules/` - Self-Improving Rules

### Was NEU wäre:
1. **Automatische Reflection Loop** - Periodische Selbst-Evaluation
2. **Rubric-basierte Scores** - Strukturierte Bewertung (→ siehe Rubric Pattern)
3. **Version Tracking** - Outputs mit Rule-Version taggen
4. **Safety Nets** - Cooldown, Thresholds, Rollback

### Mögliche Implementation:

**Light (Rules-basiert):**
- Session-End Hook mit Rubric-Evaluation
- Score → Experience Memory loggen
- Bei niedrigem Score → Suggestion für Rule-Update

**Medium (Hook-basiert):**
- Stop-Hook evaluiert Session-Qualität
- Automatischer Suggestion-Eintrag in `_memory/suggestions/`
- Manuelles Review und Rule-Updates

**Deep (Automatisch):**
- Eigener Reflection-Agent
- Automatische Rule-Updates bei Score < Threshold
- Rollback-Mechanismus für Rules

---

## Relevante Safety Nets für Evolving

| Safety Net | Evolving Equivalent |
|------------|---------------------|
| Cooldown Period | Min. 1 Session zwischen Rule-Updates |
| Update Threshold | Score < 3.5 → Suggestion, < 2.5 → Update |
| Max Updates/Day | Max 2 Rule-Changes pro Tag |
| Version Control | Git für `.claude/rules/` |
| Human Override | Manuelle Approval für kritische Rules |

---

## North Star Guardrails (KRITISCH)

Schutz gegen "Adversarial Drift" - verhindert dass das System sich in die falsche Richtung verbessert.

### Meta-Prompt für den Evaluator

Der Reflection-Agent braucht eigene Guardrails:

```
1. "Du evaluierst einen Bot für [DOMAIN]"
2. "Der Bot sollte NICHT erweitert werden um Themen außerhalb [DOMAIN] zu behandeln"
3. "Wenn User off-topic fragen, ist das KEIN Prompt-Problem - der Bot handelt korrekt"
4. "Nur Änderungen vorschlagen die den Bot BESSER in [DOMAIN] machen - nicht breiter"
5. "Schütze gegen adversarial drift durch wiederholte seltsame Anfragen"
```

### Don't Over-Correct Prinzip

**UPDATE nur wenn:**
- Average Score < 3.5/5
- ODER gleiche Schwäche erscheint 3+ mal
- ODER spezifische Knowledge Gap wiederholt auftaucht

**MAINTAIN (kein Update) wenn:**
- Scores generell gut (>3.5)
- Issues sind one-off Edge Cases
- "Problem" ist User-Error oder Out-of-Scope
- Kürzlich gab es Updates (Cooldown aktiv)

### Für Evolving anwenden

Bei Self-Improving Rules:
- Rule nicht ändern nur weil ein User etwas Unerwartetes fragte
- Pattern-Erkennung: Mindestens 3 ähnliche Issues bevor Änderung
- Scope beibehalten: Rules machen Evolving besser, nicht generischer

---

## Takeaways

1. **Feedback Loop ist der Kern** - Store → Reflect → Evaluate → Improve
2. **Safety Nets sind kritisch** - Ohne sie: instabiles System
3. **Version Tracking ermöglicht A/B** - Welcher Prompt/Rule performt besser?
4. **Human Override immer behalten** - System kann sich nicht selbst locken

---

## Related

- [Self-Assessment Rubric Pattern](../patterns/self-assessment-rubric-pattern.md) - 5-Kriterien Scoring
- [Self-Improving Rules Pattern](../patterns/self-improving-rules-pattern.md) - Bestehende Rule-Evolution
- [Experience Memory Schema](../../_memory/experiences/SCHEMA.md) - Score-basiertes Filtering
- [Memory Decay Pattern](memory-decay-pattern.md) - Relevanz über Zeit

---

**Erstellt**: 2025-12-23
**Quelle**: Mark Kashef - Self-Improving AI Systems Package
