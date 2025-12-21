"""
Workflow Engine - Step Executor

Executes individual workflow steps based on their type.
"""

import asyncio
import subprocess
import sys
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, TYPE_CHECKING

from workflows.engine.models import (
    BranchCondition,
    ErrorAction,
    LowConfidenceAction,
    ModelType,
    StepDefinition,
    StepResult,
    StepStatus,
)
from workflows.engine.interpolation import Interpolator
from workflows.engine.exceptions import (
    StepExecutionError,
    LowConfidenceError,
    PermissionDeniedError,
)

if TYPE_CHECKING:
    from workflows.engine.context import WorkflowContext


# ═══════════════════════════════════════════════════════════════
# MODEL SELECTOR
# ═══════════════════════════════════════════════════════════════

class ModelSelector:
    """Selects optimal model based on step complexity."""

    COMPLEXITY_MAP = {
        "low": "haiku",
        "medium": "sonnet",
        "high": "opus",
    }

    # Step type to default complexity
    TYPE_COMPLEXITY = {
        "bash": "low",
        "command": "low",
        "script": "low",
        "prompt": "medium",
        "agent": "high",
        "framework": "high",
    }

    def select(self, step: StepDefinition) -> str:
        """Select model for a step."""
        # Explicit model specified
        if step.model and step.model != ModelType.AUTO:
            return step.model.value

        # Explicit complexity specified
        if step.complexity:
            return self.COMPLEXITY_MAP.get(step.complexity.value, "sonnet")

        # Auto-detect based on step type
        step_type = step.get_execution_type()
        default_complexity = self.TYPE_COMPLEXITY.get(step_type, "medium")

        # Upgrade for complex indicators
        if step.confidence_gate and step.confidence_gate > 80:
            default_complexity = "high"
        if step.branch:
            default_complexity = "high"

        return self.COMPLEXITY_MAP.get(default_complexity, "sonnet")


# ═══════════════════════════════════════════════════════════════
# STEP HANDLERS (Strategy Pattern)
# ═══════════════════════════════════════════════════════════════

class StepHandler(ABC):
    """Base class for step execution handlers."""

    @abstractmethod
    async def execute(
        self,
        step: StepDefinition,
        context: 'WorkflowContext',
        interpolator: Interpolator,
        model: str,
    ) -> StepResult:
        """Execute the step and return result."""
        pass


class BashHandler(StepHandler):
    """Executes bash commands."""

    async def execute(
        self,
        step: StepDefinition,
        context: 'WorkflowContext',
        interpolator: Interpolator,
        model: str,
    ) -> StepResult:
        command = interpolator.interpolate(step.bash)
        context.log(f"Executing bash: {command}")

        start_time = datetime.now()
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=self._parse_timeout(step.timeout),
                cwd=str(Path.cwd()),
            )

            duration_ms = int((datetime.now() - start_time).total_seconds() * 1000)

            if result.returncode != 0:
                return StepResult(
                    status=StepStatus.FAILED,
                    data={"stdout": result.stdout, "stderr": result.stderr},
                    error=f"Exit code {result.returncode}: {result.stderr}",
                    duration_ms=duration_ms,
                )

            return StepResult(
                status=StepStatus.SUCCESS,
                data={
                    "stdout": result.stdout.strip(),
                    "stderr": result.stderr.strip(),
                    "exit_code": result.returncode,
                },
                duration_ms=duration_ms,
            )

        except subprocess.TimeoutExpired:
            return StepResult(
                status=StepStatus.FAILED,
                error=f"Command timed out after {step.timeout}",
            )
        except Exception as e:
            return StepResult(
                status=StepStatus.FAILED,
                error=str(e),
            )

    def _parse_timeout(self, timeout: Optional[str]) -> Optional[float]:
        """Parse timeout string to seconds."""
        if not timeout:
            return 120  # Default 2 minutes

        if timeout.endswith("s"):
            return float(timeout[:-1])
        if timeout.endswith("m"):
            return float(timeout[:-1]) * 60
        if timeout.endswith("h"):
            return float(timeout[:-1]) * 3600

        return float(timeout)


