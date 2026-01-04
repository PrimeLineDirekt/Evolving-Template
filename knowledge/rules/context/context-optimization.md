# Context Optimization Rule

**Priorität**: HOCH
**Trigger**: Bei langen Sessions, vielen Tool Outputs, komplexen Multi-Step Tasks
**Quelle**: Agent-Skills-for-Context-Engineering, claude-code-tools Deep Dives

---

## Warum wichtig?

> "Token Usage erklärt 80% der Performance-Varianz bei komplexen Reasoning Tasks"

Selbst bei 200K Token Modellen degradiert Performance unter bestimmten Bedingungen massiv.

---

## Die 5 Degradation Patterns erkennen

### 1. Lost-in-the-Middle
**Symptom**: Wichtige Info in der Mitte wird ignoriert
**Erkennung**: Kritische Daten zwischen langen Tool Outputs
**Mitigation**: Wichtiges nach VORNE oder HINTEN verschieben

### 2. Context Poisoning
**Symptom**: Halluzinationen, falsche Referenzen
**Erkennung**: Veraltete RAG-Ergebnisse, breite Queries
**Mitigation**: Strenge Relevanz-Filterung VOR Context-Injection

### 3. Context Distraction
**Symptom**: Fokus-Verlust, irrelevante Tangenten
**Erkennung**: Viele lange Tool Outputs (>83% des Contexts!)
**Mitigation**: Aggressive Kompression von Tool Outputs

### 4. Context Confusion
**Symptom**: Rollen-Verwechslung, Fehlinterpretationen
**Erkennung**: Unklare Struktur, gemischte Formate
**Mitigation**: Klare XML-Tags, konsistente Formatierung

### 5. Context Clash
**Symptom**: Inkonsistente Outputs, Widersprüche
**Erkennung**: Widersprüchliche Instructions aus verschiedenen Quellen
**Mitigation**: Prioritäts-Hierarchie definieren (System > User > RAG)

---

## 4-Bucket Framework anwenden

Bei Context-Prob Aktion durchführen:

```
┌─────────────────────────────────────────────────────────┐
│                  Context Input                          │
└─────────────────────────────────────────────────────────┘
                         │
         ┌───────────────┼───────────────┐
         ▼               ▼               ▼
    ┌─────────┐    ┌──────────┐    ┌──────────┐
    │  WRITE  │    │  SELECT  │    │ COMPRESS │
    └─────────┘    └──────────┘    └──────────┘
         │               │               │
         └───────────────┼───────────────┘
                         ▼
                   ┌──────────┐
                   │ ISOLATE  │
                   └──────────┘
```

### Bucket 1: WRITE (Bessere Inputs)
- Tool Descriptions präzisieren
- System Prompts spezifisch formulieren
- RAG Queries fokussieren

### Bucket 2: SELECT (Richtige Auswahl)
- Top-K statt All (z.B. Top 3 statt Top 10)
- Recency Filter (nur letzte N Turns)
- Relevance Threshold (Score < 0.7 → Exclude)

### Bucket 3: COMPRESS (Weniger Tokens)
| Technik | Token-Reduktion |
|---------|-----------------|
| JSON → YAML | ~15-20% |
| Verbose → Compact | ~30-40% |
| AI Summarization | ~50-70% |
| Observation Masking | ~75-95% |

### Bucket 4: ISOLATE (Saubere Trennung)
- XML Section Tags (`<system>`, `<user_query>`, `<tool_result>`)
- Clear Separators (`---` oder `===`)
- Role Markers (`[SYSTEM]`, `[USER]`, `[ASSISTANT]`)
- Priority Headers (`[PRIORITY: HIGH]`)

---

## Model-Specific Thresholds

| Model | Degradation Onset | Severe Degradation |
|-------|-------------------|-------------------|
| Claude Opus 4.5 | ~100K | ~180K |
| Claude Sonnet 4.5 | ~80K | ~150K |
| GPT-5.2 | ~64K | ~200K |
| Gemini 3 Pro | ~500K | ~800K |

**Implikation**: Bei ~80% des Thresholds proaktiv komprimieren!

---

## Praktische Checkliste

Bei langen Sessions oder vielen Tool Calls:

```
□ Lost-in-Middle?
  → Wichtige Info nach vorne/hinten verschieben

□ Poisoning?
  → RAG-Ergebnisse filtern, Relevanz prüfen

□ Distraction?
  → Tool Outputs komprimieren, Noise entfernen

□ Confusion?
  → Klare Tags und Struktur hinzufügen

□ Clash?
  → Prioritäts-Hierarchie definieren
```

---

## Observation Masking (für Tool Outputs)

```python
# Bei langen Tool Outputs:
if len(observation) > 2000:
    # Komprimieren statt voll anzeigen
    summary = extract_key_info(observation)
    return f"[Tool Result Summary: {summary}]"

# NIEMALS maskieren:
# - Kritisch für aktuellen Task
# - Vom letzten Turn
# - In aktivem Reasoning verwendet
```

---

## Counterintuitive Findings beachten

1. **Single Distractors haben outsized Impact**
   - Ein irrelevantes Dokument triggert bereits Degradation
   - Lieber zu wenig als zu viel Context

2. **Shuffled > Coherent Haystacks**
   - Incoherenter Context zwingt zu exaktem Matching
   - Nicht versuchen, alles "schön" zu ordnen

3. **Larger Context kann schaden**
   - Performance bleibt stabil bis Threshold, dann rapider Abfall
   - Proaktiv komprimieren VOR dem Limit

---

## Integration mit anderen Rules

- `domain-memory-bootup.md` - Hydrate mit Decay-Filtering
- `auto-enhancement.md` - Context-Extraction optimieren
- `experience-suggest.md` - Nur high-relevance Experiences

---

## Wann aktiv werden?

| Situation | Aktion |
|-----------|--------|
| Session > 50 Turns | SELECT + COMPRESS prüfen |
| Tool Output > 5000 chars | Observation Masking |
| Mehrere RAG Queries | Relevance Threshold |
| Multi-Agent Task | Context Partitioning |
| Fehler/Halluzinationen | Poisoning Check |

---

## Related

- [Context Degradation Patterns](../../knowledge/learnings/context-degradation-patterns.md)
- [Four-Bucket Context Pattern](../../knowledge/patterns/four-bucket-context-pattern.md)
- [Observation Compression Pattern](../../knowledge/patterns/observation-compression-pattern.md)
