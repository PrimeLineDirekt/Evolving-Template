# Multi-Agent Advisory Scenario Template

## Overview

Ein Template für **profil-basierte Multi-Agent Beratungssysteme** - optimal für komplexe, personalisierte Beratung in beliebigen Domains.

## Wann dieses Template nutzen?

**Perfekt für:**
- Umfassende Beratung basierend auf User-Profil
- Domains mit 5+ spezialisierten Fachbereichen
- Keine Follow-up Fragen - ein umfassender Report ist das Endprodukt
- High-Stakes Entscheidungen (Steuern, Recht, Finanzen, Gesundheit)

**Nicht geeignet für:**
- Einzelne spezifische Fragen → Nutze `autonomous-research` Template
- Einfache Lookups → Direkte KB-Suche
- Interaktive Chatbots → Anderes Pattern

## Pattern: Multi-Agent Advisory

```
┌─────────────────────────────────────────────────────────────┐
│                     USER PROFILE                            │
│              (126+ Felder, strukturiert)                    │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                  ORCHESTRATOR                               │
│  - Complexity Score berechnen                               │
│  - Relevante Agents auswählen                               │
│  - Model Tier zuweisen                                      │
│  - Checkpoints verwalten                                    │
└─────────────────────┬───────────────────────────────────────┘
                      │
          ┌───────────┼───────────┬───────────┐
          ▼           ▼           ▼           ▼
     ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐
     │ Agent 1 │ │ Agent 2 │ │ Agent 3 │ │ Agent N │
     │ (Opus)  │ │(Sonnet) │ │(Sonnet) │ │ (Haiku) │
     │ Tier 1  │ │ Tier 2  │ │ Tier 2  │ │ Tier 3  │
     └────┬────┘ └────┬────┘ └────┬────┘ └────┬────┘
          │           │           │           │
          └───────────┴───────────┴───────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                    REPORTER                                  │
│  - Outputs konsolidieren                                     │
│  - Konflikte auflösen                                        │
│  - Confidence aggregieren                                    │
│  - Final Report generieren                                   │
└─────────────────────────────────────────────────────────────┘
                      │
                      ▼
                 FINAL REPORT
```

## Kern-Konzepte

### 1. Profile-Based Agent Selection

**Mandatory Agents** (immer aktiv):
```python
# Agents die IMMER laufen, unabhängig vom Profil
mandatory_agents = [
    "profil_analyse",    # Master Assessment
    "{domain}_core",     # Kern-Domain Agent
    "checkliste",        # Action Items
]
```

**Conditional Agents** (basierend auf Profil):
```python
# Beispiel-Logik für Agent-Auswahl
if profile.has_business:
    selected.append("business_agent")
if profile.has_children:
    selected.append("family_agent")
if profile.net_worth > threshold:
    selected.append("wealth_agent")
```

### 2. Complexity Score (20-100)

Bewertet Profil-Komplexität für:
- Model Tier Auswahl
- Agent-Anzahl Begrenzung
- HITL Trigger

```python
score = 20  # Base
if high_income: score += 15
if high_net_worth: score += 20
if business_owner: score += 15
if special_circumstances: score += 10
# ... etc.
```

### 3. Model Tiering

| Tier | Model | Wann nutzen |
|------|-------|-------------|
| **1** | Opus | Kritische Analyse, komplexe Entscheidungen, hoher €-Impact |
| **2** | Sonnet | Standard-Analyse, moderate Komplexität |
| **3** | Haiku | Strukturierte Tasks, Checklisten, Simple Lookups |

### 4. Risk Zone Classification

```
🟢 GRÜN (Sicher)     - Standard-Verfahren, etabliert
🟡 GELB (Moderat)    - Legal aber nicht Standard, Dokumentation nötig
🟠 ORANGE (Aggressiv) - Am Limit, Expertenberatung zwingend
❌ VERBOTEN          - Illegal, niemals empfehlen
```

### 5. Confidence Scoring

**3-Tier Sources:**
- Primary (Tier 1): 1.0 Basisfaktor
- Secondary (Tier 2): 0.8 Basisfaktor
- Tertiary (Tier 3): 0.6 Basisfaktor

**Formel:**
```
confidence = base_score × aktualität × konsistenz + vollständigkeit_bonus
```

**HITL Trigger:** < 0.75

## Template-Dateien

```
multi-agent-advisory/
├── README.md                   # Diese Datei
├── scenario.json               # Szenario-Konfiguration
├── agents/
│   ├── orchestrator-agent.md   # Koordination & Checkpoints
│   ├── selector-agent.md       # Agent-Auswahl Logik
│   ├── specialist-agent.md     # Template für Domain-Experts
│   └── reporter-agent.md       # Report-Generierung
└── prompts/
    ├── selection.md            # Agent-Auswahl Prompt
    ├── specialist.md           # Domain-Expert System Prompt
    ├── confidence-scoring.md   # Confidence-Berechnung
    ├── risk-zones.md           # Risk Classification
    └── reporting.md            # Report-Format
```

## Schnellstart

### 1. Szenario erstellen

```bash
cp -r .claude/templates/scenarios/multi-agent-advisory/ .claude/scenarios/my-advisory/
```

### 2. Platzhalter ersetzen

In allen Dateien:
- `{DOMAIN}` → z.B. "tax-advisory", "legal-advisory"
- `{DOMAIN_NAME}` → z.B. "Steuerberatung", "Rechtsberatung"
- `{MANDATORY_AGENTS}` → Deine Pflicht-Agents
- `{CONDITIONAL_AGENTS}` → Deine optionalen Agents

### 3. Agents definieren

Für jeden Agent:
1. Kopiere `specialist-agent.md`
2. Definiere Expertise-Bereich
3. Setze Model Tier (1/2/3)
4. Definiere KB-Queries

### 4. Knowledge Base aufbauen

Struktur:
```
knowledge-base/{domain}/
├── {category-1}/
│   └── *.md
├── {category-2}/
│   └── *.md
└── ...
```

## Referenz-Implementierung

Siehe **{PROJECT} v2** als vollständige Implementierung:
- 17 Specialist Agents
- 72 KB-Dokumente (621k Wörter)
- Risk Zone Classification
- 3-Tier Model Selection
- ResilientOrchestrator mit Crash Recovery

→ `knowledge/prompts/patterns/{PROJECT_ID}-agents/README.md`

## Use Cases

| Domain | Mandatory Agents | Conditional Agents |
|--------|------------------|-------------------|
| **Tax/Emigration** | profil_analyse, steuer, checkliste | business, family, crypto, senior |
| **Legal Advisory** | case_analysis, compliance, summary | contract, litigation, ip |
| **Financial Planning** | profile, goals, risk | investment, insurance, estate |
| **Medical Advisory** | diagnosis, treatment, summary | specialist, pharmacy, rehab |

## Best Practices

1. **Mandatory ≤ 3**: Nicht mehr als 3 Pflicht-Agents
2. **Total ≤ 10**: Max 10 Agents pro Analyse
3. **Tier 1 sparsam**: Nur 2-3 Agents auf Opus
4. **KB first**: Agents ohne KB-Quellen → Confidence Penalty
5. **HITL bei < 0.75**: Niemals Auto-Publish bei niedriger Confidence

---

**Template Version**: 1.0.0
**Basiert auf**: {PROJECT} v2 (Production-Proven)
**Pattern**: Multi-Agent Advisory
