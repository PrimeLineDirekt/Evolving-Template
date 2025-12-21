"""
Workflow Engine - FastAPI Service

REST API and WebSocket endpoints for workflow management.
"""

import asyncio
import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from workflows.engine import (
    WorkflowRunner,
    load_workflow,
    list_workflows,
    WorkflowContext,
    StepStatus,
)
from workflows.engine.audit import AuditLogger


# ═══════════════════════════════════════════════════════════════
# FASTAPI APP
# ═══════════════════════════════════════════════════════════════

app = FastAPI(
    title="Workflow Engine API",
    description="AI-nativer Workflow-Orchestrator für das Evolving-System",
    version="0.1.0",
)

# CORS for Dashboard
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Active workflow runs
active_runs: Dict[str, Dict[str, Any]] = {}


# ═══════════════════════════════════════════════════════════════
# REQUEST/RESPONSE MODELS
# ═══════════════════════════════════════════════════════════════

class WorkflowRunRequest(BaseModel):
    variables: Optional[Dict[str, Any]] = None
    dry_run: bool = False


class WorkflowRunResponse(BaseModel):
    run_id: str
    workflow_name: str
    status: str
    started_at: str
    message: str


class WorkflowStatusResponse(BaseModel):
    run_id: str
    workflow_name: str
    status: str
    current_step: int
    total_steps: int
    progress_percent: float
    tokens_used: int
    cost: float
    started_at: str
    completed_at: Optional[str]
    error: Optional[str]


class WorkflowListItem(BaseModel):
    name: str
    description: str
    version: str
    trigger_type: str
    steps_count: int
    permissions_profile: str
    preferences_profile: str


class StepResult(BaseModel):
    name: str
    status: str
    duration_ms: Optional[int]
    tokens_used: Optional[int]
    error: Optional[str]


class WorkflowResultResponse(BaseModel):
    run_id: str
    workflow_name: str
    status: str
    started_at: str
    completed_at: Optional[str]
    duration_seconds: float
    total_tokens: int
    total_cost: float
    steps: List[StepResult]
    variables: Dict[str, Any]
    error: Optional[str]


# ═══════════════════════════════════════════════════════════════
# WORKFLOW ENDPOINTS
# ═══════════════════════════════════════════════════════════════

@app.get("/api/workflows", response_model=List[WorkflowListItem])
async def get_workflows():
    """List all available workflows."""
    workflows = []
    for name in list_workflows():
        try:
            workflow = load_workflow(name)
            workflows.append(WorkflowListItem(
                name=workflow.name,
                description=workflow.description,
                version=workflow.version,
                trigger_type=workflow.trigger.type.value,
                steps_count=len(workflow.steps),
                permissions_profile=workflow.permissions_profile,
                preferences_profile=workflow.preferences_profile,
            ))
        except Exception as e:
            # Include errored workflows with error info
            workflows.append(WorkflowListItem(
                name=name,
                description=f"Error: {str(e)}",
                version="unknown",
                trigger_type="unknown",
                steps_count=0,
                permissions_profile="unknown",
                preferences_profile="unknown",
            ))

    return workflows


@app.get("/api/workflows/{name}")
async def get_workflow(name: str):
    """Get workflow details."""
    try:
        workflow = load_workflow(name)
        return {
            "name": workflow.name,
            "description": workflow.description,
            "version": workflow.version,
            "trigger": {
                "type": workflow.trigger.type.value,
                "cron": workflow.trigger.cron,
                "watch": workflow.trigger.watch,
                "event": workflow.trigger.event,
            },
            "permissions_profile": workflow.permissions_profile,
            "preferences_profile": workflow.preferences_profile,
            "variables": [
                {
                    "name": v.name,
                    "type": v.type,
                    "default": v.default,
                    "required": v.required,
                    "prompt": v.prompt,
                }
                for v in workflow.variables
            ],
            "steps": [
                {
                    "name": s.name,
                    "description": s.description,
                    "type": s.get_execution_type(),
                    "model": s.model.value,
                    "condition": s.condition,
                }
                for s in workflow.steps
            ],
            "settings": {
                "on_error": workflow.settings.on_error.value,
                "max_steps": workflow.settings.max_steps,
                "timeout": workflow.settings.timeout,
            },
            "budget": {
                "max_tokens": workflow.budget.max_tokens if workflow.budget else None,
                "max_cost": workflow.budget.max_cost if workflow.budget else None,
            } if workflow.budget else None,
        }
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.post("/api/workflows/{name}/run", response_model=WorkflowRunResponse)
async def run_workflow(name: str, request: WorkflowRunRequest):
    """Start a workflow execution."""
    try:
        workflow = load_workflow(name)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

    runner = WorkflowRunner()

    # Generate run ID
    context = WorkflowContext(workflow_name=name)
    run_id = context.run_id

    # Store run info
    active_runs[run_id] = {
        "workflow_name": name,
        "status": "starting",
        "context": context,
        "started_at": datetime.now().isoformat(),
    }

    # Start execution in background
    asyncio.create_task(_execute_workflow(runner, name, run_id, request))

    return WorkflowRunResponse(
        run_id=run_id,
        workflow_name=name,
        status="starting",
        started_at=active_runs[run_id]["started_at"],
        message="Workflow execution started",
    )


