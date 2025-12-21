"""
Workflow Engine - Permission Engine

Controls tool usage, file access, and resource limits during workflow execution.
"""

import fnmatch
import re
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

from workflows.engine.models import PermissionsProfile, ToolConstraint, ResourceLimits
from workflows.engine.parser import load_permissions
from workflows.engine.exceptions import PermissionDeniedError


# ═══════════════════════════════════════════════════════════════
# PERMISSION RESULT
# ═══════════════════════════════════════════════════════════════

class PermissionDecision(str, Enum):
    ALLOW = "allow"
    DENY = "deny"
    ASK = "ask"
    CONSTRAINED = "constrained"


@dataclass
class PermissionResult:
    """Result of a permission check."""
    decision: PermissionDecision
    reason: str
    constraints: Optional[Dict[str, Any]] = None

    @property
    def allowed(self) -> bool:
        return self.decision in (PermissionDecision.ALLOW, PermissionDecision.CONSTRAINED)

    @property
    def needs_confirmation(self) -> bool:
        return self.decision == PermissionDecision.ASK


@dataclass
class BudgetUsage:
    """Current budget usage."""
    tokens: int = 0
    cost: float = 0.0
    api_calls: int = 0
    files_modified: int = 0


# ═══════════════════════════════════════════════════════════════
# PERMISSION ENGINE
# ═══════════════════════════════════════════════════════════════

