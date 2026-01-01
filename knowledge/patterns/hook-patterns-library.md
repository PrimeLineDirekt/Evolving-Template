# Hook Patterns Library

**Quelle**: davila7/claude-code-templates
**Typ**: Pattern Collection
**Anwendung**: Wiederverwendbare Hook-Patterns für Claude Code

---

## Konzept

Standardisierte Hook-Patterns für häufige Automatisierungen. Jedes Pattern nutzt Claude Code Environment Variables.

---

## Environment Variables

| Variable | Beschreibung |
|----------|--------------|
| `CLAUDE_TOOL_NAME` | Name des ausgeführten Tools (Edit, Write, Bash, etc.) |
| `CLAUDE_TOOL_FILE_PATH` | Pfad zur bearbeiteten Datei |
| `CLAUDE_PROJECT_DIR` | Projekt-Root Verzeichnis |

---

## Pattern Katalog

### 1. Logging Pattern

**Zweck**: Tool-Nutzung protokollieren

```bash
# PreToolUse - Alle Tools
echo "[$(date)] $CLAUDE_TOOL_NAME" >> ~/.claude/activity.log
```

**Use Case**: Audit Trail, Debugging, Analytics

---

### 2. Backup Pattern

**Zweck**: Backup vor Bearbeitung

```bash
# PreToolUse - Edit|MultiEdit
[[ -f "$CLAUDE_TOOL_FILE_PATH" ]] && \
  cp "$CLAUDE_TOOL_FILE_PATH" "$CLAUDE_TOOL_FILE_PATH.$(date +%s).bak" 2>/dev/null || true
```

**Use Case**: Safety Net für wichtige Dateien

---

### 3. Auto-Format Pattern

**Zweck**: Automatische Formatierung nach Bearbeitung

```bash
# PostToolUse - Edit
if [[ "$CLAUDE_TOOL_FILE_PATH" =~ \.(js|ts)$ ]]; then
  npx prettier --write "$CLAUDE_TOOL_FILE_PATH" 2>/dev/null || true
elif [[ "$CLAUDE_TOOL_FILE_PATH" == *.py ]]; then
  black "$CLAUDE_TOOL_FILE_PATH" 2>/dev/null || true
fi
```

**Use Case**: Konsistente Code-Formatierung

---

### 4. Git Auto-Add Pattern

**Zweck**: Geänderte Dateien automatisch stagen

```bash
# PostToolUse - Edit|Write
git rev-parse --git-dir >/dev/null 2>&1 && \
  git add "$CLAUDE_TOOL_FILE_PATH" 2>/dev/null || true
```

**Use Case**: Keine vergessenen Änderungen

---

### 5. Notification Pattern

**Zweck**: Desktop-Benachrichtigung bei Tool-Abschluss

```bash
# PostToolUse - *
if command -v osascript >/dev/null; then
  osascript -e 'display notification "$CLAUDE_TOOL_NAME completed" with title "Claude Code"'
elif command -v notify-send >/dev/null; then
  notify-send "Claude Code" "$CLAUDE_TOOL_NAME completed"
fi
```

**Use Case**: Awareness bei langen Operationen

---

### 6. Auto-Test Pattern

**Zweck**: Tests nach Bearbeitung ausführen

```bash
# PostToolUse - Edit
if [[ -f package.json ]]; then
  npm test 2>/dev/null || yarn test 2>/dev/null || true
elif [[ -f pytest.ini ]]; then
  pytest 2>/dev/null || true
fi
```

**Use Case**: Sofortiges Feedback

---

### 7. Auto-Build Pattern

**Zweck**: Build nach Bearbeitung triggern

```bash
# PostToolUse - Edit
if [[ -f package.json ]] && grep -q '"build"' package.json; then
  npm run build 2>/dev/null || true
elif [[ -f Makefile ]]; then
  make 2>/dev/null || true
fi
```

**Use Case**: Kontinuierliches Build

---

### 8. Security Scan Pattern

**Zweck**: Sicherheits-Check nach Bearbeitung

```bash
# PostToolUse - Edit|Write
if command -v gitleaks >/dev/null; then
  gitleaks detect --source="$CLAUDE_TOOL_FILE_PATH" --no-git 2>/dev/null || true
fi
grep -qE '(password|secret|key)\s*=' "$CLAUDE_TOOL_FILE_PATH" && \
  echo "⚠️ Potential secrets in $CLAUDE_TOOL_FILE_PATH" || true
```

**Use Case**: Keine Secrets committen

---

### 9. File Protection Pattern

**Zweck**: Kritische Dateien vor Bearbeitung schützen

```bash
# PreToolUse - Edit|Write
for p in '/etc/*' '/usr/bin/*' '*.production.*' '*prod*config*' '/node_modules/*'; do
  [[ "$CLAUDE_TOOL_FILE_PATH" == $p ]] && \
    echo "Error: Protected file" >&2 && exit 1
done
```

**Use Case**: Schutz vor versehentlichen Änderungen

---

## Kombinierte Patterns

### Development Workflow

```json
{
  "hooks": {
    "PreToolUse": [{
      "matcher": "Edit|Write",
      "hooks": [{"type": "command", "command": "BACKUP_PATTERN"}]
    }],
    "PostToolUse": [
      {"matcher": "Edit", "hooks": [{"type": "command", "command": "FORMAT_PATTERN"}]},
      {"matcher": "Edit|Write", "hooks": [{"type": "command", "command": "GIT_ADD_PATTERN"}]}
    ]
  }
}
```

### Security Workflow

```json
{
  "hooks": {
    "PreToolUse": [{
      "matcher": "Edit|Write",
      "hooks": [{"type": "command", "command": "PROTECT_PATTERN"}]
    }],
    "PostToolUse": [{
      "matcher": "Edit|Write",
      "hooks": [{"type": "command", "command": "SECURITY_PATTERN"}]
    }]
  }
}
```

---

## Best Practices

### 1. Error Suppression

```bash
2>/dev/null || true
```

Hooks sollten Claude nie blockieren wenn Tool nicht verfügbar.

### 2. Conditional Execution

```bash
[[ -f "$CLAUDE_TOOL_FILE_PATH" ]] && ...
```

Prüfen ob Datei existiert bevor Operation.

### 3. Tool Detection

```bash
command -v gitleaks >/dev/null && ...
```

Prüfen ob Tool installiert.

### 4. Matcher nutzen

```json
{"matcher": "Edit|Write", "hooks": [...]}
```

Nicht auf alle Tools anwenden wenn nicht nötig.

---

## Integration

### In settings.json

```json
{
  "hooks": {
    "PostToolUse": [{
      "matcher": "Edit",
      "hooks": [{
        "type": "command",
        "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/auto-format.sh"
      }]
    }]
  }
}
```

### Als eigenständige Scripte

```
.claude/hooks/
├── backup.sh
├── auto-format.sh
├── git-add.sh
├── security-scan.sh
└── protect.sh
```

---

## Related

- `.claude/hooks/` - Unsere implementierten Hooks
- `knowledge/learnings/safety-hooks-framework.md` - Safety Hooks
- `_archive/repos/2025-12-27-claude-code-templates/_analysis.md` - Quelle
