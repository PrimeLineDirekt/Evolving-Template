---
role: orchestrator
type: system
domain: market-analysis
focus: agent-coordination-and-synthesis
models: [sonnet]
dependencies: [
  macro-data-collector-agent,
  market-technical-analyst-agent,
  macro-economist-agent,
  meta-analyst-agent,
  pattern-recognizer-agent,
  forecast-synthesizer-agent,
  learning-optimizer-agent
]
related_patterns: [multi-agent-orchestration-pattern]
related_scenarios: [macro-analyse]
---

# Macro Orchestrator Agent

**Primary Role**: Coordinate all Macro-Analyse agents and synthesize comprehensive market analysis

**Responsibility**: Orchestrate parallel/sequential execution, validate outputs, generate final reports

## Agent Orchestration Map

```
PARALLEL PHASE 1 (Collect)
├── macro-data-collector-agent      → Fetch all data in parallel
│   ├─ Crypto data (BTC, XRP, XLM, XDC)
│   ├─ Metals data (Gold, Silver)
│   ├─ Macro data (CPI, Fed rates, Yields, Treasury)
│   ├─ Events (SEC, FOMC, Elections)
│   └─ News (Reuters, Reddit, CryptoPanic)
│
└─ Validation: All sources returned? Quality > 85%?

PARALLEL PHASE 2 (Analyze)
├─ market-technical-analyst-agent   → Calculate technical scores
├─ macro-economist-agent            → Liquidity, inflation, Fed analysis
└─ meta-analyst-agent              → Narratives, geopolitics, cui bono

PARALLEL PHASE 3 (Patterns & Context)
├─ pattern-recognizer-agent         → Historical patterns, contrarian signals
└─ [meta-analyst results from Phase 2]

SEQUENTIAL PHASE 4 (Synthesize)
└─ forecast-synthesizer-agent       → Combine all inputs into forecasts
   └─ Input: Technical score (67)
   └─ Input: Macro score (63)
   └─ Input: Patterns (election cycle 75% prob)
   └─ Input: Narratives (Fed pivot incoming)
   └─ Output: Multi-scenario forecasts with confidence

SEQUENTIAL PHASE 5 (Learning)
└─ learning-optimizer-agent         → Update model, store experiences

SEQUENTIAL PHASE 6 (Output)
└─ Orchestrator generates:
   ├─ Dashboard updates
   ├─ PDF report (if daily trigger)
   └─ Experience memory entries
```

## Execution Workflow

### Hourly Execution (Real-time Data)

```python
every_hour():
    # PHASE 1: Collect (parallel, 30s timeout)
    data_tasks = [
        macro_data_collector.fetch_all_sources(),  # Real-time: Binance, Zillow, FRED
    ]
    data = await parallel_execute(data_tasks, timeout=30s)

    # Validate
    assert data.quality_score > 85, "Data quality issue"

    # PHASE 2-3: Analyze (parallel, 60s timeout)
    analysis_tasks = [
        technical_analyst.analyze_price_action(data),
        macro_economist.analyze_liquidity_cycles(data),
        meta_analyst.detect_narratives(data)
    ]
    analyses = await parallel_execute(analysis_tasks, timeout=60s)

    # PHASE 4: Synthesize (sequential, 45s)
    patterns = pattern_recognizer.find_patterns(data, analyses)
    forecast = forecast_synthesizer.generate_forecast(analyses, patterns)

    # PHASE 6: Update outputs
    update_dashboard(forecast)
```

### Daily Execution (PDF Report @ 18:00 {COUNTRY} Time = 11:00 UTC = 06:00 EST)

```python
at_18_00_vietnam_time():
    # Run all phases above (fresh data after US market close)
    forecast = run_hourly_execution()

    # PHASE 5: Learning update
    learning_optimizer.review_previous_forecasts()
    learning_optimizer.update_model_weights()

    # PHASE 6: Generate PDF
    pdf_report = generate_pdf_report(forecast, analyses, patterns)
    save_pdf(pdf_report, f"reports/{YYYY}-{MM}-{DD}-market-special.pdf")

    # Update domain memory
    update_domain_memory({
        "last_forecast": forecast,
        "last_analysis_time": now(),
        "next_catalyst": get_next_catalyst()
    })
```

### Weekly Execution (Backtest & Model Refinement)

```python
every_week():
    # PHASE 5: Deep learning review
    learning_optimizer.run_backtest(past_7_days)
    learning_optimizer.calculate_accuracy_metrics()
    learning_optimizer.identify_model_weak_points()

    # PHASE 1-4: Refined forecast with learnings
    forecast = run_full_analysis_with_recent_learnings()

    # Store as "Weekly Meta-Analysis Report"
    update_pdf_report_with_learning_insights()
```

## Output Validation

### Quality Gates Before Output

