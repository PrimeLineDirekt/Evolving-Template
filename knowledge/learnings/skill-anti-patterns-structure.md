# Skill Anti-Patterns Structure

**Quelle**: cc-skills-nanobananapro (Deep Dive 2025-12-27)
**Confidence**: 95% (aus Produktions-Skills extrahiert)
**Typ**: Learning / Best Practice

---

## Kontext

Skills können Claude dazu bringen, Fehler zu machen wenn sie keine klaren Anti-Patterns und Variation Guidance enthalten. Dieses Learning zeigt die bewährte Struktur aus produktionsreifen Skills.

---

## Die 4 Säulen eines robusten Skills

### 1. CRITICAL: Model/Library Enforcement

```markdown
## CRITICAL: Exact Model Names

**Use ONLY these exact strings. Do not invent, guess, or add suffixes.**

| Exact String | Alias | Use Case |
|--------------|-------|----------|
| `gemini-2.5-flash-image` | Nano Banana | Fast iterations |
| `gemini-3-pro-image-preview` | Nano Banana Pro | Quality output |

**Common mistakes to avoid:**
- ❌ `gemini-2.5-flash-preview-05-20` — wrong, date suffixes are for text models
- ❌ `gemini-2.5-pro-image` — wrong, doesn't do image generation
- ❌ `gemini-3-flash-image` — wrong, doesn't exist

**The only valid models are X and Y — no variations.**
```

**Warum wichtig**:
- LLMs "halluzinieren" gerne Varianten von Namen
- Date-Suffixe werden oft fälschlich hinzugefügt
- Klare Tabelle mit EXAKTEN Strings verhindert Raten

---

### 2. Anti-Patterns Section

Strukturiertes Format für jedes Anti-Pattern:

```markdown
## Anti-Patterns to Avoid

❌ **[Was nicht tun]**:
Why wrong: [Begründung warum es problematisch ist]
Better: [Der korrekte Ansatz]

❌ **Using wrong aspect ratio**:
Why wrong: 21:9 on 1:1 request wastes tokens, unexpected crop
Better: Match aspect ratio to intended use case

❌ **No loading states**:
Why wrong: Image generation takes 5-30s, users think it's broken
Better: Show progress indicators and estimated wait time
```

**Typische Anti-Pattern Kategorien**:

| Kategorie | Beispiele |
|-----------|-----------|
| **Naming/Config** | Falsche Model-Namen, falsche Parameter |
| **Performance** | Memory leaks, zu viele Draw Calls |
| **Security** | API Keys client-side, keine Rate Limits |
| **UX** | Keine Loading States, schlechte Error Messages |
| **Code Quality** | Alles in einer Funktion, Hardcoding |
| **Storage** | Base64 in DB, keine Caching-Strategie |

---

### 3. Variation Guidance

Explizite Anweisungen um Konvergenz zu verhindern:

```markdown
## Variation Guidance

**IMPORTANT**: Every app should feel uniquely designed for its purpose.

**Vary across dimensions**:
- **UI Style**: Minimal, brutalist, playful, professional, dark, light
- **Color Scheme**: Warm, cool, monochrome, vibrant, muted
- **Layout**: Single page, wizard, sidebar, grid, list
- **Interaction**: Click-to-generate, drag-drop, real-time, batch

**Avoid overused patterns**:
- ❌ Default Tailwind purple gradients
- ❌ Generic "AI startup" aesthetic
- ❌ Same component libraries for every project
- ❌ Inter/Roboto fonts without thought

**Context should drive design**:
- **Meme generator** → Bold, fun, casual
- **Product mockup tool** → Clean, professional, grid-based
- **Art exploration** → Gallery-first, visual-heavy
```

**Warum wichtig**:
- LLMs neigen zu "Modal Collapse" - konvergieren auf häufigste Muster
- Ohne explizite Variation Guidance sieht alles gleich aus
- Context-driven Design erzwingt Nachdenken

---

### 4. Philosophy/Mental Model Section

Konzeptuelle Grundlagen vor der Implementierung:

