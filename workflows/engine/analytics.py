"""
Workflow Engine - Analytics & Optimization

Usage tracking, ROI calculation, and optimization suggestions.
"""

import json
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional

from workflows.engine.models import WorkflowDefinition, StepDefinition, ModelType
from workflows.engine.parser import load_workflow, list_workflows


# ═══════════════════════════════════════════════════════════════
# DATA MODELS
# ═══════════════════════════════════════════════════════════════

@dataclass
class WorkflowStats:
    """Statistics for a single workflow."""
    workflow_name: str
    total_runs: int
    successful_runs: int
    failed_runs: int
    success_rate: float
    avg_duration_seconds: float
    avg_tokens: int
    avg_cost: float
    total_tokens: int
    total_cost: float
    estimated_time_saved_hours: float
    last_run: Optional[str] = None


@dataclass
class RunSummary:
    """Summary of a single run."""
    run_id: str
    workflow_name: str
    status: str
    started_at: str
    completed_at: Optional[str]
    duration_seconds: float
    tokens_used: int
    cost: float
    steps_completed: int
    steps_failed: int


@dataclass
class ROIReport:
    """Return on Investment report."""
    period_start: str
    period_end: str
    total_workflows_run: int
    total_tokens_used: int
    total_cost: float
    total_duration_hours: float
    estimated_manual_hours: float
    estimated_time_saved_hours: float
    roi_multiplier: float
    cost_per_hour_saved: float
    breakdown_by_workflow: Dict[str, Dict[str, Any]]


@dataclass
class OptimizationSuggestion:
    """A suggestion for workflow optimization."""
    workflow_name: str
    suggestion_type: str
    message: str
    potential_savings: str
    priority: str
    details: Dict[str, Any] = field(default_factory=dict)


# ═══════════════════════════════════════════════════════════════
# MANUAL TIME ESTIMATES
# ═══════════════════════════════════════════════════════════════

# Estimated manual time for workflow types (in minutes)
MANUAL_TIME_ESTIMATES = {
    "idea-forge-full": 180,      # 3 hours
    "weekly-review": 60,         # 1 hour
    "inbox-processing": 30,      # 30 minutes
    "morning-briefing": 15,      # 15 minutes
    "default": 30,               # Default 30 minutes
}


# ═══════════════════════════════════════════════════════════════
# ANALYTICS ENGINE
# ═══════════════════════════════════════════════════════════════

