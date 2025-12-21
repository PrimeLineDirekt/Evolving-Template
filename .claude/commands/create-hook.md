---
description: Erstellt neuen Hook aus Template
model: haiku
argument-hint: [optional: hook-type]
---

Du bist mein Hook Creation Assistant. Deine Aufgabe ist es, einen neuen Hook aus Templates zu erstellen.

## Schritt 1: Hook-Typ erfassen

Wenn der User einen Typ als Argument übergeben hat ($ARGUMENTS ist nicht leer), nutze das als Hook-Typ.

Wenn $ARGUMENTS leer ist, frage:
"Welchen Hook-Typ möchtest du erstellen?"

**Optionen**:

1. **post-tool-use** - Event-driven nach Tool-Nutzung
   - Triggert: Nach Write, Edit, Read, etc.
   - Für: Auto-Cross-Referencing, Index-Updates, Logging
   - Beispiele: Markdown validation, Auto-linking, Stats tracking

2. **stop** - Session Summary bei Conversation-Ende
   - Triggert: Wenn Conversation endet
   - Für: Session-Logs, Activity-Summaries, Cleanup
   - Beispiele: Session summary, File archival, Stats aggregation

3. **custom** - Custom Hook (User definiert)
   - Nutzt post-tool-use als Basis
   - User definiert eigene Trigger-Logic

Falls unsicher, empfehle **post-tool-use** für die meisten Automation-Use-Cases.

## Schritt 2: Hook-Namen erfassen

Frage: "Wie soll der Hook heißen? (beschreibend, z.B. 'markdown-validator')"

### Naming Conventions:
- Lowercase mit hyphens
- Beschreibend (was macht der Hook?)
- Ohne .sh Extension (wird automatisch hinzugefügt)

**Beispiele**:
- markdown-validator
- auto-cross-reference
- session-logger
- idea-indexer
- backup-trigger

## Schritt 3: Template lesen

Lese das entsprechende Template:

```
post-tool-use: .claude/templates/hooks/post-tool-use.sh
stop: .claude/templates/hooks/stop-hook.sh
custom: .claude/templates/hooks/post-tool-use.sh (als Basis)
```

Nutze das Read-Tool um den Template-Inhalt zu laden.

## Schritt 4: Informationen sammeln

Basierend auf dem gewählten Hook-Typ:

### Für Post-Tool-Use Hook:

**Erfrage**:
1. **Welche Tools monitoren?** (z.B. "Write, Edit" oder "nur Write")
2. **Welche Pfade monitoren?** (z.B. "ideas/", "knowledge/", "*.md")
3. **Was soll passieren bei Write?** (Custom Logic)
4. **Was soll passieren bei Edit?** (Custom Logic)
5. **Logging aktivieren?** (Y/N, Default: Y)
6. **Debug-Mode?** (Y/N, Default: N)

**Monitoring-Patterns Beispiele**:
```
Pfade:
  - "ideas/" → Alle Dateien in ideas/
  - "*.md" → Alle Markdown-Dateien
  - "knowledge/.*\.md" → Regex pattern
  - "projects/.*/README.md" → Spezifisches Pattern
```

**Custom Logic Beispiele**:
```
Write Event:
  - Markdown validieren
  - Cross-References updaten
  - Index aktualisieren
  - Backup erstellen

Edit Event:
  - Änderungen loggen
  - Related files updaten
  - Validation triggern
```

### Für Stop Hook:

**Erfrage**:
1. **Wo sollen Summaries gespeichert werden?** (z.B. "knowledge/sessions" oder ".sessions")
2. **Welches Format?** (markdown/json/text, Default: markdown)
3. **Was soll getrackt werden?**
   - Timestamp? (Y/N)
   - Tools used? (Y/N)
   - Files modified? (Y/N)
   - Topics? (Y/N)
4. **Custom Topic-Detection?** (Optional: Logic um Topics zu identifizieren)

**Summary-Location Beispiele**:
```
- knowledge/sessions/ → In Knowledge Base
- .sessions/ → Hidden directory
- logs/sessions/ → In logs
```

## Schritt 5: Placeholders ersetzen

Ersetze alle `{PLACEHOLDERS}` im Template:

### Post-Tool-Use Placeholders:
- `{PATH_PATTERN_1}` → Erster Pfad-Pattern (z.B. "ideas/")
- `{PATH_PATTERN_2}` → Zweiter Pfad-Pattern (z.B. "knowledge/")
- `{CUSTOM_WRITE_LOGIC}` → Write-Handler Code
- `{CUSTOM_EDIT_LOGIC}` → Edit-Handler Code
- `{CROSS_REFERENCE_LOGIC}` → Cross-Reference Code (optional)
- `{INDEX_UPDATE_LOGIC}` → Index Update Code (optional)

### Stop Hook Placeholders:
- `{SUMMARY_OUTPUT_PATH}` → Output-Verzeichnis
- `{markdown|json|text}` → Format auswählen
- `{SESSION_DESCRIPTION}` → Placeholder für Session-Beschreibung
- `{CUSTOM_TOPIC_DETECTION}` → Topic-Detection Logic

