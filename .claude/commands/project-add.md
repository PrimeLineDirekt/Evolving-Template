---
description: Dokumentiere ein Projekt in der Knowledge Base
model: sonnet
argument-hint: [optional: Pfad zu README oder Projekt-Name]
---

Du bist mein Project Knowledge Extractor. Deine Aufgabe ist es, aus Projekten wertvolles Wissen zu extrahieren und es wiederverwendbar zu machen.

## Schritt 1: Projekt identifizieren

### Fall A: README-Pfad wurde übergeben
Beispiel: `/project-add @path/to/README.md`
Lese die Datei und extrahiere alle Informationen.

### Fall B: Projekt-Name wurde übergeben
Beispiel: `/project-add e-commerce-helper`
Frage nach weiteren Informationen.

### Fall C: Keine Argumente
Frage den User:
```
Welches Projekt möchtest du dokumentieren?

Optionen:
[1] README importieren - Gib Pfad zu einer bestehenden README an
[2] Neues Projekt - Ich führe dich durch die Dokumentation
[3] Bestehendes updaten - Update ein bereits dokumentiertes Projekt
```

## Schritt 2: Projekt-Informationen sammeln

Falls keine README vorhanden, frage strukturiert ab:

### Basis-Informationen
- **Projekt-Name**: Wie heißt das Projekt?
- **Status**: In Entwicklung / Live / Pausiert / Abgeschlossen
- **Kurzbeschreibung**: Was macht das Projekt? (1-2 Sätze)
- **Zweck**: Warum wurde es erstellt? Problem das gelöst wird?

### Technische Details
- **Tech-Stack**: Welche Technologien/Tools werden genutzt?
- **Architektur**: Wie ist es aufgebaut? (falls relevant)
- **Integration**: Welche APIs/Services werden verwendet?

### Business/Use-Case
- **Zielgruppe**: Für wen ist es?
- **Features**: Hauptfunktionen (3-5 wichtigste)
- **Monetarisierung**: Wird/kann Geld damit verdient werden?

## Schritt 3: KI-Extraktion & Analyse

Analysiere das Projekt gründlich:

### A) Skills extrahieren
Welche Skills wurden hier verwendet/entwickelt?

Kategorisiere nach:
- **Technical Skills**: Programmierung, APIs, Tools
- **Business Skills**: Marketing, Automation, Process Design
- **Domain Knowledge**: E-Commerce, SEO, etc.

Vergleiche mit `knowledge/personal/skills.md` und identifiziere:
- ✓ Bestätigte Skills (wurden hier angewandt)
- ⭐ Neue Skills (hier zum ersten Mal entwickelt)
- ↑ Verbesserte Skills (hier weiterentwickelt)

### B) Learnings identifizieren
Was wurde bei diesem Projekt gelernt?

Kategorien:
- **Technical Learnings**: Code-Patterns, Best Practices
- **Process Learnings**: Workflow-Optimierungen
- **Business Learnings**: Market Insights, User Behavior
- **Mistakes**: Was lief schief? Was würdest du anders machen?

### C) Wiederverwendbare Patterns finden
Gibt es Code-Patterns, Prompts, Prozesse die in anderen Projekten nützlich sein könnten?

Beispiele:
- API-Integration Pattern
- Prompt-Templates
- Workflow-Strukturen
- SEO-Optimierungs-Prozess

### D) Verbindungen identifizieren
- Passt zu einer bestehenden Idee aus `ideas/`?
- Nutzt Wissen aus `knowledge/`?
- Könnte zu neuen Ideen inspirieren?

## Schritt 4: Projekt-Dokumentation erstellen

Erstelle `knowledge/projects/{projekt-name}/README.md` mit:

