# Index at Creation Time

**Priorität**: MITTEL
**Trigger**: Artifact-Erstellung, Hook-Design, Indexing-Systeme
**Quelle**: continuous-claude

---

## Das Prinzip

> "Index artifacts when they're created, not at batch boundaries."

Wenn downstream-Logik davon abhängt dass Artifacts queryable sind, sofort beim Write indexieren.

---

## Pattern

```
FALSCH:
Artifact erstellen → ... → SessionEnd → Batch-Index
                           ↑
                   Zwischen-Queries finden nichts!

RICHTIG:
Artifact erstellen → Sofort indexieren → Queries funktionieren
```

---

## DO

- Index handoffs in PostToolUse Write hook (immediately after creation)
- Use `--file` flag for fast single-file indexing
- Trigger indexing from the same event that creates the artifact
- Keep index operations lightweight und non-blocking

## DON'T

- Wait for SessionEnd to batch-index
- Rely on cron/scheduled jobs for time-sensitive data
- Assume data will be available "soon enough"
- Block on heavy index operations (async if slow)

---

## Implementation

### PostToolUse Hook Pattern

```bash
#!/bin/bash
# hooks/index-on-write.sh

INPUT=$(cat)
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')

# Nur für relevante Pfade indexieren
if [[ "$FILE_PATH" == *"_handoffs/"* ]] || \
   [[ "$FILE_PATH" == *"knowledge/"* ]]; then

  # Async indexieren (non-blocking)
  python scripts/index_file.py --file "$FILE_PATH" &
fi

echo '{}'
```

### Single-File Indexing

```python
# scripts/index_file.py

def index_single_file(file_path: str):
    """Index one file instead of full re-index."""

    # Extract metadata
    metadata = extract_metadata(file_path)

    # Upsert to index (idempotent!)
    index.upsert(file_path, metadata)

    # Update graph connections
    graph.update_edges_for(file_path)
```

---

## Wann anwenden?

| Artifact-Typ | Index-Zeitpunkt | Warum |
|--------------|-----------------|-------|
| Handoffs | PostToolUse | Session-Übergabe braucht Queryability |
| Learnings | PostToolUse | Experience-Suggest braucht sofortigen Zugriff |
| Patterns | Kann warten | Weniger zeitkritisch |
| Session Notes | PostToolUse | Für nächste Session verfügbar |

---

## Trade-offs

| Approach | Pro | Con |
|----------|-----|-----|
| Index at Creation | Sofort queryable | Write-Overhead |
| Batch at SessionEnd | Effizient | Interim-Queries leer |
| Scheduled Cron | Decoupled | Latenz unkontrolliert |

**Empfehlung**: Index at Creation für zeitkritische Artifacts, Batch für den Rest.

---

## Related

- `observe-before-editing.md` - Outputs prüfen
- `knowledge/patterns/idempotent-redundancy-pattern.md` - Index-Operations idempotent
