# Confidence Scoring Prompt Template

## Standard Confidence Scoring Methodology

Include this in ALL specialist agent system prompts:

```markdown
## CONFIDENCE-SCORING-METHODIK

Du MUSST deinen Confidence-Score (0.0-1.0) nach dieser standardisierten Methodik berechnen:

### Faktoren für die Bewertung:

1. **KB-Quellen-Qualität:**
   - Primary Source (Tier 1): Basisfaktor 1.0
   - Secondary Source (Tier 2): Basisfaktor 0.8
   - Tertiary Source (Tier 3): Basisfaktor 0.6
   - Keine Quellen: Basisfaktor 0.4

2. **Aktualität der Information:**
   - Aktuell (<1 Jahr alt): ×1.0
   - Leicht veraltet (1-2 Jahre): ×0.85
   - Älter (>2 Jahre): ×0.6

3. **Vollständigkeit der Analyse:**
   - Alle relevanten Aspekte abgedeckt: +0.15
   - Teilweise abgedeckt: ±0.0
   - Wesentliche Lücken: -0.15

4. **Konsistenz:**
   - Keine Widersprüche in Quellen: ×1.0
   - Minor Widersprüche (geklärt): ×0.9
   - Major Widersprüche (ungelöst): ×0.7

### Formel:
```
confidence = base_score × aktualität × konsistenz + vollständigkeit_bonus
```

### Grenzen:
- Maximum bei kritischen Lücken: 0.65
- Minimum bei validen Quellen: 0.50
- HITL-Trigger unter: 0.75

### In deiner Antwort:
Erkläre kurz, wie du zu deinem Confidence-Score gekommen bist.
```

## Source Tier Definitions

| Tier | Name | Description | Examples |
|------|------|-------------|----------|
| **1** | Primary | Authoritative sources | Laws, regulations, official guidelines |
| **2** | Secondary | Interpretive sources | Court rulings, official interpretations |
| **3** | Tertiary | Reference sources | Articles, summaries, explanations |

## Confidence Thresholds

| Score | Interpretation | Action |
|-------|---------------|--------|
| 0.85+ | Premium Quality | Auto-publish |
| 0.75-0.84 | Good Quality | Auto-publish with minor review |
| 0.50-0.74 | Acceptable | HITL Review required |
| <0.50 | Low Quality | Do not publish |

## Aggregation for Multi-Agent Reports

```python
def aggregate_confidence(agent_results, profile_weights):
    """
    Calculate weighted confidence score across all agents.

    Args:
        agent_results: Dict of {agent_id: confidence_score}
        profile_weights: Dict of {agent_id: weight} based on profile relevance

    Returns:
        Aggregated confidence score (0.0-1.0)
    """
    weighted_sum = 0
    total_weight = 0

    for agent_id, score in agent_results.items():
        weight = profile_weights.get(agent_id, 0.1)
        weighted_sum += score * weight
        total_weight += weight

    base_score = weighted_sum / total_weight if total_weight > 0 else 0

    # Apply penalties
    low_confidence_agents = sum(1 for s in agent_results.values() if s < 0.6)
    penalty = low_confidence_agents * 0.05

    return max(0.0, min(1.0, base_score - penalty))
```

## Usage in Agent Prompts

Add to every specialist agent's system prompt:

```python
CONFIDENCE_SCORING_PROMPT = """
## CONFIDENCE-SCORING-METHODIK
[Full content from above]
"""

system_prompt = f"""
# {Agent Name}

{agent_specific_content}

{CONFIDENCE_SCORING_PROMPT}
"""
```
