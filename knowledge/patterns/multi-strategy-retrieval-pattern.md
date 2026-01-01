# Multi-Strategy Retrieval Pattern

**Source**: vectorize-io/hindsight (4-Wege Retrieval)
**Typ**: Pattern
**Relevanz**: HOCH - State-of-the-Art Memory Retrieval
**Erstellt**: 2025-12-22

---

## Problem

Einzelne Retrieval-Strategien haben fundamentale Schwächen:

| Strategie | Schwäche |
|-----------|----------|
| **Nur Vector** | Misst semantische Ähnlichkeit, ignoriert exakte Matches |
| **Nur Keyword** | Findet "TypeScript" nicht bei "TS" Query |
| **Nur Graph** | Langsam bei großen Graphen, keine Fuzzy-Matches |
| **Nur Temporal** | Ignoriert Relevanz, nur Aktualität |

**Benchmark-Ergebnis** (Zep):
- Nur Vector RAG: 60-70% Accuracy
- Multi-Strategy: **94.8% Accuracy**

---

## Lösung: 4-Wege Parallel Retrieval

```
                    ┌─────────────┐
                    │    Query    │
                    └──────┬──────┘
                           │
       ┌───────────────────┼───────────────────┐
       │                   │                   │
       ▼                   ▼                   ▼
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│  SEMANTIC   │    │   KEYWORD   │    │    GRAPH    │
│   (Vector)  │    │   (BM25)    │    │ (Traversal) │
│             │    │             │    │             │
│ Embeddings  │    │ Full-Text   │    │ Entity +    │
│ Cosine Sim  │    │ TF-IDF      │    │ Relation    │
└──────┬──────┘    └──────┬──────┘    └──────┬──────┘
       │                   │                   │
       └───────────────────┼───────────────────┘
                           │
                           ▼
                  ┌─────────────────┐
                  │  TEMPORAL       │
                  │  (Time Filter)  │
                  │                 │
                  │ Recency Boost   │
                  │ Valid Window    │
                  └────────┬────────┘
                           │
                           ▼
                  ┌─────────────────┐
                  │  SCORE FUSION   │
                  │                 │
                  │ Weighted Merge  │
                  │ Deduplication   │
                  │ Ranking         │
                  └────────┬────────┘
                           │
                           ▼
                  ┌─────────────────┐
                  │    Results      │
                  └─────────────────┘
```

---

## Die 4 Strategien im Detail

### 1. Semantic Retrieval (Vector)

**Was**: Embedding-basierte Ähnlichkeitssuche

**Wie**:
```python
# Pseudocode
query_embedding = embed(query)
results = vector_db.search(
    query_embedding,
    metric="cosine",
    top_k=20
)
```

**Stärken**:
- Findet semantisch ähnliche Konzepte
- "Error handling" findet auch "Exception management"

**Schwächen**:
- Teuer (Embedding-Berechnung)
- Kann bei exakten Begriffen versagen

### 2. Keyword Retrieval (BM25)

**Was**: Klassische Full-Text-Suche mit TF-IDF Scoring

**Wie**:
```python
# Pseudocode
results = search_index.query(
    query,
    algorithm="bm25",
    top_k=20
)
```

**Stärken**:
- Schnell
- Exakte Matches
- Funktioniert gut für technische Begriffe

**Schwächen**:
- Keine Synonyme
- Reihenfolge-sensitiv

### 3. Graph Retrieval (Traversal)

**Was**: Entity-basierte Suche mit Relationship-Expansion

**Wie**:
```python
# Pseudocode
entities = extract_entities(query)
results = []
for entity in entities:
    node = graph.find_node(entity)
    related = graph.traverse(node, depth=2)
    results.extend(related)
```

**Stärken**:
- Findet verwandte Konzepte
- Kontextuelle Expansion
- Gut für "Was hängt mit X zusammen?"

**Schwächen**:
- Benötigt gut gepflegten Graph
- Kann zu viele Results liefern