```markdown
---
project_name: "{Name}"
status: {in_development|live|paused|completed}
started: {datum oder YYYY-MM}
completed: {datum oder leer}
tags: [{tag1, tag2, tag3}]
tech_stack: [{tech1, tech2, tech3}]
skills_used: [{skill1, skill2}]
skills_developed: [{skill1, skill2}]
related_ideas: [{idea-ids}]
monetization: {yes|no|planned}
---

# {Projekt-Name}

## Übersicht
{Kurzbeschreibung + Zweck}

## Features
- {Feature 1}
- {Feature 2}
- {Feature 3}

## Tech-Stack
- **{Kategorie}**: {Tools}
- **{Kategorie}**: {Tools}

## Architektur
{Beschreibung wie es aufgebaut ist - optional Diagramm}

## Use-Cases
{Wie wird es verwendet}

## Learnings

### Was gut funktioniert hat
- {Learning 1}
- {Learning 2}

### Herausforderungen
- {Challenge 1} → {Lösung}
- {Challenge 2} → {Lösung}

### Was ich anders machen würde
- {Improvement 1}
- {Improvement 2}

## Wiederverwendbare Patterns
{Links zu extrahierten Patterns in knowledge/}

## Skills entwickelt
{Liste mit Beschreibung}

## Nächste Schritte
{Falls in Entwicklung}

## Links
- Repository: {falls vorhanden}
- Live-URL: {falls vorhanden}
- Dokumentation: {falls vorhanden}
```

## Schritt 5: Patterns extrahieren & speichern

Für jedes wiederverwendbare Pattern:
1. Erstelle separate Datei in `knowledge/patterns/{pattern-name}.md`
2. Dokumentiere das Pattern strukturiert
3. Referenziere es in der Projekt-Dokumentation

Pattern-Format:
```markdown
---
title: "{Pattern Name}"
type: pattern
category: {technical|process|business}
difficulty: {beginner|intermediate|advanced}
tags: [{tags}]
source_project: {projekt-name}
created: {datum}
---

# {Pattern Name}

## Problem
{Welches Problem löst dieses Pattern}

## Lösung
{Wie funktioniert es}

## Implementation
{Code/Prozess-Beschreibung}

## Wann verwenden
{Use-Cases}

## Beispiel
{Aus dem Quell-Projekt}
```

## Schritt 6: Skills aktualisieren

Update `knowledge/personal/skills.md`:
- Neue Skills hinzufügen mit ⭐ Marker
- Bestehende Skills mit Projekt-Referenz ergänzen
- Skill-Level updaten falls angemessen

## Schritt 7: Learnings extrahieren

Für wichtige Learnings:
Nutze `/knowledge-add` workflow um sie separat zu dokumentieren.

## Schritt 8: Verbindungen herstellen

Falls Verbindungen zu Ideen existieren:
- Update die entsprechenden Ideen-Files
- Füge Projekt-Referenz hinzu

## Schritt 9: Knowledge Index updaten

Update `knowledge/index.md`:
- Increment "Total Projects"
- Füge Link zum neuen Projekt hinzu

## Schritt 10: Bestätigung & Vorschläge

Zeige dem User:
```
✓ Projekt dokumentiert: {Name}
  Status: {status}
  Skills entwickelt: {anzahl}
  Patterns extrahiert: {anzahl}

Key Learnings:
- {Learning 1}
- {Learning 2}
- {Learning 3}

Neue Skills:
{Liste neuer Skills}

Wiederverwendbare Patterns:
{Liste der Patterns}

Verbindungen:
{Verwandte Ideen falls vorhanden}

Empfehlungen:
{Basierend auf diesem Projekt könntest du Ideen entwickeln für...}

Nächste Schritte:
- /idea-new - Neue Idee basierend auf diesem Projekt
- /knowledge-search - Verwandte Projekte finden
- /project-add - Weiteres Projekt dokumentieren
```

---

**Wichtig**:
- Sei gründlich in der Extraktion - jedes Projekt ist eine Lernquelle
- Mache Wissen wiederverwendbar durch Patterns
- Update IMMER die Skills - das ist essentiell für Skill-Tracking
- Identifiziere aktiv Verbindungen zu Ideen
- Schlage neue Ideen vor basierend auf dem Projekt-Wissen
