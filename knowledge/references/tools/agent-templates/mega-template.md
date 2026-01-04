---
title: "Agent Mega-Template"
type: reference
category: agent-template
domain: [agents, templates, architecture, best-practices]
source: VoltAgent + obra/superpowers + Evolving + 12-Factor-Agents
source_date: 2025-12-13
completeness: complete
tags: [agent, template, specialist, orchestrator, best-practices]
---

# Agent Mega-Template

## TL;DR

Universal agent template combining VoltAgent patterns, obra/superpowers skills, 12-Factor-Agents principles, and Evolving best practices. Covers Specialist, Orchestrator, and Research agent types with full implementation code.

---

## Agent Types Overview

| Type | Purpose | State | Coordination |
|------|---------|-------|--------------|
| **Specialist** | Single domain expertise | Stateless | Called by others |
| **Orchestrator** | Coordinate multiple agents | Manages flow | Controls specialists |
| **Research** | Multi-source information | Aggregates data | Confidence scoring |

---

# Part 1: Specialist Agent Template

## When to Use

- Single, well-defined domain
- Reusable across contexts
- No need to coordinate other agents
- Clear input/output contract

## Template Structure

```markdown
---
agent: {domain}-specialist-agent
type: specialist
domain: [{primary-domain}, {secondary-domain}]
version: 1.0
dependencies: []
---

# {Domain} Specialist Agent

## Identity
You are a specialist agent focused exclusively on {domain}. You have deep expertise
in {specific-expertise} and follow established best practices.

## Core Capabilities
1. [Primary capability]
2. [Secondary capability]
3. [Tertiary capability]

## Input Contract
You receive:
- `task`: The specific task to accomplish
- `context`: Relevant background information
- `constraints`: Any limitations to respect

## Output Contract
You return:
```json
{
  "success": boolean,
  "result": {
    // Domain-specific output
  },
  "confidence": 0.0-1.0,
  "reasoning": "Brief explanation",
  "metadata": {
    "tokens_used": number,
    "duration_ms": number
  }
}
```

## Methodology
1. [First step of your approach]
2. [Second step]
3. [Third step]
4. [Verification step]

## Constraints
- [What you will NOT do]
- [Boundaries of your domain]
- [When to escalate]

## Error Handling
If you encounter:
- Missing information: Request clarification
- Out of domain: Return with `success: false` and explain
- Uncertainty: Include in confidence score

## Quality Checklist
- [ ] Output matches contract
- [ ] Confidence score is accurate
- [ ] Reasoning is clear
- [ ] No hallucinated information
```

## Implementation (TypeScript)

```typescript
// agents/specialist.ts
import Anthropic from "@anthropic-ai/sdk";

interface AgentInput {
  task: string;
  context?: Record<string, any>;
  constraints?: string[];
}

interface AgentOutput<T> {
  success: boolean;
  result?: T;
  confidence: number;
  reasoning: string;
  metadata: {
    tokens_used: number;
    duration_ms: number;
    model: string;
  };
  error?: string;
}

abstract class SpecialistAgent<TInput extends AgentInput, TOutput> {
  protected client: Anthropic;
  protected model: string;
  protected systemPrompt: string;

  constructor(config: {
    model?: string;
    systemPrompt: string;
  }) {
    this.client = new Anthropic();
    this.model = config.model || "claude-sonnet-4-20250514";
    this.systemPrompt = config.systemPrompt;
  }

  abstract validateInput(input: TInput): { valid: boolean; errors: string[] };
  abstract parseOutput(response: string): TOutput;

  async execute(input: TInput): Promise<AgentOutput<TOutput>> {
    const startTime = Date.now();

    // Validate input
    const validation = this.validateInput(input);
    if (!validation.valid) {
      return {
        success: false,
        confidence: 1.0,
        reasoning: "Input validation failed",
        error: validation.errors.join(", "),
        metadata: {
          tokens_used: 0,
          duration_ms: Date.now() - startTime,
          model: this.model,
        },
      };
    }

    try {
      const response = await this.client.messages.create({
        model: this.model,
        max_tokens: 4096,
        system: this.systemPrompt,
        messages: [
          {
            role: "user",
            content: this.formatPrompt(input),
          },
        ],
      });

      const content = response.content[0];
      if (content.type !== "text") {
        throw new Error("Unexpected response type");
      }

      const result = this.parseOutput(content.text);

      return {
        success: true,
        result,
        confidence: this.calculateConfidence(result),
        reasoning: this.extractReasoning(content.text),
        metadata: {
          tokens_used: response.usage.input_tokens + response.usage.output_tokens,
          duration_ms: Date.now() - startTime,
          model: this.model,
        },
      };
    } catch (error) {
      return {
        success: false,
        confidence: 0,
        reasoning: "Execution failed",
        error: (error as Error).message,
        metadata: {
          tokens_used: 0,
          duration_ms: Date.now() - startTime,
          model: this.model,
        },
      };
    }
  }

  protected abstract formatPrompt(input: TInput): string;
  protected abstract calculateConfidence(result: TOutput): number;
  protected abstract extractReasoning(response: string): string;
}
```