### 4. Temporal Retrieval (Time Filter)

**Was**: Zeit-basierte Filterung und Boosting

**Wie**:
```python
# Pseudocode
results = base_results.filter(
    lambda r: r.valid_until is None or r.valid_until > now
).boost(
    lambda r: recency_score(r.created_at)
)
```

**Stärken**:
- Priorisiert aktuelle Information
- Filtert veraltete Fakten

**Schwächen**:
- Alte aber relevante Info kann verloren gehen

---

## Score Fusion

Ergebnisse aller Strategien müssen kombiniert werden:

### Reciprocal Rank Fusion (RRF)

```python
def rrf_score(rankings, k=60):
    """
    Combine multiple ranking lists.

    rankings: dict of {doc_id: rank} for each strategy
    k: constant (typically 60)
    """
    scores = {}
    for strategy, ranking in rankings.items():
        for doc_id, rank in ranking.items():
            if doc_id not in scores:
                scores[doc_id] = 0
            scores[doc_id] += 1 / (k + rank)
    return sorted(scores.items(), key=lambda x: -x[1])
```

### Weighted Combination

```python
def weighted_fusion(results, weights):
    """
    weights = {
        'semantic': 0.4,
        'keyword': 0.3,
        'graph': 0.2,
        'temporal': 0.1
    }
    """
    final_scores = {}
    for strategy, weight in weights.items():
        for doc, score in results[strategy]:
            if doc not in final_scores:
                final_scores[doc] = 0
            final_scores[doc] += score * weight
    return sorted(final_scores.items(), key=lambda x: -x[1])
```

---

## Implementation für Evolving

### Aktueller Status

| Strategie | Evolving Status |
|-----------|-----------------|
| Semantic (Vector) | Nicht implementiert |
| Keyword | Context Router (basic) |
| Graph | Knowledge Graph vorhanden |
| Temporal | `--recent` Flag in `/recall` |

### Empfohlene Erweiterungen

#### Phase 1: Keyword verbessern (LOW Effort)

Erweitere Context Router mit Fuzzy-Matching:
```python
# In _graph/cache/context-router.json
{
  "typescript-error": {
    "keywords": ["typescript", "ts", "type error", "tsc"],
    "fuzzy": true
  }
}
```

#### Phase 2: Graph Traversal nutzen (MEDIUM Effort)

Bei `/recall` automatisch verwandte Nodes einbeziehen:
```
Query: "API error"
→ Keyword Match: exp-2025-001 (API Error)
→ Graph Expansion: exp-2025-002 (HTTP Client), exp-2025-003 (Auth Error)
```

#### Phase 3: Vector Search (HIGH Effort, Optional)

Nur wenn Experience Memory stark wächst (100+ Experiences):
- SQLite + sqlite-vss Extension
- Oder externe API (OpenAI Embeddings)

---

## Gewichtung nach Use Case

| Use Case | Semantic | Keyword | Graph | Temporal |
|----------|----------|---------|-------|----------|
| Error Debugging | 0.3 | 0.5 | 0.1 | 0.1 |
| Architecture Decision | 0.4 | 0.2 | 0.3 | 0.1 |
| Pattern Discovery | 0.5 | 0.1 | 0.3 | 0.1 |
| Recent Issues | 0.2 | 0.3 | 0.1 | 0.4 |

---

## Metriken

| Metrik | Beschreibung | Ziel |
|--------|--------------|------|
| **Recall@10** | Relevante Results in Top 10 | > 80% |
| **MRR** | Mean Reciprocal Rank | > 0.5 |
| **Latency** | Retrieval-Zeit | < 500ms |

---

## Related

- [Context Window Ownership Pattern](context-window-ownership-pattern.md)
- [Experience Memory](../../_memory/experiences/)
- [Knowledge Graph](../../_graph/)
- [Memory Decay Pattern](../learnings/memory-decay-pattern.md)

---

**Navigation**: [← Patterns](README.md) | [Knowledge Index](../index.md)
