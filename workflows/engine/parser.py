"""
Workflow Engine - YAML Parser

Loads YAML workflow definitions and converts them to typed objects.
"""

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml

try:
    import jsonschema
    HAS_JSONSCHEMA = True
except ImportError:
    HAS_JSONSCHEMA = False

from workflows.engine.models import (
    AuditConfig,
    BranchCondition,
    BudgetConfig,
    Complexity,
    DecisionMaking,
    CodingPrefs,
    CommunicationPrefs,
    DomainPrefs,
    AutomationPrefs,
    ModelPrefs,
    ErrorAction,
    LogLevel,
    LowConfidenceAction,
    ModelType,
    NotifyConfig,
    PermissionsProfile,
    PreferencesProfile,
    ResourceLimits,
    StepDefinition,
    ToolConstraint,
    TriggerConfig,
    TriggerType,
    VariableConfig,
    WorkflowDefinition,
    WorkflowSettings,
)
from workflows.engine.exceptions import (
    WorkflowNotFoundError,
    WorkflowValidationError,
    ProfileNotFoundError,
)


# ═══════════════════════════════════════════════════════════════
# PATH CONFIGURATION
# ═══════════════════════════════════════════════════════════════

def get_workflows_root() -> Path:
    """Get the root workflows directory."""
    return Path(__file__).parent.parent


def get_definitions_path() -> Path:
    """Get the workflow definitions directory."""
    return get_workflows_root() / "definitions"


def get_permissions_path() -> Path:
    """Get the permissions profiles directory."""
    return get_workflows_root() / "permissions"


def get_preferences_path() -> Path:
    """Get the preferences profiles directory."""
    return get_workflows_root() / "preferences"


def get_schema_path() -> Path:
    """Get the JSON schemas directory."""
    return get_workflows_root() / "schema"


# ═══════════════════════════════════════════════════════════════
# YAML LOADING
# ═══════════════════════════════════════════════════════════════

def load_yaml(path: Path) -> Dict[str, Any]:
    """Load a YAML file and return as dict."""
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    with open(path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f) or {}


def validate_against_schema(data: Dict[str, Any], schema_name: str) -> List[str]:
    """Validate data against JSON schema, return list of errors."""
    if not HAS_JSONSCHEMA:
        return []  # Skip validation if jsonschema not installed

    schema_path = get_schema_path() / f"{schema_name}.schema.json"
    if not schema_path.exists():
        return [f"Schema not found: {schema_path}"]

    with open(schema_path, 'r', encoding='utf-8') as f:
        schema = json.load(f)

    errors = []
    validator = jsonschema.Draft7Validator(schema)
    for error in validator.iter_errors(data):
        path = ".".join(str(p) for p in error.absolute_path)
        errors.append(f"{path}: {error.message}" if path else error.message)

    return errors


# ═══════════════════════════════════════════════════════════════
# WORKFLOW PARSER
# ═══════════════════════════════════════════════════════════════

def parse_trigger(data: Dict[str, Any]) -> TriggerConfig:
    """Parse trigger configuration."""
    if not data:
        return TriggerConfig(type=TriggerType.MANUAL)

    return TriggerConfig(
        type=TriggerType(data.get("type", "manual")),
        cron=data.get("cron"),
        watch=data.get("watch"),
        event=data.get("event"),
    )


def parse_variable(data: Dict[str, Any]) -> VariableConfig:
    """Parse a single variable configuration."""
    return VariableConfig(
        name=data["name"],
        type=data.get("type", "string"),
        default=data.get("default"),
        prompt=data.get("prompt"),
        required=data.get("required", False),
    )


def parse_branch(data: Dict[str, Any]) -> BranchCondition:
    """Parse a branch condition with nested steps."""
    return BranchCondition(
        condition=data["condition"],
        steps=[parse_step(s) for s in data.get("steps", [])],
    )


def parse_step(data: Dict[str, Any]) -> StepDefinition:
    """Parse a single step definition."""
    # Parse branch conditions if present
    branch = None
    if "branch" in data:
        branch = [parse_branch(b) for b in data["branch"]]

    # Parse model type
    model = ModelType.AUTO
    if "model" in data:
        model = ModelType(data["model"])

    # Parse complexity
    complexity = None
    if "complexity" in data:
        complexity = Complexity(data["complexity"])

    # Parse error action
    on_error = ErrorAction.ABORT
    if "on_error" in data:
        on_error = ErrorAction(data["on_error"])

    # Parse low confidence action
    on_low_confidence = LowConfidenceAction.MANUAL_REVIEW
    if "on_low_confidence" in data:
        on_low_confidence = LowConfidenceAction(data["on_low_confidence"])

    return StepDefinition(
        name=data["name"],
        description=data.get("description"),
        command=data.get("command"),
        prompt=data.get("prompt"),
        bash=data.get("bash"),
        agent=data.get("agent"),
        framework=data.get("framework"),
        script=data.get("script"),
        mode=data.get("mode"),
        config=data.get("config"),
        condition=data.get("condition"),
        loop=data.get("loop"),
        loop_as=data.get("loop_as"),
        parallel=data.get("parallel", False),
        depends_on=data.get("depends_on"),
        branch=branch,
        store_as=data.get("store_as"),
        output=data.get("output"),
        template=data.get("template"),
        confidence_gate=data.get("confidence_gate"),
        on_low_confidence=on_low_confidence,
        model=model,
        complexity=complexity,
        on_error=on_error,
        retry_count=data.get("retry_count", 0),
        retry_delay=data.get("retry_delay"),
        timeout=data.get("timeout"),
    )


