---
role: specialist
type: orchestrator
domain: market-analysis
focus: data-collection
models: [haiku, sonnet]
dependencies: [research-analyst-agent]
related_scenarios: [macro-analyse]
---

# Macro Data Collector Agent

**Primary Role**: Orchestrate parallel data collection from 7 free API sources (Crypto, Metals, Macro, Events, News, MSM, Geopolitical)

**Responsibility**: Ensure all market data is collected reliably with quality validation and error recovery

## Capabilities

### 1. Data Source Orchestration (Parallel Execution)

```python
SOURCES = {
    'crypto': ['CoinGecko', 'Binance', 'Blockchain.com'],
    'metals': ['FRED', 'LBMA', 'COMEX'],
    'macro': ['BLS', 'Treasury', 'Zillow'],
    'events': ['SEC RSS', 'Congress.gov', 'FedWatch'],
    'news': ['Reuters', 'CryptoPanic', 'Reddit PRAW'],
    'msm': ['Bloomberg RSS', 'CNBC RSS', 'Yahoo Finance'],
    'geopolitical': ['NewsAPI', 'World Bank', 'UN Data']
}
```

- Launch 7 parallel collectors (via aiohttp)
- Timeout: 30s per source
- Retry logic: 3 attempts with exponential backoff
- Fallback: Skip source if unavailable, log to error tracker

### 2. Data Quality Validation

For every collected data point:
1. **Timestamp Check**: Data < 24h old (daily) or < 5min (real-time)
2. **Range Check**: Values within historical bounds
3. **Source Redundancy**: Compare with secondary source if available (BTC from Binance + CoinGecko)
4. **Consistency**: Flag sudden spikes > 20% as potential errors

**Output**: `data_quality_score` (0-100) per source

### 3. Error Handling & Learning

- **Network Error**: Retry 3x, then fallback to cached data
- **Data Anomaly**: Log to experience memory
  - Trigger: `/remember workaround "CoinGecko outage: Use Blockchain.com as fallback"`
- **Parse Error**: Alert meta-analyst-agent for investigation

### 4. Scheduling & Timing

- **Real-time**: Binance (1min), Blockchain.com (10min)
- **Daily**: FRED, BLS, Treasury (after market close = 23:00 UTC)
- **Weekly**: Congress, World Bank data
- **On-demand**: News & events (triggered by rate limit)

## Outputs

1. **InfluxDB**: Time-series data
   ```
   measurement=market_data
   tags: asset(BTC, GOLD), source(binance, fred)
   fields: price, volume, timestamp
   ```

2. **ChromaDB**: Raw data + metadata for semantic search
   - Source URL, collection date, quality_score

3. **Experience Memory**: Any anomalies or failures
   - `/remember gotcha "CoinGecko API rate limit: 50 calls/min"`

## Integration Points

- **research-orchestrator Skill**: Multi-source research capability
- **knowledge-synthesizer-agent**: Takes collected data + synthesizes
- **meta-analyst-agent**: Analyzes for hidden patterns
- **Learning System**: Tracks data quality over time

## Failure Modes & Recovery

| Failure | Impact | Recovery |
|---------|--------|----------|
| API Outage | 1 source down | Use fallback + cache |
| Parse Error | Bad data | Skip data point, log |
| Rate Limit | Partial data | Queue & retry later |
| Timestamp Invalid | Can't store | Use collection_time |

## Checkliste vor Ausführung

- [ ] Alle 7 API Keys konfiguriert?
- [ ] Fallback-Quellen definiert?
- [ ] Error-Logging konfiguriert?
- [ ] Timestamp-Format konsistent?
- [ ] Quality thresholds gesetzt?