### Configuration Updates:
Im Template-Header (bash comments) die CONFIGURATION-Sektion anpassen:

```bash
# CONFIGURATION
MONITORED_TOOLS=("Write" "Edit")  # Anpassen
MONITORED_PATHS=(
  "ideas/"
  "knowledge/"
)  # Anpassen
LOG_FILE=".claude/hooks/logs/{hook-name}.log"  # Anpassen
DEBUG=0  # 0 oder 1
```

**Wichtig**: Custom Logic muss valides Bash sein. Falls User nicht Bash-versiert:
- Biete einfache Beispiele
- Generiere Basis-Logic automatisch
- User kann später erweitern

## Schritt 6: Custom Logic generieren (falls nötig)

Für Post-Tool-Use Hooks, generiere Basis-Logic:

**Beispiel für Markdown Validation**:
```bash
process_write() {
  local file_path="$1"

  debug_log "Processing Write event for: $file_path"

  # Validate markdown
  if [[ "$file_path" =~ \.md$ ]]; then
    # Check frontmatter exists
    if ! grep -q "^---$" "$file_path"; then
      info_log "Missing frontmatter in $file_path"
    fi

    # Check for broken links (basic)
    if grep -q "\[.*\](.*404.*)" "$file_path"; then
      info_log "Potential broken link in $file_path"
    fi
  fi

  info_log "Write processed: $file_path"
}
```

**Beispiel für Auto-Index Update**:
```bash
process_write() {
  local file_path="$1"

  debug_log "Processing Write event for: $file_path"

  # Update index if idea file
  if [[ "$file_path" =~ ideas/.*\.md$ ]]; then
    # Extract idea-id from filename
    local idea_id=$(basename "$file_path" .md)

    # Trigger index update (example - anpassen!)
    # python3 .claude/scripts/update_index.py "$idea_id"

    info_log "Index updated for: $idea_id"
  fi

  info_log "Write processed: $file_path"
}
```

Frage User: "Soll ich Basis-Logic für {use-case} generieren oder möchtest du eigene Logic definieren?"

## Schritt 7: Validierung

Vor dem Schreiben prüfe:

- [ ] Alle Placeholders ersetzt
- [ ] Bash-Syntax ist valide (kein offensichtlicher Syntax-Error)
- [ ] Shebang vorhanden (`#!/bin/bash`)
- [ ] `trap 'exit 0' ERR` vorhanden (CRITICAL für Hooks!)
- [ ] `exit 0` am Ende (CRITICAL!)
- [ ] Hook-Name folgt Konventionen
- [ ] Datei existiert noch nicht (oder User bestätigt Überschreiben)
- [ ] Directory `.claude/hooks/` existiert

**CRITICAL**: Hooks MÜSSEN IMMER mit exit 0 enden, sonst blocken sie Claude!

Falls Datei bereits existiert, frage:
"Der Hook `.claude/hooks/{name}.sh` existiert bereits. Überschreiben? (Y/N)"

## Schritt 8: Hook-Datei erstellen

**Pfad**: `.claude/hooks/{name}.sh`

Nutze Write-Tool mit vollständig ausgefülltem Template.

## Schritt 9: Executable machen

Nach Write, führe aus:
```bash
chmod +x .claude/hooks/{name}.sh
```

Nutze Bash-Tool für diesen Command.

## Schritt 10: Settings.json konfigurieren (optional)

Frage: "Soll ich den Hook in .claude/settings.json konfigurieren?"

Falls ja:
1. Read `.claude/settings.json`
2. Prüfe ob `hooks` Section existiert
3. Füge Hook hinzu:

**Für post-tool-use Hook**:
```json
{
  "hooks": {
    "post_tool_use": [
      {
        "name": "{hook-name}",
        "script": ".claude/hooks/{hook-name}.sh",
        "enabled": true
      }
    ]
  }
}
```

**Für stop Hook**:
```json
{
  "hooks": {
    "stop": [
      {
        "name": "{hook-name}",
        "script": ".claude/hooks/{hook-name}.sh",
        "enabled": true
      }
    ]
  }
}
```

4. Edit die Datei mit der neuen Hook-Config

## Schritt 11: Bestätigung

Zeige dem User:

```
✓ Hook erfolgreich erstellt!

Datei: .claude/hooks/{name}.sh
Typ: {post-tool-use|stop} Hook
Triggers: {TRIGGER_BESCHREIBUNG}
Monitored Paths: {LIST_OF_PATHS}

{Falls settings.json updated}
✓ Hook konfiguriert in .claude/settings.json

Nächste Schritte:
→ Hook ist bereits executable (chmod +x applied)
→ Teste: {TESTING_INSTRUCTION}
→ Check Logs: .claude/hooks/logs/{name}.log
→ Passe Logic an falls nötig

{Falls NICHT in settings.json}
Optional: Füge Hook zu .claude/settings.json hinzu für automatische Aktivierung

Debugging:
→ Enable DEBUG=1 in Hook-Datei für verbose logging
→ Monitor logs: tail -f .claude/hooks/logs/{name}.log
```

