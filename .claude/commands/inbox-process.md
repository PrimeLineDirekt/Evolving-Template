---
description: Verarbeite Dateien aus der Inbox automatisch
model: haiku
---

Du bist mein Inbox-Processing-Engine. Deine Aufgabe ist es, Dateien aus `_inbox/` zu analysieren, zu kategorisieren und ins System einzupflegen.

## Schritt 1: Inbox scannen

Liste alle Dateien in `_inbox/`:
- Ignoriere `.gitkeep`, `README.md`
- Verarbeite: `.md`, `.txt`, `.pdf` (falls unterstützt)

Falls keine Dateien:
```
📭 Inbox ist leer

Lege Dateien in _inbox/ ab und sage mir Bescheid!
```

Falls Dateien gefunden:
```
📬 {anzahl} Datei(en) in der Inbox gefunden

Starte Verarbeitung...
```

## Schritt 2: Jede Datei analysieren

Für jede Datei:

### A) Datei lesen
Nutze Read-Tool um vollständigen Inhalt zu laden.

### B) Intelligente Kategorisierung

Analysiere den Inhalt und bestimme den **Typ**:

#### Typ 1: Projekt-README
**Erkennungsmerkmale:**
- Beschreibt Projekt/Tool/System
- Enthält Abschnitte wie: Features, Tech-Stack, Installation, Use-Cases
- Dokumentations-Charakter
- Oft technische Details

**Beispiel-Indikatoren:**
- "# Project Name"
- "## Features"
- "## Installation"
- "Tech Stack", "Architecture"
- Beschreibt WAS gebaut wurde

#### Typ 2: Prompt/Template
**Erkennungsmerkmale:**
- Strukturierter AI-Prompt
- Anweisungen für KI-Systeme
- Template-Charakter
- Wiederverwendbare Instruktionen

**Beispiel-Indikatoren:**
- "Du bist ein..."
- "Deine Aufgabe ist..."
- Klare Anweisungsstruktur
- Variablen/Platzhalter
- "System:", "User:", "Assistant:"

#### Typ 3: Idee
**Erkennungsmerkmale:**
- Beschreibt NEUE Geschäftsidee/Konzept
- Zukunftsorientiert ("könnte", "würde")
- Noch nicht umgesetzt
- Opportunity/Problem-Lösung

**Beispiel-Indikatoren:**
- "Idee:", "Konzept:"
- Beschreibt Potential
- Market Need
- Innovation
- "Das könnte funktionieren weil..."

#### Typ 4: Learning/Note
**Erkennungsmerkmale:**
- Erkenntnis aus Erfahrung
- Best Practice
- Notiz zu Thema
- Ressourcen-Sammlung

**Beispiel-Indikatoren:**
- "Ich habe gelernt..."
- "Best Practice für..."
- "Wichtige Ressourcen:"
- Reflektiv

**Entscheidungs-Baum:**
```
Beschreibt es ein bestehendes Projekt?
├─ Ja → Projekt-README
└─ Nein
   └─ Ist es eine Anweisung/Prompt?
      ├─ Ja → Prompt
      └─ Nein
         └─ Beschreibt es eine neue Idee?
            ├─ Ja → Idee
            └─ Nein → Learning/Note
```

**Confidence-Level:**
Gib an wie sicher du bist (0-10).
Falls < 7: Frage User nach Bestätigung.

### C) Metadata extrahieren

Je nach Typ:

**Für Projekte:**
- Projekt-Name
- Tech-Stack
- Features (Top 3-5)
- Status

**Für Prompts:**
- Zweck
- Use-Case
- Variablen

**Für Ideen:**
- Titel
- Kategorie (grob)
- Problem das gelöst wird

**Für Learnings:**
- Thema
- Key Insight
- Kontext

## Schritt 3: Bestätigung (bei Unsicherheit)

Falls Confidence < 7:
```
📄 Datei: {filename}

Meine Analyse:
Typ: {typ} (Confidence: {score}/10)
{Kurze Begründung}

Stimmt das?
[1] Ja, korrekt
[2] Nein, es ist: {alternative Optionen}
```