class PermissionEngine:
    """
    Enforces permissions during workflow execution.

    Features:
    - Tool access control (always_allow, ask_once, never_allow)
    - File path restrictions (readable, writable, protected)
    - Command filtering (allowed, denied patterns)
    - Resource limits (tokens, cost, files, API calls)
    - Secret protection (never log patterns)
    """

    def __init__(self, profile: Optional[PermissionsProfile] = None, profile_name: str = "default"):
        if profile:
            self.profile = profile
        else:
            self.profile = load_permissions(profile_name)

        # Track tools that have been asked and approved
        self._asked_tools: Set[str] = set()

        # Track current usage for limit checking
        self._usage = BudgetUsage()

    # ─────────────────────────────────────────────────────────────
    # TOOL ACCESS CONTROL
    # ─────────────────────────────────────────────────────────────

    def check_tool(self, tool: str, **params) -> PermissionResult:
        """
        Check if a tool call is permitted.

        Args:
            tool: Tool name (e.g., "Read", "Write", "Bash")
            **params: Tool parameters (e.g., path, command)

        Returns:
            PermissionResult with decision and reason
        """
        # Check never_allow first
        for constraint in self.profile.never_allow:
            if self._matches_constraint(tool, constraint, **params):
                return PermissionResult(
                    decision=PermissionDecision.DENY,
                    reason=f"Tool '{tool}' is in never_allow list"
                )

        # Check always_allow
        if tool in self.profile.always_allow:
            return PermissionResult(
                decision=PermissionDecision.ALLOW,
                reason="Tool is always allowed"
            )

        # Check allow_with_constraints
        for constraint in self.profile.allow_with_constraints:
            if constraint.tool == tool:
                if self._check_constraints(constraint, **params):
                    return PermissionResult(
                        decision=PermissionDecision.CONSTRAINED,
                        reason="Tool allowed within constraints",
                        constraints={
                            "paths": constraint.paths,
                            "commands": constraint.commands,
                            "patterns": constraint.patterns,
                        }
                    )
                else:
                    return PermissionResult(
                        decision=PermissionDecision.DENY,
                        reason=f"Tool '{tool}' violates constraints"
                    )

        # Check ask_once
        if tool in self.profile.ask_once:
            if tool in self._asked_tools:
                return PermissionResult(
                    decision=PermissionDecision.ALLOW,
                    reason="Tool was previously approved"
                )
            return PermissionResult(
                decision=PermissionDecision.ASK,
                reason="Tool requires one-time approval"
            )

        # Default deny
        return PermissionResult(
            decision=PermissionDecision.DENY,
            reason=f"Tool '{tool}' is not in allowed list"
        )

    def approve_tool(self, tool: str):
        """Mark a tool as approved (for ask_once tools)."""
        self._asked_tools.add(tool)

    def _matches_constraint(
        self,
        tool: str,
        constraint: ToolConstraint,
        **params
    ) -> bool:
        """Check if tool call matches a constraint."""
        if constraint.tool != tool:
            return False

        # Check patterns
        if constraint.patterns:
            text = str(params)
            for pattern in constraint.patterns:
                if re.search(pattern, text, re.IGNORECASE):
                    return True

        return True

    def _check_constraints(
        self,
        constraint: ToolConstraint,
        **params
    ) -> bool:
        """Check if params satisfy constraint requirements."""
        # Check path constraints
        if constraint.paths and "path" in params:
            path = params["path"]
            if not any(fnmatch.fnmatch(path, p) for p in constraint.paths):
                return False

        # Check command constraints
        if constraint.commands and "command" in params:
            command = params["command"]
            if not any(cmd in command for cmd in constraint.commands):
                return False

        return True

    # ─────────────────────────────────────────────────────────────
    # FILE ACCESS CONTROL
    # ─────────────────────────────────────────────────────────────

    def check_file_read(self, path: str) -> PermissionResult:
        """Check if a file can be read."""
        # Check protected paths
        for protected in self.profile.protected_paths:
            if fnmatch.fnmatch(path, protected):
                return PermissionResult(
                    decision=PermissionDecision.DENY,
                    reason=f"Path matches protected pattern: {protected}"
                )

        # Check readable paths
        readable = self.profile.readable_paths
        if isinstance(readable, str):
            readable = [readable]

        for pattern in readable:
            if fnmatch.fnmatch(path, pattern):
                return PermissionResult(
                    decision=PermissionDecision.ALLOW,
                    reason="Path is readable"
                )

        return PermissionResult(
            decision=PermissionDecision.DENY,
            reason="Path is not in readable patterns"
        )

    def check_file_write(self, path: str) -> PermissionResult:
        """Check if a file can be written."""
        # Check protected paths first
        for protected in self.profile.protected_paths:
            if fnmatch.fnmatch(path, protected):
                return PermissionResult(
                    decision=PermissionDecision.DENY,
                    reason=f"Path matches protected pattern: {protected}"
                )

        # Check writable paths
        for pattern in self.profile.writable_paths:
            if fnmatch.fnmatch(path, pattern):
                return PermissionResult(
                    decision=PermissionDecision.ALLOW,
                    reason="Path is writable"
                )

        return PermissionResult(
            decision=PermissionDecision.DENY,
            reason="Path is not in writable patterns"
        )

    # ─────────────────────────────────────────────────────────────
    # COMMAND ACCESS CONTROL
    # ─────────────────────────────────────────────────────────────

    def check_command(self, command: str) -> PermissionResult:
        """Check if a bash command is permitted."""
        # Check denied patterns first
        for denied in self.profile.denied_commands:
            if re.search(denied, command, re.IGNORECASE):
                return PermissionResult(
                    decision=PermissionDecision.DENY,
                    reason=f"Command matches denied pattern: {denied}"
                )

        # Check allowed patterns
        for allowed in self.profile.allowed_commands:
            if re.search(allowed, command, re.IGNORECASE):
                return PermissionResult(
                    decision=PermissionDecision.ALLOW,
                    reason="Command matches allowed pattern"
                )

        # If allowed_commands is empty, allow all (except denied)
        if not self.profile.allowed_commands:
            return PermissionResult(
                decision=PermissionDecision.ALLOW,
                reason="No command restrictions"
            )

        return PermissionResult(
            decision=PermissionDecision.DENY,
            reason="Command not in allowed patterns"
        )

    # ─────────────────────────────────────────────────────────────
    # RESOURCE LIMITS
    # ─────────────────────────────────────────────────────────────

    def check_resource_limits(self, usage: BudgetUsage) -> PermissionResult:
        """Check if resource usage is within limits."""
        limits = self.profile.resource_limits

        if usage.tokens > limits.max_tokens_per_step:
            return PermissionResult(
                decision=PermissionDecision.DENY,
                reason=f"Token limit exceeded: {usage.tokens} > {limits.max_tokens_per_step}"
            )

        if usage.files_modified > limits.max_files_per_step:
            return PermissionResult(
                decision=PermissionDecision.DENY,
                reason=f"File limit exceeded: {usage.files_modified} > {limits.max_files_per_step}"
            )

        if usage.api_calls > limits.max_api_calls:
            return PermissionResult(
                decision=PermissionDecision.DENY,
                reason=f"API call limit exceeded: {usage.api_calls} > {limits.max_api_calls}"
            )

        return PermissionResult(
            decision=PermissionDecision.ALLOW,
            reason="Within resource limits"
        )

    def update_usage(
        self,
        tokens: int = 0,
        cost: float = 0.0,
        api_calls: int = 0,
        files_modified: int = 0
    ):
        """Update current usage tracking."""
        self._usage.tokens += tokens
        self._usage.cost += cost
        self._usage.api_calls += api_calls
        self._usage.files_modified += files_modified

    def get_usage(self) -> BudgetUsage:
        """Get current usage."""
        return self._usage

    def reset_step_usage(self):
        """Reset per-step usage counters."""
        self._usage = BudgetUsage()

    # ─────────────────────────────────────────────────────────────
    # SECRET PROTECTION
    # ─────────────────────────────────────────────────────────────

    def should_redact(self, key: str) -> bool:
        """Check if a key should be redacted in logs."""
        for pattern in self.profile.never_log_patterns:
            if fnmatch.fnmatch(key, pattern):
                return True
        return False

    def redact_secrets(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Redact sensitive data from a dictionary."""
        redacted = {}
        for key, value in data.items():
            if self.should_redact(key):
                redacted[key] = "[REDACTED]"
            elif isinstance(value, dict):
                redacted[key] = self.redact_secrets(value)
            else:
                redacted[key] = value
        return redacted

    def is_env_var_allowed(self, var: str) -> bool:
        """Check if an environment variable access is allowed."""
        return var in self.profile.allowed_env_vars

    # ─────────────────────────────────────────────────────────────
    # SDK INTEGRATION
    # ─────────────────────────────────────────────────────────────

    def get_allowed_tools(self) -> List[str]:
        """Get list of allowed tools for SDK QueryOptions."""
        tools = list(self.profile.always_allow)

        # Add constrained tools
        for constraint in self.profile.allow_with_constraints:
            if constraint.tool not in tools:
                tools.append(constraint.tool)

        # Add approved ask_once tools
        for tool in self._asked_tools:
            if tool not in tools:
                tools.append(tool)

        return tools

    def get_blocked_tools(self) -> List[str]:
        """Get list of blocked tools."""
        return [c.tool for c in self.profile.never_allow]


# ═══════════════════════════════════════════════════════════════
# PERMISSION GUARD (Decorator)
# ═══════════════════════════════════════════════════════════════

class PermissionGuard:
    """
    Context manager and decorator for permission-checked operations.

    Usage:
        engine = PermissionEngine(profile)

        with PermissionGuard(engine, "Write", path="ideas/new.md"):
            # Write operation here
            pass

        @PermissionGuard.require(engine, "Bash")
        async def run_command(command):
            pass
    """

    def __init__(self, engine: PermissionEngine, tool: str, **params):
        self.engine = engine
        self.tool = tool
        self.params = params

    def __enter__(self):
        result = self.engine.check_tool(self.tool, **self.params)
        if not result.allowed:
            raise PermissionDeniedError(self.tool, result.reason)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return False

    @staticmethod
    def require(engine: PermissionEngine, tool: str):
        """Decorator factory for permission-required functions."""
        def decorator(func):
            async def wrapper(*args, **kwargs):
                result = engine.check_tool(tool, **kwargs)
                if not result.allowed:
                    raise PermissionDeniedError(tool, result.reason)
                return await func(*args, **kwargs)
            return wrapper
        return decorator


# ═══════════════════════════════════════════════════════════════
# FILE SIZE CHECKER
# ═══════════════════════════════════════════════════════════════

def parse_size(size_str: str) -> int:
    """Parse size string to bytes."""
    size_str = size_str.upper().strip()

    multipliers = {
        "B": 1,
        "KB": 1024,
        "MB": 1024 * 1024,
        "GB": 1024 * 1024 * 1024,
    }

    for suffix, mult in multipliers.items():
        if size_str.endswith(suffix):
            number = float(size_str[:-len(suffix)].strip())
            return int(number * mult)

    return int(size_str)


def check_file_size(path: Path, max_size: str) -> PermissionResult:
    """Check if file size is within limit."""
    if not path.exists():
        return PermissionResult(
            decision=PermissionDecision.ALLOW,
            reason="File does not exist yet"
        )

    file_size = path.stat().st_size
    max_bytes = parse_size(max_size)

    if file_size > max_bytes:
        return PermissionResult(
            decision=PermissionDecision.DENY,
            reason=f"File size {file_size} exceeds limit {max_size}"
        )

    return PermissionResult(
        decision=PermissionDecision.ALLOW,
        reason="File size within limit"
    )