class WorkflowAnalytics:
    """
    Tracks and analyzes workflow usage.

    Features:
    - Run statistics per workflow
    - ROI calculations
    - Trend analysis
    - Usage reports
    """

    def __init__(self, logs_dir: Optional[Path] = None):
        self.logs_dir = logs_dir or Path("workflows/logs")

    def get_workflow_stats(self, workflow_name: str) -> WorkflowStats:
        """Get statistics for a single workflow."""
        runs = self._load_runs(workflow_name)

        if not runs:
            return WorkflowStats(
                workflow_name=workflow_name,
                total_runs=0,
                successful_runs=0,
                failed_runs=0,
                success_rate=0.0,
                avg_duration_seconds=0.0,
                avg_tokens=0,
                avg_cost=0.0,
                total_tokens=0,
                total_cost=0.0,
                estimated_time_saved_hours=0.0,
            )

        successful = [r for r in runs if r["status"] == "success"]
        failed = [r for r in runs if r["status"] == "failed"]

        total_duration = sum(r.get("duration_seconds", 0) for r in runs)
        total_tokens = sum(r.get("total_tokens", 0) for r in runs)
        total_cost = sum(r.get("total_cost", 0) for r in runs)

        # Calculate time saved
        manual_time_minutes = MANUAL_TIME_ESTIMATES.get(
            workflow_name,
            MANUAL_TIME_ESTIMATES["default"]
        )
        time_saved_hours = (len(successful) * manual_time_minutes) / 60

        return WorkflowStats(
            workflow_name=workflow_name,
            total_runs=len(runs),
            successful_runs=len(successful),
            failed_runs=len(failed),
            success_rate=len(successful) / len(runs) * 100 if runs else 0,
            avg_duration_seconds=total_duration / len(runs) if runs else 0,
            avg_tokens=total_tokens // len(runs) if runs else 0,
            avg_cost=total_cost / len(runs) if runs else 0,
            total_tokens=total_tokens,
            total_cost=total_cost,
            estimated_time_saved_hours=time_saved_hours,
            last_run=runs[-1].get("started_at") if runs else None,
        )

    def get_all_stats(self) -> List[WorkflowStats]:
        """Get statistics for all workflows."""
        stats = []
        for name in list_workflows():
            stats.append(self.get_workflow_stats(name))
        return stats

    def get_roi_report(
        self,
        days: int = 30,
        hourly_rate: float = 50.0,
    ) -> ROIReport:
        """Generate ROI report for a period."""
        cutoff = datetime.now() - timedelta(days=days)
        cutoff_str = cutoff.isoformat()

        all_runs = []
        for name in list_workflows():
            runs = self._load_runs(name)
            for run in runs:
                if run.get("started_at", "") >= cutoff_str:
                    run["workflow_name"] = name
                    all_runs.append(run)

        # Calculate totals
        total_tokens = sum(r.get("total_tokens", 0) for r in all_runs)
        total_cost = sum(r.get("total_cost", 0) for r in all_runs)
        total_duration = sum(r.get("duration_seconds", 0) for r in all_runs)

        # Calculate time saved
        breakdown = {}
        total_manual_hours = 0.0

        for name in list_workflows():
            workflow_runs = [r for r in all_runs if r.get("workflow_name") == name]
            successful = len([r for r in workflow_runs if r["status"] == "success"])

            manual_minutes = MANUAL_TIME_ESTIMATES.get(name, MANUAL_TIME_ESTIMATES["default"])
            manual_hours = (successful * manual_minutes) / 60
            total_manual_hours += manual_hours

            breakdown[name] = {
                "runs": len(workflow_runs),
                "successful": successful,
                "tokens": sum(r.get("total_tokens", 0) for r in workflow_runs),
                "cost": sum(r.get("total_cost", 0) for r in workflow_runs),
                "manual_hours_saved": manual_hours,
            }

        # Calculate ROI
        time_saved_hours = total_manual_hours
        value_of_time_saved = time_saved_hours * hourly_rate
        roi_multiplier = value_of_time_saved / total_cost if total_cost > 0 else 0
        cost_per_hour = total_cost / time_saved_hours if time_saved_hours > 0 else 0

        return ROIReport(
            period_start=cutoff_str,
            period_end=datetime.now().isoformat(),
            total_workflows_run=len(all_runs),
            total_tokens_used=total_tokens,
            total_cost=total_cost,
            total_duration_hours=total_duration / 3600,
            estimated_manual_hours=total_manual_hours,
            estimated_time_saved_hours=time_saved_hours,
            roi_multiplier=roi_multiplier,
            cost_per_hour_saved=cost_per_hour,
            breakdown_by_workflow=breakdown,
        )

    def get_recent_runs(self, limit: int = 20) -> List[RunSummary]:
        """Get most recent runs across all workflows."""
        all_runs = []

        for name in list_workflows():
            runs = self._load_runs(name)
            for run in runs:
                all_runs.append(RunSummary(
                    run_id=run.get("run_id", "unknown"),
                    workflow_name=name,
                    status=run.get("status", "unknown"),
                    started_at=run.get("started_at", ""),
                    completed_at=run.get("completed_at"),
                    duration_seconds=run.get("duration_seconds", 0),
                    tokens_used=run.get("total_tokens", 0),
                    cost=run.get("total_cost", 0),
                    steps_completed=len(run.get("step_results", {})),
                    steps_failed=0,  # TODO: Calculate from step data
                ))

        # Sort by start time descending
        all_runs.sort(key=lambda r: r.started_at, reverse=True)
        return all_runs[:limit]

    def _load_runs(self, workflow_name: str) -> List[Dict[str, Any]]:
        """Load all runs for a workflow from logs."""
        runs = []

        if not self.logs_dir.exists():
            return runs

        for log_file in self.logs_dir.glob(f"{workflow_name}-*.json"):
            # Skip audit logs
            if ".audit." in log_file.name:
                continue

            try:
                data = json.loads(log_file.read_text())
                runs.append(data)
            except Exception:
                pass

        # Sort by start time
        runs.sort(key=lambda r: r.get("started_at", ""))
        return runs


