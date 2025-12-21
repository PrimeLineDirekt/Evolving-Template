# Blackboard Pattern

**Typ**: Agent Pattern
**Confidence**: 88%
**Source**: FareedKhan-dev/all-agentic-architectures
**Priority**: P1 - High

---

## Problem

Multi-Agent Systeme erfordern Koordination. Direkte Agent-zu-Agent Kommunikation skaliert schlecht (n² Verbindungen bei n Agents).

## Solution

Zentrales "Blackboard" (Shared Memory) mit Controller-Koordination:

```
┌─────────────────────────────────────────────────────────┐
│                                                         │
│                    ┌───────────────┐                    │
│                    │  BLACKBOARD   │                    │
│                    │ ┌───────────┐ │                    │
│                    │ │ Entry 1   │ │                    │
│                    │ │ Entry 2   │ │                    │
│                    │ │ ...       │ │                    │
│                    │ └───────────┘ │                    │
│                    └───────┬───────┘                    │
│                            │                            │
│         ┌──────────────────┼──────────────────┐        │
│         │                  │                  │        │
│         ▼                  ▼                  ▼        │
│   ┌──────────┐       ┌──────────┐       ┌──────────┐   │
│   │ Agent A  │       │ Agent B  │       │ Agent C  │   │
│   │(Expert 1)│       │(Expert 2)│       │(Expert 3)│   │
│   └──────────┘       └──────────┘       └──────────┘   │
│         │                  │                  │        │
│         └──────────────────┼──────────────────┘        │
│                            │                            │
│                     ┌──────▼──────┐                     │
│                     │ CONTROLLER  │                     │
│                     │(Koordinator)│                     │
│                     └─────────────┘                     │
│                                                         │
└─────────────────────────────────────────────────────────┘

Workflow:
1. Controller analysiert Blackboard-Status
2. Controller wählt nächsten Agent
3. Agent liest relevante Einträge
4. Agent schreibt Ergebnis auf Blackboard
5. Repeat bis Task complete
```

## Implementation

### Blackboard Data Structure

```python
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Any, Optional
from enum import Enum

class EntryType(str, Enum):
    QUERY = "query"
    ANALYSIS = "analysis"
    FINDING = "finding"
    RECOMMENDATION = "recommendation"
    DECISION = "decision"
    FINAL = "final"

class BlackboardEntry(BaseModel):
    key: str
    entry_type: EntryType
    value: Any
    source_agent: str
    timestamp: datetime = Field(default_factory=datetime.now)
    confidence: float = Field(ge=0, le=1)
    dependencies: list[str] = Field(default=[])  # Keys of entries this depends on
    metadata: dict = Field(default={})

class Blackboard:
    def __init__(self):
        self.entries: dict[str, BlackboardEntry] = {}
        self.history: list[BlackboardEntry] = []

    def write(
        self,
        key: str,
        value: Any,
        entry_type: EntryType,
        agent: str,
        confidence: float,
        dependencies: list[str] = []
    ) -> BlackboardEntry:
        entry = BlackboardEntry(
            key=key,
            entry_type=entry_type,
            value=value,
            source_agent=agent,
            confidence=confidence,
            dependencies=dependencies
        )
        self.entries[key] = entry
        self.history.append(entry)
        return entry

    def read(self, key: str) -> Optional[BlackboardEntry]:
        return self.entries.get(key)

    def read_by_type(self, entry_type: EntryType) -> list[BlackboardEntry]:
        return [e for e in self.entries.values() if e.entry_type == entry_type]

    def read_by_agent(self, agent: str) -> list[BlackboardEntry]:
        return [e for e in self.entries.values() if e.source_agent == agent]

    def get_summary(self) -> dict:
        return {
            "total_entries": len(self.entries),
            "by_type": {t.value: len(self.read_by_type(t)) for t in EntryType},
            "by_agent": self._count_by_agent(),
            "latest_entry": self.history[-1] if self.history else None
        }

    def _count_by_agent(self) -> dict:
        counts = {}
        for entry in self.entries.values():
            counts[entry.source_agent] = counts.get(entry.source_agent, 0) + 1
        return counts
```

### Controller Logic

```python
class ControllerDecision(BaseModel):
    next_agent: Optional[str]
    reasoning: str
    is_complete: bool
    final_answer: Optional[str] = None

class BlackboardController:
    def __init__(self, agents: dict[str, str]):
        """
        agents: dict mapping agent_name to capability description
        """
        self.agents = agents

    def decide_next(self, blackboard: Blackboard) -> ControllerDecision:
        summary = blackboard.get_summary()

        prompt = f"""
        Blackboard Status:
        {summary}

        Recent Entries:
        {self._format_recent_entries(blackboard)}

        Available Agents:
        {self._format_agents()}

        Decide:
        1. Is the task complete? If so, what's the final answer?
        2. If not complete, which agent should contribute next?
        3. What should they focus on?
        """

        return llm.with_structured_output(ControllerDecision).invoke(prompt)

    def _format_recent_entries(self, blackboard: Blackboard, n: int = 5) -> str:
        recent = blackboard.history[-n:] if blackboard.history else []
        return "\n".join([
            f"- [{e.source_agent}] {e.key}: {e.value[:100]}..."
            for e in recent
        ])

    def _format_agents(self) -> str:
        return "\n".join([f"- {name}: {desc}" for name, desc in self.agents.items()])
```

