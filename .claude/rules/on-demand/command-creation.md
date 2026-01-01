# Command-Erstellung

**Priorität**: KRITISCH

Regeln für das Erstellen neuer Slash-Commands.

## Bei JEDEM neuen Command

1. **Command-Datei erstellen**:
   ```
   .claude/commands/{name}.md
   ```

2. **Plain-Text Trigger hinzufügen**:
   ```
   .claude/workflow-patterns.md
   ```

3. **Dokumentation aktualisieren**:
   ```
   .claude/COMMANDS.md
   ```

## Keine Commands ohne Plain-Text Detection!

Ein Command ohne Trigger-Patterns ist nutzlos für normale User-Interaktion.

## Checkliste

- [ ] Command-Datei in `.claude/commands/` erstellt
- [ ] Trigger-Patterns in `workflow-patterns.md` definiert
- [ ] Command in `COMMANDS.md` dokumentiert
- [ ] Model-Empfehlung angegeben (opus/sonnet/haiku)

## Template

```markdown
# /command-name

Kurze Beschreibung was der Command tut.

## Trigger-Patterns
- "natürliche phrase 1"
- "natürliche phrase 2"

## Model: haiku|sonnet|opus

## Workflow
[Steps...]
```
