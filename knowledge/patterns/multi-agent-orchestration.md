---
title: "Multi-Agent Orchestration Pattern"
type: pattern
category: ai-architecture
created: 2024-11-22
updated: 2025-12-09
source: ki-auswanderungs-berater, {PROJECT_ID}
confidence: 95%
tags: [multi-agent, orchestration, n8n, langgraph, performance, scalability, resilient]
---

# Multi-Agent Orchestration Pattern

## Problem

Single AI Agent für komplexe Tasks führt zu:
- Langen Processing-Zeiten (8-12 Min für comprehensive reports)
- Mangelnder Domain-Spezialisierung
- Schwieriger Fehler-Isolierung
- Schlechter Scalability

## Solution

**Master Orchestrator + Specialized Agents Pattern** mit paralleler Ausführung.

### Architecture

```
┌─────────────────────────────┐
│   Master Orchestrator       │
│   (Koordination + Routing)  │
└──────────┬──────────────────┘
           │
    ┌──────┴────────┬──────────────┬──────────────┐
    │               │              │              │
┌───▼────┐    ┌────▼───┐    ┌────▼───┐    ┌────▼───┐
│Agent 1 │    │Agent 2 │    │Agent 3 │... │Agent N │
│Steuer  │    │Familie │    │Logistik│    │Report  │
└────┬───┘    └────┬───┘    └────┬───┘    └────┬───┘
     │             │              │              │
     └─────────────┴──────────────┴──────────────┘
                   │
            ┌──────▼───────┐
            │  Aggregation  │
            │    & Report   │
            └──────────────┘
```

### Components

**1. Master Orchestrator**
- Profile analysis
- Agent selection (nur relevante)
- Dependency management
- Error handling

**2. Specialized Agents (16+)**
- Domain expertise
- Focused scope
- Structured output
- Self-validation

**3. Reporter Agent**
- Output aggregation
- Executive summary
- Format consistency
- Quality checks

## Example (KI Auswanderungs-Berater)

### 29-Agent System

**Performance**:
- Legacy Sequential: 8-12 minutes
- Multi-Agent Parallel: ~45 seconds
- **Improvement: 70%+**

**Agents**:
- Financial (4): Steuer, Finanzplanung, Krypto, Unternehmens-Verlagerung
- Family (3): Familie-Kinder, Krankenversicherung, Senioren
- Logistics (4): Umzug, Verträge, Tierverlagerung, Probe-Auswanderung
- Special (5): Digitale Nomaden, Notfall, Rückkehr, etc.
- Meta (3): Profil-Analyse, Checkliste, Reporter

### Profile-Based Selection

**Key Innovation**: Nicht alle 29 Agents für jeden User.

```javascript
if (profile.hasChildren) {
  agents.push('familie-kinder')
}

if (profile.hasPets) {
  agents.push('tierverlagerung')
}

if (profile.isEntrepreneur) {
  agents.push('unternehmens-verlagerung')
}

// Result: 8-15 agents per user (not 29)
```

**Benefit**: Efficiency ohne Feature-Loss

## Implementation Guide

### Step 1: Domain Decomposition

Zerlege komplexe Task in spezialisierte Domänen:

```
Auswanderung →
  - Steuerliche Aspekte
  - Finanzplanung
  - Logistik (Umzug, Versand)
  - Familie (Kinder, Schule)
  - Rechtliches (Verträge, Versicherung)
  - Integration (Sprache, Kultur)
```

**Rule**: Jede Domäne = 1 Agent

### Step 2: Agent Design

**Template**:
```markdown
# Agent: {Name}

## Identity
Du bist ein {Domain} Experte mit {Credentials}

## Input
- User Profile (126 Felder)
- Dependencies von: {Other Agents}

## Output Format
Strukturiert (JSON/Markdown):
- EXECUTIVE SUMMARY
- DETAILLIERTE ANALYSE
- ACTION ITEMS
- DEPENDENCIES (für andere Agents)

## Quality Criteria
- Mindestens 3 konkrete Action Items
- Alle kritischen Punkte adressiert
- Keine Widersprüche mit Dependencies
```

### Step 3: Dependency Management

**Explicit Dependencies**:
```
Agent: Krankenversicherung
Dependencies:
  - Profil-Analyse (Familiensituation)
  - Steueroptimierung (Ansässigkeits-Status)

Output für:
  - Reporter (Health Section)
  - Finanzplanung (Insurance Costs)
```

**Execution Order**:
1. Independent Agents (parallel)
2. Dependent Agents (after dependencies)
3. Reporter (after all)

### Step 4: Master Orchestrator Logic

