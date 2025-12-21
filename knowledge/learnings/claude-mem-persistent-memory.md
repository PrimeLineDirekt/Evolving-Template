# Claude-Mem Persistent Memory System

> **Source**: [thedotmack/claude-mem](https://github.com/thedotmack/claude-mem)
> **Version**: v6.4.9+
> **Type**: Learning / External Project Analysis
> **Relevance**: HIGH - Persistent Memory, Hook Architecture, Token Efficiency

## Konzept

Claude-Mem ist ein Plugin-System das persistente Memory über Sessions hinweg ermöglicht durch:
1. **Hook-basierte Capture** - Tool-Outputs automatisch erfassen
2. **AI-gestützte Compression** - Semantische Observations generieren
3. **Progressive Disclosure** - Index-Layer mit Token-Kosten zeigen
4. **Hybrid Search** - SQLite FTS5 + Chroma Vector Search

## 5-Hook Lifecycle Architektur

```
SessionStart      → Context Injection (letzte Observations laden)
     ↓
UserPromptSubmit  → Session erstellen, Prompt speichern
     ↓
PostToolUse       → Tool-Output zu Observation komprimieren
     ↓
Stop              → Session-Summary generieren
     ↓
SessionEnd        → Cleanup, Status finalisieren
```

### Hook-Implementation Pattern

```typescript
// Fire-and-Forget HTTP Pattern
async function saveHook(input: PostToolUseInput): Promise<HookResponse> {
  await ensureWorkerRunning();

  const response = await fetch(`http://127.0.0.1:${port}/api/sessions/observations`, {
    method: 'POST',
    body: JSON.stringify({
      claudeSessionId: input.session_id,
      toolName: input.tool_name,
      toolInput: input.tool_input,
      toolResponse: input.tool_response,
      project: extractProjectName(input.cwd)
    })
  });

  return createHookResponse();
}
```

**Key Insight**: Hooks sind reine HTTP-Clients. Die Logik liegt im Worker Service.

## Observation Model

### Datenstruktur

```typescript
interface ObservationRecord {
  id: number;
  sdk_session_id: string;
  project: string;
  text: string;
  type: 'decision' | 'bugfix' | 'feature' | 'refactor' | 'discovery' | 'change';
  title?: string;
  subtitle?: string;
  narrative?: string;
  facts?: string;
  concepts?: string[];  // JSON Array
  source_files?: string;
  prompt_number?: number;
  discovery_tokens?: number;
  created_at_epoch: number;
}
```

### Observation Types

| Type | Icon | Beschreibung |
|------|------|--------------|
| decision | - | Architektur-/Design-Entscheidung |
| bugfix | - | Fehler behoben |
| feature | - | Neues Feature implementiert |
| refactor | - | Code umstrukturiert |
| discovery | - | Neue Erkenntnis |
| change | - | Allgemeine Änderung |

## AI Prompts für Observation-Generierung

### Init Prompt (Session Start)

```
Du bist ein Memory Agent der eine parallele Claude Code Session beobachtet.
Deine Aufgabe: Learnings, Builds und Konfigurationen aufzeichnen.

WICHTIG: Dokumentiere was GELERNT/GEBAUT/GEFIXT/DEPLOYED/KONFIGURIERT wurde,
nicht was du (der Observer) tust.

Gute Observation: "Authentication unterstützt jetzt OAuth2"
Schlechte Observation: "Ich habe mir den Auth-Code angesehen"
```

### Observation Prompt (PostToolUse)

```xml
<tool_execution>
  <tool_name>{toolName}</tool_name>
  <timestamp>{timestamp}</timestamp>
  <working_directory>{cwd}</working_directory>
  <input>{parsedInput}</input>
  <outcome>{parsedResult}</outcome>
</tool_execution>
```

### Summary Prompt (Stop)

```xml
<session_summary>
  <request>{Was wurde angefragt}</request>
  <investigated>{Was wurde untersucht}</investigated>
  <learned>{Was wurde gelernt}</learned>
  <completed>{Was wurde abgeschlossen}</completed>
  <next_steps>{Aktuelle Arbeitsrichtung, nicht zukünftige Arbeit}</next_steps>
</session_summary>
```

## Token Efficiency Pattern

### Das Problem

```
Standard Session: O(N²) Komplexität
- Claude re-synthetisiert alle vorherigen Outputs
- ~50 Tool Uses = Context Window erschöpft
```

### Die Lösung: Observation Compression

```
Tool Output: ~2000-10000 Tokens
     ↓
AI Compression
     ↓
Observation: ~500 Tokens (75-95% Reduktion)
```

### Token-Berechnung

```typescript
const CHARS_PER_TOKEN_ESTIMATE = 4;

