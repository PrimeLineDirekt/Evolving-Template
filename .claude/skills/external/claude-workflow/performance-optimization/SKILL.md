
---
name: performance-optimization
description: Guides performance analysis and optimization for any application. Use when diagnosing slowness, optimizing code, improving load times, or when asked about performance.
---

# Performance Optimization Skill

## Performance Analysis Process

### 1. Measure First
Never optimize without data. Always profile before changing code.

```bash
# Node.js profiling
node --prof app.js
node --prof-process isolate*.log > profile.txt

# Python profiling
python -m cProfile -o profile.stats app.py
python -m pstats profile.stats

# Web performance
lighthouse https://example.com --output=json
```

### 2. Identify Bottlenecks

#### Common Bottleneck Categories
| Category | Symptoms | Tools |
|----------|----------|-------|
| CPU | High CPU usage, slow computation | Profiler, flame graphs |
| Memory | High RAM, GC pauses, OOM | Heap snapshots, memory profiler |
| I/O | Slow disk/network, waiting | strace, network inspector |
| Database | Slow queries, lock contention | Query analyzer, EXPLAIN |

### 3. Apply Optimizations

## Frontend Optimizations

### Bundle Size
```javascript
// BAD: Import entire library
import _ from 'lodash';

// GOOD: Import only needed functions
import debounce from 'lodash/debounce';

// GOOD: Use dynamic imports for code splitting
const HeavyComponent = lazy(() => import('./HeavyComponent'));
```

### Rendering
```javascript
// BAD: Render on every parent update
function Child({ data }) {
  return <ExpensiveComponent data={data} />;
}

// GOOD: Memoize when props don't change
const Child = memo(function Child({ data }) {
  return <ExpensiveComponent data={data} />;
});

// GOOD: Use useMemo for expensive computations
const processed = useMemo(() => expensiveCalc(data), [data]);
```

### Images
```html
<!-- BAD: Unoptimized -->
<img src="large-image.jpg" />

<!-- GOOD: Optimized -->
<img
  src="image.webp"
  srcset="image-300.webp 300w, image-600.webp 600w"
  sizes="(max-width: 600px) 300px, 600px"
  loading="lazy"
  decoding="async"
/>
```

## Backend Optimizations

### Database Queries
```sql
-- BAD: N+1 Query Problem
SELECT * FROM users;
-- Then for each user:
SELECT * FROM orders WHERE user_id = ?;

-- GOOD: Single query with JOIN
SELECT u.*, o.*
FROM users u
LEFT JOIN orders o ON u.id = o.user_id;

-- GOOD: Or use pagination
SELECT * FROM users LIMIT 100 OFFSET 0;
```

### Caching Strategy
```javascript
// Multi-layer caching
const getUser = async (id) => {
  // L1: In-memory cache (fastest)
  let user = memoryCache.get(`user:${id}`);
  if (user) return user;

  // L2: Redis cache (fast)
  user = await redis.get(`user:${id}`);
  if (user) {
    memoryCache.set(`user:${id}`, user, 60);
    return JSON.parse(user);
  }

  // L3: Database (slow)
  user = await db.users.findById(id);
  await redis.setex(`user:${id}`, 3600, JSON.stringify(user));
  memoryCache.set(`user:${id}`, user, 60);

  return user;
};
```

### Async Processing
```javascript
// BAD: Blocking operation
app.post('/upload', async (req, res) => {
  await processVideo(req.file);  // Takes 5 minutes
  res.send('Done');
});

// GOOD: Queue for background processing
app.post('/upload', async (req, res) => {
  const jobId = await queue.add('processVideo', { file: req.file });
  res.send({ jobId, status: 'processing' });
});
```

## Algorithm Optimizations

### Time Complexity Improvements
```javascript
// BAD: O(n^2) - nested loops
function findDuplicates(arr) {
  const duplicates = [];
  for (let i = 0; i < arr.length; i++) {
    for (let j = i + 1; j < arr.length; j++) {
      if (arr[i] === arr[j]) duplicates.push(arr[i]);
    }
  }
  return duplicates;
}

// GOOD: O(n) - hash map
function findDuplicates(arr) {
  const seen = new Set();
  const duplicates = new Set();
  for (const item of arr) {
    if (seen.has(item)) duplicates.add(item);
    seen.add(item);
  }
  return [...duplicates];
}
```

## Performance Metrics

### Web Vitals (Target Values)
| Metric | Good | Needs Work | Poor |
|--------|------|------------|------|
| LCP | < 2.5s | 2.5-4s | > 4s |
| FID | < 100ms | 100-300ms | > 300ms |
| CLS | < 0.1 | 0.1-0.25 | > 0.25 |
| TTFB | < 800ms | 800ms-1.8s | > 1.8s |

### API Performance (Target Values)
| Metric | Target |
|--------|--------|
| P50 Latency | < 100ms |
| P95 Latency | < 500ms |
| P99 Latency | < 1s |
| Error Rate | < 0.1% |
