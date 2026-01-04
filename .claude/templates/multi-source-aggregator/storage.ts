/**
 * Multi-Source Aggregator - Storage Backends
 *
 * Choose your storage: JSON file, SQLite, or Supabase.
 */

import type { AggregatedItem, Storage, QueryOptions } from './types';

// ============================================================
// JSON FILE STORAGE (Simple, Local)
// ============================================================

import * as fs from 'fs/promises';
import * as path from 'path';

export function jsonStorage(filePath: string): Storage {
  return {
    async upsert(item: AggregatedItem): Promise<void> {
      const items = await this.loadItems();
      const key = `${item.source}:${item.id}`;
      items[key] = item;
      await this.saveItems(items);
    },

    async upsertBatch(newItems: AggregatedItem[]): Promise<void> {
      const items = await this.loadItems();
      for (const item of newItems) {
        const key = `${item.source}:${item.id}`;
        items[key] = item;
      }
      await this.saveItems(items);
    },

    async query(options: QueryOptions): Promise<AggregatedItem[]> {
      const items = await this.loadItems();
      let result = Object.values(items);

      // Filter by sources
      if (options.sources?.length) {
        result = result.filter(i => options.sources!.includes(i.source));
      }

      // Filter by date
      if (options.since) {
        result = result.filter(i => new Date(i.created_at) >= options.since!);
      }

      // Sort
      const orderBy = options.orderBy || 'normalizedScore';
      const order = options.order || 'desc';
      result.sort((a, b) => {
        const aVal = a[orderBy] as number || 0;
        const bVal = b[orderBy] as number || 0;
        return order === 'desc' ? bVal - aVal : aVal - bVal;
      });

      // Limit
      if (options.limit) {
        result = result.slice(0, options.limit);
      }

      return result;
    },

    async getLastUpdated(): Promise<Date | null> {
      try {
        const stat = await fs.stat(filePath);
        return stat.mtime;
      } catch {
        return null;
      }
    },

    // Internal helpers
    async loadItems(): Promise<Record<string, AggregatedItem>> {
      try {
        const data = await fs.readFile(filePath, 'utf-8');
        return JSON.parse(data);
      } catch {
        return {};
      }
    },

    async saveItems(items: Record<string, AggregatedItem>): Promise<void> {
      await fs.mkdir(path.dirname(filePath), { recursive: true });
      await fs.writeFile(filePath, JSON.stringify(items, null, 2));
    },
  } as Storage & { loadItems: () => Promise<Record<string, AggregatedItem>>; saveItems: (items: Record<string, AggregatedItem>) => Promise<void> };
}

// ============================================================
// SUPABASE STORAGE (Production, Serverless)
// ============================================================

/*
import { createClient, SupabaseClient } from '@supabase/supabase-js';

export function supabaseStorage(url: string, key: string, table: string = 'items'): Storage {
  const client = createClient(url, key);

  return {
    async upsert(item: AggregatedItem): Promise<void> {
      const { error } = await client
        .from(table)
        .upsert(item, { onConflict: 'source,id' });
      if (error) throw error;
    },

    async upsertBatch(items: AggregatedItem[]): Promise<void> {
      const { error } = await client
        .from(table)
        .upsert(items, { onConflict: 'source,id' });
      if (error) throw error;
    },

    async query(options: QueryOptions): Promise<AggregatedItem[]> {
      let query = client.from(table).select('*');

      if (options.sources?.length) {
        query = query.in('source', options.sources);
      }
      if (options.since) {
        query = query.gt('created_at', options.since.toISOString());
      }

      const orderBy = options.orderBy || 'normalizedScore';
      query = query.order(orderBy, { ascending: options.order === 'asc' });

      if (options.limit) {
        query = query.limit(options.limit);
      }

      const { data, error } = await query;
      if (error) throw error;
      return data || [];
    },

    async getLastUpdated(): Promise<Date | null> {
      const { data } = await client.rpc('items_last_modified');
      return data ? new Date(data) : null;
    },
  };
}
*/

// ============================================================
// IN-MEMORY STORAGE (Testing)
// ============================================================

export function memoryStorage(): Storage {
  const items = new Map<string, AggregatedItem>();
  let lastUpdated: Date | null = null;

  return {
    async upsert(item: AggregatedItem): Promise<void> {
      items.set(`${item.source}:${item.id}`, item);
      lastUpdated = new Date();
    },

    async upsertBatch(newItems: AggregatedItem[]): Promise<void> {
      for (const item of newItems) {
        items.set(`${item.source}:${item.id}`, item);
      }
      lastUpdated = new Date();
    },

    async query(options: QueryOptions): Promise<AggregatedItem[]> {
      let result = Array.from(items.values());

      if (options.sources?.length) {
        result = result.filter(i => options.sources!.includes(i.source));
      }
      if (options.since) {
        result = result.filter(i => new Date(i.created_at) >= options.since!);
      }

      const orderBy = options.orderBy || 'normalizedScore';
      const order = options.order || 'desc';
      result.sort((a, b) => {
        const aVal = (a as any)[orderBy] || 0;
        const bVal = (b as any)[orderBy] || 0;
        return order === 'desc' ? bVal - aVal : aVal - bVal;
      });

      if (options.limit) {
        result = result.slice(0, options.limit);
      }

      return result;
    },

    async getLastUpdated(): Promise<Date | null> {
      return lastUpdated;
    },
  };
}
