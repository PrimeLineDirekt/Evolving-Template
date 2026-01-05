---
name: compose-agent
description: Erstelle einen dynamischen Agent aus dem Trait-System (480 Kombinationen)
trigger: /compose-agent
model: sonnet
argument-hint: <expertise> [personality] [approach]
arguments:
  - name: expertise
    required: true
    description: Domain expertise (researcher, engineer, etc.)
  - name: personality
    required: false
    default: "direct"
    description: Communication style (precise, creative, etc.)
  - name: approach
    required: false
    default: "systematic"
    description: Execution pattern (systematic, iterative, etc.)
---

# /compose-agent

Erstellt einen dynamischen Agent aus dem Trait-System.

**Kombinations-Power**: 10 Expertise x 8 Personality x 6 Approach = **480 einzigartige Agents**

---

## Usage

```
/compose-agent <expertise> [personality] [approach]
```

**Defaults**:
- personality: `direct`
- approach: `systematic`

---

## Examples

```bash
# Vollständig spezifiziert
/compose-agent researcher skeptical systematic
/compose-agent engineer precise iterative
/compose-agent strategist empathetic consultative

# Mit Defaults (personality=direct, approach=systematic)
/compose-agent analyst
/compose-agent creative

# Teilweise spezifiziert
/compose-agent security cautious    # approach=systematic (default)
/compose-agent architect thorough exploratory
```

---

## Valid Trait Values

### Expertise (10)

| Key | Beschreibung | Tools | Disclaimer |
|-----|--------------|-------|------------|
| `researcher` | Deep investigation, multi-source validation | WebSearch, WebFetch, Read, Grep | - |
| `architect` | System design, trade-off analysis | Read, Glob, Grep, Write | - |
| `engineer` | Implementation, debugging, optimization | Read, Write, Edit, Bash, LSP | - |
| `analyst` | Data analysis, pattern recognition | Read, Bash, WebSearch | - |
| `strategist` | Planning, prioritization, roadmapping | Read, Write, TodoWrite | - |
| `legal` | Legal analysis, compliance checking | WebSearch, Read | Yes |
| `creative` | Ideation, unconventional solutions | WebSearch, Read | - |
| `security` | Threat modeling, vulnerability assessment | Read, Grep, Bash, LSP | Yes |
| `communications` | Outreach, messaging, PR | Read, Write, WebSearch | - |
| `medical` | Health research, medical info synthesis | WebSearch, Read | Yes |

### Personality (8)

| Key | Beschreibung | Voice |
|-----|--------------|-------|
| `precise` | Exact, cites sources, no ambiguity | "According to...", "Specifically..." |
| `creative` | Lateral thinking, unconventional | "What if...", "Imagine..." |
| `cautious` | Highlights risks, edge cases | "However...", "One concern is..." |
| `direct` | Concise, no fluff, straight to point | "Bottom line:", "Key point:" |
| `thorough` | Covers all aspects, comprehensive | "Additionally...", "Furthermore..." |
| `contrarian` | Devil's advocate, challenges assumptions | "Have you considered...", "The opposite view..." |
| `empathetic` | User-focused, considers emotions | "I understand...", "That's a valid concern..." |
| `skeptical` | Questions claims, demands evidence | "What's the evidence for...", "Let's verify..." |

### Approach (6)

| Key | Pattern | Best For |
|-----|---------|----------|
| `systematic` | Linear step-by-step | Complex problems, audits, compliance |
| `exploratory` | Diverge-converge | Research, unknown domains, discovery |
| `iterative` | Spiral refinement | Creative work, evolving requirements |
| `parallel` | Branching | Optimization, A/B analysis, multi-option |
| `adversarial` | Attack-defend | Security review, robustness testing |
| `consultative` | Dialogue | Advisory, unclear requirements |

---

## Recommended Combinations

| Kombination | Alias | Use Case |
|-------------|-------|----------|
| `researcher skeptical systematic` | Academic Researcher | Rigorous multi-source research |
| `engineer precise iterative` | Senior Developer | Quality-focused implementation |
| `strategist direct consultative` | Executive Advisor | Strategic planning with stakeholders |
| `security cautious adversarial` | Security Auditor | Threat modeling, pen test planning |
| `creative creative exploratory` | Innovation Lead | Brainstorming, ideation sessions |
| `analyst thorough systematic` | Business Analyst | Comprehensive data analysis |
| `legal cautious systematic` | Compliance Officer | Regulatory review, contract analysis |
| `medical empathetic consultative` | Health Advisor | Supportive health information |

---

## Output

Der Command generiert einen vollständigen Agent-Prompt mit:

1. **Identity Header** - Expertise + Personality + Approach
2. **Voice & Tone** - Sprachstil, Marker, Vermeidungen
3. **Execution Pattern** - Schritte basierend auf Approach
4. **Tools** - Verfügbare Tools für die Expertise
5. **Output Style** - Erwartetes Output-Format
6. **Disclaimer** - Falls Expertise es erfordert (legal, security, medical)

---

## Execution Flow

```
1. Parse Arguments
   └─ expertise (required)
   └─ personality (default: direct)
   └─ approach (default: systematic)

2. Validate Traits
   └─ Check against valid options
   └─ Return error with suggestions if invalid

3. Load Trait Data
   └─ knowledge/agents/trait-taxonomy.json
   └─ knowledge/agents/voice-mappings.json
   └─ knowledge/agents/disclaimers.json (if needed)

4. Compose Agent
   └─ Fill .claude/templates/agents/dynamic-agent.md
   └─ Apply all placeholders

5. Output Agent Prompt
   └─ Complete markdown agent definition
   └─ Ready for immediate use
```

---

## Error Messages

**Ungültige Expertise**:
```
Fehler: Ungültige Expertise "{input}"

Gültige Optionen:
researcher, architect, engineer, analyst, strategist,
legal, creative, security, communications, medical

Beispiel: /compose-agent researcher skeptical systematic
```

**Ungültige Personality**:
```
Fehler: Ungültige Personality "{input}"

Gültige Optionen:
precise, creative, cautious, direct, thorough,
contrarian, empathetic, skeptical

Default ist "direct" wenn nicht angegeben.
```

**Ungültiger Approach**:
```
Fehler: Ungültiger Approach "{input}"

Gültige Optionen:
systematic, exploratory, iterative, parallel,
adversarial, consultative

Default ist "systematic" wenn nicht angegeben.
```

---

## Related

- **Agent Factory**: `.claude/agents/agent-factory.md`
- **Template**: `.claude/templates/agents/dynamic-agent.md`
- **Trait System**: `knowledge/agents/trait-taxonomy.json`
- **Voice Mappings**: `knowledge/agents/voice-mappings.json`
- **Disclaimers**: `knowledge/agents/disclaimers.json`

---

## Quick Reference Card

```
┌─────────────────────────────────────────────────────────────┐
│  /compose-agent <expertise> [personality] [approach]        │
├─────────────────────────────────────────────────────────────┤
│  EXPERTISE (10)     PERSONALITY (8)     APPROACH (6)        │
│  ─────────────      ──────────────      ────────────        │
│  researcher         precise             systematic          │
│  architect          creative            exploratory         │
│  engineer           cautious            iterative           │
│  analyst            direct (default)    parallel            │
│  strategist         thorough            adversarial         │
│  legal*             contrarian          consultative        │
│  creative           empathetic                              │
│  security*          skeptical                               │
│  communications                                             │
│  medical*                                                   │
│                                                             │
│  * = includes disclaimer                                    │
├─────────────────────────────────────────────────────────────┤
│  480 unique combinations available                          │
└─────────────────────────────────────────────────────────────┘
```