**Testing Instructions** (basierend auf Typ):
- post-tool-use: "Bearbeite eine Datei in {monitored_path} und prüfe Logs"
- stop: "Beende Conversation und prüfe {summary_path}/"

**Beispiel**:
```
✓ Hook erfolgreich erstellt!

Datei: .claude/hooks/markdown-validator.sh
Typ: post-tool-use Hook
Triggers: Write, Edit
Monitored Paths: ideas/, knowledge/

✓ Hook konfiguriert in .claude/settings.json

Nächste Schritte:
→ Hook ist bereits executable (chmod +x applied)
→ Teste: Bearbeite eine .md Datei in ideas/ oder knowledge/
→ Check Logs: .claude/hooks/logs/markdown-validator.log
→ Passe Validation-Logic an falls nötig

Debugging:
→ Enable DEBUG=1 in Hook-Datei für verbose logging
→ Monitor logs: tail -f .claude/hooks/logs/markdown-validator.log
```

---

## Tool Usage

**Required Tools**:
- `Read`: Template lesen, settings.json lesen
- `Write`: Hook-Datei erstellen
- `Edit`: settings.json updaten (optional)
- `Bash`: chmod +x ausführen

**Tool Pattern**:
```
1. Read template file
2. Replace all placeholders
3. Validate bash syntax (basic)
4. Write hook file
5. Bash: chmod +x
6. (Optional) Read settings.json
7. (Optional) Edit settings.json
8. Confirm to user
```

---

## Error Handling

### Template nicht gefunden

```
IF template_not_found:
  Liste verfügbare Hook-Templates
  Frage User welcher Template
  Retry
```

### Bash Syntax Error

```
IF syntax_error_detected:
  Zeige problematische Zeile
  Erkläre Fehler
  Biete Fix an oder frage User
  Retry
```

### chmod fehlschlägt

```
IF chmod_fails:
  Warne User
  Gib manuelle Anleitung:
    "Führe aus: chmod +x .claude/hooks/{name}.sh"
  Hook wurde erstellt aber nicht executable
```

### settings.json Update fehlschlägt

```
IF settings_update_fails:
  Hook wurde trotzdem erstellt
  Gib manuelle Anleitung für settings.json
  Zeige JSON-Snippet zum Copy-Paste
```

---

## Validation Checklist

Vor Bestätigung prüfe:

- [ ] Template erfolgreich gelesen
- [ ] Alle Placeholders ersetzt
- [ ] Shebang vorhanden
- [ ] trap und exit 0 vorhanden (CRITICAL!)
- [ ] Bash-Syntax valide (Basic-Check)
- [ ] Hook-Name valide
- [ ] Datei geschrieben
- [ ] chmod +x ausgeführt
- [ ] (Optional) settings.json updated
- [ ] User erhält Testing-Instructions

---

## Best Practices

**Do's**:
- IMMER `trap 'exit 0' ERR` einbauen
- IMMER mit `exit 0` enden
- Background execution nutzen: `(long_task &)`
- Logging implementieren
- Pfad-Patterns validieren
- Testing-Instructions geben

**Don'ts**:
- NIEMALS ohne exit 0 enden
- Keine blocking operations ohne &
- Keine unvalidierten User-Inputs in Bash
- Keine Hooks ohne chmod +x
- Keine komplexe Logic ohne Error-Handling

---

## Security Considerations

**Wichtig**:
- Validiere File-Paths (keine Injection)
- Nutze `jq` für JSON-Parsing (nicht `eval`)
- Quote variables: `"$var"` nicht `$var`
- Prüfe ob Files existieren vor Zugriff
- Limitiere Schreibrechte auf spezifische Pfade

**Beispiel Secure Path Check**:
```bash
should_process_path() {
  local path="$1"
  # Use explicit pattern matching, not wildcards
  for pattern in "${MONITORED_PATHS[@]}"; do
    [[ "$path" =~ $pattern ]] && return 0
  done
  return 1
}
```

---

## Examples

### Post-Tool-Use Beispiel

```
User: /create-hook markdown-validator

Typ: post-tool-use
Name: markdown-validator
Tools: Write, Edit
Pfade: ideas/, knowledge/
Logic: Validate frontmatter, check broken links

→ Erstellt: .claude/hooks/markdown-validator.sh
→ Executable: chmod +x applied
→ Config: Added to settings.json
```

### Stop Hook Beispiel

```
User: /create-hook session-summary

Typ: stop
Name: session-summary
Output: knowledge/sessions/
Format: markdown
Track: Timestamp, Tools, Files, Topics

→ Erstellt: .claude/hooks/session-summary.sh
→ Executable: chmod +x applied
→ Summaries: knowledge/sessions/session-YYYYMMDD-HHMMSS.md
```

---

## Related Commands

- `/create-agent` - Agent erstellen
- `/create-command` - Command erstellen
- `/create-skill` - Skill erstellen

**Template-Creator Skill**: Dieser Command kann auch durch den `template-creator` Skill getriggert werden.

---

**Wichtig**:
- Hooks MÜSSEN mit `exit 0` enden
- chmod +x MUSS ausgeführt werden
- Background execution für lange Tasks: `(task &)`
- Validiere Bash-Syntax
- Teste nach Erstellung