## Example: Code Review Specialist

```typescript
// agents/code-review-specialist.ts
interface CodeReviewInput extends AgentInput {
  code: string;
  language: string;
  focus?: ("security" | "performance" | "readability" | "all")[];
}

interface CodeReviewResult {
  issues: {
    severity: "critical" | "major" | "minor";
    line?: number;
    message: string;
    suggestion?: string;
  }[];
  summary: string;
  score: number;
}

class CodeReviewSpecialist extends SpecialistAgent<CodeReviewInput, CodeReviewResult> {
  constructor() {
    super({
      model: "claude-sonnet-4-20250514",
      systemPrompt: `You are a code review specialist. You analyze code for:
- Security vulnerabilities
- Performance issues
- Readability problems
- Best practice violations

Return your analysis as JSON with this structure:
{
  "issues": [{ "severity": "critical|major|minor", "line": number, "message": "...", "suggestion": "..." }],
  "summary": "Brief overall assessment",
  "score": 1-10
}

Be specific and actionable. Don't invent issues that don't exist.`,
    });
  }

  validateInput(input: CodeReviewInput) {
    const errors: string[] = [];
    if (!input.code || input.code.length < 10) {
      errors.push("Code must be at least 10 characters");
    }
    if (!input.language) {
      errors.push("Language must be specified");
    }
    return { valid: errors.length === 0, errors };
  }

  formatPrompt(input: CodeReviewInput): string {
    return `Review this ${input.language} code:

\`\`\`${input.language}
${input.code}
\`\`\`

Focus areas: ${input.focus?.join(", ") || "all"}
${input.constraints?.length ? `Constraints: ${input.constraints.join(", ")}` : ""}`;
  }

  parseOutput(response: string): CodeReviewResult {
    const jsonMatch = response.match(/\{[\s\S]*\}/);
    if (!jsonMatch) throw new Error("No JSON in response");
    return JSON.parse(jsonMatch[0]);
  }

  calculateConfidence(result: CodeReviewResult): number {
    // Higher confidence if issues are well-documented
    const issueQuality = result.issues.every((i) => i.message && i.severity) ? 0.3 : 0;
    const hasSpecifics = result.issues.some((i) => i.line) ? 0.2 : 0;
    const baseConfidence = 0.5;
    return Math.min(1.0, baseConfidence + issueQuality + hasSpecifics);
  }

  extractReasoning(response: string): string {
    const parsed = JSON.parse(response.match(/\{[\s\S]*\}/)?.[0] || "{}");
    return parsed.summary || "Code review completed";
  }
}
```

---

# Part 2: Orchestrator Agent Template

## When to Use

- Coordinate multiple specialist agents
- Complex multi-step workflows
- Need to synthesize results from multiple sources
- Error recovery and fallback handling

## Template Structure

```markdown
---
agent: {domain}-orchestrator-agent
type: orchestrator
domain: [{workflow-domain}]
version: 1.0
dependencies:
  - specialist-agent-1
  - specialist-agent-2
  - specialist-agent-3
---

# {Domain} Orchestrator Agent

## Identity
You are an orchestrator agent that coordinates multiple specialists to accomplish
complex {domain} tasks. You decompose tasks, delegate to appropriate specialists,
and synthesize their outputs into coherent results.

## Available Specialists
1. **{Specialist 1}**: [capabilities]
2. **{Specialist 2}**: [capabilities]
3. **{Specialist 3}**: [capabilities]

