# Memory Decay Pattern

**Source**: QuixiAI/agi-memory, vectorize-io/hindsight
**Typ**: Learning
**Relevanz**: MITTEL - Optimiert Experience Memory über Zeit
**Erstellt**: 2025-12-22

---

## Problem

Statische Relevanz-Scores führen zu:
- Veraltete Experiences bleiben prominent
- Memory wird überladen mit irrelevanten Einträgen
- Keine natürliche "Vergessens"-Kurve wie bei Menschen
- Manual Cleanup erforderlich

**Aktueller Status in Evolving**:
- `relevance_score` ist statisch (nur manuell anpassbar)
- Experiences bleiben ewig mit gleichem Score
- Kein automatischer Decay

---

## Lösung: Time-Based Decay

### Kernformel

```
effective_relevance = base_relevance * decay_factor

decay_factor = exp(-decay_rate * days_since_access)
```

**Variablen**:
| Variable | Beschreibung | Default |
|----------|--------------|---------|
| `base_relevance` | Ursprünglicher relevance_score | 50-100 |
| `decay_rate` | Wie schnell Decay passiert | 0.01 (1%/Tag) |
| `days_since_access` | Tage seit letztem Zugriff | Berechnet |

### Decay-Kurve Beispiel

```
Tag 0:   100 * exp(-0.01 * 0)   = 100.0  (100%)
Tag 7:   100 * exp(-0.01 * 7)   = 93.2   (93%)
Tag 30:  100 * exp(-0.01 * 30)  = 74.1   (74%)
Tag 90:  100 * exp(-0.01 * 90)  = 40.7   (41%)
Tag 180: 100 * exp(-0.01 * 180) = 16.5   (17%)
```

### Access Boost

Bei jedem Zugriff:
1. `last_accessed` = heute
2. `access_count++`
3. Optional: `base_relevance += 5` (bis max 100)

**Effekt**: Häufig genutzte Experiences bleiben relevant.

---

## Implementation für Evolving

### Schema-Erweiterung für Experiences

```json
{
  "id": "exp-2025-001",
  "type": "solution",
  "relevance_score": 85,
  "decay_config": {
    "decay_rate": 0.01,
    "min_score": 10,
    "boost_on_access": 5
  },
  "access_tracking": {
    "created": "2025-12-01",
    "last_accessed": "2025-12-20",
    "access_count": 7
  }
}
```

### Berechnungs-Logik (Pseudocode)

```python
def calculate_effective_relevance(experience):
    import math
    from datetime import datetime

    # Parse dates
    last_accessed = datetime.fromisoformat(
        experience['access_tracking']['last_accessed']
    )
    now = datetime.now()
    days_since = (now - last_accessed).days

    # Get config
    decay_rate = experience.get('decay_config', {}).get('decay_rate', 0.01)
    min_score = experience.get('decay_config', {}).get('min_score', 10)
    base_score = experience['relevance_score']

    # Calculate decay
    decay_factor = math.exp(-decay_rate * days_since)
    effective_score = base_score * decay_factor

    # Apply minimum
    return max(effective_score, min_score)
```

### Integration in experience-suggest.md Rule

```markdown
## Decay-Aware Filtering

Vor dem Vorschlagen von Experiences:

1. `effective_relevance` berechnen (nicht raw score)
2. Filter: `effective_relevance >= 30`
3. Sortieren nach `effective_relevance` DESC
4. Bei Zugriff: Access-Tracking updaten
```

---

## Decay-Rate Empfehlungen

| Experience Type | Decay Rate | Begründung |
|-----------------|------------|------------|
| `solution` | 0.005 (0.5%/Tag) | Lösungen bleiben lange relevant |
| `pattern` | 0.003 (0.3%/Tag) | Patterns sind zeitlos |
| `decision` | 0.01 (1%/Tag) | Entscheidungen werden revisited |
| `workaround` | 0.02 (2%/Tag) | Workarounds werden obsolet |
| `gotcha` | 0.01 (1%/Tag) | Stolperfallen bleiben relevant |
| `preference` | 0.001 (0.1%/Tag) | User-Präferenzen ändern sich selten |

---

## Cleanup-Strategie

### Automatischer Cleanup

Experiences mit `effective_relevance < 10` nach 180 Tagen:

```
Option A: Archivieren → _memory/experiences/archive/
Option B: Löschen (nach User-Bestätigung)
Option C: In /memory-stats als "Cleanup-Pending" anzeigen
```

### Manueller Override

User kann Decay verhindern:
```json
{
  "decay_config": {
    "decay_rate": 0,  // Kein Decay
    "pinned": true    // Immer relevant
  }
}
```

---

## Vergleich: Vor/Nach Decay

### Ohne Decay (aktuell)

```
exp-2024-001: relevance_score = 90 (1 Jahr alt, nie genutzt)
exp-2025-050: relevance_score = 70 (1 Woche alt, 5x genutzt)

→ Alte Experience wird bevorzugt obwohl irrelevant
```

### Mit Decay (neu)

```
exp-2024-001: effective = 90 * exp(-0.01 * 365) = 2.3
exp-2025-050: effective = 70 * exp(-0.01 * 7) = 65.2

→ Aktive Experience wird korrekt bevorzugt
```

---

## Hindsight-Ergänzung: Reflect Operation

AGI-Memory und Hindsight haben eine **Reflect** Operation:
- Analysiert bestehende Memories
- Generiert neue Insights aus Patterns
- Könnte als `/reflect` Command implementiert werden

**Beispiel**:
```
/reflect

Analysiere: 47 Experiences aus den letzten 90 Tagen

Erkannte Patterns:
1. TypeScript Errors: 8 Solutions → Gemeinsamer Root Cause: Interface-Mismatches
2. API Integration: 5 Workarounds → Sollte als Pattern konsolidiert werden
3. Dashboard Bugs: 12 Gotchas → Häufigster Trigger: State Management

Vorschlag: 3 neue Pattern-Experiences erstellen?
```

---

## Related

- [Experience Memory System](_memory/experiences/)
- [Experience Suggest Rule](.claude/rules/experience-suggest.md)
- [Memory Decay Rule](.claude/rules/memory-decay.md) (NEU)

---

**Navigation**: [← Learnings](README.md) | [Knowledge Index](../index.md)
