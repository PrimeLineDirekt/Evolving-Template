# Cross-Reference Sync

**Priorität**: KRITISCH

Bei Änderungen an Projekten, Patterns, Learnings oder Prompts müssen diese 5 Dateien synchron gehalten werden:

## Betroffene Dateien

1. `README.md` - System Overview & Stats
2. `.claude/CONTEXT.md` - Technical Context & Structure
3. `knowledge/index.md` - Knowledge Base Index
4. `START.md` - User Stats
5. `.claude/SYSTEM-MAP.md` - Komponenten-Inventar

## Trigger

Diese Regel wird ausgelöst bei:
- Neues Projekt hinzugefügt
- Neues Pattern erstellt
- Neues Learning dokumentiert
- Neuer Prompt erstellt
- Statistiken ändern sich (Counts)

## Workflow

```
Änderung gemacht
     ↓
Prüfe alle 5 Dateien
     ↓
Update Stats/Counts/Listen
     ↓
Konsistenz sicherstellen
```

## Beispiel: Neues Pattern

Wenn `knowledge/patterns/new-pattern.md` erstellt wird:

1. `knowledge/patterns/README.md` - Pattern zur Liste hinzufügen
2. `knowledge/index.md` - Pattern Count erhöhen, Pattern listen
3. `README.md` - Pattern Count in Stats erhöhen
4. `START.md` - Pattern Count erhöhen
5. `.claude/CONTEXT.md` - Pattern in Struktur & Stats einfügen
6. `.claude/SYSTEM-MAP.md` - Changelog updaten
