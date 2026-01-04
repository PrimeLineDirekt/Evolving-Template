---
title: "Claude-Flow Coordination Patterns"
type: reference
category: orchestration
domain: [multi-agent, swarm, coordination, patterns]
source: ruvnet/claude-flow
source_date: 2025-12-13
completeness: complete
tags: [swarm, hive-mind, pipeline, topology, coordination, multi-agent]
---

# Claude-Flow Coordination Patterns

Enterprise-grade multi-agent orchestration patterns from claude-flow v2.7.0.

## TL;DR

Three coordination modes for different scales: **Swarm** (quick tasks), **Hive-Mind** (complex projects), **Pipeline** (sequential workflows). Choose topology based on fault tolerance needs: Hierarchical (simple), Mesh (resilient), Adaptive (dynamic).

---

## Coordination Modes

### Swarm Mode

**Purpose**: Quick task execution without setup overhead.

**When to Use**:
- Single focused objective
- Immediate needs
- Short-lived tasks (minutes to hours)
- No cross-session persistence needed

**Characteristics**:
- Instant activation
- Temporary context
- Task-focused agents
- Minimal coordination overhead

**Example Use Cases**:
- Build an API endpoint
- Implement a feature
- Fix a bug
- Run analysis

**Implementation Pattern**:
```typescript
interface SwarmConfig {
  objective: string;
  maxAgents: number;
  topology: 'hierarchical' | 'mesh';
  timeout?: number;
}

async function executeSwarm(config: SwarmConfig): Promise<SwarmResult> {
  // 1. Parse objective into subtasks
  const subtasks = await decomposeObjective(config.objective);

  // 2. Spawn specialized agents
  const agents = await spawnAgents(subtasks, config.maxAgents);

  // 3. Coordinate execution
  const results = await coordinateExecution(agents, config.topology);

  // 4. Aggregate results
  return aggregateResults(results);
}
```

**Evolving Integration**:
- Use for `/analyze-repo` parallel analysis
- Multi-file code generation
- Parallel research tasks

---

### Hive-Mind Mode

**Purpose**: Complex project coordination with persistent context.

**When to Use**:
- Multi-session projects
- Cross-domain complexity
- Shared knowledge required
- Long-running initiatives

**Characteristics**:
- Interactive setup wizard
- SQLite-backed memory
- Session resumption
- Project-wide context

**Example Use Cases**:
- Feature development across files
- Refactoring projects
- Documentation overhauls
- System migrations

**Implementation Pattern**:
```typescript
interface HiveMindConfig {
  projectId: string;
  domains: string[];  // e.g., ['frontend', 'backend', 'testing']
  memoryPath: string;
  sessionId?: string; // For resumption
}

class HiveMind {
  private memory: SQLiteMemory;
  private agents: Map<string, DomainAgent>;

  async initialize(config: HiveMindConfig): Promise<void> {
    // 1. Load or create memory
    this.memory = await SQLiteMemory.open(config.memoryPath);

    // 2. Restore session if resuming
    if (config.sessionId) {
      await this.restoreSession(config.sessionId);
    }

    // 3. Spawn domain agents
    for (const domain of config.domains) {
      this.agents.set(domain, new DomainAgent(domain, this.memory));
    }
  }

  async executeTask(task: Task): Promise<TaskResult> {
    // 1. Determine relevant domains
    const domains = this.classifyTask(task);

    // 2. Gather context from memory
    const context = await this.memory.query(task.keywords);

    // 3. Coordinate domain agents
    const results = await this.coordinateDomains(domains, task, context);

    // 4. Update memory with learnings
    await this.memory.store(results.learnings);

    return results;
  }
}
```

**Memory Schema**:
```sql
-- Entities (projects, files, concepts)
CREATE TABLE entities (
  id TEXT PRIMARY KEY,
  type TEXT NOT NULL,
  name TEXT NOT NULL,
  observations TEXT,  -- JSON array
  created_at TIMESTAMP,
  updated_at TIMESTAMP
);

-- Relations (dependencies, references)
CREATE TABLE relations (
  from_id TEXT,
  to_id TEXT,
  relation_type TEXT,
  metadata TEXT,  -- JSON
  PRIMARY KEY (from_id, to_id, relation_type)
);

-- Session state
CREATE TABLE sessions (
  id TEXT PRIMARY KEY,
  state TEXT,  -- JSON
  created_at TIMESTAMP,
  resumed_at TIMESTAMP
);
```

