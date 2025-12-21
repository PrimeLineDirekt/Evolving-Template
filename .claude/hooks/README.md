# Claude Code Hooks

Automatisierung für konsistente Workflows und Session-Tracking.

## Was sind Hooks?

Hooks sind Skripte, die automatisch bei bestimmten Events ausgeführt werden. Sie erweitern Claude Code um Automatisierung, Validierung und Tracking.

**Vorteile:**
- Konsistenz-Checks automatisieren
- Session-Dokumentation vereinfachen
- Fehler früh erkennen
- Workflows standardisieren

## Verfügbare Hook-Events

Claude Code unterstützt 10 Hook-Events:

| Event | Trigger | Use Case |
|-------|---------|----------|
| `Start` | Session startet | Initialisierung, Setup |
| `Stop` | Session endet | Cleanup, Summary |
| `PreToolUse` | Vor Tool-Aufruf | Validierung, Safety Checks |
| `PostToolUse` | Nach Tool-Aufruf | Konsistenz-Checks, Sync |
| `PreGitCommit` | Vor Git Commit | Linting, Tests |
| `PostGitCommit` | Nach Git Commit | Notifications |
| `PreGitPush` | Vor Git Push | Safety Checks |
| `PostGitPush` | Nach Git Push | Deployment |
| `PreSlashCommand` | Vor Slash Command | Authorization |
| `PostSlashCommand` | Nach Slash Command | Logging |

## StatusLine Configuration

### Context Monitor (StatusLine)

**File:** `context-monitor.sh`
**Trigger:** StatusLine (permanent display)
**Purpose:** Live-Anzeige von Session-Kosten, Modell und Dauer

**Anzeige-Format:**
```
Evolving 🟢 $0.0234 | sonnet-4.5 | 45.3s
         │   │        │           │
         │   │        │           └─ Session-Dauer
         │   │        └─ Aktuelles Modell (gekürzt)
         │   └─ Echte API-Kosten in USD
         └─ Status basierend auf Kosten
```

**Farbschema (basiert auf Kosten):**
- 🟢 Grün: < $0.10 (minimal)
- 🟡 Gelb: $0.10 - $0.50 (niedrig)
- 🟠 Orange: $0.50 - $1.00 (medium)
- 🔴 Rot: > $1.00 (hoch)

**Design-Entscheidung (Simplified):**
Token-Zählung aus JSONL-Transcripts wurde bewusst NICHT implementiert wegen:
1. **Multiple Transcripts:** Main + Sub-Agents (keine single source of truth)
2. **Cache Complexity:** Cache-Creation-Tokens komplex zu berechnen
3. **Reliability:** API-Cost ist 100% akkurat, Token-Count wäre Schätzung

Stattdessen: **Fokus auf zuverlässige API-Metriken** (Cost, Model, Duration)

**Technische Details:**
- Liest JSON via stdin (nicht Umgebungsvariablen!)
- Nutzt `jq` wenn verfügbar, sonst grep/sed fallback
- Non-blocking, schnell (<50ms)
- Simpel & zuverlässig

**Configuration (settings.json):**
```json
{
  "statusLine": {
    "type": "command",
    "command": "bash \"$CLAUDE_PROJECT_DIR\"/.claude/hooks/context-monitor.sh",
    "padding": 1
  }
}
```

**Wichtig:** StatusLine Hooks erhalten **keine** Umgebungsvariablen wie `CLAUDE_TOKEN_USAGE_INPUT`. Stattdessen kommen alle Daten via stdin als JSON mit:
- `cost.total_cost_usd` - Echte API-Kosten
- `cost.total_duration_ms` - Session-Dauer in Millisekunden
- `model.display_name` - Voller Model-Name (wird gekürzt)

---

## Installierte Hooks

### 1. Auto Cross-Reference Hook

**File:** `auto-cross-reference.sh`
**Trigger:** `PostToolUse` (Write|Edit)
**Purpose:** Erinnert Claude an Synchronisierung der Master Documents

**Master Documents:**
1. `README.md` - Projekt-Overview
2. `.claude/CONTEXT.md` - KI-Context
3. `knowledge/index.md` - Knowledge Base Index
4. `START.md` - Onboarding

**Was passiert:**
- Hook erkennt wenn ein Master Document geändert wird
- Claude erhält Erinnerung, alle 4 Dokumente zu synchronisieren
- Verhindert inkonsistente Stats/Counts/Strukturen

**Beispiel-Output:**
```
⚠️ CROSS-REFERENCE SYNCHRONIZATION RULE:

Master Document geändert. Prüfe ob diese 4 Dokumente synchron sind:
1. README.md
2. .claude/CONTEXT.md
3. knowledge/index.md
4. START.md

Aktualisiere alle relevanten Stats, Counts, Strukturen.
```

### 2. Session Summary Hook

**File:** `session-summary.sh`
**Trigger:** `Stop`
**Purpose:** Erstellt Session-Summary bei Session-Ende

**Was passiert:**
- Erzeugt Timestamp (YYYY-MM-DD-HHMMSS)
- Erstellt `knowledge/sessions/` Ordner falls nötig
- Claude erhält Aufforderung, Summary zu schreiben

**Summary-Struktur:**
```markdown
# Session Summary - {timestamp}

**Session ID:** {session_id}
**Date:** {date}

## Activities
- Activity 1
- Activity 2

## Deliverables
- Deliverable 1
- Deliverable 2

## Next Steps
- [ ] Task 1
- [ ] Task 2
```