## Orchestration Patterns
- Sequential: A → B → C
- Parallel: [A, B, C] → Merge
- Conditional: IF condition THEN A ELSE B
- Retry: On failure, retry with backoff

## Workflow
1. Analyze incoming task
2. Decompose into subtasks
3. Assign to appropriate specialists
4. Monitor execution
5. Handle failures with fallbacks
6. Synthesize final result

## Error Handling
- Specialist failure: Try alternate specialist or degrade gracefully
- Timeout: Return partial results with explanation
- Invalid input: Request clarification

## Output Contract
```json
{
  "success": boolean,
  "result": {
    "synthesized_output": any,
    "specialist_results": [
      { "agent": "name", "success": boolean, "output": any }
    ]
  },
  "workflow": {
    "steps_completed": number,
    "steps_total": number,
    "execution_path": ["step1", "step2", ...]
  }
}
```
```

## Implementation (TypeScript)

```typescript
// agents/orchestrator.ts
interface WorkflowStep {
  id: string;
  agent: string;
  input: any;
  dependsOn?: string[];
  optional?: boolean;
  fallback?: string;
}

interface WorkflowResult {
  success: boolean;
  result: {
    synthesized_output: any;
    specialist_results: Array<{
      stepId: string;
      agent: string;
      success: boolean;
      output: any;
      duration_ms: number;
    }>;
  };
  workflow: {
    steps_completed: number;
    steps_total: number;
    execution_path: string[];
  };
}

class OrchestratorAgent {
  private specialists: Map<string, SpecialistAgent<any, any>>;
  private maxRetries: number = 3;
  private timeout: number = 30000;

  constructor(specialists: Record<string, SpecialistAgent<any, any>>) {
    this.specialists = new Map(Object.entries(specialists));
  }

  async executeWorkflow(steps: WorkflowStep[]): Promise<WorkflowResult> {
    const results: WorkflowResult["result"]["specialist_results"] = [];
    const executionPath: string[] = [];
    const completedSteps = new Map<string, any>();

    // Build dependency graph
    const dependencyGraph = this.buildDependencyGraph(steps);

    // Execute steps respecting dependencies
    for (const step of this.topologicalSort(dependencyGraph)) {
      executionPath.push(step.id);

      // Check if dependencies are met
      if (step.dependsOn) {
        const unmetDeps = step.dependsOn.filter(
          (dep) => !completedSteps.has(dep)
        );
        if (unmetDeps.length > 0) {
          if (step.optional) {
            continue;
          }
          throw new Error(`Unmet dependencies: ${unmetDeps.join(", ")}`);
        }
      }

      // Build input with dependency outputs
      const enrichedInput = this.enrichInputWithDependencies(
        step.input,
        step.dependsOn,
        completedSteps
      );

      // Execute with retry logic
      const result = await this.executeWithRetry(step, enrichedInput);

      results.push({
        stepId: step.id,
        agent: step.agent,
        success: result.success,
        output: result.result,
        duration_ms: result.metadata.duration_ms,
      });

      if (result.success) {
        completedSteps.set(step.id, result.result);
      } else if (!step.optional) {
        // Try fallback if available
        if (step.fallback) {
          const fallbackResult = await this.executeFallback(
            step.fallback,
            enrichedInput
          );
          if (fallbackResult.success) {
            completedSteps.set(step.id, fallbackResult.result);
            continue;
          }
        }
        // Non-optional step failed without successful fallback
        break;
      }
    }

    return {
      success:
        completedSteps.size ===
        steps.filter((s) => !s.optional).length,
      result: {
        synthesized_output: this.synthesize(completedSteps),
        specialist_results: results,
      },
      workflow: {
        steps_completed: completedSteps.size,
        steps_total: steps.length,
        execution_path: executionPath,
      },
    };
  }

  private async executeWithRetry(
    step: WorkflowStep,
    input: any
  ): Promise<AgentOutput<any>> {
    const specialist = this.specialists.get(step.agent);
    if (!specialist) {
      throw new Error(`Unknown specialist: ${step.agent}`);
    }

    let lastError: Error | undefined;
    for (let attempt = 1; attempt <= this.maxRetries; attempt++) {
      try {
        const result = await Promise.race([
          specialist.execute({ ...input, task: input.task || step.id }),
          this.timeoutPromise(),
        ]);
        if (result.success) return result;
        lastError = new Error(result.error || "Unknown error");
      } catch (error) {
        lastError = error as Error;
      }

      // Exponential backoff
      if (attempt < this.maxRetries) {
        await this.delay(Math.pow(2, attempt) * 100);
      }
    }

    return {
      success: false,
      confidence: 0,
      reasoning: `Failed after ${this.maxRetries} attempts`,
      error: lastError?.message,
      metadata: { tokens_used: 0, duration_ms: 0, model: "unknown" },
    };
  }

