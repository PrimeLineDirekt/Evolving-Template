# Domain Memory Schema

**Version**: 1.0
**Created**: 2025-12-13
**Purpose**: Persistent structured state für alle Evolving Workflows

---

## Konzept

```
┌─────────────────────────────────────────────────────────────┐
│                     DOMAIN MEMORY                            │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐   │
│  │ _memory/     │  │ ideas/       │  │ knowledge/       │   │
│  │ (State)      │  │ index.json   │  │ index.json       │   │
│  └──────────────┘  └──────────────┘  └──────────────────┘   │
└─────────────────────────────────────────────────────────────┘
         ▲
         │ Read → Work → Write
         │
    ┌────┴────────────────────────────────────┐
    │  JEDE Claude Session (Worker Agent)     │
    │  1. Bootup: Read Memory                 │
    │  2. Orient: Check State                 │
    │  3. Pick: Single Task                   │
    │  4. Work: Implement                     │
    │  5. Update: Write Progress              │
    │  6. Exit: Clean State                   │
    └─────────────────────────────────────────┘
```

---

## Struktur

```
_memory/
├── SCHEMA.md           # Diese Datei
├── index.json          # Meta-Index aller aktiven Memory States
│
├── workflows/          # Workflow-spezifischer State
│   ├── active.json     # Aktuell aktiver Workflow
│   └── history.json    # Abgeschlossene Workflows
│
├── projects/           # Pro aktivem Projekt
│   ├── {project}.json  # Project-specific domain memory
│   └── ...
│
└── sessions/           # Session-übergreifend
    └── context.json    # Aktueller Session Context
```

---

## Schema: index.json

```json
{
  "version": "1.0",
  "last_updated": "2025-12-13T22:00:00Z",

  "active_context": {
    "project": "{your-project-name}",
    "workflow": null,
    "focus": "Current Focus Area"
  },

  "projects": [
    {
      "id": "{project-id}",
      "status": "active",
      "memory_file": "projects/{project-id}.json"
    }
  ],

  "stats": {
    "total_sessions": 0,
    "total_tasks_completed": 0,
    "last_session": null
  }
}
```

---

## Schema: Project Memory

```json
{
  "id": "project-id",
  "name": "Human readable name",
  "type": "project",
  "status": "active | paused | completed",
  "created": "2025-12-13",
  "last_updated": "2025-12-13T22:00:00Z",

  "goals": {
    "primary": "Main objective",
    "success_criteria": [
      "Criterion 1",
      "Criterion 2"
    ],
    "features": [
      {
        "id": "f1",
        "name": "Feature Name",
        "status": "passing | failing | untested",
        "priority": "high | medium | low"
      }
    ]
  },

  "state": {
    "current_phase": "Phase description",
    "current_task": null,
    "blocking_issues": [],
    "recent_changes": []
  },

  "progress": [
    {
      "date": "2025-12-13",
      "session_id": "session-001",
      "action": "What was done",
      "result": "Outcome",
      "next": "Suggested next step"
    }
  ],

  "failures": [
    {
      "date": "2025-12-13",
      "what": "What failed",
      "why": "Root cause",
      "learned": "Lesson learned",
      "resolved": false
    }
  ],

  "capabilities": {
    "tech_stack": ["Python", "LangGraph"],
    "available_tools": ["Claude", "GitHub"],
    "constraints": ["No frontend work"]
  },

  "references": {
    "codebase": "/path/to/code",
    "docs": "knowledge/projects/...",
    "related_ideas": []
  }
}
```

---

## Schema: Workflow Memory

```json
{
  "id": "workflow-id",
  "type": "workflow",
  "workflow_type": "idea-work | project-work | research | debugging",
  "status": "active | paused | completed",
  "started": "2025-12-13T22:00:00Z",
  "last_updated": "2025-12-13T22:00:00Z",

  "context": {
    "trigger": "User request or automatic",
    "target": "What we're working on",
    "scope": "Boundaries of this workflow"
  },

  "goals": {
    "primary": "Main goal",
    "checklist": [
      {"item": "Step 1", "done": true},
      {"item": "Step 2", "done": false}
    ]
  },

  "state": {
    "current_step": "What's being worked on",
    "completed_steps": [],
    "blocked_by": null
  },

  "progress": [],
  "failures": []
}
```

---

