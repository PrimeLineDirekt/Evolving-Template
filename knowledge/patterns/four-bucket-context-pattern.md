# Four-Bucket Context Pattern

**Quelle**: muratcankoylan/Agent-Skills-for-Context-Engineering
**Kategorie**: Context Management
**Komplexität**: Mittel

---

## Übersicht

Vier Strategien für effektives Context Management. Jede Strategie adressiert unterschiedliche Situationen und Degradation-Typen.

```
┌─────────────────────────────────────────────────────────────────┐
│                    CONTEXT MANAGEMENT                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   ┌─────────┐   ┌─────────┐   ┌─────────┐   ┌─────────┐       │
│   │  WRITE  │   │ SELECT  │   │COMPRESS │   │ ISOLATE │       │
│   │         │   │         │   │         │   │         │       │
│   │Authorita│   │ Gezielt │   │Zusammen-│   │Sub-Agent│       │
│   │tive     │   │ einsch- │   │fassen   │   │auslagern│       │
│   │setzen   │   │ leusen  │   │         │   │         │       │
│   └─────────┘   └─────────┘   └─────────┘   └─────────┘       │
│        │             │             │             │             │
│        ▼             ▼             ▼             ▼             │
│   Kritische     Task-       Lange        Spezialisierte       │
│   Constraints   relevanter  Historien    Tasks                │
│                 Kontext                                        │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Die Vier Buckets

### 1. WRITE - Authoritative Setzen

**Wann**: Kritische Constraints, die NICHT ignoriert werden dürfen.

**Wie**:
- In System Prompt / CLAUDE.md platzieren
- Als "KRITISCH" oder "WICHTIG" markieren
- Am Anfang des Kontexts (höchste Attention)

**Beispiele**:
```markdown
# KRITISCH: Sicherheitsregeln

Diese Regeln dürfen NIEMALS ignoriert werden:
- Keine API-Keys im Code
- Keine SQL-Injections
- Immer Input validieren
```

**Verhindert**: Context Poisoning, Instruction Clash

---

### 2. SELECT - Gezielt Einschleusen

**Wann**: Task-spezifischer Kontext, der für die aktuelle Aufgabe relevant ist.

**Wie**:
- Nur relevante Dateien/Patterns laden
- Context Router nutzen für Keyword-Matching
- "Just-in-Time" Loading statt "Everything-at-Start"

**Beispiele**:
```
User: "Erstelle einen neuen Agent"

SELECT:
- .claude/templates/specialist-agent.md
- knowledge/patterns/agent-orchestration-pattern.md
- Ein Beispiel-Agent als Referenz

NICHT laden:
- Alle 17 Agents
- Alle Patterns
- Gesamte Knowledge Base
```

**Verhindert**: Context Distraction, Lost-in-Middle

---

### 3. COMPRESS - Zusammenfassen

**Wann**: Lange Historien, vergangene Sessions, umfangreiche Dokumente.

**Wie**:
- Ledger Quick Resume (2-3 Sätze)
- Key Decisions statt Full History
- "What matters NOW" Fokus

**Techniken**:

| Technik | Beschreibung | Wann |
|---------|--------------|------|
| **Anchored Iterative** | Zusammenfassung mit Anker-Punkten | Lange Sessions |
| **Opaque** | Nur Ergebnis, nicht Prozess | Abgeschlossene Tasks |
| **Regenerative** | Kompletter Neu-Summary | Bei Confusion |

**Beispiel**:
```markdown
## Quick Resume (COMPRESS)

> Ledger System implementiert. PreCompact Hook erstellt.
> Nächster Schritt: Four-Bucket Pattern dokumentieren.
```

**Verhindert**: Context Overload, Summary Degradation

---

### 4. ISOLATE - In Sub-Agent Auslagern

**Wann**: Spezialisierte Tasks, die eigenen Kontext brauchen.

**Wie**:
- Task Tool mit spezifischem Agent
- Klares Input/Output Interface
- Sub-Agent bekommt frischen Kontext

**Beispiele**:
```
Haupt-Session:
  "Analysiere dieses Repository"

ISOLATE → research-analyst-agent:
  - Bekommt: Repo-URL, spezifische Fragen
  - Arbeitet: Mit frischem Kontext
  - Liefert: Strukturierte Findings

Haupt-Session:
  Verarbeitet Findings weiter
```

**Verhindert**: Context Confusion, Telephone Game Problem

---

## Entscheidungsbaum

```
Welche Strategie?
       │
       ▼
┌──────────────────┐
│ Darf NIEMALS     │──YES──▶ WRITE
│ ignoriert werden?│
└────────┬─────────┘
         │ NO
         ▼
┌──────────────────┐
│ Nur für diesen   │──YES──▶ SELECT
│ Task relevant?   │
└────────┬─────────┘
         │ NO
         ▼
┌──────────────────┐
│ Zu lang/         │──YES──▶ COMPRESS
│ historisch?      │
└────────┬─────────┘
         │ NO
         ▼
┌──────────────────┐
│ Spezialisiert/   │──YES──▶ ISOLATE
│ eigenständig?    │
└──────────────────┘
```

---

## Context Degradation Typen

Diese Pattern adressiert folgende Degradation-Probleme:

| Degradation | Problem | Bucket-Lösung |
|-------------|---------|---------------|
| **Lost-in-Middle** | Mittlerer Kontext wird ignoriert | WRITE (vorne), SELECT (hinten) |
| **Poisoning** | Falsche Info übernommen | WRITE (authoritative) |
| **Distraction** | Irrelevantes lenkt ab | SELECT (nur relevantes) |
| **Confusion** | Widersprüchliche Info | COMPRESS (Single Truth) |
| **Clash** | Alte vs. neue Instructions | WRITE (timestamps, override) |

---

## Praktische Anwendung

### Bei Session-Start

```
1. WRITE: CLAUDE.md + Rules laden (authoritative)
2. SELECT: Domain Memory für aktives Projekt
3. COMPRESS: Ledger Quick Resume lesen
4. (Bei Bedarf) ISOLATE: Spezial-Tasks an Agents
```

### Bei Task-Wechsel

```
1. SELECT: Neuen Task-relevanten Kontext laden
2. COMPRESS: Vorherigen Task kurz zusammenfassen
3. (Optional) WRITE: Neue Constraints definieren
```

### Bei Context-Problemen

```
1. COMPRESS: Aktuellen Stand zusammenfassen
2. /clear: Frischen Kontext holen
3. WRITE + SELECT: Nur Notwendiges neu laden
```

---

## Integration mit Evolving

| Evolving-Komponente | Bucket |
|---------------------|--------|
| CLAUDE.md, Rules | WRITE |
| Context Router | SELECT |
| Ledger Quick Resume | COMPRESS |
| Task Tool + Agents | ISOLATE |
| Domain Memory | SELECT + COMPRESS |

---

## Metriken

**Tokens-per-Task** statt Tokens-per-Request:
- Nicht: "Wie viele Tokens pro API Call?"
- Sondern: "Wie viele Tokens für die gesamte Aufgabe?"

Bessere Context-Strategie = Weniger Gesamttokens bei gleicher Qualität.

---

## Related

- [Context Window Ownership](context-window-ownership-pattern.md)
- [Clear, Don't Compact Rule](../../.claude/rules/clear-dont-compact.md)
- [Domain Memory Bootup](../../.claude/rules/domain-memory-bootup.md)
- [Ledger System](../../_ledgers/README.md)
