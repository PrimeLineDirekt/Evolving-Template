# Etsy Poster Creator Reference

## Quick Start

```
User: "Create Etsy listing for Wall Art sunset beach watercolor"
→ Bilingual SEO + Midjourney Prompts + Pinterest Pins
```

## Workflow Phases

```
1. Input → Category, Motif, Style
2. Midjourney → V6/V7 selection, aspect ratio, stylize
3. SEO → EN + DE titles, tags, descriptions
4. Pinterest → Mobile titles, ALT text
5. Trends → Google Trends analysis
6. Validate → 5+ images @ 2000px+
```

## Category Defaults

| Category | AR | Version | Stylize |
|----------|-----|---------|---------|
| Wall Art | 2:3 | v7 | 100-200 |
| Baby Room | 2:3 | v6 | 0-50 |
| Kitchen | 4:5 | v7 | 50-150 |
| Office | 16:9 | v7 | 100-250 |
| Bedroom | 2:3 | v7 | 50-150 |
| Living Room | 3:2 | v7 | 100-200 |

## SEO Rules

**Title**: Natural language, 140 chars max
```
✅ "Serene Sunset Beach Watercolor Print - Coastal Wall Art"
❌ "Sunset Beach Print Wall Art Poster Download" (keyword stuffing)
```

**Tags**: 13 total = 3 broad + 5 mid + 5 long-tail
- German tags: auto-shorten to ≤20 chars

## Pinterest Rules

- Title: 45-65 chars (mobile-optimized)
- ALT text: SEO-rich for +123% clicks
- Images: Vertical preferred (82% mobile)

## Midjourney Selection

| Context | Version | Why |
|---------|---------|-----|
| Baby/Kids | v6 | Softer, safer aesthetics |
| Everything else | v7 | Faster, modern style |

## Output Format

```markdown
# {Category} - {Motif} {Style}

## MIDJOURNEY PROMPT
{prompt} --ar {ar} --stylize {s} --{version}

## ETSY LISTING (EN)
Title: {title}
Tags: {13 tags}
Description: {description}

## ETSY LISTING (DE)
Titel: {title}
Tags: {13 tags}
Beschreibung: {description}

## PINTEREST
Pin Title: {45-65 chars}
ALT Text: {seo alt}

## TRENDS
Direction: {rising|stable}
Peak: {months}
```

## Validation Checklist

- [ ] 5+ images @ 2000px+
- [ ] First image mobile-optimized
- [ ] Natural language title
- [ ] German tags ≤20 chars
- [ ] Correct V6/V7 selection
