# Context Window Ownership Pattern

**Typ**: Agent Architecture Pattern
**Confidence**: 90%
**Source**: HumanLayer 12-Factor Agents (Factor 3)
**Priority**: P1 - High

---

## Problem

Standard LLM Message-Formate (OpenAI-Style `role: user/assistant/system`) sind:

- Token-ineffizient (viel Overhead)
- Nicht optimiert für spezifische Use Cases
- Starr und unflexibel
- Keine Kontrolle über Information Density

## Solution

**Aktive Context-Kontrolle**: Statt Standard-Formate zu akzeptieren, Context explizit für den spezifischen Use Case strukturieren.

```
┌─────────────────────────────────────┐
│         Context Components          │
├─────────────────────────────────────┤
│  • System Prompts & Instructions    │
│  • Retrieved Data (RAG)             │
│  • Historical State & Tool Results  │
│  • Memory (Past Conversations)      │
│  • Structured Output Specs          │
└─────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────┐
│    Custom Context Engineering       │
│  ┌─────────────────────────────┐   │
│  │  Transform to Optimal Format │   │
│  │  (XML, YAML, Compact JSON)   │   │
│  └─────────────────────────────┘   │
└─────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────┐
│         LLM Processing              │
│   (Stateless: Input → Output)       │
└─────────────────────────────────────┘
```

**Core Principle**: "Everything is context engineering. LLMs are stateless functions that turn inputs into outputs."

## Implementation

### Event-Based Context Structure

```python
from typing import Literal, Union, List
from dataclasses import dataclass

@dataclass
class Event:
    """Single event in the context thread."""
    type: str  # e.g., "user_query", "tool_result", "error"
    data: Union[dict, str]

@dataclass
class Thread:
    """Complete context thread."""
    events: List[Event]


def event_to_prompt(event: Event) -> str:
    """Convert event to XML-tagged prompt section."""
    if isinstance(event.data, dict):
        # YAML for structured data (more token-efficient than JSON)
        import yaml
        data_str = yaml.dump(event.data, default_flow_style=False)
    else:
        data_str = str(event.data)

    return f"<{event.type}>\n{data_str}</{event.type}>"


def thread_to_prompt(thread: Thread) -> str:
    """Convert entire thread to LLM prompt."""
    return '\n\n'.join(
        event_to_prompt(event) for event in thread.events
    )
```

### Praktisches Beispiel

**Standard Format (Ineffizient)**:
```json
{
  "messages": [
    {"role": "system", "content": "You are a deployment assistant..."},
    {"role": "user", "content": "Deploy the latest backend"},
    {"role": "assistant", "content": null, "tool_calls": [...]},
    {"role": "tool", "tool_call_id": "...", "content": "{\"tags\": [...]}"}
  ]
}
```

**Optimiertes Format (Token-Efficient)**:
```xml
<slack_message>
From: @alex
Channel: #deployments
Text: Can you deploy the latest backend?
</slack_message>

<list_git_tags_result>
tags:
  - name: v1.2.3
    commit: abc123
    date: 2024-03-15
</list_git_tags_result>

<deploy_backend>
intent: deploy_backend
tag: v1.2.3
</deploy_backend>
```

### Context Builder Pattern

