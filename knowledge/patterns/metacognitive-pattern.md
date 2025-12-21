# Metacognitive Pattern (Self-Aware Agents)

**Typ**: Agent Pattern
**Confidence**: 88%
**Source**: FareedKhan-dev/all-agentic-architectures
**Priority**: P1 - High

---

## Problem

Agents wissen nicht, was sie nicht wissen:
- Handeln außerhalb ihrer Kompetenz ohne Warnung
- Overconfidence bei unsicheren Antworten
- Keine Selbsteinschätzung der eigenen Limitationen
- Falsche Model-Wahl (Haiku für komplexe Tasks)

## Solution

Self-Model mit Capability Assessment vor jeder Aktion:

```
Query
  │
  ▼
┌─────────────────────────────────────────────┐
│           SELF-ASSESSMENT                    │
│                                             │
│  "Kann ich das?"                            │
│  "Was brauche ich dafür?"                   │
│  "Wie sicher bin ich?"                      │
│                                             │
│  ┌─────────────────────────────────────┐    │
│  │ Capabilities Check                   │   │
│  │ • Required skills                    │   │
│  │ • Available tools                    │   │
│  │ • Model requirements                 │   │
│  │ • Confidence level                   │   │
│  └─────────────────────────────────────┘    │
└─────────────────┬───────────────────────────┘
                  │
      ┌───────────┼───────────┐
      │           │           │
      ▼           ▼           ▼
┌─────────┐ ┌─────────┐ ┌─────────┐
│  HIGH   │ │ MEDIUM  │ │  LOW    │
│Confidence│ │Confidence│ │Confidence│
│         │ │         │ │         │
│Execute  │ │ Clarify │ │Escalate │
│directly │ │ first   │ │or Refuse│
└─────────┘ └─────────┘ └─────────┘
```

## Implementation

### Self-Assessment Models

```python
from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum

class ConfidenceLevel(str, Enum):
    HIGH = "high"      # > 0.8
    MEDIUM = "medium"  # 0.5 - 0.8
    LOW = "low"        # < 0.5

class SuggestedAction(str, Enum):
    EXECUTE = "execute"           # Proceed with task
    CLARIFY = "clarify"           # Ask for more info
    ESCALATE = "escalate"         # Hand to human/better model
    DELEGATE = "delegate"         # Use specialized agent
    REFUSE = "refuse"             # Cannot/should not do

class SelfAssessment(BaseModel):
    can_handle: bool
    confidence: float = Field(ge=0, le=1)
    confidence_level: ConfidenceLevel
    required_capabilities: list[str]
    available_capabilities: list[str]
    missing_capabilities: list[str]
    suggested_action: SuggestedAction
    reasoning: str
    recommended_model: Optional[str] = None  # haiku/sonnet/opus
    alternative_agents: list[str] = Field(default=[])

class Capability(BaseModel):
    name: str
    description: str
    proficiency: float = Field(ge=0, le=1)  # How good at this
    requires_tools: list[str] = Field(default=[])
```

### Metacognitive Agent Base Class

```python
class MetacognitiveAgent:
    def __init__(
        self,
        name: str,
        capabilities: list[Capability],
        available_tools: list[str]
    ):
        self.name = name
        self.capabilities = capabilities
        self.available_tools = available_tools
        self.self_model = self._build_self_model()

    def _build_self_model(self) -> str:
        cap_list = "\n".join([
            f"- {c.name}: {c.description} (proficiency: {c.proficiency})"
            for c in self.capabilities
        ])

        return f"""
        I am {self.name}, an AI agent.

        MY CAPABILITIES:
        {cap_list}

        MY TOOLS:
        {self.available_tools}

        MY LIMITATIONS:
        - I should not attempt tasks requiring capabilities I don't have
        - I should escalate when confidence is low
        - I should be honest about uncertainty
        - I should recommend better-suited agents when available

        DECISION RULES:
        - Confidence > 0.8: Execute directly
        - Confidence 0.5-0.8: Ask clarifying questions first
        - Confidence < 0.5: Escalate or refuse
        """

    def assess_task(self, query: str, context: dict = {}) -> SelfAssessment:
        prompt = f"""
        {self.self_model}

        TASK: {query}
        CONTEXT: {context}

        Perform honest self-assessment:
        1. What capabilities does this task require?
        2. Which do I have? Which am I missing?
        3. How confident am I that I can succeed?
        4. What should I do?

        Be conservative - it's better to ask for help than fail.
        """

        return llm.with_structured_output(SelfAssessment).invoke(prompt)

    def process(self, query: str, context: dict = {}) -> dict:
        # Always assess first
        assessment = self.assess_task(query, context)

        if assessment.suggested_action == SuggestedAction.EXECUTE:
            return self._execute(query, context, assessment)

        elif assessment.suggested_action == SuggestedAction.CLARIFY:
            return self._request_clarification(query, assessment)

        elif assessment.suggested_action == SuggestedAction.ESCALATE:
            return self._escalate(query, assessment)

        elif assessment.suggested_action == SuggestedAction.DELEGATE:
            return self._delegate(query, assessment)

        else:  # REFUSE
            return self._refuse(query, assessment)

    def _execute(self, query: str, context: dict, assessment: SelfAssessment) -> dict:
        # Actual task execution
        result = self._do_task(query, context)
        return {
            "status": "completed",
            "result": result,
            "confidence": assessment.confidence,
            "reasoning": assessment.reasoning
        }

    def _request_clarification(self, query: str, assessment: SelfAssessment) -> dict:
        questions = self._generate_clarifying_questions(query, assessment)
        return {
            "status": "needs_clarification",
            "questions": questions,
            "missing": assessment.missing_capabilities,
            "reasoning": assessment.reasoning
        }

    def _escalate(self, query: str, assessment: SelfAssessment) -> dict:
        return {
            "status": "escalated",
            "recommended_model": assessment.recommended_model,
            "alternative_agents": assessment.alternative_agents,
            "reasoning": assessment.reasoning,
            "missing_capabilities": assessment.missing_capabilities
        }

    def _delegate(self, query: str, assessment: SelfAssessment) -> dict:
        return {
            "status": "delegated",
            "delegate_to": assessment.alternative_agents[0],
            "reasoning": assessment.reasoning
        }

    def _refuse(self, query: str, assessment: SelfAssessment) -> dict:
        return {
            "status": "refused",
            "reasoning": assessment.reasoning,
            "missing_capabilities": assessment.missing_capabilities
        }
```