class CommandHandler(StepHandler):
    """Executes slash commands via Claude Code."""

    async def execute(
        self,
        step: StepDefinition,
        context: 'WorkflowContext',
        interpolator: Interpolator,
        model: str,
    ) -> StepResult:
        command = interpolator.interpolate(step.command)
        context.log(f"Executing command: {command}")

        start_time = datetime.now()
        try:
            # Use Claude Code SDK for command execution
            from claude_code_sdk import query, QueryOptions, Model

            model_enum = self._get_model_enum(model)

            response = await query(
                prompt=f"Execute this command and return the result: {command}",
                options=QueryOptions(model=model_enum),
            )

            duration_ms = int((datetime.now() - start_time).total_seconds() * 1000)

            # Extract text from response
            result_text = ""
            tokens = 0
            for message in response:
                if hasattr(message, 'content'):
                    for block in message.content:
                        if hasattr(block, 'text'):
                            result_text += block.text
                if hasattr(message, 'usage'):
                    tokens += getattr(message.usage, 'output_tokens', 0)

            context.add_tokens(tokens, model)

            return StepResult(
                status=StepStatus.SUCCESS,
                data=result_text.strip(),
                tokens_used=tokens,
                duration_ms=duration_ms,
                model_used=model,
            )

        except ImportError:
            context.log_warning("Claude Code SDK not available, simulating command")
            return StepResult(
                status=StepStatus.SUCCESS,
                data=f"[Simulated] Command executed: {command}",
                duration_ms=int((datetime.now() - start_time).total_seconds() * 1000),
            )
        except Exception as e:
            return StepResult(
                status=StepStatus.FAILED,
                error=str(e),
            )

    def _get_model_enum(self, model: str):
        """Convert model string to SDK enum."""
        from claude_code_sdk import Model

        model_map = {
            "haiku": Model.CLAUDE_3_5_HAIKU,
            "sonnet": Model.CLAUDE_SONNET_4,
            "opus": Model.CLAUDE_OPUS_4,
        }
        return model_map.get(model.lower(), Model.CLAUDE_SONNET_4)


class PromptHandler(StepHandler):
    """Executes AI prompts via Claude Code SDK."""

    async def execute(
        self,
        step: StepDefinition,
        context: 'WorkflowContext',
        interpolator: Interpolator,
        model: str,
    ) -> StepResult:
        prompt = interpolator.interpolate(step.prompt)
        context.log(f"Executing prompt with {model}")

        start_time = datetime.now()
        try:
            from claude_code_sdk import query, QueryOptions, Model

            model_enum = self._get_model_enum(model)

            response = await query(
                prompt=prompt,
                options=QueryOptions(model=model_enum),
            )

            duration_ms = int((datetime.now() - start_time).total_seconds() * 1000)

            # Extract text and usage
            result_text = ""
            tokens = 0
            confidence = None

            for message in response:
                if hasattr(message, 'content'):
                    for block in message.content:
                        if hasattr(block, 'text'):
                            result_text += block.text
                if hasattr(message, 'usage'):
                    tokens += getattr(message.usage, 'output_tokens', 0)

            context.add_tokens(tokens, model)

            # Try to extract confidence from response
            if "[confidence:" in result_text.lower():
                import re
                match = re.search(r'\[confidence:\s*(\d+)\]', result_text.lower())
                if match:
                    confidence = float(match.group(1))

            return StepResult(
                status=StepStatus.SUCCESS,
                data=result_text.strip(),
                confidence=confidence,
                tokens_used=tokens,
                duration_ms=duration_ms,
                model_used=model,
            )

        except ImportError:
            context.log_warning("Claude Code SDK not available, simulating prompt")
            return StepResult(
                status=StepStatus.SUCCESS,
                data=f"[Simulated] Prompt response for: {prompt[:50]}...",
                duration_ms=int((datetime.now() - start_time).total_seconds() * 1000),
            )
        except Exception as e:
            return StepResult(
                status=StepStatus.FAILED,
                error=str(e),
            )

    def _get_model_enum(self, model: str):
        from claude_code_sdk import Model

        model_map = {
            "haiku": Model.CLAUDE_3_5_HAIKU,
            "sonnet": Model.CLAUDE_SONNET_4,
            "opus": Model.CLAUDE_OPUS_4,
        }
        return model_map.get(model.lower(), Model.CLAUDE_SONNET_4)


