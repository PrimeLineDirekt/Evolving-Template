# Prompt Coach Analysis Methodology

> > **Type**: Learning / Prompt Quality Analysis
> **Relevance**: HIGH - Komplementiert unser prompt-pro-framework

## Konzept

**prompt-pro-framework**: ERSTELLT optimierte Prompts
**prompt-coach**: ANALYSIERT existierende Prompts, findet Schwächen

Zusammen bilden sie einen Complete Prompt Lifecycle:
```
Erste Iteration → prompt-pro-framework (Creation)
                       ↓
                 Nutzung im Alltag
                       ↓
          prompt-coach (Analysis & Feedback)
                       ↓
           Verbesserte Prompts erstellen
```

## 8-Dimensionale Analyse

### 1. Token Usage & Cost Analysis

```typescript
interface TokenAnalysis {
  input_tokens: number;
  output_tokens: number;
  cost: number;
  model: 'opus' | 'sonnet' | 'haiku';
}

// Wichtig: Deduplication für Streaming Logs
const uniqueCalls = new Set(
  logs.map(log => `${log.message.id}-${log.requestId}`)
);
```

**Model Pricing (Stand 2025)**:
| Model | Input | Output |
|-------|-------|--------|
| Opus | $15/1M | $75/1M |
| Sonnet | $3/1M | $15/1M |
| Haiku | $0.25/1M | $1.25/1M |

### 2. Prompt Quality Scoring

**4 Dimensionen** (jeweils 0-10):

| Dimension | Frage | Gewicht |
|-----------|-------|---------|
| **Clarity** | Ist die Anfrage unmissverständlich? | 30% |
| **Specificity** | Enthält sie alle nötigen Infos? | 30% |
| **Actionability** | Kann Claude sofort handeln? | 25% |
| **Scope** | Ist der Umfang angemessen? | 15% |

**Gesamtscore**: Gewichteter Durchschnitt

### 3. Context-Aware Scoring

**Kritischer Insight**: Kürze ist nicht automatisch schlecht!

```
Score hoch (8-10/10) TROTZ Kürze, wenn:
- Claude hat Environmental Context (git diff, recent files)
- Prompt antwortet auf Claude's Frage ("yes", "1", "2")
- Konversations-History gibt Referenz ("it", "this")
- Standard-Operations (git commit, run tests)

Score niedrig (0-4/10) bei:
- "fix the bug" ohne Datei, Error, Context
- "optimize it" ohne Success Criteria
- "update the component" mit mehreren Kandidaten
```

### 4. Tool Usage Analysis

```typescript
interface ToolUsage {
  tool: string;
  count: number;
  category: 'builtin' | 'mcp';
}

// Unternutzte Tools identifizieren
const underutilized = tools.filter(t =>
  t.count < averageCount * 0.3 &&
  isHighValueTool(t.tool)
);
```

### 5. Session Efficiency

```typescript
interface SessionMetrics {
  iterations_per_task: number;      // Niedriger = besser
  clarification_requests: number;   // Niedriger = besser Prompts
  completion_rate: number;          // Höher = besser
  time_to_completion: number;       // Niedriger = besser
}
```

### 6. Productivity Patterns

```typescript
interface ProductivityAnalysis {
  peak_hours: number[];           // z.B. [9, 10, 14, 15]
  peak_days: string[];            // z.B. ["Tuesday", "Wednesday"]
  average_session_length: number;
  focus_blocks: TimeRange[];
}
```

### 7. File Modification Heatmap

```typescript
interface FileHotspot {
  path: string;
  edit_count: number;
  lines_changed: number;
  last_modified: Date;
}

// Top 10 meistbearbeitete Files
const hotspots = files
  .sort((a, b) => b.edit_count - a.edit_count)
  .slice(0, 10);
```

### 8. Error & Recovery Analysis

```typescript
interface ErrorPattern {
  error_type: string;
  frequency: number;
  avg_recovery_time: number;  // Minuten
  common_fixes: string[];
}
```

## The Golden Rule

> **"Zeige deinen Prompt einem Kollegen mit minimalem Kontext. Wenn er verwirrt ist, wird Claude es auch sein."**

Claude behandeln wie einen fähigen, aber neu eingestellten Teammitglied:
- Hat alle Fähigkeiten
- Braucht vollständige Instruktionen
- Kennt DEINEN spezifischen Kontext nicht

## Anti-Pattern Katalog

### Missing File Context

```
❌ "fix the bug"
✅ "fix the validation error in src/utils/validator.ts
    where the email regex fails on international addresses"
```

**Warum besser**: Datei + Funktion + exaktes Problem

### Vague Action Words

```
❌ "optimize the component"
✅ "optimize UserList component by adding React.memo
    to prevent unnecessary re-renders when parent state updates"
```

**Warum besser**: Problem + Lösungsansatz + messbares Ergebnis

### Missing Error Details

```
❌ "it's not working"
✅ "the login form isn't submitting—clicking submit button
    triggers no network requests, expecting POST to /api/auth/login"
```

**Warum besser**: Expected vs Actual Behavior mit Symptomen

### Ambiguous Scope

```
❌ "update the docs"
✅ "update README.md with installation instructions
    and usage examples for the get-transcript tool"
```

**Warum besser**: Spezifisches Dokument + erforderliche Sections

## Vagueness Indicators (aus Analyse)

| Indicator | Häufigkeit | Beschreibung |
|-----------|------------|--------------|
| Missing file path | 42% | Keine Datei genannt |
| Missing error details | 23% | Kein Error-Output |
| Missing success criteria | 30% | Unklar wann "fertig" |
| Missing specific approach | 19% | Keine Methode genannt |

## Integration mit Evolving

### Synergien mit prompt-pro-framework

```
                 CREATION CYCLE
                      ↓
prompt-pro-framework → Generiert optimalen Prompt
                      ↓
                 Claude nutzt Prompt
                      ↓
                  ANALYSIS CYCLE
                      ↓
   prompt-coach → Analysiert Qualität
                      ↓
              Feedback & Suggestions
                      ↓
           Verbesserter Prompt (zurück zu Creation)
```

### Mögliche Erweiterungen

1. **/prompt-analyze Command**:
   ```
   /prompt-analyze "Mein Prompt hier"
   → Gibt Score + Verbesserungsvorschläge
   ```

2. **Session Analytics Integration**:
   - Token-Tracking in `_memory/sessions/`
   - Productivity Patterns in `_memory/workflows/`

3. **Auto-Enhancement Rule erweitern**:
   - Vagueness Detection vor Ausführung
   - Automatische Context-Anreicherung

### Unterschied zu unserem System

| prompt-coach | Evolving |
|--------------|----------|
| Analysiert JSONL Logs | Kein Log-basiertes Tracking |
| Post-hoc Analyse | Real-time Enhancement |
| Token-Cost-Fokus | Qualitäts-Fokus |

## Key Takeaways

1. **Context-aware Scoring**: Kurz ≠ Schlecht wenn Context vorhanden
2. **Golden Rule**: Colleague-Test für Prompts
3. **8-Dimensionale Analyse**: Umfassende Qualitätsbewertung
4. **Anti-Pattern Katalog**: Konkrete Verbesserungsbeispiele
5. **Deduplication**: Wichtig für akkurate Token-Analyse

---

## Related

- `.claude/skills/prompt-pro-framework/` - Prompt Creation Skill
- `.claude/rules/auto-enhancement.md` - Real-time Enhancement
- `knowledge/prompts/` - Prompt Library
