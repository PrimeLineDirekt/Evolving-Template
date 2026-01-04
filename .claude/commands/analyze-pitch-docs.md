# Analyze Pitch Docs

**Model**: sonnet
**Description**: Verarbeite Pitch-System Dokumente aus der Inbox

---

## Workflow

Du orchestrierst die Analyse von Windenergie Pitch-System Dokumenten mit drei spezialisierten Agents.

**WICHTIG**: Alle Agents arbeiten dokumentbasiert - keine Vorannahmen über Inhalte. Fachliche Korrektheit hat oberste Priorität.

---

## Schritte

### 1. Inbox scannen

Prüfe `_inbox/` nach neuen Dateien:
- PDF, DOCX, PPTX, MD, TXT
- Ignoriere bereits verarbeitete Dateien (check `knowledge/external-projects/schulung-pitch/raw/`)

**Output**:
```
Gefundene Dateien:
1. {dateiname} ({typ}, {größe})
2. ...
```

### 2. Für jede Datei: Document Analyzer

Nutze `pitch-document-analyzer-agent` für technische Analyse:
- Dokumenttyp bestimmen
- Metadaten extrahieren
- Themen-Hierarchie erstellen
- Fachbegriffe erfassen (nur aus Dokument!)
- Technische Spezifikationen
- Hersteller/System-Referenzen

**Speichere Analyse in**:
`knowledge/external-projects/schulung-pitch/raw/{dateiname}-analysis.md`

### 3. Content Categorizer

Nutze `pitch-content-categorizer-agent`:
- Primäre Kategorie bestimmen
- Unterkategorie verfeinern
- Tags generieren
- Glossar-Einträge extrahieren
- Wiederverwendbare Snippets identifizieren

**Erstelle kategorisierte Datei in**:
`knowledge/external-projects/schulung-pitch/{kategorie}/{unterkategorie}/{dateiname}.md`

### 4. Bei PPTX: Style Extractor

Nutze `pitch-style-extractor-agent` zusätzlich:
- Slide-Typen identifizieren
- Struktur-Patterns erkennen
- Formulierungsmuster extrahieren
- Stil-Profil erstellen

**Speichere Stil-Profil in**:
`knowledge/external-projects/schulung-pitch/style/{dateiname}-style.json`

### 5. Index aktualisieren

Update `knowledge/external-projects/schulung-pitch/index.json`:
- Neues Dokument hinzufügen
- Stats aktualisieren
- Neue Hersteller/Systeme tracken

### 6. Glossar erweitern

Update `knowledge/external-projects/schulung-pitch/glossary/terms.json`:
- Neue Begriffe hinzufügen
- Duplikate prüfen
- Bei Widersprüchen: beide Definitionen dokumentieren mit Quelle

---

## Agent-Orchestrierung

```
                        ┌─────────────────────┐
                        │   _inbox/ scannen   │
                        └──────────┬──────────┘
                                   │
                    ┌──────────────▼──────────────┐
                    │  pitch-document-analyzer    │
                    │  (für jede Datei)           │
                    └──────────────┬──────────────┘
                                   │
              ┌────────────────────┴────────────────────┐
              │                                         │
    ┌─────────▼─────────┐                    ┌─────────▼─────────┐
    │  pitch-content-   │                    │  pitch-style-     │
    │  categorizer      │                    │  extractor        │
    │  (immer)          │                    │  (nur bei PPTX)   │
    └─────────┬─────────┘                    └─────────┬─────────┘
              │                                         │
              └────────────────────┬────────────────────┘
                                   │
                    ┌──────────────▼──────────────┐
                    │  Index & Glossar updaten    │
                    └──────────────┬──────────────┘
                                   │
                    ┌──────────────▼──────────────┐
                    │  Zusammenfassung ausgeben   │
                    └─────────────────────────────┘
```

---

## Output Format

```markdown
# Pitch-Dokument Analyse abgeschlossen

**Verarbeitet**: {Datum}
**Dateien**: {N}

---

## Verarbeitete Dokumente

### 1. {Dateiname}
- **Typ**: {dokumenttyp}
- **Hersteller**: {hersteller oder "Nicht spezifiziert"}
- **System**: {system oder "Allgemein"}
- **Kategorisiert als**: `{pfad}`
- **Neue Glossar-Einträge**: {N}
- **Stil-Profil**: {Ja/Nein}

### 2. {Dateiname}
...

---

## Neue KB-Einträge

| Datei | Kategorie | Pfad |
|-------|-----------|------|
| ... | ... | ... |

---

## Glossar-Updates

{N} neue Begriffe hinzugefügt:
- {Begriff 1} ({Kategorie})
- {Begriff 2} ({Kategorie})
...

---

## Nächste Schritte

- [ ] Original-Dateien aus `_inbox/` löschen?
- [ ] Querverweise zu existierenden Dokumenten prüfen
- [ ] Stil-Profile für neue Präsentationen nutzen
```

---

## Error Handling

**Datei nicht lesbar:**
- Überspringen, Warnung ausgeben
- In Zusammenfassung als "Fehler" markieren

**Unklare Kategorisierung:**
- Als `systems/general/` einordnen
- Tag "needs-review" hinzufügen
- In Zusammenfassung hervorheben

**Widersprüchliche Fachbegriffe:**
- Beide Definitionen in Glossar aufnehmen
- Mit Quellenangabe versehen
- Als "widersprüchlich" markieren

---

## Qualitätssicherung

Nach Abschluss:
1. Prüfe ob alle Dateien verarbeitet wurden
2. Prüfe ob Index konsistent ist
3. Prüfe ob Glossar keine Duplikate enthält
4. Zeige Warnungen für "needs-review" Items

---

## Plain Text Trigger

**Confidence 9-10:**
- "Analysiere die Pitch-Dokumente"
- "Verarbeite die Pitch-System Dateien"
- "Neue Schulungsunterlagen analysieren"

**Confidence 7-8:**
- "Was ist in der Inbox?" (wenn Pitch-Dateien erkannt)
- "Schau dir die neuen Dateien an"