```python
def validate_forecast(forecast, analyses):
    """Ensure forecast quality before publishing"""

    checks = [
        # Check 1: Score validity
        assert 0 < technical_score <= 100, "Technical score invalid"
        assert 0 < macro_score <= 100, "Macro score invalid"
        assert 0 < confidence <= 100, "Confidence invalid"

        # Check 2: Scenario sum to 100%
        assert sum([bull_prob, base_prob, bear_prob]) == 1.0, "Probs don't sum"

        # Check 3: Prices make sense
        assert bear_case < base_case < bull_case, "Prices illogical"

        # Check 4: Assumptions present
        assert len(forecast.key_assumptions) >= 3, "Need assumptions"

        # Check 5: Catalyst calendar present
        assert len(forecast.next_catalysts) >= 2, "Need catalysts"

        # Check 6: Confidence justified
        assert forecast.confidence < 95, "Too confident (overfit)"
        assert forecast.confidence > 30, "Too uncertain (underfit)"
    ]

    return all(checks) ? forecast : raise_validation_error()
```

## Error Recovery

### If Agent Fails

```python
try:
    technical_score = market_technical_analyst.analyze()
except TimeoutError:
    log_error("Technical analyst timeout")
    technical_score = 50  # Neutral default
    store_experience("error: technical_analyst_timeout")

try:
    macro_score = macro_economist.analyze()
except DataError:
    log_error("Macro data unavailable")
    macro_score = previous_macro_score  # Use last known good
    store_experience("error: macro_data_missing")
```

### If Multiple Agents Fail

```python
if failed_agents >= 3:
    log_error("Too many failures, skip forecast generation")
    send_alert("Macro-Analyse system degraded")
    use_previous_forecast_with_warning()
else:
    proceed_with_available_data()
```

## Dashboard Integration

### Real-time Widget Updates

```
Every 15 minutes: Update price tiles
Every hour: Update analysis scores
Every 6 hours: Update forecast
Daily (18:00 {COUNTRY}): Update PDF + weekly insights
```

### System Health Monitoring

```json
{
  "system_status": "healthy",
  "last_update": "2025-01-15T10:23:00Z",
  "agent_status": {
    "data_collector": "✓ 100%",
    "technical_analyst": "✓ 100%",
    "macro_economist": "✓ 100%",
    "meta_analyst": "✓ 100%",
    "pattern_recognizer": "✓ 100%",
    "forecast_synthesizer": "✓ 100%",
    "learning_optimizer": "✓ 100%"
  },
  "data_quality": "87%",
  "forecast_confidence": "65%",
  "next_catalyst": "CPI on Jan 12"
}
```

## Performance Metrics Tracked

```python
metrics = {
    "execution_time": 145,  # seconds
    "data_quality": 87,     # %
    "agents_successful": 7/7,
    "forecast_confidence": 65,  # %
    "model_accuracy_30day": 68.2,  # %
    "last_error": None,
    "uptime": 99.8  # %
}
```

## Failure Modes & Recovery

| Failure | Recovery | User Impact |
|---------|----------|------------|
| One agent times out | Use default score (50) | Forecast slightly lower confidence |
| Data source unavailable | Use cached data | Slight lag in real-time updates |
| Multiple agents fail | Skip forecast, use previous | Daily PDF may be delayed |
| System crash | Auto-restart, resume | Depends on duration |

## Integration with Evolving Memory

### Domain Memory Updates

```
Every hour:
  _memory/projects/macro-analyse.json
  └─ current_state.last_forecast = forecast
  └─ current_state.analysis_time = now()

Every day:
  _memory/projects/macro-analyse.json
  └─ progress[].date = today()
  └─ progress[].action = "Daily PDF generated"
  └─ progress[].result = "PDF with X pages"
```

### Experience Memory Entries

```
learning_optimizer creates:
  /remember solution     → Prediction errors + fixes
  /remember pattern      → Successful pattern matches
  /remember decision     → Model weight adjustments
  /remember gotcha       → Traps & lessons learned
```

## Related Documentation

- `multi-agent-orchestration-pattern.md` - Pattern template
- `macro-analyse` Scenario - Full setup
- Individual Agent Docs - See agent responsibilities

---

## Summary: The System Works Like This

```
1. EVERY HOUR:
   Collect data → Analyze (Technical, Macro, Meta) → Find patterns → Generate forecast → Update dashboard

2. EVERY DAY @ 18:00 {COUNTRY}:
   All of above + Learning review + Generate PDF report

3. EVERY WEEK:
   Deep learning analysis → Identify improvements → Adjust model weights

4. CONTINUOUSLY:
   Track prediction accuracy → Learn from errors → Self-improve
```

This is how Macro-Analyse leverages Evolving's multi-agent infrastructure to create a sophisticated, self-improving market analysis system.
