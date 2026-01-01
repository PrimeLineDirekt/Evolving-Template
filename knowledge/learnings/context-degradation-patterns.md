# Context Degradation Patterns

**Source**: Agent-Skills-for-Context-Engineering (Deep Dive 2025-12-27)
**Typ**: Learning
**Relevanz**: HOCH - Erklärt warum Agents bei langen Contexts versagen
**Erstellt**: 2025-12-22
**Updated**: 2025-12-27 (Deep Dive mit vollständigem Skill-Content)

---

## Problem

Context Windows haben fundamentale Limitationen. Selbst bei 200K Token Modellen degradiert die Performance unter bestimmten Bedingungen massiv.

**Empirische Erkenntnis** (BrowseComp Research):
> "Token Usage erklärt 80% der Performance-Varianz bei komplexen Reasoning Tasks"

**RULER Benchmark Findings** (aus Agent-Skills):
> "Nur 50% der Modelle die 32K+ Context behaupten, halten satisfactory Performance bei 32K Tokens. Near-perfect Needle-in-Haystack Tests übersetzen NICHT zu echtem Long-Context Understanding."

---

## Die 5 Degradation Patterns

### 1. Lost-in-the-Middle

**Was**: Information in der Mitte des Contexts wird schlechter verarbeitet als am Anfang oder Ende.

**Empirische Evidenz** (Agent-Skills):
> "Relevant information placed in the middle of context experiences 10-40% lower recall accuracy compared to the same information at beginning or end."

**Attention Sink Mechanism**:
Models allocate massive attention to first token (BOS token) to stabilize internal states. Dies kreiert einen "Attention Sink" der das Attention Budget absorbiert. Bei wachsendem Context wird das limitierte Budget dünner verteilt, und mittlere Tokens bekommen nicht genug Attention Weight.

**Model-Thresholds** (aktualisiert 2025):
| Model | Degradation Onset | Severe Degradation | Notes |
|-------|-------------------|-------------------|-------|
| GPT-5.2 | ~64K | ~200K | Best overall mit Thinking Mode |
| Claude Opus 4.5 | ~100K | ~180K | 200K Window, strong attention mgmt |
| Claude Sonnet 4.5 | ~80K | ~150K | Optimiert für Agents & Coding |
| Gemini 3 Pro | ~500K | ~800K | 1M Context, native multimodal |
| Gemini 3 Flash | ~300K | ~600K | 3x Speed vs 2.5, 81.2% MMMU-Pro |

**Mitigation**: Wichtige Informationen am Anfang ODER Ende platzieren, nie in der Mitte.

---

### 2. Context Poisoning

**Was**: Irrelevante oder widersprüchliche Informationen "vergiften" den gesamten Context.

**Symptome**:
- Halluzinationen steigen
- Agent referenziert falsche Fakten
- Widersprüchliche Outputs

**Ursachen**:
- Veraltete RAG-Ergebnisse
- Zu breite Retrieval-Queries
- Nicht-kuratierte Tool Outputs

**Mitigation**: Strenge Relevanz-Filterung VOR Context-Injection.

---

### 3. Context Distraction

**Was**: Hoher Noise-to-Signal Ratio führt zu Fokus-Verlust.

**Beispiel**:
```
# Schlecht: 50 irrelevante Tool Outputs, dann die eigentliche Frage
# Gut: Nur relevante 3 Tool Outputs, klar strukturiert
```

**Metriken** (Agent-Skills Repo):
- Tool Outputs = **83.9%** des typischen Agent-Contexts
- Multi-Agent Overhead = **~15x** Baseline Tokens

**Mitigation**: Aggressive Kompression von Tool Outputs (→ Observation Compression Pattern).

---

### 4. Context Confusion

**Was**: Unklare Struktur führt zu Fehlinterpretationen.

**Symptome**:
- Agent verwechselt User-Input mit System-Instructions
- Tool Results werden als User-Messages interpretiert
- Rollen-Vermischung bei Multi-Agent

