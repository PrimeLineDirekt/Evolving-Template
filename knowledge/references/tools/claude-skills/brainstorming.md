---
title: "Brainstorming"
type: reference
category: claude-skill
domain: [collaboration, design, ideation]
source: obra/superpowers
source_date: 2025-12-13
completeness: complete
tags: [brainstorming, design, collaboration, socratic, ideation]
---

# Brainstorming

## TL;DR

Interactive design refinement using Socratic questioning. 3 Phases: Understand (clarify one question at a time) → Explore (present 2-3 approaches with trade-offs) → Design (validate incrementally in 200-300 word sections). YAGNI ruthlessly.

## When to Use

- Creative development phases
- New feature conceptualization
- Architecture decisions
- Problem exploration
- Design before implementation

**Not for:**
- Routine/mechanical tasks
- Clear requirements with obvious solutions
- Pure execution work

---

## Phase 1: Understanding

### Review Context First
```markdown
Before asking questions, review:
- [ ] Current project files and structure
- [ ] Recent commits and changes
- [ ] Existing documentation
- [ ] Related code/features
```

### Ask Clarifying Questions

**One question at a time** - Don't overwhelm with multiple questions.

**Prefer multiple choice when possible:**

```markdown
### Question 1: Target Users
Who is the primary user for this feature?

a) **End users** - Non-technical people using the product
b) **Developers** - People integrating with our API
c) **Admins** - Internal team managing the system
d) **All of the above** - Multiple user types
```

**Focus questions on:**
- Purpose and goals
- Constraints and limitations
- Success criteria
- User needs
- Technical boundaries

### Example Question Flow

```markdown
## Understanding Session

### Q1: Core Purpose
What problem does this feature solve?
→ [User answer]

### Q2: Success Criteria
How will we know it's working? Pick the most important:
a) Users complete task in under 30 seconds
b) Zero errors in production
c) 50% reduction in support tickets
d) Other: ___

→ [User answer]

### Q3: Constraints
What can't change?
a) Current database schema
b) Existing API contracts
c) UI framework
d) Nothing is off-limits

→ [User answer]

### Q4: Timeline Priority
What's most important?
a) Ship fast with minimal scope
b) Build it right, take more time
c) Balance both

→ [User answer]
```

---

## Phase 2: Exploration

### Present 2-3 Approaches

Always present options with trade-offs. Lead with recommendation.

```markdown
## Approach Options

### Option A: Simple Database Queue (Recommended)
**Description:** Store jobs in PostgreSQL, poll for new work
**Pros:**
- No new infrastructure
- Easy to debug and monitor
- Transactions with existing data

**Cons:**
- Polling has latency
- Scales to ~1000 jobs/min

**Best for:** Simple async needs, small-medium scale

---

### Option B: Redis-Based Queue
**Description:** Use Redis + Bull for job processing
**Pros:**
- Real-time processing
- Scales to 100k+ jobs/min
- Built-in retry/delay features

**Cons:**
- New infrastructure to manage
- Data not transactional with DB

**Best for:** High volume, real-time requirements

---

### Option C: Cloud Native (SQS/Cloud Tasks)
**Description:** Use managed queue service
**Pros:**
- Zero maintenance
- Infinite scale
- Built-in dead letter queues

**Cons:**
- Cloud lock-in
- Harder to test locally
- Additional costs

**Best for:** Cloud-native apps, variable workloads

---

## Recommendation
Option A is recommended because:
1. Matches your "ship fast" priority
2. No new infrastructure
3. Can migrate to B/C later if needed

Shall I detail Option A further?
```

### Explore Before Settling

Don't commit to first idea. Ask:
- "What if we did the opposite?"
- "What would Google/Stripe do?"
- "What's the simplest thing that could work?"
- "What would we regret in 6 months?"

---

## Phase 3: Design

### Present in 200-300 Word Sections

Validate incrementally - don't dump 2000 words at once.

