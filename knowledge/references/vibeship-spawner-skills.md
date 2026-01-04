# Vibeship Spawner Skills

**Quelle**: https://github.com/obra/vibeship-spawner-skills
**Extrahiert**: 2026-01-01
**Kategorie**: reference

---

## Übersicht

Umfangreiche Skill-Bibliothek mit **462 Skills** in **35 Kategorien**. Jeder Skill besteht aus einem 4-File System für vollständige Expertise-Repräsentation.

## 4-File System

| Datei | Zweck |
|-------|-------|
| `skill.yaml` | Kern-Wissen, Patterns, Best Practices |
| `sharp-edges.yaml` | Bekannte Gotchas, Fehlerquellen |
| `validations.yaml` | Output-Qualitätskriterien, Checklisten |
| `collaboration.yaml` | Zusammenarbeit mit anderen Skills |

## Kategorien-Übersicht (35 Kategorien)

| Kategorie | Skills | Fokus |
|-----------|--------|-------|
| **ai-agents** | 23 | Multi-Agent Systems, Orchestrierung, Memory |
| **ai** | 24 | LLM Integration, Prompt Engineering, RAG |
| **devops** | 22 | CI/CD, Docker, Kubernetes, IaC |
| **game-dev** | 51 | Unity, Unreal, Game Design, Physics |
| **marketing** | 36 | SEO, Content, Social Media, Analytics |
| **mind** | 10 | Debugging, Reasoning, Problem-Solving |
| **frontend** | 15 | React, Vue, CSS, Accessibility |
| **backend** | 18 | APIs, Databases, Authentication |
| **security** | 12 | Auth, Encryption, Vulnerability Analysis |
| **data** | 14 | ETL, Analytics, Visualization |
| **mobile** | 11 | iOS, Android, React Native |
| **testing** | 9 | Unit, Integration, E2E Testing |
| **cloud** | 16 | AWS, GCP, Azure, Serverless |
| **languages** | 28 | Python, TypeScript, Go, Rust |
| **tools** | 20 | Git, Docker, CLI Tools |

*Weitere 20 Kategorien mit insgesamt ~193 Skills (3D, animation, audio, blockchain, etc.)*

---

## Top Skills: AI-Agents (23 Skills)

### Multi-Agent Orchestration
**Patterns für Agent-Koordination:**
- **Sequential Chain**: Agent A → Agent B → Agent C (Response as Input)
- **Parallel Execution**: [Agent A, Agent B, Agent C] → Aggregator
- **Router/Dispatcher**: Classifier → Selected Specialist Agent
- **Hierarchical Supervisor**: Manager Agent koordiniert Worker Agents

**Anti-Patterns zu vermeiden:**
- Agent Soup (zu viele Agents ohne klare Rollen)
- Circular Dependencies (Agents rufen sich gegenseitig)
- Shared State Mutations (Race Conditions)

### Agent Memory Systems
**CoALA Framework Typen:**
| Memory Type | Zweck | Beispiel |
|-------------|-------|----------|
| Semantic | Fakten, Wissen | "User bevorzugt TypeScript" |
| Episodic | Vergangene Events | "Letzte Session: Bug in auth.ts" |
| Procedural | How-To Wissen | "So deploye ich auf Railway" |

**Vector Store Auswahl:**
- **Pinecone**: Cloud-first, managed, skaliert
- **Qdrant**: Self-hosted, Rust-basiert, schnell
- **ChromaDB**: Einfach, Python-nativ, dev-friendly
- **pgvector**: PostgreSQL-Integration, ACID

### Weitere AI-Agent Skills
- `agentic-rag` - Retrieval-Augmented Generation
- `agent-tool-use` - Tool Calling Patterns
- `agent-evaluation` - Testing & Metrics
- `human-in-the-loop` - HITL Patterns
- `agent-observability` - Logging & Tracing

---

## Top Skills: Mind (10 Skills)

