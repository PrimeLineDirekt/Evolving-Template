# Quality Orchestrator Agent Template

**Quelle**: ccplugins/ceo-quality-controller-agent (16KB)
**Abstrahiert**: 2025-12-29
**Status**: template

---

## Zweck

Template für Quality Control Orchestrator mit Dynamic Agent Discovery und Multi-Dimensional Assessment.

## Core Patterns (aus Original abstrahiert)

### 1. Dynamic Agent Discovery

```typescript
// Pattern: Discover available agents in project
const discoverAvailableAgents = async (): Promise<AgentCapability[]> => {
  const agentFiles = await scanDirectory('.claude/agents/');
  return agentFiles.map(parseAgentCapabilities);
};

// Pattern: Route task to optimal agent
const routeTaskToOptimalAgent = (task: Task, availableAgents: Agent[]): Agent => {
  const capabilityMatch = availableAgents.filter(agent =>
    agent.capabilities.some(cap => task.requiredCapabilities.includes(cap))
  );
  return selectBestMatch(capabilityMatch, task.priority, task.complexity);
};
```

### 2. Project Type Auto-Detection

Scan for project indicators:
- **Language**: package.json, Cargo.toml, pom.xml, requirements.txt
- **Framework**: Next.js, React, Django, Spring Boot
- **Architecture**: Monorepo, microservices, serverless
- **Testing**: Jest, Pytest, JUnit, Playwright
- **Build System**: npm, cargo, maven, gradle

### 3. Multi-Dimensional Quality Assessment

| Dimension | Focus Areas |
|-----------|-------------|
| **Code Quality** | Standards compliance, maintainability, complexity |
| **Security** | Vulnerabilities, secrets, dependencies |
| **Architecture** | Design patterns, scalability, maintainability |
| **Testing** | Coverage, effectiveness, automation |
| **Documentation** | Completeness, accuracy, standards |
| **Performance** | Optimization, resource usage, benchmarks |

### 4. Agent Chaining Patterns

```yaml
discovery_chain: |
  "First discover available agents,
   then analyze project structure,
   then route tasks to specialists,
   finally synthesize report"

validation_chain: |
  "First security scanning,
   then code review,
   then test validation,
   finally aggregate results"
```

### 5. Quality Assessment Output Format

```yaml
quality_assessment:
  status: APPROVED | REJECTED | REVISION_REQUIRED
  project_type: [detected_characteristics]
  validation_chain: [agents_used]
  quality_dimensions:
    - dimension: [category]
      score: [0-100]
      status: [passed|failed|warning]
      issues_found:
        - severity: [critical|high|medium|low]
          description: "Issue description"
          recommendation: "Fix suggestion"

  overall_quality_score: [0-100]
  deployment_ready: [true|false]
  next_actions:
    - agent: [optimal_agent]
      task: "Remediation task"
      priority: [critical|high|medium|low]
```

### 6. Quality Folder Structure

```
/QUALITY-CONTROL/
├── project-analysis/
│   ├── project-type-detection.md
│   ├── technology-stack-analysis.md
│   └── agent-capability-mapping.md
├── quality-reports/
│   ├── code-quality-assessment.md
│   ├── security-report.md
│   ├── testing-analysis.md
│   └── performance-analysis.md
├── validation-history/
│   ├── quality-gate-results.md
│   └── decision-rationale.md
└── deployment-readiness/
    ├── pre-deployment-checklist.md
    └── rollback-procedures.md
```

### 7. Adaptive Quality Thresholds

```typescript
const getQualityThresholds = (projectType: ProjectType) => {
  const baseThresholds = {
    security: { critical: 0, high: 0 },
    codeQuality: { maintainability: 80 },
    testing: { coverage: 75 },
    documentation: { completeness: 80 }
  };

  // Adjust based on project type
  if (projectType === 'financial_system') {
    return { ...baseThresholds, testing: { coverage: 95 }};
  }
  return baseThresholds;
};
```

## Placeholders

| Placeholder | Description |
|-------------|-------------|
| `{project_type}` | Detected project type |
| `{agents_available}` | List of discovered agents |
| `{quality_score}` | Overall quality score 0-100 |
| `{dimension}` | Quality dimension being assessed |

## Integration mit Evolving

- Nutzt `.claude/agents/` für Agent Discovery
- Quality Reports nach `knowledge/` oder dediziertem Ordner
- Kann als Orchestrator für Multi-Agent Scenarios dienen
- Integration mit Experience Memory für Quality Learnings
