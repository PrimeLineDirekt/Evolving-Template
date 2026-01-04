# Perplexity Labs Prompt Engineering

## KRITISCHE REGELN

### 1. KEINE NEWLINES IN QUERIES!

**Problem**: Newline = Enter = Query wird sofort abgeschickt. Nur die erste Zeile kommt an.

**Loesung**: Alles in EINER Zeile. Struktur durch Semikolons und nummerierte Listen.

```
FALSCH (wird nach erster Zeile abgeschickt):
"Erstelle ein Dashboard.
Features:
- Chart 1
- Chart 2"

RICHTIG (komplette Query):
"Erstelle ein INTERAKTIVES DASHBOARD fuer X. Features: (1) Chart-Typ A mit Dimensionen X, Y, Z; (2) Chart-Typ B fuer Vergleich; (3) Tabelle mit Spalten A, B, C. Datenquellen: Benchmarks 2026, GitHub Stars."
```

### 2. KONKRETES ARTEFAKT BENENNEN

Labs baut was du sagst, nicht was du meinst.

| Vage (SCHLECHT) | Konkret (GUT) |
|-----------------|---------------|
| "Erstelle einen Report" | "Erstelle ein INTERAKTIVES VERGLEICHS-DASHBOARD" |
| "Analysiere X" | "Erstelle eine SPREADSHEET mit Feature-Matrix" |
| "Zeig mir Y" | "Baue eine WEB-APP mit Dropdown und Charts" |

### 3. FEATURES NUMMERIEREN UND DETAILLIEREN

Nicht: "mit verschiedenen Charts"
Sondern: "(1) Radar-Chart mit 5 Dimensionen (Performance, Cost, Ease-of-Use, Community, Enterprise-Support); (2) Scatter-Plot zeigt X vs Y; (3) Bar-Chart fuer Ranking"

### 4. DATENQUELLEN EXPLIZIT ANGEBEN

Labs recherchiert basierend auf deinen Angaben. Sei spezifisch:
- "Datenquellen: Offizielle Dokumentation, GitHub Stars Stand Januar 2026, Benchmark-Papers"
- "Basierend auf: aktuellen Preislisten, Hersteller-Websites, unabhaengige Reviews"

### 5. OUTPUT-FORMAT SPEZIFIZIEREN

- "Als interaktives HTML-Dashboard mit funktionierendem JavaScript"
- "Mit herunterladbarem CSV der Rohdaten"
- "Inklusive produktionsreifer Code-Snippets mit Fehlerbehandlung"

---

## PROMPT-TEMPLATE STRUKTUR

```
[ARTEFAKT-TYP] fuer [THEMA].

Features: (1) [Feature-A] mit [Details]; (2) [Feature-B] fuer [Zweck]; (3) [Feature-C] mit [Spezifikation]; (4) [Feature-D] zeigt [Was].

Datenquellen: [Quelle-1], [Quelle-2], [Quelle-3].

Output: [Format-Spezifikation].
```

---

## BEISPIEL: Schwacher vs Starker Prompt

### SCHWACH (Ergebnis: generischer Text-Report)

```
Erstelle einen Report ueber AI Agent Frameworks
```

### STARK (Ergebnis: vollstaendiges interaktives Dashboard)

```
Erstelle ein INTERAKTIVES VERGLEICHS-DASHBOARD fuer AI-Agent Frameworks 2026. Features: (1) Dropdown zum Framework-Auswaehlen (LangGraph, CrewAI, AutoGen, OpenAI Swarm, Semantic Kernel); (2) Radar-Chart mit Vergleich auf 5 Dimensionen (Performance, Ease-of-Use, Cost, Claude-Support, Community); (3) Tabelle als Feature-Matrix mit Checkmarks (State Management, Parallel Execution, Memory, Tool Use); (4) Code-Snippet-Box mit Hello-World Multi-Agent Beispiel pro Framework inklusive Anthropic/Claude Integration. Datenquellen: Aktuelle Benchmarks 2026, GitHub Stars, offizielle Dokumentation. Output: Funktionierendes HTML-Dashboard mit interaktiven Elementen.
```

---

## KOMPLEXITAETS-LEVELS

### Level 1: Basic (Funktioniert, aber minimal)
- Ein Artefakt-Typ genannt
- Keine Feature-Details
- Keine Datenquellen

### Level 2: Standard (Gute Ergebnisse)
- Artefakt-Typ + 2-3 Features
- Einige Details
- Datenquellen erwaehnt

### Level 3: Advanced (Optimale Ergebnisse)
- Spezifischer Artefakt-Typ
- 4+ nummerierte Features mit Details
- Jedes Feature hat Spezifikation
- Explizite Datenquellen
- Output-Format definiert

### Level 4: Expert (Maximale Kontrolle)
- Alles von Level 3
- Interaktionsmuster beschrieben
- Fallback-Verhalten definiert
- Spezifische Technologien genannt
- Edge-Cases adressiert

---

## QUALITY CHECKLIST VOR ABSENDEN

- [ ] Keine Newlines in der Query?
- [ ] Konkreter Artefakt-Typ genannt?
- [ ] Features nummeriert (1), (2), (3)?
- [ ] Jedes Feature hat Details?
- [ ] Datenquellen angegeben?
- [ ] Output-Format spezifiziert?
- [ ] Fuer User verstaendlich wenn er Ergebnis sieht?

---

## HAEUFIGE FEHLER

| Fehler | Konsequenz | Loesung |
|--------|------------|---------|
| Newlines in Query | Nur erste Zeile wird gesendet | Semikolons statt Umbrueche |
| Vages "Dashboard erstellen" | Labs raet was gemeint ist | Konkret: "Radar-Chart mit X, Y, Z" |
| Keine Datenquellen | Zufaellige Quellen genutzt | Explizit: "Basierend auf GitHub, Docs" |
| "Charts hinzufuegen" | Generische Charts | "Bar-Chart fuer Ranking nach Metrik X" |
| Zu kurze Query | Minimales Ergebnis | Mehr Details = besseres Ergebnis |

---

## META: Warum komplexe Prompts?

Labs ist ein **Builder**, kein Researcher. Es konstruiert Artefakte basierend auf Anweisungen.

Je praeziser die Anweisungen:
- Desto weniger "Raten" durch Labs
- Desto naeher am gewuenschten Ergebnis
- Desto weniger Iterations noetig

Ein 200-Wort-Prompt der alles spezifiziert spart 3 Iterationen mit vagen 20-Wort-Prompts.
