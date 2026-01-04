# Idempotent Redundancy

**Priorität**: MITTEL
**Trigger**: Fallback-Logik, Belt-and-Suspenders Patterns, Repair-Hooks
**Quelle**: continuous-claude

---

## Das Prinzip

> "Redundancy without idempotency causes loops, churn, or data corruption."

Redundante Pfade (Fallbacks, mehrfache Sicherungen) nur wenn sie idempotent sind.

---

## DO

- Prüfen ob Wert existiert bevor geschrieben wird (Fallback nur wenn fehlt)
- Atomic Write/Rename für File Operations
- Reconciliation Steps sicher wiederholbar machen
- `_is_merge: true` für Update-Operations

## DON'T

- Unconditional writes in Fallback-Pfaden
- Multiple Writers die sich überschreiben
- "Repair" Actions die weitere Repairs triggern
- Fire-and-forget ohne Idempotenz-Check

---

## Pattern: Check-Before-Write

```python
# SCHLECHT: Überschreibt immer
def save_progress(data):
    write_file('progress.json', data)

# GUT: Idempotent
def save_progress(data):
    existing = read_file_if_exists('progress.json')
    if existing != data:
        write_file('progress.json', data)
```

---

## Pattern: Atomic Operations

```bash
# SCHLECHT: Partial write möglich
echo "$content" > target.md

# GUT: Atomic via rename
echo "$content" > target.md.tmp
mv target.md.tmp target.md
```

---

## Pattern: Merge statt Replace

```python
# SCHLECHT: Überschreibt alles
memory['experiences'] = new_experiences

# GUT: Merged idempotent
for exp in new_experiences:
    if exp['id'] not in memory['experiences']:
        memory['experiences'][exp['id']] = exp
```

---

## Wann kritisch?

| Situation | Risiko | Lösung |
|-----------|--------|--------|
| Hook schreibt File | Doppelte Einträge | Check-before-append |
| Fallback-Indexing | Duplicate Index | Upsert statt Insert |
| Error Recovery | Infinite Loop | Max-Retries + Backoff |
| Multi-Agent Write | Race Condition | Locking oder Merge |

---

## Beispiel: Experience Memory

```python
# Experience hinzufügen (idempotent)
def add_experience(exp: Experience):
    exp_id = exp['id']  # z.B. "exp-2025-001"
    exp_path = f"_memory/experiences/{exp_id}.json"

    # Idempotent: Existiert bereits?
    if os.path.exists(exp_path):
        existing = read_json(exp_path)
        if existing == exp:
            return  # Nichts zu tun

    # Atomic write
    write_json_atomic(exp_path, exp)
```

---

## Anti-Pattern: Repair Loop

```python
# SCHLECHT: Kann Loop verursachen
def repair_hook():
    if is_broken():
        fix_it()  # fix_it() triggert repair_hook() erneut!

# GUT: Idempotent mit Guard
def repair_hook():
    if is_broken() and not is_being_repaired():
        mark_as_repairing()
        try:
            fix_it()
        finally:
            mark_as_repaired()
```

---

## Integration

Diese Rule arbeitet zusammen mit:
- `index-at-creation.md` - Index-Operations idempotent
- `clear-dont-compact.md` - Ledger-Updates idempotent
- `domain-memory-bootup.md` - Memory-Writes idempotent