**Mitigation**:
- Klare XML-Tags für Sections (`<user_query>`, `<tool_result>`, `<system>`)
- Konsistente Formatierung
- Explizite Rollen-Marker

---

### 5. Context Clash

**Was**: Widersprüchliche Instructions aus verschiedenen Quellen.

**Beispiel**:
```
System Prompt: "Antworte immer auf Deutsch"
RAG Document: "Always respond in English"
→ Agent ist verwirrt, Output inkonsistent
```

**Mitigation**:
- Klare Prioritäts-Hierarchie definieren
- System Prompt hat höchste Priorität
- Konflikte explizit auflösen

---

## 4-Bucket Mitigation Framework

Systematischer Ansatz zur Context-Optimierung:

```
┌─────────────────────────────────────────────────────────┐
│                  Context Input                          │
└─────────────────────────────────────────────────────────┘
                         │
         ┌───────────────┼───────────────┐
         ▼               ▼               ▼
    ┌─────────┐    ┌──────────┐    ┌──────────┐
    │  WRITE  │    │  SELECT  │    │ COMPRESS │
    │         │    │          │    │          │
    │ Bessere │    │ Richtige │    │ Weniger  │
    │ Inputs  │    │ Auswahl  │    │ Tokens   │
    └─────────┘    └──────────┘    └──────────┘
         │               │               │
         └───────────────┼───────────────┘
                         ▼
                   ┌──────────┐
                   │ ISOLATE  │
                   │          │
                   │ Saubere  │
                   │ Trennung │
                   └──────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│                  Optimized Context                       │
└─────────────────────────────────────────────────────────┘
```

### Bucket 1: WRITE (Bessere Inputs)

**Ziel**: Qualität der Input-Daten verbessern

| Aktion | Beispiel |
|--------|----------|
| Tool Descriptions optimieren | "Search documents" → "Search tax documents by keyword, returns top 5 matches with relevance scores" |
| System Prompts präzisieren | Vage → Spezifisch mit Beispielen |
| RAG Queries verfeinern | Breite Query → Fokussierte Sub-Queries |

### Bucket 2: SELECT (Richtige Auswahl)

**Ziel**: Nur relevante Information inkludieren

| Aktion | Beispiel |
|--------|----------|
| Top-K statt All | RAG: Top 3 statt Top 10 Ergebnisse |
| Recency Filter | Nur Events der letzten N Turns |
| Relevance Threshold | Score < 0.7 → Exclude |

### Bucket 3: COMPRESS (Weniger Tokens)

**Ziel**: Gleiche Information in weniger Tokens

| Aktion | Token-Reduktion |
|--------|-----------------|
| JSON → YAML | ~15-20% |
| Verbose → Compact Format | ~30-40% |
| AI-gestützte Summarization | ~50-70% |
| Observation Masking | ~75-95% |

### Bucket 4: ISOLATE (Saubere Trennung)

**Ziel**: Interference zwischen Context-Teilen verhindern

| Aktion | Beispiel |
|--------|----------|
| XML Section Tags | `<system>`, `<user_query>`, `<retrieved_docs>` |
| Clear Separators | `---` oder `===` zwischen Sections |
| Role Markers | `[SYSTEM]`, `[USER]`, `[ASSISTANT]` |
| Priority Headers | `[PRIORITY: HIGH]` für wichtige Instructions |

---

## Praktische Checkliste

Bei Context-Problemen systematisch durchgehen:

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

## Token Economics (Empirische Daten)

| Metrik | Wert | Quelle |
|--------|------|--------|
| Tool Outputs Anteil | 83.9% | Agent-Skills Repo |
| Multi-Agent Overhead | ~15x Baseline | Agent-Skills Repo |
| Performance-Varianz durch Tokens | 80% | BrowseComp |
| Lost-in-Middle Drop | ~30-50% | RULER Benchmark |

**Implikation**: Token-Optimierung hat den größten ROI für Agent-Performance.

---

## Evolving Integration

### Bestehende Patterns die helfen

| Pattern | Adressiert |
|---------|------------|
| Context Window Ownership | WRITE, SELECT, COMPRESS |
| Observation Compression | COMPRESS (75-95% Reduktion) |
| Progressive Disclosure | SELECT (On-demand Loading) |

