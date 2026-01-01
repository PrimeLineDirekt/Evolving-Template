# Observe Before Editing

**Priorität**: HOCH
**Trigger**: Bei Bug-Fixes, Hook-Debugging, unerwartetem Verhalten
**Quelle**: continuous-claude

---

## Das Prinzip

> "Outputs don't lie. Code might. Check outputs first."

Bevor Code editiert wird um einen Bug zu fixen, erst bestätigen was das System **tatsächlich produziert hat**.

---

## Workflow

### 1. Check Outputs (NICHT Code!)

| Situation | Prüf-Befehl |
|-----------|-------------|
| "Hook lief nicht" | `ls -la .claude/cache/` |
| "Dateien nicht erstellt" | `ls -la {expected-path}/` |
| "Fehler aufgetreten" | `tail .claude/cache/*.log` |
| "Falsches Verhalten" | Befehl manuell ausführen |

### 2. Verifiziere Pfade

```bash
# Projekt-Cache (lokal):
ls -la .claude/cache/

# User-Cache (global):
ls -la ~/.claude/cache/

# Beide prüfen - nicht verwechseln!
```

### 3. Run Manually

```bash
# Hook manuell testen:
echo '{"tool_name":"Write","tool_input":{"file_path":"test.md"}}' | \
  .claude/hooks/my-hook.sh

# Script manuell ausführen:
python scripts/my-script.py --help
```

### 4. DANN erst Code editieren

Nur wenn die Outputs bestätigt haben dass:
- Etwas tatsächlich nicht funktioniert
- Der Fehler lokalisiert ist
- Der erwartete Output definiert ist

---

## DO

- Check if expected directories exist
- Check if expected files were created
- Check logs for errors
- Run the failing command manually to see actual error
- Only then edit code

## DON'T

- Assume "hook didn't run" without checking outputs
- Edit code based on what you *think* should happen
- Confuse global vs project paths (check both)
- Trust stack traces ohne Output-Verification

---

## Beispiele aus der Praxis

| Session | Learning |
|---------|----------|
| Token Limit Error | War unsichtbar bis manueller Run es enthüllte |
| Hook Failure | Falscher Cache-Pfad geprüft (`~/.claude/` vs `.claude/`) |
| "Nichts passiert" | Output-Files waren da, nur an anderem Ort |
| DB Error | Erst `ls {db-path}` zeigte: File existiert gar nicht |

---

## Checkliste vor Code-Edit

```
□ Expected outputs geprüft (existieren? korrekt?)
□ Logs geprüft (Fehler? Warnings?)
□ Befehl manuell ausgeführt (actual error?)
□ Pfade verifiziert (project vs global?)
□ Erst DANN Code editieren
```

---

## Related

- `clear-dont-compact.md` - Session State Management
- `knowledge/patterns/hook-development-reference.md` - Hook Testing
