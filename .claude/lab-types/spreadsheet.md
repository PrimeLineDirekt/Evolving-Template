# Lab-Type: Spreadsheet

## Beschreibung
Strukturierte Datenanalyse mit CSV/Excel Output, Feature-Matrices und Vergleichstabellen.

---

## Query-Template (OHNE NEWLINES!)

```
Erstelle eine UMFASSENDE [TABELLEN-TYP] fuer [THEMA]. Spalten: ([SPALTE-1], [SPALTE-2], [SPALTE-3], [SPALTE-4], [SPALTE-5], [SPALTE-6]). Zeilen: Mindestens [ANZAHL] Eintraege, sortiert nach [SORTIER-KRITERIUM]. Zusaetzlich: (1) Bewertungs-Score von 1-10 fuer jede Zeile; (2) Farbcodierung/Highlighting der Top-3 und Bottom-3; (3) Summary-Sektion mit Key Insights und Empfehlungen; (4) Quellenangabe pro Datenpunkt. Datenquellen: [QUELLE-1], [QUELLE-2], [QUELLE-3]. Output: CSV-Export plus Analyse-Summary.
```

---

## Beispiel-Queries (Copy-Paste Ready)

### VPN-Vergleichs-Spreadsheet
```
Erstelle eine UMFASSENDE VERGLEICHS-TABELLE fuer Top 15 VPN-Anbieter 2026. Spalten: (Name, Monatspreis, Jahrespreis, Server-Anzahl, Laender-Abdeckung, Speed-Score 1-10, Privacy-Score 1-10, Streaming-Kompatibilitaet, Torrenting-erlaubt, Besonderheiten). Zeilen: 15 Anbieter sortiert nach Preis-Leistung. Zusaetzlich: (1) Gesamtscore berechnet aus Speed + Privacy + Preis-Leistung; (2) Highlighting der Top-3 und Budget-Empfehlung; (3) Summary mit Empfehlung nach Use-Case (Streaming, Privacy, Business); (4) Quellenangabe pro Anbieter. Datenquellen: Offizielle Websites Januar 2026, TechRadar Reviews, Reddit Erfahrungsberichte. Output: CSV plus detaillierte Analyse.
```

### Digital-Nomad-Staedte-Spreadsheet
```
Erstelle eine UMFASSENDE VERGLEICHS-TABELLE fuer 25 beste Digital Nomad Staedte 2026. Spalten: (Stadt, Land, Monatskosten-Gesamt, Miete-1BR, CoWorking-Tag, Internet-Speed-Mbps, Safety-Score, Weather-Score, Visa-Optionen, Zeitzone-UTC, Nomad-Community-Groesse). Zeilen: 25 Staedte sortiert nach Gesamtscore. Zusaetzlich: (1) Gesamtscore gewichtet (30% Kosten, 25% Internet, 20% Safety, 15% Community, 10% Visa); (2) Highlighting der Top-5 und Hidden-Gems; (3) Summary mit Empfehlung nach Budget ($1000, $1500, $2500+); (4) Quellenangabe Nomad List, Numbeo. Datenquellen: Nomad List Januar 2026, Numbeo Cost of Living, lokale Expat-Gruppen. Output: CSV plus Entscheidungs-Guide.
```

### Feature-Matrix-Spreadsheet
```
Erstelle eine UMFASSENDE FEATURE-MATRIX fuer Note-Taking Apps 2026 (Notion, Obsidian, Roam, Logseq, Capacities, Tana). Spalten: (App-Name, Preis-Free, Preis-Pro, Offline-Mode, Markdown-Support, Backlinks, Graph-View, API, Mobile-Apps, Sync-Optionen, Plugin-System, Collaboration, Export-Formate). Zeilen: 6 Apps mit Checkmarks oder Ja/Nein/Partial. Zusaetzlich: (1) Feature-Count pro App; (2) Highlighting der Feature-Leaders pro Kategorie; (3) Summary mit Empfehlung nach Use-Case (Personal PKM, Team, Developer, Writer); (4) Quellenangaben offizielle Docs. Datenquellen: Offizielle Feature-Pages Januar 2026, Product Hunt Reviews. Output: CSV plus Decision-Matrix.
```

---

## Tabellen-Typen fuer Query

- VERGLEICHS-TABELLE
- FEATURE-MATRIX
- RANKING-TABELLE
- PREIS-LISTE
- SCORING-MATRIX
- DECISION-MATRIX
- CHECKLIST-TABELLE

---

## Spalten-Kategorien

### Allgemein
- Name, Beschreibung, Kategorie, Link/URL

### Preise
- Preis-Free, Preis-Monat, Preis-Jahr, Preis-Lifetime

### Bewertungen
- Score 1-10, Rating 1-5, Sterne, Prozent

### Features
- Checkmark (Ja/Nein), Partial, N/A

### Metriken
- Speed, Size, Count, Duration

### Kommentare
- Besonderheiten, Notizen, Quelle

---

## Erwartete Assets

| Asset | Format | Beschreibung |
|-------|--------|--------------|
| data.csv | CSV | Haupt-Tabelle, importierbar |
| analysis.md | Markdown | Key Insights und Empfehlungen |
| decision-guide.md | Markdown | Entscheidungshilfe |

---

## Qualitaets-Checks

- [ ] CSV ist valide und in Excel/Sheets importierbar?
- [ ] Spalten-Header sind eindeutig?
- [ ] Mindestens 10 Zeilen mit vollstaendigen Daten?
- [ ] Scoring/Bewertung konsistent?
- [ ] Quellen fuer alle Datenpunkte?
- [ ] Summary mit actionable Empfehlungen?
