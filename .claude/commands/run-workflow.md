# Run Workflow

Führt einen Workflow aus dem `workflows/definitions/` Verzeichnis aus.

## Arguments
$ARGUMENTS

## Workflow

### 1. Parse Arguments

Argumente:
- `workflow_name` (required) - Name des Workflows
- `--variables` oder `-v` - JSON-String mit Variablen
- `--dry-run` oder `-d` - Nur Preview, keine Ausführung
- `--yes` oder `-y` - Keine Bestätigung erforderlich
- `--resume` oder `-r` - Run-ID zum Fortsetzen

Beispiele:
- `/run-workflow weekly-review`
- `/run-workflow idea-forge-full -v '{"idea_input": "SaaS Tool"}'`
- `/run-workflow inbox-processing --dry-run`
- `/run-workflow idea-forge-full --resume 20241206-123456-abc123`

### 2. Load & Validate Workflow

```python
from workflows.engine import load_workflow, list_workflows

# Zeige verfügbare Workflows wenn keiner angegeben
if not workflow_name:
    available = list_workflows()
    print("Verfügbare Workflows:")
    for name in available:
        workflow = load_workflow(name)
        print(f"  - {name}: {workflow.description}")
    return

# Lade Workflow
workflow = load_workflow(workflow_name)
```

### 3. Preview Steps

Zeige immer einen Preview der Steps:

```
Workflow: {workflow.name} (v{workflow.version})
Beschreibung: {workflow.description}

Permissions: {workflow.permissions_profile}
Preferences: {workflow.preferences_profile}

Steps:
1. {step.name} [{step.get_execution_type()}] - {step.model}
2. ...

Variablen:
- {var.name}: {var.default or "(required)"}
...

Geschätzte Kosten: ~${estimated_cost}
Geschätzte Dauer: ~{estimated_duration}
```

### 4. Confirm (unless --yes)

Wenn nicht `--yes`:
- Frage User: "Workflow ausführen? (y/n)"
- Bei 'n': Abbruch

### 5. Execute

```python
from workflows.engine import WorkflowRunner

runner = WorkflowRunner()

if dry_run:
    result = await runner.dry_run(workflow_name, variables=parsed_variables)
else:
    result = await runner.run(
        workflow_name,
        variables=parsed_variables,
        resume_from=resume_id
    )
```

### 6. Report Results

Nach Ausführung:

```
═══════════════════════════════════════════════════════
Workflow Complete: {workflow.name}
═══════════════════════════════════════════════════════

Status: {result.status}
Dauer: {result.duration_seconds}s
Tokens: {result.total_tokens}
Kosten: ${result.total_cost:.4f}

Steps:
✓ Step 1: Erfasse Idee (success)
✓ Step 2: Validiere Idee (success)
⚠ Step 3: Expandiere (skipped - condition not met)
✓ Step 4: Dokumentation (success)

Logs: workflows/logs/{workflow.name}-{result.run_id}.json
```

Bei Fehler:
```
✗ Workflow Failed: {error}

Fehlgeschlagener Step: {step_name}
Fehler: {error_message}

Checkpoint: {checkpoint_path}
Fortsetzen mit: /run-workflow {name} --resume {run_id}
```

## Output Format

Der Output sollte:
1. Klar strukturiert sein
2. Farbcodes verwenden (✓ grün, ✗ rot, ⚠ gelb)
3. Wichtige Metriken zeigen (Tokens, Kosten, Dauer)
4. Bei Fehlern den Resume-Befehl zeigen

## Notes

- Workflows sind in `workflows/definitions/*.yaml` definiert
- Permissions in `workflows/permissions/*.yaml`
- Preferences in `workflows/preferences/*.yaml`
- Logs werden in `workflows/logs/` gespeichert
- Checkpoints in `workflows/checkpoints/` für Resume