---

### Pipeline Mode

**Purpose**: Sequential workflow execution with dependencies.

**When to Use**:
- Ordered operations required
- Stage dependencies exist
- Validation gates needed
- Audit trail required

**Characteristics**:
- Pre/post hooks
- Stage isolation
- Dependency management
- Rollback capability

**Example Use Cases**:
- CI/CD workflows
- Data processing pipelines
- Multi-stage analysis
- Content generation pipelines

**Implementation Pattern**:
```typescript
interface PipelineStage<TInput, TOutput> {
  name: string;
  execute: (input: TInput, context: PipelineContext) => Promise<TOutput>;
  validate?: (output: TOutput) => Promise<boolean>;
  rollback?: (input: TInput) => Promise<void>;
}

class Pipeline<T extends Record<string, any>> {
  private stages: PipelineStage<any, any>[] = [];
  private context: PipelineContext;

  addStage<TIn, TOut>(stage: PipelineStage<TIn, TOut>): this {
    this.stages.push(stage);
    return this;
  }

  async execute(input: T): Promise<PipelineResult<T>> {
    let current = input;
    const completed: string[] = [];

    for (const stage of this.stages) {
      try {
        // Pre-hook
        await this.context.hooks.pre(stage.name, current);

        // Execute
        const output = await stage.execute(current, this.context);

        // Validate
        if (stage.validate && !await stage.validate(output)) {
          throw new ValidationError(stage.name);
        }

        // Post-hook
        await this.context.hooks.post(stage.name, output);

        completed.push(stage.name);
        current = output;

      } catch (error) {
        // Rollback completed stages in reverse
        await this.rollback(completed.reverse());
        throw error;
      }
    }

    return { success: true, output: current };
  }
}
```

---

## Topology Patterns

### Hierarchical Topology

```
        ┌─────────┐
        │  Queen  │
        └────┬────┘
             │
    ┌────────┼────────┐
    │        │        │
┌───┴───┐┌───┴───┐┌───┴───┐
│Worker1││Worker2││Worker3│
└───────┘└───────┘└───────┘
```

**Characteristics**:
- Central coordinator (Queen)
- Clear command structure
- Simple routing
- Single point of failure

**When to Use**:
- Well-defined task breakdown
- Consistent subtask complexity
- Central decision-making needed

**Implementation**:
```typescript
class HierarchicalCoordinator {
  private workers: Worker[] = [];

  async distribute(task: Task): Promise<TaskResult[]> {
    // 1. Decompose task
    const subtasks = await this.decompose(task);

    // 2. Assign to workers
    const assignments = this.assignOptimally(subtasks, this.workers);

    // 3. Execute and collect
    const results = await Promise.all(
      assignments.map(({ worker, subtask }) =>
        worker.execute(subtask)
      )
    );

    // 4. Aggregate
    return this.aggregate(results);
  }
}
```

---

### Mesh Topology

```
┌───────┐     ┌───────┐
│Agent A│◄───►│Agent B│
└───┬───┘     └───┬───┘
    │             │
    │  ┌───────┐  │
    └─►│Agent C│◄─┘
       └───┬───┘
           │
       ┌───┴───┐
       │Agent D│
       └───────┘
```

**Characteristics**:
- Peer-to-peer communication
- No single point of failure
- Dynamic routing
- Higher complexity

**When to Use**:
- Fault tolerance required
- Agents need direct communication
- Distributed workloads
- Horizontal scaling

