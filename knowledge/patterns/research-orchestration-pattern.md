# Research Orchestration Pattern

**Quelle**: anthropic-cookbook/patterns/agents/research_lead_agent.md
**Extrahiert**: 2025-12-28
**Tags**: research, orchestration, subagents, parallel-execution, query-classification

---

## Überblick

Strukturiertes Framework für Research-Aufgaben mit intelligenter Query-Klassifikation und effizienter Subagent-Delegation.

---

## Query Type Classification

### 1. Depth-First Query
**Signal**: Multiple perspectives on same issue, "going deep"

- Core question remains singular but benefits from diverse approaches
- Parallel agents explore different viewpoints/methodologies/sources

**Beispiele**:
- "What are the most effective treatments for depression?" → Different treatment approaches
- "What caused the 2008 financial crisis?" → Economic, regulatory, behavioral perspectives
- "Best approach to building AI finance agents?" → Technology, architecture, implementation views

**Strategie**: 3-5 perspective-based subagents, synthesize findings

### 2. Breadth-First Query
**Signal**: Distinct, independent sub-questions, "going wide"

- Query naturally divides into parallel research streams
- Independent subtopics that can be researched simultaneously

**Beispiele**:
- "Compare economic systems of Nordic countries" → One agent per country
- "Fortune 500 CEOs net worth and ages" → Divide into segments
- "Compare frontend frameworks" → One per framework

**Strategie**: Enumerate subtopics, clear boundaries, prevent overlap

### 3. Straightforward Query
**Signal**: Focused, well-defined, single investigation

- Can be handled by single focused agent
- Simple fact-finding or minor analysis

**Beispiele**:
- "Current population of Tokyo?" → Simple fact lookup
- "List all Fortune 500 companies" → Single source fetch
- "Tell me about bananas" → Basic explanation

**Strategie**: 1 subagent with clear, direct instructions

---

## Subagent Count Guidelines

| Query Complexity | Subagents | Example |
|------------------|-----------|---------|
| Simple/Straightforward | 1 | "Tax deadline this year?" |
| Standard | 2-3 | "Compare top 3 cloud providers" |
| Medium | 3-5 | "AI impact on healthcare" |
| High | 5-10 (max 20) | "Fortune 500 CEOs data" |

**Iron Rule**: Never >20 subagents. If seems necessary → restructure approach.

> "More subagents = more overhead. Only add when they provide distinct value."

---

## Research Process

### Phase 1: Assessment & Breakdown

1. **Identify** main concepts, key entities, relationships
2. **List** specific facts/data points needed
3. **Note** temporal/contextual constraints
4. **Analyze** what user cares about most
5. **Determine** required answer format

### Phase 2: Query Type Determination

- Explicitly state reasoning for classification
- Match to Depth-First, Breadth-First, or Straightforward
- Consider hybrid approaches

### Phase 3: Research Plan Development

**For Depth-First**:
- Define 3-5 methodological approaches
- List expert viewpoints to explore
- Plan unique insights per perspective
- Specify synthesis strategy

**For Breadth-First**:
- Enumerate independent sub-questions
- Prioritize by importance & complexity
- Define clear boundaries (prevent overlap)
- Plan aggregation strategy

**For Straightforward**:
- Identify direct path to answer
- Specify exact data points needed
- Determine relevant sources
- Plan verification methods

### Phase 4: Plan Execution

- Deploy subagents immediately after planning
- Use parallel execution where possible
- Monitor progress, adapt to findings
- Know when to stop (diminishing returns)

---

## Delegation Best Practices

### Clear Task Descriptions must include:

1. **Specific objective** (ideally 1 core objective)
2. **Expected output format** (list, report, answer, etc.)
3. **Background context** about user's question
4. **Key questions** to answer
5. **Suggested sources** and quality criteria
6. **Specific tools** to use
7. **Scope boundaries** to prevent drift

### Example Good Task Description:

```
Research the semiconductor supply chain crisis and its current status.
Use web_search and web_fetch tools.

Begin by examining:
- Quarterly reports from TSMC, Samsung, Intel (investor relations)
- Industry reports from SEMI, Gartner, IDC

Investigate government responses:
- US CHIPS Act progress at commerce.gov
- EU Chips Act at ec.europa.eu

Prioritize original sources over news aggregators.

Focus on:
- Current bottlenecks
- Projected capacity increases
- Geopolitical factors
- Expert predictions

Output: Dense fact report covering current situation, solutions,
future outlook with specific timelines and quantitative data.
```

---

## Parallel Execution Pattern

```
ALWAYS parallel for 2+ independent subagents:

[Planning Phase] → Sequential (you do this)
       ↓
[Subagent Creation] → PARALLEL (3 subagents simultaneously)
       ↓
[Results Collection] → Wait for all
       ↓
[Synthesis] → Sequential (you do this)
```

**Important**: While waiting for subagents, use time efficiently:
- Analyze previous results
- Update research plan
- Reason about query

---

## Stopping Criteria

**Stop research when**:
- Sufficient information gathered for good answer
- Further research has diminishing returns
- Time constraints reached
- Confidence threshold met

> "If you have identified the top 5 startups with high confidence, stop immediately and write the report rather than continuing unnecessarily."

---

## Anti-Patterns

| Anti-Pattern | Better Approach |
|--------------|-----------------|
| >20 subagents | Restructure approach, consolidate tasks |
| Subagent for trivial tasks | Do simple calculations yourself |
| Overlapping subagent tasks | Define clear boundaries |
| Subagent writes final report | YOU always synthesize final output |
| Sequential when parallel possible | Use parallel tool calls |

---

## Integration mit Evolving

Dieses Pattern ergänzt:
- `research-analyst-agent.md` - Als Orchestration Layer
- `parallel-agent-dispatch-pattern.md` - Execution Details
- `/sparring` Command - Research Mode

---

## Related

- [Parallel Agent Dispatch](parallel-agent-dispatch-pattern.md)
- [Recursive Research Pattern](recursive-research-pattern.md)
- [Intake Gate Pattern](intake-gate-pattern.md)
