/**
 * Multi-Source Aggregator - Main Orchestrator
 *
 * Coordinates fetching, normalizing, filtering, and storing.
 */

import type {
  AggregatedItem,
  FetchConfig,
  SourceFetcher,
  ContentFilter,
  NormalizerConfig,
  Storage
} from './types';
import { filterItems, defaultFilter } from './filter';
import { normalizeItems, defaultNormalizers } from './normalizer';

// ============================================================
// AGGREGATOR CONFIG
// ============================================================

export interface AggregatorConfig {
  fetchers: SourceFetcher[];
  storage: Storage;
  filter?: ContentFilter;
  normalizers?: NormalizerConfig;
  onFetcherError?: (fetcher: string, error: Error) => void;
}

// ============================================================
// MAIN AGGREGATOR
// ============================================================

export class Aggregator {
  private config: AggregatorConfig;

  constructor(config: AggregatorConfig) {
    this.config = config;
  }

  /**
   * Fetch from all sources, normalize, filter, and store.
   */
  async aggregate(fetchConfig?: FetchConfig): Promise<AggregatedItem[]> {
    const config = fetchConfig || { since: this.getDefaultSince() };

    // 1. Parallel fetch from all sources
    const items = await this.fetchAll(config);
    console.log(`Fetched ${items.length} items from ${this.config.fetchers.length} sources`);

    // 2. Normalize scores
    const normalized = normalizeItems(
      items,
      this.config.normalizers || defaultNormalizers
    );

    // 3. Filter content
    const filtered = filterItems(
      normalized,
      this.config.filter || defaultFilter
    );
    console.log(`After filtering: ${filtered.length} items`);

    // 4. Sort by normalized score
    filtered.sort((a, b) => (b.normalizedScore || 0) - (a.normalizedScore || 0));

    // 5. Store (idempotent upsert)
    await this.config.storage.upsertBatch(filtered);
    console.log(`Stored ${filtered.length} items`);

    return filtered;
  }

  /**
   * Fetch from all sources in parallel with graceful degradation.
   */
  private async fetchAll(config: FetchConfig): Promise<AggregatedItem[]> {
    const results = await Promise.all(
      this.config.fetchers.map(fetcher =>
        fetcher.fetch(config).catch(err => {
          console.error(`Fetcher ${fetcher.name} failed:`, err);
          this.config.onFetcherError?.(fetcher.name, err);
          return []; // Graceful degradation
        })
      )
    );

    return results.flat();
  }

  /**
   * Default: 7 days ago
   */
  private getDefaultSince(): Date {
    const date = new Date();
    date.setDate(date.getDate() - 7);
    return date;
  }
}

// ============================================================
// SCHEDULED AGGREGATION
// ============================================================

/**
 * Run aggregation on a schedule (for Cloudflare Workers, Node cron, etc.)
 */
export async function runScheduledAggregation(
  aggregator: Aggregator,
  options?: {
    sinceDays?: number;
    onComplete?: (items: AggregatedItem[]) => void;
    onError?: (error: Error) => void;
  }
): Promise<void> {
  try {
    const since = new Date();
    since.setDate(since.getDate() - (options?.sinceDays || 7));

    const items = await aggregator.aggregate({ since });

    console.log(`Scheduled aggregation complete: ${items.length} items`);
    options?.onComplete?.(items);

  } catch (error) {
    console.error('Scheduled aggregation failed:', error);
    options?.onError?.(error as Error);
  }
}

// ============================================================
// USAGE EXAMPLE
// ============================================================

/*
import { githubFetcher, redditFetcher, huggingfaceFetcher } from './fetcher';
import { jsonStorage } from './storage';

const aggregator = new Aggregator({
  fetchers: [githubFetcher, redditFetcher, huggingfaceFetcher],
  storage: jsonStorage('./data/items.json'),
  filter: {
    bannedStrings: ['crypto', 'nft'],
    minScore: 5,
  },
});

// Manual run
const items = await aggregator.aggregate();

// Scheduled (every hour)
setInterval(() => runScheduledAggregation(aggregator), 60 * 60 * 1000);
*/
