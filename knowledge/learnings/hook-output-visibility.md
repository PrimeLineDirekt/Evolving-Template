# Hook Output Visibility in Claude Code

**Quelle**: Debugging Context Warning Hook (2025-12-30)
**Kontext**: PreToolUse Hook sollte warnen, aber Warnungen waren unsichtbar
**Kategorie**: claude-code, hooks, debugging

---

## Das Problem

Ein PreToolUse Hook wurde implementiert der bei hohem Context % warnen sollte:

```bash
# Der Hook schrieb nach stderr:
echo "⚠️ KRITISCH: Context bei ${pct}%!" >&2
echo '{}'
```

**Ergebnis**: Keine Warnung sichtbar. Hook lief, aber User sah nichts.

---

## Root Cause

Claude Code Hooks haben unterschiedliche Output-Kanäle mit unterschiedlicher Sichtbarkeit:

| Output | Sichtbarkeit | Use Case |
|--------|--------------|----------|
| `stderr` | Nur verbose mode (Ctrl+O) | Debug-Logs |
| `stdout` JSON mit `systemMessage` | **Immer sichtbar** | User-Warnungen |
| `stdout` JSON mit `reason` | Nur für Claude | Erklärungen für AI |

---

## Die Lösung

Für User-sichtbare Nachrichten: `systemMessage` im JSON verwenden!

```bash
# FALSCH (unsichtbar):
echo "⚠️ Warning!" >&2
echo '{}'

# RICHTIG (sichtbar für User):
echo '{"systemMessage": "⚠️ Warning!", "continue": true}'
```

---

## Vollständiges Beispiel

```bash
#!/bin/bash
# PreToolUse Hook mit User-Warnung

if [[ $SOME_CONDITION ]]; then
  # Warnung für User (immer sichtbar)
  echo '{"systemMessage": "⚠️ Warnung!", "continue": true}'
else
  # Kein Output nötig
  echo '{}'
fi
```

---

## Hook JSON Fields (PreToolUse)

| Field | Typ | Zweck |
|-------|-----|-------|
| `systemMessage` | string | **User-sichtbare Nachricht** |
| `reason` | string | Erklärung für Claude (nicht User) |
| `continue` | boolean | Tool-Ausführung erlauben? |
| `permissionDecision` | string | "allow", "deny", "ask" |

---

## Key Takeaway

> **stderr ist für Debug-Logs. systemMessage ist für User-Warnungen.**

Wenn Hooks dem User etwas mitteilen sollen, muss es im JSON stdout als `systemMessage` erscheinen.

---

## Related

- [Hook Patterns Library](../patterns/hook-patterns-library.md)
- [Hook Development Reference](../patterns/hook-development-reference.md)
- [Context Budget Awareness Rule](../../.claude/rules/context-budget-awareness.md)