def parse_budget(data: Optional[Dict[str, Any]]) -> Optional[BudgetConfig]:
    """Parse budget configuration."""
    if not data:
        return None

    return BudgetConfig(
        max_tokens=data.get("max_tokens"),
        max_cost=data.get("max_cost"),
    )


def parse_audit(data: Optional[Dict[str, Any]]) -> AuditConfig:
    """Parse audit configuration."""
    if not data:
        return AuditConfig()

    log_level = LogLevel.STANDARD
    if "log_level" in data:
        log_level = LogLevel(data["log_level"])

    return AuditConfig(
        log_level=log_level,
        include_prompts=data.get("include_prompts", False),
        include_outputs=data.get("include_outputs", True),
    )


def parse_notify(data: Optional[Dict[str, Any]]) -> NotifyConfig:
    """Parse notify configuration."""
    if not data:
        return NotifyConfig()

    return NotifyConfig(
        on_complete=data.get("on_complete", False),
        on_error=data.get("on_error", True),
        method=data.get("method", "log"),
    )


def parse_settings(data: Dict[str, Any]) -> WorkflowSettings:
    """Parse workflow settings from root level."""
    on_error = ErrorAction.ABORT
    if "on_error" in data:
        on_error = ErrorAction(data["on_error"])

    return WorkflowSettings(
        on_error=on_error,
        max_steps=data.get("max_steps", 50),
        timeout=data.get("timeout", "30m"),
        dry_run=data.get("dry_run", False),
    )


def parse_workflow(data: Dict[str, Any], source_path: Optional[Path] = None) -> WorkflowDefinition:
    """Parse a complete workflow definition from dict."""
    return WorkflowDefinition(
        name=data["name"],
        description=data.get("description", ""),
        version=data.get("version", "1.0"),
        trigger=parse_trigger(data.get("trigger")),
        permissions_profile=data.get("permissions_profile", "default"),
        preferences_profile=data.get("preferences_profile", "default"),
        variables=[parse_variable(v) for v in data.get("variables", [])],
        steps=[parse_step(s) for s in data.get("steps", [])],
        settings=parse_settings(data),
        budget=parse_budget(data.get("budget")),
        audit=parse_audit(data.get("audit")),
        notify=parse_notify(data.get("notify")),
        source_path=source_path,
    )


def load_workflow(name: str) -> WorkflowDefinition:
    """Load a workflow by name from the definitions directory."""
    path = get_definitions_path() / f"{name}.yaml"

    if not path.exists():
        raise WorkflowNotFoundError(name)

    data = load_yaml(path)

    # Validate against schema (non-blocking - parser handles edge cases)
    errors = validate_against_schema(data, "workflow")
    if errors:
        # Log validation warnings but continue - parser is more flexible
        import logging
        logging.warning(f"Workflow '{name}' has schema warnings: {errors}")

    return parse_workflow(data, source_path=path)


def list_workflows() -> List[str]:
    """List all available workflow names."""
    definitions_path = get_definitions_path()
    if not definitions_path.exists():
        return []

    return [
        p.stem for p in definitions_path.glob("*.yaml")
        if not p.name.startswith("_")
    ]


# ═══════════════════════════════════════════════════════════════
# PERMISSIONS PARSER
# ═══════════════════════════════════════════════════════════════

def parse_tool_constraint(data: Dict[str, Any]) -> ToolConstraint:
    """Parse a tool constraint."""
    return ToolConstraint(
        tool=data["tool"],
        paths=data.get("paths"),
        commands=data.get("commands"),
        patterns=data.get("patterns"),
    )


def parse_resource_limits(data: Optional[Dict[str, Any]]) -> ResourceLimits:
    """Parse resource limits."""
    if not data:
        return ResourceLimits()

    return ResourceLimits(
        max_file_size=data.get("max_file_size", "10MB"),
        max_files_per_step=data.get("max_files_per_step", 20),
        max_tokens_per_step=data.get("max_tokens_per_step", 50000),
        max_api_calls=data.get("max_api_calls", 100),
    )


