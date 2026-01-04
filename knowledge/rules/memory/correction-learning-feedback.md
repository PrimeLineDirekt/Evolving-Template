# Correction Learning Feedback

**Priorität**: HOCH
**Trigger**: Bei JEDER User-Korrektur automatisch

---

## Konzept

Wenn {USER} korrigiert ("Nein, mach X statt Y"), wird das systematisch erfasst und führt zu:
1. Sofortigem Preference-Eintrag
2. Anpassung der Autonomie-Schwellwerte
3. Verbesserung zukünftiger Entscheidungen

---

## Korrektur-Erkennung

### Signale für Korrektur

| Signal | Beispiel | Typ |
|--------|----------|-----|
| Explizite Ablehnung | "Nein", "Nicht so", "Falsch" | hard_correction |
| Alternative Anweisung | "Mach stattdessen X", "Lieber Y" | soft_correction |
| Präferenz-Äußerung | "Ich bevorzuge", "Mir gefällt besser" | preference |
| Wiederholung mit Änderung | "Ich meinte X nicht Y" | clarification |

---

## Feedback-Flow

```
User-Korrektur erkannt
    │
    ▼
Klassifiziere Korrektur-Typ
    │
    ├─ hard_correction → Sofort lernen + Autonomy DOWN
    ├─ soft_correction → Lernen + Track
    ├─ preference → Preference speichern
    └─ clarification → Context-Fehler, minimal tracking
    │
    ▼
Experience erstellen (type: preference)
    │
    ▼
User-Profile updaten:
    - corrections_count++
    - domain_specific_corrections[domain]++
    │
    ▼
Autonomy-Threshold anpassen (wenn nötig)
```

---

## Autonomy-Anpassung

### Bei Korrekturen

```
Korrektur in Domain X
    │
    ▼
_memory/user-profile.json:
    domains.X.corrections++
    │
    ├─ corrections > 3 in 7 Tagen?
    │       │
    │       └─ hitl_threshold für Domain X erhöhen
    │          (mehr fragen, weniger autonom)
    │
    └─ corrections = 0 in 14 Tagen?
            │
            └─ hitl_threshold für Domain X senken
               (mehr Autonomie)
```

### Threshold-Formel

```
base_threshold = 0.2  # Default HITL threshold

domain_factor = 1 + (corrections_7d * 0.1)
adjusted_threshold = min(base_threshold * domain_factor, 0.8)
```

---

## Experience-Format (Korrektur)

```json
{
  "type": "preference",
  "summary": "{USER} bevorzugt X über Y in Context Z",
  "category": "workflow",
  "preference": "Bei A immer B machen, nicht C",
  "confidence": 90,
  "correction_context": {
    "original_action": "C gemacht",
    "corrected_to": "B",
    "domain": "typescript",
    "session_id": "..."
  }
}
```

---

## User-Profile Integration

`_memory/user-profile.json`:

```json
{
  "corrections": {
    "total": 15,
    "last_7_days": 2,
    "by_domain": {
      "typescript": 3,
      "architecture": 1,
      "workflow": 2
    }
  },
  "domains": {
    "typescript": {
      "level": "learning",
      "hitl_threshold": 0.3,
      "corrections": 3,
      "last_correction": "2026-01-03"
    }
  }
}
```

---

## Feedback-Loop

```
Session 1: Korrektur → Preference gespeichert
           │
           ▼
Session 2: Ähnliche Situation
           │
           ├─ Preference gefunden?
           │       │
           │       └─ JA: Korrekte Aktion wählen
           │
           └─ Erfolg? → confidence++
                     → hitl_threshold--
```

---

## Reporting

Bei `/memory-stats` zeigen:

```
## Correction Learning

Korrekturen (letzte 7 Tage): 2
Top-Domains: typescript (3), workflow (2)
Angepasste Thresholds:
  - typescript: 0.2 → 0.3 (mehr HITL)

Erfolgreiche Auto-Fixes seit Korrektur: 5
```

---

## Nicht übertreiben

- Einzelne Korrektur = 1x Preference
- Nicht bei jeder Korrektur sofort Autonomy anpassen
- Mindestens 3 Korrekturen in 7 Tagen für Threshold-Änderung
- Nach 14 Tagen ohne Korrektur: Reset möglich

---

## Related

- `autonomy-classifier.md` - Autonomy-Modi
- `auto-learning.md` - Preference-Speicherung
- `_memory/user-profile.json` - User-State