# ═══════════════════════════════════════════════════════════════
# WORKFLOW OPTIMIZER
# ═══════════════════════════════════════════════════════════════

class WorkflowOptimizer:
    """
    Analyzes workflows and suggests optimizations.

    Optimizations:
    - Model downgrades (opus → sonnet where possible)
    - Parallelization opportunities
    - Caching suggestions
    - Step consolidation
    """

    def analyze(self, workflow_name: str) -> List[OptimizationSuggestion]:
        """Analyze a workflow and return optimization suggestions."""
        suggestions = []

        try:
            workflow = load_workflow(workflow_name)
        except Exception:
            return suggestions

        # Check for model optimization
        suggestions.extend(self._check_model_optimization(workflow))

        # Check for parallelization
        suggestions.extend(self._check_parallelization(workflow))

        # Check for step consolidation
        suggestions.extend(self._check_consolidation(workflow))

        # Check for caching
        suggestions.extend(self._check_caching(workflow))

        return suggestions

    def _check_model_optimization(
        self, workflow: WorkflowDefinition
    ) -> List[OptimizationSuggestion]:
        """Check for steps that could use cheaper models."""
        suggestions = []

        for step in workflow.steps:
            if step.model == ModelType.OPUS:
                # Check if step is simple enough for sonnet
                if self._is_simple_step(step):
                    suggestions.append(OptimizationSuggestion(
                        workflow_name=workflow.name,
                        suggestion_type="model_downgrade",
                        message=f"Step '{step.name}' could use Sonnet instead of Opus",
                        potential_savings="~80% token cost reduction",
                        priority="medium",
                        details={
                            "step": step.name,
                            "current_model": "opus",
                            "suggested_model": "sonnet",
                        },
                    ))
            elif step.model == ModelType.SONNET:
                # Check if step is simple enough for haiku
                if self._is_trivial_step(step):
                    suggestions.append(OptimizationSuggestion(
                        workflow_name=workflow.name,
                        suggestion_type="model_downgrade",
                        message=f"Step '{step.name}' could use Haiku instead of Sonnet",
                        potential_savings="~90% token cost reduction",
                        priority="low",
                        details={
                            "step": step.name,
                            "current_model": "sonnet",
                            "suggested_model": "haiku",
                        },
                    ))

        return suggestions

    def _check_parallelization(
        self, workflow: WorkflowDefinition
    ) -> List[OptimizationSuggestion]:
        """Check for steps that could run in parallel."""
        suggestions = []

        # Find independent steps
        independent_groups = []
        current_group = []

        for i, step in enumerate(workflow.steps):
            if step.depends_on:
                if current_group:
                    independent_groups.append(current_group)
                    current_group = []
            else:
                # Check if step depends on previous step's output
                if i > 0:
                    prev_step = workflow.steps[i - 1]
                    if prev_step.store_as and f"{{{{{prev_step.store_as}}}}}" in str(step):
                        if current_group:
                            independent_groups.append(current_group)
                            current_group = []
                    else:
                        current_group.append(step.name)
                else:
                    current_group.append(step.name)

        if current_group:
            independent_groups.append(current_group)

        # Suggest parallelization for groups > 1
        for group in independent_groups:
            if len(group) > 1:
                suggestions.append(OptimizationSuggestion(
                    workflow_name=workflow.name,
                    suggestion_type="parallelization",
                    message=f"Steps {group} could run in parallel",
                    potential_savings="~50% time reduction",
                    priority="medium",
                    details={
                        "steps": group,
                    },
                ))

        return suggestions

    def _check_consolidation(
        self, workflow: WorkflowDefinition
    ) -> List[OptimizationSuggestion]:
        """Check for steps that could be consolidated."""
        suggestions = []

        # Find consecutive prompt steps that could be combined
        consecutive_prompts = []

        for i, step in enumerate(workflow.steps):
            if step.prompt:
                if consecutive_prompts and consecutive_prompts[-1][1] == i - 1:
                    consecutive_prompts[-1] = (consecutive_prompts[-1][0], i, step.name)
                else:
                    consecutive_prompts.append((step.name, i, step.name))

        for group in consecutive_prompts:
            if len(group) > 2:
                start_name, _, end_name = group
                suggestions.append(OptimizationSuggestion(
                    workflow_name=workflow.name,
                    suggestion_type="consolidation",
                    message=f"Steps from '{start_name}' to '{end_name}' could be combined",
                    potential_savings="~30% token reduction",
                    priority="low",
                    details={
                        "steps": [start_name, end_name],
                    },
                ))

        return suggestions

    def _check_caching(
        self, workflow: WorkflowDefinition
    ) -> List[OptimizationSuggestion]:
        """Check for caching opportunities."""
        suggestions = []

        # Check for steps with static inputs that could be cached
        for step in workflow.steps:
            if step.agent and not step.condition:
                # Agent steps with no conditions could potentially cache results
                suggestions.append(OptimizationSuggestion(
                    workflow_name=workflow.name,
                    suggestion_type="caching",
                    message=f"Step '{step.name}' results could be cached",
                    potential_savings="~100% cost for repeated runs",
                    priority="low",
                    details={
                        "step": step.name,
                        "type": "agent_result_cache",
                    },
                ))

        return suggestions

    def _is_simple_step(self, step: StepDefinition) -> bool:
        """Check if step is simple enough for a smaller model."""
        # Check step type
        if step.get_execution_type() in ("bash", "command", "output"):
            return True

        # Check prompt length
        if step.prompt and len(step.prompt) < 500:
            return True

        # Check for low complexity indicator
        if step.complexity and step.complexity.value in ("low", "medium"):
            return True

        return False

    def _is_trivial_step(self, step: StepDefinition) -> bool:
        """Check if step is trivial (can use haiku)."""
        # Very simple operations
        if step.get_execution_type() in ("bash", "output"):
            return True

        # Very short prompts
        if step.prompt and len(step.prompt) < 200:
            return True

        return False


