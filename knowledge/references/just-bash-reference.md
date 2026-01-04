# just-bash Reference

**URL**: https://github.com/vercel-labs/just-bash
**NPM**: `npm install just-bash`
**Typ**: Sandboxed Bash Environment for AI Agents
**Status**: Alpha (Pre-release)
**Checked**: 2025-12-29

---

## Was ist das?

Simulierte Bash-Umgebung mit In-Memory Virtual Filesystem. Designed für AI Agents die sichere, sandboxed Bash-Execution brauchen.

## Key Features

### Supported Commands

| Kategorie | Commands |
|-----------|----------|
| **File Ops** | cat, cp, ln, ls, mkdir, mv, rm, stat, touch, tree |
| **Text Processing** | awk, base64, cut, diff, grep, head, jq, sed, sort, tail, tr, uniq, wc, xargs |
| **Navigation** | basename, cd, dirname, du, echo, env, find, pwd, tee |
| **Shell** | alias, bash, chmod, date, expr, seq, sh, sleep, timeout, which |
| **Network** | curl, html-to-markdown |

### Shell Features

- Pipes (`|`)
- Redirections (`>`, `>>`, `2>`, `2>&1`, `<`)
- Chaining (`&&`, `||`, `;`)
- Variable Expansion, Glob Patterns
- Conditionals, Functions, Loops
- Symbolic/Hard Links

---

## Architektur

### Virtual Filesystem (VFS)

```
/home/user     # Default Working Dir
/bin           # Command Stubs
/usr/bin       # Command Stubs
/tmp           # Temporary Storage
```

### OverlayFS (Copy-on-Write)

```
Real Filesystem (Read-Only)
        ↓
    OverlayFS
        ↓
In-Memory Layer (Writes)
```

**Effekt**: Agent kann lesen vom echten FS, aber alle Writes bleiben in Memory.

---

## Security Model

### Sandboxing

- Nur Zugriff auf provided Filesystem
- Keine native Binary/WASM Execution
- Kein Network Access by default

### URL Filtering (Allow-List)

```typescript
network: {
  allowedUrlPrefixes: ["https://api.github.com/repos/myorg/"],
  allowedMethods: ["GET", "HEAD", "POST"],
}
```

- Origin Matching (scheme + host + port)
- Path-Prefix Validation
- Redirect Protection

### Execution Limits

| Limit | Default | Zweck |
|-------|---------|-------|
| maxCallDepth | - | Rekursions-Schutz |
| maxCommandCount | - | Loop-Schutz |
| maxLoopIterations | - | Infinite Loop Prevention |
| maxAwkIterations | - | AWK-spezifisch |
| maxSedIterations | - | SED-spezifisch |

---

## AI SDK Integration

```typescript
import { createBashTool } from "just-bash/ai";
import { generateText } from "ai";

const bashTool = createBashTool({
  files: { "/data/users.json": '[{"name": "Alice"}]' },
});

const result = await generateText({
  model: "anthropic/claude-haiku-4.5",
  tools: { bash: bashTool },
  prompt: "Count the users in /data/users.json",
});
```

---

## CLI Usage

```bash
# Inline Script
just-bash -c 'ls -la && cat package.json | head -5'

# Mit Project Root
just-bash -c 'grep -r "TODO" src/' --root /path/to/project

# Piped Input
echo 'find . -name "*.ts" | wc -l' | just-bash

# Script File
just-bash ./scripts/deploy.sh

# JSON Output
just-bash -c 'echo hello' --json
```

---

## Programmatic API

### Basic

```typescript
import { Bash } from "just-bash";

const env = new Bash();
await env.exec('echo "Hello" > greeting.txt');
const result = await env.exec("cat greeting.txt");
// result.stdout = "Hello\n"
// result.exitCode = 0
```

### Mit Config

```typescript
const env = new Bash({
  files: { "/data/file.txt": "content" },
  env: { MY_VAR: "value" },
  cwd: "/app",
  executionLimits: { maxCallDepth: 50 },
});
```

### OverlayFS

```typescript
import { OverlayFs } from "just-bash";

const overlay = new OverlayFs({ root: "/path/to/project" });
const env = new Bash({ fs: overlay, cwd: overlay.getMountPoint() });
// Reads from real FS, writes stay in memory
```

---

## Wann relevant?

| Use Case | Passt? |
|----------|--------|
| AI Agent braucht Bash aber sicher | ✅ Ja |
| Sandbox für Code-Execution | ✅ Ja |
| Testing ohne echte Filesystem-Änderungen | ✅ Ja |
| Production mit untrusted Input | ⚠️ Vorsicht (DOS möglich) |
| Native Binary Execution nötig | ❌ Nein |

---

## Integration mit Evolving

Potentielle Use Cases:
- Sichere Script-Execution in Agents
- Sandboxed Code-Testing
- AI SDK Tool für Bash-Tasks

**Note**: Vercel Labs Projekt, Alpha Status. Für Production OS-Level Isolation empfohlen.

---

## Related

- `cc-wf-studio-reference.md` - Anderes Tool für Claude Code
- `ralph-wiggum-loop-pattern.md` - Self-Improvement Loops
- `.claude/hooks/` - Hook-basierte Automation
