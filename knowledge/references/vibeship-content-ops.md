# VibeShip Content Ops

**Quelle**: vibeship-knowledgebase/docs/.content-ops/
**Extrahiert**: 2026-01-01
**Kategorie**: reference

---

## Übersicht

Content Operations Pipeline für world-class vibe coding content. 3-Phasen System mit Spawner Skills Integration, 14 Personas für humanisierten Content, und rigorosem QA-System.

## Enhanced Pipeline (3 Phasen)

```
PHASE 1: DISCOVERY + RESEARCH
├── Ahrefs MCP → Keyword Data
├── Content Strategy + SEO Skills
├── Competitor Gap Analysis
└── Output: Enhanced Content Brief

PHASE 2: PERSONALITY + WRITING
├── Persona Selection (14 Personas)
├── Blog Writing + Copywriting Skills
├── Voice Notes & Signature Moves
└── Output: Human-feeling Content

PHASE 3: QA + POLISH
├── 5 Quality Checks (SEO, LLM, Tech, Human, Design)
├── Value Score Assessment (min 20/25)
└── Output: Publication-ready Svelte Component
```

---

## Die 14 Personas

### Vulnerabilities (Security Content)

| Handle | Rolle | Best For |
|--------|-------|----------|
| **@pager_duty** | The Firefighter | Breach-heavy, critical vulns, urgency |
| **@flaggedthis** | The Auditor | Checklists, compliance, process |
| **@eli5sec** | The Translator | Complex vulns simplified, analogies |
| **@breachlore** | The Historian | Famous breaches, CVE history |

### Prompts & Tools

| Handle | Rolle | Best For |
|--------|-------|----------|
| **@keystrokecounts** | The Optimizer | Tool comparisons, workflow optimization |
| **@tryhard_tk** | The Tinkerer | New features, experiments, roundups |
| **@deletedmost** | The Minimalist | Streamlining, anti-bloat, essentials |

### Guides & Stacks

| Handle | Rolle | Best For |
|--------|-------|----------|
| **@ninascales** | The Architect | Architecture, system design, scaling |
| **@pat_ships** | The Pragmatist | MVP security, shipping, time pressure |
| **@danawhy** | The Debugger | Troubleshooting, error resolution |
| **@samexplains** | The Mentor | Foundational guides, mental models |

### Vibe Coding General

| Handle | Rolle | Best For |
|--------|-------|----------|
| **@vibecheckpassed** | The Evangelist | Tool showcases, adoption guides |
| **@waitwhat_** | The Skeptic | Caution, balanced takes, reality checks |
| **@buildermagic** | The Builder | Tutorials, hands-on, "build X with Y" |

---

## Persona Selection Matrix

```python
IF topic.urgency == HIGH:
    → @pager_duty (Firefighter)
IF topic.needs_simplification:
    → @eli5sec (Translator)
IF topic.is_comparison:
    → @keystrokecounts (Optimizer)
IF topic.is_tutorial:
    → @buildermagic (Builder)
IF topic.needs_skepticism:
    → @waitwhat_ (Skeptic)
IF topic.is_architecture:
    → @ninascales (Architect)
DEFAULT:
    → @samexplains (Mentor)
```

---

## QA Checklist (5 Checks)

### 1. SEO Validation (SEO Skill)
- [ ] Title under 60 chars with primary keyword
- [ ] Meta description 150-160 chars with CTA
- [ ] Primary keyword in first 100 words
- [ ] Primary keyword in at least one H2
- [ ] 5-10 internal links with descriptive anchors
- [ ] 1-2 external authority links (OWASP, CWE)
- [ ] FAQ targets PAA questions from Ahrefs

### 2. LLM Citation Check (Content Strategy Skill)
- [ ] Each section 75-225 words (extractable)
- [ ] Sections self-contained (quotable alone)
- [ ] Facts have attribution + links
- [ ] FAQ answers start with direct answer
- [ ] Specific numbers, not vague claims
- [ ] First sentence answers implied question

### 3. Technical Accuracy (Domain Skill)
- [ ] CWE/OWASP references correct
- [ ] Code examples compile/run
- [ ] Security advice is current best practice
- [ ] Links are valid
- [ ] Statistics have sources

