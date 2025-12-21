"""
Workflow Engine - Trigger System

Handles cron, file watch, and event-based workflow triggers.
"""

import asyncio
import json
import re
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Set

from workflows.engine.models import TriggerConfig, TriggerType
from workflows.engine.parser import load_workflow, list_workflows


# ═══════════════════════════════════════════════════════════════
# TRIGGER BASE
# ═══════════════════════════════════════════════════════════════

@dataclass
class TriggerEvent:
    """Event that triggered a workflow."""
    trigger_type: TriggerType
    workflow_name: str
    timestamp: datetime
    data: Dict[str, Any] = field(default_factory=dict)


class TriggerHandler(ABC):
    """Base class for trigger handlers."""

    @abstractmethod
    async def start(self):
        """Start the trigger handler."""
        pass

    @abstractmethod
    async def stop(self):
        """Stop the trigger handler."""
        pass

    @abstractmethod
    def register(self, workflow_name: str, config: TriggerConfig):
        """Register a workflow for this trigger type."""
        pass


# ═══════════════════════════════════════════════════════════════
# CRON SCHEDULER
# ═══════════════════════════════════════════════════════════════

@dataclass
class CronJob:
    """A scheduled cron job."""
    workflow_name: str
    cron_expression: str
    next_run: Optional[datetime] = None
    last_run: Optional[datetime] = None
    enabled: bool = True


class CronScheduler(TriggerHandler):
    """
    Cron-based workflow scheduler.

    Supports standard cron expressions:
    - "0 9 * * 1" - Every Monday at 9:00
    - "0 8 * * *" - Every day at 8:00
    - "*/30 * * * *" - Every 30 minutes
    """

    def __init__(self, on_trigger: Callable[[TriggerEvent], None]):
        self.on_trigger = on_trigger
        self.jobs: Dict[str, CronJob] = {}
        self._running = False
        self._task: Optional[asyncio.Task] = None

    async def start(self):
        """Start the cron scheduler."""
        self._running = True
        self._task = asyncio.create_task(self._run_loop())

    async def stop(self):
        """Stop the cron scheduler."""
        self._running = False
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass

    def register(self, workflow_name: str, config: TriggerConfig):
        """Register a workflow with cron trigger."""
        if config.type != TriggerType.CRON or not config.cron:
            return

        job = CronJob(
            workflow_name=workflow_name,
            cron_expression=config.cron,
        )
        job.next_run = self._calculate_next_run(config.cron)
        self.jobs[workflow_name] = job

    async def _run_loop(self):
        """Main scheduler loop."""
        while self._running:
            now = datetime.now()

            for job in self.jobs.values():
                if not job.enabled or not job.next_run:
                    continue

                if now >= job.next_run:
                    # Trigger workflow
                    event = TriggerEvent(
                        trigger_type=TriggerType.CRON,
                        workflow_name=job.workflow_name,
                        timestamp=now,
                        data={"cron": job.cron_expression},
                    )
                    self.on_trigger(event)

                    # Update job
                    job.last_run = now
                    job.next_run = self._calculate_next_run(job.cron_expression)

            # Sleep until next check
            await asyncio.sleep(60)  # Check every minute

    def _calculate_next_run(self, cron_expression: str) -> datetime:
        """Calculate next run time from cron expression."""
        try:
            from croniter import croniter
            return croniter(cron_expression, datetime.now()).get_next(datetime)
        except ImportError:
            # Fallback: simple parsing for common patterns
            return self._simple_next_run(cron_expression)

    def _simple_next_run(self, cron_expression: str) -> datetime:
        """Simple next run calculation without croniter."""
        parts = cron_expression.split()
        if len(parts) != 5:
            return datetime.now()

        minute, hour, day, month, weekday = parts
        now = datetime.now()

        # Very basic: just add 1 day for daily schedules
        next_run = now.replace(second=0, microsecond=0)

        if hour != "*":
            next_run = next_run.replace(hour=int(hour))
        if minute != "*":
            next_run = next_run.replace(minute=int(minute))

        if next_run <= now:
            next_run = next_run.replace(day=next_run.day + 1)

        return next_run

    def get_schedule(self) -> List[Dict[str, Any]]:
        """Get current schedule."""
        return [
            {
                "workflow": job.workflow_name,
                "cron": job.cron_expression,
                "next_run": job.next_run.isoformat() if job.next_run else None,
                "last_run": job.last_run.isoformat() if job.last_run else None,
                "enabled": job.enabled,
            }
            for job in self.jobs.values()
        ]


