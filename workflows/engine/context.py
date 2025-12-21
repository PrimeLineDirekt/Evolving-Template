"""
Workflow Engine - Context Manager

Manages workflow state, step results, and execution history.
"""

import json
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional

from workflows.engine.models import StepStatus, LogLevel


# ═══════════════════════════════════════════════════════════════
# LOG ENTRY
# ═══════════════════════════════════════════════════════════════

class LogType(str, Enum):
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    DEBUG = "debug"
    STEP_START = "step_start"
    STEP_END = "step_end"
    TOOL_CALL = "tool_call"


@dataclass
class LogEntry:
    timestamp: datetime
    type: LogType
    message: str
    step: Optional[str] = None
    data: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "timestamp": self.timestamp.isoformat(),
            "type": self.type.value,
            "message": self.message,
            "step": self.step,
            "data": self.data,
        }


# ═══════════════════════════════════════════════════════════════
# CONTEXT SNAPSHOT (for checkpointing)
# ═══════════════════════════════════════════════════════════════

@dataclass
class ContextSnapshot:
    """Immutable snapshot of context state for checkpointing."""
    run_id: str
    workflow_name: str
    current_step: int
    variables: Dict[str, Any]
    step_results: Dict[str, Any]
    token_usage: int
    cost: float
    timestamp: datetime

    def to_dict(self) -> Dict[str, Any]:
        return {
            "run_id": self.run_id,
            "workflow_name": self.workflow_name,
            "current_step": self.current_step,
            "variables": self.variables,
            "step_results": self.step_results,
            "token_usage": self.token_usage,
            "cost": self.cost,
            "timestamp": self.timestamp.isoformat(),
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ContextSnapshot':
        return cls(
            run_id=data["run_id"],
            workflow_name=data["workflow_name"],
            current_step=data["current_step"],
            variables=data["variables"],
            step_results=data["step_results"],
            token_usage=data["token_usage"],
            cost=data["cost"],
            timestamp=datetime.fromisoformat(data["timestamp"]),
        )


# ═══════════════════════════════════════════════════════════════
# MODEL COST TABLE
# ═══════════════════════════════════════════════════════════════

# Approximate costs per 1M tokens (input/output averaged)
MODEL_COSTS = {
    "haiku": 0.00025,      # $0.25 per 1M tokens
    "sonnet": 0.003,       # $3.00 per 1M tokens
    "opus": 0.015,         # $15.00 per 1M tokens
    "claude-3-haiku": 0.00025,
    "claude-3-sonnet": 0.003,
    "claude-3-opus": 0.015,
    "claude-3-5-sonnet": 0.003,
    "claude-sonnet-4": 0.003,
    "claude-opus-4": 0.015,
}


def estimate_cost(tokens: int, model: str) -> float:
    """Estimate cost for token usage on a model."""
    # Normalize model name
    model_key = model.lower()
    for key in MODEL_COSTS:
        if key in model_key:
            return (tokens / 1_000_000) * MODEL_COSTS[key]
    # Default to sonnet pricing
    return (tokens / 1_000_000) * MODEL_COSTS["sonnet"]


# ═══════════════════════════════════════════════════════════════
# WORKFLOW CONTEXT
# ═══════════════════════════════════════════════════════════════

class WorkflowContext:
    """
    Manages all state during workflow execution.

    Provides:
    - Variable storage and retrieval
    - Step result tracking
    - Token/cost accounting
    - Logging
    - Checkpointing for crash recovery
    """

    def __init__(
        self,
        workflow_name: str,
        run_id: Optional[str] = None,
        log_level: LogLevel = LogLevel.STANDARD,
    ):
        self.workflow_name = workflow_name
        self.run_id = run_id or self._generate_run_id()
        self.log_level = log_level

        self.started_at = datetime.now()
        self.completed_at: Optional[datetime] = None

        # State
        self.variables: Dict[str, Any] = {}
        self.step_results: Dict[str, Any] = {}
        self.current_step: int = 0
        self.current_step_name: Optional[str] = None
        self.status: StepStatus = StepStatus.PENDING

        # Accounting
        self.token_usage: int = 0
        self.cost: float = 0.0

        # Logs
        self.logs: List[LogEntry] = []

        # Checkpoint path
        self._checkpoint_dir = Path("workflows/checkpoints")
        self._checkpoint_dir.mkdir(parents=True, exist_ok=True)

    def _generate_run_id(self) -> str:
        """Generate unique run ID."""
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        short_uuid = str(uuid.uuid4())[:8]
        return f"{timestamp}-{short_uuid}"

    # ─────────────────────────────────────────────────────────────
    # VARIABLE MANAGEMENT
    # ─────────────────────────────────────────────────────────────

    def store(self, key: str, value: Any):
        """Store a value in context."""
        self.variables[key] = value
        self._log(LogType.DEBUG, f"Stored '{key}'", data={"key": key})

    def get(self, key: str, default: Any = None) -> Any:
        """Get a value from context."""
        # Check variables first
        if key in self.variables:
            return self.variables[key]

        # Check step results
        if key in self.step_results:
            return self.step_results[key]

        return default

    def get_all(self) -> Dict[str, Any]:
        """Get all context data for interpolation."""
        return {
            **self.variables,
            **self.step_results,
            "workflow": self.workflow_name,
            "run_id": self.run_id,
        }

    def store_step_result(self, step_name: str, result: Any):
        """Store a step's result."""
        self.step_results[step_name] = result
        self._log(
            LogType.DEBUG,
            f"Stored step result for '{step_name}'",
            step=step_name,
        )

    # ─────────────────────────────────────────────────────────────
    # TOKEN & COST TRACKING
    # ─────────────────────────────────────────────────────────────

    def add_tokens(self, count: int, model: str = "sonnet"):
        """Add token usage and update cost estimate."""
        self.token_usage += count
        self.cost += estimate_cost(count, model)

    def get_usage(self) -> Dict[str, Any]:
        """Get current usage statistics."""
        return {
            "tokens": self.token_usage,
            "cost": round(self.cost, 4),
            "steps_completed": len(self.step_results),
            "duration_seconds": self._get_duration_seconds(),
        }

    def _get_duration_seconds(self) -> float:
        """Get elapsed time in seconds."""
        end = self.completed_at or datetime.now()
        return (end - self.started_at).total_seconds()

    # ─────────────────────────────────────────────────────────────
    # LOGGING
    # ─────────────────────────────────────────────────────────────

    def log(self, message: str, level: LogType = LogType.INFO):
        """Add a log entry."""
        self._log(level, message, step=self.current_step_name)

    def log_step_start(self, step_name: str):
        """Log step start."""
        self.current_step_name = step_name
        self._log(LogType.STEP_START, f"Starting step: {step_name}", step=step_name)

    def log_step_end(self, step_name: str, status: StepStatus):
        """Log step completion."""
        self._log(
            LogType.STEP_END,
            f"Completed step: {step_name} ({status.value})",
            step=step_name,
            data={"status": status.value},
        )

    def log_tool_call(self, tool: str, params: Dict[str, Any], result: Any = None):
        """Log a tool call."""
        if self.log_level == LogLevel.VERBOSE:
            self._log(
                LogType.TOOL_CALL,
                f"Tool call: {tool}",
                step=self.current_step_name,
                data={"tool": tool, "params": params, "result": result},
            )
        elif self.log_level == LogLevel.STANDARD:
            self._log(
                LogType.TOOL_CALL,
                f"Tool call: {tool}",
                step=self.current_step_name,
                data={"tool": tool},
            )

    def log_error(self, message: str, error: Optional[Exception] = None):
        """Log an error."""
        data = {"error": str(error)} if error else None
        self._log(LogType.ERROR, message, step=self.current_step_name, data=data)

    def log_warning(self, message: str):
        """Log a warning."""
        self._log(LogType.WARNING, message, step=self.current_step_name)

    def _log(
        self,
        log_type: LogType,
        message: str,
        step: Optional[str] = None,
        data: Optional[Dict[str, Any]] = None,
    ):
        """Internal logging method."""
        # Filter by log level
        if self.log_level == LogLevel.MINIMAL:
            if log_type not in (LogType.ERROR, LogType.STEP_START, LogType.STEP_END):
                return

        entry = LogEntry(
            timestamp=datetime.now(),
            type=log_type,
            message=message,
            step=step,
            data=data,
        )
        self.logs.append(entry)

    def get_logs(self, step: Optional[str] = None) -> List[LogEntry]:
        """Get logs, optionally filtered by step."""
        if step:
            return [log for log in self.logs if log.step == step]
        return self.logs

    # ─────────────────────────────────────────────────────────────
    # CHECKPOINTING
    # ─────────────────────────────────────────────────────────────

    def checkpoint(self) -> ContextSnapshot:
        """Create a snapshot for crash recovery."""
        snapshot = ContextSnapshot(
            run_id=self.run_id,
            workflow_name=self.workflow_name,
            current_step=self.current_step,
            variables=self.variables.copy(),
            step_results=self.step_results.copy(),
            token_usage=self.token_usage,
            cost=self.cost,
            timestamp=datetime.now(),
        )

        # Persist to disk
        checkpoint_path = self._get_checkpoint_path()
        checkpoint_path.write_text(
            json.dumps(snapshot.to_dict(), indent=2, ensure_ascii=False)
        )

        self._log(LogType.DEBUG, f"Checkpoint created at step {self.current_step}")
        return snapshot

    def restore(self, snapshot: ContextSnapshot):
        """Restore from a checkpoint."""
        self.run_id = snapshot.run_id
        self.workflow_name = snapshot.workflow_name
        self.current_step = snapshot.current_step
        self.variables = snapshot.variables.copy()
        self.step_results = snapshot.step_results.copy()
        self.token_usage = snapshot.token_usage
        self.cost = snapshot.cost

        self._log(
            LogType.INFO,
            f"Restored from checkpoint at step {self.current_step}",
        )

    def _get_checkpoint_path(self) -> Path:
        """Get path for checkpoint file."""
        return self._checkpoint_dir / f"{self.workflow_name}-{self.run_id}.json"

    def clear_checkpoint(self):
        """Remove checkpoint file after successful completion."""
        checkpoint_path = self._get_checkpoint_path()
        if checkpoint_path.exists():
            checkpoint_path.unlink()

    @classmethod
    def load_checkpoint(cls, workflow_name: str, run_id: str) -> Optional['WorkflowContext']:
        """Load context from a checkpoint file."""
        checkpoint_dir = Path("workflows/checkpoints")
        checkpoint_path = checkpoint_dir / f"{workflow_name}-{run_id}.json"

        if not checkpoint_path.exists():
            return None

        data = json.loads(checkpoint_path.read_text())
        snapshot = ContextSnapshot.from_dict(data)

        context = cls(workflow_name=workflow_name, run_id=run_id)
        context.restore(snapshot)
        return context

    # ─────────────────────────────────────────────────────────────
    # STATUS MANAGEMENT
    # ─────────────────────────────────────────────────────────────

    def mark_running(self):
        """Mark workflow as running."""
        self.status = StepStatus.RUNNING

    def mark_completed(self):
        """Mark workflow as completed successfully."""
        self.status = StepStatus.SUCCESS
        self.completed_at = datetime.now()
        self.clear_checkpoint()

    def mark_failed(self, error: str):
        """Mark workflow as failed."""
        self.status = StepStatus.FAILED
        self.completed_at = datetime.now()
        self.log_error(error)

    def mark_paused(self):
        """Mark workflow as paused (for manual intervention)."""
        self.status = StepStatus.PAUSED
        self.checkpoint()

    # ─────────────────────────────────────────────────────────────
    # SERIALIZATION
    # ─────────────────────────────────────────────────────────────

    def to_dict(self) -> Dict[str, Any]:
        """Serialize context to dictionary."""
        return {
            "run_id": self.run_id,
            "workflow_name": self.workflow_name,
            "status": self.status.value,
            "started_at": self.started_at.isoformat(),
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "current_step": self.current_step,
            "variables": self.variables,
            "step_results": self.step_results,
            "token_usage": self.token_usage,
            "cost": round(self.cost, 4),
            "logs": [log.to_dict() for log in self.logs],
        }

    def to_summary(self) -> Dict[str, Any]:
        """Get a brief summary of context state."""
        return {
            "run_id": self.run_id,
            "workflow": self.workflow_name,
            "status": self.status.value,
            "steps_completed": len(self.step_results),
            "current_step": self.current_step,
            "tokens": self.token_usage,
            "cost": f"${self.cost:.4f}",
            "duration": f"{self._get_duration_seconds():.1f}s",
        }
