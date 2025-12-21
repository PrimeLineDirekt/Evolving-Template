---
description: Session-Handoff erstellen für Kontextwechsel oder Pause
model: haiku
---

Du erstellst ein strukturiertes Handoff-Dokument für Session-Übergaben. Perfekt wenn:
- Die Session lang wird und Context knapp
- Du eine Pause machst
- Du den Kontext an eine neue Session übergeben willst

---

## Schritt 1: Aktuellen Stand analysieren

**Sammle Informationen über**:

1. **Was wurde gemacht?**
   - Lies die letzten Aktionen aus dem Kontext
   - Welche Dateien wurden erstellt/geändert?
   - Welche Entscheidungen wurden getroffen?

2. **Was ist noch offen?**
   - Offene TODOs
   - Ungelöste Fragen
   - Bekannte Issues

3. **Was ist der nächste logische Schritt?**
   - Unmittelbar nächste Aktion
   - Abhängigkeiten

---

## Schritt 2: Handoff-Dokument erstellen

**Speichere als**: `_handoffs/YYYY-MM-DD-{topic}.md`

```markdown
# Session Handoff: {TOPIC}

**Erstellt**: {DATUM} {UHRZEIT}
**Session-Dauer**: ~{geschätzt}
**Kontext-Nutzung**: {hoch/mittel/niedrig}

---

## Was wurde erreicht

### Abgeschlossen
- [x] {Task 1}
- [x] {Task 2}

### Erstellt/Geändert
| Datei | Aktion | Beschreibung |
|-------|--------|--------------|
| {path} | Created | {was} |
| {path} | Modified | {was geändert} |

### Entscheidungen
- **{Entscheidung 1}**: {Begründung}
- **{Entscheidung 2}**: {Begründung}

---

## Offene Punkte

### Noch zu tun
- [ ] {Task 1} - {Priorität}
- [ ] {Task 2} - {Priorität}

### Offene Fragen
- {Frage 1}?
- {Frage 2}?

### Bekannte Issues
- {Issue}: {Beschreibung}

---

## Nächste Session

### Empfohlener Einstieg
```
@_handoffs/YYYY-MM-DD-{topic}.md - Fortsetzung
```

### Sofort-Aktionen
1. {Erste Aktion}
2. {Zweite Aktion}

### Kontext laden
Diese Dateien sind relevant:
- `{datei1}` - {warum}
- `{datei2}` - {warum}

---

## Quick Summary (Copy-Paste für neue Session)

```
Letzte Session: {TOPIC}

Stand:
- {1-Satz was gemacht wurde}

Nächster Schritt:
- {konkrete nächste Aktion}

Relevante Dateien:
- {datei1}
- {datei2}
```
```

---

## Schritt 3: Ordner erstellen falls nötig

```bash
mkdir -p _handoffs
```

---

## Schritt 4: User informieren

```markdown
## Session Handoff erstellt

**Gespeichert**: `_handoffs/{filename}.md`

### Für die nächste Session

Starte mit:
```
@_handoffs/{filename}.md - Fortsetzung
```

Oder kopiere den Quick Summary oben.

### Zusammenfassung

**Erreicht**: {kurz}
**Offen**: {kurz}
**Nächster Schritt**: {konkret}
```

---

## Automatische Erkennung

**Dieser Command wird vorgeschlagen wenn**:
- Session länger als 30 Minuten
- Viele Dateien geändert wurden
- User sagt "Pause", "später", "morgen weiter"
- Context-Warnung erscheint

---

## Beispiel Output

```markdown
# Session Handoff: GitHub Repo Analyzer Integration

**Erstellt**: 2025-12-01 14:30
**Session-Dauer**: ~2h
**Kontext-Nutzung**: hoch

---

## Was wurde erreicht

### Abgeschlossen
- [x] github-repo-analyzer-agent erstellt
- [x] /analyze-repo Command erstellt
- [x] SYSTEM-MAP.md erstellt
- [x] better-agents analysiert und integriert

### Erstellt/Geändert
| Datei | Aktion | Beschreibung |
|-------|--------|--------------|
| .claude/agents/github-repo-analyzer-agent.md | Created | Dual-System Analyzer |
| .claude/commands/analyze-repo.md | Created | Repo Analysis Command |
| .claude/SYSTEM-MAP.md | Created | System Inventory |
| .mcp.json | Created | MCP Configuration |

---

## Nächste Session

### Sofort-Aktionen
1. Claude Code neu starten (für neue Commands)
2. /analyze-repo testen

### Kontext laden
- `.claude/SYSTEM-MAP.md`
- `knowledge/learnings/better-agents-patterns.md`
```

---

## Related

- `/sparring` - Für Brainstorming vor Handoff
- `/system-health` - System-Status prüfen
- `START.md` - Standard Session-Einstieg