**Implementation**:
```typescript
interface MeshAgent {
  id: string;
  peers: Set<string>;

  broadcast(message: Message): Promise<void>;
  receive(message: Message): Promise<void>;
  findPeer(capability: string): MeshAgent | null;
}

class MeshCoordinator {
  private agents: Map<string, MeshAgent> = new Map();

  async executeDistributed(task: Task): Promise<TaskResult> {
    // 1. Find capable agents
    const capable = this.findCapable(task.requirements);

    // 2. Elect leader for this task
    const leader = await this.electLeader(capable);

    // 3. Leader coordinates execution
    return leader.coordinate(task, capable);
  }

  private async electLeader(candidates: MeshAgent[]): Promise<MeshAgent> {
    // Simple: lowest ID wins
    // Complex: Raft consensus
    return candidates.sort((a, b) => a.id.localeCompare(b.id))[0];
  }
}
```

---

### Adaptive Topology

**Characteristics**:
- Dynamic switching between patterns
- Load-aware routing
- Self-healing
- Optimal for variable workloads

**When to Use**:
- Unpredictable workload patterns
- Need both simple and complex coordination
- Self-optimization desired

**Implementation**:
```typescript
class AdaptiveCoordinator {
  private currentTopology: 'hierarchical' | 'mesh' = 'hierarchical';
  private metrics: MetricsCollector;

  async execute(task: Task): Promise<TaskResult> {
    // 1. Evaluate current state
    const loadLevel = await this.metrics.getLoadLevel();
    const failureRate = await this.metrics.getFailureRate();

    // 2. Decide topology
    this.currentTopology = this.selectTopology(loadLevel, failureRate);

    // 3. Execute with selected topology
    if (this.currentTopology === 'hierarchical') {
      return this.hierarchicalExecute(task);
    } else {
      return this.meshExecute(task);
    }
  }

  private selectTopology(load: number, failures: number): TopologyType {
    // High failures → mesh for resilience
    if (failures > 0.1) return 'mesh';

    // Low load → hierarchical for simplicity
    if (load < 0.5) return 'hierarchical';

    // High load → mesh for distribution
    return 'mesh';
  }
}
```

---

## Memory Systems

### AgentDB (Vector-Based)

**Performance**: 96x-164x faster than traditional search

**Features**:
- HNSW indexing for semantic search
- Quantization for efficiency
- Reflexion learning
- Causal reasoning

**When to Use**:
- Semantic similarity search
- Large knowledge bases
- Learning from past experiences

**Implementation Pattern**:
```typescript
interface AgentDBConfig {
  dimensions: number;  // Embedding size
  metric: 'cosine' | 'euclidean';
  efConstruction: number;  // Build-time accuracy
  efSearch: number;  // Query-time accuracy
}

class AgentDB {
  async store(key: string, embedding: number[], metadata: any): Promise<void>;
  async search(query: number[], k: number): Promise<SearchResult[]>;
  async learn(experience: Experience): Promise<void>;  // Reflexion
}
```

---

### ReasoningBank (SQLite-Based)

**Performance**: 2-3ms query latency

**Features**:
- Deterministic embeddings
- No API dependencies
- Namespace isolation
- Process restart survival

**When to Use**:
- Offline operation
- Exact matching needed
- Simple relationships
- Cost-sensitive

**Implementation Pattern**:
```typescript
class ReasoningBank {
  private db: SQLiteDatabase;

  async store(namespace: string, key: string, value: any): Promise<void> {
    await this.db.run(
      'INSERT OR REPLACE INTO reasoning (namespace, key, value) VALUES (?, ?, ?)',
      [namespace, key, JSON.stringify(value)]
    );
  }

  async query(namespace: string, pattern: string): Promise<any[]> {
    return this.db.all(
      'SELECT value FROM reasoning WHERE namespace = ? AND key LIKE ?',
      [namespace, pattern]
    );
  }
}
```

---

### Hybrid Memory

**Best of Both Worlds**:
```typescript
class HybridMemory {
  private agentDb: AgentDB;
  private reasoningBank: ReasoningBank;

  async query(input: string): Promise<MemoryResult[]> {
    // 1. Try semantic search first
    const semantic = await this.agentDb.search(
      await this.embed(input),
      5
    );

    // 2. Fall back to exact match if needed
    if (semantic.length === 0 || semantic[0].score < 0.7) {
      const exact = await this.reasoningBank.query('*', `%${input}%`);
      return exact;
    }

    return semantic;
  }
}
```

