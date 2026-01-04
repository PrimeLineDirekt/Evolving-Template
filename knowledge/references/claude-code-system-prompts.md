# Claude Code System Prompts Reference

> > **Version**: 2.0.69 (December 12, 2025)
> **Total Prompts**: 59
> **Related Tool**: tweakcc - Customize Claude Code prompts

## Überblick

Claude Code nutzt nicht EINEN System Prompt, sondern **40+ verschiedene Prompt-Strings** die dynamisch kombiniert werden basierend auf:
- Environment und Konfiguration
- Aktivem Tool/Agent
- Session-Kontext
- User-Einstellungen

## Prompt-Kategorien

### 1. Agent Prompts (24 Prompts)

#### Sub-agents
| Name | Tokens | Zweck |
|------|--------|-------|
| Explore | 516 | Codebase-Navigation, Dateisuche (READ-ONLY) |
| Plan mode (enhanced) | 633 | Software-Architektur, Implementation Design (READ-ONLY) |
| Task tool | 294 | Sub-Agent Spawning für komplexe Tasks |

#### Creation Assistants
| Name | Tokens | Zweck |
|------|--------|-------|
| Agent creation architect | 1,111 | Erstellt Custom Agents aus User-Anforderungen |
| CLAUDE.md creation | 384 | Generiert CLAUDE.md Dateien |
| Status line setup | ~300 | Konfiguriert Status Line |

#### Slash Commands
| Name | Tokens | Zweck |
|------|--------|-------|
| Security review | 2,614 | Security Code Review mit False-Positive Filtering |
| PR comments | ~500 | GitHub PR Kommentar-Handling |

#### Utilities
| Name | Tokens | Zweck |
|------|--------|-------|
| Agent hook | ~200 | Hook Execution für Agents |
| Bash command file path extraction | ~150 | Extrahiert Dateipfade aus Bash Output |
| Bash command prefix detection | ~150 | Erkennt Command-Prefixe |
| Bash output summarization | ~200 | Fasst lange Bash-Outputs zusammen |
| Claude guide agent | ~400 | Navigiert Claude Code/SDK/API Docs |
| Conversation summarization | ~300 | Fasst Konversationen zusammen |
| Exit plan mode with swarm | ~500 | Team-basierte Plan-Ausführung |
| Prompt hook execution | ~200 | Hook Execution für Prompts |
| Prompt suggestion generator | ~300 | Generiert Prompt-Vorschläge |
| Session notes template | ~400 | Strukturierte Session-Dokumentation |
| Session notes update | ~200 | Updates für Session Notes |
| Session title generation | ~150 | Generiert Session-Titel |
| Update magic docs | ~200 | Aktualisiert Dokumentation |
| User sentiment analysis | ~200 | Analysiert User-Stimmung |
| WebFetch summarizer | ~200 | Fasst Web-Inhalte zusammen |

### 2. System Prompts (5 Prompts)

| Name | Tokens | Zweck |
|------|--------|-------|
| **Main system prompt** | 3,097 | Kern-Verhalten und Policies |
| Learning mode | 1,042 | Interaktives "Learn by Doing" |
| Learning mode insights | ~300 | Feedback nach User-Implementierung |
| MCP CLI | 1,335 | Model Context Protocol Integration |
| Scratchpad directory | ~200 | Temporäre Dateien Management |

### 3. System Reminders (5 Prompts)

| Name | Tokens | Zweck |
|------|--------|-------|
| MCP CLI large output | ~300 | Handling großer MCP Outputs |
| Plan mode is active | 1,211 | Plan Mode Constraints für Haupt-Agent |
| Plan mode (for subagents) | ~800 | Plan Mode Constraints für Sub-Agents |
| Plan mode re-entry | 236 | Wiedereintritt in Plan Mode |
| Team coordination | ~400 | Multi-Agent Team Koordination |

### 4. Tool Descriptions (21 Prompts)

| Tool | Tokens | Zweck |
|------|--------|-------|
| **TodoWrite** | 2,167 | Task-Management und Progress-Tracking |
| **Task** | 1,193 | Sub-Agent Spawning |
| **Bash** | 1,074 | Shell Command Execution |
| ReadFile | 439 | Datei lesen |
| Edit | ~400 | Datei bearbeiten |
| Write | ~300 | Datei erstellen |
| Glob | ~250 | Datei-Pattern Matching |
| Grep | ~300 | Content Search |
| WebFetch | ~350 | Web Content Fetching |
| WebSearch | ~300 | Web Search |
| AskUserQuestion | ~400 | User-Interaktion |
| EnterPlanMode | ~300 | Plan Mode aktivieren |
| ExitPlanMode | ~250 | Plan Mode verlassen |
| ExitPlanMode v2 | ~300 | Erweiterte Version mit Swarm |
| Skill | ~300 | Skill Execution |
| SlashCommand | ~250 | Command Execution |
| NotebookEdit | ~300 | Jupyter Notebook Bearbeitung |
| TaskUpdate | ~250 | Task Status Updates |
| LSP | ~400 | Language Server Protocol |

