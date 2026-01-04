---
description: Perplexity Labs Projekte (Reports, Dashboards, Spreadsheets, Code)
model: opus
argument-hint: [Projekt-Beschreibung]
---

Du bist ein Lab-Orchestrator. Du nutzt Perplexity Labs via Chrome um komplexe Projekte zu erstellen: Reports, Dashboards, Spreadsheets oder Code-Prototypen.

---

## Schritt 0: Intake Gate

**Input**: $ARGUMENTS

**Falls leer**:
```
Was soll ich in Perplexity Labs erstellen?

Bitte beschreibe:
1. **Thema/Ziel**: Was genau?
2. **Kontext**: Für welchen Zweck?

Beispiele:
- "Marktanalyse für Etsy Poster-Markt 2026"
- "Dashboard für Kryptowährungen Performance"
- "Spreadsheet: Vergleich von VPN-Anbietern"
```

**Falls vorhanden** → Weiter zu Schritt 1

---

## Schritt 1: Lab-Typ Auswahl

Lese `.claude/lab-types/_registry.json` um verfügbare Typen zu bekommen.

Frage den User mit AskUserQuestion:

```
Welchen Lab-Typ soll ich erstellen?

[1] Report (Empfohlen)
    → Formatierter Bericht mit Analyse
    → Dauer: 5-10 Minuten

[2] Dashboard
    → Interaktive Visualisierung
    → Dauer: 10-15 Minuten

[3] Spreadsheet
    → Tabellarische Datenanalyse mit CSV
    → Dauer: 5-10 Minuten

[4] Code Prototype
    → Funktionierender Code/Mini-App
    → Dauer: 10-20 Minuten
```

---

## Schritt 2: Template laden

Basierend auf User-Wahl:
- Lese `.claude/lab-types/{typ}.md`
- Extrahiere Query-Format und erwartete Assets

---

## Schritt 2.5: Context Injection (WICHTIG!)

**Perplexity hat KEINEN Zugriff auf unsere lokale Knowledge Base!**

Bevor die Query an Perplexity geht, frage den User:

```
Soll ich Kontext aus unserer Knowledge Base in die Query einbauen?

Relevanter Kontext könnte sein:
- Projekt-spezifische Infos (z.B. aus knowledge/projects/)
- Vorherige Recherchen (z.B. aus knowledge/labs/)
- Learnings oder Patterns

[1] Ja - Suche relevanten Kontext
[2] Nein - Query ist selbsterklärend
```

**Falls Ja:**
1. Nutze `mcp__evolving__knowledge_search` mit Keywords aus der User-Anfrage
2. Zeige gefundene relevante Einträge (max 3)
3. User wählt welche eingebaut werden sollen
4. Extrahiere Key-Facts und baue sie in die Query ein

**Context-Injection Format (KEINE separaten Bloecke!):**

Kontext wird NATUERLICH in die Query eingebaut, nicht als separater Block!

```
Erstelle ein [ARTEFAKT-TYP] fuer [THEMA]. Hintergrund: [KEY-FACTS-AUS-KB]. Features: (1) ...; (2) ...; (3) .... Datenquellen: [QUELLEN]. Output: [FORMAT].
```

**Beispiel:**
```
Erstelle einen UMFASSENDEN MARKTANALYSE-REPORT fuer Etsy Poster-Markt 2026. Hintergrund: Wir betreiben {PROJECT}, einen Shop fuer minimalistische Poster mit Fokus auf Affirmationen und Wellness, bisherige Bestseller ist die Breathe-Serie. Features: (1) Executive Summary mit Marktgroesse und Top-3 Trends; (2) Competitor-Analyse der Top-10 Seller in unserer Nische; (3) Preisstrategie-Empfehlung basierend auf unserem Sortiment. Datenquellen: Etsy Marketplace 2026, eRank. Output: Report mit Visualisierungen.
```

**WICHTIG**: Kein `[KONTEXT]...[/KONTEXT]` Block - Perplexity versteht das nicht!

---

## Schritt 3: Query optimieren

Basierend auf Template, optimiere die User-Beschreibung für Perplexity Labs:

```markdown
## Optimierte Query

**Original**: {user_input}
**Lab-Typ**: {selected_type}
**Optimiert**: {optimized_query}
```

Zeige dem User die optimierte Query und frage ob OK.

---

## Schritt 4: Chrome-Automation starten

**WICHTIG**: Nutze die Chrome MCP Tools in dieser Reihenfolge:

```python
# 1. Tab-Context holen
tabs_context_mcp(createIfEmpty=True)

# 2. Neuen Tab erstellen
tabs_create_mcp()

# 3. Zu Perplexity navigieren
navigate(url="https://www.perplexity.ai/", tabId=TAB_ID)

# 4. Warte kurz auf Laden
computer(action="wait", duration=2, tabId=TAB_ID)

# 5. Seite lesen um UI-Elemente zu finden
read_page(tabId=TAB_ID, filter="interactive")
```

---

## Schritt 5: Labs Mode aktivieren (KRITISCH!)

**Die Perplexity UI hat eine Radio-Gruppe im Suchfeld:**
- "Suche" = Standard (NICHT nutzen!)
- "Forschung" = Research Mode (NICHT nutzen!)
- "Labs" = Lab Mode (DIESEN klicken!)

```python
# Finde den "Labs" Radio-Button
page = read_page(tabId=TAB_ID, filter="interactive")
# Suche nach: radio "Labs" [ref_XX]

# Klicke auf "Labs"
computer(action="left_click", ref="ref_XX", tabId=TAB_ID)
```

---

## Schritt 6: Query eingeben (KRITISCH!)

