# Multi-Agent Ultrathink Pattern

**Quelle**: ccplugins/ultrathink
**Kategorie**: multi-agent, orchestration
**Erstellt**: 2025-12-29

---

## Problem

Komplexe Coding-Tasks erfordern verschiedene Perspektiven: Architektur, Research, Implementation, Testing. Ein einzelner Agent kann nicht alle optimal abdecken.

## Lösung

Coordinator Agent orchestriert 4 spezialisierte Sub-Agents für umfassende Task-Bearbeitung.

## Pattern

### Struktur

```
                    ┌─────────────────┐
                    │   Coordinator   │
                    │     Agent       │
                    └────────┬────────┘
                             │
         ┌───────────┬───────┴───────┬───────────┐
         ▼           ▼               ▼           ▼
    ┌─────────┐ ┌─────────┐   ┌─────────┐ ┌─────────┐
    │Architect│ │Research │   │  Coder  │ │ Tester  │
    │  Agent  │ │  Agent  │   │  Agent  │ │  Agent  │
    └─────────┘ └─────────┘   └─────────┘ └─────────┘
```

### Die 4 Sub-Agents

| Agent | Rolle | Output |
|-------|-------|--------|
| **Architect** | High-level System Design | Approach, Struktur, Constraints |
| **Research** | External Knowledge, Best Practices | Findings, Precedents |
| **Coder** | Implementation | Code Changes, Modifications |
| **Tester** | Validation | Test Design, Verification |

### Execution Process

1. **Deconstruct**: Task in logische Schritte zerlegen
2. **Assign**: Arbeit an Sub-Agents verteilen
3. **Document**: Findings jedes Agents dokumentieren
4. **Synthesize**: "Ultrathink" Reflection - alle Perspektiven kombinieren
5. **Iterate**: Bei Knowledge Gaps wiederholen

### Output Format

```markdown
## Reasoning Transcript
- Decision points
- Analysis journey
- Agent contributions

## Final Answer
- Concrete implementation steps
- Code changes (in Markdown)

## Next Actions
- Follow-up tasks
- Open questions
```

## Wann anwenden?

- Komplexe Features mit vielen Unknowns
- Architektur-Entscheidungen
- Tasks die Research + Implementation brauchen
- Wenn verschiedene Perspektiven wertvoll sind

## Vergleich mit Evolving

| Aspect | ccplugins/ultrathink | Evolving ultrathink.md Rule |
|--------|---------------------|----------------------------|
| Typ | Multi-Agent Command | Quality Principles Rule |
| Fokus | 4 Sub-Agents orchestrieren | 5 Prinzipien (Foundation, SSOT, Composition, Naming, Roadmap) |
| Trigger | `/ultrathink <task>` | Bei komplexen Aufgaben automatisch |

**Synergie**: Beide Ansätze können kombiniert werden - die Rule definiert Qualitätsprinzipien, das Pattern definiert Agent-Orchestration.

## Beispiel

```
/ultrathink Implementiere User Authentication mit OAuth2

Coordinator:
1. Architect Agent → Designs OAuth2 Flow, Token Storage, Middleware
2. Research Agent → Findet Best Practices, Security Considerations
3. Coder Agent → Implementiert basierend auf Design + Research
4. Tester Agent → Designt Auth-Tests, Edge Cases

Synthesis:
- Alle 4 Perspektiven kombiniert
- Konkrete Implementation mit Tests
- Follow-up: Rate Limiting, Audit Logging
```

## Related

- `.claude/rules/ultrathink.md` - Evolving Ultrathink Principles
- `quality-orchestrator-template.md` - Ähnliches Multi-Agent Pattern
- `parallel-agent-dispatch-pattern.md` - Parallelisierung
