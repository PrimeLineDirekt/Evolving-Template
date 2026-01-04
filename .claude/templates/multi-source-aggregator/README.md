# Multi-Source Aggregator Template

**Source**: replicate/hype
**Use Case**: News Feeds, Trend Tracking, Knowledge Aggregation

## Dateien

```
multi-source-aggregator/
├── README.md           # Diese Datei
├── types.ts            # Unified Item Interface
├── fetcher.ts          # Fetcher Interface + Beispiele
├── normalizer.ts       # Score Normalization
├── filter.ts           # Content Filtering
├── aggregator.ts       # Orchestrator
└── storage.ts          # Idempotent Storage
```

## Quick Start

1. Kopiere Template-Dateien in dein Projekt
2. Passe `types.ts` an dein Domain-Model an
3. Implementiere Fetcher für deine Quellen
4. Konfiguriere Filter und Normalizer
5. Wähle Storage-Backend (Supabase, SQLite, JSON)

## Customization Points

| Datei | Was anpassen? |
|-------|---------------|
| `types.ts` | Felder im `AggregatedItem` erweitern |
| `fetcher.ts` | Neue Quellen hinzufügen |
| `normalizer.ts` | Score-Gewichtung pro Quelle |
| `filter.ts` | Banned Strings, Min-Score |
| `storage.ts` | Backend wählen (Supabase/SQLite/JSON) |