def parse_permissions(data: Dict[str, Any]) -> PermissionsProfile:
    """Parse a permissions profile from dict."""
    tools = data.get("tools", {})
    file_access = data.get("file_access", {})
    command_access = data.get("command_access", {})
    secrets = data.get("secrets", {})

    # Parse tool constraints
    allow_with_constraints = []
    for item in tools.get("allow_with_constraints", []):
        allow_with_constraints.append(parse_tool_constraint(item))

    never_allow = []
    for item in tools.get("never_allow", []):
        if isinstance(item, dict):
            never_allow.append(parse_tool_constraint(item))

    return PermissionsProfile(
        name=data["name"],
        description=data.get("description", ""),
        inherits=data.get("inherits"),
        always_allow=tools.get("always_allow", []),
        allow_with_constraints=allow_with_constraints,
        ask_once=tools.get("ask_once", []),
        never_allow=never_allow,
        readable_paths=file_access.get("readable", "**/*"),
        writable_paths=file_access.get("writable", []),
        protected_paths=file_access.get("protected", []),
        resource_limits=parse_resource_limits(data.get("resource_limits")),
        allowed_commands=command_access.get("allowed", []),
        denied_commands=command_access.get("denied", []),
        allowed_env_vars=secrets.get("allowed_env_vars", []),
        never_log_patterns=secrets.get("never_log", []),
    )


def load_permissions(name: str, resolved: Dict[str, PermissionsProfile] = None) -> PermissionsProfile:
    """Load a permissions profile by name, resolving inheritance."""
    if resolved is None:
        resolved = {}

    if name in resolved:
        return resolved[name]

    path = get_permissions_path() / f"{name}.yaml"

    if not path.exists():
        raise ProfileNotFoundError("Permissions", name)

    data = load_yaml(path)
    profile = parse_permissions(data)

    # Resolve inheritance
    if profile.inherits:
        parent = load_permissions(profile.inherits, resolved)

        # Merge with parent (child overrides)
        profile.always_allow = list(set(parent.always_allow + profile.always_allow))
        profile.ask_once = list(set(parent.ask_once + profile.ask_once))

        if not profile.writable_paths:
            profile.writable_paths = parent.writable_paths
        if not profile.protected_paths:
            profile.protected_paths = parent.protected_paths

    resolved[name] = profile
    return profile


# ═══════════════════════════════════════════════════════════════
# PREFERENCES PARSER
# ═══════════════════════════════════════════════════════════════

def parse_preferences(data: Dict[str, Any]) -> PreferencesProfile:
    """Parse a preferences profile from dict."""
    dm = data.get("decision_making", {})
    coding = data.get("coding", {})
    comm = data.get("communication", {})
    domain = data.get("domain", {})
    auto = data.get("automation", {})
    model = data.get("model_preferences", {})

    return PreferencesProfile(
        name=data["name"],
        description=data.get("description", ""),
        decision_making=DecisionMaking(
            when_multiple_approaches=dm.get("when_multiple_approaches", "prefer_simpler"),
            when_uncertain=dm.get("when_uncertain", "batch_questions"),
            when_error=dm.get("when_error", "fix_and_continue"),
            risk_tolerance=dm.get("risk_tolerance", "medium"),
        ),
        coding=CodingPrefs(
            languages=coding.get("languages", []),
            style=coding.get("style", "functional"),
            comments=coding.get("comments", "minimal"),
        ),
        communication=CommunicationPrefs(
            language=comm.get("language", "German"),
            verbosity=comm.get("verbosity", "concise"),
            format=comm.get("format", "markdown"),
            emojis=comm.get("emojis", False),
        ),
        domain=DomainPrefs(
            focus_areas=domain.get("focus_areas", []),
            tech_stack=domain.get("tech_stack", []),
            avoid=domain.get("avoid", []),
        ),
        automation=AutomationPrefs(
            auto_commit=auto.get("auto_commit", False),
            auto_fix_lint=auto.get("auto_fix_lint", True),
            auto_update_docs=auto.get("auto_update_docs", True),
            batch_similar_tasks=auto.get("batch_similar_tasks", True),
        ),
        model_preferences=ModelPrefs(
            default=model.get("default", "sonnet"),
            complex_reasoning=model.get("complex_reasoning", "opus"),
            simple_tasks=model.get("simple_tasks", "haiku"),
            cost_sensitivity=model.get("cost_sensitivity", "medium"),
        ),
    )


def load_preferences(name: str) -> PreferencesProfile:
    """Load a preferences profile by name."""
    path = get_preferences_path() / f"{name}.yaml"

    if not path.exists():
        raise ProfileNotFoundError("Preferences", name)

    data = load_yaml(path)
    return parse_preferences(data)
