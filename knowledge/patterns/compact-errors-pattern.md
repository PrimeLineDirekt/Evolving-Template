# Compact Errors Pattern

**Typ**: Agent Architecture Pattern
**Confidence**: 88%
**Source**: HumanLayer 12-Factor Agents (Factor 9)
**Priority**: P2 - Medium

---

## Problem

Wenn Tool-Calls fehlschlagen, werden Fehler oft:

- Raw in den Context gedumpt (Token-Verschwendung)
- Nicht strukturiert formatiert (LLM versteht sie schlecht)
- Ohne Limit akkumuliert (Infinite Error Loops)
- Nicht für Self-Healing optimiert

## Solution

**Structured Error Handling**: Fehler kompakt und strukturiert in den Context einbauen, mit Limits und Escalation.

```
Tool Call Failed
      │
      ▼
┌──────────────────────┐
│  Format Error        │
│  (Compact Structure) │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│  Append to Context   │
│  <error>...</error>  │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐     ┌──────────────────┐
│  Check Error Count   │────►│  > Threshold?    │
└──────────────────────┘     └────────┬─────────┘
                                      │
                        ┌─────────────┴─────────────┐
                        │                           │
                        ▼                           ▼
                 ┌──────────┐               ┌──────────────┐
                 │  Retry   │               │  Escalate    │
                 │  (LLM)   │               │  to Human    │
                 └──────────┘               └──────────────┘
```

## Implementation

### Error Event Structure

```python
from dataclasses import dataclass
from typing import Optional, List
from datetime import datetime

@dataclass
class CompactError:
    """Structured error for context inclusion."""

    tool_name: str
    error_type: str  # "validation", "timeout", "auth", "unknown"
    message: str
    suggestion: Optional[str] = None  # What the LLM could try instead
    timestamp: datetime = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()

    def to_context(self) -> str:
        """Format for context window inclusion."""
        parts = [
            f"tool: {self.tool_name}",
            f"type: {self.error_type}",
            f"message: {self.message}"
        ]
        if self.suggestion:
            parts.append(f"suggestion: {self.suggestion}")

        return "<error>\n" + "\n".join(parts) + "\n</error>"


def format_error(exception: Exception, tool_name: str) -> CompactError:
    """Convert exception to compact error."""

    # Categorize error
    error_type = "unknown"
    suggestion = None

    if "timeout" in str(exception).lower():
        error_type = "timeout"
        suggestion = "Try with a simpler query or smaller dataset"
    elif "auth" in str(exception).lower() or "401" in str(exception):
        error_type = "auth"
        suggestion = "Check credentials or request human approval"
    elif "validation" in str(exception).lower() or "invalid" in str(exception).lower():
        error_type = "validation"
        suggestion = "Check input format and required fields"
    elif "not found" in str(exception).lower() or "404" in str(exception):
        error_type = "not_found"
        suggestion = "Verify the resource exists or try alternative"

    return CompactError(
        tool_name=tool_name,
        error_type=error_type,
        message=str(exception)[:200],  # Truncate long errors
        suggestion=suggestion
    )
```

### Error-Aware Agent Loop

```python
from typing import List
from dataclasses import dataclass, field

@dataclass
class ErrorTracker:
    """Track errors per tool to prevent infinite loops."""

    max_consecutive_errors: int = 3
    max_total_errors: int = 10

    # State
    consecutive_errors: dict = field(default_factory=dict)  # tool -> count
    total_errors: int = 0
    error_history: List[CompactError] = field(default_factory=list)

    def record_error(self, error: CompactError) -> bool:
        """
        Record error and check if should escalate.

        Returns:
            True if should continue, False if should escalate
        """
        self.total_errors += 1
        self.error_history.append(error)

        # Track consecutive errors per tool
        self.consecutive_errors[error.tool_name] = \
            self.consecutive_errors.get(error.tool_name, 0) + 1

        # Check thresholds
        if self.consecutive_errors[error.tool_name] >= self.max_consecutive_errors:
            return False  # Escalate

        if self.total_errors >= self.max_total_errors:
            return False  # Escalate

        return True  # Continue

    def record_success(self, tool_name: str):
        """Reset consecutive counter on success."""
        self.consecutive_errors[tool_name] = 0

    def get_context_errors(self, max_errors: int = 3) -> str:
        """Get recent errors for context."""
        recent = self.error_history[-max_errors:]
        return "\n\n".join(e.to_context() for e in recent)


class ResilientAgentLoop:
    """Agent loop with error compaction and escalation."""

    def __init__(self):
        self.error_tracker = ErrorTracker()
        self.thread_events: List[dict] = []

    async def run(self, initial_message: str):
        """Main agent loop with error handling."""

        self.thread_events.append({
            "type": "user_message",
            "data": initial_message
        })

        while True:
            # Determine next step
            context = self._build_context()
            next_step = await self._determine_next_step(context)

            if next_step.is_done:
                return next_step.result

            # Execute tool
            try:
                result = await self._execute_tool(next_step)

                # Success - record and continue
                self.error_tracker.record_success(next_step.tool_name)
                self.thread_events.append({
                    "type": f"{next_step.tool_name}_result",
                    "data": result
                })

            except Exception as e:
                # Format error compactly
                error = format_error(e, next_step.tool_name)

                # Check if should escalate
                should_continue = self.error_tracker.record_error(error)

                if not should_continue:
                    return await self._escalate_to_human(error)

                # Add error to context for LLM to learn from
                self.thread_events.append({
                    "type": "error",
                    "data": error.to_context()
                })

    def _build_context(self) -> str:
        """Build context including recent errors."""
        # ... build from thread_events
        pass

    async def _escalate_to_human(self, error: CompactError) -> dict:
        """Escalate to human when error threshold exceeded."""
        return {
            "status": "escalated",
            "reason": f"Too many errors with {error.tool_name}",
            "last_error": error.message,
            "error_history": [e.to_context() for e in self.error_tracker.error_history]
        }
```

