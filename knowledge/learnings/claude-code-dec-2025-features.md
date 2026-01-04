# Claude Code December 2025 Features

> > **Relevanz**: Hoch - Features die Evolving-Workflows verbessern
> **Stand**: 2025-12-19 (aktualisiert)

---

## High-Impact Features

### 1. Claude in Chrome (Beta) - v2.0.72 ✅ AKTIV

**Was**: Browser-Kontrolle direkt aus Claude Code via Chrome Extension.

**Setup**:
1. Extension installieren: https://claude.ai/chrome
2. In Claude Code: `/chrome` startet Browser-Kontrolle

**Verfügbare Tools** (via MCP):
- `mcp__claude-in-chrome__navigate` - URL navigieren
- `mcp__claude-in-chrome__read_page` - Accessibility Tree lesen
- `mcp__claude-in-chrome__find` - Elemente per Natural Language finden
- `mcp__claude-in-chrome__computer` - Maus/Keyboard Interaktion
- `mcp__claude-in-chrome__screenshot` - Screenshots machen
- `mcp__claude-in-chrome__form_input` - Formulare ausfüllen
- `mcp__claude-in-chrome__javascript_tool` - JS ausführen
- `mcp__claude-in-chrome__get_page_text` - Text extrahieren
- `mcp__claude-in-chrome__gif_creator` - GIF-Recording
- `mcp__claude-in-chrome__tabs_context_mcp` - Tab-Kontext holen

**Use Cases für Evolving**:
- Web Research automatisieren
- Screenshots von Webseiten für Analyse
- Form-Ausfüllung für Tests
- Competitive Analysis
- Web Scraping für Knowledge Base

**Status**: ✅ Verfügbar und einsatzbereit!

---

### 2. Named Sessions - v2.0.64

**Was**: Sessions benennen und später fortsetzen.

**Commands**:
```bash
/rename dashboard-work       # Session benennen
/resume dashboard-work       # In REPL fortsetzen
claude --resume dashboard-work  # Von Terminal
```

**Use Cases für Evolving**:
- Projekt-spezifische Sessions (z.B. "{project-name}", "dashboard")
- Langfristige Arbeit ohne Memory-Verlust
- Parallele Kontexte für verschiedene Projekte

**Integration**:
- Kombiniert mit Domain Memory für persistenten State
- Könnte `/scenario` ergänzen

---

### 3. Background Agents - v2.0.60

**Was**: Agents laufen im Hintergrund während Hauptarbeit weitergeht.

**Use Cases für Evolving**:
- Research-Agent läuft parallel zur Implementierung
- Build/Test im Hintergrund
- Long-running Analysis Tasks

**Status**: Automatisch verfügbar wenn Task-Tool genutzt wird.

---

### 4. Async Operations - v2.0.64

**Was**: Agents und Bash-Commands können asynchron laufen und Main-Agent "aufwecken".

**Bedeutung**:
- Multi-Task Workflows möglich
- Bessere Orchestrierung von langen Tasks
- Parallelisierung

---

### 5. Quick Model Switch - v2.0.65

**Was**: Modell wechseln während man tippt.

**Shortcut**:
- macOS: `Option + P`
- Linux/Windows: `Alt + P`

**Bedeutung für Evolving**:
- Schneller als `/opus`, `/sonnet`, `/haiku` Commands
- Inline-Wechsel für spezifische Anfragen

**Update**: Unsere Model-Switcher Commands bleiben trotzdem nützlich für explizite Workflows.

---

### 6. Thinking Mode Default für Opus 4.5 - v2.0.67

**Was**: Extended Thinking ist jetzt standardmäßig aktiviert für Opus 4.5.

**Bedeutung**:
- `/opus+` Ultrathink-Command ist jetzt quasi Standard
- Bessere Reasoning-Qualität automatisch

**Toggle**: `Alt + T` (nicht mehr Tab)

---

### 7. MCP Wildcard Permissions - v2.0.70

**Was**: Alle Tools eines MCP-Servers erlauben/verbieten mit einem Eintrag.

**Syntax**:
```json
{
  "allow": ["mcp__github__*"],
  "deny": ["mcp__dangerous-server__*"]
}
```

**Bedeutung für Evolving**:
- Einfachere `.claude.json` Konfiguration
- Bulk-Permissions für MCP Server

---

### 8. `--agent` CLI Flag - v2.0.59

**Was**: Agent-Override für eine Session.

**Syntax**:
```bash
claude --agent research-analyst
```

**Use Cases**:
- Direkt in Agent-Modus starten
- Kombiniert mit Named Sessions

---

### 9. `/stats` Command - v2.0.64

**Was**: Persönliche Nutzungsstatistiken.

**Zeigt**:
- Favorite Model
- Usage Graph
- Usage Streak

**Nutzen**: Optimierung der eigenen Workflows basierend auf Daten.

---

### 10. Context Window Info - v2.0.65

**Was**: `current_usage` Feld für genaue Context-Window-Berechnungen.

**Bedeutung**: Besseres Token-Management für lange Sessions.

---

## Bereits genutzt (kein Action nötig)

| Feature | Version | Status |
|---------|---------|--------|
| `.claude/rules/` Directory | v2.0.64 | Aktiv (12 Rules) |
| Thinking Mode Toggle | v2.0.67 | Via `/opus+` |
| MCP Server Support | v2.0.71+ | Aktiv (3 Server) |

---

## Action Items

| Feature | Priorität | Aktion | Status |
|---------|-----------|--------|--------|
| Chrome Extension | Hoch | Testen & Workflow dokumentieren | ✅ Aktiv |
| Named Sessions | Hoch | In COMMANDS.md dokumentieren | ✅ Dokumentiert |
| Background Agents | Mittel | Bei Research-Workflows nutzen | ✅ Verfügbar |
| `--agent` Flag | Niedrig | Für Scenario-Starts evaluieren | Backlog |

---

## Keyboard Shortcuts (Quick Reference)

| Shortcut | Funktion | Plattform |
|----------|----------|-----------|
| `Option + P` | Model wechseln während Tippen | macOS |
| `Alt + P` | Model wechseln während Tippen | Linux/Win |
| `Alt + T` | Thinking Mode Toggle | Alle |
| `Tab` | Prompt Suggestion akzeptieren | Alle |
| `Ctrl + R` | History Search (bash-style) | Alle |
| `Alt + Y` | Yank-pop (kill ring cycle) | Alle |

---

## Related

- `.claude/COMMANDS.md` - Workflow-Dokumentation (inkl. Native Commands Sektion)
- `knowledge/references/claude-code-system-prompts.md` - System Prompts
- `_memory/` - Domain Memory (ergänzt Named Sessions)

