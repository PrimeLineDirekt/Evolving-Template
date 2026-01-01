# Multi-Source Aggregation Pattern

**Quelle**: github.com/replicate/hype
**Extrahiert**: 2025-12-30
**Tags**: aggregation, data-collection, parallel-fetch, normalization

---

## Problem

Daten aus mehreren heterogenen Quellen sammeln, normalisieren und vereinheitlicht speichern.

**Herausforderungen:**
- Verschiedene APIs mit unterschiedlichen Formaten
- Unterschiedliche Metriken (Stars, Likes, Upvotes, Run-Count)
- Spam/Noise filtern
- Idempotente Updates (keine Duplikate)

---

## Lösung

```
┌─────────────────────────────────────────────────┐
│              Trigger (Scheduled/Manual)          │
└─────────────────────┬───────────────────────────┘
                      │
      ┌───────────────┼───────────────┬───────────────┐
      ▼               ▼               ▼               ▼
┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐
│ Source A │   │ Source B │   │ Source C │   │ Source N │
│ Fetcher  │   │ Fetcher  │   │ Fetcher  │   │ Fetcher  │
└────┬─────┘   └────┬─────┘   └────┬─────┘   └────┬─────┘
     │              │              │              │
     └──────────────┴──────────────┴──────────────┘
                          │
                    Promise.all
                          │
                 ┌────────▼────────┐
                 │   Normalize to  │
                 │ Unified Schema  │
                 └────────┬────────┘
                          │
                 ┌────────▼────────┐
                 │  Score & Filter │
                 └────────┬────────┘
                          │
                 ┌────────▼────────┐
                 │ Idempotent Save │
                 └─────────────────┘
```

---

## Komponenten

### 1. Unified Item Interface

```typescript
interface AggregatedItem {
  id: string;           // Unique identifier
  source: string;       // Origin (github, reddit, api-x, ...)
  title: string;        // Display name
  author: string;       // Creator/Owner
  score: number;        // Normalized popularity metric
  description: string;  // Summary/excerpt
  url: string;          // Link to original
  created_at: string;   // ISO timestamp
  metadata?: Record<string, unknown>;  // Source-specific extras
}
```

### 2. Fetcher Interface

```typescript
interface SourceFetcher {
  name: string;
  fetch(config: FetchConfig): Promise<AggregatedItem[]>;
}

interface FetchConfig {
  since?: Date;         // Only items after this date
  limit?: number;       // Max items to fetch
  filters?: string[];   // Source-specific filters
}
```

### 3. Parallel Fetch Orchestrator

```typescript
async function fetchAllSources(
  fetchers: SourceFetcher[],
  config: FetchConfig
): Promise<AggregatedItem[]> {

  // Parallel execution
  const results = await Promise.all(
    fetchers.map(f => f.fetch(config).catch(err => {
      console.error(`Fetcher ${f.name} failed:`, err);
      return []; // Graceful degradation
    }))
  );

  // Flatten all results
  return results.flat();
}
```

### 4. Score Normalizer

Verschiedene Metriken auf gemeinsame Skala bringen:

```typescript
type ScoreNormalizer = (item: AggregatedItem) => number;

const normalizers: Record<string, ScoreNormalizer> = {
  // High-volume sources: dampen
  reddit: (item) => item.score * 0.3,

  // Log-scale for exponential metrics
  replicate: (item) => Math.pow(item.score, 0.6),

  // Linear passthrough
  github: (item) => item.score,

  // Custom per source
  hackernews: (item) => item.score * 2.5,
};

function normalizeScore(item: AggregatedItem): number {
  const normalizer = normalizers[item.source] || (i => i.score);
  return normalizer(item);
}
```

### 5. Content Filter

Spam, Scam, Irrelevantes rausfiltern:

```typescript
interface ContentFilter {
  bannedStrings?: string[];
  bannedPatterns?: RegExp[];
  minScore?: number;
  requiredFields?: string[];
  customFilter?: (item: AggregatedItem) => boolean;
}

function filterItems(
  items: AggregatedItem[],
  filter: ContentFilter
): AggregatedItem[] {
  return items.filter(item => {
    // Banned strings check
    const text = `${item.title} ${item.description}`.toLowerCase();
    for (const banned of filter.bannedStrings || []) {
      if (text.includes(banned)) return false;
    }

    // Min score check
    if (filter.minScore && item.score < filter.minScore) {
      return false;
    }

    // Required fields
    for (const field of filter.requiredFields || []) {
      if (!item[field as keyof AggregatedItem]) return false;
    }

    // Custom filter
    if (filter.customFilter && !filter.customFilter(item)) {
      return false;
    }

    return true;
  });
}
```

### 6. Idempotent Storage

