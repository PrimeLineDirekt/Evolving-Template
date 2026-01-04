# /pattern-scan

Scan current market setup against historical pattern library.

## Model: sonnet

## Workflow

1. Extract key characteristics of current setup
2. Compare against pattern library
3. Find matches (election cycles, CPI lag, sentiment extremes, etc.)
4. Retrieve historical outcomes
5. Calculate probability of repetition
6. Output: Pattern matches with historical context

## Output Format

```
## Pattern Scan Results

### Pattern 1: Election Cycle Pattern
Match Score: 87/100
Historical Outcomes:
  - 2020: BTC +125% in 6 months
  - 2016: BTC +156% in 6 months
  - 2012: BTC +79% in 6 months

Current Probability: 75%

### Pattern 2: CPI Shelter Lag Pattern
Match Score: 72/100
Real Rents: -2.3% YoY (falling)
CPI Shelter: +6.1% YoY (still rising)
Historical: When real rents fall, CPI catches up in 6 months

Probability: 80% CPI shelter falls within 6 months

### Pattern 3: Sentiment Extremes
Match Score: 65/100
Fear & Greed: 18 (Extreme Fear)
Historical: Last 5 times <20 → +100-1,500% in 6 months

Probability: 70% bottom forming

### Summary
Multiple bullish patterns aligning.
High probability setup for sustained rally.
Confidence: 75%
```

## Usage

```
/pattern-scan
/pattern-scan BTC
/pattern-scan detailed
```

## Plain Text Trigger

- "Finde Muster"
- "Historische Muster"
- "Welche Muster sieht du?"