async def _execute_workflow(
    runner: WorkflowRunner,
    name: str,
    run_id: str,
    request: WorkflowRunRequest,
):
    """Background task to execute workflow."""
    try:
        active_runs[run_id]["status"] = "running"

        if request.dry_run:
            result = await runner.dry_run(name, variables=request.variables)
        else:
            result = await runner.run(name, variables=request.variables)

        active_runs[run_id]["status"] = result.status.value
        active_runs[run_id]["result"] = result
        active_runs[run_id]["completed_at"] = datetime.now().isoformat()

    except Exception as e:
        active_runs[run_id]["status"] = "failed"
        active_runs[run_id]["error"] = str(e)
        active_runs[run_id]["completed_at"] = datetime.now().isoformat()


@app.get("/api/workflows/{name}/runs/{run_id}", response_model=WorkflowStatusResponse)
async def get_run_status(name: str, run_id: str):
    """Get status of a workflow run."""
    if run_id not in active_runs:
        # Try to load from logs
        log_path = Path(f"workflows/logs/{name}-{run_id}.json")
        if log_path.exists():
            log_data = json.loads(log_path.read_text())
            return WorkflowStatusResponse(
                run_id=run_id,
                workflow_name=name,
                status=log_data.get("status", "unknown"),
                current_step=len(log_data.get("step_results", {})),
                total_steps=len(log_data.get("step_results", {})),
                progress_percent=100.0,
                tokens_used=log_data.get("total_tokens", 0),
                cost=log_data.get("total_cost", 0.0),
                started_at=log_data.get("started_at", ""),
                completed_at=log_data.get("completed_at"),
                error=log_data.get("error"),
            )
        raise HTTPException(status_code=404, detail="Run not found")

    run = active_runs[run_id]
    context = run.get("context")
    result = run.get("result")

    if result:
        total_steps = len(result.step_results)
        current_step = total_steps
        progress = 100.0
    elif context:
        workflow = load_workflow(name)
        total_steps = len(workflow.steps)
        current_step = context.current_step
        progress = (current_step / total_steps * 100) if total_steps > 0 else 0
    else:
        total_steps = 0
        current_step = 0
        progress = 0

    return WorkflowStatusResponse(
        run_id=run_id,
        workflow_name=name,
        status=run["status"],
        current_step=current_step,
        total_steps=total_steps,
        progress_percent=progress,
        tokens_used=result.total_tokens if result else (context.token_usage if context else 0),
        cost=result.total_cost if result else (context.cost if context else 0.0),
        started_at=run["started_at"],
        completed_at=run.get("completed_at"),
        error=run.get("error"),
    )


@app.get("/api/workflows/{name}/runs/{run_id}/result", response_model=WorkflowResultResponse)
async def get_run_result(name: str, run_id: str):
    """Get full result of a completed workflow run."""
    # First check active runs
    if run_id in active_runs:
        run = active_runs[run_id]
        result = run.get("result")

        if not result:
            raise HTTPException(status_code=400, detail="Run not completed yet")

        steps = []
        for step_name, step_data in result.step_results.items():
            steps.append(StepResult(
                name=step_name,
                status="success",
                duration_ms=None,
                tokens_used=None,
                error=None,
            ))

        return WorkflowResultResponse(
            run_id=run_id,
            workflow_name=name,
            status=result.status.value,
            started_at=result.started_at.isoformat(),
            completed_at=result.completed_at.isoformat() if result.completed_at else None,
            duration_seconds=result.duration_seconds,
            total_tokens=result.total_tokens,
            total_cost=result.total_cost,
            steps=steps,
            variables=result.variables,
            error=result.error,
        )

    # Try to load from logs
    log_path = Path(f"workflows/logs/{name}-{run_id}.json")
    if log_path.exists():
        log_data = json.loads(log_path.read_text())

        steps = []
        for step_name in log_data.get("step_results", {}).keys():
            steps.append(StepResult(
                name=step_name,
                status="success",
                duration_ms=None,
                tokens_used=None,
                error=None,
            ))

        return WorkflowResultResponse(
            run_id=run_id,
            workflow_name=name,
            status=log_data.get("status", "unknown"),
            started_at=log_data.get("started_at", ""),
            completed_at=log_data.get("completed_at"),
            duration_seconds=log_data.get("duration_seconds", 0),
            total_tokens=log_data.get("total_tokens", 0),
            total_cost=log_data.get("total_cost", 0.0),
            steps=steps,
            variables=log_data.get("variables", {}),
            error=log_data.get("error"),
        )

    raise HTTPException(status_code=404, detail="Run not found")


