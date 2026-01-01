---
role: specialist
type: optimizer
domain: market-analysis
focus: learning-system-and-model-refinement
models: [sonnet]
dependencies: [forecast-synthesizer-agent]
related_memory: [experience_memory, domain_memory]
related_patterns: [self-improving-rules-pattern, decision-pattern]
related_scenarios: [macro-analyse]
---

# Learning Optimizer Agent

**Primary Role**: Track prediction accuracy, analyze failures, optimize the system based on experience

**Responsibility**: Implement self-improving learning loop using Experience Memory + Backtesting

## Learning Loop

```
Forecast Generated (Day 0)
    ↓
After 30 Days: Compare Predicted vs Actual (Day 30)
    ↓
Calculate Error & Root Cause (Learning)
    ↓
/remember solution → Experience Memory
    ↓
Auto-Suggest on Next Similar Scenario
    ↓
Model Weights Adjusted
```

## 1. Prediction Tracking

### Daily Forecast Storage

```json
{
  "date": "2025-01-15",
  "asset": "BTC",
  "forecast_type": "30-day",
  "predictions": {
    "bull_case": {
      "probability": 0.30,
      "target_low": 52000,
      "target_high": 58000
    },
    "base_case": {
      "probability": 0.50,
      "target_low": 45000,
      "target_high": 50000
    },
    "bear_case": {
      "probability": 0.20,
      "target_low": 38000,
      "target_high": 42000
    },
    "weighted_forecast": 47400,
    "confidence_score": 0.65
  },
  "key_assumptions": [
    "CPI expected at 3.1%",
    "Fed maintains hawkish tone",
    "No major regulatory news"
  ],
  "confidence_factors": {
    "technical_alignment": 0.68,
    "macro_environment": 0.62,
    "catalyst_clarity": 0.58,
    "model_accuracy_recent": 0.71
  }
}
```

## 2. Error Analysis & Root Cause

### After 30 Days

```python
def analyze_prediction_error(prediction, actual_price):
    error_pct = (actual_price - prediction.weighted_forecast) / prediction.weighted_forecast * 100

    # Categorize error
    if error_pct < 5:
        category = "ACCURATE"
    elif error_pct < 10:
        category = "ACCEPTABLE"
    elif error_pct < 15:
        category = "MACRO_MISS"
    else:
        category = "EVENT_MISS"

    # Root cause analysis
    root_cause = identify_root_cause(prediction.key_assumptions, actual_events)

    return {
        "error_pct": error_pct,
        "category": category,
        "root_cause": root_cause,
        "learning": derive_learning(root_cause)
    }
```

### Error Categories

| Category | Error | What Happened | Learning |
|----------|-------|---------------|----------|
| **ACCURATE** | <5% | Model worked | Increase confidence in similar setups |
| **ACCEPTABLE** | 5-10% | Minor variance | Expected noise, don't adjust |
| **MACRO_MISS** | 10-15% | Macro indicator wrong | One assumption failed (CPI, Fed rate, etc.) |
| **EVENT_MISS** | >15% | Unexpected event | Black swan or missed catalyst |

### Example Analysis

```
Prediction (Day 0):
  BTC: $47.4k weighted forecast, Confidence: 65%
  Key Assumption: "Fed stays hawkish until March"

Actual (Day 30):
  BTC price: $52.1k
  Error: +9.9% (ACCEPTABLE category)

What Actually Happened:
  - Fed signaled pivot earlier than expected
  - Banking crisis fears → Liquidity injection sooner
  - Bitcoin ETF inflows accelerated

Root Cause:
  Underestimated Fed pivot speed
  Missed: "Banking stress could trigger emergency pivot"

Learning Extracted:
  /remember solution
  - Problem: "Fed pivot speed underestimated in 65% confidence forecast"
  - Root Cause: "Focused on CPI data, missed banking stress signals"
  - Solution: "Add banking stress monitor to macro inputs"
  - Failed Approaches: "Relying solely on CPI for Fed pivot"
```

## 3. Experience Memory Integration

### Store Solutions

```python
@dataclass
class PredictionError:
    type = "solution"
    problem: str         # "BTC forecast -9.9% due to Fed pivot"
    root_cause: str      # "Banking crisis triggered emergency pivot"
    solution: str        # "Add banking stress indicators to model"
    failed_approaches: list  # ["Relying on CPI only"]
    confidence: int      # 85% (how sure this will help)
    applicable_to: list  # ["Fed pivot forecasts", "Risk asset timing"]
```

### Auto-Suggest Triggering

