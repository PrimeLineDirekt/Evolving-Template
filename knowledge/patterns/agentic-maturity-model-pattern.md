# Agentic Maturity Model Pattern

**Quelle**: Nebulock-Inc/agentic-threat-hunting-framework
**Typ**: Meta-Pattern
**Anwendung**: Progression von manuellem zu autonomem AI-Einsatz

---

## Konzept

Ein 5-Level Framework für die progressive Integration von AI in Workflows. Jedes Level baut auf dem vorherigen auf.

> "Most teams will live at Levels 1–2. Everything beyond that is optional maturity."

---

## Die 5 Levels

| Level | Name | Capability |
|-------|------|-----------|
| **0** | Ad-hoc | Wissen in Slack, Tickets, Notizen |
| **1** | Documented | Persistente, strukturierte Records |
| **2** | Searchable | AI liest und erinnert sich |
| **3** | Generative | AI führt Aktionen aus (via Tools) |
| **4** | Agentic | Autonome Agents arbeiten selbstständig |

---

## Level Details

### Level 0: Ad-hoc

**Charakteristik:**
- Wissen verteilt über Slack, E-Mails, Tickets
- Keine strukturierte Dokumentation
- Jede Aufgabe startet bei Null
- "Tab Explosion" bei jeder Session

**Problem:** Kein institutionelles Gedächtnis.

---

### Level 1: Documented

**Charakteristik:**
- Strukturierte Dokumentation (Markdown)
- Standardisierte Templates
- Persistente Records
- Knowledge Transfer möglich

**Was du bekommst:**
- Wissen überlebt Sessions
- Neue Teammitglieder können lernen
- Suchbare Historie

**Beispiel (Evolving):**
- `ideas/` mit strukturierten Ideen
- `knowledge/` mit Learnings/Patterns
- `_memory/` mit Project State

---

### Level 2: Searchable

**Charakteristik:**
- AI liest dein Repo
- AI erinnert sich an vorherige Arbeit
- AI gibt kontextbezogene Vorschläge
- Sofortiger Context-Abruf

**Was du bekommst:**
- AI antwortet basierend auf deinem Wissen
- Keine Wiederholungsarbeit
- Schnelle Kontextbereitstellung

**Erforderliche Dateien:**
- `CLAUDE.md` - System-Kontext
- `AGENTS.md` - Environment Catalog
- Knowledge Base mit strukturierten Docs

**Beispiel:**
```
User: "Was wissen wir über API-Integration?"
AI: [Durchsucht knowledge/, patterns/, learnings/]
    "3 relevante Patterns gefunden:
     - REST Best Practices (aus Projekt X)
     - Error Handling Pattern
     - Rate Limiting Learning"
```

---

### Level 3: Generative

**Charakteristik:**
- AI führt Aktionen aus (nicht nur vorschlagen)
- Tool-Integration (MCP, APIs)
- AI erstellt Dateien, führt Queries aus
- Du validierst, AI exekutiert

**Was du bekommst:**
- AI erstellt Drafts
- AI führt Recherche aus
- AI dokumentiert automatisch

**Der Unterschied:**
```
Level 2:
  User: "Erstelle ein Pattern"
  AI: "Hier ist ein Vorschlag: [text]"
  User: [Kopiert manuell in Datei]

Level 3:
  User: "Erstelle ein Pattern"
  AI: [Erstellt Datei, updated Index, committed]
  AI: "Pattern erstellt in knowledge/patterns/x.md"
```

---

### Level 4: Agentic

**Charakteristik:**
- Autonome Agents arbeiten ohne Prompts
- Agents koordinieren untereinander
- Du validierst und genehmigst
- Proaktive statt reaktive Arbeit

**Was du bekommst:**
- Agents überwachen Feeds/Repos
- Agents generieren Drafts
- Agents benachrichtigen bei Bedarf
- Du fokussierst auf Entscheidungen

**Beispiel-Szenario:**
```
1. Monitor-Agent checkt GitHub alle 6h
2. Findet relevantes neues Repo
3. Analyzer-Agent führt Deep Dive durch
4. Reporter-Agent erstellt Summary
5. Notifier-Agent: "Neues Repo analysiert. Review?"
```

---

## Progression im Evolving-Kontext

| Level | Evolving Feature | Status |
|-------|------------------|--------|
| 0 | Vor Evolving | - |
| 1 | ideas/, knowledge/, _memory/ | ✓ |
| 2 | CLAUDE.md, Context Router, /recall | ✓ |
| 3 | Slash Commands, MCP Tools | ✓ |
| 4 | Background Agents, Autonomous Workflows | Partial |

---

## Wann welches Level anstreben?

**Level 1-2 für jeden:**
- Sofortiger Nutzen
- Geringer Aufwand
- Basis für alles weitere

**Level 3 wenn:**
- Wiederkehrende Tasks
- Tool-Integration möglich
- Team nutzt AI regelmäßig

**Level 4 wenn:**
- Klare Monitoring-Anforderungen
- Risiko-Toleranz für Autonomie
- Technische Kapazität für Agent-Development

---

## Key Insight

> "The progression is about WHO does the work, not WHAT gets done:
> - Level 1-2: You do, AI assists
> - Level 3: AI does, you direct
> - Level 4: AI does, you validate"

---

## ABLE Framework (Hypothesis Scoping)

Für Level 2+ hilfreich: Strukturiertes Scoping für Analysen/Recherchen.

| Field | Description | Example |
|-------|-------------|---------|
| **A**ctor | Wer/Was (optional) | "Neues GitHub Repo" |
| **B**ehavior | Was passiert | "Enthält MCP Patterns" |
| **L**ocation | Wo | "GitHub, /src/ Ordner" |
| **E**vidence | Welche Daten | "README.md, package.json, .claude/" |

---

## Related

- [Context Window Ownership Pattern](context-window-ownership-pattern.md)
- [Progressive Disclosure Pattern](progressive-disclosure-pattern.md)
- [LOCK Methodology Pattern](lock-methodology-pattern.md)
