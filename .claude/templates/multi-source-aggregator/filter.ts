/**
 * Multi-Source Aggregator - Content Filtering
 *
 * Remove spam, scams, and low-quality content.
 */

import type { AggregatedItem, ContentFilter } from './types';

// ============================================================
// DEFAULT FILTER CONFIG
// ============================================================

export const defaultFilter: ContentFilter = {
  bannedStrings: [
    'crypto', 'nft', 'telegram', 'solana',
    'stealer', 'hack', 'crack', 'keygen'
  ],
  bannedPatterns: [
    /telegram.*bot/i,
    /free.*money/i,
    /\$\d+.*passive/i,
  ],
  minScore: 1,
  requiredFields: ['author', 'title'],
  maxAge: 30, // days
};

// ============================================================
// FILTER FUNCTION
// ============================================================

export function filterItems(
  items: AggregatedItem[],
  config: ContentFilter = defaultFilter
): AggregatedItem[] {
  return items.filter(item => isValidItem(item, config));
}

export function isValidItem(
  item: AggregatedItem,
  config: ContentFilter = defaultFilter
): boolean {
  const text = `${item.title} ${item.description}`.toLowerCase();

  // Check banned strings
  for (const banned of config.bannedStrings || []) {
    if (text.includes(banned.toLowerCase())) {
      return false;
    }
  }

  // Check banned patterns
  for (const pattern of config.bannedPatterns || []) {
    if (pattern.test(text)) {
      return false;
    }
  }

  // Check minimum score
  if (config.minScore !== undefined && item.score < config.minScore) {
    return false;
  }

  // Check required fields
  for (const field of config.requiredFields || []) {
    const value = item[field];
    if (value === undefined || value === null || value === '') {
      return false;
    }
  }

  // Check max age
  if (config.maxAge !== undefined) {
    const ageInDays = (Date.now() - new Date(item.created_at).getTime()) / (1000 * 60 * 60 * 24);
    if (ageInDays > config.maxAge) {
      return false;
    }
  }

  // Custom filter
  if (config.customFilter && !config.customFilter(item)) {
    return false;
  }

  return true;
}

// ============================================================
// FILTER BUILDER (Fluent API)
// ============================================================

export class FilterBuilder {
  private config: ContentFilter = {};

  ban(...strings: string[]): this {
    this.config.bannedStrings = [
      ...(this.config.bannedStrings || []),
      ...strings
    ];
    return this;
  }

  banPattern(...patterns: RegExp[]): this {
    this.config.bannedPatterns = [
      ...(this.config.bannedPatterns || []),
      ...patterns
    ];
    return this;
  }

  minScore(score: number): this {
    this.config.minScore = score;
    return this;
  }

  require(...fields: (keyof AggregatedItem)[]): this {
    this.config.requiredFields = fields;
    return this;
  }

  maxAgeDays(days: number): this {
    this.config.maxAge = days;
    return this;
  }

  custom(fn: (item: AggregatedItem) => boolean): this {
    this.config.customFilter = fn;
    return this;
  }

  build(): ContentFilter {
    return this.config;
  }
}

// Usage:
// const filter = new FilterBuilder()
//   .ban('crypto', 'nft')
//   .minScore(10)
//   .require('author', 'title')
//   .maxAgeDays(7)
//   .build();
