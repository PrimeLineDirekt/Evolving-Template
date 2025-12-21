# System Builder Learnings

**Projekt**: Evolving System Builder
**Datum**: 2025-12-14
**Status**: Initial Implementation Complete

## Kontext

Implementation eines System-Generators der komplette Multi-Agent Projekte aus Blueprints erstellt.

## Key Learnings

### 1. Blueprints erweitern Scenarios - nicht ersetzen

**Learning**: Scenarios hatten bereits 70% der benötigten Struktur. Blueprints sind Scenarios + Generation Config + Knowledge Injection.

**Vorher**: Komplett neues Blueprint-System geplant
**Nachher**: Blueprints als Layer über Scenarios

**Benefit**: Weniger Code, konsistente Struktur, Wiederverwendung bestehender Templates.

### 2. 4-Agent Pipeline ist optimal

**Learning**: Die Aufteilung in Analyzer → Architect → Generator → Validator ist ideal für Separation of Concerns.

| Agent | Verantwortung | Model |
|-------|---------------|-------|
| Analyzer | WAS (Requirements) | Sonnet |
| Architect | WIE (Design) | Opus |
| Generator | ERSTELLEN (Files) | Sonnet |
| Validator | PRÜFEN (Quality) | Haiku |

**Warum funktioniert es**:
- Klare Übergaben zwischen Agents
- Jeder Agent hat einen definierten Input/Output
- Fehler sind leicht lokalisierbar
- Model-Tiers sind sinnvoll verteilt

### 3. Context Router für Knowledge Injection

**Learning**: Der bestehende Context Router (`_graph/cache/context-router.json`) ist perfekt für automatische Knowledge Injection.

```json
"system-creation": {
  "keywords": ["create system", "system erstellen"],
  "primary": ["blueprint-...", "pattern-..."],
  "secondary": ["learning-..."]
}
```

**Benefit**: Keine neue Infrastruktur nötig, nutzt bestehenden Knowledge Graph.

### 4. Schrittweise Bestätigung ist wichtig

**Learning**: Auto-Mode (`--auto`) ist für Experten, aber Default sollte schrittweise Bestätigung sein.

**User-Feedback-Punkte**:
1. Nach Blueprint-Auswahl
2. Nach Architektur-Preview
3. Nach Generation (vor Validation)

**Warum**: User hat Kontrolle, kann Customization vornehmen, versteht was passiert.

### 5. Standalone Systems sind kritisch

**Learning**: Generierte Systeme dürfen KEINE Runtime-Dependency zu Evolving haben.

**Implementiert**:
- Eigene CLAUDE.md (vollständiger Kontext)
- Kopierte Patterns (nicht referenziert)
- Eigene Memory-Struktur
- Eigene Commands

**Warum**: User kann System in eigenem Ordner nutzen ohne Evolving zu kennen.

### 6. Template Placeholders brauchen Validation

**Learning**: Vergessene Placeholders (`{PLACEHOLDER}`) sind schwer zu finden.

**Lösung**: Validator prüft auf verbleibende `{...}` Patterns:

```python
def check_placeholders(content):
    import re
    placeholders = re.findall(r'\{[A-Z_]+\}', content)
    return placeholders  # Should be empty
```

### 7. Blueprint Detection Keywords

**Learning**: Keywords müssen DE + EN sein und Anti-Patterns definieren.

**Gut**:
```
"system erstellen", "create system", "multi-agent"
```

**Anti-Patterns (nicht triggern)**:
```
"system funktioniert" (Status, nicht Creation)
"welches system" (Frage, nicht Creation)
```

## Architektur-Entscheidungen

### Decision 1: Extern vs. Intern generieren

**Entscheidung**: Extern (eigener Ordner)
**Alternativen**: Intern (.claude/scenarios/), Beides
**Begründung**: User will eigenständige Projekte, nicht mehr Komplexität in Evolving

### Decision 2: 1 Blueprint zum Start

**Entscheidung**: Nur multi-agent-advisory initial
**Alternativen**: 3 Blueprints, Generischer Generator
**Begründung**: Schnell iterieren, Learnings sammeln, dann erweitern

### Decision 3: Task-Tool für Agent-Orchestration

**Entscheidung**: Echte Task-Agents via Task-Tool
**Alternativen**: Pseudo-Agents (sequenzielle Steps)
**Begründung**: Parallelisierung möglich, saubere Trennung, nutzt Claude's Stärken

## Metriken

| Metrik | Wert |
|--------|------|
| Neue Dateien | 14 |
| Modifizierte Dateien | 6 |
| Agents erstellt | 4 |
| Commands erstellt | 1 |
| Templates erstellt | 4 |
| Blueprints erstellt | 1 |
| Patterns dokumentiert | 1 |
| Test-Run | Erfolgreich (12 Files generiert) |

## Offene Punkte / Backlog

1. **Weitere Blueprints**: autonomous-research, simple-workflow
2. **Resume-Funktion**: Bei Abbruch weitermachen (`--resume`)
3. **Dry-Run verbessern**: Detailliertere Preview
4. **Knowledge Trimming**: Patterns auf essentielle Teile reduzieren
5. **Testing**: Automatische Tests für generierte Systeme

## Wiederverwendbarkeit

Dieses Pattern kann angewendet werden für:
- Andere Meta-Generatoren (Prompt-Generator, Agent-Generator)
- Template-basierte Scaffolding-Systeme
- Knowledge-injizierte Projekt-Setups

## Related

- `knowledge/patterns/system-generation-pattern.md` - Pattern-Dokumentation
- `.claude/blueprints/` - Blueprint-Definitionen
- `.claude/commands/create-system.md` - Command-Dokumentation
