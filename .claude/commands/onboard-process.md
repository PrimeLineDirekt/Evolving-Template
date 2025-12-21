---
description: Verarbeite ausgefüllten Onboarding-Fragebogen
model: sonnet
---

Du bist mein Onboarding-Processing-Engine. Deine Aufgabe ist es, den ausgefüllten `_ONBOARDING.md` Fragebogen zu lesen, alle Informationen zu extrahieren und ins System einzupflegen.

## Schritt 1: Fragebogen laden

Lese `_ONBOARDING.md` vollständig.

Falls Datei nicht existiert:
```
❌ _ONBOARDING.md nicht gefunden

Soll ich das Onboarding-Dokument erstellen?
Falls du es schon ausgefüllt hast, prüfe den Dateinamen.
```

Falls Datei leer oder kaum ausgefüllt:
```
📋 _ONBOARDING.md gefunden aber scheint noch leer zu sein

Möchtest du:
[1] Trotzdem verarbeiten (falls minimal ausgefüllt)
[2] Abbrechen und erst ausfüllen
```

## Schritt 2: Alle Abschnitte parsen

Lese und parse systematisch jeden Abschnitt:

### Parsing-Logik

**Erkennung ob ausgefüllt:**
- Nur `<!-- Kommentare -->` → Leer
- Nur `---` Trennlinien → Leer
- Nur Fragen-Titel → Leer
- **Echter Content** (Text, Stichpunkte, Antworten) → Ausgefüllt

**Was extrahieren:**
- A) Persönliche Informationen
- B) Skills (Technical, Business, Soft, Lernwünsche)
- C) Projekte (alle Projekt-Blöcke)
- D) Ideen (alle Ideen-Blöcke)
- E) Prompts (alle Prompt-Blöcke)
- F) Ziele & Vision
- G) Interessen & Themen
- H) Learnings & Erkenntnisse
- I) Zusätzliche Informationen

## Schritt 3: Preview & Bestätigung

Zeige dem User was du gefunden hast:

```
═══════════════════════════════════
📋 Onboarding-Fragebogen Analyse
═══════════════════════════════════

Gefundene Informationen:

✓ Persönliche Infos: Ja
✓ Skills: {anzahl} Technical, {anzahl} Business, {anzahl} Soft
✓ Projekte: {anzahl} gefunden
✓ Ideen: {anzahl} gefunden
✓ Prompts: {anzahl} gefunden
✓ Learnings: {anzahl} gefunden
✓ Ziele & Vision: Ja
✓ Interessen: {anzahl} Themen

Details:
────────────────────────────────────

Projekte:
1. {Projekt-Name} - {Status}
2. {Projekt-Name} - {Status}

Ideen:
1. {Ideen-Titel}
2. {Ideen-Titel}

Prompts:
1. {Prompt-Name}
2. {Prompt-Name}

────────────────────────────────────

Ich werde jetzt:
→ Persönliche Infos in about-me.md einpflegen
→ Skills in skills.md einpflegen
→ {anzahl} Projekte mit /project-add verarbeiten
→ {anzahl} Ideen mit /idea-new erfassen
→ {anzahl} Prompts mit /knowledge-add speichern
→ {anzahl} Learnings mit /knowledge-add speichern

Soll ich fortfahren?
[Ja / Nein / Zeig mir mehr Details]
```

Falls "Zeig mir mehr Details": Zeige ausführliche Preview aller Inhalte.

## Schritt 4: Verarbeitung durchführen

### A) Persönliche Informationen

Lese `knowledge/personal/about-me.md` und **update/ergänze**:

```markdown
# About Me

## Persönliche Informationen
**Name**: {aus Fragebogen}
**Hintergrund**: {aus Fragebogen}
**Standort**: {aus Fragebogen}
**Status**: {aus Fragebogen}

## Working Style
{aus Fragebogen: Arbeitsweise}

## Motivation & Antrieb
{aus Fragebogen: Was treibt dich an}

## Ziele

### Kurzfristig (3 Monate)
{aus Abschnitt F}

### Mittelfristig (1 Jahr)
{aus Abschnitt F}

### Langfristig (3-5 Jahre)
{aus Abschnitt F}

## Interessen & Themen
{aus Abschnitt G}
- {Thema 1}
- {Thema 2}

## Communities & Netzwerke
{aus Abschnitt G}

{Behalte bestehenden Content, füge neues hinzu}
```