```typescript
interface Storage {
  upsert(item: AggregatedItem): Promise<void>;
  query(options: QueryOptions): Promise<AggregatedItem[]>;
}

// Composite key prevents duplicates
const compositeKey = `${item.source}:${item.id}`;

// Upsert pattern (insert or update)
await storage.upsert(item, {
  onConflict: ['source', 'id']
});
```

---

## Vollständiges Beispiel

```typescript
// 1. Define fetchers
const fetchers: SourceFetcher[] = [
  {
    name: 'github',
    async fetch(config) {
      const resp = await fetch(
        `https://api.github.com/search/repositories?q=created:>${config.since?.toISOString().slice(0,10)}&sort=stars`
      );
      const data = await resp.json();
      return data.items.map(repo => ({
        id: repo.id.toString(),
        source: 'github',
        title: repo.full_name,
        author: repo.owner.login,
        score: repo.stargazers_count,
        description: repo.description || '',
        url: repo.html_url,
        created_at: repo.created_at,
      }));
    }
  },
  // ... more fetchers
];

// 2. Define filters
const filter: ContentFilter = {
  bannedStrings: ['crypto', 'nft', 'telegram'],
  minScore: 5,
  requiredFields: ['author', 'title'],
};

// 3. Aggregate
async function aggregate() {
  const since = new Date();
  since.setDate(since.getDate() - 7);

  // Fetch from all sources
  const items = await fetchAllSources(fetchers, { since });

  // Normalize scores
  const scored = items.map(item => ({
    ...item,
    score: normalizeScore(item),
  }));

  // Filter
  const filtered = filterItems(scored, filter);

  // Sort by normalized score
  filtered.sort((a, b) => b.score - a.score);

  // Save idempotently
  for (const item of filtered) {
    await storage.upsert(item);
  }

  return filtered;
}
```

---

## Anwendungsfälle

| Use Case | Sources | Score-Metrik |
|----------|---------|--------------|
| ML/AI News | GitHub, HuggingFace, Reddit | Stars, Likes, Upvotes |
| Tech Trends | HN, Reddit, Twitter/X | Points, Upvotes, Likes |
| Research Papers | arXiv, Semantic Scholar | Citations, Downloads |
| Knowledge Feed | RSS, APIs, Scraper | Recency, Relevance |
| Competitor Watch | GitHub, ProductHunt, Crunchbase | Activity, Funding |

---

## Varianten

### Time-Bucketed Aggregation

```typescript
type TimeBucket = 'past_day' | 'past_week' | 'past_month';

function getFromDate(bucket: TimeBucket): Date {
  const now = new Date();
  const days = { past_day: 1, past_week: 7, past_month: 30 };
  now.setDate(now.getDate() - days[bucket]);
  return now;
}
```

### Weighted Multi-Factor Score

```typescript
function calculateScore(item: AggregatedItem): number {
  const recencyWeight = getRecencyWeight(item.created_at); // 0-1
  const popularityWeight = normalizeScore(item) / 1000;    // 0-1
  const qualityWeight = item.metadata?.quality || 0.5;     // 0-1

  return (
    recencyWeight * 0.3 +
    popularityWeight * 0.5 +
    qualityWeight * 0.2
  ) * 100;
}
```

### Graceful Degradation

```typescript
async function fetchWithFallback(
  primary: SourceFetcher,
  fallback: SourceFetcher,
  config: FetchConfig
): Promise<AggregatedItem[]> {
  try {
    return await primary.fetch(config);
  } catch (err) {
    console.warn(`${primary.name} failed, using ${fallback.name}`);
    return fallback.fetch(config);
  }
}
```

---

## Best Practices

1. **Parallel, nicht Sequential** - Promise.all für unabhängige Sources
2. **Graceful Degradation** - Ein Fetcher-Fehler killt nicht alles
3. **Idempotent Writes** - Composite Key (source + id) für Upsert
4. **Score Normalization** - Verschiedene Metriken vergleichbar machen
5. **Content Filtering** - Spam früh rausfiltern
6. **Rate Limiting** - API-Limits respektieren
7. **Caching** - Ergebnisse cachen (z.B. 5min)

---

## Anti-Patterns

| Anti-Pattern | Problem | Lösung |
|--------------|---------|--------|
| Sequential Fetching | Langsam | Promise.all |
| Raw Score Comparison | Unfair (1000 Reddit ≠ 1000 GitHub) | Normalization |
| No Deduplication | Duplikate bei Re-runs | Upsert mit Composite Key |
| Fail-Fast | Ein Fehler stoppt alles | try/catch pro Fetcher |
| Unbounded Fetch | Memory-Explosion | Limits + Pagination |

---

## Related

- [Parallel Agent Dispatch Pattern](parallel-agent-dispatch-pattern.md)
- [Multi-Strategy Retrieval Pattern](multi-strategy-retrieval-pattern.md)
- [Idempotent Redundancy Rule](../../.claude/rules/idempotent-redundancy.md)
