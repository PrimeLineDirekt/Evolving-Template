"""
Workflow Engine - Audit Logger

Immutable audit trail for workflow executions.
"""

import hashlib
import json
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional


# ═══════════════════════════════════════════════════════════════
# AUDIT ENTRY TYPES
# ═══════════════════════════════════════════════════════════════

class AuditEventType(str, Enum):
    # Workflow lifecycle
    WORKFLOW_START = "workflow_start"
    WORKFLOW_COMPLETE = "workflow_complete"
    WORKFLOW_FAILED = "workflow_failed"
    WORKFLOW_PAUSED = "workflow_paused"
    WORKFLOW_RESUMED = "workflow_resumed"

    # Step lifecycle
    STEP_START = "step_start"
    STEP_COMPLETE = "step_complete"
    STEP_FAILED = "step_failed"
    STEP_SKIPPED = "step_skipped"

    # Tool usage
    TOOL_CALL = "tool_call"
    TOOL_RESULT = "tool_result"

    # Permission events
    PERMISSION_CHECK = "permission_check"
    PERMISSION_DENIED = "permission_denied"
    PERMISSION_GRANTED = "permission_granted"

    # Budget events
    BUDGET_UPDATE = "budget_update"
    BUDGET_WARNING = "budget_warning"
    BUDGET_EXCEEDED = "budget_exceeded"

    # Checkpoint events
    CHECKPOINT_CREATED = "checkpoint_created"
    CHECKPOINT_RESTORED = "checkpoint_restored"

    # Error events
    ERROR = "error"
    WARNING = "warning"


@dataclass
class AuditEntry:
    """A single audit log entry."""
    timestamp: str
    event_type: AuditEventType
    workflow_name: str
    run_id: str
    step_name: Optional[str]
    message: str
    data: Optional[Dict[str, Any]]
    previous_hash: Optional[str]
    entry_hash: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "timestamp": self.timestamp,
            "event_type": self.event_type.value,
            "workflow_name": self.workflow_name,
            "run_id": self.run_id,
            "step_name": self.step_name,
            "message": self.message,
            "data": self.data,
            "previous_hash": self.previous_hash,
            "entry_hash": self.entry_hash,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'AuditEntry':
        return cls(
            timestamp=data["timestamp"],
            event_type=AuditEventType(data["event_type"]),
            workflow_name=data["workflow_name"],
            run_id=data["run_id"],
            step_name=data.get("step_name"),
            message=data["message"],
            data=data.get("data"),
            previous_hash=data.get("previous_hash"),
            entry_hash=data["entry_hash"],
        )


@dataclass
class AuditSummary:
    """Summary of audit log."""
    workflow_name: str
    run_id: str
    started_at: str
    completed_at: Optional[str]
    status: str
    total_entries: int
    steps_started: int
    steps_completed: int
    steps_failed: int
    steps_skipped: int
    tool_calls: int
    permission_denials: int
    errors: int
    warnings: int
    tokens_used: int
    cost: float
    duration_seconds: float
    integrity_valid: bool


# ═══════════════════════════════════════════════════════════════
# AUDIT LOGGER
# ═══════════════════════════════════════════════════════════════

