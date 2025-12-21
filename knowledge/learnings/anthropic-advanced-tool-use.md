# Anthropic Advanced Tool Use - Learnings

**Quelle:** [Anthropic Engineering Blog - Advanced Tool Use](https://www.anthropic.com/engineering/advanced-tool-use)
**Datum:** November 2024
**Confidence:** 95% (Offizielles Anthropic Engineering)

---

## Kontext

Beim Railway-Deployment eines Multi-Agent Systems entdeckt, dass der KB-Indexer 6178 serielle API-Calls machte statt Batch-Operationen. Bei der Recherche nach Optimierungen auf den Anthropic Advanced Tool Use Artikel gestoßen.

**Auslöser:** Build-Timeout durch 6178 serielle Embedding-API-Calls

---

## Die drei Beta-Features

### 1. Tool Search Tool
**Problem:** Bei vielen Tools werden alle Definitionen vorab geladen → hoher Token-Verbrauch

**Lösung:** Tools on-demand entdecken
- Agent fragt: "Welche Tools brauche ich für X?"
- System liefert nur relevante Tools

**Impact:** 85% Token-Reduktion bei großen Tool-Bibliotheken

**Wann nutzen:**
- Mehr als 10-15 Tools verfügbar
- Nicht alle Tools für jede Aufgabe relevant
- Token-Kosten ein Faktor

---

### 2. Programmatic Tool Calling
**Problem:** Einzelne sequentielle API-Calls sind langsam und token-intensiv

**Lösung:** Tools durch Code orchestrieren
```python
# Statt vieler einzelner Tool-Calls:
results = await asyncio.gather(*[
    call_tool(tool_id, params)
    for tool_id in needed_tools
])
```

**Impact:** 37% Token-Reduktion bei komplexen Aufgaben

**Wann nutzen:**
- Mehrere ähnliche Operationen
- Abhängigkeiten zwischen Tools
- Komplexe Workflows

---

### 3. Tool Use Examples
**Problem:** Schema-Definitionen allein → 72% Genauigkeit

**Lösung:** Konkrete Beispiele in Tool-Beschreibungen
```json
{
  "name": "analyze_profile",
  "examples": [
    {
      "input": {"income": 150000, "target": "CH"},
      "output": {"recommendation": "Pauschalbesteuerung", "confidence": 0.85}
    }
  ]
}
```

**Impact:** Genauigkeit von 72% → 90%

**Wann nutzen:**
- Ambige Tool-Parameter
- Komplexe Input/Output-Strukturen
- Kritische Operationen

---

## Erkenntnisse

### Haupterkenntnis
**Batch > Seriell, immer.** Der KB-Indexer hat bewiesen: 6178 serielle Calls = Timeout. Die gleiche Operation als Batch wäre in Sekunden fertig gewesen.

### Strategische Schichtung
Nicht alle Features gleichzeitig einsetzen. Mit dem größten Engpass beginnen:
1. **Kontext-Überfluss?** → Tool Search Tool
2. **Viele intermediate results?** → Programmatic Tool Calling
3. **Parameter-Fehler?** → Tool Use Examples

### Pre-computed > Runtime
Für statische Daten (KB-Embeddings, Configs) besser lokal generieren und committen als zur Runtime berechnen.

---

## Anwendung

### Für Multi-Agent Systeme
| Feature | Anwendung | Priorität |
|---------|-----------|-----------|
| Tool Use Examples | Agent-Prompts mit I/O-Beispielen | Hoch |
| Programmatic Calling | Orchestrator erweitern | Mittel |
| Tool Search | Dynamische Agent-Auswahl | Niedrig |

### Für Evolving
| Feature | Anwendung | Priorität |
|---------|-----------|-----------|
| Tool Search | Bei 8+ Agents relevant | Mittel |
| Tool Use Examples | Skill-Definitionen | Hoch |
| Programmatic Calling | Multi-Agent Orchestration | Hoch |

### Für zukünftige Projekte
- **API-Calls zählen** vor Deployment
- **Batch-Endpoints** bevorzugen (oft 50% günstiger)
- **Caching** für wiederholte Operationen
- **Pre-indexing** für statische Daten

---

## Verwandte Learnings

- Project-specific learnings (add your own)

---

## Offene Fragen

- [ ] Wann werden diese Features GA (General Availability)?
- [ ] Gibt es Python SDK Support für Tool Search?
- [ ] Wie kombiniert man alle drei Features optimal?

---

**Navigation:** [← Learnings Index](README.md) | [Knowledge Base](../index.md)