# ═══════════════════════════════════════════════════════════════
# FILE WATCHER
# ═══════════════════════════════════════════════════════════════

@dataclass
class WatchConfig:
    """Configuration for file watching."""
    workflow_name: str
    pattern: str
    debounce_ms: int = 1000


class FileWatcher(TriggerHandler):
    """
    File system watcher for triggering workflows on file changes.

    Supports glob patterns:
    - "_inbox/*" - Any file in _inbox
    - "ideas/**/*.md" - Any markdown in ideas tree
    """

    def __init__(self, on_trigger: Callable[[TriggerEvent], None]):
        self.on_trigger = on_trigger
        self.watches: Dict[str, WatchConfig] = {}
        self._running = False
        self._task: Optional[asyncio.Task] = None
        self._last_changes: Dict[str, datetime] = {}

    async def start(self):
        """Start the file watcher."""
        self._running = True
        self._task = asyncio.create_task(self._watch_loop())

    async def stop(self):
        """Stop the file watcher."""
        self._running = False
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass

    def register(self, workflow_name: str, config: TriggerConfig):
        """Register a workflow with watch trigger."""
        if config.type != TriggerType.WATCH or not config.watch:
            return

        self.watches[workflow_name] = WatchConfig(
            workflow_name=workflow_name,
            pattern=config.watch,
        )

    async def _watch_loop(self):
        """Main watcher loop using polling."""
        # Track file modification times
        file_mtimes: Dict[str, float] = {}

        while self._running:
            for watch in self.watches.values():
                try:
                    # Find matching files
                    pattern_path = Path(watch.pattern)
                    if pattern_path.is_absolute():
                        base = pattern_path.parent
                        glob_pattern = pattern_path.name
                    else:
                        base = Path(".")
                        glob_pattern = watch.pattern

                    for file_path in base.glob(glob_pattern):
                        if not file_path.is_file():
                            continue

                        mtime = file_path.stat().st_mtime
                        path_key = str(file_path)

                        if path_key in file_mtimes:
                            if mtime > file_mtimes[path_key]:
                                # File changed
                                await self._handle_change(watch, file_path)

                        file_mtimes[path_key] = mtime

                except Exception:
                    pass

            await asyncio.sleep(2)  # Poll every 2 seconds

    async def _handle_change(self, watch: WatchConfig, file_path: Path):
        """Handle a file change."""
        # Debounce
        now = datetime.now()
        key = f"{watch.workflow_name}:{file_path}"

        if key in self._last_changes:
            elapsed = (now - self._last_changes[key]).total_seconds() * 1000
            if elapsed < watch.debounce_ms:
                return

        self._last_changes[key] = now

        # Trigger
        event = TriggerEvent(
            trigger_type=TriggerType.WATCH,
            workflow_name=watch.workflow_name,
            timestamp=now,
            data={
                "file": str(file_path),
                "pattern": watch.pattern,
            },
        )
        self.on_trigger(event)


# ═══════════════════════════════════════════════════════════════
# EVENT BUS
# ═══════════════════════════════════════════════════════════════

@dataclass
class EventSubscription:
    """A subscription to an event."""
    workflow_name: str
    event_pattern: str


