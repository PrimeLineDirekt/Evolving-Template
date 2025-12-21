# Prompts - Meta-Prompting Storage

Dieser Ordner speichert Prompts die mit `/create-prompt` erstellt wurden.

---

## Struktur

```
prompts/
├── README.md              ← Du bist hier
├── 001-{name}.md          ← Erster Prompt
├── 002-{name}.md          ← Zweiter Prompt
├── ...
└── archive/               ← Ausgeführte/archivierte Prompts
    └── YYYY-MM-DD/
        └── {prompts}
```

---

## Workflow

### 1. Prompt erstellen

```
/create-prompt Analysiere meine Konkurrenz
```

→ Erstellt: `prompts/001-competitor-analysis.md`

### 2. Prompt ausführen

```
/run-prompt 001
```

→ Führt Prompt in frischem Sub-Agent Kontext aus

### 3. Prompt archivieren (optional)

Nach Ausführung wird angeboten:
- Archive → `prompts/archive/2025-12-01/001-xxx.md`
- Keep → Bleibt für Wiederverwendung
- Delete → Wird gelöscht

---

## Datei-Format

```markdown
---
created: YYYY-MM-DD
type: research|creative|strategy|technical
level: 1-5
model: haiku|sonnet|opus
status: ready|draft|archived
---

# Prompt Title

{DER PROMPT INHALT}

---

## Metadata

**Erstellt von**: /create-prompt
**Ausführen mit**: /run-prompt {NNN}
```

---

## Commands

| Command | Zweck |
|---------|-------|
| `/create-prompt {task}` | Neuen Prompt erstellen |
| `/run-prompt {N}` | Prompt ausführen |
| `/run-prompt {N} {M} --parallel` | Mehrere parallel |
| `/run-prompt {N} {M} --sequential` | Mehrere sequentiell |

---

## Warum Meta-Prompting?

### Context Separation

```
OHNE Meta-Prompting:
┌─────────────────────────────────┐
│  Gleicher Kontext               │
│  Planning + Execution gemischt  │
│  → Context Bleeding             │
└─────────────────────────────────┘

MIT Meta-Prompting:
┌───────────────┐    ┌───────────────┐
│  Context A    │    │  Context B    │
│  /create      │    │  /run         │
│  (Planning)   │    │  (Execution)  │
└───────────────┘    └───────────────┘
        ↓                   ↑
   001-prompt.md ───────────┘
```

### Wiederverwendung

- Einmal erstellt, mehrfach genutzt
- Prompts verbessern ohne neu zu erstellen
- Library aufbauen

### Parallelisierung

- Unabhängige Prompts gleichzeitig ausführen
- Abhängige Prompts sequentiell verketten

---

## Naming Convention

**Format**: `{NNN}-{kebab-case-name}.md`

**Beispiele**:
- `001-seo-optimization.md`
- `002-competitor-analysis.md`
- `003-pricing-strategy-research.md`
- `004-content-calendar-creation.md`

**Regeln**:
- 3-stellige Nummer (001, 002, ...)
- Kebab-case für Namen
- Max 5 Wörter im Namen
- Beschreibend aber kurz

---

## Prompt Quality

Alle Prompts folgen dem **Prompt Pro Framework**:

- 5-Level Technique Hierarchy
- XML-Struktur für Klarheit
- Success Criteria definiert
- Output-Format spezifiziert

→ Siehe `.claude/skills/prompt-pro-framework/` für Details

---

**Erstellt**: 2025-12-01
**System**: Evolving Meta-Prompting
