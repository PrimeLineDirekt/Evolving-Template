# Learning: Better Agents Patterns

**Quelle**: https://github.com/langwatch/better-agents
**Analysiert**: 2025-12-01
**Relevanz für Evolving**: 7/10

---

## Übersicht

Better Agents ist ein CLI-Tool für produktionsreife Agent-Projekte. Die wichtigsten Patterns und was wir daraus lernen können.

---

## Pattern 1: AGENTS.md Development Guidelines

### Was es ist
Eine zentrale Markdown-Datei im Root des Projekts die:
- Entwicklungsrichtlinien für AI Agents definiert
- Best Practices dokumentiert
- Architektur-Entscheidungen erklärt
- Als Kontext für Coding Assistants dient

### Unser Equivalent
`.claude/CONTEXT.md` - erfüllt denselben Zweck

### Learning
Das Pattern ist validiert - wir machen es bereits richtig.

---

## Pattern 2: Agent Testing Pyramid

### Was es ist
Strukturiertes Testing für AI Agents mit zwei Ebenen:

1. **Scenario Tests** (`tests/scenarios/`)
   - End-to-End Tests für Agent-Verhalten
   - Simulieren echte Konversationen
   - Format: Python/TypeScript Test-Dateien

2. **Evaluation Notebooks** (`tests/evaluations/`)
   - Jupyter Notebooks für Performance-Messung
   - Metriken und Analysen
   - Nutzung von LangWatch API

### Relevanz für Evolving
**Hoch** - Wir haben aktuell keine Tests für unsere Agents.

### Mögliche Integration
```
.claude/tests/
├── scenarios/
│   ├── idea-validator-scenario.md
│   └── research-analyst-scenario.md
└── evaluations/
    └── agent-performance.md
```

---

## Pattern 3: Prompt Versioning (YAML)

### Was es ist
YAML-basiertes Prompt-Format mit:
```yaml
model: gpt-4o
temperature: 0.7
messages:
  - role: system
    content: "You are a helpful AI assistant."
```

Plus `prompts.json` als zentrales Registry.

### Bewertung
| Aspekt | YAML | Markdown (unser) |
|--------|------|------------------|
| LLM-Verständnis | Muss geparst werden | Nativ verstanden |
| Struktur | Streng | Flexibel |
| API-Integration | Besser | Schlechter |
| Team-Collab | Versionierung | Reviews |

### Entscheidung
**Bleiben bei Markdown** - besser für LLM-Prompts.
Registry-Idee übernehmen: `knowledge/prompts/index.json`

---

## Pattern 4: MCP Integration

### Was es ist
`.mcp.json` im Projekt-Root für:
- Framework-Expertise (Agno, Mastra)
- Tool-Integrationen
- Shared Team-Konfigurationen

### Integration in Evolving
Erstellt: `.mcp.json` mit:
- GitHub Server (Repository-Zugriff)
- Sequential Thinking (strukturiertes Problemlösen)
- Context7 (aktuelle Dokumentation)

---

## Pattern 5: Project Scaffolding

### Was es ist
CLI-basierte Projektgenerierung:
```bash
npx @langwatch/better-agents init my-agent
```

Generiert standardisierte Struktur mit Templates.

### Unser Equivalent
`/create-agent`, `/create-command`, etc. Commands
Plus Templates in `.claude/templates/`

### Learning
Wir haben ein gleichwertiges System, aber interaktiver.

---

## Pattern 6: Observability

### Was es ist
Integriertes Monitoring via LangWatch:
- Agent-Verhalten tracken
- Performance messen
- Fehler identifizieren

### Relevanz für Evolving
**Mittel** - Interessant für Produktion, aber benötigt externe Services.

### Status
Backlog - evaluieren wenn Agent-Nutzung steigt.

---

## Zusammenfassung: Was wir übernommen haben

| Pattern | Status | Datei/Location |
|---------|--------|----------------|
| AGENTS.md | Bereits vorhanden | .claude/CONTEXT.md |
| MCP Config | Erstellt | .mcp.json |
| Scenario Testing | Pending | .claude/tests/scenarios/ |
| Prompt Registry | Pending | knowledge/prompts/index.json |
| YAML Prompts | Abgelehnt | Bleiben bei Markdown |
| Observability | Backlog | Später evaluieren |

---

## Quellen

- [Better Agents GitHub](https://github.com/langwatch/better-agents)
- [Top 10 MCP Servers 2025](https://apidog.com/blog/top-10-mcp-servers-for-claude-code/)
- [Claude Code MCP Docs](https://docs.anthropic.com/en/docs/claude-code/mcp)

---

**Erstellt durch**: github-repo-analyzer-agent
**Integration**: SYSTEM-MAP.md Changelog
