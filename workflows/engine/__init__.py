"""
Workflow Automation Engine

AI-nativer, deklarativer Workflow-Orchestrator für das Evolving-System.

Modules:
    parser      - YAML → WorkflowDefinition
    validator   - Schema + Logic Validation
    interpolation - {{variable}} Resolution
    context     - State Management
    executor    - Step Execution
    permissions - Tool/File Access Control
    model_selector - Dynamic Model Selection
    knowledge_connector - KB Integration
    scheduler   - Cron Jobs
    watcher     - File Watching
    events      - Event Bus
    audit       - Logging & Audit Trail
    api         - FastAPI Endpoints

Usage:
    from workflows.engine import WorkflowRunner

    runner = WorkflowRunner()
    result = await runner.run("idea-forge-full", variables={"idea_input": "..."})
"""

__version__ = "0.1.0"

# Direct imports for implemented modules
from workflows.engine.models import (
    WorkflowDefinition,
    StepDefinition,
    StepResult,
    WorkflowResult,
    PermissionsProfile,
    PreferencesProfile,
    TriggerType,
    StepStatus,
    ErrorAction,
    ModelType,
)
from workflows.engine.exceptions import (
    WorkflowError,
    WorkflowValidationError,
    WorkflowNotFoundError,
    StepExecutionError,
    PermissionDeniedError,
    BudgetExceededError,
    InterpolationError,
)
from workflows.engine.parser import (
    load_workflow,
    load_permissions,
    load_preferences,
    list_workflows,
)
from workflows.engine.interpolation import Interpolator, interpolate, evaluate_condition
from workflows.engine.context import WorkflowContext, ContextSnapshot
from workflows.engine.executor import StepExecutor, ModelSelector


# Additional imports from implemented modules
from workflows.engine.runner import WorkflowRunner, run_workflow, run_workflow_sync
from workflows.engine.permissions import PermissionEngine, PermissionGuard
from workflows.engine.knowledge_connector import KnowledgeConnector, PromptRegistry
from workflows.engine.audit import AuditLogger
from workflows.engine.triggers import TriggerManager, WorkflowDaemon, emit_event
from workflows.engine.analytics import WorkflowAnalytics, WorkflowOptimizer, DryRunner


__all__ = [
    # Models
    "WorkflowDefinition",
    "StepDefinition",
    "StepResult",
    "WorkflowResult",
    "PermissionsProfile",
    "PreferencesProfile",
    "TriggerType",
    "StepStatus",
    "ErrorAction",
    "ModelType",
    # Exceptions
    "WorkflowError",
    "WorkflowValidationError",
    "WorkflowNotFoundError",
    "StepExecutionError",
    "PermissionDeniedError",
    "BudgetExceededError",
    "InterpolationError",
    # Parser
    "load_workflow",
    "load_permissions",
    "load_preferences",
    "list_workflows",
    # Interpolation
    "Interpolator",
    "interpolate",
    "evaluate_condition",
    # Context
    "WorkflowContext",
    "ContextSnapshot",
    # Executor
    "StepExecutor",
    "ModelSelector",
    # Runner
    "WorkflowRunner",
    "run_workflow",
    "run_workflow_sync",
    # Permissions
    "PermissionEngine",
    "PermissionGuard",
    # Knowledge
    "KnowledgeConnector",
    "PromptRegistry",
    # Audit
    "AuditLogger",
    # Triggers
    "TriggerManager",
    "WorkflowDaemon",
    "emit_event",
    # Analytics
    "WorkflowAnalytics",
    "WorkflowOptimizer",
    "DryRunner",
]
