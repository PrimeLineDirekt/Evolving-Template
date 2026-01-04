---
description: Session-Handoff erstellen für Kontextwechsel oder Pause
model: haiku
---

Du erstellst ein strukturiertes Handoff-Dokument für Session-Übergaben.

**Features:**
- Learning-Extraktion am Ende komplexer Sessions
- `--detailed` Flag für Enhanced Session Notes

---

## KRITISCH: Workflow-Reihenfolge

```
1. Analysieren (intern, kein Output)
2. mkdir -p _handoffs
3. Write Tool ausführen (PFLICHT!)
4. Erst NACH Write: User kurz informieren
```

**⚠️ NIEMALS Handoff-Inhalt im Chat anzeigen!**
Der User sieht den Inhalt in der gespeicherten Datei.

---

## Schritt 1: Analysieren (KEIN Output!)

Sammle INTERN (nicht im Chat ausgeben):

1. **Was wurde gemacht?** - Aktionen, Dateien, Entscheidungen
2. **Was ist offen?** - TODOs, Fragen, Issues
3. **Nächster Schritt?** - Konkrete nächste Aktion

---

## Schritt 2: Ordner erstellen

```bash
mkdir -p _handoffs
```

---

## Schritt 3: Write Tool SOFORT ausführen

**JETZT Write Tool aufrufen** mit Pfad: `_handoffs/YYYY-MM-DD-{topic}.md`

Nutze dieses Template für den Datei-Inhalt:

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
| Entscheidung | Begründung | Datum |
|--------------|------------|-------|
| {Entscheidung 1} | {Warum} | {YYYY-MM-DD} |

---

## Offene Punkte

### Noch zu tun
- [ ] {Task 1} - {Priorität}
- [ ] {Task 2} - {Priorität}

### Offene Fragen
- {Frage 1}?

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
- `{datei1}` - {warum}
- `{datei2}` - {warum}

---

## Quick Summary

```
Letzte Session: {TOPIC}
Stand: {1-Satz}
Nächster Schritt: {konkret}
Dateien: {wichtigste}
```
```

---

## Schritt 4: User informieren (NACH Write!)

**Erst wenn Write erfolgreich war**, kurze Bestätigung:

```
✅ Handoff gespeichert: `_handoffs/{filename}.md`

Nächste Session: @_handoffs/{filename}.md

Zusammenfassung:
- Erreicht: {1 Satz}
- Offen: {1 Satz}
- Nächster Schritt: {konkret}
```

**Das ist ALLES was im Chat erscheint!** Kein Handoff-Inhalt!

---

## Schritt 5: Learning-Extraktion (Optional)

**Complexity Score berechnen:**

| Indikator | Punkte |
|-----------|--------|
| Mehrere Retries/Korrekturen | +2 |
| User-Feedback zur Korrektur | +2 |
| Neuer Ansatz entwickelt | +2 |
| Multi-Step Problemlösung | +1 |
| Externe Recherche nötig | +1 |

**Score ≥ 3?** → Frage ob Learning gespeichert werden soll.

---

## Enhanced Mode: `--detailed`

Bei `--detailed` oder langen Sessions:
- Nutze 10-Section Template aus `.claude/templates/session-notes-template.md`
- Mehr Details zu Errors, Workflow, Learnings

---

## Checkliste vor Abschluss

- [ ] Write Tool wurde ausgeführt (nicht nur Text generiert!)
- [ ] Datei existiert in `_handoffs/`
- [ ] User wurde informiert (kurz, nicht der volle Inhalt)
