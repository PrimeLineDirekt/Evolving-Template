# PRD Planning Agent Template

**Quelle**: ccplugins/planning-prd-agent (34KB)
**Abstrahiert**: 2025-12-29
**Status**: template

---

## Zweck

Template für PRD-Erstellung mit strukturiertem Task Breakdown und Dependency Analysis.

## Core Sections (aus Original abstrahiert)

### 1. PRD Structure

```markdown
# PRD: {Feature Name}
Generated: {Date}
Version: {Version}

## Table of Contents
1. Source/Context Reference
2. Technical Interpretation
3. Functional Specifications
4. Technical Requirements & Constraints
5. User Stories with Acceptance Criteria
6. Task Breakdown Structure
7. Dependencies & Integration Points
8. Risk Assessment & Mitigation
9. Testing & Validation Requirements
10. Monitoring & Observability
11. Success Metrics & Definition of Done
12. Technical Debt & Future Considerations
```

### 2. Task Breakdown Format

```markdown
## TASK-{ID}: {Task Name}
**Type**: {Frontend|Backend|Database|DevOps|QA}
**Effort Estimate**: {hours/points}
**Dependencies**: [{TASK-IDs}]

### Description
{What needs to be built}

### Technical Requirements
{Specific technical details}

### Acceptance Criteria
{How we know it's complete}

### Implementation Notes
{Helpful context}
```

### 3. Dependency Reasoning Pattern

1. **Dependency Mapping**: List all tasks with explicit dependencies
2. **Critical Path Calculation**: Identify longest dependent sequence
3. **Dependency Graph**: Mermaid diagram showing relationships
4. **Risk Assessment**: Identify risks in dependency chains
5. **Status Assignment Logic**: To Do / Blocked / In Progress based on dependencies

### 4. Phase Structure

```
Phase 0: Clarification & Context Gathering
Phase 1: Discovery & Analysis
Phase 2: Technology Research & Best Practices
Phase 3: Technical Design with Dependency Reasoning
Phase 4: Documentation Creation
```

### 5. Quality Standards

- **Testability**: Every requirement must be testable
- **Completeness**: All edge cases addressed
- **Clarity**: Zero ambiguity
- **Traceability**: Clear mapping from requirements to tasks
- **Realistic**: Estimates include buffer

## Placeholders

| Placeholder | Description |
|-------------|-------------|
| `{Feature Name}` | Name of feature/project |
| `{TASK-ID}` | Task identifier (TASK-001, TASK-002) |
| `{Type}` | Frontend, Backend, Database, DevOps, QA |
| `{Dependencies}` | List of dependent TASK-IDs |

## Output Files

1. `prd_{feature_name}_{YYYYMMDD}.md` - Full PRD
2. `task_assignments_{YYYYMMDD}.md` - Task assignment table

## Integration mit Evolving

- Nutzt Plan-Mode für initiale Planung
- Generiert Tasks für TodoWrite
- Dependency Graph kann in _graph/ integriert werden
