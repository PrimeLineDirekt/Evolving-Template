# Memory Decay Rule

**Priorität**: NIEDRIG (Background-Optimierung)
**Trigger**: Bei `/recall`, `/memory-stats`, Experience-Suggest

---

## Konzept

Experiences verlieren Relevanz über Zeit, außer sie werden aktiv genutzt.
Dies verhindert Memory-Überladung und priorisiert aktuelle Erfahrungen.

---

## Decay-Formel

```
effective_relevance = base_relevance * exp(-decay_rate * days_since_access)
```

**Standard Decay Rates**:

| Type | Rate | Halbwertszeit |
|------|------|---------------|
| `solution` | 0.005/Tag | ~139 Tage |
| `pattern` | 0.003/Tag | ~231 Tage |
| `decision` | 0.01/Tag | ~69 Tage |
| `workaround` | 0.02/Tag | ~35 Tage |
| `gotcha` | 0.01/Tag | ~69 Tage |
| `preference` | 0.001/Tag | ~693 Tage |

---

## Wann anwenden?

### Bei `/recall` (Suche)

1. Für jede gefundene Experience: `effective_relevance` berechnen
2. Filter: `effective_relevance >= 30`
3. Sortieren nach `effective_relevance` DESC
4. Top-N zurückgeben

### Bei Experience-Suggest (Auto)

1. Potentielle Matches finden
2. `effective_relevance` berechnen
3. Nur vorschlagen wenn `effective_relevance >= 40`

### Bei `/memory-stats`

1. Alle Experiences laden
2. `effective_relevance` für jede berechnen
3. Anzeigen:
   - "Cleanup-Pending": `effective_relevance < 20`
   - "Decay Warning": `effective_relevance < 40`

---

## Access-Boost

Bei jedem Zugriff auf eine Experience:

```
1. last_accessed = heute
2. access_count++
3. base_relevance = min(base_relevance + 5, 100)
```

**Effekt**: Decay-Timer wird zurückgesetzt, Score steigt leicht.

---

## Beispiel-Berechnung

```
Experience: exp-2025-001
Type: solution
base_relevance: 80
last_accessed: vor 60 Tagen
decay_rate: 0.005

effective = 80 * exp(-0.005 * 60)
         = 80 * 0.741
         = 59.3

→ Noch über Threshold (30), wird angezeigt
```

---

## Cleanup-Trigger

Experiences mit `effective_relevance < 10` nach 180+ Tagen:

```
Bei /memory-stats:
  "3 Experiences haben sehr niedrige Relevanz:
   - exp-2024-012: solution (effective: 8.2)
   - exp-2024-015: workaround (effective: 5.1)
   - exp-2024-018: gotcha (effective: 9.0)

   Archivieren? [ja/nein]"
```

---

## Override: Pinned Experiences

User kann Decay deaktivieren:

```json
{
  "decay_config": {
    "pinned": true
  }
}
```

Gepinnte Experiences:
- Kein Decay
- Werden immer in `/memory-stats` angezeigt
- Markiert mit 📌 in Output

---

## Integration

Diese Rule ergänzt:
- `experience-suggest.md` - Decay-aware Filtering
- `/recall` Command - Sorting by effective_relevance
- `/memory-stats` Command - Decay Warnings

Dokumentation: `knowledge/learnings/memory-decay-pattern.md`
