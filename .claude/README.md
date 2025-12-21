# Claude Code Workflows - Dokumentation

Dieser Ordner (`.claude/`) enthält alle Workflows (Slash Commands) für das Evolving System.

---

## Was sind Workflows?

Workflows sind **Slash Commands** - wiederverwendbare, strukturierte Aufgaben die mit `/command` ausgeführt werden.

**Beispiel**:
```
/idea-new
```

Jeder Workflow ist eine Markdown-Datei in `.claude/commands/` die Claude anweist, eine spezifische Aufgabe durchzuführen.

---

## Alle verfügbaren Workflows

### 🎯 Ideen-Management

#### `/idea-new` - Neue Idee erfassen
**Purpose**: Idee mit vollständiger KI-Analyse erfassen

**Usage**:
```
/idea-new
```
oder mit Argument:
```
/idea-new Ein Tool das Online-Sellers beim Listing hilft
```

**Was passiert**:
1. Idee beschreiben (oder aus Argument)
2. KI analysiert:
   - Kategorie (auto)
   - Potential-Score (1-10 mit Begründung)
   - Benötigte Skills
   - Monetarisierungspotential
   - Verbindungen zu anderen Ideen/Projekten
3. Erstellt strukturiertes Markdown
4. Updated Index

**File**: `.claude/commands/idea-new.md`

---

#### `/idea-work` - An Idee arbeiten
**Purpose**: Iteratives Sparring für Ideenentwicklung

**Usage**:
```
/idea-work
```
oder mit ID:
```
/idea-work idea-2024-001
```
oder mit Filter:
```
/idea-work active
```

**Modes**:
- **Brainstorming**: Idee erweitern & neue Aspekte finden
- **Validierung**: Kritisch hinterfragen & Schwächen identifizieren
- **Konkretisierung**: Von Idee zu konkretem Umsetzungsplan
- **Problemlösung**: Spezifisches Problem/Blocker bearbeiten
- **Freies Sparring**: Du gibst die Richtung vor

**Was passiert**:
1. Idee auswählen (Liste/ID/Filter)
2. Modus wählen
3. Sparring Session
4. Fortschritt inline dokumentieren
5. Status/Timestamps updaten

**File**: `.claude/commands/idea-work.md`

---

#### `/idea-list` - Übersicht & Filter
**Purpose**: Dashboard für alle Ideen

**Usage**:
```
/idea-list
```
mit Filtern:
```
/idea-list status:active
/idea-list category:business
/idea-list potential:high
/idea-list recent
/idea-list stats
/idea-list matrix
```

**Views**:
- **Compact** (Standard): Kurze Liste
- **Detailed**: Vollständige Details
- **Stats**: Statistiken & Insights
- **Matrix**: Potential vs. Effort
- **Gaps**: Skill-Gap Analyse
- **Stale**: Lange nicht bearbeitete Ideen

**File**: `.claude/commands/idea-list.md`

---

#### `/idea-connect` - Synergien finden
**Purpose**: Connection Engine - findet Verbindungen zwischen Ideen

**Usage**:
```
/idea-connect
```
oder für spezifische Idee:
```
/idea-connect idea-2024-001
```

**Was passiert**:
1. Alle Ideen laden & analysieren
2. Verschiedene Verbindungstypen finden:
   - Thematische Überschneidungen
   - Gemeinsame Skills
   - Sequentielle Synergien (A → B)
   - Kombinatorische Synergien (A + B = C)
3. Synergie-Score berechnen (1-10)
4. Cluster identifizieren
5. Platform-Opportunities erkennen
6. Cross-References updaten
7. Neue kombinierte Ideen vorschlagen

**File**: `.claude/commands/idea-connect.md`

---

### 📚 Wissens-Management

#### `/knowledge-add` - Wissen hinzufügen
**Purpose**: Wissen strukturiert zur Knowledge Base hinzufügen

**Usage**:
```
/knowledge-add
```
oder mit Datei:
```
/knowledge-add @path/to/file.md
```

**Types**:
- **Prompt**: Wiederverwendbarer Prompt/Template
- **Learning**: Erkenntnis aus Projekt/Erfahrung
- **Resource**: Nützliche Ressource (Link, Tool, Methode)
- **Note**: Allgemeine Notiz/Wissen

