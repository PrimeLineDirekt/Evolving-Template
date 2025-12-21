# PEV Pattern (Plan-Execute-Verify)

**Typ**: Agent Pattern
**Confidence**: 90%
**Source**: FareedKhan-dev/all-agentic-architectures
**Priority**: P1 - High

---

## Problem

Komplexe Tasks scheitern weil:
1. Keine explizite Planung vor Ausführung
2. Keine Überprüfung der Ergebnisse
3. Keine Möglichkeit zur Korrektur bei Fehlern

## Solution

Drei-Phasen-Ansatz mit Self-Correction Loop:

```
┌─────────────────────────────────────────────────────┐
│                    PEV CYCLE                        │
│                                                     │
│    ┌──────────┐    ┌──────────┐    ┌──────────┐   │
│    │  PLANNER │───▶│ EXECUTOR │───▶│ VERIFIER │   │
│    └──────────┘    └──────────┘    └────┬─────┘   │
│         ▲                               │          │
│         │                               │          │
│         │         ┌─────────┐          │          │
│         └─────────│ REPLAN? │◀─────────┘          │
│                   └─────────┘                      │
│                        │                           │
│                        ▼                           │
│                   [COMPLETE]                       │
└─────────────────────────────────────────────────────┘
```

## Implementation

### Pydantic Models

```python
from pydantic import BaseModel, Field
from typing import Optional

class PlanStep(BaseModel):
    step_id: int
    description: str = Field(description="What to do")
    expected_output: str = Field(description="Success criteria")
    dependencies: list[int] = Field(default=[], description="IDs of required prior steps")
    tools_needed: list[str] = Field(default=[], description="Tools to use")

class Plan(BaseModel):
    goal: str
    steps: list[PlanStep]
    estimated_complexity: int = Field(ge=1, le=10)

class ExecutionResult(BaseModel):
    step_id: int
    actual_output: str
    success: bool
    error: Optional[str] = None
    artifacts: dict = Field(default={})

class VerificationResult(BaseModel):
    step_id: int
    is_valid: bool
    issues: list[str] = Field(default=[])
    needs_replan: bool
    can_continue: bool
```

### LangGraph Implementation

```python
from langgraph.graph import StateGraph, START, END
from typing import TypedDict

class PEVState(TypedDict):
    query: str
    plan: Plan
    current_step_index: int
    execution_results: list[ExecutionResult]
    verification: VerificationResult
    retry_count: int
    max_retries: int
    final_output: str

def planner_node(state: PEVState) -> dict:
    """Creates or updates the plan"""

    context = ""
    if state.get("execution_results"):
        # Include previous results for replanning
        context = f"""
        Previous attempt results:
        {format_results(state['execution_results'])}

        Issues encountered:
        {state['verification'].issues if state.get('verification') else 'None'}
        """

    prompt = f"""
    Task: {state['query']}
    {context}

    Create a step-by-step plan.
    Each step should be atomic and verifiable.
    """

    plan = llm.with_structured_output(Plan).invoke(prompt)
    return {
        "plan": plan,
        "current_step_index": 0,
        "retry_count": state.get("retry_count", 0)
    }

def executor_node(state: PEVState) -> dict:
    """Executes the current step"""

    step = state["plan"].steps[state["current_step_index"]]

    # Get dependencies
    dependencies = {}
    for dep_id in step.dependencies:
        dep_result = next(
            (r for r in state["execution_results"] if r.step_id == dep_id),
            None
        )
        if dep_result:
            dependencies[dep_id] = dep_result.actual_output

    prompt = f"""
    Execute this step:
    {step.description}

    Expected output: {step.expected_output}
    Dependencies: {dependencies}
    Available tools: {step.tools_needed}
    """

    try:
        result = execute_with_tools(prompt, step.tools_needed)
        execution_result = ExecutionResult(
            step_id=step.step_id,
            actual_output=result,
            success=True
        )
    except Exception as e:
        execution_result = ExecutionResult(
            step_id=step.step_id,
            actual_output="",
            success=False,
            error=str(e)
        )

    return {
        "execution_results": state["execution_results"] + [execution_result]
    }

def verifier_node(state: PEVState) -> dict:
    """Verifies the execution result"""

    step = state["plan"].steps[state["current_step_index"]]
    latest_result = state["execution_results"][-1]

    prompt = f"""
    Verify this execution:

    Expected: {step.expected_output}
    Actual: {latest_result.actual_output}
    Success: {latest_result.success}
    Error: {latest_result.error}

    Determine:
    1. Does the output meet expectations?
    2. Are there any issues?
    3. Should we replan or continue?
    """

    verification = llm.with_structured_output(VerificationResult).invoke(prompt)
    verification.step_id = step.step_id

    return {"verification": verification}

def route_after_verify(state: PEVState) -> str:
    """Decides next action based on verification"""

    v = state["verification"]

    if v.needs_replan:
        if state["retry_count"] >= state.get("max_retries", 2):
            return "fail"
        return "replan"

    if not v.can_continue:
        return "fail"

    if state["current_step_index"] >= len(state["plan"].steps) - 1:
        return "complete"

    return "next_step"

def next_step_node(state: PEVState) -> dict:
    return {"current_step_index": state["current_step_index"] + 1}

def replan_node(state: PEVState) -> dict:
    return {"retry_count": state["retry_count"] + 1}

def complete_node(state: PEVState) -> dict:
    # Aggregate all results into final output
    outputs = [r.actual_output for r in state["execution_results"] if r.success]
    return {"final_output": "\n\n".join(outputs)}

# Build Graph
graph = StateGraph(PEVState)
graph.add_node("plan", planner_node)
graph.add_node("execute", executor_node)
graph.add_node("verify", verifier_node)
graph.add_node("next_step", next_step_node)
graph.add_node("replan", replan_node)
graph.add_node("complete", complete_node)
graph.add_node("fail", lambda s: {"final_output": "Task failed after retries"})

graph.add_edge(START, "plan")
graph.add_edge("plan", "execute")
graph.add_edge("execute", "verify")
graph.add_conditional_edges(
    "verify",
    route_after_verify,
    {
        "next_step": "next_step",
        "replan": "replan",
        "complete": "complete",
        "fail": "fail"
    }
)
graph.add_edge("next_step", "execute")
graph.add_edge("replan", "plan")
graph.add_edge("complete", END)
graph.add_edge("fail", END)

pev_chain = graph.compile()
```