## Hook-Entwicklung

### Input/Output Format

Hooks kommunizieren via JSON über stdin/stdout.

**Input (von Claude Code):**
```json
{
  "tool_name": "Write",
  "tool_input": {
    "file_path": "/path/to/file.md"
  },
  "session_id": "xyz",
  "cwd": "/working/directory"
}
```

**Output (an Claude Code):**
```json
{
  "hookSpecificOutput": {
    "hookEventName": "PostToolUse",
    "additionalContext": "Message for Claude..."
  }
}
```

### Exit Codes

Hooks verwenden standard Exit Codes:

- `0` - Success (Hook erlaubt Operation)
- `1` - Generic Error
- `2` - Block (Hook verhindert Operation)

**Wichtig:** PostToolUse/Stop Hooks sollten IMMER mit `exit 0` enden (non-blocking).

### Sicherheit

**Non-Blocking Design:**
```bash
#!/bin/bash
set -euo pipefail  # Fail on errors

# ... your logic ...

# Always exit 0 for PostToolUse/Stop hooks
exit 0
```

**Error Handling:**
```bash
# Graceful fallback
file_path=$(echo "$input" | jq -r '.tool_input.file_path // empty')

if [ -z "$file_path" ]; then
  exit 0  # No file_path, skip silently
fi
```

**Timeouts:**
- Hooks haben 5s timeout (konfiguriert in `settings.json`)
- Schnelle Checks bevorzugen
- Heavy operations vermeiden

### Testing

**1. Manual Testing:**
```bash
# Test auto-cross-reference hook
echo '{"tool_input":{"file_path":"README.md"}}' | bash .claude/hooks/auto-cross-reference.sh

# Test session-summary hook
echo '{"session_id":"test-123","cwd":"'$(pwd)'"}' | bash .claude/hooks/session-summary.sh
```

**2. Environment Testing:**
```bash
# Set CLAUDE_TOOL_INPUT (für PreToolUse Hooks)
CLAUDE_TOOL_INPUT="git push" bash .claude/hooks/your-hook.sh
```

**3. Validate JSON Output:**
```bash
echo '...' | bash hook.sh | jq .
```

## Configuration

Hooks werden in `.claude/settings.json` konfiguriert:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "bash \"$CLAUDE_PROJECT_DIR\"/.claude/hooks/auto-cross-reference.sh",
            "timeout": 5
          }
        ]
      }
    ],
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "bash \"$CLAUDE_PROJECT_DIR\"/.claude/hooks/session-summary.sh",
            "timeout": 5
          }
        ]
      }
    ]
  }
}
```

**Parameter:**
- `matcher` - Regex für Tool-Namen (nur PostToolUse)
- `type` - Immer `"command"`
- `command` - Shell Command (nutze `$CLAUDE_PROJECT_DIR` für Portabilität)
- `timeout` - Max. Laufzeit in Sekunden

## Troubleshooting

### Hook wird nicht ausgeführt

**Check 1: Executable Permissions**
```bash
chmod +x .claude/hooks/*.sh
ls -la .claude/hooks/
```

**Check 2: JSON Syntax**
```bash
cat .claude/settings.json | jq .
```

**Check 3: Hook Output**
```bash
# Test manually (siehe Testing section)
```

### Hook blockiert Operations

**PreToolUse/PreGitPush Hooks:**
- Exit Code 2 blockiert Operation
- Check Logic im Hook

**PostToolUse/Stop Hooks:**
- Sollten NIE blockieren (immer exit 0)
- Falls doch: Timeout erhöhen oder Hook deaktivieren

### JSON Parse Errors

**Problem:** `jq: parse error`

**Lösung:**
```bash
# Validate JSON before cat
valid_json='{"key":"value"}'
echo "$valid_json" | jq . > /dev/null && echo "$valid_json"
```

### Environment Variables fehlen

**Available Variables:**
- `$CLAUDE_PROJECT_DIR` - Projekt-Root
- `$CLAUDE_TOOL_INPUT` - Tool Input (PreToolUse)

**Check:**
```bash
echo "Project: $CLAUDE_PROJECT_DIR"
echo "Input: $CLAUDE_TOOL_INPUT"
```

## Best Practices

1. **Keep it Fast**
   - Hooks sollten < 1s laufen
   - Timeout ist 5s, aber User wartet

2. **Fail Gracefully**
   - Immer exit 0 für PostToolUse/Stop
   - Keine Blockierung bei Fehlern

3. **Clear Messages**
   - User-friendly Output
   - Klare Handlungsanweisungen

4. **Test Thoroughly**
   - Manual Testing vor Aktivierung
   - Edge Cases prüfen

5. **Document Well**
   - Kommentare im Script
   - README update

## Referenzen

**Offizielle Docs:**
- Claude Code Hooks Documentation (siehe `~/.claude/docs/`)

**Beispiele:**
- `~/.claude/hooks/git-safe-push.sh` - Globaler Hook
- `.claude/hooks/auto-cross-reference.sh` - Projekt-Hook
- `.claude/hooks/session-summary.sh` - Projekt-Hook

**Community:**
- GitHub Discussions
- Discord Community

---

**Version:** 1.0.0
**Last Updated:** 2025-11-27
