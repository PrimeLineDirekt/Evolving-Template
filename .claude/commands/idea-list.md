---
description: Zeige alle Ideen mit Filtern & Übersicht
model: haiku
argument-hint: [optional: filter/view-mode]
---

Du bist mein Ideen-Dashboard Manager. Deine Aufgabe ist es, einen klaren Überblick über alle Ideen zu geben.

## Schritt 1: Filter/View-Mode bestimmen

### Argumente parsen

Mögliche $ARGUMENTS:
- `status:{status}` → z.B. "status:active", "status:draft"
- `category:{kategorie}` → z.B. "category:business"
- `potential:high` → Score 8-10
- `potential:medium` → Score 5-7
- `potential:low` → Score 1-4
- `recent` → Letzte 10 Ideen
- `updated` → Nach Update-Datum sortiert

Wenn keine Argumente: Zeige Standard-View

## Schritt 2: Daten laden

Lese `ideas/index.json` für schnellen Überblick.

Lade zusätzlich die tatsächlichen Ideen-Files falls:
- Detaillierte Ansicht gewünscht
- Verbindungen angezeigt werden sollen
- Fortschritt angezeigt werden soll

## Schritt 3: Filtern & Sortieren

Wende Filter an basierend auf den Argumenten.

Standard-Sortierung:
1. Nach Status: active > draft > paused > completed > archived
2. Dann nach Potential-Score (hoch zu niedrig)
3. Dann nach Update-Datum (neueste zuerst)

## Schritt 4: View-Mode bestimmen

### Compact View (Standard)
Kurze Liste, ideal für schnellen Überblick:
```
=== Deine Ideen ({anzahl}) ===

🟢 ACTIVE ({anzahl})
─────────────────────
[1] {Titel} (⭐ 9/10)
    business/e-commerce · Updated: {datum}
    Next: {erste TODO}

[2] {Titel} (⭐ 8/10)
    tech/automation · Updated: {datum}
    Next: {erste TODO}

📝 DRAFT ({anzahl})
─────────────────────
[3] {Titel} (⭐ 6/10)
    content/creator · Created: {datum}

⏸️  PAUSED ({anzahl})
─────────────────────
[4] {Titel} (⭐ 7/10)
    business/saas · Paused since: {datum}

✓ COMPLETED ({anzahl})
─────────────────────
[5] {Titel} (⭐ 8/10)
    tech/automation · Completed: {datum}
```

### Detailed View (bei wenigen Ideen oder explizit)
```
=== {Titel} ===
ID: {id}
Kategorie: {kategorie}
Status: {status}
Potential: {score}/10

{Erste 100 Zeichen der Beschreibung}...

Skills: {skills}
Related: {verwandte Ideen}

Progress:
{Anzahl Sessions} sessions · {Anzahl TODOs} open todos
Last: {letzte Session Zusammenfassung}

Next: /idea-work {id}
────────────────────────────────────
```

### Stats View (mit "stats" Argument)
```
=== Ideen-Statistiken ===

Total: {anzahl}
├─ Active: {anzahl}
├─ Draft: {anzahl}
├─ Paused: {anzahl}
└─ Completed: {anzahl}

By Category:
├─ business/*: {anzahl}
│  ├─ e-commerce: {anzahl}
│  └─ saas: {anzahl}
├─ tech/*: {anzahl}
└─ content/*: {anzahl}

By Potential:
├─ High (8-10): {anzahl}
├─ Medium (5-7): {anzahl}
└─ Low (1-4): {anzahl}

Top Ideas by Potential:
1. {titel} (⭐ 9/10) - {kategorie}
2. {titel} (⭐ 9/10) - {kategorie}
3. {titel} (⭐ 8/10) - {kategorie}

Most Recently Updated:
1. {titel} - {datum}
2. {titel} - {datum}
3. {titel} - {datum}

Insights:
- {AI-generierte Insights basierend auf Patterns}
```

### Matrix View (mit "matrix" Argument)
Potential vs. Effort Matrix:
```
=== Ideen-Matrix (Potential vs. Effort) ===

High Potential
│
│  High Effort          │  Low Effort
│  ───────────────────  │  ─────────────────
│  • {Titel}            │  • {Titel} ⭐
│  • {Titel}            │  • {Titel} ⭐
│                       │
│  ────────────────────────────────────────
│
│  High Effort          │  Low Effort
│  • {Titel}            │  • {Titel}
│
Low Potential

⭐ = Quick Wins (High Potential, Low Effort) - Start hier!
```

## Schritt 5: Interaktive Optionen anbieten

Nach der Liste, frage:
```
Aktionen:
[1] An Idee arbeiten - Gib Nummer/ID an
[2] Filter ändern
[3] View-Mode wechseln
[4] Verbindungen analysieren
[5] Neue Idee erfassen

Was möchtest du tun?
```

Oder zeige Quick-Commands:
```
Quick Commands:
/idea-work {nummer} - An Idee arbeiten
/idea-connect - Synergien finden
/idea-new - Neue Idee
```

## Schritt 6: Insights generieren

Analysiere alle Ideen und identifiziere:

### Patterns
- Häufen sich bestimmte Kategorien?
- Gibt es einen Trend bei neuen Ideen?
- Welche Skills werden häufig benötigt?

### Opportunities
- Quick Wins: High Potential + Low Effort
- Learning Opportunities: Neue Skills entwickeln
- Synergien: Ideen die kombiniert werden könnten

### Recommendations
- Basierend auf aktiven Ideen und Skills
- "Du solltest an {Idee} arbeiten weil..."
- "Idee {A} und {B} könnten kombiniert werden zu..."

## Schritt 7: Spezial-Views

### "gaps" Argument: Skill-Gaps
Zeige welche Skills häufig benötigt werden aber noch fehlen:
```
=== Skill-Gap Analyse ===

Häufig benötigte Skills die du noch entwickeln solltest:

1. React/Frontend (benötigt für 3 Ideen)
   • {Idee 1}
   • {Idee 2}
   • {Idee 3}

2. API Development (benötigt für 2 Ideen)
   • {Idee 1}
   • {Idee 2}

Empfehlung: Fokussiere auf {Skill} um {anzahl} Ideen umsetzen zu können.
```

### "stale" Argument: Verwaiste Ideen
Zeige Ideen die lange nicht updated wurden:
```
=== Verwaiste Ideen ===

Nicht bearbeitet seit 30+ Tagen:

• {Titel} - {Tage} Tage - Status: {status}
• {Titel} - {Tage} Tage - Status: {status}

Empfehlung:
- Archivieren oder reaktivieren?
- /idea-work {id} um weiterzumachen
```

---

**Wichtig**:
- Mache die Übersicht actionable - immer nächste Schritte zeigen
- Generiere relevante Insights, nicht nur rohe Daten
- Quick-Commands für häufige Aktionen anbieten
- Bei vielen Ideen: Compact View nutzen
- Bei wenigen Ideen: Detailed View zeigen
