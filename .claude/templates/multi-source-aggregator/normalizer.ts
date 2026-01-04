/**
 * Multi-Source Aggregator - Score Normalization
 *
 * Different sources have different metrics.
 * Normalize them to a comparable scale.
 */

import type { AggregatedItem, NormalizerConfig, ScoreNormalizer } from './types';

// ============================================================
// DEFAULT NORMALIZERS
// ============================================================

/**
 * Configure score normalization per source.
 *
 * Problem: 1000 Reddit upvotes ≠ 1000 GitHub stars
 * Solution: Apply source-specific transformations
 */
export const defaultNormalizers: NormalizerConfig = {
  // Reddit: High volume, dampen by 0.3
  reddit: (item) => item.score * 0.3,

  // Replicate: Exponential distribution, use log-scale
  replicate: (item) => Math.pow(item.score, 0.6),

  // GitHub: Linear passthrough (baseline)
  github: (item) => item.score,

  // HuggingFace: Similar to GitHub
  huggingface: (item) => item.score,

  // HackerNews: High signal, boost slightly
  hackernews: (item) => item.score * 1.5,

  // Default: Linear passthrough
  default: (item) => item.score,
};

// ============================================================
// NORMALIZER FUNCTION
// ============================================================

export function normalizeScore(
  item: AggregatedItem,
  config: NormalizerConfig = defaultNormalizers
): number {
  const normalizer = config[item.source] || config.default || ((i) => i.score);
  return normalizer(item);
}

export function normalizeItems(
  items: AggregatedItem[],
  config: NormalizerConfig = defaultNormalizers
): AggregatedItem[] {
  return items.map(item => ({
    ...item,
    normalizedScore: normalizeScore(item, config),
  }));
}

// ============================================================
// ADVANCED: Multi-Factor Scoring
// ============================================================

interface ScoringWeights {
  popularity: number;  // Raw score weight
  recency: number;     // Time decay weight
  quality: number;     // Quality signal weight (if available)
}

const defaultWeights: ScoringWeights = {
  popularity: 0.5,
  recency: 0.3,
  quality: 0.2,
};

/**
 * Calculate weighted multi-factor score.
 *
 * Combines popularity, recency, and quality signals.
 */
export function calculateMultiFactorScore(
  item: AggregatedItem,
  weights: ScoringWeights = defaultWeights
): number {
  // Popularity (normalized to 0-1)
  const maxScore = 10000; // Adjust based on your data
  const popularityScore = Math.min(item.score / maxScore, 1);

  // Recency (exponential decay)
  const ageInDays = (Date.now() - new Date(item.created_at).getTime()) / (1000 * 60 * 60 * 24);
  const recencyScore = Math.exp(-ageInDays / 7); // Half-life of 7 days

  // Quality (from metadata if available)
  const qualityScore = (item.metadata?.quality as number) ?? 0.5;

  // Weighted combination
  return (
    popularityScore * weights.popularity +
    recencyScore * weights.recency +
    qualityScore * weights.quality
  ) * 100;
}