# ═══════════════════════════════════════════════════════════════
# DRY RUN PREVIEW
# ═══════════════════════════════════════════════════════════════

@dataclass
class DryRunPreview:
    """Preview of workflow execution."""
    workflow_name: str
    version: str
    steps: List[Dict[str, Any]]
    estimated_tokens: int
    estimated_cost: float
    estimated_duration_seconds: float
    tools_used: List[str]
    files_affected: List[str]


class DryRunner:
    """
    Simulates workflow execution without actually running.

    Provides:
    - Step-by-step preview
    - Resource estimates
    - Tool usage preview
    - File impact analysis
    """

    # Token estimates by step type
    TOKEN_ESTIMATES = {
        "bash": 100,
        "command": 500,
        "script": 200,
        "prompt": 2000,
        "agent": 5000,
        "framework": 10000,
        "output": 100,
        "branch": 500,
    }

    # Duration estimates by step type (seconds)
    DURATION_ESTIMATES = {
        "bash": 5,
        "command": 30,
        "script": 10,
        "prompt": 20,
        "agent": 60,
        "framework": 120,
        "output": 2,
        "branch": 10,
    }

    def preview(self, workflow_name: str) -> DryRunPreview:
        """Generate a dry run preview."""
        workflow = load_workflow(workflow_name)

        steps = []
        tools_used = set()
        files_affected = []
        total_tokens = 0
        total_duration = 0

        for step in workflow.steps:
            step_type = step.get_execution_type()

            # Estimate tokens
            tokens = self.TOKEN_ESTIMATES.get(step_type, 1000)
            total_tokens += tokens

            # Estimate duration
            duration = self.DURATION_ESTIMATES.get(step_type, 30)
            total_duration += duration

            # Track tools
            if step_type == "bash":
                tools_used.add("Bash")
            elif step_type in ("prompt", "agent"):
                tools_used.add("AI")
            elif step_type == "output":
                tools_used.add("Write")
                if step.output:
                    files_affected.append(step.output)

            steps.append({
                "name": step.name,
                "type": step_type,
                "model": step.model.value,
                "estimated_tokens": tokens,
                "estimated_duration": duration,
                "condition": step.condition,
                "output": step.output,
            })

        # Estimate cost (using average pricing)
        estimated_cost = (total_tokens / 1_000_000) * 5  # ~$5 per 1M tokens

        return DryRunPreview(
            workflow_name=workflow.name,
            version=workflow.version,
            steps=steps,
            estimated_tokens=total_tokens,
            estimated_cost=estimated_cost,
            estimated_duration_seconds=total_duration,
            tools_used=list(tools_used),
            files_affected=files_affected,
        )
