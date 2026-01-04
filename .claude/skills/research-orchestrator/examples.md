# Research Orchestrator Examples

## Example 1: Market Research

**Input**: "Research AI art generation market 2025"

### Executive Summary
**Topic**: AI Art Generation Market 2025
**Confidence**: 87%
**Key Finding**: Market growing 25% YoY, Midjourney leads consumer segment
**Action**: Focus on niche customization features

### Key Findings

**Finding 1: Market Size**
- Confidence: 92%
- Sources: Statista, Grand View Research, Forbes
- Insight: $5.2B market, projected $15B by 2028

**Finding 2: Competitive Landscape**
- Confidence: 85%
- Leaders: Midjourney (consumer), DALL-E (enterprise), Stable Diffusion (open-source)

### Contradictions Resolved
- Statista: "$4.8B market" vs Grand View: "$5.4B market"
- Resolution: Different scope definitions, averaged to $5.2B

---

## Example 2: Technical Research

**Input**: "Research MCP protocol best practices"

### Executive Summary
**Topic**: MCP Protocol Implementation
**Confidence**: 78%
**Key Finding**: Tool definitions critical, rate limiting essential
**Action**: Implement structured tool schemas

### Findings

**Finding 1: Tool Definition Patterns**
- Confidence: 85%
- Sources: Anthropic docs, Claude Code repo, community patterns
- Insight: JSON Schema validation improves reliability 40%

**Finding 2: Error Handling**
- Confidence: 72%
- Sources: GitHub issues, community discussions
- Insight: Graceful degradation prevents cascading failures

### Knowledge Gaps
- Performance benchmarks under load (needs testing)
- Long-running operation patterns (emerging)

---

## Example 3: Product Research

**Input**: "Research Etsy SEO best practices 2025"

### Executive Summary
**Topic**: Etsy SEO 2025
**Confidence**: 91%
**Key Finding**: Natural language titles outperform keyword stuffing
**Action**: Update title generator algorithm

### Findings

**Finding 1: Title Optimization**
- Confidence: 94%
- Sources: Etsy Seller Handbook, eRank, Marmalead
- Evidence: Listings with natural titles see +23% CTR

**Finding 2: Tag Strategy**
- Confidence: 88%
- 13 tags optimal: 3 broad + 5 mid + 5 long-tail

---

## Anti-Patterns

### ❌ Single Source
```
Finding: "Market is $10B"
Source: One blog post
Confidence: Should be <30%
```

### ❌ Outdated Data
```
Finding: Based on 2021 report
Action: Must find 2024/2025 data
```

### ❌ Unresolved Contradiction
```
Source A: "X is best practice"
Source B: "X is anti-pattern"
→ Must analyze context and resolve
```

### ❌ No Actionable Insight
```
Finding: "Market exists"
→ Should be: "Enter via niche X because..."
```
