# LOCK Methodology Pattern

> **Source**: Nebulock-Inc/agentic-threat-hunting-framework
> **Type**: Investigation/Research Pattern
> **Origin**: Threat Hunting, aber universell anwendbar
> **Relevanz**: MEDIUM - Strukturierte Investigation für Research Tasks

## Konzept

LOCK ist ein 4-Phasen-Framework für strukturierte Untersuchungen:

```
Learn → Observe → Check → Keep
  ↓        ↓        ↓       ↓
Context  Hypothese  Test   Record
```

## Die 4 Phasen

### Phase 1: LEARN (Kontext sammeln)

**Zweck**: Hintergrund und Trigger verstehen.

**Fragen**:
- Was hat diese Untersuchung ausgelöst?
- Welcher Kontext ist relevant?
- Was wissen wir bereits?
- Welche Ressourcen stehen zur Verfügung?

**Output**:
```markdown
## Learn
- **Trigger**: {Was hat die Untersuchung gestartet?}
- **Context**: {Relevanter Hintergrund}
- **Known**: {Was wissen wir schon?}
- **Resources**: {Verfügbare Quellen/Tools}
```

### Phase 2: OBSERVE (Hypothese bilden)

**Zweck**: Testbare Hypothese formulieren.

**Fragen**:
- Was vermuten wir?
- Welches Verhalten/Pattern suchen wir?
- Wie würde sich unser Verdacht manifestieren?

**Output**:
```markdown
## Observe
- **Hypothesis**: {Testbare Annahme}
- **Observable Indicators**: {Was würden wir sehen wenn wahr?}
- **Expected Pattern**: {Konkretes Muster}
```

### Phase 3: CHECK (Testen)

**Zweck**: Hypothese mit Daten validieren.

**Fragen**:
- Wie testen wir die Hypothese?
- Welche Queries/Suchen führen wir aus?
- Was sind die Grenzen des Tests?

**Guardrails**:
- Zeitfenster begrenzen
- Ergebnis-Caps setzen
- Ressourcen-intensive Operationen explizit genehmigen

**Output**:
```markdown
## Check
- **Method**: {Wie wird getestet?}
- **Query/Search**: {Konkrete Abfrage}
- **Constraints**: {Zeit-Limit, Result-Cap}
- **Results**: {Ergebnisse}
```

### Phase 4: KEEP (Dokumentieren)

**Zweck**: Erkenntnisse festhalten, auch wenn nichts gefunden.

**Fragen**:
- Was haben wir gelernt?
- Was funktionierte? Was nicht?
- Welche nächsten Schritte ergeben sich?

**Output**:
```markdown
## Keep
- **Finding**: {Was wurde entdeckt/gelernt}
- **Outcome**: {Confirmed | Refuted | Inconclusive}
- **Worked**: {Was funktionierte}
- **Didn't Work**: {Was nicht funktionierte}
- **Next Steps**: {Folge-Aktionen}
- **Lessons**: {Lessons Learned}
```

## Vollständiges Template

```markdown
# Investigation: {Title}

**ID**: INV-{YYYY-NNN}
**Status**: draft | in_progress | completed
**Created**: YYYY-MM-DD
**Related**: [Verknüpfte Investigations]

---

## Learn

**Trigger**: Was hat diese Untersuchung ausgelöst?

**Context**:
- Relevanter Hintergrund
- Bekannte Informationen

**Resources**:
- Verfügbare Datenquellen
- Tools und Zugriffe

---

## Observe

**Hypothesis**:
> Testbare Annahme in einem Satz

**Observable Indicators**:
- Was wir sehen sollten wenn die Hypothese stimmt
- Konkrete Patterns/Verhalten

---

## Check

**Method**: Beschreibung des Test-Ansatzes

**Query/Search**:
```
{Konkrete Suche/Abfrage}
```

**Constraints**:
- Zeitfenster: {z.B. letzte 7 Tage}
- Result-Cap: {z.B. max 100 Ergebnisse}

**Results**:
{Ergebnisse der Untersuchung}

---

## Keep

**Outcome**: ✓ Confirmed | ✗ Refuted | ○ Inconclusive

**Finding**:
{Was wurde entdeckt oder gelernt}

**What Worked**:
- {Erfolgreicher Ansatz 1}
- {Erfolgreicher Ansatz 2}

**What Didn't Work**:
- {Fehlgeschlagener Ansatz 1}

**Lessons Learned**:
- {Erkenntnis für zukünftige Untersuchungen}

**Next Steps**:
- [ ] {Folge-Aktion 1}
- [ ] {Folge-Aktion 2}
```

## Memory & Persistence

### 3-Tier Recall System

```
Tier 1: CLI-basierte Suche (wenn verfügbar)
        athf hunt search "keyword"
        athf hunt list --category X

Tier 2: Grep-basierte Suche (Fallback)
        grep -r "pattern" investigations/

Tier 3: YAML Frontmatter Parsing
        Strukturierte Metadaten für Filter
```

### Datei-Organisation

```
investigations/
├── INV-2025-001.md         # Hypothese + Ergebnisse
├── INV-2025-001_queries/   # Queries/Code
└── INV-2025-001_runs/      # Datierte Ausführungen
    ├── 2025-12-14.md
    └── 2025-12-16.md
```

**Key**: Alle Artefakte teilen dieselbe ID → Sofortige Auffindbarkeit.

## Integration mit Evolving

### Anwendungsfälle

1. **Research Tasks**:
   ```
   /research "Thema" --methodology LOCK
   ```

2. **Debugging**:
   ```
   /debug "Problem" → LOCK-strukturiertes Investigation
   ```

3. **Idea Validation**:
   ```
   /idea-work INV-LOCK → Strukturierte Ideen-Prüfung
   ```

### Mögliche Implementation

```markdown
# investigations/ Ordner

Ähnlich wie hunts/ in ATHF:
- YAML Frontmatter für Metadaten
- LOCK-Struktur für Inhalt
- Datierte Iterationen für Refinement
- Verknüpfung mit ideas/ und knowledge/
```

## Best Practices

1. **Immer dokumentieren**: Auch wenn nichts gefunden wird
2. **Hypothesen testbar formulieren**: Konkret, nicht vage
3. **Tests begrenzen**: Zeit + Ergebnisse cappen
4. **Negative Ergebnisse wertvoll**: "Haben geprüft, war nicht der Fall"
5. **Iterationen tracken**: Datierte Ausführungen zeigen Refinement
6. **Verknüpfungen pflegen**: Related-Feld nutzen

## Vergleich: LOCK vs. Evolving Patterns

| Aspect | LOCK | Evolving /debug |
|--------|------|-----------------|
| Struktur | 4 Phasen | 5 Schritte |
| Fokus | Hypothese → Test | Problem → Fix |
| Output | Investigation Doc | Lösung |
| Persistence | Explizit | Implizit |

**Synergie**: LOCK für explorative Research, /debug für bekannte Probleme.

---

## Related

- `.claude/commands/debug.md` - Problem-fokussiertes Debugging
- `.claude/skills/research-orchestrator/` - Research Skill
- `knowledge/patterns/recursive-research-pattern.md` - Tiefe Analyse
