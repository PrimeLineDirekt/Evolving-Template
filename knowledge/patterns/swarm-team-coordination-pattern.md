# Swarm / Team Coordination Pattern

> **Source**: Piebald-AI/claude-code-system-prompts (v2.0.60)
> **Type**: Multi-Agent Orchestration Pattern
> **Status**: Claude Code Native Feature (ExitPlanMode with Swarm)

## Konzept

Koordinierte Team-Workflows mit mehreren Worker-Agents, die parallel an Tasks arbeiten. Ein Team-Lead koordiniert, verteilt Arbeit und aggregiert Ergebnisse.

## Architektur

```
                    ┌─────────────────┐
                    │   Team-Lead     │
                    │  (Coordinator)  │
                    └────────┬────────┘
                             │
              ┌──────────────┼──────────────┐
              │              │              │
       ┌──────▼──────┐ ┌─────▼─────┐ ┌──────▼──────┐
       │  Worker 1   │ │ Worker 2  │ │  Worker 3   │
       │  (Task A)   │ │ (Task B)  │ │  (Task C)   │
       └──────┬──────┘ └─────┬─────┘ └──────┬──────┘
              │              │              │
              └──────────────┼──────────────┘
                             │
                    ┌────────▼────────┐
                    │   Aggregated    │
                    │    Results      │
                    └─────────────────┘
```

## 5-Phasen-Workflow

### Phase 1: Task Creation
```
Plan parsen → Discrete Tasks extrahieren

TaskCreateTool({
  subject: "Implement user authentication",
  description: "Create login/logout endpoints with JWT"
})
```

### Phase 2: Team Establishment
```
TeammateTool({
  operation: "spawnTeam",
  teamName: "plan-implementation"
})
```

### Phase 3: Worker Deployment
```
Für jeden Worker:
TeammateTool({
  operation: "spawn",
  type: "worker",
  team: "plan-implementation"
})
```

### Phase 4: Work Distribution
```
Für jeden Task:
TeammateTool({
  operation: "assignTask",
  worker: "worker-1",
  task: "task-id-123"
})
```

### Phase 5: Results Synthesis
```
Team-Lead:
1. Monitor Progress (Task Status)
2. Collect Findings (von jedem Worker)
3. Aggregate Results
4. Report: Accomplishments, Obstacles, Next Actions
```

## Team Coordination Protocol

### Naming Convention
```
WICHTIG: Immer Namen verwenden, NIEMALS UUIDs!

✓ "team-lead", "analyzer", "researcher"
✗ "agent-uuid-12345-abcde"
```

### Communication
```
Team-Lead ←→ Workers via:
- Task Assignments
- Progress Updates
- Result Submissions
- Status Queries
```

### Shared Resources
```
_team/
├── config.json       # Team-Konfiguration
├── tasks.json        # Task-Liste mit Status
└── results/          # Aggregierte Ergebnisse
```

## Use Cases

### 1. Parallel Code Review
```
Team-Lead: Code Review Coordinator
Worker 1: Security Reviewer
Worker 2: Performance Reviewer
Worker 3: Code Quality Reviewer
→ Aggregated Review Report
```

### 2. Research Task
```
Team-Lead: Research Coordinator
Worker 1: Academic Sources
Worker 2: Industry Sources
Worker 3: Community/Forums
→ Synthesized Research Report
```

### 3. Feature Implementation
```
Team-Lead: Implementation Coordinator
Worker 1: Backend Development
Worker 2: Frontend Development
Worker 3: Testing
→ Integrated Feature
```

### 4. Documentation
```
Team-Lead: Documentation Coordinator
Worker 1: API Documentation
Worker 2: User Guides
Worker 3: Architecture Docs
→ Complete Documentation Set
```

## Integration mit Evolving

### Möglicher Blueprint: `parallel-workers`

```json
{
  "name": "parallel-workers",
  "description": "Parallel Task Execution mit Worker Team",
  "structure": {
    "team_lead": {
      "role": "coordinator",
      "model": "opus"
    },
    "workers": {
      "count": "dynamic",
      "model": "sonnet",
      "specialization": "task-based"
    }
  },
  "workflow": [
    "task_decomposition",
    "worker_spawn",
    "parallel_execution",
    "result_aggregation"
  ]
}
```

### Unterschied zu unserem Multi-Agent System

| Unser System | Swarm Pattern |
|--------------|---------------|
| Sequential Orchestration | Parallel Execution |
| Agent → Agent → Agent | Team-Lead → [Workers] → Aggregation |
| Spezialisierte Agents | Generische Workers mit Task Assignment |
| Statische Konfiguration | Dynamisches Spawning |

### Wann Swarm nutzen?

- Tasks sind unabhängig voneinander
- Parallelisierung spart Zeit
- Ergebnisse müssen aggregiert werden
- Workload ist aufteilbar

### Wann NICHT Swarm nutzen?

- Tasks haben Dependencies
- Sequentielle Ausführung nötig
- Single-Expert besser (z.B. Deep Analysis)
- Overhead der Koordination > Parallelisierungsgewinn

## Implementierung (Konzept)

### ExitPlanMode mit Swarm

```typescript
ExitPlanMode({
  launchSwarm: true,
  teammateCount: 3
})
```

### TaskUpdate Tool

Ermöglicht dynamische Task-Updates während Ausführung:

```typescript
TaskUpdate({
  taskId: "task-123",
  status: "in_progress" | "completed" | "blocked",
  progress: "50%",
  notes: "Waiting for API response"
})
```

## Zukünftige Evolving Integration

1. **Blueprint erstellen**: `parallel-workers.json`
2. **TeammateTool simulieren**: Via parallel Task Agents
3. **Result Aggregation Pattern**: Gemeinsamer Output-Merge

---

## Related

- [Multi-Agent Orchestration Pattern](multi-agent-orchestration-pattern.md)
- [Blackboard Pattern](blackboard-pattern.md)
- `.claude/blueprints/` - System Blueprints