---

## Agent Coordination Patterns

### Queen-Led (Central Coordinator)

```typescript
class QueenCoordinator {
  private workers: Map<string, WorkerAgent> = new Map();

  async assignTask(task: Task): Promise<void> {
    // 1. Analyze task complexity
    const complexity = await this.analyzeComplexity(task);

    // 2. Select appropriate worker
    const worker = this.selectWorker(task.domain, complexity);

    // 3. Prepare context
    const context = await this.prepareContext(task);

    // 4. Dispatch
    await worker.execute({ task, context });
  }

  private selectWorker(domain: string, complexity: number): WorkerAgent {
    // Match domain expertise
    const domainWorkers = [...this.workers.values()]
      .filter(w => w.domains.includes(domain));

    // Select by current load and capability
    return domainWorkers
      .sort((a, b) => a.load - b.load)
      [0];
  }
}
```

---

### Consensus-Based (Distributed Decision)

```typescript
interface ConsensusResult {
  decision: string;
  confidence: number;
  votes: Map<string, string>;
}

class ConsensusCoordinator {
  private agents: Agent[];

  async decide(question: string): Promise<ConsensusResult> {
    // 1. Collect votes from all agents
    const votes = await Promise.all(
      this.agents.map(async agent => ({
        agentId: agent.id,
        vote: await agent.vote(question),
        confidence: await agent.getConfidence()
      }))
    );

    // 2. Weight by confidence
    const weighted = this.weightVotes(votes);

    // 3. Determine majority
    const decision = this.findMajority(weighted);

    return {
      decision: decision.choice,
      confidence: decision.totalWeight / votes.length,
      votes: new Map(votes.map(v => [v.agentId, v.vote]))
    };
  }
}
```

---

## Integration with Evolving

### Swarm for Analysis

```typescript
// Example: Parallel codebase analysis
const analysisSwarm = {
  objective: "Analyze codebase architecture",
  agents: [
    { type: 'structure-analyst', focus: 'directory-layout' },
    { type: 'dependency-analyst', focus: 'imports' },
    { type: 'pattern-analyst', focus: 'design-patterns' },
    { type: 'quality-analyst', focus: 'code-metrics' }
  ],
  aggregator: 'architecture-synthesizer'
};
```

### Hive-Mind for Projects

```typescript
// Example: Multi-session feature development
const featureHive = {
  projectId: '{PROJECT_ID}',
  domains: ['agents', 'orchestrator', 'knowledge-base'],
  memory: './project-memory.sqlite',
  sessionResumeEnabled: true
};
```

### Pipeline for Workflows

```typescript
// Example: Content generation pipeline
const contentPipeline = [
  { stage: 'research', agent: 'research-analyst' },
  { stage: 'outline', agent: 'content-planner' },
  { stage: 'generate', agent: 'content-writer' },
  { stage: 'refine', agent: 'editor' },
  { stage: 'optimize', agent: 'seo-specialist' }
];
```

---

## Quick Reference

### Mode Selection

| Need | Mode |
|------|------|
| Quick task | Swarm |
| Multi-session project | Hive-Mind |
| Ordered workflow | Pipeline |

### Topology Selection

| Need | Topology |
|------|----------|
| Simple coordination | Hierarchical |
| Fault tolerance | Mesh |
| Variable workload | Adaptive |

### Memory Selection

| Need | Memory |
|------|--------|
| Semantic search | AgentDB |
| Offline/simple | ReasoningBank |
| Best of both | Hybrid |

---

## Related

- [Agent Templates](../agent-templates/mega-template.md)
- [MCP Servers](../mcp-servers/index.md)
- [Claude Skills](../claude-skills/index.md)
- [Multi-Agent Orchestration Pattern](../../../../patterns/multi-agent-orchestration.md)

---

**Source**: ruvnet/claude-flow v2.7.0
**Last Updated**: 2025-12-13