class AgentHandler(StepHandler):
    """Executes agent prompts."""

    async def execute(
        self,
        step: StepDefinition,
        context: 'WorkflowContext',
        interpolator: Interpolator,
        model: str,
    ) -> StepResult:
        agent_name = step.agent
        prompt = interpolator.interpolate(step.prompt or "")
        context.log(f"Executing agent: {agent_name} with {model}")

        # Load agent prompt from .claude/agents/
        agent_path = Path(f".claude/agents/{agent_name}.md")
        if not agent_path.exists():
            return StepResult(
                status=StepStatus.FAILED,
                error=f"Agent not found: {agent_name}",
            )

        agent_prompt = agent_path.read_text()
        full_prompt = f"{agent_prompt}\n\n---\n\n{prompt}"

        start_time = datetime.now()
        try:
            from claude_code_sdk import query, QueryOptions, Model

            model_enum = self._get_model_enum(model)

            response = await query(
                prompt=full_prompt,
                options=QueryOptions(model=model_enum),
            )

            duration_ms = int((datetime.now() - start_time).total_seconds() * 1000)

            result_text = ""
            tokens = 0
            confidence = None

            for message in response:
                if hasattr(message, 'content'):
                    for block in message.content:
                        if hasattr(block, 'text'):
                            result_text += block.text
                if hasattr(message, 'usage'):
                    tokens += getattr(message.usage, 'output_tokens', 0)

            context.add_tokens(tokens, model)

            # Extract confidence if present
            if "[confidence:" in result_text.lower():
                import re
                match = re.search(r'\[confidence:\s*(\d+)\]', result_text.lower())
                if match:
                    confidence = float(match.group(1))

            return StepResult(
                status=StepStatus.SUCCESS,
                data=result_text.strip(),
                confidence=confidence,
                tokens_used=tokens,
                duration_ms=duration_ms,
                model_used=model,
            )

        except ImportError:
            context.log_warning("Claude Code SDK not available, simulating agent")
            return StepResult(
                status=StepStatus.SUCCESS,
                data=f"[Simulated] Agent {agent_name} response",
                duration_ms=int((datetime.now() - start_time).total_seconds() * 1000),
            )
        except Exception as e:
            return StepResult(
                status=StepStatus.FAILED,
                error=str(e),
            )

    def _get_model_enum(self, model: str):
        from claude_code_sdk import Model

        model_map = {
            "haiku": Model.CLAUDE_3_5_HAIKU,
            "sonnet": Model.CLAUDE_SONNET_4,
            "opus": Model.CLAUDE_OPUS_4,
        }
        return model_map.get(model.lower(), Model.CLAUDE_SONNET_4)


class ScriptHandler(StepHandler):
    """Executes Python scripts."""

    async def execute(
        self,
        step: StepDefinition,
        context: 'WorkflowContext',
        interpolator: Interpolator,
        model: str,
    ) -> StepResult:
        script_path = interpolator.interpolate(step.script)
        context.log(f"Executing script: {script_path}")

        start_time = datetime.now()
        try:
            # Pass context variables as environment
            import os
            env = os.environ.copy()
            for key, value in context.variables.items():
                env[f"WORKFLOW_{key.upper()}"] = str(value)

            result = subprocess.run(
                [sys.executable, script_path],
                capture_output=True,
                text=True,
                timeout=self._parse_timeout(step.timeout),
                env=env,
            )

            duration_ms = int((datetime.now() - start_time).total_seconds() * 1000)

            if result.returncode != 0:
                return StepResult(
                    status=StepStatus.FAILED,
                    data={"stdout": result.stdout, "stderr": result.stderr},
                    error=f"Script failed: {result.stderr}",
                    duration_ms=duration_ms,
                )

            return StepResult(
                status=StepStatus.SUCCESS,
                data=result.stdout.strip(),
                duration_ms=duration_ms,
            )

        except Exception as e:
            return StepResult(
                status=StepStatus.FAILED,
                error=str(e),
            )

    def _parse_timeout(self, timeout: Optional[str]) -> Optional[float]:
        if not timeout:
            return 300  # Default 5 minutes for scripts

        if timeout.endswith("s"):
            return float(timeout[:-1])
        if timeout.endswith("m"):
            return float(timeout[:-1]) * 60
        if timeout.endswith("h"):
            return float(timeout[:-1]) * 3600

        return float(timeout)