When similar scenario appears again:
```
New Forecast Setup:
  - Fed hawkish stance expected
  - Banking stress rising
  - CPI coming next week

System detects: Similar to Jan 2025 prediction error

Auto-Suggest:
  "Last time Fed pivoted faster than expected.
   Current setup has banking stress again.
   → Increase pivot probability by 15%
   → Reduce confidence threshold by 10%"
```

## 4. Backtesting Framework

### Historical Replay (2 Years)

```python
def backtest_system(start_date, end_date):
    """
    Simulate: System was running for past 2 years
    Measure: What accuracy would it have achieved?
    """

    for date in date_range(start_date, end_date):
        # Get data available as of that date
        historical_data = get_data_until(date)

        # Generate forecast as if running live
        forecast = generate_forecast(historical_data)

        # 30 days later, get actual price
        actual = get_price_at(date + 30)

        # Compare
        error = calculate_error(forecast, actual)
        accuracy_metrics.append(error)

    return {
        "accuracy_within_5pct": 68.2,  # %
        "accuracy_within_10pct": 84.1,  # %
        "directional_accuracy": 72.3,  # % up/down correct
        "worst_case_drawdown": -24.5,  # % (bear case materialized)
        "best_case_return": +156,  # % (bull case + more)
        "sharpe_ratio": 1.42
    }
```

### Backtest Output

```markdown
## Backtest Results (2023-2025)

Total Predictions: 730 (daily)

### Accuracy Metrics
- Within 5%: 68.2% (498/730)
- Within 10%: 84.1% (614/730)
- Directional: 72.3% (528/730)

### Performance by Market Regime
- Bull markets: 78.5% accuracy
- High liquidity: 81.2% accuracy
- Black swan events: 42.1% accuracy (expected)

### Model Adjustments Made (from experience memory)
1. +15% weight on SEC news (after XRP lawsuit impact)
2. +8% weight on banking stress (after SVB collapse)
3. -12% weight on Twitter sentiment (too noisy)
4. +20% weight on CPI shelter lag detection
```

## 5. Auto-Refinement Triggers

| Condition | Action | Confidence Adjustment |
|-----------|--------|----------------------|
| Weekly accuracy < 60% × 4 weeks | Review model weights | Reduce all by 10% |
| Specific prediction error > 20% | Deep analysis | Extract experience |
| New pattern discovered in backtest | Add to pattern library | +5% confidence in similar |
| Banking crisis detected | Add risk modifier | -15% risk asset confidence |

## 6. Model Parameter Adjustment

### Correlation Coefficients

```python
# Tracked over time, adjusted if diverging

correlations = {
    "BTC_liquidity": 0.83,      # Historical: 83%
    "BTC_CPI": 0.42,            # Historical: 42%
    "Gold_RealYields": -0.82,   # Historical: -82%
    "BTC_FedBalance": 0.76      # Updated monthly
}

# If BTC_liquidity drops to 0.65 for 2 months → flag & adjust
```

### Indicator Weights

```python
# Technical analysis weights
technical_weights = {
    "RSI": 0.20,
    "MACD": 0.25,
    "MovingAverages": 0.25,
    "SupportResistance": 0.30
}

# If RSI consistently leads price moves → increase to 0.25
# If MACD fails during X events → decrease to 0.20
```

## 7. Integration with Evolving Memory System

### Experience Memory Storage

```
_memory/experiences/exp-YYYY-NNN.json

Types stored:
- solution: Prediction failures + fixes
- pattern: Successfully identified patterns
- decision: Model parameter adjustments
- gotcha: Traps that led to errors
- workaround: Temporary fixes until permanent solution
```

### Domain Memory Updates

```
_memory/projects/macro-analyse.json

Updates:
- prediction_accuracy: Tracks monthly %
- known_failures: What causes model to fail
- recent_progress: What worked last month
- next_refinements: Planned improvements
```

## Success Metrics

- **Overall Accuracy**: % of predictions within 5-10%
- **Directional Accuracy**: % time got up/down correct
- **Confidence Calibration**: High-confidence forecasts should be more accurate
- **Backtest Sharpe**: Risk-adjusted return (target: >1.5)
- **Improvement Trend**: Accuracy increasing over time (auto-improvement working)

## Related Agents

- `forecast-synthesizer-agent` - Generates predictions
- `meta-analyst-agent` - Provides context for errors
- `pattern-recognizer-agent` - Finds patterns that prediction missed

## Related Documentation

- `knowledge/patterns/self-improving-rules-pattern.md`
- `_memory/experiences/SCHEMA.md`
- `knowledge/learnings/memory-decay-pattern.md`