function calculateReadCost(observation: Observation): number {
  const obsSize = [
    observation.title,
    observation.subtitle,
    observation.narrative,
    observation.facts
  ].join(' ').length;

  return Math.ceil(obsSize / CHARS_PER_TOKEN_ESTIMATE);
}
```

## Progressive Disclosure Pattern

### 4-Schritt Workflow

```
1. SEARCH    → Query ausführen, Index-Ergebnisse bekommen (~50-100 Tokens/Result)
2. TIMELINE  → Chronologischen Kontext verstehen
3. REVIEW    → Relevante IDs identifizieren
4. FETCH     → Nur benötigte Details laden (~500-1000 Tokens/Observation)
```

### Index vs Full Display

**Index View** (niedrige Token-Kosten):
```
[ID: 142] 14:30 [feature] Implemented OAuth2 authentication (~350 tokens)
[ID: 143] 14:45 [decision] Chose JWT over session cookies (~280 tokens)
```

**Full View** (höhere Token-Kosten):
```
[ID: 142] 14:30 [feature] Implemented OAuth2 authentication

Narrative: Added OAuth2 support using passport.js with Google provider...
Facts:
- Created auth/oauth.ts with passport configuration
- Added GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET to .env
- Modified user model to support OAuth providers
Files: src/auth/oauth.ts, src/models/user.ts, .env.example
```

### Batch Fetching

```typescript
// IMMER Batch verwenden bei 2+ Observations
const observations = await mcp.get_batch_observations({ ids: [142, 143, 145] });

// NICHT einzeln fetchen (10-100x langsamer)
// const obs1 = await mcp.get_observation({ id: 142 });
// const obs2 = await mcp.get_observation({ id: 143 });
```

## Endless Mode (Beta)

### Konzept

```
Standard:  Full Tool Outputs im Context = O(N²) = ~50 Tool Uses max
Endless:   Compressed Observations = O(N) = ~1000+ Tool Uses möglich
```

### Implementation

```
Tool Execute
     ↓
Compress to ~500 Token Observation (sofort)
     ↓
Archive Full Output to Disk
     ↓
Keep Only Observation in Context
```

**Erwartete Ergebnisse**:
- ~95% Token-Reduktion
- ~20x mehr Tool Uses pro Session
- Lineare O(N) Skalierung

## Privacy System

### Dual-Tag Approach

```markdown
<!-- User-kontrolliert: Wird NICHT gespeichert -->
<private>
Sensible Daten hier...
</private>

<!-- System-generiert: Wird nach Injection gestripped -->
<claude-mem-context>
Automatisch injizierte Observations...
</claude-mem-context>
```

**Edge Processing**: Tag-Stripping passiert in der Hook-Layer vor Storage.

## Database Schema

### SQLite mit FTS5

```sql
-- Observations mit Full-Text Search
CREATE TABLE observations (
  id INTEGER PRIMARY KEY,
  sdk_session_id TEXT,
  project TEXT,
  type TEXT,
  title TEXT,
  subtitle TEXT,
  narrative TEXT,
  facts TEXT,
  concepts TEXT,  -- JSON Array
  created_at_epoch INTEGER
);

CREATE VIRTUAL TABLE observations_fts USING fts5(
  title, subtitle, narrative, facts,
  content='observations'
);

-- Session Summaries
CREATE TABLE session_summaries (
  id INTEGER PRIMARY KEY,
  sdk_session_id TEXT,
  request TEXT,
  investigated TEXT,
  learned TEXT,
  completed TEXT,
  next_steps TEXT
);
```

### Chroma Vector DB

Für semantische Suche zusätzlich zu FTS5 Keyword-Suche.

## Integration mit Evolving

### Was wir übernehmen können

| Konzept | Evolving Equivalent | Status |
|---------|---------------------|--------|
| Observation Types | Experience Types | Bereits implementiert |
| Hook Architecture | .claude/hooks/ | Bereits vorhanden |
| Progressive Disclosure | - | Pattern erstellen |
| Token Efficiency | - | Pattern erstellen |
| Session Summary | /whats-next | Bereits vorhanden |
| Endless Mode | - | Konzept dokumentieren |

### Unterschiede zu unserem System

| claude-mem | Evolving |
|------------|----------|
| Plugin-basiert | Natives Claude Code |
| Worker Service (Bun) | Direkte File-Operationen |
| SQLite + Chroma | JSON Files + _memory/ |
| Automatische Capture | Manuelle /remember Commands |

### Mögliche Erweiterungen

1. **Automatic Observation Hook**: PostToolUse Hook der wichtige Änderungen automatisch erfasst
2. **Token Cost Visibility**: Bei /recall Token-Kosten für Details anzeigen
3. **Batch Fetch Pattern**: Bei mehreren Experience-Abrufen Batching nutzen

## Best Practices aus claude-mem

1. **Fokus auf Deliverables**: "Was wurde GEBAUT" nicht "Was wurde GETAN"
2. **Observation Compression**: Full Output → Semantic Summary
3. **Progressive Disclosure**: Index first, Details on demand
4. **Batch Operations**: Immer batchen bei 2+ Items
5. **Privacy by Design**: Stripping an der Edge (Hook-Layer)

---

## Related

- `knowledge/patterns/progressive-disclosure-pattern.md` (zu erstellen)
- `knowledge/patterns/observation-compression-pattern.md` (zu erstellen)
- `.claude/rules/experience-suggest.md` - Unser Experience Auto-Suggest
- `_memory/experiences/` - Unser Experience Memory System
