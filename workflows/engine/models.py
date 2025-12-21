"""
Workflow Engine - Data Models

Typed dataclasses for all workflow components.
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Union


# ═══════════════════════════════════════════════════════════════
# ENUMS
# ═══════════════════════════════════════════════════════════════

class TriggerType(str, Enum):
    MANUAL = "manual"
    CRON = "cron"
    WATCH = "watch"
    EVENT = "event"


class StepStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    SKIPPED = "skipped"
    PAUSED = "paused"


class ErrorAction(str, Enum):
    ABORT = "abort"
    SKIP = "skip"
    RETRY = "retry"
    PAUSE = "pause"
    CONTINUE = "continue"


class ModelType(str, Enum):
    AUTO = "auto"
    HAIKU = "haiku"
    SONNET = "sonnet"
    OPUS = "opus"


class Complexity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class LogLevel(str, Enum):
    MINIMAL = "minimal"
    STANDARD = "standard"
    VERBOSE = "verbose"


class LowConfidenceAction(str, Enum):
    RETRY = "retry"
    ABORT = "abort"
    MANUAL_REVIEW = "manual_review"


# ═══════════════════════════════════════════════════════════════
# TRIGGER CONFIG
# ═══════════════════════════════════════════════════════════════

@dataclass
class TriggerConfig:
    type: TriggerType
    cron: Optional[str] = None
    watch: Optional[str] = None
    event: Optional[str] = None


# ═══════════════════════════════════════════════════════════════
# VARIABLE CONFIG
# ═══════════════════════════════════════════════════════════════

@dataclass
class VariableConfig:
    name: str
    type: str = "string"
    default: Any = None
    prompt: Optional[str] = None
    required: bool = False


# ═══════════════════════════════════════════════════════════════
# BUDGET & AUDIT CONFIG
# ═══════════════════════════════════════════════════════════════

@dataclass
class BudgetConfig:
    max_tokens: Optional[int] = None
    max_cost: Optional[float] = None


@dataclass
class AuditConfig:
    log_level: LogLevel = LogLevel.STANDARD
    include_prompts: bool = False
    include_outputs: bool = True


@dataclass
class NotifyConfig:
    on_complete: bool = False
    on_error: bool = True
    method: str = "log"


# ═══════════════════════════════════════════════════════════════
# STEP DEFINITION
# ═══════════════════════════════════════════════════════════════

@dataclass
class BranchCondition:
    condition: str
    steps: List['StepDefinition'] = field(default_factory=list)


@dataclass
class StepDefinition:
    name: str
    description: Optional[str] = None

    # Execution type (one of)
    command: Optional[str] = None
    prompt: Optional[str] = None
    bash: Optional[str] = None
    agent: Optional[str] = None
    framework: Optional[str] = None
    script: Optional[str] = None

    # Framework-specific
    mode: Optional[str] = None
    config: Optional[Dict[str, Any]] = None

    # Flow control
    condition: Optional[str] = None
    loop: Optional[str] = None
    loop_as: Optional[str] = None
    parallel: bool = False
    depends_on: Optional[str] = None

    # Branching
    branch: Optional[List[BranchCondition]] = None

    # Output
    store_as: Optional[str] = None
    output: Optional[str] = None
    template: Optional[str] = None

    # Quality control
    confidence_gate: Optional[float] = None
    on_low_confidence: LowConfidenceAction = LowConfidenceAction.MANUAL_REVIEW

    # Model selection
    model: ModelType = ModelType.AUTO
    complexity: Optional[Complexity] = None

    # Error handling
    on_error: ErrorAction = ErrorAction.ABORT
    retry_count: int = 0
    retry_delay: Optional[str] = None
    timeout: Optional[str] = None

    def get_execution_type(self) -> str:
        """Return the type of execution for this step."""
        if self.command:
            return "command"
        elif self.prompt:
            return "prompt"
        elif self.bash:
            return "bash"
        elif self.agent:
            return "agent"
        elif self.framework:
            return "framework"
        elif self.script:
            return "script"
        elif self.branch:
            return "branch"
        elif self.output and self.template:
            return "output"
        return "unknown"


# ═══════════════════════════════════════════════════════════════
# WORKFLOW DEFINITION
# ═══════════════════════════════════════════════════════════════

@dataclass
class WorkflowSettings:
    on_error: ErrorAction = ErrorAction.ABORT
    max_steps: int = 50
    timeout: str = "30m"
    dry_run: bool = False


@dataclass
class WorkflowDefinition:
    name: str
    description: str = ""
    version: str = "1.0"

    trigger: TriggerConfig = field(default_factory=lambda: TriggerConfig(type=TriggerType.MANUAL))

    permissions_profile: str = "default"
    preferences_profile: str = "default"

    variables: List[VariableConfig] = field(default_factory=list)
    steps: List[StepDefinition] = field(default_factory=list)

    settings: WorkflowSettings = field(default_factory=WorkflowSettings)
    budget: Optional[BudgetConfig] = None
    audit: AuditConfig = field(default_factory=AuditConfig)
    notify: NotifyConfig = field(default_factory=NotifyConfig)

    # Metadata
    source_path: Optional[Path] = None


# ═══════════════════════════════════════════════════════════════
# STEP RESULT
# ═══════════════════════════════════════════════════════════════

@dataclass
class StepResult:
    status: StepStatus
    data: Any = None
    confidence: Optional[float] = None
    error: Optional[str] = None
    tokens_used: int = 0
    duration_ms: int = 0
    model_used: Optional[str] = None

    @property
    def success(self) -> bool:
        return self.status == StepStatus.SUCCESS


# ═══════════════════════════════════════════════════════════════
# WORKFLOW RESULT
# ═══════════════════════════════════════════════════════════════

@dataclass
class WorkflowResult:
    workflow_name: str
    run_id: str
    status: StepStatus
    started_at: datetime
    completed_at: Optional[datetime] = None

    step_results: Dict[str, StepResult] = field(default_factory=dict)
    variables: Dict[str, Any] = field(default_factory=dict)

    total_tokens: int = 0
    total_cost: float = 0.0

    error: Optional[str] = None

    @property
    def duration_seconds(self) -> float:
        if self.completed_at:
            return (self.completed_at - self.started_at).total_seconds()
        return 0.0

    @property
    def success(self) -> bool:
        return self.status == StepStatus.SUCCESS


# ═══════════════════════════════════════════════════════════════
# PERMISSION MODELS
# ═══════════════════════════════════════════════════════════════

@dataclass
class ToolConstraint:
    tool: str
    paths: Optional[List[str]] = None
    commands: Optional[List[str]] = None
    patterns: Optional[List[str]] = None


@dataclass
class ResourceLimits:
    max_file_size: str = "10MB"
    max_files_per_step: int = 20
    max_tokens_per_step: int = 50000
    max_api_calls: int = 100


@dataclass
class PermissionsProfile:
    name: str
    description: str = ""
    inherits: Optional[str] = None

    always_allow: List[str] = field(default_factory=list)
    allow_with_constraints: List[ToolConstraint] = field(default_factory=list)
    ask_once: List[str] = field(default_factory=list)
    never_allow: List[ToolConstraint] = field(default_factory=list)

    readable_paths: Union[str, List[str]] = "**/*"
    writable_paths: List[str] = field(default_factory=list)
    protected_paths: List[str] = field(default_factory=list)

    resource_limits: ResourceLimits = field(default_factory=ResourceLimits)

    allowed_commands: List[str] = field(default_factory=list)
    denied_commands: List[str] = field(default_factory=list)

    allowed_env_vars: List[str] = field(default_factory=list)
    never_log_patterns: List[str] = field(default_factory=list)


# ═══════════════════════════════════════════════════════════════
# PREFERENCES MODELS
# ═══════════════════════════════════════════════════════════════

@dataclass
class DecisionMaking:
    when_multiple_approaches: str = "prefer_simpler"
    when_uncertain: str = "batch_questions"
    when_error: str = "fix_and_continue"
    risk_tolerance: str = "medium"


@dataclass
class CodingPrefs:
    languages: List[str] = field(default_factory=list)
    style: str = "functional"
    comments: str = "minimal"


@dataclass
class CommunicationPrefs:
    language: str = "German"
    verbosity: str = "concise"
    format: str = "markdown"
    emojis: bool = False


@dataclass
class DomainPrefs:
    focus_areas: List[str] = field(default_factory=list)
    tech_stack: List[str] = field(default_factory=list)
    avoid: List[str] = field(default_factory=list)


@dataclass
class AutomationPrefs:
    auto_commit: bool = False
    auto_fix_lint: bool = True
    auto_update_docs: bool = True
    batch_similar_tasks: bool = True


@dataclass
class ModelPrefs:
    default: str = "sonnet"
    complex_reasoning: str = "opus"
    simple_tasks: str = "haiku"
    cost_sensitivity: str = "medium"


@dataclass
class PreferencesProfile:
    name: str
    description: str = ""

    decision_making: DecisionMaking = field(default_factory=DecisionMaking)
    coding: CodingPrefs = field(default_factory=CodingPrefs)
    communication: CommunicationPrefs = field(default_factory=CommunicationPrefs)
    domain: DomainPrefs = field(default_factory=DomainPrefs)
    automation: AutomationPrefs = field(default_factory=AutomationPrefs)
    model_preferences: ModelPrefs = field(default_factory=ModelPrefs)