class EventBus(TriggerHandler):
    """
    Event-based workflow triggering.

    Events:
    - "idea.created" - New idea created
    - "knowledge.updated" - KB updated
    - "workflow.completed" - Workflow finished
    """

    def __init__(self, on_trigger: Callable[[TriggerEvent], None]):
        self.on_trigger = on_trigger
        self.subscriptions: Dict[str, List[EventSubscription]] = {}
        self._running = False

    async def start(self):
        """Start the event bus."""
        self._running = True

    async def stop(self):
        """Stop the event bus."""
        self._running = False

    def register(self, workflow_name: str, config: TriggerConfig):
        """Register a workflow with event trigger."""
        if config.type != TriggerType.EVENT or not config.event:
            return

        event_pattern = config.event
        if event_pattern not in self.subscriptions:
            self.subscriptions[event_pattern] = []

        self.subscriptions[event_pattern].append(EventSubscription(
            workflow_name=workflow_name,
            event_pattern=event_pattern,
        ))

    def emit(self, event_name: str, data: Optional[Dict[str, Any]] = None):
        """Emit an event."""
        if not self._running:
            return

        now = datetime.now()

        # Check exact matches
        if event_name in self.subscriptions:
            for sub in self.subscriptions[event_name]:
                event = TriggerEvent(
                    trigger_type=TriggerType.EVENT,
                    workflow_name=sub.workflow_name,
                    timestamp=now,
                    data={"event": event_name, **(data or {})},
                )
                self.on_trigger(event)

        # Check wildcard matches
        for pattern, subs in self.subscriptions.items():
            if "*" in pattern:
                regex = pattern.replace(".", r"\.").replace("*", ".*")
                if re.match(regex, event_name):
                    for sub in subs:
                        event = TriggerEvent(
                            trigger_type=TriggerType.EVENT,
                            workflow_name=sub.workflow_name,
                            timestamp=now,
                            data={"event": event_name, **(data or {})},
                        )
                        self.on_trigger(event)


# ═══════════════════════════════════════════════════════════════
# TRIGGER MANAGER
# ═══════════════════════════════════════════════════════════════

class TriggerManager:
    """
    Central manager for all trigger types.

    Usage:
        manager = TriggerManager()
        manager.register_all_workflows()
        await manager.start()

        # Later...
        manager.event_bus.emit("idea.created", {"id": "idea-2024-001"})
    """

    def __init__(self, on_trigger: Optional[Callable[[TriggerEvent], None]] = None):
        self._trigger_queue: asyncio.Queue = asyncio.Queue()
        self._on_trigger = on_trigger or self._default_handler

        # Initialize handlers
        self.cron_scheduler = CronScheduler(self._handle_trigger)
        self.file_watcher = FileWatcher(self._handle_trigger)
        self.event_bus = EventBus(self._handle_trigger)

        self._running = False
        self._processor_task: Optional[asyncio.Task] = None

    def _handle_trigger(self, event: TriggerEvent):
        """Handle a trigger event."""
        self._trigger_queue.put_nowait(event)

    async def _default_handler(self, event: TriggerEvent):
        """Default trigger handler - runs the workflow."""
        from workflows.engine import WorkflowRunner

        runner = WorkflowRunner()

        # Add trigger data as variables
        variables = event.data.copy()
        variables["_trigger_type"] = event.trigger_type.value
        variables["_trigger_time"] = event.timestamp.isoformat()

        await runner.run(event.workflow_name, variables=variables)

    async def start(self):
        """Start all trigger handlers."""
        self._running = True

        # Start handlers
        await self.cron_scheduler.start()
        await self.file_watcher.start()
        await self.event_bus.start()

        # Start processor
        self._processor_task = asyncio.create_task(self._process_triggers())

    async def stop(self):
        """Stop all trigger handlers."""
        self._running = False

        await self.cron_scheduler.stop()
        await self.file_watcher.stop()
        await self.event_bus.stop()

        if self._processor_task:
            self._processor_task.cancel()
            try:
                await self._processor_task
            except asyncio.CancelledError:
                pass

    async def _process_triggers(self):
        """Process trigger events from queue."""
        while self._running:
            try:
                event = await asyncio.wait_for(
                    self._trigger_queue.get(),
                    timeout=1.0
                )
                await self._on_trigger(event)
            except asyncio.TimeoutError:
                continue
            except Exception as e:
                # Log error but continue
                print(f"Trigger processing error: {e}")

    def register_workflow(self, workflow_name: str):
        """Register a single workflow's triggers."""
        workflow = load_workflow(workflow_name)

        if workflow.trigger.type == TriggerType.CRON:
            self.cron_scheduler.register(workflow_name, workflow.trigger)
        elif workflow.trigger.type == TriggerType.WATCH:
            self.file_watcher.register(workflow_name, workflow.trigger)
        elif workflow.trigger.type == TriggerType.EVENT:
            self.event_bus.register(workflow_name, workflow.trigger)

    def register_all_workflows(self):
        """Register all workflows from definitions."""
        for name in list_workflows():
            try:
                self.register_workflow(name)
            except Exception as e:
                print(f"Failed to register {name}: {e}")

    def get_status(self) -> Dict[str, Any]:
        """Get trigger system status."""
        return {
            "running": self._running,
            "cron_jobs": len(self.cron_scheduler.jobs),
            "file_watches": len(self.file_watcher.watches),
            "event_subscriptions": sum(
                len(subs) for subs in self.event_bus.subscriptions.values()
            ),
            "schedule": self.cron_scheduler.get_schedule(),
        }


