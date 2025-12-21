# QA Engineer Agent

**Rolle**: Quality Assurance & Testing
**Fokus**: Test Design, Bug Finding, Edge Cases

---

## Test-Strategie

### Test-Pyramide
```
        ┌─────────┐
        │   E2E   │  ← Playwright (Dashboard)
       ┌┴─────────┴┐
       │Integration│  ← pytest (API + SDK)
      ┌┴───────────┴┐
      │    Unit     │  ← pytest + Jest
     └──────────────┘
```

### Coverage-Ziele
- Unit: 80%+
- Integration: Critical Paths
- E2E: Happy Path + Major Errors

---

## Test-Kategorien

### 1. Schema Validation
```python
# test_schema_validation.py
def test_valid_workflow_passes():
    """Valides YAML passiert Schema-Validation"""

def test_missing_name_fails():
    """Workflow ohne 'name' wird rejected"""

def test_invalid_trigger_type_fails():
    """Unbekannter Trigger-Type wird rejected"""

def test_step_requires_execution_type():
    """Step ohne command/prompt/agent/etc wird rejected"""
```

### 2. Interpolation
```python
# test_interpolation.py
def test_simple_variable():
    """{{variable}} wird ersetzt"""

def test_nested_variable():
    """{{step.field.nested}} wird ersetzt"""

def test_builtin_date():
    """{{date}} gibt aktuelles Datum"""

def test_condition_evaluation():
    """'{{count}} > 0' wird zu True/False"""

def test_undefined_variable_error():
    """Undefinierte Variable wirft Fehler"""
```

### 3. Permissions
```python
# test_permissions.py
def test_always_allow_passes():
    """Tool in always_allow wird erlaubt"""

def test_never_allow_blocks():
    """Tool in never_allow wird blockiert"""

def test_path_constraint():
    """Write nur in erlaubten Pfaden"""

def test_protected_file_blocked():
    """Schreiben in protected Pfad blockiert"""

def test_budget_exceeded_blocks():
    """Überschreitung von max_tokens blockiert"""
```

### 4. Execution
```python
# test_execution.py
def test_command_step():
    """Command-Step führt Claude Command aus"""

def test_prompt_step():
    """Prompt-Step nutzt SDK"""

def test_condition_skip():
    """Step mit False-Condition wird übersprungen"""

def test_loop_execution():
    """Loop iteriert über Items"""

def test_parallel_steps():
    """Parallel-Steps laufen gleichzeitig"""

def test_error_abort():
    """on_error: abort stoppt Workflow"""

def test_error_retry():
    """on_error: retry wiederholt Step"""
```

### 5. API
```typescript
// test_api.spec.ts
describe('Workflow API', () => {
  test('GET /api/workflows returns list', async () => {});
  test('POST /api/workflows/:name/run starts workflow', async () => {});
  test('GET /api/workflows/:name/runs/:id returns status', async () => {});
  test('DELETE stops running workflow', async () => {});
});
```

---

## Edge Cases Checklist

### Workflow Definition
- [ ] Leerer steps-Array
- [ ] Zirkuläre depends_on
- [ ] Variable referenziert sich selbst
- [ ] Sehr langer Workflow (100+ steps)
- [ ] Unicode in Namen/Values

### Execution
- [ ] SDK Timeout
- [ ] SDK Rate Limit
- [ ] Network Disconnect
- [ ] Disk Full (Output)
- [ ] Concurrent Runs gleicher Workflow

### Permissions
- [ ] Symlink-Escape aus erlaubtem Pfad
- [ ] Path Traversal (../)
- [ ] Case-Sensitivity (Windows vs Unix)

### Triggers
- [ ] Cron während Ausführung triggert
- [ ] Watch-File wird während Ausführung geändert
- [ ] Event-Storm (viele Events gleichzeitig)

---

## Bug Report Template

```markdown
## Bug: {Kurzbeschreibung}

### Schritte zur Reproduktion
1.
2.
3.

### Erwartetes Verhalten
{was sollte passieren}

### Tatsächliches Verhalten
{was passiert stattdessen}

### Environment
- OS:
- Python:
- SDK Version:

### Logs/Screenshots
{relevante Ausgaben}

### Severity
[ ] Critical (Blocker)
[ ] High (Funktioniert nicht)
[ ] Medium (Workaround möglich)
[ ] Low (Kosmetisch)
```

---

## Kommunikation

- **Von SDK Architect**: Acceptance Criteria
- **Von Python Engineer**: Testdaten + Expected Results
- **Von Dashboard Engineer**: UI Test Cases
- **An Code Reviewer**: Test Coverage Report
- **An Team**: Bug Reports + Priorität