**Was passiert**:
1. Type bestimmen
2. Content erfassen
3. **KI extrahiert**:
   - Key Insights
   - Skills
   - Themen & Tags
   - Verbindungen
4. Auto-Kategorisierung
5. Speichern in `knowledge/{category}/`
6. Skills updaten falls neu

**File**: `.claude/commands/knowledge-add.md`

---

#### `/knowledge-search` - Semantische Suche
**Purpose**: Knowledge Base durchsuchen

**Usage**:
```
/knowledge-search API Integration
```
oder als Frage:
```
/knowledge-search Wie optimiere ich Online-Listings?
```

**Was passiert**:
1. Query analysieren (Intent verstehen)
2. Durchsuchen:
   - Projects
   - Prompts
   - Personal Knowledge
   - Ideas
   - Learnings, Resources, Notes
3. Relevanz-Score (1-10)
4. Nach Gruppen sortieren (Direkt relevant / Verwandt)
5. Kontextuell präsentieren:
   - Standard-Format
   - Answer-First (bei Fragen)
   - Learning-Path (bei Skills)

**File**: `.claude/commands/knowledge-search.md`

---

#### `/project-add` - Projekt dokumentieren
**Purpose**: Wissen aus Projekten extrahieren und dokumentieren

**Usage**:
```
/project-add
```
oder mit README:
```
/project-add @path/to/README.md
```

**Was passiert**:
1. Projekt-Informationen sammeln (README oder abfragen)
2. **KI extrahiert**:
   - Skills (verwendet/neu entwickelt)
   - Learnings (was gut lief, Challenges)
   - Wiederverwendbare Patterns
   - Verbindungen zu Ideen
3. Projekt dokumentieren in `knowledge/projects/`
4. Patterns extrahieren → `knowledge/patterns/`
5. **Skills updaten** in `knowledge/personal/skills.md`
6. Learnings separat dokumentieren
7. Cross-References zu Ideen

**File**: `.claude/commands/project-add.md`

---

### 🔄 Automation

#### `/inbox-process` - Inbox verarbeiten
**Purpose**: Dateien aus `_inbox/` automatisch verarbeiten

**Usage**:
```
/inbox-process
```

**Was passiert**:
1. Scannt `_inbox/` nach Dateien (.md, .txt, .pdf)
2. Für jede Datei:
   - **Lesen & Analysieren**
   - **Typ bestimmen** (Projekt/Prompt/Idee/Learning)
     - Mit Confidence-Level (0-10)
     - Bei < 7: User fragen
   - **Passenden Workflow ausführen**:
     - Projekt-README → `/project-add`
     - Prompt → `/knowledge-add` (type: prompt)
     - Idee → `/idea-new`
     - Learning/Note → `/knowledge-add`
   - **Ins System einpflegen**
   - **Cleanup-Frage**: Original löschen/behalten/archivieren?
3. Zusammenfassung aller verarbeiteten Dateien

**Supported Formats**: `.md`, `.txt`, `.pdf`

**File**: `.claude/commands/inbox-process.md`

---

### 💭 Entwicklung & Sparring

#### `/sparring` - Freies Brainstorming
**Purpose**: Universal Thought-Partner & Brainstorming

**Usage**:
```
/sparring
```
oder mit Thema:
```
/sparring E-Commerce Trends
```

**Modes**:
1. **Freies Brainstorming**: Neue Ideen entwickeln
2. **Problem-Solving**: Spezifisches Problem lösen
3. **Strategie-Entwicklung**: Business/Projekt-Strategie
4. **Opportunitäts-Scan**: Neue Möglichkeiten finden
5. **Devil's Advocate**: Kritisch hinterfragen
6. **Wissens-Synthese**: Bestehendes Wissen neu verbinden
7. **Vision-Building**: Große Zukunftspläne entwickeln

**Was passiert**:
1. Modus wählen
2. **Kontext laden** (About-Me, Skills, Ideas, Projects)
3. Session durchführen (modus-spezifisch)
4. Session dokumentieren in `knowledge/sessions/`
5. Follow-up Aktionen vorschlagen:
   - Neue Idee → `/idea-new`
   - Neues Wissen → `/knowledge-add`
   - Skills updaten

**File**: `.claude/commands/sparring.md`

---

## Model Selection Strategy

