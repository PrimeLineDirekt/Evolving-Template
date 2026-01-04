# Automatische Archivierung

**Priorität**: NIEDRIG (Proaktiv bei Session-Ende)
**Trigger**: Bei `/whats-next`, Session-Ende, oder wenn Claude Archivierung erkennt

---

## Konzept

Alte Handoffs, abgeschlossene Pläne und Ledgers sollen automatisch archiviert werden, OHNE dass der User daran erinnern muss.

---

## Wann archivieren?

### Bei Session-Ende (nach /whats-next)

1. **Ledger prüfen**: Ist `_ledgers/CURRENT.md` als ABGESCHLOSSEN markiert?
   - Ja → Archivieren nach `_ledgers/archive/YYYY-MM-DD-{topic}.md`
   - Nein → Behalten

2. **Handoffs prüfen**: Sind Handoffs älter als 14 Tage?
   - Ja → Nach `_handoffs/archive/` verschieben
   - Nein → Behalten

3. **Pläne prüfen**: Ist ein Plan als COMPLETED markiert?
   - Ja → Nach `knowledge/plans/archive/` verschieben
   - Nein → Behalten (Parked Plans bleiben!)

---

## Archiv-Struktur

```
_ledgers/
├── CURRENT.md              # Aktives Ledger
└── archive/
    └── YYYY-MM-DD-{topic}.md

_handoffs/
├── {aktuelle handoffs}     # < 14 Tage
└── archive/
    └── {alte handoffs}     # > 14 Tage

knowledge/plans/
├── {parked/active plans}   # Warten auf Implementation
└── archive/
    └── {completed plans}   # Status: COMPLETED/ARCHIVED
```

---

## Automatische Checks

### Bei jedem Session-Start (domain-memory-bootup)

Nach Memory-Check kurz prüfen:
- Alte Handoffs vorhanden? → Mention: "X Handoffs könnten archiviert werden"
- Ledger abgeschlossen? → Automatisch archivieren + neues Template
- Plan completed? → Mention: "Plan X ist abgeschlossen, archivieren?"

### Bei /whats-next

Am Ende des Handoff-Erstellens:
1. Aktuelles Ledger archivieren (wenn abgeschlossen)
2. Prüfen ob alte Handoffs da sind
3. Neue leere CURRENT.md erstellen

---

## Archivierungs-Workflow

```bash
# Ledger archivieren
mv _ledgers/CURRENT.md _ledgers/archive/YYYY-MM-DD-{topic}.md

# Alte Handoffs archivieren (> 14 Tage)
mv _handoffs/2025-12-01-*.md _handoffs/archive/

# Completed Plan archivieren
mv knowledge/plans/{plan}.md knowledge/plans/archive/
```

---

## Kriterien für Archivierung

| Typ | Kriterium | Ziel-Ordner |
|-----|-----------|-------------|
| Ledger | Status: ABGESCHLOSSEN | `_ledgers/archive/` |
| Handoffs | Älter als 14 Tage | `_handoffs/archive/` |
| Pläne | Status: COMPLETED/ARCHIVED | `knowledge/plans/archive/` |

### Was NICHT archiviert wird

- **Parked Plans**: Warten auf Implementation
- **Aktuelle Handoffs**: < 14 Tage alt
- **CURRENT.md**: Nur wenn abgeschlossen

---

## Proaktive Erinnerung

Bei Session-Start, wenn Archivierung nötig:

```
"Housekeeping: 5 Handoffs älter als 14 Tage, 1 abgeschlossenes Ledger.
 Soll ich archivieren? [ja/nein]"
```

**Wichtig**: Nicht nervig sein - maximal 1x pro Session erwähnen.

---

## Integration

Diese Rule erweitert:
- `domain-memory-bootup.md` - Archiv-Check nach Memory-Load
- `/whats-next` - Automatisches Ledger-Archivieren
- `session-summary.sh` Hook - Archiv-Reminder am Ende