### Empfohlene Erweiterungen

1. **experience-suggest.md**: Relevance Threshold (Score < 30 = Skip)
2. **domain-memory-bootup.md**: Nur aktuelles Projekt laden, nicht alle
3. **Tool Outputs**: YAML statt JSON wo möglich

---

## Counterintuitive Findings (Agent-Skills)

### Shuffled Haystacks Outperform Coherent Ones

> "Shuffled (incoherent) haystacks produce better performance than logically coherent ones."

**Erklärung**: Coherent Context kreiert false associations die Retrieval verwirren. Incoherent Context zwingt Models zu exaktem Matching.

### Single Distractors Have Outsized Impact

> "Even a single irrelevant document reduces performance significantly. The effect follows a step function—presence of ANY distractor triggers degradation."

**Nicht**: Proportional zum Noise-Anteil
**Sondern**: Binärer Trigger sobald ein Distractor vorhanden ist.

### Needle-Question Similarity Matters

> "Lower similarity between needle and question pairs shows faster degradation with context length."

**Implikation**: Tasks die Inference über dissimilaren Content erfordern sind besonders vulnerabel.

### Larger Contexts Can Hurt

> "Models exhibit non-linear degradation with context length. Performance remains stable up to threshold, then degrades rapidly."

**Kosten-Implikation**: 400K Token Context ist nicht 2x Kosten von 200K - es ist exponentiell mehr in Zeit und Computing.

---

## Model-Specific Behavior (Agent-Skills)

| Model | Failure Mode | Empfehlung |
|-------|--------------|------------|
| **Claude 4.5** | Lowest hallucination, calibrated uncertainty. Refuses/asks clarification statt fabricate. | High-stakes tasks, conservative approach |
| **GPT-5.2** | Two modes: instant (fast) vs thinking (reasoning). Thinking mode reduces hallucination through verification. | Speed vs accuracy tradeoff per request |
| **Gemini 3** | Native multimodality, 1M context. Strong at multi-modal reasoning. | Multi-modal tasks, very long contexts |

---

## Context Optimization Techniques (Agent-Skills)

### Compaction

Summarizing context near limits, then reinitialize with summary:

```python
# Priority for compression:
1. Tool outputs → Replace with summaries
2. Old turns → Summarize early conversation
3. Retrieved docs → Summarize if recent versions exist
4. System prompt → NEVER compress
```

**Target**: 50-70% token reduction with <5% quality degradation.

### Observation Masking

```python
# Replace verbose tool outputs with compact references
if len(observation) > max_length:
    ref_id = store_observation(observation)
    return f"[Obs:{ref_id} elided. Key: {extract_key(observation)}]"

# Never mask:
# - Critical to current task
# - From most recent turn
# - Used in active reasoning
```

**Target**: 60-80% reduction in masked observations.

### KV-Cache Optimization

```python
# Stable content first for cache hits
context = [system_prompt, tool_definitions]  # Cacheable
context += [reused_templates]                 # Reusable
context += [unique_content]                   # Unique

# Avoid:
# - Timestamps in prompts
# - Dynamic content early in context
# - Inconsistent formatting
```

**Target**: 70%+ cache hit rate for stable workloads.

### Context Partitioning

> "The most aggressive form of context optimization is partitioning work across sub-agents with isolated contexts."

**Pattern**: Coordinator mit Summary + Sub-Agents mit isoliertem Detail-Context.

---

## Related

- [Context Window Ownership Pattern](../patterns/context-window-ownership-pattern.md)
- [Observation Compression Pattern](../patterns/observation-compression-pattern.md)
- [Compact Errors Pattern](../patterns/compact-errors-pattern.md)
- [Resume Strategies Pattern](../patterns/resume-strategies-pattern.md)
- [Safety Hooks Framework Pattern](../patterns/safety-hooks-framework-pattern.md)

---

**Navigation**: [← Learnings](README.md) | [Knowledge Index](../index.md)