```javascript
// 1. Profile Analysis
const relevantAgents = selectAgents(profile)

// 2. Dependency Graph
const graph = buildDependencyGraph(relevantAgents)

// 3. Parallel Batches
const batches = [
  [agents with no dependencies],
  [agents depending on batch 1],
  ...
]

// 4. Execute
for (const batch of batches) {
  await Promise.all(batch.map(agent => execute(agent)))
}

// 5. Aggregate
const report = await reporter.aggregate(allOutputs)
```

### Step 5: Error Handling

```javascript
try {
  output = await agent.execute()
} catch (error) {
  // Fallback to simpler agent or graceful degradation
  output = await fallbackAgent.execute()

  // Log for review
  logAgentFailure(agent, error)
}
```

## Tool: n8n for Orchestration

**Why n8n**:
- Visual workflow editor
- Built-in AI nodes (Claude, OpenAI)
- Error handling & retries
- Webhook triggers
- Sub-workflow support

**Pattern**:
```
Webhook Trigger →
  Profile Parse →
    Conditional Branches (if hasChildren, if hasPets) →
      Parallel Agent Execution →
        Aggregation →
          Reporter →
            Response
```

## Trade-offs

### Pros
- **70%+ faster** (parallel vs sequential)
- Domain expertise (specialized agents)
- Better error isolation
- Scalable (add new agents easily)
- Testable (test agents independently)

### Cons
- Complexity (29 agents vs 1)
- Dependency management overhead
- Requires orchestration tool (n8n, LangGraph)
- Prompt maintenance (29 prompts)

## When to Use

**YES**:
- Complex multi-domain tasks
- Long processing times (>3 min)
- Need for domain specialization
- Personalization requirements

**NO**:
- Simple single-domain tasks
- Sub-60-second tasks
- Prototyping phase

## Best Practices

### 1. Start Simple
Begin with 3-5 core agents, expand later.

### 2. Clear Agent Boundaries
No overlapping responsibilities.

### 3. Structured Outputs
Agents must output parseable format (JSON/Markdown).

### 4. Self-Validation
Each agent validates its output before returning.

### 5. Graceful Degradation
If agent fails, system continues with reduced output.

## Real-World Results

**KI Auswanderungs-Berater**:
- 29 Agents orchestrated via n8n
- 8-12 min → 45 sec (70%+ improvement)
- Profile-based selection (8-15 agents per user)
- Zero production failures

**Key Insight**: Parallel > Sequential for multi-domain AI tasks

---

## Token Economics (Empirische Daten)

**Source**: Agent-Skills-for-Context-Engineering (multi-agent-patterns)

| Architecture | Token Multiplier | Use Case |
|--------------|------------------|----------|
| Single agent chat | **1x** baseline | Simple queries |
| Single agent with tools | **~4x** baseline | Tool-using tasks |
| Multi-agent system | **~15x** baseline | Complex research/coordination |

**BrowseComp Research Finding**:
> "Three factors explain 95% of performance variance: token usage (80% of variance), number of tool calls, and model choice."

### Implikationen

1. **Token-Optimierung hat höchsten ROI** - 80% der Performance-Varianz
2. **Model Upgrade > Token Increase** - Claude Sonnet 4.5 bringt mehr als Token-Verdopplung
3. **Multi-Agent lohnt sich bei Parallelisierung** - 15x Tokens aber parallele Verarbeitung

---

## The Telephone Game Problem

**Source**: LangGraph Benchmarks

### Das Problem

Supervisor-Architekturen hatten in Benchmarks **50% schlechtere Performance** als optimierte Versionen.

**Ursache**: "Telephone Game" - Supervisor paraphrasiert Sub-Agent Responses, verliert dabei Fidelity.

```
Sub-Agent: "Der DBA-Artikel 5 Abs. 2 lit. a findet Anwendung..."
     ↓
Supervisor (paraphrasiert): "Es gibt steuerliche Regelungen..."
     ↓
User erhält: Vereinfachte, unpräzise Antwort
```

### Die Lösung: forward_message Tool

Implementiere einen **Direct Pass-Through Mechanism**:

```python
def forward_message(message: str, to_user: bool = True) -> dict:
    """
    Forward sub-agent response directly to user without supervisor synthesis.

    Use when:
    - Sub-agent response is final and complete
    - Supervisor synthesis would lose important details
    - Response format must be preserved exactly
    """
    if to_user:
        return {"type": "direct_response", "content": message}
    return {"type": "supervisor_input", "content": message}
```

### Wann Direct Pass-Through?

| Situation | Pass-Through? | Grund |
|-----------|---------------|-------|
| Technische Details | JA | Präzision wichtig |
| Rechtliche Formulierungen | JA | Exakte Wortwahl relevant |
| Zahlen & Daten | JA | Keine Interpretation nötig |
| Zusammenfassung mehrerer Agents | NEIN | Aggregation nötig |
| Widersprüchliche Agent-Outputs | NEIN | Resolution nötig |

