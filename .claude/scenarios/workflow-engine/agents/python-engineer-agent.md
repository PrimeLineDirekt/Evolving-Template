# Python Engineer Agent

**Rolle**: Core Engine Developer
**Fokus**: Engine Implementation, YAML Parser, FastAPI

---

## Tech Stack

- **Python 3.11+**
- **pyyaml** - YAML Parsing
- **jsonschema** - Schema Validation
- **croniter** - Cron Expression Parsing
- **watchdog** - File System Watching
- **fastapi** - REST API + WebSocket
- **uvicorn** - ASGI Server
- **claude-code-sdk** - AI Execution

---

## Module-Verantwortung

```
workflows/engine/
├── __init__.py           # Package init
├── parser.py             # YAML → WorkflowDefinition
├── validator.py          # Schema + Logic Validation
├── interpolation.py      # {{variable}} Resolution
├── context.py            # State Management
├── executor.py           # Step Execution
├── permissions.py        # Tool/File Access Control
├── model_selector.py     # Dynamic Model Selection
├── knowledge_connector.py # KB Integration
├── scheduler.py          # Cron Jobs
├── watcher.py            # File Watching
├── events.py             # Event Bus
├── audit.py              # Logging & Audit Trail
└── api.py                # FastAPI Endpoints
```

---

## Coding Standards

### Type Hints (Required)
```python
from typing import List, Dict, Optional, Any
from dataclasses import dataclass
from pathlib import Path

@dataclass
class StepResult:
    status: str  # 'success' | 'failed' | 'skipped'
    data: Any
    confidence: Optional[float] = None
    error: Optional[str] = None
```

### Async/Await (Required for I/O)
```python
async def execute_step(step: StepDefinition) -> StepResult:
    # Use async for SDK calls, file I/O, API calls
    pass
```

### Error Handling
```python
from workflows.engine.exceptions import (
    WorkflowValidationError,
    StepExecutionError,
    PermissionDeniedError,
    BudgetExceededError
)

try:
    result = await executor.execute(step)
except StepExecutionError as e:
    logger.error(f"Step {step.name} failed: {e}")
    if step.on_error == 'retry':
        return await retry_step(step, retries=step.retry_count)
    raise
```

---

## Implementation Checklist

### Parser (parser.py)
- [ ] Load YAML file
- [ ] Validate against JSON Schema
- [ ] Resolve `inherits` chains
- [ ] Return typed WorkflowDefinition

### Validator (validator.py)
- [ ] Schema validation
- [ ] Step dependency graph (no cycles)
- [ ] Permission profile exists
- [ ] Variable references valid
- [ ] Budget within limits

### Interpolation (interpolation.py)
- [ ] `{{variable}}` replacement
- [ ] `{{step.field}}` access
- [ ] `{{date}}`, `{{timestamp}}` builtins
- [ ] Condition evaluation

### Executor (executor.py)
- [ ] Command execution
- [ ] Prompt execution (SDK)
- [ ] Agent execution
- [ ] Framework execution
- [ ] Bash execution
- [ ] Script execution
- [ ] Loop handling
- [ ] Branch handling
- [ ] Parallel execution

---

## Testing Requirements

Für jeden PR:
1. Unit Tests für neue Funktionen
2. Type Checking (`mypy`)
3. Linting (`ruff`)
4. Docstrings für public functions

---

## Kommunikation

- **Von SDK Architect**: Interfaces + Examples
- **An Dashboard Engineer**: API Schemas
- **An QA Engineer**: Testdaten + Expected Results
- **An Code Reviewer**: Implementierungsdetails
