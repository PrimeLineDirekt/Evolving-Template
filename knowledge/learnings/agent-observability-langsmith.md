# Agent Observability mit LangSmith

**Quelle**: LangChain Docs, Blog "Debugging Deep Agents"
**Typ**: Learning
**Relevanz**: {PROJECT} v2, zukünftige Multi-Agent Systeme
**Erstellt**: 2025-12-22

---

## Wann Observability?

### Decision Framework

```
                    Brauchst du Agent Observability?
                              │
                              ▼
                 ┌────────────────────────┐
                 │ Wie viele Agent-Steps? │
                 └───────────┬────────────┘
                             │
              ┌──────────────┼──────────────┐
              ▼              ▼              ▼
           1-3 Steps    4-10 Steps     10+ Steps
              │              │              │
              ▼              ▼              ▼
         ❌ Overkill    ⚠️ Optional    ✅ Essential
```

### Konkrete Kriterien

| Kriterium | Ohne Observability | Mit Observability |
|-----------|-------------------|-------------------|
| Agent-Steps pro Query | 1-3 | 4+ |
| Autonome Laufzeit | Sekunden | Minuten bis Stunden |
| Production Traffic | Nein / Testing | Ja, echte User |
| Multi-Agent Orchestration | Nein | Ja |
| Kosten-Tracking nötig | Nein | Ja (Opus teuer!) |
| User Feedback sammeln | Nein | Ja |
| Debugging-Aufwand | Gering | Hoch ("Wo ging's schief?") |

---

## LangSmith Architektur

### Hierarchie

```
Thread (Conversation)
    │
    ├── Trace 1 (Single Query Execution)
    │       │
    │       ├── Run: Orchestrator LLM Call
    │       ├── Run: Agent A Tool Call
    │       ├── Run: Agent A LLM Response
    │       ├── Run: Agent B Tool Call
    │       └── Run: Final LLM Response
    │
    └── Trace 2 (Follow-up Query)
            │
            └── ...
```

### Datenmodell

```python
# Run (einzelner Step)
{
    "id": "run-uuid",
    "name": "steuer-agent",
    "run_type": "llm" | "tool" | "chain",
    "inputs": {"query": "..."},
    "outputs": {"response": "..."},
    "start_time": "2025-12-22T10:00:00Z",
    "end_time": "2025-12-22T10:00:02Z",
    "latency_ms": 2000,
    "tokens": {"input": 500, "output": 200},
    "cost": 0.0035,
    "error": null,
    "parent_run_id": "parent-uuid"
}
```

---

## LangSmith Features

### 1. Tracing (Core)

**Was:** Jeden LLM-Call und Tool-Aufruf aufzeichnen.

**Nutzen:**
- Nachvollziehen welcher Agent was wann gemacht hat
- Input/Output für jeden Step sehen
- Latenz und Token-Verbrauch pro Step

**Integration (LangGraph):**
```python
import os
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = "ls__xxx"
os.environ["LANGCHAIN_PROJECT"] = "{PROJECT_ID}"

# Das war's - alle LangGraph Calls werden automatisch getraced
```

### 2. Cost Tracking

**Was:** Token-Kosten pro Model aggregieren.

**Nutzen für {PROJECT}:**
```
Query: "Wie optimiere ich meine Steuern als Auswanderer?"

Kosten-Breakdown:
├── Orchestrator (Haiku): $0.001
├── Steuer-Agent (Opus): $0.045    ← Teuerster!
├── DBA-Agent (Sonnet): $0.008
├── Risiko-Agent (Sonnet): $0.008
└── Total: $0.062

→ Optimierung: Steuer-Agent auf Sonnet? Spart 80%!
```

### 3. Feedback Collection

**Was:** User-Feedback zu Responses speichern.

**Typen:**
- Thumbs Up/Down (einfach)
- Score 1-5 (granular)
- Text-Feedback (detailliert)
- Corrections (Ground Truth)

**API:**
```python
from langsmith import Client

client = Client()
client.create_feedback(
    run_id="run-uuid",
    key="user-rating",
    score=1,  # Thumbs up
    comment="Sehr hilfreiche Antwort!"
)
```

### 4. Online Evaluators

**Was:** Automatische Qualitätsprüfung auf Traces.

