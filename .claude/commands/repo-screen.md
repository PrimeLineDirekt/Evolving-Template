# /repo-screen

Schneller Relevanz-Check für GitHub Repos bevor Deep Analysis.

## Usage

```
/repo-screen [URL oder Liste von URLs]
```

## Model: haiku

## Trigger-Patterns
- "Check diese Repos"
- "Sind diese Repos relevant"
- "Screen die Repos"
- "Prüfe ob relevant"

## Workflow

### 1. Input parsen
Extrahiere alle GitHub URLs aus der Eingabe.

### 2. Pro Repo: Quick Screen

Für jede URL:

```
a) README.md fetchen via WebFetch:
   https://raw.githubusercontent.com/{owner}/{repo}/main/README.md
   (Fallback: master branch)

b) Relevanz-Indikatoren checken:

   STRUKTUR (aus README oder Repo-Beschreibung):
   - .claude/ Ordner erwähnt?
   - agents/, skills/, commands/ Struktur?
   - MCP Server / .mcp.json?
   - CLAUDE.md / AGENTS.md?

   KEYWORDS (im README):
   - "Claude" / "Anthropic" / "Claude Code"
   - "Multi-Agent" / "Agent Orchestration"
   - "MCP" / "Model Context Protocol"
   - "Knowledge Base" / "Second Brain"
   - "Prompt Engineering" / "Prompts"
   - "Workflow Automation" / "n8n"
   - "AI-First" / "LLM"
   - "Skills" / "Commands" / "Hooks"

c) Relevanz-Entscheidung:
   - JA: Mindestens 2 starke Indikatoren ODER 1 sehr starker (Claude Code spezifisch)
   - NEIN: Keine oder schwache Indikatoren
```

### 3. Output generieren

Format pro Repo:
```
{owner}/{repo} → JA/NEIN
Grund: {1-2 Sätze warum relevant oder nicht}
---
```

### 4. Zusammenfassung

```
SCREEN ERGEBNIS:
- Relevant: X Repos
- Skip: Y Repos

Relevante Repos für Deep Analysis:
- {liste}

Nächster Schritt: /analyze-repo {url} für Details
```

## Beispiel

Input:
```
/repo-screen
https://github.com/anthropics/claude-code
https://github.com/random/gaming-framework
https://github.com/modelcontextprotocol/servers
```

Output:
```
anthropics/claude-code → JA
Grund: Offizielles Claude Code CLI - direkt relevant für unser System.
---
random/gaming-framework → NEIN
Grund: Gaming Framework ohne AI/Agent Bezug.
---
modelcontextprotocol/servers → JA
Grund: MCP Server Referenz-Implementierungen - relevant für MCP Integration.
---

SCREEN ERGEBNIS:
- Relevant: 2 Repos
- Skip: 1 Repo

Relevante Repos für Deep Analysis:
- anthropics/claude-code
- modelcontextprotocol/servers
```

## Hinweise

- Nutze WebFetch für Remote-Zugriff
- Bei Rate-Limits: Kurz warten zwischen Requests
- Bei Fehlern (404, private Repo): Als "SKIP - nicht zugänglich" markieren
