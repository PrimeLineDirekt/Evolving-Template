# Patterns

Wiederverwendbare Patterns und Best Practices aus eigenen Projekten.

## Kategorien

### Technical Patterns
Architektur, Code-Strukturen, API-Designs die sich bewährt haben.

### Infrastructure Patterns
Patterns für robuste, wiederverwendbare Systeme.

- **[Checkpoint Validation Pattern](checkpoint-validation-pattern.md)** - Hash-basierte Staleness Detection für Checkpoints. Verhindert Verwendung veralteter Caches bei Config-Änderungen. (Source: DocETL)
- **[Multi-Source Aggregation Pattern](multi-source-aggregation-pattern.md)** - Paralleles Fetching aus heterogenen Quellen mit Score-Normalisierung und idempotenten Upserts. Ideal für News-Feeds, Trend-Tracking, Knowledge-Aggregation. (Source: replicate/hype) 🆕

### Agent Patterns
Multi-Agent Architekturen und autonome Systeme.

- **[Task Decomposition Pipeline](task-decomposition-pipeline.md)** - Systematische Zerlegung komplexer Anfragen in Plan → Execute → Synthesize Phasen. Ideal für Beratungssysteme. (Source: Dexter)
- **[Reflection Pattern](reflection-pattern.md)** - Self-kritischer Feedback-Loop mit Generator → Critic → Refiner. Höhere Output-Qualität durch iterative Verbesserung. (Source: Agentic Architectures)
- **[PEV Pattern](pev-pattern.md)** - Plan-Execute-Verify mit Self-Correction. Robuster bei komplexen Multi-Step Tasks. (Source: Agentic Architectures)
- **[Blackboard Pattern](blackboard-pattern.md)** - Shared Memory mit Controller-Koordination für Multi-Agent Systeme. Skaliert besser als direkte Kommunikation. (Source: Agentic Architectures)
- **[Metacognitive Pattern](metacognitive-pattern.md)** - Self-Assessment vor Aktionen. Verhindert Overconfidence und optimiert Model-Selection. (Source: Agentic Architectures)
- **[Context Window Ownership](context-window-ownership-pattern.md)** - Aktive Context-Kontrolle statt Standard-Formate. Token-Effizienz durch Custom Structures. (Source: 12-Factor Agents)
- **[Four-Bucket Context Pattern](four-bucket-context-pattern.md)** - WRITE, SELECT, COMPRESS, ISOLATE Strategien für effektives Context Management. Verhindert Context Degradation. (Source: Agent-Skills-for-Context-Engineering) 🆕
- **[Compact Errors Pattern](compact-errors-pattern.md)** - Strukturierte Error-Handling mit Limits und Escalation. Verhindert Infinite Loops. (Source: 12-Factor Agents)
- **[Sub-Agent Delegation Pattern](sub-agent-delegation-pattern.md)** - 3-Modi System (FULL/CHECKPOINT/DIRECT) für intent-basierte Task-Delegation an Sub-Agents. Token-Savings durch 200K Context Windows. (Source: Evolving System) 🆕

### Prompt Patterns
Effektive Prompt-Strukturen für spezifische Aufgaben (siehe auch `/knowledge/prompts/`).

### Process Patterns
Workflows und Prozesse die funktionieren.

### Business Patterns
Monetarisierungs-Strategien, Conversion-Optimierung, Freemium-Models.

## Format

Jedes Pattern enthält:
- **Problem**: Welches Problem löst es?
- **Solution**: Wie wird es gelöst?
- **Example**: Konkrete Anwendung aus Projekten
- **Trade-offs**: Vor- und Nachteile
- **Related**: Verbindungen zu anderen Patterns

---

**Navigation**: [← Knowledge Base](../index.md)