  private synthesize(results: Map<string, any>): any {
    // Override in subclass for domain-specific synthesis
    return Object.fromEntries(results);
  }

  private timeoutPromise(): Promise<never> {
    return new Promise((_, reject) =>
      setTimeout(() => reject(new Error("Timeout")), this.timeout)
    );
  }

  private delay(ms: number): Promise<void> {
    return new Promise((resolve) => setTimeout(resolve, ms));
  }

  // ... other helper methods
}
```

---

# Part 3: Research Agent Template

## When to Use

- Gather information from multiple sources
- Need confidence scoring
- Cross-reference and validate findings
- Synthesize coherent summary

## Template Structure

```markdown
---
agent: {domain}-research-agent
type: research
domain: [{research-domain}]
version: 1.0
sources:
  - knowledge-base
  - web-search
  - document-analysis
---

# {Domain} Research Agent

## Identity
You are a research agent specializing in {domain}. You gather information from
multiple sources, cross-reference findings, and provide confidence-scored summaries.

## Source Types
1. **Primary**: Direct, authoritative sources
2. **Secondary**: Indirect but reliable sources
3. **Tertiary**: Supporting evidence

## Confidence Scoring
| Source Type | Weight |
|-------------|--------|
| Primary verified | 1.0 |
| Primary unverified | 0.8 |
| Secondary verified | 0.7 |
| Secondary unverified | 0.5 |
| Tertiary | 0.3 |

## Output Contract
```json
{
  "findings": [
    {
      "claim": "The finding",
      "confidence": 0.0-1.0,
      "sources": ["source1", "source2"],
      "source_types": ["primary", "secondary"]
    }
  ],
  "summary": "Synthesized conclusion",
  "overall_confidence": 0.0-1.0,
  "gaps": ["What couldn't be determined"],
  "recommendations": ["Next steps"]
}
```

## Methodology
1. Define research question
2. Identify relevant sources
3. Gather information
4. Cross-reference findings
5. Score confidence
6. Synthesize summary
7. Identify gaps
```

## Implementation

```typescript
// agents/research-agent.ts
interface ResearchInput {
  question: string;
  context?: string;
  sources?: ("kb" | "web" | "docs")[];
  maxSources?: number;
}

interface Finding {
  claim: string;
  confidence: number;
  sources: string[];
  source_types: ("primary" | "secondary" | "tertiary")[];
  evidence: string;
}

interface ResearchOutput {
  findings: Finding[];
  summary: string;
  overall_confidence: number;
  gaps: string[];
  recommendations: string[];
}

class ResearchAgent {
  private sourceWeights = {
    primary_verified: 1.0,
    primary_unverified: 0.8,
    secondary_verified: 0.7,
    secondary_unverified: 0.5,
    tertiary: 0.3,
  };

  async research(input: ResearchInput): Promise<AgentOutput<ResearchOutput>> {
    const findings: Finding[] = [];

    // 1. Gather from all sources
    const sourcesToUse = input.sources || ["kb", "web", "docs"];

    for (const source of sourcesToUse) {
      const sourceFindings = await this.gatherFromSource(
        input.question,
        source
      );
      findings.push(...sourceFindings);
    }

    // 2. Cross-reference and deduplicate
    const crossReferenced = this.crossReference(findings);

    // 3. Calculate overall confidence
    const overallConfidence = this.calculateOverallConfidence(crossReferenced);

    // 4. Synthesize summary
    const summary = await this.synthesize(crossReferenced, input.question);

    // 5. Identify gaps
    const gaps = this.identifyGaps(crossReferenced, input.question);

    return {
      success: true,
      result: {
        findings: crossReferenced,
        summary,
        overall_confidence: overallConfidence,
        gaps,
        recommendations: this.generateRecommendations(gaps),
      },
      confidence: overallConfidence,
      reasoning: `Found ${crossReferenced.length} findings from ${sourcesToUse.length} sources`,
      metadata: {
        tokens_used: 0, // Track in actual implementation
        duration_ms: 0,
        model: "claude-sonnet-4-20250514",
      },
    };
  }