```markdown
## Design: Simple Database Queue

### Section 1: Data Model

We'll add a `jobs` table:

```sql
CREATE TABLE jobs (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  type VARCHAR(50) NOT NULL,
  payload JSONB NOT NULL,
  status VARCHAR(20) DEFAULT 'pending',
  attempts INT DEFAULT 0,
  max_attempts INT DEFAULT 3,
  scheduled_at TIMESTAMP DEFAULT NOW(),
  started_at TIMESTAMP,
  completed_at TIMESTAMP,
  error TEXT,
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_jobs_pending ON jobs(scheduled_at)
  WHERE status = 'pending';
```

Job lifecycle: `pending → processing → completed/failed`

**Pause:** Does this data model work for your use case?
```

After confirmation, continue:

```markdown
### Section 2: Worker Process

The worker polls for jobs every second:

```typescript
async function pollJobs(): Promise<void> {
  const job = await db.query(`
    UPDATE jobs
    SET status = 'processing', started_at = NOW()
    WHERE id = (
      SELECT id FROM jobs
      WHERE status = 'pending'
        AND scheduled_at <= NOW()
      ORDER BY scheduled_at
      LIMIT 1
      FOR UPDATE SKIP LOCKED
    )
    RETURNING *
  `);

  if (job) {
    await processJob(job);
  }
}
```

The `FOR UPDATE SKIP LOCKED` prevents multiple workers from grabbing the same job.

**Pause:** Ready for error handling section?
```

### Cover These Topics

- Architecture overview
- Data model / schema
- Component interactions
- Error handling
- Testing strategy
- Migration path

---

## YAGNI Ruthlessly

**You Aren't Gonna Need It**

```markdown
## Feature Scope Check

### Requested Features
1. [x] Process jobs asynchronously
2. [x] Retry on failure (3 times)
3. [x] Basic monitoring

### Nice-to-haves (DEFER)
- [ ] Job priorities
- [ ] Job dependencies
- [ ] Distributed tracing
- [ ] Custom retry strategies
- [ ] Job batching

### Rationale
"Nice-to-haves" add 3x complexity for uncertain value.
Build minimal version first, add features when needed.
```

---

## Post-Design Actions

### 1. Document the Design

```markdown
# docs/plans/YYYY-MM-DD-feature-name-design.md

## Summary
One paragraph describing what we're building and why.

## Decision
Which approach we chose and key reasons.

## Design
- Data model
- Components
- Interactions
- Error handling

## Open Questions
- [Any unresolved items]

## Next Steps
1. [First implementation task]
2. [Second task]
```

### 2. Commit to Git

```bash
git add docs/plans/2025-01-15-job-queue-design.md
git commit -m "docs: Add job queue design document"
```

### 3. Transition to Implementation

```markdown
## Ready for Implementation?

Design is documented and committed.

Options:
a) **Create implementation plan** - Break into 2-5 min tasks
b) **Set up git worktree** - Isolated workspace for development
c) **Start with specific section** - Begin coding one component
d) **Pause here** - Continue later

What would you like to do?
```

---

## Key Principles

### One Question at a Time
```markdown
// BAD
What's the purpose, who are the users, what's the timeline,
and what constraints do we have?

// GOOD
What's the primary purpose of this feature?
[wait for answer]

Who is the main user?
[wait for answer]
```

### Prefer Multiple Choice
```markdown
// BAD
What database should we use?

// GOOD
Which database fits best?
a) PostgreSQL - You already use it
b) MongoDB - Flexible schema needs
c) Redis - Speed is critical
d) Other: ___
```

### Explore Alternatives
```markdown
Before settling on an approach:
- [ ] Considered 2-3 options
- [ ] Documented trade-offs
- [ ] Confirmed with user
- [ ] Identified simplest viable option
```

### Validate Incrementally
```markdown
Present design in chunks:
1. Data model → Confirm
2. Core logic → Confirm
3. Error handling → Confirm
4. Testing → Confirm

Not: [2000 word document] → Confirm
```

---

## Template: Brainstorming Session

```markdown
# Brainstorming: [Feature Name]

## Context Gathered
- [What I learned from codebase]
- [Relevant existing patterns]

## Understanding Questions

### Q1: [Question]
→ Answer:

### Q2: [Question]
→ Answer:

## Approaches Explored

### Option A: [Name]
- Pros: ...
- Cons: ...

### Option B: [Name]
- Pros: ...
- Cons: ...

## Chosen Approach
[Option X] because [reasons]

## Design Sections

### Section 1: [Topic]
[200-300 words]
✓ Validated

### Section 2: [Topic]
[200-300 words]
✓ Validated

## Next Steps
1. [ ] Document in docs/plans/
2. [ ] Commit design
3. [ ] Create implementation plan
```

---

## Related Skills

- **writing-plans** - Create implementation plan after design
- **executing-plans** - Execute in batches with checkpoints
- **dispatching-parallel-agents** - Concurrent implementation

---

**Source:** obra/superpowers
**Navigation:** [← Claude Skills](index.md) | [← References](../../index.md)