**Feature**: Jeder Command nutzt automatisch das optimale Modell für seine Aufgabe!

### Quick Model Switcher

Für Ad-hoc Model-Switching gibt es jetzt 4 Quick-Commands:

| Command | Modell | Use Case | Kosten |
|---------|--------|----------|--------|
| `/opus` | **Opus** | Maximum Quality, komplexe Reasoning-Tasks | $$$$ |
| `/opus+` | **Opus + Ultrathink** | Maximales Extended Thinking für komplexeste Aufgaben | $$$$$ |
| `/sonnet` | **Sonnet 4.5** | Balanced Performance für Coding & Analyse | $$$ |
| `/haiku` | **Haiku** | Schnell & Kostengünstig für einfache Tasks | $ |

**Usage:**
```
/opus Was ist die beste Architektur für ein verteiltes System?
```
Oder ohne Frage (dann manuell stellen):
```
/opus
→ Modell gewechselt zu Opus
Deine Frage...
```

### Per-Command Model Configuration

**Alle Workflows nutzen automatisch optimale Modelle:**

#### 🔴 Opus (Maximum Quality)
- `/sparring` - Tiefes Brainstorming & Strategieentwicklung
- `/idea-connect` - Komplexe Synergien zwischen Ideen erkennen
- `/project-analyze` - Externe Codebase-Analyse

#### 🟠 Opus Plan (Hybrid: Planning + Execution)
- `/idea-work` - Planning mit Opus, Execution mit Sonnet

#### 🔵 Sonnet (Balanced)
- `/idea-new` - Ideen-Analyse & Dokumentation
- `/project-add` - Wissensextraktion aus Projekten
- `/onboard-process` - Komplexe Onboarding-Analyse

#### 🟢 Haiku (Fast & Cheap)
- `/idea-list` - Einfaches Listing & Filtering
- `/knowledge-search` - Schnelle Knowledge Base Suche
- `/knowledge-add` - Wissen kategorisieren & speichern
- `/inbox-process` - Batch-Verarbeitung von Dateien
- `/create-*` - Template-Generierung (Agent, Command, Hook, Skill)
- `/system-health` - System-Diagnostik

### Model-Auswahl Matrix

| Task-Typ | Modell | Begründung |
|----------|--------|------------|
| Komplexes Reasoning | Opus | Tiefes Denken, mehrere Perspektiven |
| Planning + Execution | OpusPlan | Beste beider Welten: Qualität + Effizienz |
| Coding & Analyse | Sonnet | Balanced Performance & Kosten |
| Suche & Lookup | Haiku | Schnell, Kosten-effizient |
| Batch-Processing | Haiku | Geschwindigkeit über Tiefe |
| Template-Generation | Haiku | Strukturiert, kein Deep Reasoning nötig |

### Kosten-Optimierung

**Automatische Optimierung durch Command-spezifische Modelle:**
- ~70% deiner Workflows nutzen Haiku (günstig)
- ~20% nutzen Sonnet (balanced)
- ~10% nutzen Opus (nur wo nötig)

**Manuelle Kontrolle:**
- Nutze `/haiku`, `/sonnet`, `/opus`, `/opus+` für freie Fragen
- Default (settings.json): Sonnet (balanced für Ad-hoc)

### Extended Thinking

Extended Thinking ist **aktiviert** (`alwaysThinkingEnabled: true` in settings.json).

**Besonders wertvoll bei:**
- `/opus+` - Maximales Ultrathink für komplexeste Probleme
- `/opus` - Standard Opus mit Extended Thinking
- `/sparring` - Tiefes Brainstorming
- `/idea-connect` - Verbindungen erkennen

**Sichtbar als:** Grauer Italic-Text vor der Antwort

---

## Plain Text Workflow Detection

**Feature**: Du musst NICHT Slash Commands nutzen - normale Sprache funktioniert auch!

### Wie es funktioniert

**Du schreibst**:
```
"Ich habe eine Idee für ein E-Commerce Tool"
```

**Ich erkenne** das Pattern und frage:
```
"Ich erkenne eine neue Idee! Soll ich /idea-new nutzen?"
```

**Du bestätigst** → Workflow wird ausgeführt!

### Pattern-Beispiele

