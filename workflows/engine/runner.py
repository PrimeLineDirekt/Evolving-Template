"""
Workflow Engine - Workflow Runner

Main orchestrator that executes complete workflows.
"""

import asyncio
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from workflows.engine.models import (
    BudgetConfig,
    ErrorAction,
    StepStatus,
    WorkflowDefinition,
    WorkflowResult,
)
from workflows.engine.parser import (
    load_workflow,
    load_permissions,
    load_preferences,
)
from workflows.engine.context import WorkflowContext
from workflows.engine.executor import StepExecutor, ModelSelector
from workflows.engine.interpolation import Interpolator
from workflows.engine.exceptions import (
    WorkflowError,
    WorkflowValidationError,
    BudgetExceededError,
    StepExecutionError,
)


# ═══════════════════════════════════════════════════════════════
# WORKFLOW RUNNER
# ═══════════════════════════════════════════════════════════════

class WorkflowRunner:
    """
    Main entry point for workflow execution.

    Usage:
        runner = WorkflowRunner()

        # Run by name
        result = await runner.run("idea-forge-full", variables={"idea": "..."})

        # Run from definition
        workflow = load_workflow("morning-briefing")
        result = await runner.run_definition(workflow)

        # Dry run (preview only)
        preview = await runner.dry_run("weekly-review")
    """

    def __init__(
        self,
        logs_dir: Optional[Path] = None,
        checkpoint_dir: Optional[Path] = None,
    ):
        self.logs_dir = logs_dir or Path("workflows/logs")
        self.checkpoint_dir = checkpoint_dir or Path("workflows/checkpoints")

        # Ensure directories exist
        self.logs_dir.mkdir(parents=True, exist_ok=True)
        self.checkpoint_dir.mkdir(parents=True, exist_ok=True)

        self.model_selector = ModelSelector()

    # ─────────────────────────────────────────────────────────────
    # PUBLIC API
    # ─────────────────────────────────────────────────────────────

    async def run(
        self,
        workflow_name: str,
        variables: Optional[Dict[str, Any]] = None,
        dry_run: bool = False,
        resume_from: Optional[str] = None,
    ) -> WorkflowResult:
        """
        Run a workflow by name.

        Args:
            workflow_name: Name of workflow in definitions/
            variables: Override/provide workflow variables
            dry_run: Preview only, don't execute
            resume_from: Run ID to resume from checkpoint

        Returns:
            WorkflowResult with execution details
        """
        # Load workflow definition
        workflow = load_workflow(workflow_name)

        # Override dry_run from settings
        if dry_run or workflow.settings.dry_run:
            return await self.dry_run(workflow_name, variables)

        return await self.run_definition(
            workflow,
            variables=variables,
            resume_from=resume_from,
        )

    async def run_definition(
        self,
        workflow: WorkflowDefinition,
        variables: Optional[Dict[str, Any]] = None,
        resume_from: Optional[str] = None,
    ) -> WorkflowResult:
        """
        Run a workflow from its definition.

        Args:
            workflow: Parsed workflow definition
            variables: Override/provide workflow variables
            resume_from: Run ID to resume from checkpoint

        Returns:
            WorkflowResult
        """
        # Load profiles
        permissions = load_permissions(workflow.permissions_profile)
        preferences = load_preferences(workflow.preferences_profile)

        # Create or restore context
        if resume_from:
            context = WorkflowContext.load_checkpoint(workflow.name, resume_from)
            if not context:
                raise WorkflowError(f"Checkpoint not found: {resume_from}")
            context.log(f"Resumed from checkpoint at step {context.current_step}")
        else:
            context = WorkflowContext(
                workflow_name=workflow.name,
                log_level=workflow.audit.log_level,
            )

        # Initialize variables
        await self._init_variables(workflow, context, variables or {})

        # Create executor
        executor = StepExecutor(context, self.model_selector)

        # Execute workflow
        result = await self._execute_workflow(workflow, context, executor)

        # Write logs
        self._write_logs(workflow, context, result)

        return result

    async def dry_run(
        self,
        workflow_name: str,
        variables: Optional[Dict[str, Any]] = None,
    ) -> WorkflowResult:
        """
        Preview workflow execution without actually running.

        Args:
            workflow_name: Name of workflow
            variables: Variables to use in preview

        Returns:
            WorkflowResult with preview data
        """
        workflow = load_workflow(workflow_name)
        context = WorkflowContext(
            workflow_name=workflow.name,
            log_level=workflow.audit.log_level,
        )

        # Initialize variables
        await self._init_variables(workflow, context, variables or {})

        # Create interpolator for previewing
        interpolator = Interpolator(context.get_all())

        # Preview each step
        preview_steps = []
        for step in workflow.steps:
            step_preview = {
                "name": step.name,
                "type": step.get_execution_type(),
                "model": self.model_selector.select(step),
            }

            # Show interpolated values where possible
            if step.condition:
                step_preview["condition"] = step.condition
                try:
                    step_preview["condition_result"] = interpolator.evaluate_condition(
                        step.condition
                    )
                except Exception:
                    step_preview["condition_result"] = "unknown"

            if step.prompt:
                try:
                    step_preview["prompt_preview"] = interpolator.interpolate(
                        step.prompt
                    )[:200] + "..."
                except Exception:
                    step_preview["prompt_preview"] = step.prompt[:200] + "..."

            if step.output:
                try:
                    step_preview["output_path"] = str(
                        interpolator.resolve_path(step.output)
                    )
                except Exception:
                    step_preview["output_path"] = step.output

            preview_steps.append(step_preview)

        # Estimate resources
        estimated_tokens = sum(
            self._estimate_step_tokens(s) for s in workflow.steps
        )
        estimated_cost = self._estimate_cost(estimated_tokens)

        return WorkflowResult(
            workflow_name=workflow.name,
            run_id=f"dry-run-{context.run_id}",
            status=StepStatus.SUCCESS,
            started_at=datetime.now(),
            completed_at=datetime.now(),
            variables=context.variables,
            step_results={"preview": preview_steps},
            total_tokens=estimated_tokens,
            total_cost=estimated_cost,
        )

    async def list_available(self) -> List[Dict[str, Any]]:
        """List all available workflows with metadata."""
        from workflows.engine.parser import list_workflows, get_definitions_path

        workflows = []
        for name in list_workflows():
            try:
                workflow = load_workflow(name)
                workflows.append({
                    "name": workflow.name,
                    "description": workflow.description,
                    "version": workflow.version,
                    "trigger": workflow.trigger.type.value,
                    "steps": len(workflow.steps),
                    "permissions": workflow.permissions_profile,
                    "preferences": workflow.preferences_profile,
                })
            except Exception as e:
                workflows.append({
                    "name": name,
                    "error": str(e),
                })

        return workflows

    # ─────────────────────────────────────────────────────────────
    # INTERNAL METHODS
    # ─────────────────────────────────────────────────────────────

    async def _init_variables(
        self,
        workflow: WorkflowDefinition,
        context: WorkflowContext,
        provided: Dict[str, Any],
    ):
        """Initialize workflow variables."""
        for var_config in workflow.variables:
            name = var_config.name

            # Use provided value, default, or None
            if name in provided:
                value = provided[name]
            elif var_config.default is not None:
                value = var_config.default
            elif var_config.required:
                raise WorkflowValidationError(
                    f"Required variable '{name}' not provided",
                    errors=[f"Missing required variable: {name}"],
                )
            else:
                value = None

            # Type coercion
            if var_config.type == "number" and value is not None:
                value = float(value)
            elif var_config.type == "boolean" and value is not None:
                value = bool(value)
            elif var_config.type == "list" and isinstance(value, str):
                import json
                value = json.loads(value)

            context.store(name, value)

    async def _execute_workflow(
        self,
        workflow: WorkflowDefinition,
        context: WorkflowContext,
        executor: StepExecutor,
    ) -> WorkflowResult:
        """Execute all workflow steps."""
        context.mark_running()
        context.log(f"Starting workflow: {workflow.name} (v{workflow.version})")

        try:
            # Execute steps
            for i, step in enumerate(workflow.steps):
                context.current_step = i

                # Check budget before each step
                if workflow.budget:
                    self._check_budget(workflow.budget, context)

                # Check max steps
                if i >= workflow.settings.max_steps:
                    raise WorkflowError(
                        f"Max steps ({workflow.settings.max_steps}) exceeded"
                    )

                # Execute step
                result = await executor.execute(step)

                # Checkpoint after each step
                context.checkpoint()

                # Handle step failure
                if not result.success:
                    if result.status == StepStatus.PAUSED:
                        return self._create_result(
                            workflow, context, StepStatus.PAUSED
                        )
                    elif workflow.settings.on_error == ErrorAction.ABORT:
                        context.mark_failed(f"Step '{step.name}' failed: {result.error}")
                        return self._create_result(
                            workflow, context, StepStatus.FAILED, result.error
                        )
                    # CONTINUE: keep going

            # All steps completed
            context.mark_completed()
            context.log(f"Workflow completed successfully")

            return self._create_result(workflow, context, StepStatus.SUCCESS)

        except BudgetExceededError as e:
            context.mark_failed(str(e))
            return self._create_result(
                workflow, context, StepStatus.FAILED, str(e)
            )
        except Exception as e:
            context.mark_failed(str(e))
            return self._create_result(
                workflow, context, StepStatus.FAILED, str(e)
            )

    def _check_budget(self, budget: BudgetConfig, context: WorkflowContext):
        """Check if budget limits are exceeded."""
        if budget.max_tokens and context.token_usage > budget.max_tokens:
            raise BudgetExceededError(
                "tokens", context.token_usage, budget.max_tokens
            )

        if budget.max_cost and context.cost > budget.max_cost:
            raise BudgetExceededError(
                "cost", context.cost, budget.max_cost
            )

    def _create_result(
        self,
        workflow: WorkflowDefinition,
        context: WorkflowContext,
        status: StepStatus,
        error: Optional[str] = None,
    ) -> WorkflowResult:
        """Create workflow result from context."""
        return WorkflowResult(
            workflow_name=workflow.name,
            run_id=context.run_id,
            status=status,
            started_at=context.started_at,
            completed_at=context.completed_at or datetime.now(),
            step_results=context.step_results,
            variables=context.variables,
            total_tokens=context.token_usage,
            total_cost=context.cost,
            error=error,
        )

    def _write_logs(
        self,
        workflow: WorkflowDefinition,
        context: WorkflowContext,
        result: WorkflowResult,
    ):
        """Write execution logs to file."""
        import json

        log_file = self.logs_dir / f"{workflow.name}-{context.run_id}.json"

        log_data = {
            "workflow": workflow.name,
            "version": workflow.version,
            "run_id": context.run_id,
            "status": result.status.value,
            "started_at": result.started_at.isoformat(),
            "completed_at": result.completed_at.isoformat() if result.completed_at else None,
            "duration_seconds": result.duration_seconds,
            "total_tokens": result.total_tokens,
            "total_cost": round(result.total_cost, 4),
            "error": result.error,
            "variables": context.variables,
            "step_results": context.step_results,
            "logs": [log.to_dict() for log in context.logs],
        }

        log_file.write_text(
            json.dumps(log_data, indent=2, ensure_ascii=False, default=str)
        )

    def _estimate_step_tokens(self, step) -> int:
        """Estimate tokens for a step."""
        step_type = step.get_execution_type()

        estimates = {
            "bash": 100,
            "command": 500,
            "script": 200,
            "prompt": 2000,
            "agent": 5000,
            "framework": 10000,
            "output": 100,
            "branch": 500,
        }

        return estimates.get(step_type, 1000)

    def _estimate_cost(self, tokens: int) -> float:
        """Estimate cost for tokens (using average model pricing)."""
        # Average pricing between haiku/sonnet/opus
        avg_cost_per_1m = 0.005  # ~$5 per 1M tokens average
        return (tokens / 1_000_000) * avg_cost_per_1m


# ═══════════════════════════════════════════════════════════════
# CONVENIENCE FUNCTIONS
# ═══════════════════════════════════════════════════════════════

async def run_workflow(
    name: str,
    variables: Optional[Dict[str, Any]] = None,
    dry_run: bool = False,
) -> WorkflowResult:
    """
    Convenience function to run a workflow.

    Args:
        name: Workflow name
        variables: Workflow variables
        dry_run: Preview only

    Returns:
        WorkflowResult
    """
    runner = WorkflowRunner()
    return await runner.run(name, variables=variables, dry_run=dry_run)


def run_workflow_sync(
    name: str,
    variables: Optional[Dict[str, Any]] = None,
    dry_run: bool = False,
) -> WorkflowResult:
    """
    Synchronous wrapper for run_workflow.

    Args:
        name: Workflow name
        variables: Workflow variables
        dry_run: Preview only

    Returns:
        WorkflowResult
    """
    return asyncio.run(run_workflow(name, variables=variables, dry_run=dry_run))
