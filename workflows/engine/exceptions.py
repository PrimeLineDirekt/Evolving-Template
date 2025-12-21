"""
Workflow Engine - Custom Exceptions

All workflow-specific exceptions for clear error handling.
"""


class WorkflowError(Exception):
    """Base exception for all workflow errors."""
    pass


class WorkflowValidationError(WorkflowError):
    """Raised when workflow validation fails."""

    def __init__(self, message: str, errors: list = None):
        super().__init__(message)
        self.errors = errors or []


class WorkflowNotFoundError(WorkflowError):
    """Raised when a workflow definition is not found."""

    def __init__(self, workflow_name: str):
        super().__init__(f"Workflow not found: {workflow_name}")
        self.workflow_name = workflow_name


class StepExecutionError(WorkflowError):
    """Raised when a step fails to execute."""

    def __init__(self, step_name: str, message: str, original_error: Exception = None):
        super().__init__(f"Step '{step_name}' failed: {message}")
        self.step_name = step_name
        self.original_error = original_error


class PermissionDeniedError(WorkflowError):
    """Raised when a permission check fails."""

    def __init__(self, tool: str, reason: str):
        super().__init__(f"Permission denied for {tool}: {reason}")
        self.tool = tool
        self.reason = reason


class BudgetExceededError(WorkflowError):
    """Raised when budget limits are exceeded."""

    def __init__(self, limit_type: str, current: float, maximum: float):
        super().__init__(f"Budget exceeded: {limit_type} ({current} > {maximum})")
        self.limit_type = limit_type
        self.current = current
        self.maximum = maximum


class InterpolationError(WorkflowError):
    """Raised when variable interpolation fails."""

    def __init__(self, expression: str, reason: str):
        super().__init__(f"Failed to interpolate '{expression}': {reason}")
        self.expression = expression
        self.reason = reason


class ConditionEvaluationError(WorkflowError):
    """Raised when condition evaluation fails."""

    def __init__(self, condition: str, reason: str):
        super().__init__(f"Failed to evaluate condition '{condition}': {reason}")
        self.condition = condition
        self.reason = reason


class TimeoutError(WorkflowError):
    """Raised when a step or workflow times out."""

    def __init__(self, entity: str, timeout: str):
        super().__init__(f"{entity} timed out after {timeout}")
        self.entity = entity
        self.timeout = timeout


class ProfileNotFoundError(WorkflowError):
    """Raised when a permission or preference profile is not found."""

    def __init__(self, profile_type: str, profile_name: str):
        super().__init__(f"{profile_type} profile not found: {profile_name}")
        self.profile_type = profile_type
        self.profile_name = profile_name


class CircularDependencyError(WorkflowError):
    """Raised when circular step dependencies are detected."""

    def __init__(self, steps: list):
        super().__init__(f"Circular dependency detected: {' -> '.join(steps)}")
        self.steps = steps


class LowConfidenceError(WorkflowError):
    """Raised when step confidence is below threshold."""

    def __init__(self, step_name: str, confidence: float, threshold: float):
        super().__init__(
            f"Step '{step_name}' confidence ({confidence}%) below threshold ({threshold}%)"
        )
        self.step_name = step_name
        self.confidence = confidence
        self.threshold = threshold