## Schritt 4: Passenden Workflow ausführen

### Typ: Projekt-README
```
→ Führe /project-add aus

Nutze den Datei-Content als Input.
Importiere als README.
```

### Typ: Prompt
```
→ Führe /knowledge-add aus

Type: prompt
Content: {Datei-Inhalt}
Auto-kategorisiere basierend auf Zweck
```

### Typ: Idee
```
→ Führe /idea-new aus

Beschreibung: {Datei-Inhalt}
Lass KI-Analyse wie gewohnt laufen
```

### Typ: Learning/Note
```
→ Führe /knowledge-add aus

Type: learning oder note (je nachdem)
Content: {Datei-Inhalt}
```

## Schritt 5: Verarbeitungs-Status

Während der Verarbeitung zeige:
```
📄 Verarbeite: {filename}
   Typ: {typ}
   Workflow: {workflow}
   Status: ⏳ In Arbeit...
```

Nach erfolgreicher Verarbeitung:
```
   Status: ✅ Verarbeitet
   Gespeichert: {pfad zum neuen Dokument}
```

## Schritt 6: Cleanup-Frage

Nach jeder verarbeiteten Datei:
```
✅ {filename} wurde verarbeitet als: {typ}
   Neuer Speicherort: {pfad}

Original-Datei in _inbox/ löschen?
[1] Ja, löschen
[2] Nein, behalten
[3] In Archiv verschieben
```

Führe User-Entscheidung aus.

Falls "Archiv": Erstelle `_inbox/archive/` und verschiebe dort hin.

## Schritt 7: Zusammenfassung

Nach allen Dateien:
```
═══════════════════════════════════
📬 Inbox-Verarbeitung abgeschlossen
═══════════════════════════════════

Verarbeitet: {anzahl} Datei(en)

Breakdown:
├─ Projekte: {anzahl}
├─ Prompts: {anzahl}
├─ Ideen: {anzahl}
└─ Knowledge: {anzahl}

Details:
────────────────────────────────────
✓ {filename} → {typ} → {speicherort}
✓ {filename} → {typ} → {speicherort}
...

Nächste Schritte:
• /idea-list - Neue Ideen anschauen
• /knowledge-search - Neues Wissen durchsuchen
• Weitere Dateien in _inbox/ ablegen
```

## Schritt 8: Error-Handling

### Datei kann nicht gelesen werden
```
❌ Fehler bei {filename}
   Grund: {error}
   Aktion: Übersprungen

→ Bitte prüfe die Datei
```

### Typ nicht eindeutig bestimmbar
```
❓ {filename} konnte nicht eindeutig kategorisiert werden

Inhalt scheint: {mögliche Typen}

Bitte gib an:
[1] Projekt
[2] Prompt
[3] Idee
[4] Learning/Note
[5] Überspringen
```

### Workflow-Fehler
```
❌ Fehler beim Verarbeiten von {filename}
   Workflow: {workflow}
   Fehler: {error}

Datei bleibt in _inbox/ für manuelle Verarbeitung.
```

## Schritt 9: Plain Text Trigger Erkennung

Dieser Workflow kann auch getriggert werden durch:
- "Verarbeite die Inbox"
- "Neue Dateien in der Inbox"
- "Schau mal in _inbox"
- "Inbox durchgehen"

Wenn du solche Phrasen im normalen Chat erkennst, frage:
"Soll ich /inbox-process ausführen?"

---

**Wichtig**:
- Sei gründlich in der Analyse - falsche Kategorisierung führt zu Chaos
- Bei Unsicherheit IMMER fragen
- Nutze die bestehenden Workflows - keine neuen Files manuell erstellen
- Dokumentiere was wohin ging in der Zusammenfassung
- Cleanup ist wichtig - Inbox soll nicht zumüllen
- Confidence-Level ehrlich einschätzen
