---
title: "Intake Gate Pattern"
type: pattern
category: command-design
tags: [user-interaction, validation, askuserquestion, best-practice]
confidence: 95%
source: taches-cc-resources
created: 2025-12-01
status: production-ready
---

# Intake Gate Pattern

## Problem

Commands starten sofort mit der Ausführung, auch wenn:
- Der User-Input vage oder unvollständig ist
- Wichtige Entscheidungen nicht geklärt sind
- Der Kontext fehlt

Das führt zu: Falschen Annahmen, Rework, frustrierten Usern.

---

## Lösung

**Intake Gate**: Ein strukturierter Einstiegspunkt vor jeder Command-Ausführung.

```
┌─────────────────┐
│  User Input     │
└────────┬────────┘
         ▼
┌─────────────────┐
│  INTAKE GATE    │◄──── Ist Input ausreichend?
│  - Validate     │      - Nein → AskUserQuestion
│  - Clarify      │      - Ja → Proceed
│  - Confirm      │
└────────┬────────┘
         ▼
┌─────────────────┐
│  DECISION GATE  │◄──── User bestätigt
│  - Proceed      │
│  - Ask more     │
│  - Add context  │
└────────┬────────┘
         ▼
┌─────────────────┐
│  EXECUTION      │
└─────────────────┘
```

---

## Implementation

### Phase 1: Input Validation

```markdown
## Schritt 0: Intake Gate

**Prüfe $ARGUMENTS**:

Falls leer oder vage:
→ Nutze AskUserQuestion mit strukturierten Optionen

Falls ausreichend:
→ Zeige Zusammenfassung, fahre fort
```

### Phase 2: Adaptive Clarification

```markdown
**Analysiere den Input auf**:
- Komplexität (einfach vs. komplex)
- Scope (klar vs. unklar)
- Abhängigkeiten (standalone vs. vernetzt)
- Risiko (niedrig vs. hoch)

**Bei Unklarheiten, frage nach**:
- Scope: "Was genau soll enthalten sein?"
- Ziel: "Was ist das gewünschte Ergebnis?"
- Kontext: "Gibt es relevante Constraints?"
- Priorität: "Was ist am wichtigsten?"
```

### Phase 3: Decision Gate

```markdown
**Vor Ausführung IMMER bestätigen**:

Ich habe verstanden:
- Task: {zusammenfassung}
- Scope: {scope}
- Output: {expected_output}

Wie möchtest du fortfahren?
1. **Proceed** - Starte Ausführung
2. **Ask more** - Ich habe weitere Fragen
3. **Add context** - Ich möchte mehr Kontext geben
```

---

## AskUserQuestion Templates

### Für Task-Typ Klärung

```json
{
  "questions": [{
    "question": "Um welche Art von Task handelt es sich?",
    "header": "Task Type",
    "options": [
      {"label": "Coding", "description": "Implementierung, Bug Fix, Feature"},
      {"label": "Analysis", "description": "Code Review, Architecture, Research"},
      {"label": "Documentation", "description": "Docs, Comments, READMEs"},
      {"label": "Planning", "description": "Roadmap, Architecture Decision"}
    ],
    "multiSelect": false
  }]
}
```

### Für Scope Klärung

```json
{
  "questions": [{
    "question": "Wie umfangreich soll die Lösung sein?",
    "header": "Scope",
    "options": [
      {"label": "Minimal", "description": "Schnellste Lösung, nur das Nötigste"},
      {"label": "Standard", "description": "Solide Lösung mit Best Practices"},
      {"label": "Comprehensive", "description": "Vollständig mit Edge Cases, Tests"}
    ],
    "multiSelect": false
  }]
}
```

### Für Priorität

```json
{
  "questions": [{
    "question": "Was ist am wichtigsten?",
    "header": "Priority",
    "options": [
      {"label": "Speed", "description": "Schnell fertig, später verbessern"},
      {"label": "Quality", "description": "Sauber und wartbar"},
      {"label": "Learning", "description": "Verstehen wie es funktioniert"}
    ],
    "multiSelect": false
  }]
}
```

---

## Wann verwenden

### IMMER bei:
- Commands die Dateien erstellen/ändern
- Multi-Step Workflows
- Ambigen User Requests
- Risikoreichen Operationen

### OPTIONAL bei:
- Einfachen Queries
- Klar definierten Inputs
- Wiederholten bekannten Tasks

---

## Beispiel: Vorher vs. Nachher

### Vorher (ohne Intake Gate)

```
User: /create-agent für API

Claude: *erstellt sofort einen generischen API Agent*
        *User wollte aber einen REST API Testing Agent*
        *Rework nötig*
```

### Nachher (mit Intake Gate)

```
User: /create-agent für API

Claude: Ich erstelle einen Agent für API-Arbeit.

        Um den richtigen Agent zu erstellen:

        [AskUserQuestion]
        - API Type: REST / GraphQL / gRPC
        - Purpose: Testing / Integration / Documentation
        - Scope: Single API / Multiple APIs

User: REST, Testing, Single API

Claude: Verstanden! Ich erstelle einen REST API Testing Agent.

        - Name: rest-api-tester-agent
        - Focus: Endpoint Testing, Response Validation
        - Tools: WebFetch, Bash (curl)

        Proceed / Ask more / Add context?

User: Proceed

Claude: *erstellt genau den gewünschten Agent*
```

---

## Integration in bestehende Commands

Füge diesen Block am Anfang jedes Commands ein:

```markdown
## Schritt 0: Intake Gate

**Input**: $ARGUMENTS

**Validation**:
- Falls leer → AskUserQuestion für {relevante Optionen}
- Falls vage → Clarifying Questions
- Falls klar → Zeige Zusammenfassung

**Decision Gate**:
Bestätige vor Ausführung:
- Proceed
- Ask more
- Add context

---
```

---

## Related Patterns

- **Progressive Disclosure** - Zeige nur relevante Optionen
- **Confirmation Before Action** - Nie destruktive Actions ohne Bestätigung
- **Context Loading** - Lade nur was wirklich nötig ist

---

**Pattern aus**: taches-cc-resources
**Adaptiert für**: Evolving System
**Status**: Production-Ready