```markdown
## Philosophy: [Domain] Mental Model

[Domain] isn't just another [Tool]—it's **[key insight] by design**.

**Think of it as [metaphor]**:
- **[Principle 1]** → [Explanation]
- **[Principle 2]** → [Explanation]
- **[Principle 3]** → [Explanation]

### Before Building, Ask
- What's the primary use case?
- Which [model/approach] fits the need?
- What's the user journey?
- What are production constraints?

### Core Principles
1. **[Principle]**: [Why]
2. **[Principle]**: [Why]
3. **[Principle]**: [Why]
```

**Warum wichtig**:
- Verhindert blindes Code-Generieren
- Erzwingt Kontext-Fragen
- Etabliert Entscheidungsrahmen

---

## Vollständige Skill-Template-Struktur

```markdown
---
name: domain-builder
description: >
  [What the skill does, when to use it, what it covers]
---

# [Skill Name]

[One-sentence value proposition]

---

## CRITICAL: [Exact Values Section]

**Use ONLY these exact [things]. Do not [common mistake].**

| Exact Value | Use Case |
|-------------|----------|
| `exact-value-1` | [When to use] |
| `exact-value-2` | [When to use] |

**Common mistakes to avoid:**
- ❌ [Wrong thing 1] — [why wrong]
- ❌ [Wrong thing 2] — [why wrong]

---

## Philosophy: [Mental Model]

[Key insight about the domain]

**Before Building, Ask**:
- [Context question 1]?
- [Context question 2]?
- [Context question 3]?

**Core Principles**:
1. **[Principle]**: [Explanation]
2. **[Principle]**: [Explanation]

---

## Quick Start

### [Basic Example]

```[language]
[Minimal working code]
```

---

## [Feature Section 1]

[Details...]

---

## Anti-Patterns to Avoid

❌ **[Anti-pattern 1]**:
Why wrong: [Reason]
Better: [Correct approach]

❌ **[Anti-pattern 2]**:
Why wrong: [Reason]
Better: [Correct approach]

---

## Variation Guidance

**IMPORTANT**: [Why variation matters]

**Vary across dimensions**:
- **[Dimension 1]**: [Options]
- **[Dimension 2]**: [Options]

**Avoid overused patterns**:
- ❌ [Common mistake 1]
- ❌ [Common mistake 2]

**Context should drive [design/implementation]**:
- **[Context 1]** → [Appropriate style]
- **[Context 2]** → [Appropriate style]

---

## Remember

**[Domain] enables [value proposition].**

The best [implementations]:
- [Quality 1]
- [Quality 2]
- [Quality 3]

[Inspiring closing statement.]
```

---

## Anwendung auf Evolving Skills

Unsere 4 Skills sollten diese Struktur haben:

| Skill | Anti-Patterns nötig? | Variation Guidance nötig? |
|-------|---------------------|--------------------------|
| template-creator | Ja (Template-Typen verwechseln) | Ja (Agent-Typen variieren) |
| prompt-pro-framework | Ja (Level-Auswahl falsch) | Nein (Prompt-spezifisch) |
| research-orchestrator | Ja (Confidence-Scoring vergessen) | Ja (Research-Tiefe variieren) |
| etsy-poster-creator | Ja (SEO-Mistakes) | Ja (Design variieren) |

---

## Checkliste für Skill-Review

- [ ] Hat CRITICAL Section mit exakten Werten?
- [ ] Hat Anti-Patterns Section mit ❌ Format?
- [ ] Hat Variation Guidance mit "Avoid overused" Liste?
- [ ] Hat Philosophy/Mental Model Section?
- [ ] Hat "Before Building, Ask" Fragen?
- [ ] Hat Quick Start mit minimalem Beispiel?
- [ ] Hat Remember Section mit Key Takeaways?

---

## Related

- [Progressive Disclosure Pattern](../patterns/progressive-disclosure-pattern.md)
- [Skill Template](../../.claude/templates/skills/progressive-skill/)
- [template-creator Skill](../../.claude/skills/template-creator/)
