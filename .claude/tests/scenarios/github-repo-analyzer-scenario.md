# Scenario: GitHub Repo Analyzer Agent

## Agent
github-repo-analyzer-agent

## Beschreibung
Testet die Dual-System Analyse-Fähigkeiten des Agents:
- SYSTEM-MAP wird korrekt geladen
- Externes Repo wird analysiert
- Findings werden kategorisiert (NEU/BESSER/ANDERS/REDUNDANT)
- Integration Roadmap wird erstellt

---

## Setup

**Voraussetzungen**:
- `.claude/SYSTEM-MAP.md` existiert und ist aktuell
- Internetzugang für Remote-Repos

**Test-Repositories**:
- Remote: `https://github.com/langwatch/better-agents`
- Lokal: Ein geklontes Repository

---

## Test Cases

### Case 1: SYSTEM-MAP Loading

**Input**:
```
Analysiere https://github.com/langwatch/better-agents
```

**Expected**:
- Agent liest `.claude/SYSTEM-MAP.md`
- Agent zeigt "SYSTEM-MAP geladen" mit Statistiken
- Keine Fehler bei Phase 1

**Validation**:
- [ ] SYSTEM-MAP wurde referenziert
- [ ] Komponenten-Zahlen werden angezeigt

---

### Case 2: Remote Repo Analysis

**Input**:
```
/analyze-repo https://github.com/langwatch/better-agents
```

**Expected**:
- README.md wird gefetcht
- package.json wird analysiert
- Tech Stack wird identifiziert
- Key Patterns werden extrahiert

**Validation**:
- [ ] Purpose korrekt erkannt (CLI für Agent-Projekte)
- [ ] Tech Stack: TypeScript, Node.js, Commander
- [ ] Mindestens 3 Patterns identifiziert

---

### Case 3: Finding Kategorisierung

**Input**:
Analyse-Output aus Case 2

**Expected**:
Jedes Finding hat eine Kategorie:
- 🟢 NEU: MCP Config, Scenario Testing
- 🟡 BESSER: Prompt Registry
- 🔵 ANDERS: YAML vs Markdown
- ⚪ REDUNDANT: AGENTS.md

**Validation**:
- [ ] Alle Findings kategorisiert
- [ ] Keine Finding ohne Kategorie
- [ ] Kategorien sind korrekt zugeordnet

---

### Case 4: Integration Roadmap

**Input**:
Analyse-Output aus Case 2

**Expected**:
- Quick Wins (< 1h) identifiziert
- Medium Effort (1-4h) identifiziert
- Larger Projects (> 4h) identifiziert
- Konkrete Dateipfade angegeben

**Validation**:
- [ ] Mindestens 1 Quick Win
- [ ] Jede Integration hat Effort-Schätzung
- [ ] Pfade sind spezifisch (nicht generisch)

---

### Case 5: SYSTEM-MAP Update

**Input**:
Nach Analyse

**Expected**:
- Changelog in SYSTEM-MAP wird vorbereitet
- Findings mit Status "Pending" eingetragen

**Validation**:
- [ ] SYSTEM-MAP Changelog erwähnt
- [ ] Konkrete Einträge vorgeschlagen

---

### Case 6: Plain Text Detection

**Input**:
```
Schau dir mal https://github.com/owner/repo an
```

**Expected**:
- Intent wird erkannt
- Frage: "Soll ich /analyze-repo ausführen?"

**Validation**:
- [ ] Keine automatische Ausführung
- [ ] Bestätigung angefordert

---

### Case 7: Lokales Repo (Edge Case)

**Input**:
```
/analyze-repo /path/to/local/repo
```

**Expected**:
- Pfad wird validiert
- Read/Glob/Grep statt WebFetch
- Git-Metadata extrahiert

**Validation**:
- [ ] Keine WebFetch-Aufrufe
- [ ] Git log/remote abgefragt

---

### Case 8: Fehlerfall - SYSTEM-MAP fehlt

**Input**:
Analyse ohne SYSTEM-MAP.md

**Expected**:
- Warnung: "SYSTEM-MAP.md nicht gefunden"
- Angebot: "Soll ich sie erstellen?"

**Validation**:
- [ ] Keine Crash
- [ ] Hilfreiche Fehlermeldung

---

## Erfolgskriterien

- [ ] Alle 8 Test Cases bestanden
- [ ] Keine unbehandelten Fehler
- [ ] Output-Format konsistent
- [ ] SYSTEM-MAP korrekt integriert

---

## Letzte Ausführung

| Datum | Ergebnis | Notizen |
|-------|----------|---------|
| 2025-12-01 | Initial | Erster Test mit better-agents |

---

**Erstellt**: 2025-12-01
**Agent Version**: 1.0