**Beispiele:**
- Hallucination Detection
- Relevance Scoring
- Toxicity Check
- Custom Evaluators (eigene Prompts)

**Setup:**
```python
# In LangSmith UI oder API
evaluator = {
    "name": "answer-relevance",
    "prompt": "Score 1-5 how relevant is {output} to {input}",
    "model": "claude-haiku",
    "threshold": 3  # Alert wenn < 3
}
```

### 5. Debugging Tools

**Polly (AI Assistant):**
- Natural Language Queries über Traces
- "Warum hat der Steuer-Agent hier falsch geantwortet?"
- "Zeig mir alle Traces wo Confidence < 0.7"

**CLI (für IDE-Integration):**
```bash
# Traces exportieren für lokale Analyse
langsmith fetch --project {PROJECT_ID} --last 24h --output traces.json
```

---

## Integration mit {PROJECT} v2

### Minimal Setup (10 Min)

```python
# src/config/observability.py
import os
from functools import wraps

def setup_langsmith():
    """Enable LangSmith tracing."""
    os.environ["LANGCHAIN_TRACING_V2"] = "true"
    os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGSMITH_API_KEY")
    os.environ["LANGCHAIN_PROJECT"] = "{PROJECT_ID}"

# In main.py
if os.getenv("ENABLE_TRACING"):
    setup_langsmith()
```

### Erweitert: Custom Metadata

```python
from langsmith import traceable

@traceable(
    name="steuer-agent",
    metadata={
        "agent_type": "specialist",
        "model_tier": "opus",
        "domain": "german-tax"
    },
    tags=["tax", "optimization"]
)
async def run_steuer_agent(query: str, context: dict):
    ...
```

### Feedback Loop

```python
# Nach User-Interaktion
async def collect_feedback(run_id: str, user_rating: int):
    """Store user feedback for continuous improvement."""
    client.create_feedback(
        run_id=run_id,
        key="user-satisfaction",
        score=user_rating,
        source_info={"version": "2.1"}
    )
```

---

## Wann NICHT LangSmith

| Situation | Besser |
|-----------|--------|
| Einfache Single-Agent Calls | Logging reicht |
| Lokale Entwicklung ohne Traffic | Print-Debugging |
| Kosten-sensitiv ohne Budget | Open-Source Alternativen |
| Datenschutz-kritisch (GDPR) | Self-hosted Lösung |

### Alternativen

| Tool | Open Source? | Self-Hosted? | LangGraph Support |
|------|--------------|--------------|-------------------|
| LangSmith | Nein | Nein | Native |
| LangFuse | Ja | Ja | Ja |
| Phoenix (Arize) | Ja | Ja | Ja |
| OpenTelemetry | Ja | Ja | Manual |

---

## Kosten

**LangSmith Pricing (Stand 2025):**
- Free Tier: 5k Traces/Monat
- Plus: $39/Monat, 50k Traces
- Enterprise: Custom

**Für {PROJECT}:**
- Development: Free Tier reicht
- Production (100 Queries/Tag): ~3k Traces/Monat → Free Tier
- Scale (1000 Queries/Tag): Plus Tier nötig

---

## Implementierungs-Roadmap

### Phase 1: Development (Jetzt möglich)

```
[ ] LANGSMITH_API_KEY in .env
[ ] setup_langsmith() in main.py
[ ] Erste Traces in Dashboard prüfen
```

### Phase 2: Debugging (Bei Bedarf)

```
[ ] Custom Metadata pro Agent
[ ] Error-Tracking konfigurieren
[ ] Latency-Alerts setzen
```

### Phase 3: Production (Bei Traffic)

```
[ ] User Feedback Collection
[ ] Online Evaluators für Quality
[ ] Cost Monitoring Dashboard
[ ] Weekly Reports automatisieren
```

---

## Related

- [{PROJECT} v2](../projects/{PROJECT_ID}/README.md)
- [Multi-Agent Orchestration Pattern](../patterns/multi-agent-orchestration.md)
- [Compact Errors Pattern](../patterns/compact-errors-pattern.md)

---

## Quellen

- LangSmith Docs
- Debugging Deep Agents Blog
- LangSmith Pricing: https://www.langchain.com/langsmith
