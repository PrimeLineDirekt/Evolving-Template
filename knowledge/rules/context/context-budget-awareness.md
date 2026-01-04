# Context Budget Awareness

**Priorität**: HOCH
**Trigger**: Bei Task-Dumps, hohem Context, Multi-Step Work
**Quelle**: continuous-claude v3 behavior

---

## Das v3-Verhalten

> "Claude decided to parallelise tasks to manage context budget before handoff"
> — parcadei, über emergentes v3-Verhalten bei 73% Context

Dies ist **kein Feature** - es ist emergentes Verhalten aus:
1. Context % ist sichtbar (StatusLine)
2. Diese Rule definiert Handlungs-Heuristiken
3. Claude reasoned über eigene Constraints

---

## Context-Thresholds

| Context % | Status | Empfohlene Aktion |
|-----------|--------|-------------------|
| < 60% | Normal | Weiterarbeiten |
| 60-69% | Advisory | Bei Stopping Point: Handoff erwägen |
| 70-79% | Warning | Handoff vorbereiten, große Tasks parallelisieren |
| 80-89% | Critical | Jetzt Handoff, dann /clear |
| ≥ 90% | Emergency | SOFORT /whats-next, dann /clear |

---

## Task Dump + High Context Pattern

**Situation**: User gibt mehrere Tasks UND Context ist > 60%

**Reasoning-Prozess** (intern):
```
"Ich habe {N} Tasks.
 Mein Context ist bei {X}%.
 Sequentielle Ausführung würde Context auf ~{Y}% treiben.
 Parallelisierung in Agents spart Context.
 Handoff nach Completion sichert State."
```

**Empfehlung aussprechen**:
```
"Context bei {X}%. Mit {N} Tasks würde ich empfehlen:
 - Tasks 1-3 parallel in Agents ausführen
 - Handoff nach Completion
 - Dann /clear für Phase 2

 Soll ich so vorgehen?"
```

---

## Wann parallelisieren?

| Bedingung | Parallel? | Grund |
|-----------|-----------|-------|
| 3+ Tasks + Context > 60% | JA | Spart Context, verhindert Degradation |
| 2 Tasks + Context > 80% | JA | Kritisch, jeder Token zählt |
| 1-2 Tasks + Context < 60% | NEIN | Overhead nicht wert |
| Tasks mit Dependencies | TEILWEISE | Nur unabhängige Tasks parallel |

---

## Self-Aware Reasoning

Claude sollte über eigene Constraints reasonen:

### Bei Session-Start
```
"Frische Session. Context-Budget: ~200K Tokens.
 Für komplexe Tasks haben wir Spielraum."
```

### Bei High Context
```
"Context bei 73%. Das bedeutet:
 - Compaction könnte bald triggern
 - Signal-Qualität könnte degradieren
 - Handoff jetzt = frischer Context danach"
```

### Bei Task Dump
```
"5 Tasks erhalten. Bei 73% Context:
 - Sequentiell: ~95% Context, Compaction wahrscheinlich
 - Parallel: ~85% Context, sauberer
 - Mit Handoff: Fresh Start für Rest"
```

---

## Handoff-Trigger

| Situation | Aktion |
|-----------|--------|
| Context > 70% + große Task abgeschlossen | `/whats-next` anbieten |
| Context > 80% + beliebiger Stopping Point | `/whats-next` dringend empfehlen |
| Context > 90% | SOFORT `/whats-next` |

---

## Agent-Orchestration bei High Context

**Statt** direkt zu implementieren:
```
Main: Read files → Understand → Edit → Test
      (2000+ Tokens verbraucht)
```

**Besser** delegieren:
```
Main: Spawn agent("implement X")
      ↓
Agent: Reads → Understands → Edits → Tests
      ↓
Main: Gets summary (~200 Tokens)
```

**Effekt**: Arbeit passiert, Context bleibt frei.

---

## Praktische Checkliste

Bei hohem Context (>70%):

```
□ Wie viele Tasks sind offen?
□ Sind Tasks unabhängig? → Parallel möglich
□ Gibt es einen natürlichen Stopping Point? → Handoff dort
□ Ist Compaction wahrscheinlich? → Lieber jetzt /clear
□ Würde Agent-Delegation helfen? → Task spawnen
```

---

## Integration

Diese Rule aktiviert emergentes Verhalten zusammen mit:
- `clear-dont-compact.md` - Ledger-basierte State
- `domain-memory-bootup.md` - Fresh Start nach Clear
- `/whats-next` Command - Handoff-Erstellung
- Agent Orchestration - Delegation für Context-Erhalt

---

## Beispiel-Flow

```
User: "Hier sind 5 Features die implementiert werden müssen:
       1. Auth System
       2. API Endpoints
       3. Frontend Forms
       4. Tests
       5. Dokumentation"

Claude (bei 73% Context):
  "Ich sehe 5 Tasks bei 73% Context.

   Empfehlung:
   1. Tasks 1-3 parallel in Agents (unabhängig)
   2. Nach Completion: /whats-next für Handoff
   3. /clear für frischen Context
   4. Tasks 4-5 in neuer Session

   So vermeiden wir Context-Degradation und
   behalten volle Signal-Qualität.

   Soll ich so vorgehen?"
```

---

## Merksätze

> "Context ist endlich. Plane entsprechend."

> "Parallelisierung spart Context, nicht nur Zeit."

> "Lieber ein sauberer Handoff als degradierter Context."

> "Claude kann über eigene Constraints reasonen - nutze das!"
