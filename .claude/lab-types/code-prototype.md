# Lab-Type: Code Prototype

## Beschreibung
Funktionierender Code oder Mini-Web-App mit professioneller Struktur und Dokumentation.

---

## Query-Template (OHNE NEWLINES!)

```
Baue eine FUNKTIONIERENDE [APP-TYP] fuer [ZWECK]. Features: (1) [FEATURE-1] mit [UI-ELEMENT-1]; (2) [FEATURE-2] mit [FUNKTIONALITAET]; (3) [FEATURE-3] fuer [USE-CASE]; (4) [FEATURE-4] speichert/zeigt [DATEN]. Technische Anforderungen: [TECH-1], [TECH-2], [TECH-3]. Design: [DESIGN-STIL] mit [FARB-SCHEMA]. Code-Qualitaet: Kommentiert, modular, produktionsreif. Output: Vollstaendiges HTML/CSS/JS Bundle das standalone laeuft, mit README zur Anpassung.
```

---

## Beispiel-Queries (Copy-Paste Ready)

### Pomodoro-Timer App
```
Baue eine FUNKTIONIERENDE POMODORO-TIMER WEB-APP fuer Produktivitaets-Tracking. Features: (1) Timer-Display zeigt Minuten:Sekunden gross in der Mitte; (2) Start/Pause/Reset Buttons mit Keyboard-Shortcuts (Space, R); (3) Einstellbare Zeiten fuer Work (25min default), Short Break (5min), Long Break (15min); (4) Session-Counter zeigt abgeschlossene Pomodoros; (5) Audio-Notification bei Timer-Ende mit auswaehlbaren Sounds; (6) LocalStorage speichert Einstellungen und taegliche Stats. Technische Anforderungen: Vanilla JS ohne Frameworks, CSS Custom Properties fuer Theming, Service Worker fuer Offline-Nutzung. Design: Minimalistisch Dark-Mode mit Akzentfarbe Tomato-Red. Code-Qualitaet: Kommentiert, ES6+ Syntax, modular aufgebaut. Output: Vollstaendiges HTML/CSS/JS Bundle.
```

### Expense-Tracker App
```
Baue eine FUNKTIONIERENDE EXPENSE-TRACKER WEB-APP fuer persoenliche Finanzen. Features: (1) Eingabeformular fuer Betrag, Kategorie (Dropdown: Food, Transport, Entertainment, Shopping, Bills, Other), Datum, Notiz; (2) Transaktions-Liste zeigt alle Eintraege sortiert nach Datum mit Edit/Delete; (3) Dashboard-Bereich zeigt Monatssumme, Kategorie-Aufschluesselung als Pie-Chart, Trend-Graph letzte 6 Monate; (4) Filter nach Kategorie und Zeitraum; (5) Export-Button fuer CSV-Download; (6) LocalStorage Persistenz mit Import/Export JSON. Technische Anforderungen: Vanilla JS, Chart.js fuer Visualisierungen, CSS Grid Layout. Design: Clean Light-Mode mit gruenen (Income) und roten (Expense) Akzenten. Code-Qualitaet: MVC-artige Struktur, kommentiert, Fehlerbehandlung. Output: Vollstaendiges Bundle mit Chart.js CDN-Link.
```

### Unit-Converter App
```
Baue eine FUNKTIONIERENDE UNIT-CONVERTER WEB-APP fuer alltaegliche Umrechnungen. Features: (1) Kategorie-Tabs (Laenge, Gewicht, Temperatur, Volumen, Zeit, Digital-Storage); (2) Von-Nach Dropdowns mit allen relevanten Einheiten pro Kategorie; (3) Echtzeit-Konvertierung bei Eingabe ohne Submit-Button; (4) Swap-Button tauscht Von/Nach; (5) Formel-Anzeige zeigt verwendete Umrechnung; (6) History-Sektion speichert letzte 10 Konvertierungen. Technische Anforderungen: Vanilla JS mit Conversion-Functions als eigenes Modul, CSS Flexbox, keine externen Libraries. Design: Material Design inspiriert mit Card-Layout, Light/Dark Toggle. Code-Qualitaet: Alle Conversions getestet, erweiterbar fuer neue Kategorien, kommentiert. Output: Single HTML-File mit embedded CSS/JS.
```

### API-Dashboard-Prototyp
```
Baue einen FUNKTIONIERENDEN API-DASHBOARD-PROTOTYP fuer REST-API Monitoring. Features: (1) Endpoint-Liste zeigt Status (Up/Down), Response-Time, Last-Checked; (2) Add-Endpoint Form mit URL, Name, Check-Interval; (3) Status-Karten zeigen Uptime-Prozent letzte 24h pro Endpoint; (4) Response-Time Chart zeigt Verlauf mit Anomalie-Highlighting; (5) Notification-Settings fuer Email-Alert bei Downtime (UI only, kein Backend); (6) Mock-Daten Generator fuer Demo-Purposes. Technische Anforderungen: Vanilla JS mit Fetch API Simulation, Chart.js fuer Graphs, CSS Variables fuer Status-Farben (green/yellow/red). Design: Dashboard-Style mit Sidebar Navigation, Dark-Mode default. Code-Qualitaet: Async/Await Pattern, Error-Handling, leicht anpassbar fuer echte APIs. Output: Demo-ready Dashboard mit simulierten Daten.
```

---

## App-Typen fuer Query

- WEB-APP
- CALCULATOR
- CONVERTER
- TRACKER
- TIMER
- DASHBOARD
- FORM-BUILDER
- VISUALIZER
- GAME
- TOOL

---

## Feature-Bausteine

### UI-Elemente
- Form mit Inputs/Dropdowns/Buttons
- Cards/Tiles fuer Datenanzeige
- Tabs/Accordion fuer Navigation
- Modal/Popup fuer Details
- Toast-Notifications

### Funktionalitaet
- CRUD Operations (Create/Read/Update/Delete)
- Real-time Updates
- Filtering/Sorting
- Search/Autocomplete
- Drag & Drop

### Persistenz
- LocalStorage
- SessionStorage
- Export/Import (JSON, CSV)
- URL-Parameter State

### Visualisierung
- Charts (Line, Bar, Pie, Radar)
- Progress-Bars
- Status-Indicators
- Sparklines

---

## Technische Optionen

| Option | Beschreibung |
|--------|--------------|
| Vanilla JS | Keine Dependencies, maximale Kontrolle |
| + Chart.js | Fuer Visualisierungen (CDN) |
| + Tailwind | Utility-First CSS (CDN) |
| Single-File | Alles in einer HTML-Datei |
| Modular | Separate CSS/JS Files |

---

## Design-Stile

- Minimalistisch (wenig Farben, viel Whitespace)
- Material Design (Cards, Shadows, Ripples)
- Glassmorphism (Blur, Transparenz)
- Brutalist (Bold, Raw)
- Dashboard-Style (Sidebar, Grids, Metrics)

---

## Erwartete Assets

| Asset | Format | Beschreibung |
|-------|--------|--------------|
| index.html | HTML | Haupt-Datei oder Single-File |
| style.css | CSS | Styling (falls separiert) |
| script.js | JS | Logik (falls separiert) |
| README.md | Markdown | Setup und Anpassungs-Guide |

---

## Qualitaets-Checks

- [ ] App laeuft ohne Fehler im Browser?
- [ ] Alle Features funktionieren?
- [ ] Responsive auf Mobile?
- [ ] Code ist kommentiert?
- [ ] Keine Console-Errors?
- [ ] Einfach anpassbar (Farben, Texte)?
