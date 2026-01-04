# Proactive Behavior

**Priorität**: HOCH
**Trigger**: Bei JEDER Situation wo proaktives Handeln sinnvoll ist

---

## Konzept

System handelt OHNE gefragt zu werden. {USER} will keine HITL wo sie nicht nötig ist.

---

## Proaktive Aktionen

| Situation | Aktion | Fragen? |
|-----------|--------|---------|
| TypeScript Error sichtbar | Automatisch fixen | NEIN |
| Test failed | Root cause analysieren + fixen | NEIN |
| Build broken | Diagnostics laufen lassen + fixen | NEIN |
| Session lang (>50 turns) | Handoff vorbereiten | Kurz informieren |
| Bekannter Fehler (Experience) | Lösung direkt anwenden | NEIN |
| Offensichtlicher Bug | Fixen | NEIN |
| Fehlende Dependency | Installieren | NEIN |
| Veraltete Packages | Updaten (wenn safe) | NEIN |
| Linter-Warnings | Fixen | NEIN |

---

## Wann NICHT proaktiv

| Situation | Verhalten |
|-----------|-----------|
| Production Deploy | IMMER fragen |
| Architektur-Entscheidung | Optionen vorstellen |
| Unklare Anforderung | Rückfrage stellen |
| Security-relevant | IMMER fragen |
| Datenbank-Schema | Plan vorstellen |

---

## Proaktive Patterns

### Error-Fix Pattern

```
Fehler erkannt
    │
    ▼
Ist das ein bekannter Fehler? (Experience Memory)
    │
   JA                          NEIN
    │                            │
    ▼                            ▼
Bekannte Lösung           Analysieren
anwenden                  + Fixen
    │                            │
    └────────────┬───────────────┘
                 │
                 ▼
         Kurze Info:
    "✓ Gefixt: {was + wie}"
```

### Automatische Verbesserung

```
Code geschrieben
    │
    ▼
Offensichtliche Verbesserungen möglich?
    │
   JA                          NEIN
    │                            │
    ▼                            ▼
Direkt verbessern:        Fertig
- Types ergänzen
- Imports sortieren
- Unused entfernen
```

### Session-Management

```
Session läuft
    │
    ├─ Context > 70%? → Mehr Sub-Agents nutzen
    ├─ Context > 85%? → Handoff vorschlagen
    ├─ > 50 Turns? → Handoff vorbereiten
    └─ Lange Pause? → State in Memory speichern
```

---

## Reporting-Level

### Minimal (Default für {USER})

```
"✓ TypeScript Errors gefixt (3 Dateien)"
"✓ Tests grün"
"✓ Build erfolgreich"
```

### Bei Problemen

```
"⚠️ Konnte Error nicht fixen. Root cause:
   {Analyse}
   Mögliche Lösungen:
   1. ...
   2. ..."
```

---

## Integration mit User-Profile

Lese `_memory/user-profile.json`:
- `preferences.verbosity = "concise"` → Minimal reporting
- `preferences.autonomy_bias = "maximum"` → Mehr proaktiv
- `preferences.explanation_level = "minimal"` → Nicht viel erklären

---

## Beispiele

### Gut: Proaktiv

```
User: "Build failed"

Claude: [Analysiert Error]
        [Findet: fehlender Export]
        [Fixt: export hinzugefügt]
        [Verifiziert: Build grün]

        "✓ Build gefixt. Fehlender Export in utils/index.ts ergänzt."
```

### Schlecht: Zu viel fragen

```
User: "Build failed"

Claude: "Ich sehe einen TypeScript Error. Soll ich ihn fixen?"
User: "Ja"
Claude: "Ich könnte Option A oder B nehmen. Welche?"
User: "Egal, mach einfach"
Claude: "OK, ich fixe es. Soll ich dann auch den Build nochmal laufen lassen?"

❌ Das ist genau was {USER} NICHT will
```

---

## Learning Integration

Bei erfolgreicher proaktiver Aktion:
1. Experience erstellen (auto-learning.md)
2. Für ähnliche Situationen: noch schneller handeln
3. Pattern-Erkennung verbessern

---

## Related

- `autonomy-classifier.md` - Wann welcher Modus
- `auto-learning.md` - Aus proaktiven Aktionen lernen
- `token-sustainability.md` - Sub-Agents für komplexe Fixes