### Model Selection Integration

```python
class ModelSelector:
    """Uses metacognition for optimal model selection"""

    MODEL_CAPABILITIES = {
        "haiku": {
            "speed": 1.0,
            "cost": 0.1,
            "reasoning": 0.6,
            "creativity": 0.5,
            "best_for": ["simple_queries", "formatting", "classification"]
        },
        "sonnet": {
            "speed": 0.7,
            "cost": 0.5,
            "reasoning": 0.8,
            "creativity": 0.8,
            "best_for": ["analysis", "coding", "general"]
        },
        "opus": {
            "speed": 0.4,
            "cost": 1.0,
            "reasoning": 1.0,
            "creativity": 1.0,
            "best_for": ["complex_reasoning", "research", "strategy"]
        }
    }

    def select_model(self, task_assessment: SelfAssessment) -> str:
        # Already recommended by assessment?
        if task_assessment.recommended_model:
            return task_assessment.recommended_model

        # Determine based on requirements
        required = set(task_assessment.required_capabilities)

        if any(cap in required for cap in ["complex_reasoning", "multi_step_planning", "research"]):
            return "opus"

        if any(cap in required for cap in ["coding", "analysis", "summarization"]):
            return "sonnet"

        if task_assessment.confidence > 0.9:
            return "haiku"  # Simple task, use fast model

        return "sonnet"  # Default to balanced
```

## Example: Evolving Integration

### Idea Validator with Metacognition

```python
idea_validator = MetacognitiveAgent(
    name="Idea Validator",
    capabilities=[
        Capability(
            name="market_analysis",
            description="Analyze market potential and competition",
            proficiency=0.8
        ),
        Capability(
            name="technical_feasibility",
            description="Assess technical implementation complexity",
            proficiency=0.9
        ),
        Capability(
            name="financial_modeling",
            description="Create financial projections",
            proficiency=0.5  # Lower proficiency - might escalate
        )
    ],
    available_tools=["web_search", "knowledge_base"]
)

# Usage
result = idea_validator.process(
    query="Validate SaaS idea for AI-powered tax consulting",
    context={"domain": "fintech", "target": "german_expats"}
)

# If financial_modeling is required with high precision:
# → Will escalate to opus or delegate to financial-expert-agent
```

### Command Router with Metacognition

```python
def route_command(user_input: str) -> dict:
    """Route to appropriate command/model based on self-assessment"""

    # Quick assessment
    assessment = assess_input_complexity(user_input)

    if assessment.confidence_level == ConfidenceLevel.HIGH:
        # Simple command, use haiku
        return {"model": "haiku", "action": assessment.suggested_action}

    elif assessment.confidence_level == ConfidenceLevel.MEDIUM:
        # Moderate complexity, use sonnet
        return {"model": "sonnet", "action": assessment.suggested_action}

    else:
        # Complex or uncertain, use opus
        return {"model": "opus", "action": "plan_first"}
```

## Trade-offs

| Pro | Contra |
|-----|--------|
| Verhindert Overconfidence | Assessment Overhead |
| Bessere Error Prevention | Kann zu konservativ sein |
| Optimale Model-Nutzung | Zusätzliche Latenz |
| Transparente Limitationen | Komplexere Agent-Logik |
| Automatische Delegation | Self-Model kann falsch sein |

## When to Use

- **JA**: Kritische Entscheidungen, Model Selection, Agent Routing
- **NEIN**: Triviale Tasks, Chat, bekannte simple Workflows

## Confidence Calibration

```python
# Calibrate self-assessment accuracy over time
class ConfidenceCalibrator:
    def __init__(self):
        self.predictions: list[tuple[float, bool]] = []

    def record(self, predicted_confidence: float, actual_success: bool):
        self.predictions.append((predicted_confidence, actual_success))

    def get_calibration_error(self) -> float:
        """Lower is better - predicted confidence should match actual success rate"""
        bins = self._bin_predictions()
        errors = []
        for bin_conf, outcomes in bins.items():
            actual_rate = sum(outcomes) / len(outcomes)
            errors.append(abs(bin_conf - actual_rate))
        return sum(errors) / len(errors)

    def should_adjust(self) -> str:
        error = self.get_calibration_error()
        if error > 0.2:
            # Check direction
            if self._is_overconfident():
                return "lower_confidence"
            return "raise_confidence"
        return "calibrated"
```

## Related Patterns

- [Model Selection Strategy](../index.md#model-selection-strategy) - Anwendung für Model Tiering
- [Multi-Agent Orchestration](multi-agent-orchestration.md) - Delegation zu spezialisierten Agents
- [Reflection Pattern](reflection-pattern.md) - Self-Critique nach Ausführung

---

**Navigation**: [← Patterns](README.md) | [Knowledge Index](../index.md)