### Context Compaction Strategy

```python
def compact_error_context(
    errors: List[CompactError],
    resolved_errors: List[CompactError],
    max_context_errors: int = 3
) -> str:
    """
    Compact errors for context window.

    Strategy:
    - Hide resolved errors (they clutter context)
    - Keep only recent unresolved errors
    - Summarize if too many
    """

    # Filter out resolved errors
    unresolved = [e for e in errors if e not in resolved_errors]

    if not unresolved:
        return ""  # No errors to show

    # Keep only most recent
    recent = unresolved[-max_context_errors:]

    # Format
    if len(unresolved) > max_context_errors:
        summary = f"<error_summary>\n{len(unresolved) - max_context_errors} older errors hidden\n</error_summary>\n\n"
    else:
        summary = ""

    return summary + "\n\n".join(e.to_context() for e in recent)
```

## Error Representation Strategies

| Strategy | When to Use | Example |
|----------|-------------|---------|
| **Full Error** | Debugging, first occurrence | Stack trace + message |
| **Compact Error** | Production, retries | Type + message + suggestion |
| **Summary** | Many errors | "3 validation errors in deploy_tool" |
| **Hidden** | Resolved errors | Remove from context entirely |

## Best Practices

### Error Limits

```python
# Recommended defaults
MAX_CONSECUTIVE_ERRORS_PER_TOOL = 3  # Same tool failing repeatedly
MAX_TOTAL_ERRORS = 10                # Overall error budget
MAX_ERRORS_IN_CONTEXT = 3            # Don't clutter context
```

### Error Categories & Suggestions

| Error Type | Auto-Suggestion |
|------------|-----------------|
| `timeout` | "Try simpler query or smaller dataset" |
| `auth` | "Request human approval for credentials" |
| `validation` | "Check input format against schema" |
| `not_found` | "Verify resource exists, list available options" |
| `rate_limit` | "Wait and retry, or use alternative API" |

### DO

1. **Kategorisieren**: Error types helfen LLM beim Verstehen
2. **Suggestions hinzufügen**: Was könnte das LLM anders machen?
3. **Limits setzen**: Infinite loops verhindern
4. **Escalate**: Humans einbeziehen wenn nötig
5. **Hide Resolved**: Gelöste Errors aus Context entfernen

### DON'T

1. **Raw Stack Traces**: Token-Verschwendung, wenig hilfreich
2. **Alle Errors behalten**: Context wird überladen
3. **Ohne Limits loopen**: Agent dreht sich im Kreis
4. **Errors ignorieren**: LLM kann aus Fehlern lernen

## Evolving Integration

### Aktueller Status

| Komponente | Error Handling | Status |
|------------|----------------|--------|
| **Orchestrator** | Basic try/catch | ⚠️ Keine Compaction |
| **Agent Loop** | Retry ohne Limit | ⚠️ Infinite Loop Risk |
| **Context** | Errors nicht strukturiert | ⚠️ Raw Append |

### Recommended Implementation

```python
# In your orchestrator
class ResilientOrchestrator:
    def __init__(self):
        self.error_tracker = ErrorTracker(
            max_consecutive_errors=3,
            max_total_errors=10
        )

    async def execute_agent(self, agent_id: str, ...):
        try:
            result = await agent.run(...)
            self.error_tracker.record_success(agent_id)
            return result
        except Exception as e:
            error = format_error(e, agent_id)

            if not self.error_tracker.record_error(error):
                # Escalate - mark session as needs_human_review
                self.session.needs_review = True
                self.session.escalation_reason = error.message
                raise EscalationError(error)

            # Add to context for retry
            self.context.add_error(error)
            raise  # Let orchestrator handle retry
```

**Effort**: ~3h | **Impact**: Prevents infinite loops, better error recovery

## Related Patterns

- [Context Window Ownership](context-window-ownership-pattern.md) - Overall Context Strategy
- [Reflection Pattern](reflection-pattern.md) - Self-Correction nach Errors
- [PEV Pattern](pev-pattern.md) - Verify-Phase kann Errors früh erkennen

---

**Navigation**: [← Patterns](README.md) | [Knowledge Index](../index.md)
