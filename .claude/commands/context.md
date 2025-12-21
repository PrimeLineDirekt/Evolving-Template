# /context

Lade relevanten Kontext aus dem Knowledge Graph basierend auf Keywords.

## Trigger-Patterns
- "Lade Kontext für {topic}"
- "Zeige relevante Entities für {topic}"
- "Was ist relevant für {topic}?"
- "/context {keywords}"

## Model: haiku

## Workflow

### 1. Keywords extrahieren
```
User Input: "Kontext für Agent-Erstellung"
Keywords: ["agent", "creation", "erstellen"]
```

### 2. Context Router abfragen
Lies `_graph/cache/context-router.json` und finde passende Route.

### 3. Primary Nodes laden
Immer laden - das sind die wichtigsten Entities.

### 4. Secondary Nodes (optional)
Bei Bedarf zusätzlich laden für tieferen Kontext.

### 5. Context Files laden
Falls definiert, auch Memory/Index Dateien einbeziehen.

## Output Format

```markdown
## Relevanter Kontext für: {topic}

### Primary Entities (immer relevant)
- **{node-name}** ({type}) - {description}
  Path: {path}

### Secondary Entities (zusätzlich hilfreich)
- **{node-name}** ({type}) - {description}

### Aktiver Memory-Kontext
Aus: {context_file}
- {key info from memory}

### Verbundene Entities (via Graph)
- {related nodes from edges.json}
```

## Beispiel

**Input**: `/context agent-creation`

**Output**:
```
## Relevanter Kontext für: Agent-Erstellung

### Primary Entities
- **Specialist Agent Template** (template) - Template für specialist agents
  Path: .claude/templates/agents/specialist-agent.md

- **Research Agent Template** (template) - Template für research agents
  Path: .claude/templates/agents/research-agent.md

- **Template Creator** (skill) - Template creation für Agents, Commands, etc.
  Path: .claude/skills/template-creator/

### Secondary Entities
- **Progressive Disclosure Pattern** (pattern) - reference.md + examples.md
- **Intake Gate Pattern** (pattern) - Input validation vor Ausführung
- **12-Factor Agents** (learning) - 12 Prinzipien für Agent Design

### Aktiver Memory-Kontext
Aus: _memory/projects/evolving-system.json
- Aktueller Focus: Domain Memory Implementation
- Features: 8 (6 passing, 1 planned)
```

## Implementierung

1. Lese `_graph/cache/context-router.json`
2. Matche Keywords gegen alle Routes
3. Sammle Primary + Secondary Nodes
4. Lese `_graph/nodes.json` für Node Details
5. Optional: Lese Edges für Verbindungen
6. Formatiere und präsentiere

## Hinweis

Dieser Command nutzt den Knowledge Graph für schnelle Kontextbereitstellung.
Der Graph wird initial generiert und bei Bedarf aktualisiert.