### 4. Humanizer Check
- [ ] No AI tells (Furthermore, It's important to note)
- [ ] Varied sentence structure
- [ ] Persona voice consistent throughout
- [ ] Signature moves used at key moments
- [ ] Opening hook lands in first 50 words

### 5. Design System Check (MANDATORY)
- [ ] Uses CSS variables only (NO hardcoded colors)
- [ ] Sharp edges (NO border-radius: 8px)
- [ ] Uses global components (.badge, .faq-list, .card)
- [ ] Under 150 lines scoped CSS
- [ ] Mobile responsive
- [ ] Code comparisons stacked vertically (NOT side-by-side)

---

## Value Score System

| Dimension | Score 1-5 | Was gemessen wird |
|-----------|-----------|-------------------|
| **Actionability** | /5 | Kann User in 10 min fixen? |
| **Clarity** | /5 | Versteht non-technical Founder? |
| **Specificity** | /5 | Framework-spezifisch, nicht generisch? |
| **Completeness** | /5 | Alles an einem Ort? |
| **Uniqueness** | /5 | Besser als Konkurrenz? |
| **TOTAL** | /25 | **Minimum 20 zum Publishen** |

---

## Workflow Modes

| Mode | Zeit | Wann nutzen |
|------|------|-------------|
| **Mode A: Quick** | ~15 min | Single Article, schnell |
| **Mode B: Quality** | ~45 min | Single Article, gründlich |
| **Mode C: Batch** | Variable | Multiple Articles parallel |

---

## Persona Packet Format

```markdown
## Persona Packet: [Article Title]

### Selected Persona
**@[handle]** - [Role Name]
**Reasoning:** [1-2 sentences why this persona fits]
**Rotation check:** ✅ Last used [date] / ⚠️ Recently used

### Opening Hook
[1-2 sentences in persona voice, punchy, characteristic]

### Signature Move Opportunities
1. **[Section]:** [How to apply technique]
2. **[Section]:** [How to apply technique]
3. **[Section]:** [How to apply technique]

### Voice Notes for Writer
**Sentence style:** [Short/medium/varied?]
**Tone:** [Urgent/patient/skeptical/enthusiastic?]
**Recurring phrases:** [Natural phrases for this persona]
**Avoid:** [What would feel out of character]
```

---

## Ahrefs MCP Integration

**Phase 1 Tools:**
```
1. keywords-explorer-overview
   → Search volume, difficulty, intent
   → Input: keywords, country="us"

2. keywords-explorer-matching-terms
   → Related keywords, long-tail
   → Input: keywords, country="us", limit=20

3. serp-overview-serp-overview
   → Top 10 analysis
   → Input: keyword, country="us"

4. site-explorer-organic-competitors
   → Competitor identification
   → Input: target domain, country="us"
```

---

## Skill Combos by Content Type

| Content Type | Primary Skills | Supporting Skills |
|--------------|---------------|-------------------|
| **Security/Vulnerabilities** | Cybersecurity, Security | Content Strategy, SEO |
| **Tool Comparisons** | Content Strategy, SEO | Developer Communications |
| **Prompts/Rules** | Developer Communications | Copywriting |
| **Guides/Tutorials** | Developer Communications | Content Strategy |

---

## Lokaler Pfad

```
{EVOLVING_PATH}/_archive/repos/2026-01-01-deep-dive/vibeship-knowledgebase/docs/.content-ops/
├── README.md                    # Quick Start
├── ENHANCED-PIPELINE.md         # Full 3-Phase Pipeline
├── PIPELINE.md                  # Original Pipeline
├── QUEUE.md                     # What to write next
├── agents/
│   ├── research-agent.md        # Phase 1 Agent
│   ├── personality-agent.md     # Phase 2 Persona Selection
│   └── writer-agent.md          # Phase 2 Writing
├── templates/
│   ├── vulnerability-brief.md
│   ├── tool-brief.md
│   └── stack-brief.md
├── guides/
│   └── content-humanizer-guide.md  # Full Persona Profiles
├── checklists/
│   └── qa-checklist.md
└── briefs/                      # Article Research Data
```

---

## Key Takeaways

1. **Persona macht den Unterschied**: Content ohne Persona-Lens ist bland
2. **Research First**: Bad brief = bad content
3. **QA ist nicht optional**: Minimum 20/25 Score zum Publishen
4. **Design System ist strict**: NO hardcoded colors, NO border-radius 8px+
5. **Rotation beachten**: Gleiche Persona nicht 2x hintereinander

---

## Related

- [vibeship-spawner-skills.md](vibeship-spawner-skills.md) - Spawner Skill Library
- [claude-skills-generator.md](claude-skills-generator.md) - Skill Templates
- [knowledge/patterns/content-humanizer-pattern.md](../patterns/content-humanizer-pattern.md)
