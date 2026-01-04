# Lab-Type: Dashboard

## Beschreibung
Interaktive Visualisierung mit Charts, Metriken, Filtern und funktionierender Web-App.

---

## Query-Template (OHNE NEWLINES!)

Nutze dieses Template und ersetze die Platzhalter:

```
Erstelle ein INTERAKTIVES [DASHBOARD-TYP] fuer [THEMA]. Features: (1) [INTERAKTIONS-ELEMENT] zum Auswaehlen von [OPTIONEN-LISTE]; (2) [CHART-TYP-1] mit Vergleich auf [ANZAHL] Dimensionen ([DIMENSION-1], [DIMENSION-2], [DIMENSION-3], [DIMENSION-4], [DIMENSION-5]); (3) [CHART-TYP-2] zeigt [METRIK-X] vs [METRIK-Y] fuer alle [ENTITIES]; (4) Tabelle als [TABELLEN-TYP] mit Spalten ([SPALTE-1], [SPALTE-2], [SPALTE-3], [SPALTE-4]); (5) [ZUSATZ-FEATURE] mit [DETAILS]. Datenquellen: [QUELLE-1], [QUELLE-2], [QUELLE-3]. Output: Funktionierendes HTML-Dashboard mit interaktiven Elementen und Export-Option.
```

---

## Beispiel-Queries (Copy-Paste Ready)

### Crypto-Dashboard
```
Erstelle ein INTERAKTIVES KRYPTO-DASHBOARD fuer Bitcoin, Ethereum und Solana Performance 2026. Features: (1) Dropdown zum Coin-Auswaehlen mit Zeitraum-Filter (7 Tage, 30 Tage, 90 Tage, 1 Jahr); (2) Line-Chart zeigt Preisverlauf mit gleitendem Durchschnitt; (3) Bar-Chart fuer taegliches Handelsvolumen; (4) Korrelations-Matrix als Heatmap zwischen allen drei Coins; (5) KPI-Cards zeigen aktuellen Preis, 24h-Aenderung, Market Cap, All-Time-High. Datenquellen: CoinGecko API Daten, aktuelle Marktpreise Januar 2026. Output: Funktionierendes HTML-Dashboard mit Live-aehnlichen Daten und responsivem Design.
```

### SaaS-Metrics-Dashboard
```
Erstelle ein INTERAKTIVES SAAS-METRICS-DASHBOARD fuer Startup-KPIs. Features: (1) Zeitraum-Selector (MTD, QTD, YTD, Custom Range); (2) Line-Charts fuer MRR, ARR, Churn Rate im Zeitverlauf; (3) Funnel-Visualisierung fuer Trial zu Paid Conversion; (4) Cohort-Tabelle zeigt Retention nach Signup-Monat; (5) KPI-Cards mit MRR, Active Users, NPS Score, CAC, LTV. Datenquellen: Typische SaaS-Benchmarks 2026, Industry Standards. Output: Dashboard mit Dummy-Daten die realistisch aussehen, Dark-Mode Design.
```

### Framework-Vergleich-Dashboard
```
Erstelle ein INTERAKTIVES VERGLEICHS-DASHBOARD fuer [FRAMEWORKS]. Features: (1) Dropdown zum Framework-Auswaehlen ([FRAMEWORK-1], [FRAMEWORK-2], [FRAMEWORK-3], [FRAMEWORK-4], [FRAMEWORK-5]); (2) Radar-Chart mit Vergleich auf 5 Dimensionen (Performance, Ease-of-Use, Cost, [SPEZIFISCH-1], [SPEZIFISCH-2]); (3) Scatter-Plot zeigt [METRIK-X] vs [METRIK-Y] fuer alle Frameworks; (4) Feature-Matrix Tabelle mit Checkmarks ([FEATURE-1], [FEATURE-2], [FEATURE-3], [FEATURE-4]); (5) Code-Snippet-Box mit Hello-World Beispiel pro Framework. Datenquellen: GitHub Stars Januar 2026, offizielle Dokumentation, Benchmark-Papers. Output: Funktionierendes HTML-Dashboard mit interaktiven Elementen.
```

---

## Feature-Optionen

### Interaktions-Elemente
- Dropdown / Select-Box
- Multi-Select mit Tags
- Radio-Buttons
- Slider (Range)
- Date-Picker
- Search/Filter-Input
- Toggle-Switches

### Chart-Typen
- Line-Chart (Zeitreihen)
- Bar-Chart (Vergleich/Ranking)
- Radar/Spider-Chart (Multi-Dimensional)
- Scatter-Plot (X vs Y)
- Pie/Donut-Chart (Anteile)
- Heatmap (Korrelation/Matrix)
- Funnel-Chart (Conversion)
- Treemap (Hierarchie)
- Gauge-Chart (KPI mit Ziel)

### Tabellen-Typen
- Feature-Matrix (Checkmarks)
- Ranking-Tabelle (sortierbar)
- Comparison-Table (Side-by-Side)
- Data-Grid (filterbar)

### KPI-Elemente
- Metric-Cards mit Trend-Indikator
- Sparklines (Mini-Charts)
- Progress-Bars
- Status-Badges

---

## Erwartete Assets

| Asset | Format | Beschreibung |
|-------|--------|--------------|
| dashboard.html | HTML | Interaktives Dashboard (selbststaendig) |
| Inline CSS/JS | - | Styles und Logic im HTML |
| charts/ | PNG | Fallback statische Charts |
| data.json | JSON | Strukturierte Daten |

---

## Post-Processing

1. **HTML herunterladen**: "Als HTML herunterladen" Button nutzen
2. **Lokal testen**: HTML-Datei im Browser oeffnen, Interaktionen pruefen
3. **Screenshots**: Verschiedene States dokumentieren
4. **Speichern**:
   ```
   knowledge/labs/{date}-{topic}/
   ├── README.md
   ├── dashboard.html
   ├── screenshots/
   │   ├── overview.png
   │   └── filtered-view.png
   └── data.json (falls extrahierbar)
   ```

---

## Qualitaets-Checks

- [ ] Dropdown/Filter funktioniert?
- [ ] Charts aktualisieren bei Auswahl?
- [ ] Alle Datenpunkte korrekt?
- [ ] Responsives Layout?
- [ ] Lesbare Achsenbeschriftungen?
- [ ] Legende vorhanden?
- [ ] Datenquelle genannt?