| Dein Text | Erkannter Workflow |
|-----------|-------------------|
| "Ich habe eine Idee: ..." | `/idea-new` |
| "Zeig mir meine Ideen" | `/idea-list` |
| "Lass uns an {Idee} arbeiten" | `/idea-work` |
| "Suche nach API Integration" | `/knowledge-search` |
| "Ich habe gelernt dass..." | `/knowledge-add` |
| "Verarbeite die Inbox" | `/inbox-process` |
| "Lass uns brainstormen über..." | `/sparring` |

**Vollständige Pattern-Liste**: Siehe `workflow-patterns.md`

### Wichtig

- Ich **frage IMMER** bevor ich einen Workflow ausführe
- **NIE** automatische Ausführung ohne Bestätigung
- Bei Unsicherheit → normale Antwort

---

## Workflow-Dateien Struktur

Jeder Workflow ist eine Markdown-Datei mit:

### Frontmatter (Optional)
```markdown
---
description: Kurze Beschreibung
argument-hint: [optionale Argumente]
allowed-tools: Tool-Permissions
model: claude-model-id
---
```

### Content
Strukturierte Anweisungen für Claude:
- **Schritt 1**: Was zuerst tun
- **Schritt 2**: Analyse/Verarbeitung
- **Schritt 3**: Output/Dokumentation
- etc.

### Variablen
- `$ARGUMENTS`: Alle übergebenen Argumente
- `$1`, `$2`: Einzelne Positionsparameter
- `` !`command` ``: Bash-Befehle ausführen
- `@path`: Dateien referenzieren

---

## Best Practices

### Für Workflow-Entwicklung

1. **Sei spezifisch**: Klare, strukturierte Anweisungen
2. **Nutze Steps**: Nummerierte Schritte für Klarheit
3. **Error-Handling**: Was tun bei Problemen
4. **Dokumentiere**: Was wird wo gespeichert
5. **Vernetzung**: Aktiv Verbindungen herstellen

### Für Nutzung

1. **Inbox bevorzugen**: Für Dateien → schnellste Methode
2. **Plain Text OK**: Musst keine Commands merken
3. **Workflows kombinieren**: z.B. `/project-add` → `/idea-connect`
4. **Kontext nutzen**: System lernt von deinen Daten

---

## Wichtige Dateien

### In diesem Ordner (`.claude/`)

- **CONTEXT.md**: Technischer Session-Context für Claude
- **README.md**: Diese Datei - Workflows-Dokumentation
- **workflow-patterns.md**: Auto-Detection Patterns
- **commands/**: Alle 9 Workflows

### Im Root

- **START.md**: User-facing Quick Start Guide
- **README.md**: System-Übersicht
- **_inbox/**: Dokument-Verarbeitung

---

## Workflow-Entwicklung

### Neuen Workflow erstellen

1. Erstelle `.claude/commands/mein-workflow.md`
2. Füge Frontmatter hinzu (optional)
3. Schreibe strukturierte Anweisungen
4. Dokumentiere in dieser README
5. Füge Patterns zu `workflow-patterns.md` hinzu (falls Plain Text)

### Bestehenden Workflow anpassen

1. Öffne `.claude/commands/{workflow}.md`
2. Editiere die Anweisungen
3. Teste den Workflow
4. Update Dokumentation falls nötig

---

## Troubleshooting

### Workflow funktioniert nicht
- Prüfe ob Datei in `.claude/commands/` existiert
- Prüfe Syntax (gültiges Markdown)
- Schaue in Frontmatter nach Permissions

### Auto-Detection triggert falsch
- Check `workflow-patterns.md`
- Pattern zu aggressiv? → Anpassen
- Confidence zu niedrig setzen

### Dateien werden nicht verarbeitet
- Sind sie in `_inbox/`?
- Unterstütztes Format? (.md, .txt, .pdf)
- `/inbox-process` ausgeführt?

---

## Weiterführende Ressourcen

- **Claude Code Docs**: https://code.claude.com/docs
- **Slash Commands Guide**: https://code.claude.com/docs/en/slash-commands.md
- **System Architektur**: `CONTEXT.md`
- **User Guide**: `../START.md`

---

**Version**: 2.0.1
**Last Updated**: 2025-12-22
**Workflows**: 34 (30 feature workflows + 4 model switchers)
**Model Optimization**: Active (per-command model selection)
**Status**: Template - Ready for Customization
