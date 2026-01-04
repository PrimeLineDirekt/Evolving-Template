---
title: "Tools Reference Index"
type: reference
category: index
domain: [tools, skills, mcp, agents]
source: multiple
source_date: 2025-12-13
completeness: complete
tags: [tools, index, reference, skills, mcp, agents]
---

# Tools Reference Index

Comprehensive reference library for Claude Code tools, skills, and integrations.

---

## Quick Navigation

| Category | Description | Count |
|----------|-------------|-------|
| [Claude Skills](#claude-skills) | obra/superpowers methodology skills | 19 |
| [MCP Servers](#mcp-servers) | Model Context Protocol integrations | 12+ |
| [Agent Templates](#agent-templates) | Reusable agent patterns | 3 types |
| [Claude-Flow](#claude-flow) | Multi-agent coordination patterns | 3 modes |
| [Document Skills](#document-skills) | Office document generation | 4 |

---

## Claude Skills

**Location**: `claude-skills/`
**Source**: obra/superpowers

Battle-tested skills for systematic development.

### Complete References

| Skill | Purpose |
|-------|---------|
| [systematic-debugging](claude-skills/systematic-debugging.md) | 4-Phase Root Cause Analysis |
| [test-driven-development](claude-skills/test-driven-development.md) | RED-GREEN-REFACTOR |
| [brainstorming](claude-skills/brainstorming.md) | Interactive Design Refinement |
| [writing-and-executing-plans](claude-skills/writing-and-executing-plans.md) | Plan Creation & Batch Execution |

### Skill Categories

| Category | Skills | Focus |
|----------|--------|-------|
| Testing | TDD, condition-based-waiting, anti-patterns | Quality |
| Debugging | systematic, root-cause, verification | Problem-solving |
| Collaboration | brainstorming, code-review, pair-programming | Teamwork |
| Git | worktrees, branch-completion | Version control |
| Planning | writing-plans, executing-plans, parallel-agents | Execution |

→ [Full Index](claude-skills/index.md)

---

## MCP Servers

**Location**: `mcp-servers/`
**Source**: modelcontextprotocol/servers

External tool integrations via Model Context Protocol.

### Priority Servers

| Server | Purpose | Status |
|--------|---------|--------|
| github | GitHub API | Configured |
| sequential-thinking | Structured reasoning | Configured |
| filesystem | Enhanced file ops | Available |
| fetch | Web content | Available |
| memory | Persistent knowledge | Available |

### Configuration

```json
// .mcp.json
{
  "mcpServers": {
    "server-name": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-name"]
    }
  }
}
```

→ [Full Reference](mcp-servers/index.md)

---

## Agent Templates

**Location**: `agent-templates/`
**Source**: VoltAgent, obra/superpowers, 12-Factor-Agents

Reusable patterns for building agents.

### Template Types

| Type | Purpose | Use Case |
|------|---------|----------|
| Specialist | Domain-focused expertise | API, Security, Testing |
| Orchestrator | Multi-agent coordination | Complex workflows |
| Research | Information gathering | Analysis, research |

### Core Components

```typescript
abstract class BaseAgent<TInput, TOutput> {
  validateInput(input: TInput): ValidationResult;
  execute(input: TInput): Promise<AgentOutput<TOutput>>;
  parseOutput(response: string): TOutput;
}
```

→ [Mega-Template](agent-templates/mega-template.md)

---

## Claude-Flow

**Location**: `claude-flow/`
**Source**: ruvnet/claude-flow

Enterprise multi-agent orchestration patterns.

### Coordination Modes

| Mode | Duration | Use Case |
|------|----------|----------|
| Swarm | Temporary | Quick tasks |
| Hive-Mind | Persistent | Complex projects |
| Pipeline | Sequential | Ordered workflows |

### Topology Patterns

| Pattern | Structure | Resilience |
|---------|-----------|------------|
| Hierarchical | Queen → Workers | Low |
| Mesh | Peer-to-peer | High |
| Adaptive | Dynamic | Variable |

### Memory Systems

| System | Performance | Use Case |
|--------|-------------|----------|
| AgentDB | 96x-164x faster | Semantic search |
| ReasoningBank | 2-3ms latency | Simple queries |
| Hybrid | Best of both | Production |

→ [Full Reference](claude-flow/index.md)

---

## Document Skills

**Location**: `document-skills/`
**Source**: anthropic-cookbook/skills

Office document generation capabilities.

### Available Skills

| Skill | Output | Capabilities |
|-------|--------|--------------|
| xlsx | Excel | Formulas, charts, tables |
| pptx | PowerPoint | Slides, themes, notes |
| pdf | PDF | Reports, formatting |
| docx | Word | Documents, styles |

### Invocation

```
@xlsx Create budget tracker
@pptx Create pitch deck
@pdf Create report
@docx Create proposal
```

→ [Full Reference](document-skills/index.md)

---

## Integration Map

```
┌─────────────────────────────────────────────────────────┐
│                    Claude Code                           │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐      │
│  │ Claude      │  │ Agent       │  │ Document    │      │
│  │ Skills      │  │ Templates   │  │ Skills      │      │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘      │
│         │                │                │              │
│         └────────────────┼────────────────┘              │
│                          │                               │
│                    ┌─────┴─────┐                        │
│                    │ Claude-   │                        │
│                    │ Flow      │                        │
│                    └─────┬─────┘                        │
│                          │                               │
│                    ┌─────┴─────┐                        │
│                    │ MCP       │                        │
│                    │ Servers   │                        │
│                    └───────────┘                        │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

---

## Usage Patterns

### Single Task

```
1. Identify task type
2. Select appropriate skill/template
3. Execute with structured input
4. Validate output
```

### Multi-Agent Workflow

```
1. Decompose into subtasks
2. Select coordination mode (Swarm/Hive-Mind/Pipeline)
3. Assign agents per subtask
4. Coordinate via topology pattern
5. Aggregate results
```

### Document Generation

```
1. Gather content/data
2. Select document type
3. Invoke document skill
4. Review and refine output
```

---

## Related

- [Knowledge Base Index](../../index.md)
- [Patterns](../../patterns/README.md)
- [Learnings](../../learnings/README.md)

---

**Last Updated**: 2025-12-13
