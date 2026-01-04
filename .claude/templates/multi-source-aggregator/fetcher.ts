/**
 * Multi-Source Aggregator - Fetcher Examples
 *
 * Implement your own fetchers following this pattern.
 */

import type { AggregatedItem, FetchConfig, SourceFetcher } from './types';

// ============================================================
// EXAMPLE: GitHub Fetcher
// ============================================================

export const githubFetcher: SourceFetcher = {
  name: 'github',

  async fetch(config: FetchConfig): Promise<AggregatedItem[]> {
    const since = config.since?.toISOString().slice(0, 10) || getDefaultSince();
    const limit = config.limit || 100;

    const resp = await fetch(
      `https://api.github.com/search/repositories?q=language:python+created:>${since}&sort=stars&order=desc&per_page=${limit}`,
      { headers: { 'User-Agent': 'my-aggregator' } }
    );

    if (!resp.ok) throw new Error(`GitHub API error: ${resp.status}`);

    const data = await resp.json() as { items: any[] };

    return data.items.map(repo => ({
      id: repo.id.toString(),
      source: 'github',
      title: repo.full_name,
      author: repo.owner.login,
      score: repo.stargazers_count,
      description: repo.description || '',
      url: repo.html_url,
      created_at: repo.created_at,
      metadata: {
        language: repo.language,
        forks: repo.forks_count,
      }
    }));
  }
};

// ============================================================
// EXAMPLE: Reddit Fetcher
// ============================================================

export const redditFetcher: SourceFetcher = {
  name: 'reddit',

  async fetch(config: FetchConfig): Promise<AggregatedItem[]> {
    const subreddits = config.filters || ['machinelearning', 'localllama'];
    const items: AggregatedItem[] = [];

    for (const subreddit of subreddits) {
      try {
        const resp = await fetch(
          `https://www.reddit.com/r/${subreddit}/top.json?sort=top&t=week&limit=50`,
          { headers: { 'User-Agent': 'my-aggregator' } }
        );

        if (!resp.ok) continue;

        const data = await resp.json() as any;

        for (const post of data.data?.children || []) {
          const { title, author, subreddit: sub, score, created_utc, id, permalink } = post.data;

          items.push({
            id: id,
            source: 'reddit',
            title: title,
            author: author,
            score: score,
            description: `/r/${sub}`,
            url: `https://www.reddit.com${permalink}`,
            created_at: new Date(created_utc * 1000).toISOString(),
            metadata: { subreddit: sub }
          });
        }
      } catch (err) {
        console.error(`Error fetching r/${subreddit}:`, err);
      }
    }

    return items;
  }
};

// ============================================================
// EXAMPLE: HuggingFace Fetcher
// ============================================================

export const huggingfaceFetcher: SourceFetcher = {
  name: 'huggingface',

  async fetch(config: FetchConfig): Promise<AggregatedItem[]> {
    const limit = config.limit || 100;

    const resp = await fetch(
      `https://huggingface.co/api/models?full=true&limit=${limit}&sort=lastModified&direction=-1`
    );

    if (!resp.ok) throw new Error(`HuggingFace API error: ${resp.status}`);

    const models = await resp.json() as any[];

    return models
      .filter(m => m.likes > 0 && m.author)
      .map(model => ({
        id: model._id,
        source: 'huggingface',
        title: model.id,
        author: model.author,
        score: model.likes,
        description: model.pipeline_tag || '',
        url: `https://huggingface.co/${model.id}`,
        created_at: model.lastModified,
        metadata: {
          downloads: model.downloads,
          pipeline: model.pipeline_tag,
        }
      }));
  }
};

// ============================================================
// TEMPLATE: Custom API Fetcher
// ============================================================

export function createApiFetcher(
  name: string,
  apiUrl: string,
  mapper: (item: any) => AggregatedItem
): SourceFetcher {
  return {
    name,
    async fetch(config: FetchConfig): Promise<AggregatedItem[]> {
      const resp = await fetch(apiUrl);
      if (!resp.ok) throw new Error(`${name} API error: ${resp.status}`);

      const data = await resp.json() as any[];
      return data.map(mapper);
    }
  };
}

// ============================================================
// HELPER
// ============================================================

function getDefaultSince(): string {
  const date = new Date();
  date.setDate(date.getDate() - 7);
  return date.toISOString().slice(0, 10);
}
