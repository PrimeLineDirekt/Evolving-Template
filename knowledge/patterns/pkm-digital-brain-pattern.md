# PKM Digital Brain Pattern

**Typ**: System Architecture Pattern
**Confidence**: 90%
**Source**: Agent-Skills-for-Context-Engineering/digital-brain-skill
**Priority**: P2 - Medium
**Erstellt**: 2026-01-01

---

## Problem

Personal Knowledge Management (PKM) Systeme scheitern an:
- Zu viel Context Bloat bei Agent-Interaktionen
- Keine klare Struktur für AI-Assistenz
- Daten-Integrität gefährdet bei AI-Edits
- Inkonsistente Voice bei Content-Generierung
- Fragmentierte Beziehungs- und Wissens-Silos

## Solution

**5-Module Digital Brain Architecture** mit Progressive Disclosure und Append-Only Data Integrity.

```
┌─────────────────────────────────────────────────────────────┐
│                    DIGITAL BRAIN                             │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐    │
│  │ IDENTITY │  │ CONTENT  │  │ KNOWLEDGE│  │ NETWORK  │    │
│  │          │  │          │  │          │  │          │    │
│  │ voice    │  │ ideas    │  │ bookmarks│  │ contacts │    │
│  │ brand    │  │ posts    │  │ research │  │ circles  │    │
│  │ values   │  │ calendar │  │ learning │  │ intros   │    │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘    │
│                                                              │
│  ┌──────────────────────────────────────┐                  │
│  │            OPERATIONS                 │                  │
│  │  todos | goals | meetings | metrics   │                  │
│  └──────────────────────────────────────┘                  │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## 5-Module Struktur

### Modul 1: Identity (READ FIRST)

**Zweck**: Personal Brand, Voice, Values - IMMER vor Content-Generierung lesen.

| Datei | Format | Inhalt |
|-------|--------|--------|
| `voice.md` | Markdown | Tone, Style, Vocabulary, Patterns |
| `brand.md` | Markdown | Positioning, Audience, Content Pillars |
| `values.yaml` | YAML | Core Beliefs, Principles |
| `bio-variants.md` | Markdown | Platform-spezifische Bios |
| `prompts/*.xml` | XML | Reusable Generation Templates |

**Critical Rule**:
> "Always read `identity/voice.md` before generating ANY content."

### Modul 2: Content

**Zweck**: Content-Pipeline von Idea bis Published Post.

```
ideas.jsonl → drafts/ → posts.jsonl
     ↓           ↓           ↓
  Capture    Develop      Log + Metrics
```

| Datei | Format | Inhalt |
|-------|--------|--------|
| `ideas.jsonl` | JSONL | Raw Ideas (append-only) |
| `posts.jsonl` | JSONL | Published Content + Metrics |
| `calendar.md` | Markdown | Content Schedule |
| `engagement.jsonl` | JSONL | Saved Inspiration |
| `templates/*.md` | Markdown | Thread, Newsletter, Post Templates |

### Modul 3: Knowledge

**Zweck**: Personal Knowledge Base - Bookmarks, Research, Learning.

| Datei | Format | Inhalt |
|-------|--------|--------|
| `bookmarks.jsonl` | JSONL | Saved Resources |
| `learning.yaml` | YAML | Skills & Learning Goals |
| `competitors.md` | Markdown | Market Landscape |
| `research/*.md` | Markdown | Deep-Dive Notes |

### Modul 4: Network

**Zweck**: Personal CRM mit Relationship Tiers.

| Datei | Format | Inhalt |
|-------|--------|--------|
| `contacts.jsonl` | JSONL | People Database |
| `interactions.jsonl` | JSONL | Meeting/Call Log |
| `circles.yaml` | YAML | Relationship Tiers |
| `intros.md` | Markdown | Introduction Tracker |

### Modul 5: Operations

**Zweck**: Productivity System - Tasks, Goals, Metrics.

| Datei | Format | Inhalt |
|-------|--------|--------|
| `todos.md` | Markdown | Task List (P0-P3) |
| `goals.yaml` | YAML | OKRs |
| `meetings.jsonl` | JSONL | Meeting Notes |
| `metrics.jsonl` | JSONL | Key Metrics |
| `reviews/*.md` | Markdown | Weekly Reviews |

---

## JSONL Append-Only Pattern

**Critical Data Integrity Rule**:

> JSONL files are **append-only**. NEVER delete entries.

### Warum Append-Only?

```
SCHLECHT (Deletion):
- Verliert History
- Keine Pattern-Analyse möglich
- "Was funktioniert hat" nicht nachvollziehbar
- AI-Fehler permanent

GUT (Append-Only):
- History preserved
- "What worked" Retrospectives möglich
- Pattern-Analyse über Zeit
- AI-Fehler reversibel via Archive-Status
```

### Status statt Deletion

```json
// Statt: Eintrag löschen
// Setze: status: "archived"

{"id": "idea_001", "status": "active", "content": "..."}
{"id": "idea_001", "status": "archived", "archived_at": "2026-01-01"}
```

### JSONL Schema-Beispiel (Idea)

```json
{
  "id": "idea_YYYYMMDD_HHMMSS",
  "created": "ISO8601",
  "updated": "ISO8601",
  "status": "raw|developing|ready|published|archived",
  "content": "The idea text",
  "pillar": "ai_agents|content|personal",
  "format": "thread|post|newsletter|video",
  "source": "How you got the idea",
  "notes": "Development notes",
  "developed_to": "post_id if published"
}
```

---

## Relationship Tiers Pattern

Aus dem Network Module:

```yaml
circles:
  inner:
    description: "Close relationships - friends, advisors, confidants"
    touchpoint_frequency: "weekly"

  active:
    description: "Current collaborators, frequent interaction"
    touchpoint_frequency: "bi-weekly"

  network:
    description: "Known contacts, periodic touchpoints"
    touchpoint_frequency: "monthly"

  dormant:
    description: "Historical connections, may reactivate"
    touchpoint_frequency: "quarterly check-in"
```

### Circle-Based Maintenance

| Circle | Touchpoint | Aktion bei Stale |
|--------|------------|------------------|
| **inner** | Weekly | Sofort erreichen |
| **active** | Bi-Weekly | Diese Woche Kontakt |
| **network** | Monthly | Nächste Woche Kontakt |
| **dormant** | Quarterly | Reactivation prüfen |

### Stale Contact Detection

```python
# agents/scripts/stale_contacts.py
def find_stale_contacts(contacts: List[Contact]) -> List[Contact]:
    stale = []
    for contact in contacts:
        days_since = (now - contact.last_contact).days
        threshold = CIRCLE_THRESHOLDS[contact.circle]
        if days_since > threshold:
            stale.append(contact)
    return sorted(stale, key=lambda c: c.circle)  # inner first
```

---

## Progressive Disclosure Architecture (L1/L2/L3)

**Core Principle**: Load only what's needed for the current task.

### Die 3 Levels

| Level | Wann geladen | Was |
|-------|--------------|-----|
| **L1: Metadata** | Immer | SKILL.md Overview (diese Datei) |
| **L2: Module Instructions** | On-demand | `[module]/[MODULE].md` |
| **L3: Data Files** | As-needed | `.jsonl`, `.yaml`, `.md` Data |

### Loading Flow

```
User: "Write a X post about AI agents"
           │
           ▼
┌─────────────────────────────────┐
│ L1: SKILL.md (bereits geladen)  │
│ → Erkenne: Content Creation     │
└─────────────────────────────────┘
           │
           ▼
┌─────────────────────────────────┐
│ L2: identity/IDENTITY.md        │
│     content/CONTENT.md          │
│ → Module Instructions           │
└─────────────────────────────────┘
           │
           ▼
┌─────────────────────────────────┐
│ L3: identity/voice.md (FIRST!)  │
│     identity/brand.md           │
│     content/posts.jsonl (recent)│
│ → Actual Data                   │
└─────────────────────────────────┘
           │
           ▼
┌─────────────────────────────────┐
│ Generate post with voice        │
└─────────────────────────────────┘
```

### Trigger-basierte L2 Loading

| Trigger Phrase | Load Modules |
|----------------|--------------|
| "write a post", "content ideas" | identity, content |
| "who is [name]", "prepare for meeting" | network, operations |
| "weekly review" | operations, content, network |
| "save this", "bookmark" | knowledge |
| "my goals" | operations |

---

## File Format Strategy

Optimiert für Agent Parsing:

| Format | Use Case | Warum |
|--------|----------|-------|
| **JSONL** | Append-only Logs | Agent-friendly, History erhalten |
| **YAML** | Structured Config | Human-readable Hierarchies |
| **Markdown** | Narrative Content | Editierbar, Rich Formatting |
| **XML** | Complex Prompts | Klare Struktur für Agents |

### Format-Entscheidungsbaum

```
Daten-Typ
    │
    ├─ Wächst über Zeit? → JSONL (append-only)
    │     (ideas, posts, contacts, interactions)
    │
    ├─ Hierarchische Struktur? → YAML
    │     (goals, values, circles, learning)
    │
    ├─ Narrative/Editierbar? → Markdown
    │     (voice, brand, todos, calendar)
    │
    └─ Komplexe Prompts? → XML
          (generation templates)
```

---

## Workflows

### Content Creation Workflow

```
1. Read identity/voice.md (REQUIRED!)
2. Check identity/brand.md for topic alignment
3. Reference content/posts.jsonl for successful patterns
4. Use content/templates/ as starting structure
5. Draft matching voice attributes
6. Log to posts.jsonl after publishing
```

### Pre-Meeting Preparation

```
1. Look up contact: network/contacts.jsonl
2. Get history: network/interactions.jsonl
3. Check pending: operations/todos.md
4. Generate brief with context
```

### Weekly Review Process

```
1. Run: python agents/scripts/weekly_review.py
2. Review metrics in operations/metrics.jsonl
3. Check stale contacts: agents/scripts/stale_contacts.py
4. Update goals progress in operations/goals.yaml
5. Plan next week in content/calendar.md
```

---

## Evolving Integration

### Mapping zu Evolving-Struktur

| Digital Brain Module | Evolving Equivalent |
|---------------------|---------------------|
| identity/ | knowledge/personal/ |
| content/ | ideas/, prompts/ |
| knowledge/ | knowledge/ (allgemein) |
| network/ | - (nicht implementiert) |
| operations/ | _memory/, _ledgers/ |

### Was wir übernehmen können

1. **JSONL Append-Only**: Für `_memory/experiences/` bereits genutzt
2. **Relationship Tiers**: Für Projekt-Stakeholder-Management
3. **Progressive Disclosure**: Bereits in Skills implementiert
4. **Voice-First**: Für `knowledge/personal/system-instructions.md`

### Potentielle Erweiterungen

```
Evolving/
├── network/                 # NEU: Personal CRM
│   ├── contacts.jsonl
│   ├── interactions.jsonl
│   └── circles.yaml
```

---

## Best Practices

### DO

1. **Voice First**: IMMER `identity/voice.md` vor Content lesen
2. **Append Only**: Niemals aus JSONL löschen, nur archivieren
3. **Update Timestamps**: `updated` Field bei Änderungen setzen
4. **Cross-Reference**: Knowledge informiert Content, Network informiert Operations
5. **Log Interactions**: Meetings/Calls immer in `interactions.jsonl`

### DON'T

1. **Skip Voice**: Content ohne Voice-Check generieren
2. **Delete Entries**: JSONL-Einträge löschen statt archivieren
3. **Overload Context**: Alle Module gleichzeitig laden
4. **Ignore History**: `posts.jsonl` nicht für Pattern-Learning nutzen

---

## Related Patterns

- [Progressive Disclosure Pattern](progressive-disclosure-pattern.md) - L1/L2/L3 Loading
- [Context Window Ownership Pattern](context-window-ownership-pattern.md) - Token Budget
- [Experience Memory Pattern](../learnings/experience-memory-pattern.md) - Append-Only für Experiences
- [Multi-Agent Orchestration Pattern](multi-agent-orchestration.md) - Agent-Module Separation

---

**Navigation**: [<- Patterns](README.md) | [Knowledge Index](../index.md)
