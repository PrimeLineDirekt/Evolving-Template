# CopilotKit Evaluation

**Datum**: 2025-12-12
**Status**: Evaluiert, nicht implementiert
**Typ**: Framework Evaluation

---

## Was ist CopilotKit?

**GitHub**: https://github.com/CopilotKit/CopilotKit
**Docs**: https://docs.copilotkit.ai
**Stars**: 25k+ (Stand: Dez 2025)
**Lizenz**: MIT

React UI Framework für AI Copilots, Chatbots und In-App AI Agents.

## Tech Stack

- **Frontend**: React, Next.js
- **Backend**: LangGraph (JS + Python), CrewAI
- **Protocol**: AG-UI (Agent-User Interaction Standard)
- **LLM**: OpenAI, Anthropic, etc.

## Key Features

### 1. UI Components
```typescript
// Pre-built Chat UI
<CopilotPopup />
<CopilotSidebar />
<CopilotChat />

// Headless API
const { visibleMessages, appendMessage } = useCopilotChat();
```

### 2. Frontend Actions
```typescript
// Agent kann Frontend-Aktionen auslösen
useCopilotAction({
  name: "openPanel",
  description: "Opens a specific panel in the dashboard",
  parameters: [{ name: "panelId", type: "string" }],
  handler: ({ panelId }) => {
    // Agent kann UI direkt manipulieren
    openPanel(panelId);
  },
});
```

### 3. CoAgents (LangGraph Integration)
```typescript
// Shared State zwischen App und Agent
const { state, setState } = useCoAgent({
  name: "research-agent",
  initialState: { query: "", results: [] },
});
```

### 4. Human-in-the-Loop
```typescript
// Agent pausiert für User-Approval
useCopilotAction({
  name: "sendEmail",
  renderAndWaitForResponse: ({ args }) => (
    <ApprovalDialog
      title="Email senden?"
      content={args.draft}
    />
  ),
});
```

### 5. Generative UI
- Agent kann React Components dynamisch rendern
- Streaming UI Updates während Agent arbeitet
- State Updates in Echtzeit

## Architektur

```
┌─────────────────┐     ┌──────────────────┐
│  React Frontend │────▶│  CopilotKit      │
│  (useCopilot*)  │     │  Runtime         │
└─────────────────┘     └────────┬─────────┘
                                 │
                        ┌────────▼─────────┐
                        │  LangGraph       │
                        │  (Python/JS)     │
                        └──────────────────┘
```

## Evaluation für Projekte

### Server-Side Rendered Project (Example)

| Aspekt | Bewertung |
|--------|-----------|
| **Tech Stack Match** | ❌ Kein React (SSR Framework) |
| **Umbau-Aufwand** | Hoch (Frontend komplett neu) |
| **Empfehlung** | **Nicht geeignet** |

**Grund**: CopilotKit ist ein React Framework. Server-side rendering projects würden kompletten Frontend-Umbau erfordern.

### React-based Project (Example)

| Aspekt | Bewertung |
|--------|-----------|
| **Tech Stack Match** | ✅ Next.js + React |
| **Bestehendes System** | Chat bereits implementiert |
| **Mehrwert** | Frontend Actions, Generative UI |
| **Aufwand** | ~1-2 Tage Umbau |
| **Empfehlung** | **Nice-to-have, nicht kritisch** |

**Grund**: Das bestehende Chat-System (`useChat` Hook, 420 Zeilen) funktioniert bereits gut mit WebSocket Streaming, Tool Calls, Cancel, und Persistence. CopilotKit würde marginalen Mehrwert bringen.

## Wann CopilotKit Sinn macht

1. **Greenfield React Projekt** mit Chat/Copilot als Kernfeature
2. **Frontend Actions** nötig (Agent steuert UI-Elemente)
3. **LangGraph Backend** bereits vorhanden
4. **Generative UI** für komplexe Workflows gewünscht
5. **HITL embedded** in Chat-Flow

## Wann CopilotKit NICHT Sinn macht

1. **Kein React** (Server-Side Rendering, Vue, Svelte, etc.)
2. **Chat bereits implementiert** und funktioniert
3. **Lokales Tool** ohne öffentliche User
4. **Einfache Chat-Anforderungen** (kein Frontend Actions nötig)

## Code-Snippets für spätere Referenz

### Installation
```bash
npx copilotkit@latest init
```

### Basic Setup
```typescript
// app/layout.tsx
import { CopilotKit } from "@copilotkit/react-core";

export default function Layout({ children }) {
  return (
    <CopilotKit runtimeUrl="/api/copilotkit">
      {children}
    </CopilotKit>
  );
}
```

### LangGraph Python Integration
```python
# Backend: CopilotKit mit LangGraph verbinden
from copilotkit.integrations.langgraph import copilotkit_customize_config

config = copilotkit_customize_config(
    config,
    emit_intermediate_state=[{
        "state_key": "research_results",
        "tool": "search",
    }]
)
```

### Frontend Action
```typescript
useCopilotAction({
  name: "executeCommand",
  description: "Execute a slash command",
  parameters: [
    { name: "command", type: "string", required: true }
  ],
  handler: async ({ command }) => {
    await executeSlashCommand(command);
    return `Executed: ${command}`;
  },
});
```

## Fazit

CopilotKit ist ein solides Framework für React-basierte AI Copilots. Evaluate against your specific tech stack and requirements.

**Best for**: Greenfield React-Projekte mit Chat-First UX.

---

**Related**:
- Scenario-specific rules (@.claude/rules/scenarios/)