# ═══════════════════════════════════════════════════════════════
# DAEMON
# ═══════════════════════════════════════════════════════════════

class WorkflowDaemon:
    """
    Background daemon for running scheduled workflows.

    Usage:
        daemon = WorkflowDaemon()
        await daemon.start()

        # In another process/terminal:
        # Check status via API or PID file
    """

    PID_FILE = Path("workflows/.daemon.pid")
    STATUS_FILE = Path("workflows/.daemon.status")

    def __init__(self):
        self.trigger_manager = TriggerManager()
        self._running = False

    async def start(self):
        """Start the daemon."""
        # Write PID file
        self.PID_FILE.parent.mkdir(parents=True, exist_ok=True)
        self.PID_FILE.write_text(str(asyncio.current_task()))

        self._running = True
        self._update_status("running")

        # Register workflows
        self.trigger_manager.register_all_workflows()

        # Start trigger manager
        await self.trigger_manager.start()

        # Keep running
        try:
            while self._running:
                self._update_status("running")
                await asyncio.sleep(60)
        finally:
            await self.trigger_manager.stop()
            self._cleanup()

    async def stop(self):
        """Stop the daemon."""
        self._running = False
        await self.trigger_manager.stop()

    def _update_status(self, status: str):
        """Update status file."""
        status_data = {
            "status": status,
            "timestamp": datetime.now().isoformat(),
            **self.trigger_manager.get_status(),
        }
        self.STATUS_FILE.write_text(json.dumps(status_data, indent=2))

    def _cleanup(self):
        """Clean up files on shutdown."""
        if self.PID_FILE.exists():
            self.PID_FILE.unlink()
        self._update_status("stopped")

    @classmethod
    def is_running(cls) -> bool:
        """Check if daemon is running."""
        if not cls.STATUS_FILE.exists():
            return False

        try:
            data = json.loads(cls.STATUS_FILE.read_text())
            return data.get("status") == "running"
        except Exception:
            return False

    @classmethod
    def get_status(cls) -> Optional[Dict[str, Any]]:
        """Get daemon status."""
        if not cls.STATUS_FILE.exists():
            return None

        try:
            return json.loads(cls.STATUS_FILE.read_text())
        except Exception:
            return None


# ═══════════════════════════════════════════════════════════════
# CONVENIENCE FUNCTIONS
# ═══════════════════════════════════════════════════════════════

async def run_daemon():
    """Start the workflow daemon."""
    daemon = WorkflowDaemon()
    await daemon.start()


def emit_event(event_name: str, data: Optional[Dict[str, Any]] = None):
    """Emit an event (requires running daemon)."""
    # Write to event queue file for daemon to pick up
    events_dir = Path("workflows/.events")
    events_dir.mkdir(parents=True, exist_ok=True)

    event_file = events_dir / f"{datetime.now().strftime('%Y%m%d%H%M%S%f')}.json"
    event_file.write_text(json.dumps({
        "name": event_name,
        "data": data or {},
        "timestamp": datetime.now().isoformat(),
    }))
