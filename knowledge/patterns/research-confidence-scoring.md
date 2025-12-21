---
title: "Research Confidence Scoring Pattern"
type: pattern
category: research-methodology
created: 2024-11-22
source: external
confidence: 95%
tags: [research, validation, quality-control, multi-source]
---

# Research Confidence Scoring Pattern

## Problem

Wie validiert man Research-Ergebnisse wenn man AI-gestützt recherchiert? Ohne systematisches Scoring System führt "gut gemeint" oft zu "falsch implementiert".

## Solution

**Multi-Source Confidence Scoring System** mit quantifizierbaren Metriken.

### Core Formula

```
Confidence Score = (Source Quality × Source Agreement × Recency × Validation) / 100

Where:
- Source Quality: Expert sources (10) > Industry blogs (7) > Forums (4)
- Source Agreement: All agree (10) > Majority (7) > Mixed (4)
- Recency: 2024-2025 (10) > 2023 (7) > older (4)
- Validation: Case studies (10) > Data (7) > Opinion (4)
```

### Scoring Tiers

- **90-100%**: Production-Ready - Trust this completely
- **80-89%**: High Confidence - Safe for most use cases
- **70-79%**: Medium Confidence - Verify in production
- **Below 70%**: Low Confidence - Needs more research

### Minimum Requirements

**For Production Systems**:
- Minimum 15 sources per critical feature
- Minimum 90% confidence for go-live
- At least 3 Tier-1 sources (official docs, expert analysis, case studies $100K+)

## Example (E-Commerce Platform Research)

### Algorithm Research Example

**Sources**: 32+ premium sources
**Validation**: 16,000+ user actions analyzed
**Case Studies**: High-revenue seller analysis
**Result**: **96.35% Confidence** → Production-Ready

**Breakdown**:
- Source Quality: 9.5/10 (mix of Tier-1 experts + official docs)
- Source Agreement: 10/10 (zero contradictions)
- Recency: 10/10 (all current year data)
- Validation: 10/10 (real case studies + data)

**Confidence = (9.5 × 10 × 10 × 10) / 100 = 95%**
**+ 1.35% for 150+ validated data points = 96.35%**

## Implementation

### Step 1: Source Categorization

```markdown
TIER 1 (Weight: 10)
- Official Documentation
- Expert Analysis (verified professionals)
- Case Studies $100K+ revenue

TIER 2 (Weight: 7)
- Industry Publications
- Reputable Blogs
- Academic Research

TIER 3 (Weight: 4)
- Forums (Reddit, Quora)
- User Reviews
- Anecdotal Evidence
```

### Step 2: Multi-Source Validation

**Required**:
- Minimum 3 sources for any claim
- Minimum 1 Tier-1 source for critical features
- Document contradictions explicitly

**Track**:
```
Claim: "Fresh content gets 90%+ traffic on platform X"
- Source 1 (Tier 1): Official Platform Docs (confirmed)
- Source 2 (Tier 1): High-revenue Case Study (88-92% fresh content)
- Source 3 (Tier 2): Platform Expert (85-95% estimate)

Agreement: High (88-95% range)
Confidence: 92%
```

### Step 3: Recency Check

```
2024-2025: Weight 10 (current)
2023: Weight 7 (recent)
2022 or older: Weight 4 (outdated for fast-moving platforms)
```

**Critical**: For algorithm-driven platforms (social media, e-commerce, search), recency is CRITICAL.

### Step 4: Documentation

```markdown
## Feature: {Name}
**Confidence Score**: 92%
**Sources**: 18 (Tier-1: 5, Tier-2: 10, Tier-3: 3)
**Last Updated**: 2024-11-20
**Validated**: Yes (case study + real data)

**Contradictions**: None
**Assumptions**: Platform algorithm stable for 6+ months
**Review Date**: [Review date based on platform update cycle]
```

## Trade-offs

### Pros
- Quantifiable quality metrics
- Multi-source bias prevention
- Clear go/no-go decisions
- Trackable over time

### Cons
- Time-intensive (15+ sources per feature)
- Requires domain knowledge for source evaluation
- Needs regular review (recency decay)

## When to Use

**YES**:
- Production systems with revenue dependency
- Features with compliance requirements
- Algorithm-dependent features (SEO, Social)
- Critical business decisions

**NO**:
- Internal tools with low risk
- Experimental features (iterate fast)
- Well-established patterns (reinventing wheel)

## Related Patterns

- **AI Content Generation Pipeline**: Uses confidence scores for output validation
- **Multi-Agent Orchestration**: Agents include confidence in outputs

## Real-World Results

**Example Projects**:
- Platform Integration: 96.35% confidence → Zero production issues
- Trend Analysis: 88% confidence → Minor recency adjustments needed
- Bilingual SEO: 92% confidence → Performed as expected

**Learning**: 90%+ confidence = reliable production deployment

---

**Related**:
- [Research Orchestrator](../prompts/research-agents/) - if available

**Navigation**: [← Patterns](README.md) | [← Knowledge Base](../index.md)
