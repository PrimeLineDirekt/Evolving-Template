# Agent Templates

Agent templates provide production-ready architectures for building specialized AI agents in your workflows.

## What are Agent Templates?

Agent templates define AI agents with specific expertise, tools, and execution patterns. They're used in multi-agent systems where different agents handle specialized domains.

## When to Use Agent Templates

- Building domain-specific experts (tax, legal, research, etc.)
- Creating research agents for multi-source validation
- Orchestrating complex workflows with multiple agents
- Implementing the Multi-Agent Orchestration pattern

## Available Templates

### 1. Specialist Agent (`specialist-agent.md`)

**Use for**: Domain experts with deep knowledge in specific areas.

**Complexity**: Medium

**Examples**:
- Tax optimization specialist
- Legal compliance expert
- Security auditor
- Financial planner

**Key Features**:
- Domain-specific expertise
- Structured input/output
- Tool configuration
- Quality validation

### 2. Research Agent (`research-agent.md`)

**Use for**: Multi-source research, data collection, and validation.

**Complexity**: Medium-High

**Examples**:
- Market research analyst
- Competitive intelligence
- Technical documentation researcher
- Trend analysis

**Key Features**:
- Multi-source validation
- Confidence scoring
- Citation management
- Synthesis and summarization

### 3. Orchestrator Agent (`orchestrator-agent.md`)

**Use for**: Coordinating multiple agents in complex workflows.

**Complexity**: High

**Examples**:
- Workflow coordinator
- Project manager agent
- Multi-agent dispatcher
- Quality assurance orchestrator

**Key Features**:
- Agent routing logic
- Dependency management
- Error handling
- Result aggregation

## Quick Start

### Creating a Specialist Agent

```bash
# 1. Copy template
cp .claude/templates/agents/specialist-agent.md .claude/agents/tax-specialist.md

# 2. Customize domain expertise
# Replace {DOMAIN} with "international-tax"
# Replace {DESCRIPTION} with "Tax optimization for expats"

# 3. Configure tools
# Add: WebSearch, Read, Bash

# 4. Define input/output formats
# Input: User financial profile
# Output: Tax optimization report
```

### Creating a Research Agent

```bash
# 1. Copy template
cp .claude/templates/agents/research-agent.md .claude/agents/market-researcher.md

# 2. Define research domains
# Replace {DOMAIN} with "market-analysis"

# 3. Configure validation logic
# Add multi-source validation rules
# Define confidence scoring criteria

# 4. Set up output format
# Executive summary + detailed findings + sources
```

### Creating an Orchestrator Agent

```bash
# 1. Copy template
cp .claude/templates/agents/orchestrator-agent.md .claude/agents/workflow-coordinator.md

# 2. Define agent routing
# Map user inputs to specialist agents

# 3. Configure dependencies
# Define which agents depend on others

# 4. Set up aggregation
# Define how to combine agent outputs
```

## Best Practices

### 1. Clear Domain Boundaries
Each specialist agent should have a well-defined domain. Avoid overlapping responsibilities.

### 2. Structured I/O
Define explicit input and output formats. Use JSON for complex data, Markdown for reports.

### 3. Tool Access
Only grant tools necessary for the agent's domain. Reduce complexity and potential errors.

### 4. Quality Validation
Agents should self-validate their outputs before returning results.

### 5. Error Handling
Define fallback behavior when agents encounter errors or missing data.

### 6. Dependency Management
For orchestrators, explicitly track dependencies between agents.

## Integration Patterns

### Pattern 1: Sequential Execution

```
Orchestrator → Agent A → Agent B → Agent C → Report
```

Use when agents have strict dependencies.

### Pattern 2: Parallel Execution

```
Orchestrator → [Agent A, Agent B, Agent C] → Aggregator → Report
```

Use when agents are independent. Dramatically faster.

### Pattern 3: Conditional Routing

```
Orchestrator → Profile Analysis →
  IF condition1 → Agent A
  IF condition2 → Agent B
  ELSE → Agent C
→ Report
```

Use when different profiles need different agents.

### Pattern 4: Hierarchical Orchestration

```
Master Orchestrator →
  Sub-Orchestrator 1 → [Agent A, Agent B]
  Sub-Orchestrator 2 → [Agent C, Agent D]
→ Master Report
```

Use for very complex systems (20+ agents).

## Example: Large Multi-Agent System (29-Agent)

**Orchestration**: Profile-based agent selection
- Profile Analysis: Determines which agents to run
- 29 Specialists: Domain-specific experts
- Reporter: Aggregates all outputs

**Performance**: 70% faster than sequential (8-12min → 45sec)

**Pattern**: Conditional routing + parallel execution

## Troubleshooting

### Agent Not Producing Expected Output?

**Check output format**: Verify the agent's output matches expected structure.

**Check tools**: Ensure agent has access to required tools.

**Check validation**: Review self-validation logic.

### Agents Producing Conflicting Results?

**Check domain boundaries**: Ensure agents have clear, non-overlapping domains.

**Add conflict resolution**: Orchestrator should handle conflicts.

**Review priorities**: Define priority hierarchy for conflicting recommendations.

### Orchestration Too Slow?

**Maximize parallelization**: Run independent agents simultaneously.

**Profile-based selection**: Don't run unnecessary agents.

**Optimize critical path**: Identify and optimize slowest dependencies.

## Advanced Topics

### Agent Memory
Agents can maintain state across executions using file storage or databases.

### Agent Communication
Agents can pass structured data to each other via the orchestrator.

### Dynamic Agent Selection
Orchestrators can decide which agents to run based on runtime conditions.

### Quality Scoring
Agents can score their own output confidence for weighted aggregation.

## Related Patterns

- **Multi-Agent Orchestration**: See `knowledge/patterns/multi-agent-orchestration.md`
- **Agent Prompts**: See `knowledge/prompts/patterns/` for agent examples
- **Progressive Disclosure**: For complex agents, use progressive skill pattern

---

**Navigation**: [← Templates](./../README.md)