## Example: Evolving Integration

### Idea Workflow mit PEV

```python
class IdeaWorkflowState(TypedDict):
    idea: Idea
    plan: Plan  # Steps: validate → expand → connect → synthesize
    current_phase: str
    phase_results: dict
    verification: VerificationResult

IDEA_WORKFLOW_STEPS = [
    PlanStep(
        step_id=1,
        description="Validate idea feasibility and market potential",
        expected_output="Validation report with scores",
        tools_needed=["idea-validator-agent"]
    ),
    PlanStep(
        step_id=2,
        description="Expand idea with features and opportunities",
        expected_output="Expanded feature list and market opportunities",
        dependencies=[1],
        tools_needed=["idea-expander-agent"]
    ),
    PlanStep(
        step_id=3,
        description="Find connections to existing ideas and projects",
        expected_output="Synergy map with connection scores",
        dependencies=[1, 2],
        tools_needed=["idea-connector-agent"]
    ),
    PlanStep(
        step_id=4,
        description="Synthesize into actionable next steps",
        expected_output="Prioritized action plan",
        dependencies=[1, 2, 3],
        tools_needed=["knowledge-synthesizer-agent"]
    )
]
```

### Project Analyze mit PEV

```python
PROJECT_ANALYZE_STEPS = [
    PlanStep(
        step_id=1,
        description="Scan directory structure and identify key files",
        expected_output="File tree with categorization",
        tools_needed=["glob", "read"]
    ),
    PlanStep(
        step_id=2,
        description="Analyze architecture patterns",
        expected_output="Architecture diagram and patterns used",
        dependencies=[1],
        tools_needed=["codebase-analyzer-agent"]
    ),
    PlanStep(
        step_id=3,
        description="Detect n8n workflows if present",
        expected_output="n8n workflow analysis (if applicable)",
        dependencies=[1],
        tools_needed=["n8n-expert-agent"]  # Conditional
    ),
    PlanStep(
        step_id=4,
        description="Generate recommendations",
        expected_output="Improvement recommendations with priorities",
        dependencies=[2, 3],
        tools_needed=["knowledge-synthesizer-agent"]
    )
]
```

## Trade-offs

| Pro | Contra |
|-----|--------|
| Robust bei komplexen Tasks | Overhead bei einfachen Tasks |
| Self-Correction eingebaut | Kann bei hartnäckigen Fehlern loopen |
| Expliziter Fortschritt | Mehr Token durch Planung + Verifikation |
| Nachvollziehbar | Replan kann Plan drastisch ändern |
| Partial Results bei Failure | Initiale Planung kann suboptimal sein |

## When to Use

- **JA**: Multi-Step Workflows, komplexe Analysen, Tasks mit Dependencies
- **NEIN**: Single-Step Tasks, schnelle Lookups, Chat

## Related Patterns

- [Task Decomposition Pipeline](task-decomposition-pipeline.md) - Ähnliche Plan-Phase
- [Reflection Pattern](reflection-pattern.md) - Verify ähnlich wie Critic
- [Multi-Agent Orchestration](multi-agent-orchestration.md) - PEV als Orchestration Strategy

---

**Navigation**: [← Patterns](README.md) | [Knowledge Index](../index.md)
