---
description: Generiert ein komplettes Multi-Agent System in einem Ziel-Ordner
model: sonnet
argument-hint: [target-path] [--blueprint TYPE]
---

# /create-system

Generiert ein vollständiges Multi-Agent System mit Agents, Commands, Knowledge-Injection und CLAUDE.md.

## Übersicht

```
/create-system ~/projects/steuer-system
/create-system ~/projects/legal-advisor --blueprint multi-agent-advisory
```

**Was passiert:**
1. Analysiert deine Anforderung
2. Matched passenden Blueprint
3. Designt Architektur mit Agent-Rollen
4. Generiert alle Dateien
5. Validiert das System
6. Gibt dir Next Steps

---

## Schritt 1: Intake Gate

**Parse Arguments:**
- `$ARGUMENTS` enthält Ziel-Pfad und optionale Flags
- Format: `{target_path} [--blueprint {id}] [--name {name}] [--domain {domain}]`

**Validierungen:**
1. Ziel-Pfad angegeben?
   - Nein → Frage: "Wo soll das System erstellt werden? (z.B. ~/projects/mein-system)"
2. Pfad existiert?
   - Nein → Frage: "Ordner existiert nicht. Soll ich ihn erstellen?"
   - Ja mit Inhalt → Warnung: "Ordner enthält bereits Dateien. Fortfahren? (könnte überschreiben)"
3. Pfad schreibbar?
   - Nein → Error: "Keine Schreibrechte für diesen Pfad"
4. Pfad NICHT in Evolving?
   - Ja in Evolving → Error: "Bitte einen externen Pfad wählen (nicht innerhalb von Evolving)"

**Wenn kein Blueprint via Flag:**
→ Frage: "Was für ein System möchtest du erstellen? Beschreibe kurz den Zweck."

---

## Schritt 2: Requirements-Analyse

**Nutze system-analyzer-agent via Task-Tool:**

```
Starte Task-Agent mit:
- subagent_type: "general-purpose"
- prompt: Lade @.claude/agents/system-analyzer-agent.md und analysiere:
  - User Request: "{user_description}"
  - Target Path: "{target_path}"
  - Available Blueprints: Lade .claude/blueprints/index.json
```

**Präsentiere Ergebnis:**
```
Analysiere deine Anforderung...

Erkannt:
- Domain: {detected_domain}
- Komplexität: {complexity}
- Geschätzte Agents: {agent_count}

Blueprint-Matches:
┌────────────────────────────┬───────┬─────────────────────────────┐
│ Blueprint                  │ Match │ Grund                       │
├────────────────────────────┼───────┼─────────────────────────────┤
│ 1. Multi-Agent Advisory    │  95%  │ Keywords: experten, team    │
│ 2. Autonomous Research     │  40%  │ Nur partial match           │
│ 3. Simple Workflow         │  25%  │ Zu einfach für Anforderung  │
└────────────────────────────┴───────┴─────────────────────────────┘

Empfehlung: Multi-Agent Advisory (95% Match)

[1] Empfehlung akzeptieren
[2] Anderen Blueprint wählen
[3] Custom System (ohne Blueprint)
```

---

## Schritt 3: Blueprint-Auswahl

**Bei Akzeptanz (Option 1):**
→ Lade Blueprint-Details aus `.claude/blueprints/{id}.json`

**Bei Option 2:**
→ Liste alle Blueprints
→ User wählt

**Bei Option 3 (Custom):**
→ Frage nach:
  - Domain
  - Anzahl Agents
  - Agent-Rollen
  - Commands

---

## Schritt 4: Customization

**Nutze system-architect-agent via Task-Tool:**

```
Starte Task-Agent mit:
- subagent_type: "general-purpose"
- model: "opus"
- prompt: Lade @.claude/agents/system-architect-agent.md und designe:
  - Blueprint: {selected_blueprint}
  - Domain: {domain}
  - Target: {target_path}
  - User Customization: {customization_answers}
```

**Customization-Fragen (basierend auf Blueprint):**
```
Konfiguration für Multi-Agent Advisory:

1. Domain-Name: steuer
2. Projekt-Name: Steuer-Beratungs-System [Enter für Default]
3. Anzahl Spezialisten (2-4): 3

Optionale Features:
[x] Validator-Agent für Risiko-Assessment
[x] Knowledge Base Struktur
[ ] Memory-System

Welche Spezialisten-Rollen?
1. Steuerberater (Hauptexperte) [Opus]
2. Steueranwalt (Rechtssicherheit) [Opus]
3. Software-Experte (Tool-Bedienung) [Sonnet]

Proceed? (Y/n)
```

---

## Schritt 5: Architektur-Preview

**Zeige dem User die geplante Architektur:**

```
Architektur-Design:

System: Steuer-Beratungs-System
Domain: steuer
Pattern: multi-agent-advisory

Agents (5):
┌─────────────────────────────────────────────────────────────────┐
│                     steuer-koordinator                          │
│                        (Sonnet)                                 │
└───────────────────────────┬─────────────────────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
        ▼                   ▼                   ▼
┌───────────────┐   ┌───────────────┐   ┌───────────────┐
│ steuerberater │   │ steueranwalt  │   │ software-     │
│    (Opus)     │   │    (Opus)     │   │ experte       │
│               │   │               │   │  (Sonnet)     │
└───────┬───────┘   └───────┬───────┘   └───────────────┘
        │                   │
        └─────────┬─────────┘
                  │
                  ▼
          ┌───────────────┐
          │    reporter   │
          │   (Haiku)     │
          └───────────────┘

Commands (2):
- /steuer-beratung → Umfassende Team-Beratung (Opus)
- /steuer-check → Schnelle Prüfung (Haiku)

Knowledge Injection:
- multi-agent-orchestration.md (Pattern)
- confidence-scoring.md (Pattern)
- ki-auswanderungs-berater-learnings.md (Reference)

Model-Verteilung:
- Opus: 2 Agents (kritische Analyse)
- Sonnet: 2 Agents (Koordination)
- Haiku: 1 Agent (Reporting)

Proceed mit Generation? (Y/n)
```