### Benchmark-Ergebnis

Mit `forward_message` Pattern:
- **Swarm-Architekturen leicht besser als Supervisor**
- Grund: Sub-Agents antworten direkt, keine Translation-Errors

### Integration in Evolving

```python
# In Agent-Output-Handling
if agent.output.is_final and not needs_aggregation:
    return forward_message(agent.output.content, to_user=True)
else:
    return {"type": "supervisor_input", "content": agent.output.summary}
```

---

## V2 Evolution: Resilient Orchestrator (Python/LangGraph)

Die {PROJECT} v2 erweitert das Pattern um kritische Production-Features:

### Resilient Orchestrator

```python
# Checkpoint-based Crash Recovery
class ResilientOrchestrator:
    def run_with_checkpoints(self, profile):
        # Checkpoint after each phase
        self.save_checkpoint("agent_selection", selected_agents)
        self.save_checkpoint("batch_1_complete", batch_1_results)
        # ...

        # On crash: Resume from last checkpoint
        if self.has_checkpoint():
            return self.resume_from_checkpoint()
```

**Features:**
- Checkpoint nach jeder Phase
- Automatische Recovery bei Crash
- Compressed Context für lange Sessions
- Graceful Degradation bei Agent-Failures

### Model Tiering

| Tier | Model | Use Case | Agents |
|------|-------|----------|--------|
| **1** | Opus | Critical Analysis (€10k+ Impact) | steueroptimierung, unternehmens_verlagerung, kryptowaehrungen |
| **2** | Sonnet | Standard Analysis | profil_analyse, krankenversicherung, finanzplanung, ... |
| **3** | Haiku | Structured Tasks | checkliste, umzug_logistik, reporter |

**Benefit:** 60-70% Kostenreduktion bei gleichbleibender Qualität für kritische Analysen.

### Complexity Score (20-100)

```python
score = 20  # Base
if income > 120k: score += 15
if net_worth > 500k: score += 20
if has_business: score += 15
score += num_children * 5
if age > 60: score += 10
# ... max 100
```

**Nutzung:**
- Agent-Anzahl Limit (5-12 je nach Score)
- HITL-Trigger bei hoher Komplexität
- Report-Detail-Level

### Risk Zone Classification

```
🟢 GRÜN (Sicher) - Standard-Verfahren, etabliert
🟡 GELB (Moderat) - Legal aber nicht Standard, Dokumentation nötig
🟠 ORANGE (Aggressiv) - Am Limit, Expertenberatung zwingend
❌ VERBOTEN - Niemals empfehlen
```

**Mindest-Anforderungen:**
- Mind. 2 Optionen in 🟢 GRÜN
- Mind. 3 Optionen GESAMT

### Confidence Scoring (3-Tier)

```
confidence = base_score × aktualität × konsistenz + vollständigkeit_bonus

KB-Quellen:
- Primary (Tier 1): 1.0 Basisfaktor
- Secondary (Tier 2): 0.8 Basisfaktor
- Tertiary (Tier 3): 0.6 Basisfaktor

Thresholds:
- < 0.50: Nicht publishen
- < 0.75: HITL Review
- ≥ 0.85: Premium Quality
```

### V2 Results

**{PROJECT} v2:**
- 17 Specialist Agents (Python/LangGraph)
- 72 KB-Dokumente (621k Wörter)
- Checkpoint-based Crash Recovery
- 3-Tier Model Selection
- Risk Zone Classification
- Production-Ready Status

---

## Template

Für neue Multi-Agent Advisory Systeme:
→ `.claude/templates/scenarios/multi-agent-advisory/`

---

**Source Projects**:
- [KI Auswanderungs-Berater v1 (n8n)](../projects/ki-auswanderungs-berater/README.md)
- [{PROJECT} v2 (Python)](../projects/{PROJECT_ID}/README.md)

**Related**:
- [17 Agent Prompts v1](../prompts/patterns/{PROJECT_ID}-agents/README.md)
- [17 Agent Prompts v2](../prompts/patterns/{PROJECT_ID}-agents/README.md)
- [Multi-Agent Advisory Template](../../.claude/templates/scenarios/multi-agent-advisory/README.md)
- [n8n Documentation](../projects/ki-auswanderungs-berater/n8n/README.md)
- [KI Auswanderungs-Berater Learnings](../learnings/ki-auswanderungs-berater-learnings.md)
- [{PROJECT} v2 Learnings](../learnings/{PROJECT_ID}-learnings.md)

**Navigation**: [← Patterns](README.md) | [← Knowledge Base](../index.md)
