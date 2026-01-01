# Idempotent Redundancy Pattern

**Source**: continuous-claude
**Extracted**: 2025-12-28
**Tags**: software-engineering, resilience, fault-tolerance

---

## Konzept

> "Redundancy is good only if idempotent."

Redundante Pfade (Fallbacks, Belt-and-Suspenders) sind wertvoll für Resilienz.
Aber ohne Idempotenz verursachen sie Loops, Churn oder Data Corruption.

---

## Das Problem

```
OHNE Idempotenz:

Primary Path → Write Data
      ↓
    Failed?
      ↓
Fallback Path → Write Data AGAIN
      ↓
    Failed?
      ↓
Recovery Hook → Write Data AGAIN
      ↓
→ Data verdoppelt, Loops, Inkonsistenz
```

---

## Die Lösung

```
MIT Idempotenz:

Primary Path → Upsert (create or update)
      ↓
    Failed?
      ↓
Fallback Path → Upsert (no-op if exists)
      ↓
    Failed?
      ↓
Recovery Hook → Upsert (safe to repeat)
      ↓
→ Korrekte Daten, keine Duplikate
```

---

## DO

| Technik | Beispiel |
|---------|----------|
| `_is_merge: true` | Braintrust Updates |
| Check before write | `if not exists(key): write(key)` |
| Atomic write/rename | Write to temp, then `mv` |
| Upsert statt Insert | `INSERT ... ON CONFLICT UPDATE` |
| Safe reconciliation | Re-runs produzieren gleiches Ergebnis |

## DON'T

| Anti-Pattern | Problem |
|--------------|---------|
| Unconditional writes | Daten verdoppeln |
| Multiple concurrent writers | Race conditions |
| Repair-Chains | `repair() → repair() → repair()` |
| Append in fallbacks | Infinite growth |

---

## Implementation Patterns

### 1. Check-Before-Write

```python
def safe_write(key: str, value: Any):
    if not exists(key):
        write(key, value)
    # Else: no-op, already exists
```

### 2. Merge Flag

```python
def update_record(record_id: str, data: dict):
    api.update(
        id=record_id,
        data=data,
        _is_merge=True  # Merge, don't replace
    )
```

### 3. Atomic Write

```python
def atomic_write(file_path: str, content: str):
    temp_path = f"{file_path}.tmp.{uuid4()}"

    # Write to temp
    with open(temp_path, 'w') as f:
        f.write(content)

    # Atomic rename
    os.rename(temp_path, file_path)
```

### 4. Idempotent Index

```python
def index_artifact(artifact_id: str, metadata: dict):
    """Safe to call multiple times."""

    # Upsert: create or update
    db.execute("""
        INSERT INTO artifacts (id, metadata, indexed_at)
        VALUES (?, ?, NOW())
        ON CONFLICT (id) DO UPDATE
        SET metadata = ?, indexed_at = NOW()
    """, (artifact_id, metadata, metadata))
```

---

## Wann anwenden?

| Situation | Idempotenz nötig? |
|-----------|-------------------|
| Fallback-Pfade | JA |
| Recovery-Hooks | JA |
| Scheduled Jobs | JA |
| Event-Handler (retries) | JA |
| Single-Shot Operations | Optional |

---

## Checkliste

```
□ Kann die Operation mehrfach ausgeführt werden?
□ Produziert wiederholte Ausführung das gleiche Ergebnis?
□ Werden Daten nicht verdoppelt/korrupt bei Retry?
□ Sind Race-Conditions zwischen Writers verhindert?
□ Können Repair-Actions sicher mehrfach laufen?
```

---

## Related

- `.claude/rules/index-at-creation.md` - Idempotent Indexing
- `hook-development-reference.md` - Hook Error Handling