class AuditLogger:
    """
    Immutable audit logger for workflow executions.

    Features:
    - Hash-chained entries for tamper detection
    - Structured logging with typed events
    - Secret redaction
    - Summary generation
    - Log rotation support
    """

    def __init__(
        self,
        workflow_name: str,
        run_id: str,
        logs_dir: Optional[Path] = None,
        include_prompts: bool = False,
        include_outputs: bool = True,
        redact_patterns: Optional[List[str]] = None,
    ):
        self.workflow_name = workflow_name
        self.run_id = run_id
        self.logs_dir = logs_dir or Path("workflows/logs")
        self.include_prompts = include_prompts
        self.include_outputs = include_outputs
        self.redact_patterns = redact_patterns or ["*_KEY", "*_SECRET", "*_TOKEN", "*PASSWORD*"]

        self.entries: List[AuditEntry] = []
        self._last_hash: Optional[str] = None
        self._started_at: Optional[str] = None

        # Ensure logs directory exists
        self.logs_dir.mkdir(parents=True, exist_ok=True)

    @property
    def log_path(self) -> Path:
        """Get path to log file."""
        return self.logs_dir / f"{self.workflow_name}-{self.run_id}.audit.json"

    # ─────────────────────────────────────────────────────────────
    # WORKFLOW EVENTS
    # ─────────────────────────────────────────────────────────────

    def log_start(self, workflow_data: Optional[Dict[str, Any]] = None):
        """Log workflow start."""
        self._started_at = datetime.now().isoformat()
        self._log(
            AuditEventType.WORKFLOW_START,
            "Workflow execution started",
            data=workflow_data,
        )

    def log_complete(self, result_data: Optional[Dict[str, Any]] = None):
        """Log successful workflow completion."""
        self._log(
            AuditEventType.WORKFLOW_COMPLETE,
            "Workflow completed successfully",
            data=self._filter_output(result_data),
        )
        self._write()

    def log_failed(self, error: str, error_data: Optional[Dict[str, Any]] = None):
        """Log workflow failure."""
        self._log(
            AuditEventType.WORKFLOW_FAILED,
            f"Workflow failed: {error}",
            data=error_data,
        )
        self._write()

    def log_paused(self, reason: str):
        """Log workflow paused."""
        self._log(
            AuditEventType.WORKFLOW_PAUSED,
            f"Workflow paused: {reason}",
        )
        self._write()

    def log_resumed(self, checkpoint_data: Optional[Dict[str, Any]] = None):
        """Log workflow resumed from checkpoint."""
        self._log(
            AuditEventType.WORKFLOW_RESUMED,
            "Workflow resumed from checkpoint",
            data=checkpoint_data,
        )

    # ─────────────────────────────────────────────────────────────
    # STEP EVENTS
    # ─────────────────────────────────────────────────────────────

    def log_step_start(self, step_name: str, step_data: Optional[Dict[str, Any]] = None):
        """Log step start."""
        data = step_data
        if data and not self.include_prompts and "prompt" in data:
            data = {k: v for k, v in data.items() if k != "prompt"}

        self._log(
            AuditEventType.STEP_START,
            f"Starting step: {step_name}",
            step_name=step_name,
            data=data,
        )

    def log_step_complete(
        self,
        step_name: str,
        result_data: Optional[Dict[str, Any]] = None,
        tokens: int = 0,
        duration_ms: int = 0,
    ):
        """Log step completion."""
        data = {
            "tokens": tokens,
            "duration_ms": duration_ms,
        }
        if self.include_outputs and result_data:
            data["result"] = self._filter_output(result_data)

        self._log(
            AuditEventType.STEP_COMPLETE,
            f"Step completed: {step_name}",
            step_name=step_name,
            data=data,
        )

    def log_step_failed(
        self,
        step_name: str,
        error: str,
        error_data: Optional[Dict[str, Any]] = None,
    ):
        """Log step failure."""
        self._log(
            AuditEventType.STEP_FAILED,
            f"Step failed: {step_name} - {error}",
            step_name=step_name,
            data=error_data,
        )

    def log_step_skipped(self, step_name: str, reason: str):
        """Log step skipped."""
        self._log(
            AuditEventType.STEP_SKIPPED,
            f"Step skipped: {step_name} - {reason}",
            step_name=step_name,
        )

    # ─────────────────────────────────────────────────────────────
    # TOOL EVENTS
    # ─────────────────────────────────────────────────────────────

    def log_tool_call(
        self,
        tool: str,
        params: Dict[str, Any],
        step_name: Optional[str] = None,
    ):
        """Log a tool call."""
        self._log(
            AuditEventType.TOOL_CALL,
            f"Tool call: {tool}",
            step_name=step_name,
            data={"tool": tool, "params": self._redact_secrets(params)},
        )

    def log_tool_result(
        self,
        tool: str,
        success: bool,
        result: Any = None,
        step_name: Optional[str] = None,
    ):
        """Log tool result."""
        data = {"tool": tool, "success": success}
        if self.include_outputs and result is not None:
            data["result"] = self._filter_output(result)

        self._log(
            AuditEventType.TOOL_RESULT,
            f"Tool result: {tool} - {'success' if success else 'failed'}",
            step_name=step_name,
            data=data,
        )

    # ─────────────────────────────────────────────────────────────
    # PERMISSION EVENTS
    # ─────────────────────────────────────────────────────────────

    def log_permission_check(
        self,
        tool: str,
        decision: str,
        reason: str,
        step_name: Optional[str] = None,
    ):
        """Log a permission check."""
        event_type = {
            "allow": AuditEventType.PERMISSION_GRANTED,
            "deny": AuditEventType.PERMISSION_DENIED,
        }.get(decision.lower(), AuditEventType.PERMISSION_CHECK)

        self._log(
            event_type,
            f"Permission {decision}: {tool} - {reason}",
            step_name=step_name,
            data={"tool": tool, "decision": decision, "reason": reason},
        )

    # ─────────────────────────────────────────────────────────────
    # BUDGET EVENTS
    # ─────────────────────────────────────────────────────────────

    def log_budget_update(
        self,
        tokens: int,
        cost: float,
        step_name: Optional[str] = None,
    ):
        """Log budget update."""
        self._log(
            AuditEventType.BUDGET_UPDATE,
            f"Budget update: {tokens} tokens, ${cost:.4f}",
            step_name=step_name,
            data={"tokens": tokens, "cost": cost},
        )

    def log_budget_warning(
        self,
        limit_type: str,
        current: float,
        limit: float,
        step_name: Optional[str] = None,
    ):
        """Log budget warning (approaching limit)."""
        self._log(
            AuditEventType.BUDGET_WARNING,
            f"Budget warning: {limit_type} at {current}/{limit}",
            step_name=step_name,
            data={"limit_type": limit_type, "current": current, "limit": limit},
        )

    def log_budget_exceeded(
        self,
        limit_type: str,
        current: float,
        limit: float,
        step_name: Optional[str] = None,
    ):
        """Log budget exceeded."""
        self._log(
            AuditEventType.BUDGET_EXCEEDED,
            f"Budget exceeded: {limit_type} ({current} > {limit})",
            step_name=step_name,
            data={"limit_type": limit_type, "current": current, "limit": limit},
        )

    # ─────────────────────────────────────────────────────────────
    # CHECKPOINT EVENTS
    # ─────────────────────────────────────────────────────────────

    def log_checkpoint_created(self, step_index: int, step_name: Optional[str] = None):
        """Log checkpoint creation."""
        self._log(
            AuditEventType.CHECKPOINT_CREATED,
            f"Checkpoint created at step {step_index}",
            step_name=step_name,
            data={"step_index": step_index},
        )

    def log_checkpoint_restored(self, step_index: int):
        """Log checkpoint restoration."""
        self._log(
            AuditEventType.CHECKPOINT_RESTORED,
            f"Restored from checkpoint at step {step_index}",
            data={"step_index": step_index},
        )

    # ─────────────────────────────────────────────────────────────
    # ERROR EVENTS
    # ─────────────────────────────────────────────────────────────

    def log_error(
        self,
        message: str,
        error_data: Optional[Dict[str, Any]] = None,
        step_name: Optional[str] = None,
    ):
        """Log an error."""
        self._log(
            AuditEventType.ERROR,
            message,
            step_name=step_name,
            data=error_data,
        )

    def log_warning(
        self,
        message: str,
        warning_data: Optional[Dict[str, Any]] = None,
        step_name: Optional[str] = None,
    ):
        """Log a warning."""
        self._log(
            AuditEventType.WARNING,
            message,
            step_name=step_name,
            data=warning_data,
        )

    # ─────────────────────────────────────────────────────────────
    # INTERNAL METHODS
    # ─────────────────────────────────────────────────────────────

    def _log(
        self,
        event_type: AuditEventType,
        message: str,
        step_name: Optional[str] = None,
        data: Optional[Dict[str, Any]] = None,
    ):
        """Create and store an audit entry."""
        timestamp = datetime.now().isoformat()

        # Calculate entry hash for integrity chain
        entry_content = json.dumps({
            "timestamp": timestamp,
            "event_type": event_type.value,
            "message": message,
            "data": data,
            "previous_hash": self._last_hash,
        }, sort_keys=True)

        entry_hash = hashlib.sha256(entry_content.encode()).hexdigest()[:16]

        entry = AuditEntry(
            timestamp=timestamp,
            event_type=event_type,
            workflow_name=self.workflow_name,
            run_id=self.run_id,
            step_name=step_name,
            message=message,
            data=data,
            previous_hash=self._last_hash,
            entry_hash=entry_hash,
        )

        self.entries.append(entry)
        self._last_hash = entry_hash

    def _write(self):
        """Write audit log to file."""
        log_data = {
            "workflow_name": self.workflow_name,
            "run_id": self.run_id,
            "entries": [e.to_dict() for e in self.entries],
            "final_hash": self._last_hash,
        }

        self.log_path.write_text(
            json.dumps(log_data, indent=2, ensure_ascii=False)
        )

    def _redact_secrets(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Redact sensitive data."""
        import fnmatch

        redacted = {}
        for key, value in data.items():
            should_redact = any(
                fnmatch.fnmatch(key.upper(), pattern.upper())
                for pattern in self.redact_patterns
            )

            if should_redact:
                redacted[key] = "[REDACTED]"
            elif isinstance(value, dict):
                redacted[key] = self._redact_secrets(value)
            else:
                redacted[key] = value

        return redacted

    def _filter_output(self, data: Any) -> Any:
        """Filter output data based on settings."""
        if data is None:
            return None

        if isinstance(data, dict):
            return self._redact_secrets(data)

        if isinstance(data, str) and len(data) > 10000:
            return data[:10000] + "... [truncated]"

        return data

    # ─────────────────────────────────────────────────────────────
    # SUMMARY & VERIFICATION
    # ─────────────────────────────────────────────────────────────

    def get_summary(self) -> AuditSummary:
        """Get audit log summary."""
        # Count events
        steps_started = sum(1 for e in self.entries if e.event_type == AuditEventType.STEP_START)
        steps_completed = sum(1 for e in self.entries if e.event_type == AuditEventType.STEP_COMPLETE)
        steps_failed = sum(1 for e in self.entries if e.event_type == AuditEventType.STEP_FAILED)
        steps_skipped = sum(1 for e in self.entries if e.event_type == AuditEventType.STEP_SKIPPED)
        tool_calls = sum(1 for e in self.entries if e.event_type == AuditEventType.TOOL_CALL)
        permission_denials = sum(1 for e in self.entries if e.event_type == AuditEventType.PERMISSION_DENIED)
        errors = sum(1 for e in self.entries if e.event_type == AuditEventType.ERROR)
        warnings = sum(1 for e in self.entries if e.event_type == AuditEventType.WARNING)

        # Calculate totals from budget updates
        tokens_used = 0
        cost = 0.0
        for entry in self.entries:
            if entry.event_type == AuditEventType.BUDGET_UPDATE and entry.data:
                tokens_used = entry.data.get("tokens", tokens_used)
                cost = entry.data.get("cost", cost)

        # Get status
        status = "running"
        completed_at = None
        for entry in reversed(self.entries):
            if entry.event_type == AuditEventType.WORKFLOW_COMPLETE:
                status = "success"
                completed_at = entry.timestamp
                break
            elif entry.event_type == AuditEventType.WORKFLOW_FAILED:
                status = "failed"
                completed_at = entry.timestamp
                break
            elif entry.event_type == AuditEventType.WORKFLOW_PAUSED:
                status = "paused"
                break

        # Calculate duration
        duration = 0.0
        if self._started_at and completed_at:
            start = datetime.fromisoformat(self._started_at)
            end = datetime.fromisoformat(completed_at)
            duration = (end - start).total_seconds()

        return AuditSummary(
            workflow_name=self.workflow_name,
            run_id=self.run_id,
            started_at=self._started_at or "",
            completed_at=completed_at,
            status=status,
            total_entries=len(self.entries),
            steps_started=steps_started,
            steps_completed=steps_completed,
            steps_failed=steps_failed,
            steps_skipped=steps_skipped,
            tool_calls=tool_calls,
            permission_denials=permission_denials,
            errors=errors,
            warnings=warnings,
            tokens_used=tokens_used,
            cost=cost,
            duration_seconds=duration,
            integrity_valid=self.verify_integrity(),
        )

    def verify_integrity(self) -> bool:
        """Verify the integrity of the audit chain."""
        if not self.entries:
            return True

        previous_hash = None
        for entry in self.entries:
            if entry.previous_hash != previous_hash:
                return False

            # Recalculate hash
            entry_content = json.dumps({
                "timestamp": entry.timestamp,
                "event_type": entry.event_type.value,
                "message": entry.message,
                "data": entry.data,
                "previous_hash": entry.previous_hash,
            }, sort_keys=True)

            expected_hash = hashlib.sha256(entry_content.encode()).hexdigest()[:16]

            if entry.entry_hash != expected_hash:
                return False

            previous_hash = entry.entry_hash

        return True

    @classmethod
    def load(cls, log_path: Path) -> 'AuditLogger':
        """Load audit log from file."""
        data = json.loads(log_path.read_text())

        logger = cls(
            workflow_name=data["workflow_name"],
            run_id=data["run_id"],
        )

        logger.entries = [AuditEntry.from_dict(e) for e in data["entries"]]
        if logger.entries:
            logger._last_hash = logger.entries[-1].entry_hash
            logger._started_at = logger.entries[0].timestamp

        return logger
