/**
 * Multi-Source Aggregator - Type Definitions
 *
 * Customize AggregatedItem fields for your domain.
 */

// ============================================================
// CORE TYPES - Customize for your domain
// ============================================================

export interface AggregatedItem {
  id: string;                    // Unique identifier (source-specific)
  source: string;                // Origin: "github" | "reddit" | "api-x" | ...
  title: string;                 // Display name
  author: string;                // Creator/Owner
  score: number;                 // Raw popularity metric (stars, upvotes, etc.)
  normalizedScore?: number;      // After normalization (filled by normalizer)
  description: string;           // Summary/excerpt
  url: string;                   // Link to original
  created_at: string;            // ISO timestamp

  // Optional: Add domain-specific fields
  metadata?: Record<string, unknown>;
  tags?: string[];
  category?: string;
}

// ============================================================
// FETCHER TYPES
// ============================================================

export interface FetchConfig {
  since?: Date;          // Only items after this date
  limit?: number;        // Max items to fetch (default: 100)
  filters?: string[];    // Source-specific filters
}

export interface SourceFetcher {
  name: string;
  fetch(config: FetchConfig): Promise<AggregatedItem[]>;
}

// ============================================================
// FILTER TYPES
// ============================================================

export interface ContentFilter {
  bannedStrings?: string[];      // ["crypto", "nft", "spam"]
  bannedPatterns?: RegExp[];     // [/telegram.*bot/i]
  minScore?: number;             // Minimum raw score
  requiredFields?: (keyof AggregatedItem)[];  // ["author", "title"]
  maxAge?: number;               // Max age in days
  customFilter?: (item: AggregatedItem) => boolean;
}

// ============================================================
// STORAGE TYPES
// ============================================================

export interface QueryOptions {
  sources?: string[];            // Filter by sources
  since?: Date;                  // Items after date
  limit?: number;                // Max results
  orderBy?: 'score' | 'normalizedScore' | 'created_at';
  order?: 'asc' | 'desc';
}

export interface Storage {
  upsert(item: AggregatedItem): Promise<void>;
  upsertBatch(items: AggregatedItem[]): Promise<void>;
  query(options: QueryOptions): Promise<AggregatedItem[]>;
  getLastUpdated(): Promise<Date | null>;
}

// ============================================================
// NORMALIZER TYPES
// ============================================================

export type ScoreNormalizer = (item: AggregatedItem) => number;

export interface NormalizerConfig {
  [source: string]: ScoreNormalizer;
}