class OutputHandler(StepHandler):
    """Writes output files from templates."""

    async def execute(
        self,
        step: StepDefinition,
        context: 'WorkflowContext',
        interpolator: Interpolator,
        model: str,
    ) -> StepResult:
        output_path = interpolator.resolve_path(step.output)
        template = step.template or ""

        context.log(f"Writing output: {output_path}")

        start_time = datetime.now()
        try:
            # Interpolate template content
            content = interpolator.interpolate(template)

            # Ensure parent directory exists
            output_path.parent.mkdir(parents=True, exist_ok=True)

            # Write file
            output_path.write_text(content, encoding="utf-8")

            duration_ms = int((datetime.now() - start_time).total_seconds() * 1000)

            return StepResult(
                status=StepStatus.SUCCESS,
                data={"path": str(output_path), "size": len(content)},
                duration_ms=duration_ms,
            )

        except Exception as e:
            return StepResult(
                status=StepStatus.FAILED,
                error=str(e),
            )


# ═══════════════════════════════════════════════════════════════
# STEP EXECUTOR
# ═══════════════════════════════════════════════════════════════

class StepExecutor:
    """
    Executes workflow steps.

    Handles:
    - Step type dispatching
    - Condition evaluation
    - Loop execution
    - Error handling
    - Confidence gating
    - Result storage
    """

    def __init__(
        self,
        context: 'WorkflowContext',
        model_selector: Optional[ModelSelector] = None,
    ):
        self.context = context
        self.model_selector = model_selector or ModelSelector()
        self.interpolator = Interpolator(context.get_all())

        # Step handlers by type
        self.handlers: Dict[str, StepHandler] = {
            "bash": BashHandler(),
            "command": CommandHandler(),
            "prompt": PromptHandler(),
            "agent": AgentHandler(),
            "script": ScriptHandler(),
            "output": OutputHandler(),
        }

    async def execute(self, step: StepDefinition) -> StepResult:
        """Execute a single step."""
        self.context.log_step_start(step.name)

        # Update interpolator context
        self.interpolator.set_context(self.context.get_all())

        # Check condition
        if step.condition:
            if not self.interpolator.evaluate_condition(step.condition):
                self.context.log(f"Condition not met: {step.condition}")
                result = StepResult(status=StepStatus.SKIPPED)
                self.context.log_step_end(step.name, result.status)
                return result

        # Handle loop
        if step.loop:
            return await self._execute_loop(step)

        # Handle branch
        if step.branch:
            return await self._execute_branch(step)

        # Select model
        model = self.model_selector.select(step)

        # Get handler
        step_type = step.get_execution_type()
        handler = self.handlers.get(step_type)

        if not handler:
            result = StepResult(
                status=StepStatus.FAILED,
                error=f"Unknown step type: {step_type}",
            )
            self.context.log_step_end(step.name, result.status)
            return result

        # Execute with retry logic
        result = await self._execute_with_retry(step, handler, model)

        # Check confidence gate
        if step.confidence_gate and result.success:
            result = self._check_confidence_gate(step, result)

        # Store result
        if step.store_as and result.success:
            self.context.store(step.store_as, result.data)
            self.context.store_step_result(step.name, result.data)

        self.context.log_step_end(step.name, result.status)
        return result

    async def _execute_with_retry(
        self,
        step: StepDefinition,
        handler: StepHandler,
        model: str,
    ) -> StepResult:
        """Execute step with retry logic."""
        max_retries = step.retry_count or 0
        retry_delay = self._parse_delay(step.retry_delay)

        for attempt in range(max_retries + 1):
            result = await handler.execute(
                step, self.context, self.interpolator, model
            )

            if result.success:
                return result

            if attempt < max_retries:
                self.context.log_warning(
                    f"Step failed, retrying ({attempt + 1}/{max_retries})"
                )
                if retry_delay:
                    await asyncio.sleep(retry_delay)
            else:
                # Handle final failure based on on_error
                return self._handle_error(step, result)

        return result

    def _handle_error(self, step: StepDefinition, result: StepResult) -> StepResult:
        """Handle step error based on on_error setting."""
        if step.on_error == ErrorAction.SKIP:
            result.status = StepStatus.SKIPPED
            self.context.log(f"Skipping failed step: {step.name}")
        elif step.on_error == ErrorAction.CONTINUE:
            self.context.log_warning(f"Continuing after error: {step.name}")
        elif step.on_error == ErrorAction.PAUSE:
            result.status = StepStatus.PAUSED
            self.context.mark_paused()
        # ABORT is default - result stays FAILED

        return result

    def _check_confidence_gate(
        self, step: StepDefinition, result: StepResult
    ) -> StepResult:
        """Check if result meets confidence threshold."""
        if result.confidence is None:
            self.context.log_warning(
                f"No confidence score for gated step: {step.name}"
            )
            return result

        if result.confidence < step.confidence_gate:
            self.context.log_warning(
                f"Confidence {result.confidence}% below gate {step.confidence_gate}%"
            )

            if step.on_low_confidence == LowConfidenceAction.RETRY:
                result.status = StepStatus.FAILED
                result.error = f"Confidence too low: {result.confidence}%"
            elif step.on_low_confidence == LowConfidenceAction.ABORT:
                result.status = StepStatus.FAILED
                result.error = f"Confidence gate failed: {result.confidence}%"
            elif step.on_low_confidence == LowConfidenceAction.MANUAL_REVIEW:
                result.status = StepStatus.PAUSED
                self.context.mark_paused()
                self.context.log(
                    f"Manual review required: confidence {result.confidence}%"
                )

        return result

    async def _execute_loop(self, step: StepDefinition) -> StepResult:
        """Execute step in a loop."""
        loop_items = self.interpolator._resolve(step.loop)

        if not isinstance(loop_items, (list, tuple)):
            return StepResult(
                status=StepStatus.FAILED,
                error=f"Loop expression must resolve to list: {step.loop}",
            )

        loop_var = step.loop_as or "item"
        results = []

        for i, item in enumerate(loop_items):
            self.context.log(f"Loop iteration {i + 1}/{len(loop_items)}")

            # Add loop variable to context
            self.context.store(loop_var, item)
            self.context.store("loop_index", i)
            self.interpolator.set_context(self.context.get_all())

            # Create a copy of step without loop to execute
            step_copy = StepDefinition(
                name=f"{step.name}[{i}]",
                description=step.description,
                command=step.command,
                prompt=step.prompt,
                bash=step.bash,
                agent=step.agent,
                framework=step.framework,
                script=step.script,
                condition=step.condition,
                store_as=None,  # Don't store individual results
                model=step.model,
                on_error=step.on_error,
                timeout=step.timeout,
            )

            result = await self.execute(step_copy)
            results.append(result.data)

            if not result.success and step.on_error == ErrorAction.ABORT:
                return StepResult(
                    status=StepStatus.FAILED,
                    data=results,
                    error=f"Loop failed at iteration {i}",
                )

        return StepResult(
            status=StepStatus.SUCCESS,
            data=results,
        )

    async def _execute_branch(self, step: StepDefinition) -> StepResult:
        """Execute branching logic."""
        for branch in step.branch:
            if self.interpolator.evaluate_condition(branch.condition):
                self.context.log(f"Branch matched: {branch.condition}")

                # Execute branch steps
                for branch_step in branch.steps:
                    result = await self.execute(branch_step)
                    if not result.success and step.on_error == ErrorAction.ABORT:
                        return result

                return StepResult(
                    status=StepStatus.SUCCESS,
                    data={"branch": branch.condition},
                )

        # No branch matched
        self.context.log("No branch condition matched")
        return StepResult(status=StepStatus.SKIPPED)

    def _parse_delay(self, delay: Optional[str]) -> Optional[float]:
        """Parse delay string to seconds."""
        if not delay:
            return None

        if delay.endswith("s"):
            return float(delay[:-1])
        if delay.endswith("m"):
            return float(delay[:-1]) * 60

        return float(delay)