### B) Skills

Lese `knowledge/personal/skills.md` und **update/ergänze**:

**Strategie:**
- Merge neue Skills mit bestehenden
- Füge Level hinzu wenn angegeben
- Markiere neue Skills mit `⭐ Neu`
- Organisiere nach Kategorien

```markdown
# Skills

## Technical Skills

### Programmierung
{aus Fragebogen - merge mit bestehendem}

### Tools & Plattformen
{aus Fragebogen - merge}

### AI & Automation
{aus Fragebogen - merge}

## Business Skills

### Marketing & Sales
{aus Fragebogen - merge}

### E-Commerce
{aus Fragebogen - merge}

## Soft Skills

### Kreativität & Innovation
{aus Fragebogen}

### Analytisches Denken
{aus Fragebogen}

## Skills zu entwickeln
{aus Abschnitt B: "Skills die ich lernen möchte"}
```

### C) Projekte verarbeiten

Für **jedes gefundene Projekt**:

1. Extrahiere alle Projekt-Informationen
2. Prüfe ob README-Pfad angegeben
   - **Falls Ja**: Lese README von dort
   - **Falls Nein**: Nutze die ausgefüllten Infos
3. **Führe `/project-add` Workflow aus** mit den Daten
4. Tracke Fortschritt:
   ```
   📦 Verarbeite Projekt 1/3: {Name}
      Status: ⏳ In Arbeit...
   ```

**Nach jedem Projekt:**
```
   Status: ✅ Verarbeitet
   Gespeichert: knowledge/projects/{name}/
```

### D) Ideen erfassen

Für **jede gefundene Idee**:

1. Extrahiere alle Ideen-Informationen
2. Bereite Input für `/idea-new` vor:
   - Beschreibung + Problem + Zielgruppe kombinieren
   - Kategorie vorschlagen
   - Monetarisierung notieren
3. **Führe `/idea-new` Workflow aus**
4. Tracke Fortschritt:
   ```
   💡 Verarbeite Idee 1/2: {Titel}
      Status: ⏳ Analysiere...
   ```

**Nach jeder Idee:**
```
   Status: ✅ Erfasst
   ID: idea-2024-001
   Potential: {score}/10
```

### E) Prompts speichern

Für **jeden gefundenen Prompt**:

1. Extrahiere:
   - Name/Zweck
   - Der Prompt selbst (aus ``` Block oder Datei)
   - Verwendung
2. **Führe `/knowledge-add` aus** mit type: prompt
3. Tracke Fortschritt:
   ```
   📝 Verarbeite Prompt 1/3: {Name}
      Status: ⏳ Speichere...
   ```

**Nach jedem Prompt:**
```
   Status: ✅ Gespeichert
   Pfad: knowledge/prompts/{category}/{name}.md
```

### F) Learnings speichern

Für **jedes gefundene Learning**:

1. Extrahiere:
   - Was gelernt
   - Kontext
   - Warum wichtig
2. **Führe `/knowledge-add` aus** mit type: learning
3. Für Best Practices: Speichere als separates Learning
4. Für Fehler: Speichere mit "Fehler → Learning" Format

**Tracke Fortschritt** wie bei Prompts.

## Schritt 5: Zusammenfassung

Nach vollständiger Verarbeitung:

```
═══════════════════════════════════
✅ Onboarding abgeschlossen!
═══════════════════════════════════

Erfolgreich verarbeitet:

📋 Persönliche Informationen
   → knowledge/personal/about-me.md (updated)

🎯 Skills
   → knowledge/personal/skills.md (updated)
   → {anzahl} neue Skills hinzugefügt
   → {anzahl} bestehende Skills erweitert

📦 Projekte: {anzahl}
   ✓ {Projekt 1} → knowledge/projects/{name}/
   ✓ {Projekt 2} → knowledge/projects/{name}/
   Skills extrahiert: {skills}

💡 Ideen: {anzahl}
   ✓ {Idee 1} - idea-2024-001 (Potential: {score}/10)
   ✓ {Idee 2} - idea-2024-002 (Potential: {score}/10)

📝 Prompts: {anzahl}
   ✓ {Prompt 1} → knowledge/prompts/...
   ✓ {Prompt 2} → knowledge/prompts/...

🎓 Learnings: {anzahl}
   ✓ {Learning 1} → knowledge/learnings/...
   ✓ {Learning 2} → knowledge/learnings/...

════════════════════════════════════

Dein System kennt dich jetzt!

Nächste Schritte:
• /idea-list - Schau dir deine Ideen an
• /idea-connect - Finde Synergien
• /knowledge-search - Durchsuche dein Wissen
```

## Schritt 6: Cleanup

Frage den User:

```
📄 _ONBOARDING.md wurde vollständig verarbeitet

Soll ich die Original-Datei jetzt löschen?

[1] Ja, löschen (empfohlen)
[2] Nein, behalten
[3] In Archiv verschieben (_ONBOARDING_backup.md)
```

**Option 1**: Lösche `_ONBOARDING.md`
```
✓ _ONBOARDING.md gelöscht
```

**Option 2**: Behalte Datei
```
✓ Datei behalten - du findest sie weiterhin im Root
```

**Option 3**: Umbenennen
```
✓ Umbenannt zu: _ONBOARDING_backup.md
```

## Schritt 7: System-Status updaten

Update `.claude/CONTEXT.md`:
- Aktualisiere Stats (Ideas, Projects, Knowledge Items)
- Update "Last Activity"
- Notiere dass Onboarding abgeschlossen

## Schritt 8: Follow-up Aktionen vorschlagen

```
💡 Empfohlene nächste Schritte:

Basierend auf deinen Informationen:

1. **Synergien finden**
   → /idea-connect
   Deine {anzahl} Ideen könnten Synergien haben!

2. **Skill-Gap Analyse**
   → /idea-list gaps
   Zeigt welche Skills für Ideen fehlen

3. **Erste Idee ausarbeiten**
   → /idea-work {top-potential-idee}
   Starte mit deiner Top-Idee (Potential: {score}/10)

4. **Wissen durchsuchen**
   → /knowledge-search {relevantes-thema}
   Entdecke Verbindungen in deinem Wissen

Was möchtest du tun?
```

---

## Error-Handling

### Parsing-Fehler

Falls ein Abschnitt nicht geparst werden kann:
```
⚠️ Warnung: Abschnitt {name} konnte nicht vollständig geparst werden

Gefunden: {was ich verstanden habe}
Unklar: {was fehlt}

Soll ich:
[1] Mit dem was ich habe fortfahren
[2] Dich fragen wie ich es interpretieren soll
[3] Diesen Abschnitt überspringen
```

### Workflow-Fehler

Falls ein Sub-Workflow fehlschlägt:
```
❌ Fehler beim Verarbeiten von {item}
   Workflow: {workflow}
   Fehler: {error-message}

Ich fahre mit den anderen Items fort.
Dieses Item kannst du später manuell hinzufügen.
```

### Datei-Konflikte

Falls z.B. Projekt schon existiert:
```
⚠️ Projekt "{name}" existiert bereits in knowledge/projects/

Soll ich:
[1] Überschreiben mit neuen Infos
[2] Merge (bestehend + neu kombinieren)
[3] Überspringen
[4] Als neues Projekt "{name}-2" speichern
```

---

## Plain Text Trigger

Dieser Workflow kann auch getriggert werden durch:
- "Verarbeite das Onboarding"
- "Onboarding fertig"
- "Ich habe den Fragebogen ausgefüllt"

Wenn du solche Phrasen erkennst, frage:
"Soll ich /onboard-process ausführen?"

---

**Wichtig**:
- Sei geduldig beim Parsen - User können unterschiedlich formatieren
- Bei Unsicherheit: IMMER fragen statt raten
- Merge intelligent mit bestehendem Content, nicht überschreiben
- Tracke jeden Schritt damit User sieht was passiert
- Preview BEVOR du etwas machst
- Cleanup nur nach Bestätigung
- Schlage sinnvolle Follow-ups vor basierend auf den Daten
