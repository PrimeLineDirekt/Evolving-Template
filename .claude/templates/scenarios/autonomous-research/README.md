# Autonomous Research Scenario Template

Dieses Template erstellt ein **Task Decomposition Pipeline** Szenario für systematische, autonome Recherche und Beratung.

## Wann nutzen?

- Beratungs-intensive Domains (Steuern, Finanzen, Legal, etc.)
- Komplexe Fragen die mehrere Aspekte haben
- Wenn konkrete Daten und Empfehlungen gebraucht werden
- Multi-Faktoren-Vergleiche und Entscheidungen

## Was ist enthalten?

```
autonomous-research/
├── scenario.json          # Szenario-Konfiguration
├── agents/
│   ├── planner-agent.md   # Zerlegt Queries in Tasks
│   ├── executor-agent.md  # Führt Tasks aus, sammelt Daten
│   └── synthesizer-agent.md # Erstellt finale Antwort
└── prompts/
    ├── planning.md        # System-Prompt für Planner
    ├── execution.md       # System-Prompt für Executor
    └── synthesis.md       # System-Prompt für Synthesizer
```

## Verwendung

### 1. Template kopieren

```bash
cp -r .claude/templates/scenarios/autonomous-research .claude/scenarios/{DEIN-SZENARIO-NAME}
```

### 2. Placeholders ersetzen

Ersetze in allen Dateien:
- `{DOMAIN}` → Deine Domain (z.B. "tax-advisory", "market-research")
- `{DOMAIN_DESCRIPTION}` → Beschreibung der Domain
- `{TOOLS}` → Verfügbare Tools für diese Domain
- `{KNOWLEDGE_SOURCES}` → Relevante Knowledge Base Pfade
- `{OUTPUT_FORMAT}` → Gewünschtes Ausgabeformat

### 3. Domain-spezifische Tools definieren

In `scenario.json` unter `tools` die verfügbaren Tools für deine Domain eintragen.

### 4. Aktivieren

```
/scenario {DEIN-SZENARIO-NAME}
```

## Beispiel-Adaptionen

| Domain | Szenario-Name | Typische Queries |
|--------|---------------|------------------|
| Steuerberatung | `tax-advisory` | "Vergleiche Steuern in X vs Y" |
| Marktforschung | `market-research` | "Analysiere Markt für Produkt X" |
| Due Diligence | `due-diligence` | "Bewerte Unternehmen X" |
| Content Research | `content-research` | "Recherchiere Thema X für Artikel" |

## Best Practices

1. **Tools spezifisch definieren** - Je präziser die Tools, desto besser die Ergebnisse
2. **Knowledge Sources verlinken** - Executor braucht Zugang zu relevanten Daten
3. **Output Format festlegen** - Synthesizer sollte wissen wie die Antwort aussehen soll
4. **Komplexitäts-Trigger** - Nur für komplexe Queries nutzen, nicht für Faktenfragen

## Referenz

Siehe `knowledge/patterns/task-decomposition-pipeline.md` für das zugrundeliegende Pattern.