### Debugging Master
**Scientific Method Loop:**
1. Observe (Logs, Error Messages, Behavior)
2. Hypothesize (Was könnte falsch sein?)
3. Predict (Wenn Hypothese stimmt, dann...)
4. Test (Verifiziere Vorhersage)
5. Conclude (Bestätige oder verwerfe)

**Bewährte Techniken:**
- **Binary Search / Wolf Fence**: Halbiere Problem-Raum
- **Five Whys**: 5x "Warum?" für Root Cause
- **Rubber Duck**: Erkläre Problem laut
- **Time Travel**: Git bisect, Checkpoint Comparison

**Anti-Patterns:**
- Confirmation Bias (nur nach Bestätigung suchen)
- Assumption Blind Spot (Annahmen nicht hinterfragen)
- Symptom Chasing (Oberfläche statt Root Cause)

### Weitere Mind Skills
- `first-principles` - Grundlagen-basiertes Denken
- `systems-thinking` - Systemisches Denken
- `decision-making` - Entscheidungsframeworks
- `problem-decomposition` - Komplexität reduzieren
- `mental-models` - Denkwerkzeuge

---

## Top Skills: DevOps (22 Skills)

### Container Orchestration
- Kubernetes Patterns (Deployments, Services, Ingress)
- Docker Multi-Stage Builds
- Helm Charts für Packaging

### CI/CD Pipelines
- GitHub Actions Workflows
- GitLab CI/CD
- ArgoCD für GitOps

### Infrastructure as Code
- Terraform Modules
- Pulumi (TypeScript IaC)
- AWS CDK Patterns

### Monitoring & Observability
- Prometheus + Grafana Stack
- OpenTelemetry Integration
- Log Aggregation (ELK, Loki)

---

## MCP Server Integration

**Verfügbare Tools:**
```
spawner_skills(action="get", name="debugging-master")
spawner_orchestrate(skills=["debugging-master", "python"], task="...")
spawner_validate(skill="agent-memory-systems", output="...")
spawner_remember(skill="...", insight="...")
```

**Workflow:**
1. `spawner_skills("list")` - Verfügbare Skills erkunden
2. `spawner_skills("get", name="...")` - Skill laden
3. `spawner_orchestrate(skills=[...])` - Mehrere Skills kombinieren
4. `spawner_validate(...)` - Output gegen Skill prüfen

---

## Lokaler Pfad

```
{EVOLVING_PATH}/_archive/repos/2026-01-01-deep-dive/vibeship-spawner-skills/
├── skills/
│   ├── ai-agents/           # 23 Skills
│   │   ├── multi-agent-orchestration/
│   │   ├── agent-memory-systems/
│   │   └── ...
│   ├── mind/                # 10 Skills
│   │   ├── debugging-master/
│   │   └── ...
│   ├── devops/              # 22 Skills
│   └── ... (35 Kategorien)
├── SKILLS_DIRECTORY.md      # Vollständiger Index
└── README.md                # System-Dokumentation
```

---

## Nutzung in Evolving

**Integration mit Model Selector:**
```
Komplexe Task → spawner_orchestrate(skills=["multi-agent-orchestration", "debugging-master"])
Research Task → spawner_skills(get, "agentic-rag")
DevOps Task → spawner_skills(get, "kubernetes") + spawner_skills(get, "terraform")
```

**Synergien mit Evolving Skills:**
- `research-orchestrator` + Vibeship `agentic-rag`
- `template-creator` + Vibeship `agent-memory-systems`
- Debugging Workflow + Vibeship `debugging-master`

---

## Related

- [claude-skills-generator.md](claude-skills-generator.md) - Skill Template Patterns
- [vibeship-content-ops.md](vibeship-content-ops.md) - Content Pipeline Skills
- [knowledge/patterns/multi-agent-orchestration.md](../patterns/multi-agent-orchestration.md)