---

## Schritt 6: Generation

**Nutze system-generator-agent via Task-Tool:**

```
Starte Task-Agent mit:
- subagent_type: "general-purpose"
- prompt: Lade @.claude/agents/system-generator-agent.md und generiere:
  - Architecture: {architecture_json}
  - Target Path: {target_path}
  - Templates: .claude/templates/generated-system/
```

**Progress-Anzeige:**
```
Generiere System...

[1/8] Verzeichnisstruktur erstellen... ✓
[2/8] CLAUDE.md generieren... ✓
[3/8] README.md generieren... ✓
[4/8] scenario.json generieren... ✓
[5/8] Agents erstellen (5)... ✓
[6/8] Commands erstellen (2)... ✓
[7/8] Knowledge Injection... ✓
[8/8] Memory Bootstrap... ✓

Generation abgeschlossen!
```

---

## Schritt 7: Validation

**Nutze system-validator-agent via Task-Tool:**

```
Starte Task-Agent mit:
- subagent_type: "general-purpose"
- model: "haiku"
- prompt: Lade @.claude/agents/system-validator-agent.md und validiere:
  - Target Path: {target_path}
  - Architecture: {architecture_json}
```

**Validation-Output:**
```
Validierung...

✓ Verzeichnisstruktur (5/5 Ordner)
✓ Required Files (3/3 Dateien)
✓ Agent Files (5/5 Agents)
✓ Command Files (2/2 Commands)
✓ Placeholder Check (0 verbleibend)
✓ CLAUDE.md Quality (156 Zeilen)
⚠ Reference Integrity (7/8 - 1 optionale Warnung)

Score: 95/100 - PASS

1 Warnung:
- Optional pattern 'reflection-pattern.md' nicht gefunden
  → Kann ignoriert oder später hinzugefügt werden
```

---

## Schritt 8: Summary & Next Steps

```
System erfolgreich generiert!

Pfad: ~/projects/steuer-system/

Dateien erstellt:
├── .claude/
│   ├── CLAUDE.md
│   ├── scenario.json
│   ├── agents/
│   │   ├── steuer-koordinator-agent.md
│   │   ├── steuerberater-agent.md
│   │   ├── steueranwalt-agent.md
│   │   ├── software-experte-agent.md
│   │   └── steuer-reporter-agent.md
│   └── commands/
│       ├── steuer-beratung.md
│       └── steuer-check.md
├── knowledge/
│   └── patterns/
│       ├── multi-agent-orchestration.md
│       └── confidence-scoring.md
├── _memory/
│   └── index.json
└── README.md

Total: 14 Dateien, 5 Agents, 2 Commands

Nächste Schritte:
1. cd ~/projects/steuer-system
2. claude code (startet Claude Code im Projekt)
3. /steuer-beratung für umfassende Beratung
4. /steuer-check für schnelle Prüfungen

Optional:
- Füge Domain-Wissen zu knowledge/ hinzu
- Passe Agents in .claude/agents/ an
- Erweitere mit eigenen Commands
```

---

## Error Handling

### Pfad-Fehler
```
IF path_not_writable:
  "Fehler: Keine Schreibrechte für {path}
   Versuche einen anderen Pfad oder führe mit sudo aus."
```

### Blueprint nicht gefunden
```
IF blueprint_not_found:
  "Blueprint '{id}' nicht gefunden.
   Verfügbare Blueprints:"
   → Liste alle aus index.json
```

### Generation fehlgeschlagen
```
IF generation_failed:
  "Generation fehlgeschlagen bei: {step}
   Fehler: {error}

   Bereits erstellte Dateien wurden beibehalten.
   Retry mit: /create-system {path} --resume"
```

### Validation fehlgeschlagen
```
IF validation_failed:
  "System generiert aber Validation fehlgeschlagen:
   {issues}

   Das System ist möglicherweise nicht vollständig nutzbar.
   Bitte manuell prüfen oder mit --force überspringen."
```

---

## Flags

| Flag | Beschreibung |
|------|--------------|
| `--blueprint {id}` | Blueprint direkt auswählen (skip matching) |
| `--name {name}` | Projekt-Name direkt setzen |
| `--domain {domain}` | Domain direkt setzen |
| `--auto` | Keine Bestätigungen (für Experten) |
| `--dry-run` | Nur zeigen was generiert würde |
| `--force` | Überschreibe existierende Dateien |

---

## Beispiele

**Minimal:**
```
/create-system ~/projects/tax-advisor
```

**Mit Blueprint:**
```
/create-system ~/projects/legal-system --blueprint multi-agent-advisory --domain legal
```

**Auto-Mode:**
```
/create-system ~/projects/quick-test --blueprint simple-workflow --auto
```

**Dry-Run:**
```
/create-system ~/projects/preview --dry-run
```

---

## Related

- `.claude/blueprints/` - Blueprint-Definitionen
- `.claude/agents/system-*-agent.md` - Builder-Agents
- `.claude/templates/generated-system/` - Generation Templates
- `knowledge/patterns/system-generation-pattern.md` - Pattern-Dokumentation