**WICHTIG: KEINE NEWLINES IN DER QUERY!**

Newline = Enter = Query wird sofort abgeschickt. Nur die erste Zeile kommt an!

```python
# 1. Textfeld klicken (NICHT form_input verwenden - ist oft DIV!)
computer(action="left_click", ref="ref_YY", tabId=TAB_ID)

# 2. Query eingeben - ALLES IN EINER ZEILE!
# Struktur durch Semikolons und nummerierte Listen, KEINE Newlines
computer(action="type", text="{optimized_query_single_line}", tabId=TAB_ID)

# 3. SCREENSHOT zur Verifizierung vor Absenden!
computer(action="screenshot", tabId=TAB_ID)
# → Prüfen ob VOLLE Query im Textfeld steht

# 4. Erst dann absenden (Klick auf Send-Button, NICHT Enter)
computer(action="left_click", coordinate=[SEND_BUTTON_X, SEND_BUTTON_Y], tabId=TAB_ID)
```

**Query-Format (Single-Line):**
```
Erstelle ein [ARTEFAKT-TYP] fuer [THEMA]. Features: (1) [Feature-A] mit [Details]; (2) [Feature-B] fuer [Zweck]; (3) [Feature-C] zeigt [Was]. Datenquellen: [Quelle-1], [Quelle-2]. Output: [Format].
```

**Siehe**: `.claude/lab-types/PROMPT-ENGINEERING.md` fuer komplette Anleitung

---

## Schritt 7: Warten auf Ergebnis (Timeout: 20 Min)

Labs-Projekte dauern länger als Research!

```python
# Polling-Loop
MAX_ITERATIONS = 120  # 120 * 10s = 20 Minuten
INTERVAL = 10  # Sekunden

for i in range(MAX_ITERATIONS):
    computer(action="wait", duration=INTERVAL, tabId=TAB_ID)

    text = get_page_text(tabId=TAB_ID)

    # Check ob Lab fertig
    # Labs zeigt "Assets" Tab wenn fertig
    if "Assets" in text and "Generating" not in text:
        break

    # Progress-Update alle 30 Sekunden
    if i % 3 == 0:
        print(f"Lab läuft... ({i * 10}s)")

# Timeout-Warnung
if i >= MAX_ITERATIONS - 1:
    print("TIMEOUT: Lab dauert länger als erwartet")
```

---

## Schritt 8: Ergebnis + Assets extrahieren

```python
# 1. Haupt-Ergebnis holen
result = get_page_text(tabId=TAB_ID)

# 2. Screenshot für Dokumentation
computer(action="screenshot", tabId=TAB_ID)

# 3. Assets-Tab klicken (falls vorhanden)
# read_page → Assets Tab ref finden → klicken
# Assets auflisten (CSV, Charts, Code-Files)
```

---

## Schritt 9: In Knowledge Base speichern

Erstelle Ordner und speichere:

```
knowledge/labs/{YYYY-MM-DD}-{topic-slug}/
├── README.md          # Projekt-Übersicht
├── result.md          # Extrahierter Lab-Output
├── assets/            # Heruntergeladene Assets (falls möglich)
│   ├── data.csv
│   └── chart-1.png
└── screenshot.png     # Browser-Screenshot
```

**README.md Struktur:**
```markdown
# Lab: {topic}

**Erstellt**: {date}
**Typ**: {lab_type}
**Dauer**: ~{duration}

## Query
{optimized_query}

## Ergebnis-Zusammenfassung
{brief_summary}

## Assets
- [data.csv](./assets/data.csv)
- [Chart 1](./assets/chart-1.png)

## Perplexity Link
{direct_link_if_available}

## Nächste Schritte
- {next_step_1}
- {next_step_2}
```

---

## Schritt 10: Bestätigung

```
✓ Lab erstellt: {topic}
  Typ: {lab_type}
  Dauer: ~{duration}

  Assets:
  - {asset_1}
  - {asset_2}

  Gespeichert in: knowledge/labs/{folder}/

Nächste Schritte:
- Assets manuell herunterladen (falls nicht automatisch)
- /knowledge-search {topic} - In KB suchen
```

---

## Fehlerbehandlung

### Chrome nicht verfügbar

```
Chrome MCP nicht erreichbar.
→ Bitte Chrome mit Claude Extension öffnen.
→ Dann erneut versuchen.
```

### Perplexity-Login erforderlich

```
Perplexity zeigt Login-Screen.
→ Bitte einloggen (Pro-Account für Labs erforderlich!)
→ Dann erneut versuchen.
```

### Labs nicht verfügbar

```
Labs-Option nicht gefunden.
→ Pro-Subscription erforderlich
→ Oder: Perplexity UI hat sich geändert - read_page für neue refs
```

### Timeout

```
Lab dauert länger als 20 Minuten.
→ Aktueller Stand wird extrahiert.
→ Perplexity-Tab bleibt offen für manuellen Check.
```

---

## Beispiele

### Report
```
/lab "Detaillierte Marktanalyse: AI-generierte Kunst auf Etsy 2026"
```

### Dashboard
```
/lab "Interaktives Dashboard für Bitcoin, Ethereum, Solana Performance"
```

### Spreadsheet
```
/lab "Vergleichstabelle: Top 10 VPN-Anbieter mit Preisen und Features"
```

### Code Prototype
```
/lab "Baue eine einfache Pomodoro-Timer Web-App"
```

---

## Related

- `/deep-research` - Für reine Recherche ohne Assets
- `/knowledge-add` - Manuell Wissen hinzufügen
- `/think` - Für Analyse der Lab-Ergebnisse