@app.delete("/api/workflows/{name}/runs/{run_id}")
async def stop_run(name: str, run_id: str):
    """Stop a running workflow."""
    if run_id not in active_runs:
        raise HTTPException(status_code=404, detail="Run not found")

    run = active_runs[run_id]

    if run["status"] not in ("starting", "running"):
        raise HTTPException(status_code=400, detail="Run is not active")

    # Mark as stopped
    run["status"] = "stopped"
    run["completed_at"] = datetime.now().isoformat()

    # TODO: Actually cancel the asyncio task

    return {"message": "Run stopped", "run_id": run_id}


# ═══════════════════════════════════════════════════════════════
# WEBSOCKET FOR LIVE STREAMING
# ═══════════════════════════════════════════════════════════════

@app.websocket("/api/workflows/{name}/stream")
async def workflow_stream(websocket: WebSocket, name: str, run_id: Optional[str] = Query(None)):
    """WebSocket for live workflow output streaming."""
    await websocket.accept()

    if not run_id or run_id not in active_runs:
        await websocket.send_json({"error": "Run not found"})
        await websocket.close()
        return

    run = active_runs[run_id]
    last_step = -1

    try:
        while True:
            context = run.get("context")

            if context and context.current_step > last_step:
                # Send step update
                await websocket.send_json({
                    "type": "step_update",
                    "step": context.current_step,
                    "step_name": context.current_step_name,
                    "status": run["status"],
                    "tokens": context.token_usage,
                    "cost": context.cost,
                })
                last_step = context.current_step

            # Send log updates
            if context and context.logs:
                recent_logs = context.logs[-5:]
                for log in recent_logs:
                    await websocket.send_json({
                        "type": "log",
                        "level": log.type.value,
                        "message": log.message,
                        "step": log.step,
                        "timestamp": log.timestamp.isoformat(),
                    })

            # Check if complete
            if run["status"] in ("success", "failed", "stopped", "paused"):
                result = run.get("result")
                await websocket.send_json({
                    "type": "complete",
                    "status": run["status"],
                    "tokens": result.total_tokens if result else 0,
                    "cost": result.total_cost if result else 0.0,
                    "error": run.get("error"),
                })
                break

            await asyncio.sleep(0.5)

    except WebSocketDisconnect:
        pass


# ═══════════════════════════════════════════════════════════════
# RUN HISTORY
# ═══════════════════════════════════════════════════════════════

@app.get("/api/workflows/{name}/runs")
async def get_run_history(
    name: str,
    limit: int = Query(default=20, le=100),
):
    """Get run history for a workflow."""
    logs_dir = Path("workflows/logs")
    runs = []

    if logs_dir.exists():
        for log_file in sorted(logs_dir.glob(f"{name}-*.json"), reverse=True)[:limit]:
            try:
                data = json.loads(log_file.read_text())
                runs.append({
                    "run_id": data.get("run_id", log_file.stem.split("-", 1)[1]),
                    "status": data.get("status", "unknown"),
                    "started_at": data.get("started_at", ""),
                    "completed_at": data.get("completed_at"),
                    "duration_seconds": data.get("duration_seconds", 0),
                    "total_tokens": data.get("total_tokens", 0),
                    "total_cost": data.get("total_cost", 0.0),
                })
            except Exception:
                pass

    return runs


# ═══════════════════════════════════════════════════════════════
# AUDIT LOGS
# ═══════════════════════════════════════════════════════════════

@app.get("/api/workflows/{name}/runs/{run_id}/audit")
async def get_audit_log(name: str, run_id: str):
    """Get audit log for a run."""
    audit_path = Path(f"workflows/logs/{name}-{run_id}.audit.json")

    if not audit_path.exists():
        raise HTTPException(status_code=404, detail="Audit log not found")

    try:
        logger = AuditLogger.load(audit_path)
        summary = logger.get_summary()

        return {
            "summary": {
                "workflow_name": summary.workflow_name,
                "run_id": summary.run_id,
                "status": summary.status,
                "started_at": summary.started_at,
                "completed_at": summary.completed_at,
                "duration_seconds": summary.duration_seconds,
                "total_entries": summary.total_entries,
                "steps_completed": summary.steps_completed,
                "steps_failed": summary.steps_failed,
                "tool_calls": summary.tool_calls,
                "errors": summary.errors,
                "tokens_used": summary.tokens_used,
                "cost": summary.cost,
                "integrity_valid": summary.integrity_valid,
            },
            "entries": [e.to_dict() for e in logger.entries],
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ═══════════════════════════════════════════════════════════════
# HEALTH CHECK
# ═══════════════════════════════════════════════════════════════

@app.get("/api/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "version": "0.1.0",
        "workflows_available": len(list_workflows()),
        "active_runs": len([r for r in active_runs.values() if r["status"] == "running"]),
    }


# ═══════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
