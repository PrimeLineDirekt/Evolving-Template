# Dashboard Engineer Agent

**Rolle**: Dashboard & UI Developer
**Fokus**: React Components, API Integration, WebSocket

---

## Tech Stack

- **Next.js 15** (App Router)
- **React 18** (Server + Client Components)
- **TypeScript**
- **Tailwind CSS** (Tokyo Night Theme)
- **SWR** - Data Fetching
- **xterm.js** - Terminal (bereits im Dashboard)

---

## Projekt-Kontext

```
dashboard/
├── src/
│   ├── app/
│   │   └── api/
│   │       └── workflows/           # NEU: API Routes
│   │           ├── route.ts         # GET /api/workflows
│   │           └── [name]/
│   │               ├── route.ts     # GET/POST /api/workflows/:name
│   │               └── runs/
│   │                   └── [runId]/
│   │                       └── route.ts
│   ├── components/
│   │   └── WorkflowPanel/           # NEU: UI Components
│   │       ├── WorkflowList.tsx
│   │       ├── WorkflowCard.tsx
│   │       ├── WorkflowRunner.tsx
│   │       ├── WorkflowLogs.tsx
│   │       └── index.ts
│   ├── hooks/
│   │   └── useWorkflows.ts          # NEU: Data Hook
│   └── types/
│       └── workflow.ts              # NEU: TypeScript Types
```

---

## Bestehende Dashboard-Patterns

### Theme (Tokyo Night)
```typescript
// Bestehende Farbpalette nutzen:
const colors = {
  bg: '#1a1b26',
  fg: '#a9b1d6',
  accent: '#7aa2f7',
  error: '#f7768e',
  success: '#9ece6a',
  warning: '#e0af68'
};
```

### API Route Pattern
```typescript
// Bestehend: dashboard/src/app/api/evolving/
// Workflow-API folgt gleichem Pattern
export async function GET(request: NextRequest) {
  const data = await fetchWorkflows();
  return NextResponse.json(data);
}
```

### Component Pattern (Client Components)
```typescript
'use client';

import { useState, useEffect } from 'react';
import { useWorkflows } from '@/hooks/useWorkflows';

export function WorkflowList() {
  const { workflows, isLoading, error } = useWorkflows();
  // ...
}
```

---

## UI Spezifikation

### Activity Bar Tab
```
[📁 Files]
[❓ Guide]
[⚙️ Workflows] ← NEU
[🍅 Pomodoro]
```

### Sidebar View
```
┌─────────────────────────────────┐
│ ⚙️ Workflows           [+ New]  │
├─────────────────────────────────┤
│ ● morning-briefing    [▶]      │
│   Cron: 8:00 täglich           │
│   Last: heute 08:00 ✓          │
│                                 │
│ ○ idea-forge-full     [▶]      │
│   Manual                        │
│   Last: gestern 14:30          │
│                                 │
│ ● weekly-review       [▶]      │
│   Cron: Mo 9:00                │
│   Next: Montag 09:00           │
└─────────────────────────────────┘
```

### Live Execution View
```
┌─────────────────────────────────────────────┐
│ ▶ idea-forge-full               [Stop] [×]  │
├─────────────────────────────────────────────┤
│ Progress: ████████░░░░░░░░ 50%              │
│                                             │
│ ✓ Step 1: Erfasse Idee                     │
│ ✓ Step 2: Validiere Idee                   │
│ ► Step 3: Idea Forge Divergenz             │
│   └─ Cycle 2/5 - Monetization Expert       │
│ ○ Step 4: Expandiere Top-Ideen             │
│ ○ Step 5: Konvergiere                      │
│                                             │
│ Tokens: 12,450 | Cost: $0.15 | Time: 2:34  │
└─────────────────────────────────────────────┘
```

---

## API Endpoints

### GET /api/workflows
```typescript
interface WorkflowSummary {
  name: string;
  description: string;
  trigger: { type: 'manual' | 'cron' | 'watch' | 'event' };
  status: 'idle' | 'running' | 'scheduled';
  lastRun?: { timestamp: string; status: 'success' | 'failed' };
  nextRun?: string;
}
```

### POST /api/workflows/:name/run
```typescript
// Request
interface RunRequest {
  variables?: Record<string, any>;
  dryRun?: boolean;
}

// Response
interface RunResponse {
  runId: string;
  startedAt: string;
}
```

### WebSocket /api/workflows/stream
```typescript
interface WorkflowEvent {
  type: 'step_start' | 'step_complete' | 'output' | 'error' | 'complete';
  runId: string;
  step?: string;
  data?: any;
}
```

---

## Implementation Checklist

### API Routes
- [ ] GET /api/workflows
- [ ] GET /api/workflows/:name
- [ ] POST /api/workflows/:name/run
- [ ] GET /api/workflows/:name/runs/:runId
- [ ] DELETE /api/workflows/:name/runs/:runId (stop)
- [ ] WebSocket streaming

### Components
- [ ] WorkflowList - Sidebar View
- [ ] WorkflowCard - Einzelner Workflow
- [ ] WorkflowRunner - Execution Modal
- [ ] WorkflowLogs - Live Output
- [ ] WorkflowProgress - Progress Bar

### Hooks
- [ ] useWorkflows() - Liste aller Workflows
- [ ] useWorkflowRun() - Laufender Workflow
- [ ] useWorkflowStream() - WebSocket Connection

---

## Kommunikation

- **Von Python Engineer**: API Schemas + Endpoints
- **An QA Engineer**: UI Test Cases
- **An Code Reviewer**: Component Structure