  private crossReference(findings: Finding[]): Finding[] {
    // Group similar findings
    const grouped = new Map<string, Finding[]>();

    for (const finding of findings) {
      const key = this.normalizeClaimForGrouping(finding.claim);
      if (!grouped.has(key)) {
        grouped.set(key, []);
      }
      grouped.get(key)!.push(finding);
    }

    // Merge grouped findings with boosted confidence
    return Array.from(grouped.values()).map((group) => {
      if (group.length === 1) return group[0];

      // Multiple sources agree - boost confidence
      const mergedConfidence = Math.min(
        1.0,
        group.reduce((sum, f) => sum + f.confidence, 0) / group.length + 0.1
      );

      return {
        claim: group[0].claim,
        confidence: mergedConfidence,
        sources: group.flatMap((f) => f.sources),
        source_types: [...new Set(group.flatMap((f) => f.source_types))],
        evidence: group.map((f) => f.evidence).join(" | "),
      };
    });
  }

  private calculateOverallConfidence(findings: Finding[]): number {
    if (findings.length === 0) return 0;

    // Weight by individual confidence
    const totalWeight = findings.reduce((sum, f) => sum + f.confidence, 0);
    return totalWeight / findings.length;
  }

  // ... other methods
}
```

---

# Part 4: Best Practices Checklist

## From 12-Factor Agents

```markdown
## 12-Factor Agent Checklist

### 1. Natural Language Outputs
- [ ] Agent writes human-readable outputs
- [ ] Other agents can understand without parsing

### 2. Context Window Ownership
- [ ] Agent owns its context window
- [ ] External systems don't manage agent memory

### 3. Compact Errors
- [ ] Error messages are token-efficient
- [ ] Include actionable information
- [ ] No stack traces in prompts

### 4. Deterministic Tools
- [ ] Tools have predictable behavior
- [ ] Same input = same output
- [ ] No hidden state changes

### 5. Unified Context
- [ ] All relevant info in context
- [ ] No hidden knowledge required
- [ ] Self-contained execution

### 6. Own Your Prompts
- [ ] System prompts are explicit
- [ ] Not relying on provider defaults
- [ ] Version controlled

### 7. Expect Small Models
- [ ] Works with smaller models
- [ ] Doesn't require largest model
- [ ] Graceful degradation

### 8. Control Execution Flow
- [ ] Human checkpoints when needed
- [ ] Clear approval gates
- [ ] Reversible actions

### 9. Fail Fast
- [ ] Validate inputs early
- [ ] Clear error messages
- [ ] Don't proceed with bad data

### 10. Emit Machine-Readable Logs
- [ ] Structured logging
- [ ] Traceable execution
- [ ] Queryable events

### 11. Separate I/O from Logic
- [ ] Pure business logic
- [ ] Testable without I/O
- [ ] Dependency injection

### 12. Configure via Environment
- [ ] Model via env vars
- [ ] API keys via env
- [ ] No hardcoded config
```

## From obra/superpowers

```markdown
## Superpowers Integration Checklist

### Methodology Integration
- [ ] Use systematic-debugging for error investigation
- [ ] Use TDD for test-first development
- [ ] Use brainstorming for design phases
- [ ] Use writing-plans for implementation planning

### Quality Gates
- [ ] Verification before completion
- [ ] Defense in depth validation
- [ ] Code review before merge
```

---

## Quick Start: Create New Agent

```bash
# 1. Copy template
cp templates/specialist-template.md agents/my-domain-agent.md

# 2. Customize
# - Update agent name and domain
# - Define capabilities
# - Specify input/output contracts
# - Add methodology

# 3. Implement
# - Create TypeScript class extending SpecialistAgent
# - Implement abstract methods
# - Add tests

# 4. Register
# - Add to agent registry
# - Update orchestrator if needed
# - Document in index
```

---

**Source:** VoltAgent + obra/superpowers + 12-Factor-Agents + Evolving
**Navigation:** [← Agent Templates](index.md) | [← References](../../index.md)