## Schema: Session Context

```json
{
  "session_id": "session-2025-12-13-001",
  "started": "2025-12-13T22:00:00Z",
  "model": "opus-4.5",

  "bootup": {
    "read_memory": true,
    "checked_state": true,
    "identified_task": "Task description"
  },

  "focus": {
    "project": "project-id",
    "workflow": "workflow-id",
    "task": "Current task"
  },

  "progress_this_session": [],

  "handoff": {
    "completed": [],
    "in_progress": [],
    "next_steps": [],
    "blockers": []
  }
}
```

---

## Bootup Ritual (KRITISCH)

**Jede Session MUSS beginnen mit:**

```
1. READ MEMORY
   - _memory/index.json → Aktiver Context
   - _memory/projects/{active}.json → Project State
   - _memory/workflows/active.json → Workflow State (falls vorhanden)

2. ORIENT
   - Was war der letzte Progress?
   - Was sind die aktuellen Goals?
   - Was sind die bekannten Failures?

3. PICK
   - Wähle EINEN Task (atomic)
   - Nicht mehrere gleichzeitig

4. ANNOUNCE
   - Teile dem User mit was du vorhast
   - Hole Bestätigung wenn nötig
```

---

## Update Ritual (KRITISCH)

**Nach jeder signifikanten Aktion:**

```
1. LOG PROGRESS
   - Was wurde getan?
   - Was war das Ergebnis?

2. UPDATE STATE
   - Feature status ändern wenn applicable
   - Blocking issues aktualisieren

3. LOG FAILURES
   - Was ging schief?
   - Warum?
   - Was wurde gelernt?

4. SUGGEST NEXT
   - Was sollte als nächstes passieren?
```

---

## Integration mit existierenden Systemen

| System | Rolle | Memory Integration |
|--------|-------|-------------------|
| `ideas/index.json` | Idea Backlog | Goals/Features für Idea-Work |
| `knowledge/index.json` | Knowledge State | Reference für alle Workflows |
| `_handoffs/` | Session Summaries | Wird zu `sessions/` migriert |
| `knowledge/plans/` | Parked Plans | Goals für geplante Arbeit |
| `TodoWrite` | Session Tasks | Temporär, wird zu Progress |

---

## Commands mit Memory

| Command | Memory Read | Memory Write |
|---------|-------------|--------------|
| `/idea-work` | projects/{idea}.json | Progress, State |
| `/project-analyze` | projects/{project}.json | Capabilities, References |
| `/debug` | workflows/active.json | Failures, Progress |
| `/sparring` | sessions/context.json | Progress |
| `/whats-next` | ALL | Handoff Summary |

---

## Beispiel: Vollständiger Workflow

### 1. User startet Session
```
User: "Weiter an {project-name} arbeiten"
```

### 2. Bootup (automatisch)
```
Claude reads:
- _memory/index.json → active_context.project = "{project-id}"
- _memory/projects/{project-id}.json

Claude knows:
- Current phase: {current-phase}
- Last progress: {last-progress}
- Blocking: None
- Next suggested: {next-step}
```

### 3. Orient & Pick
```
Claude: "Ich sehe wir sind bei {phase}.
         Letzte Session: {last-progress}.
         Nächster Schritt wäre {next-step}.
         Soll ich damit weitermachen?"
```

### 4. Work
```
[Claude arbeitet an {next-step}]
```

### 5. Update Memory
```json
// Progress hinzufügen
{
  "date": "YYYY-MM-DD",
  "action": "{action-taken}",
  "result": "{result}",
  "next": "{suggested-next-step}"
}

// State aktualisieren
"current_phase": "{new-phase}"
```

### 6. Session Ende
```
Claude: "Session beendet. Progress gespeichert.
         Nächste Session: {next-step}."
```

---

## Migration von _handoffs/

Die existierenden `_handoffs/` Dateien werden zu:
- `_memory/sessions/history.json` (zusammengefasst)
- Alte Dateien können archiviert werden

---

## Validation

Ein Memory State ist VALID wenn:
- [ ] `id` vorhanden und unique
- [ ] `status` ist einer der erlaubten Werte
- [ ] `last_updated` ist aktuell
- [ ] `goals.primary` ist definiert
- [ ] Mindestens ein `progress` Entry existiert

---

**Version**: 1.0
**Author**: Claude