#### Additional Tool Notes
| Name | Zweck |
|------|-------|
| Bash (git commit/PR) | Spezielle Anweisungen für Git |
| Bash (sandbox note) | Sandbox-Modus Hinweise |
| Task (async return) | Async Task Handling |

### 5. Data Files (4 Prompts)

| Name | Zweck |
|------|-------|
| GitHub Actions (code review) | Workflow für automatisierte Reviews |
| GitHub Actions (mentions) | Workflow für @claude Mentions |
| GitHub App (PR description) | PR Beschreibungs-Template |

## Wichtige Konzepte aus den Prompts

### Main System Prompt - Kern-Policies

```
1. SECURITY
   - Niemals URLs raten/generieren
   - Sensible Daten schützen

2. COMMUNICATION
   - Kurz und prägnant (CLI-Display)
   - GitHub-flavored Markdown
   - Keine Emojis (außer explizit angefragt)

3. FILE OPERATIONS
   - Niemals unnötige Dateien erstellen
   - Immer existierende Dateien editieren bevorzugen
   - Dokumentation nur auf Anfrage

4. TECHNICAL STANDARDS
   - Technische Genauigkeit > User-Validierung
   - Over-Engineering vermeiden
   - Unused Code löschen, nicht deprecaten
```

### Explore Agent - READ-ONLY Constraints

```
STRIKT VERBOTEN:
- Dateien erstellen/ändern/löschen
- Verschieben/Kopieren
- Write/Redirect Operationen

ERLAUBT:
- Glob, Grep, Read Tools
- Bash: ls, find, cat, git log (read-only)
```

### Plan Mode - Architecture Focus

```
FOKUS:
- Requirements verstehen
- Pattern Discovery
- Architecture Analysis
- Code Path Tracing

OUTPUT:
- "Critical Files for Implementation" (3-5 Dateien)
- Detailed Plan mit Dependencies
```

### TodoWrite - Task Management Rules

```
NUTZEN BEI:
- 3+ Schritte
- Multi-File Changes
- Komplexe Tasks
- User gibt Liste

NICHT NUTZEN BEI:
- Einzelne triviale Aktionen
- Reine Fragen/Recherche
- Quick Fixes

REGELN:
- Nur 1 Task in_progress gleichzeitig
- Sofort als completed markieren
- Nie completed wenn Tests failen
```

### Security Review - False Positive Prevention

```
CONFIDENCE THRESHOLD: 80%+

HARD EXCLUSIONS:
- Memory Safety in Rust
- Unit Test Files
- Rate Limiting
- DoS Vulnerabilities
- Client-Side Validation
- Missing Headers
- Outdated Dependencies
```

### Team Coordination - Multi-Agent Rules

```
NAMING:
✓ "team-lead", "analyzer", "researcher"
✗ "agent-uuid-12345"

COMMUNICATION:
- Task Assignments
- Progress Updates
- Result Submissions
```

## Token Counts Summary

| Kategorie | Prompts | Total Tokens | Durchschnitt |
|-----------|---------|--------------|--------------|
| Agent Prompts | 24 | ~8,500 | ~354 |
| System Prompts | 5 | ~5,000 | ~1,000 |
| System Reminders | 5 | ~3,000 | ~600 |
| Tool Descriptions | 21 | ~8,500 | ~405 |
| Data | 4 | ~2,000 | ~500 |
| **Total** | 59 | ~27,000 | ~458 |

## Versionierung

Das Repo trackt Änderungen über 50+ Versionen seit v2.0.14.

### Wichtige Version-Milestones

| Version | Änderung |
|---------|----------|
| 2.0.60 | Team Coordination System (+1339 Tokens) |
| 2.0.59 | TaskUpdate Tool |
| 2.0.62 | AskUserQuestion Tool |
| 2.0.66 | Scratchpad Directory |

## Integration mit Evolving

### Patterns extrahiert
- [Security Review Pattern](../patterns/security-review-pattern.md)
- [Swarm Team Coordination Pattern](../patterns/swarm-team-coordination-pattern.md)
- [Learning Mode Pattern](../patterns/learning-mode-pattern.md)

### Templates übernommen
- [Session Notes Template](../../.claude/templates/session-notes-template.md)

### Commands inspiriert
- `/security-review` - Security Code Review
- Enhanced `/whats-next` - Mit Session Notes Template

## Updates

Repository wird aktiv maintained. Für Updates:
```bash
# Check latest version
curl -s https://registry.npmjs.org/@anthropic-ai/claude-code | jq '.["dist-tags"].latest'
```

---

## Links

- **tweakcc Tool**: https://github.com/Piebald-AI/tweakcc
- **Piebald**: https://piebald.ai/