### LangGraph Integration

```python
from langgraph.graph import StateGraph, START, END
from typing import TypedDict

class BlackboardState(TypedDict):
    query: str
    blackboard: Blackboard
    controller_decision: ControllerDecision
    iterations: int
    max_iterations: int

def controller_node(state: BlackboardState) -> dict:
    controller = BlackboardController(AVAILABLE_AGENTS)
    decision = controller.decide_next(state["blackboard"])
    return {"controller_decision": decision}

def agent_dispatch_node(state: BlackboardState) -> dict:
    """Routes to the appropriate agent"""
    agent_name = state["controller_decision"].next_agent
    blackboard = state["blackboard"]

    # Get relevant context for this agent
    relevant_entries = get_relevant_entries(blackboard, agent_name)

    # Agent processes and writes to blackboard
    agent_result = AGENTS[agent_name].process(
        query=state["query"],
        context=relevant_entries
    )

    # Write result to blackboard
    blackboard.write(
        key=f"{agent_name}_output_{state['iterations']}",
        value=agent_result.output,
        entry_type=agent_result.entry_type,
        agent=agent_name,
        confidence=agent_result.confidence
    )

    return {
        "blackboard": blackboard,
        "iterations": state["iterations"] + 1
    }

def should_continue(state: BlackboardState) -> str:
    if state["controller_decision"].is_complete:
        return "finalize"
    if state["iterations"] >= state["max_iterations"]:
        return "finalize"
    return "dispatch"

def finalize_node(state: BlackboardState) -> dict:
    if state["controller_decision"].final_answer:
        return {"final_output": state["controller_decision"].final_answer}

    # Synthesize from blackboard
    final_entries = state["blackboard"].read_by_type(EntryType.RECOMMENDATION)
    return {"final_output": synthesize(final_entries)}

# Build Graph
graph = StateGraph(BlackboardState)
graph.add_node("controller", controller_node)
graph.add_node("dispatch", agent_dispatch_node)
graph.add_node("finalize", finalize_node)

graph.add_edge(START, "controller")
graph.add_conditional_edges(
    "controller",
    should_continue,
    {"dispatch": "dispatch", "finalize": "finalize"}
)
graph.add_edge("dispatch", "controller")
graph.add_edge("finalize", END)

blackboard_chain = graph.compile()
```

## Example: Evolving Integration

### Multi-Agent Idea Validation

```python
IDEA_AGENTS = {
    "technical_expert": "Evaluates technical feasibility and architecture",
    "market_analyst": "Analyzes market potential and competition",
    "user_researcher": "Assesses user needs and adoption likelihood",
    "financial_advisor": "Estimates costs, revenue, and ROI"
}

def validate_idea_with_blackboard(idea: str) -> dict:
    blackboard = Blackboard()

    # Initial entry
    blackboard.write(
        key="original_idea",
        value=idea,
        entry_type=EntryType.QUERY,
        agent="user",
        confidence=1.0
    )

    # Run blackboard system
    result = blackboard_chain.invoke({
        "query": idea,
        "blackboard": blackboard,
        "iterations": 0,
        "max_iterations": 10
    })

    return {
        "validation": result["final_output"],
        "contributions": blackboard.get_summary(),
        "trace": [e.dict() for e in blackboard.history]
    }
```

### Sparring Session mit Blackboard

```python
SPARRING_AGENTS = {
    "challenger": "Questions assumptions and plays devil's advocate",
    "expander": "Explores possibilities and extensions",
    "synthesizer": "Combines insights into coherent conclusions",
    "pragmatist": "Focuses on practical implementation"
}

# Controller decides based on conversation flow
# Each agent reads previous contributions
# Builds on or challenges prior entries
```

## Trade-offs

| Pro | Contra |
|-----|--------|
| Skaliert besser als direkte Kommunikation | Single Point of Failure |
| Asynchrone Updates möglich | Controller kann Bottleneck werden |
| Komplette Trace der Diskussion | Blackboard kann groß werden |
| Flexible Agent-Aktivierung | Komplexere Implementierung |
| Agents können parallel lesen | Schreib-Konflikte möglich |

## When to Use

- **JA**: Multi-Expert Systems, komplexe Beratung, iterative Verfeinerung
- **NEIN**: Simple Single-Agent Tasks, strikt sequentielle Workflows

## Comparison: Blackboard vs Direct Orchestration

| Aspekt | Blackboard | Direct Orchestration |
|--------|------------|---------------------|
| Kommunikation | Via Shared Memory | Direct Calls |
| Coupling | Loose | Tight |
| Flexibility | High (opportunistic) | Lower (predetermined) |
| Debugging | Easy (trace in BB) | Harder (distributed) |
| Overhead | Higher (BB management) | Lower |

## Related Patterns

- [Multi-Agent Orchestration](multi-agent-orchestration.md) - Alternative Koordination
- [Ensemble Pattern](../learnings/agentic-architectures-patterns.md#7-ensemble-pattern) - Parallel statt opportunistisch
- [PEV Pattern](pev-pattern.md) - Kann mit Blackboard kombiniert werden

---

**Navigation**: [← Patterns](README.md) | [Knowledge Index](../index.md)
