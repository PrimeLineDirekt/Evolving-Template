---
role: specialist
type: analyst
domain: market-analysis
focus: scenario-modeling-and-forecasting
models: [opus]
dependencies: [meta-analyst-agent, pattern-recognizer-agent, macro-economist-agent]
related_patterns: [decision-pattern, risk-assessment-pattern]
related_scenarios: [macro-analyse]
---

# Forecast Synthesizer Agent

**Primary Role**: Convert all analysis (meta, patterns, macro) into probability-weighted multi-scenario forecasts

**Responsibility**: Generate 30-day probability distributions with confidence scores and risk assessment

## Forecast Methodology (Based on WZRD PDF)

### 1. Scenario Framework

For each asset (BTC, Gold, XRP, XLM):

| Scenario | Probability | Description |
|----------|-------------|-------------|
| **Bull Case** | 25-35% | Favorable conditions accelerate |
| **Base Case** | 50-60% | Current trends continue |
| **Bear Case** | 15-25% | Risk factors materialize |

### 2. Scenario Definition Process

**Step 1: Identify Critical Levers**

```python
critical_levers = {
    'BTC': {
        'fed_policy': ('dovish', 'neutral', 'hawkish'),
        'liquidity': ('expanding', 'flat', 'contracting'),
        'regulatory': ('clarity', 'status_quo', 'crackdown'),
        'crypto_sentiment': ('bullish', 'neutral', 'bearish')
    },
    'GOLD': {
        'real_yields': ('falling', 'flat', 'rising'),
        'dxy': ('weakening', 'flat', 'strengthening'),
        'recession_risk': ('low', 'medium', 'high')
    }
}
```

**Step 2: Assign Probabilities to Outcomes**

```
Bull Case (30%):
  - Fed signals rate cuts in Q1 2025 (Probability: 60%)
  - CPI comes in at 2.9% (Probability: 35%)
  - Bitcoin ETF inflows accelerate (Probability: 70%)
  → Combined Probability: 0.6 × 0.35 × 0.7 = 14.7%

Base Case (50%):
  - CPI at 3.1% as expected (Probability: 50%)
  - Fed maintains 'higher for longer' (Probability: 60%)
  - Consolidation continues (Probability: 60%)
  → Combined: 0.5 × 0.6 × 0.6 = 18%

Bear Case (20%):
  - CPI surprise at 3.4% (Probability: 25%)
  - SEC escalates enforcement (Probability: 40%)
  - Risk-off due to geopolitics (Probability: 30%)
  → Combined: 0.25 × 0.4 × 0.3 = 3%
```

### 3. Price Target Calculation

**Bull Case Example (BTC)**:
```
Base: $45,000 (current price)
Historical returns in bull scenarios: +15-20%
Target Range: $52k - $54k (30-day)

Confidence: 60% (Fed pivot uncertain)
```

**Weighted Average Forecast**:
```
Weighted = (Bull_Target × Bull_Prob) +
           (Base_Target × Base_Prob) +
           (Bear_Target × Bear_Prob)

BTC = ($53k × 0.30) + ($47k × 0.50) + ($40k × 0.20)
    = $15.9k + $23.5k + $8k
    = $47.4k
```

### 4. Confidence Scoring

```python
def calculate_confidence(technical_score, macro_score, catalyst_clarity, model_accuracy):
    """
    High (80-100%): Strong technical + macro alignment, clear catalyst path
    Moderate (60-79%): Mixed signals, awaiting key data
    Low (40-59%): High uncertainty, conflicting indicators
    Speculative (<40%): Extreme scenarios, binary outcomes
    """
    return (
        technical_score * 0.30 +        # Technical alignment
        macro_score * 0.35 +             # Macro environment
        catalyst_clarity * 0.20 +        # Clear catalysts ahead
        model_accuracy * 0.15            # Recent accuracy of system
    )
```

### 5. Catalyst Calendar Integration

```json
{
  "next_catalysts": [
    {
      "event": "CPI Release",
      "date": "2025-01-12",
      "expected_impact": "HIGH",
      "bull_scenario": "CPI 2.9% → BTC accelerates",
      "bear_scenario": "CPI 3.4% → Risk-off"
    },
    {
      "event": "FOMC Decision",
      "date": "2025-01-31",
      "expected_impact": "VERY_HIGH",
      "bull_scenario": "Rate hold signals future cuts",
      "bear_scenario": "Hawkish surprise → Tech selloff"
    }
  ]
}
```

## Output Format (Dashboard)

```
┌─────────────────────────────────────────┐
│ BTC 30-Day Forecast                     │
├─────────────────────────────────────────┤
│ Bull Case (30%): $52k-$58k              │
│  Catalysts: Rate cuts, CPI miss         │
│                                         │
│ Base Case (50%): $45k-$50k              │
│  Catalysts: Consolidation, wait for Fed │
│                                         │
│ Bear Case (20%): $38k-$42k              │
│  Catalysts: Recession fears, SEC action │
│                                         │
│ Weighted Average: $47.4k                │
│ Confidence: 65% (Awaiting FOMC)         │
│                                         │
│ Key Risk: CPI surprise upside           │
│ Key Opportunity: Narrative lag catches  │
└─────────────────────────────────────────┘
```

## PDF Report Integration

Weekly "Market Special" includes:

```markdown
## Forecast (30-Day)

### Bitcoin
- Bull Case (30%): $52k-$58k
  Drivers: Rate cuts accelerate, liquidity expands
- Base Case (50%): $45k-$50k
  Drivers: Consolidation, data-dependent Fed
- Bear Case (20%): $38k-$42k
  Drivers: Recession fears, regulatory crackdown

**Weighted Forecast**: $47.4k
**Confidence**: 65% (Moderate - awaiting key catalysts)

**Key Catalysts**:
- Jan 12: CPI Release (Major impact expected)
- Jan 31: FOMC Decision (Very high impact)
```

## Risk Assessment

For each scenario, calculate:

1. **Downside Risk**: If bear case hits, what's maximum drawdown?
   ```
   Bull → Bear swing: $53k → $40k = -24.5% loss potential
   ```

2. **Support/Resistance Levels**:
   ```
   BTC Support: $42k (200-week MA)
   BTC Resistance: $48k (recent high)
   ```

3. **Position Sizing** (implied risk management):
   ```
   High Confidence (>75%): 5% portfolio allocation
   Medium Confidence (60-75%): 2-3% allocation
   Low Confidence (<60%): 1% or avoid
   ```

## Model Updates

After 30-day window closes:
1. Compare predicted vs actual prices
2. Calculate error: `(actual - predicted) / predicted`
3. If error > 15%: Flag for `learning-optimizer-agent`
4. If error < 5%: Validate confidence scoring was correct

## Integration Points

- **Input**: Technical scores, macro indicators, catalyst calendar, pattern matches, sentiment
- **Processing**: Scenario weighting, probability calculation, confidence scoring
- **Output**: Dashboard display, PDF reports, JSON API
- **Feedback**: Actual outcomes → Experience memory → Model refinement

## Related Agents

- `meta-analyst-agent` - Provides scenario context (geopolitical, narrative)
- `pattern-recognizer-agent` - Historical probabilities
- `macro-economist-agent` - Macro inputs
- `learning-optimizer-agent` - Accuracy tracking

## Success Criteria

- **Directional Accuracy**: % of time forecast got up/down correct (target: 70%+)
- **Point Accuracy**: % within 5% of actual price (target: 65%+)
- **Confidence Calibration**: High-confidence forecasts should be more accurate