```python
class ContextBuilder:
    """Builds optimized context for LLM calls."""

    def __init__(self, max_tokens: int = 8000):
        self.max_tokens = max_tokens
        self.events: List[Event] = []

    def add_system_context(self, instructions: str) -> 'ContextBuilder':
        """Add system instructions."""
        self.events.insert(0, Event(
            type="system",
            data=instructions
        ))
        return self

    def add_user_input(self, input_data: dict) -> 'ContextBuilder':
        """Add user input with relevant metadata."""
        self.events.append(Event(
            type="user_input",
            data=input_data
        ))
        return self

    def add_tool_result(self, tool_name: str, result: dict) -> 'ContextBuilder':
        """Add tool execution result."""
        self.events.append(Event(
            type=f"{tool_name}_result",
            data=result
        ))
        return self

    def add_retrieved_context(self, docs: List[str], source: str) -> 'ContextBuilder':
        """Add RAG-retrieved documents."""
        self.events.append(Event(
            type=f"retrieved_{source}",
            data={"documents": docs}
        ))
        return self

    def build(self) -> str:
        """Build final context string."""
        return thread_to_prompt(Thread(events=self.events))

    def build_with_truncation(self) -> str:
        """Build with intelligent truncation if needed."""
        full_context = self.build()

        # Simple token estimation (4 chars ≈ 1 token)
        estimated_tokens = len(full_context) // 4

        if estimated_tokens <= self.max_tokens:
            return full_context

        # Truncate older events (keep system + recent)
        system_events = [e for e in self.events if e.type == "system"]
        other_events = [e for e in self.events if e.type != "system"]

        # Keep most recent events
        while estimated_tokens > self.max_tokens and len(other_events) > 1:
            other_events.pop(0)  # Remove oldest
            truncated = Thread(events=system_events + other_events)
            estimated_tokens = len(thread_to_prompt(truncated)) // 4

        return thread_to_prompt(Thread(events=system_events + other_events))
```

## Format Comparison

| Format | Tokens (Est.) | Readability | Flexibility |
|--------|---------------|-------------|-------------|
| OpenAI Messages JSON | 100% (Baseline) | Medium | Low |
| XML-Tagged | ~70-80% | High | High |
| YAML Data | ~60-75% | High | High |
| Compact Custom | ~50-60% | Medium | Very High |

## Best Practices

### DO

1. **Experimentieren**: "I don't know what's the best approach, but I know you want the flexibility to try EVERYTHING"
2. **Structured Data als YAML**: Weniger Tokens als JSON, besser lesbar
3. **Semantic Tags**: `<deployment_result>` statt generisches `<data>`
4. **Filter Sensitive Data**: VOR dem LLM-Call entfernen
5. **Relevanz priorisieren**: Wichtigste Infos zuerst

### DON'T

1. **Blindes Framework-Vertrauen**: Standard-Formate hinterfragen
2. **Alles behalten**: Irrelevante History entfernen
3. **Raw Errors dumpen**: Errors strukturiert formatieren (→ Compact Errors Pattern)
4. **One-Size-Fits-All**: Verschiedene Tasks brauchen verschiedene Formate

## Evolving Integration

### Aktueller Status

| Komponente | Context Control | Status |
|------------|-----------------|--------|
| **Orchestrator** | Event-based Thread | ⚠️ Standard JSON |
| **Agent Prompts** | Strukturierte Sections | ✅ XML-Style |
| **Tool Results** | Direct Append | ⚠️ Optimierbar |
| **Error Handling** | Append to Context | ⚠️ Siehe Compact Errors |

### Empfehlung

**Für komplexe Multi-Agent Systeme**: Bei nächstem Refactoring Context Builder Pattern einführen:

```python
# In resilient_orchestrator.py
context = (
    ContextBuilder(max_tokens=6000)
    .add_system_context(agent.system_prompt)
    .add_user_input({"profile": profile.summary, "query": query})
    .add_retrieved_context(kb_results, source="tax_knowledge")
    .build()
)
```

**Aufwand**: ~4h | **Impact**: Token-Reduktion ~20-30%

## When to Use

- **JA**: Multi-Turn Agents, RAG Systems, Tool-Heavy Workflows
- **NEIN**: Simple Single-Turn Calls, Bereits optimierte Pipelines

## Related Patterns

- [Compact Errors Pattern](compact-errors-pattern.md) - Error-spezifische Context-Optimierung
- [Checkpoint Validation](checkpoint-validation-pattern.md) - Context State Management
- [Multi-Agent Orchestration](multi-agent-orchestration.md) - Context Sharing zwischen Agents

---

**Navigation**: [← Patterns](README.md) | [Knowledge Index](../index.md)
