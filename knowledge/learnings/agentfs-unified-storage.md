# AgentFS Unified Agent Storage

> **Source**: [tursodatabase/agentfs](https://github.com/tursodatabase/agentfs)
> **Type**: Learning / Infrastructure Pattern
> **Relevance**: HIGH - Agent State Management, Audit Trail, Reproducibility

## Konzept

AgentFS ist ein purpose-built Filesystem für AI Agents mit drei integrierten Storage-Layers:

```
┌─────────────────────────────────────────────┐
│              Single SQLite File              │
├─────────────────────────────────────────────┤
│  Layer 1: Tool Call Audit Trail (Immutable) │
│  Layer 2: Virtual Filesystem (POSIX-like)   │
│  Layer 3: Key-Value Store (Agent State)     │
└─────────────────────────────────────────────┘
```

## Warum relevant für Evolving?

| AgentFS Feature | Evolving Equivalent | Insight |
|-----------------|---------------------|---------|
| Tool Call Audit | - | Fehlt uns komplett |
| KV Store | _memory/ JSON | SQLite wäre robuster |
| Virtual FS | Filesystem direkt | Sandboxing interessant |
| Snapshots | Git commits | Agent-spezifisches Snapshot |

## Die drei Storage-Layer

### Layer 1: Tool Call Audit Trail

**Zweck**: Immutable Log aller Tool-Aufrufe für Debugging, Compliance, Analyse.

```sql
CREATE TABLE tool_calls (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,           -- Tool name (Read, Write, Bash, etc.)
  parameters TEXT,              -- JSON: Input parameters
  result TEXT,                  -- JSON: Success result (mutually exclusive with error)
  error TEXT,                   -- JSON: Error details
  started_at INTEGER NOT NULL,  -- Unix timestamp
  completed_at INTEGER NOT NULL,
  duration_ms INTEGER NOT NULL
);

CREATE INDEX idx_tool_calls_name ON tool_calls(name);
CREATE INDEX idx_tool_calls_started ON tool_calls(started_at);
```

**Key Constraint**: `result` XOR `error` - genau einer ist non-NULL.

**Query Patterns**:

```sql
-- Performance Analyse: Welche Tools sind langsam?
SELECT
  name,
  COUNT(*) as total_calls,
  SUM(CASE WHEN result IS NOT NULL THEN 1 ELSE 0 END) as successes,
  SUM(CASE WHEN error IS NOT NULL THEN 1 ELSE 0 END) as failures,
  AVG(duration_ms) as avg_duration_ms
FROM tool_calls
GROUP BY name;

-- Zeitfenster: Was passierte in den letzten 10 Minuten?
SELECT * FROM tool_calls
WHERE started_at > strftime('%s', 'now') - 600
ORDER BY started_at DESC;

-- Tool-spezifische History
SELECT * FROM tool_calls
WHERE name = 'Write'
ORDER BY started_at DESC
LIMIT 20;
```

### Layer 2: Virtual Filesystem

**Zweck**: POSIX-ähnliches Filesystem für Agent-Dateien, isoliert vom Host.

```sql
-- Inode Metadata
CREATE TABLE fs_inode (
  ino INTEGER PRIMARY KEY AUTOINCREMENT,
  mode INTEGER NOT NULL,        -- Unix mode bits (type + permissions)
  uid INTEGER NOT NULL DEFAULT 0,
  gid INTEGER NOT NULL DEFAULT 0,
  size INTEGER NOT NULL DEFAULT 0,
  atime INTEGER NOT NULL,       -- Access time
  mtime INTEGER NOT NULL,       -- Modification time
  ctime INTEGER NOT NULL        -- Change time
);

-- Directory Entries
CREATE TABLE fs_dentry (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  parent_ino INTEGER NOT NULL,
  ino INTEGER NOT NULL,
  UNIQUE(parent_ino, name)
);

-- File Content (chunked)
CREATE TABLE fs_data (
  ino INTEGER NOT NULL,
  chunk_index INTEGER NOT NULL,
  data BLOB NOT NULL,
  PRIMARY KEY (ino, chunk_index)
);

-- Configuration
CREATE TABLE fs_config (
  key TEXT PRIMARY KEY,
  value TEXT NOT NULL
);
-- Immutable: chunk_size = 4096
```

**Mode Bits**:
- Regular File: `0o100000 | permissions`
- Directory: `0o040000 | permissions`
- Symlink: `0o120000 | permissions`
- Root directory: immer inode 1

### Layer 3: Key-Value Store

**Zweck**: Agent State, Context, Preferences.

```sql
CREATE TABLE kv_store (
  key TEXT PRIMARY KEY,
  value TEXT NOT NULL,          -- JSON serialized
  created_at INTEGER DEFAULT (unixepoch()),
  updated_at INTEGER DEFAULT (unixepoch())
);
```

**Namespacing Convention**:
```
user:preferences
agent:state:current_task
session:2025-12-16:context
```

**Operations**:
```sql
-- Upsert
INSERT INTO kv_store (key, value, updated_at)
VALUES (?, ?, unixepoch())
ON CONFLICT(key) DO UPDATE SET
  value = excluded.value,
  updated_at = excluded.updated_at;

-- Get
SELECT value FROM kv_store WHERE key = ?;

-- List all with timestamps
SELECT key, created_at, updated_at FROM kv_store
ORDER BY updated_at DESC;
```

## Key Benefits

### 1. Auditability

```
Jede Operation wird geloggt:
- Welches Tool wurde aufgerufen?
- Mit welchen Parametern?
- Was war das Ergebnis?
- Wie lange hat es gedauert?

→ Debugging: "Warum hat das nicht funktioniert?"
→ Compliance: "Was hat der Agent getan?"
→ Analyse: "Welche Tools sind ineffizient?"
```

### 2. Reproducibility

```bash
# Agent-State snapshot
cp .agentfs/my-agent.db .agentfs/my-agent-snapshot.db

# Restore to exact state
cp .agentfs/my-agent-snapshot.db .agentfs/my-agent.db

# Test alternative scenarios
sqlite3 .agentfs/my-agent.db "DELETE FROM tool_calls WHERE id > 100"
```

### 3. Portability

```
Ein File = Kompletter Agent State
- Filesystem
- State
- History

→ Git-versionierbar
→ Zwischen Maschinen übertragbar
→ Cloud-deployable (Turso)
```

### 4. Sandboxing

```bash
# Isolierte Ausführung
agentfs run /bin/bash

# Agent sieht nur /agent filesystem
$ echo "test" > /agent/output.txt  # OK
$ echo "test" > /etc/passwd        # Blocked
```

## Integration mit Evolving

### Mögliche Anwendungen

1. **Tool Call Audit für Sessions**:
   ```
   _memory/sessions/
   └── session-2025-12-16.db  # SQLite mit tool_calls table
   ```

2. **Experience Memory Migration**:
   ```
   Aktuell: _memory/experiences/*.json
   Potentiell: SQLite mit besserer Query-Performance
   ```

3. **Agent Sandboxing für /create-system**:
   ```
   Generierte Systeme in isolierter Umgebung testen
   ```

### Schema für Evolving Agent Audit

```sql
-- Angepasst für Evolving
CREATE TABLE agent_actions (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  session_id TEXT NOT NULL,
  tool_name TEXT NOT NULL,
  tool_input TEXT,              -- JSON
  tool_output TEXT,             -- JSON
  tokens_used INTEGER,
  model TEXT,
  started_at INTEGER NOT NULL,
  completed_at INTEGER NOT NULL,
  duration_ms INTEGER NOT NULL,
  success BOOLEAN NOT NULL
);

CREATE INDEX idx_actions_session ON agent_actions(session_id);
CREATE INDEX idx_actions_tool ON agent_actions(tool_name);
CREATE INDEX idx_actions_time ON agent_actions(started_at);

-- Experience Memory in SQLite
CREATE TABLE experiences (
  id TEXT PRIMARY KEY,
  type TEXT NOT NULL,
  summary TEXT NOT NULL,
  context TEXT,
  problem TEXT,
  solution TEXT,
  root_cause TEXT,
  tags TEXT,                    -- JSON array
  project TEXT,
  relevance_score INTEGER DEFAULT 50,
  access_count INTEGER DEFAULT 0,
  created_at INTEGER,
  last_accessed INTEGER
);

CREATE INDEX idx_exp_type ON experiences(type);
CREATE INDEX idx_exp_project ON experiences(project);
CREATE INDEX idx_exp_score ON experiences(relevance_score);
```

## Best Practices aus AgentFS

1. **Single File Storage**: Alles in einer SQLite-Datei = Einfachheit
2. **Immutable Audit Log**: Insert-only für History = Vertrauen
3. **Chunked File Storage**: Große Files in 4KB Chunks = Effizienz
4. **Namespaced Keys**: `prefix:category:key` = Organisation
5. **Timestamp Tracking**: created_at + updated_at = Transparenz

## Vergleich: AgentFS vs. Evolving _memory/

| Aspect | AgentFS | Evolving |
|--------|---------|----------|
| Storage | SQLite | JSON Files |
| Query | SQL | File reads |
| Audit | Built-in | Nicht vorhanden |
| Snapshot | File copy | Git |
| Performance | High (indexed) | Medium |
| Complexity | Higher | Lower |

**Empfehlung**: Für einfache Fälle bleiben JSON Files OK. Bei wachsendem Scale → SQLite evaluieren.

---

## Related

- `_memory/` - Aktuelles Memory System
- `_memory/experiences/` - Experience Memory
- `knowledge/patterns/observation-compression-pattern.md` - Token Efficiency
