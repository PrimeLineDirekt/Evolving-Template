# Browser Automation Pattern

> **Typ**: Infrastructure Pattern
> **Anwendung**: Web Scraping, Browser Automation, Data Extraction

---

## Problem

Langsame, sequentielle Browser-Operationen bei Web Scraping und Automation.

## Lösung

Multi-Tab Parallelisierung mit strukturierter Datenextraktion.

---

## Pattern-Struktur

```
┌─────────────────────────────────────────────────┐
│                  ORCHESTRATOR                    │
│  (Claude Code Main Thread)                       │
└─────────────────┬───────────────────────────────┘
                  │
    ┌─────────────┼─────────────┐
    │             │             │
    ▼             ▼             ▼
┌───────┐   ┌───────┐   ┌───────┐
│ Tab 1 │   │ Tab 2 │   │ Tab N │
│ URL A │   │ URL B │   │ URL N │
└───┬───┘   └───┬───┘   └───┬───┘
    │           │           │
    ▼           ▼           ▼
┌───────────────────────────────┐
│     PARALLEL EXTRACTION       │
│  (JavaScript / get_page_text) │
└───────────────────────────────┘
                │
                ▼
        ┌───────────────┐
        │   AGGREGATOR   │
        │ (Results merge)│
        └───────────────┘
```

---

## Implementierung

### Phase 1: Tab Pool erstellen

```
# N Tabs parallel erstellen
tabs_create_mcp × N  (in einem Tool-Call Block)
```

**Empfohlen:** 4-8 Tabs für optimale Performance.

### Phase 2: Parallel Navigation

```
# Alle URLs gleichzeitig laden
navigate(url_1, tab_1)
navigate(url_2, tab_2)
...
navigate(url_N, tab_N)
```

**Wichtig:** Alle Calls in EINEM Block für echte Parallelität.

### Phase 3: Wait (optional)

```
wait(1-2 seconds)
```

Gibt dynamischen Seiten Zeit zum Laden.

### Phase 4: Parallel Extraction

```
# Option A: Text extrahieren
get_page_text(tab_1)
get_page_text(tab_2)
...

# Option B: Strukturierte Daten (EMPFOHLEN)
javascript_tool(extraction_script, tab_1)
javascript_tool(extraction_script, tab_2)
...
```

### Phase 5: Aggregate

Ergebnisse zusammenführen und verarbeiten.

---

## Extraction Scripts

### Links extrahieren

```javascript
Array.from(document.querySelectorAll('a[href]'))
  .map(a => ({ text: a.textContent.trim(), url: a.href }))
  .filter(l => l.text && l.url)
```

### Tabellen extrahieren

```javascript
Array.from(document.querySelectorAll('table'))
  .map(table => ({
    headers: Array.from(table.querySelectorAll('th')).map(th => th.textContent.trim()),
    rows: Array.from(table.querySelectorAll('tr')).slice(1).map(row =>
      Array.from(row.cells).map(cell => cell.textContent.trim())
    )
  }))
```

### Produkt-Listings (E-Commerce)

```javascript
Array.from(document.querySelectorAll('[data-product], .product, .listing'))
  .map(el => ({
    title: el.querySelector('h1,h2,h3,.title')?.textContent?.trim(),
    price: el.querySelector('.price,[data-price]')?.textContent?.trim(),
    image: el.querySelector('img')?.src
  }))
```

### Meta-Daten

```javascript
({
  title: document.title,
  description: document.querySelector('meta[name="description"]')?.content,
  canonical: document.querySelector('link[rel="canonical"]')?.href,
  ogImage: document.querySelector('meta[property="og:image"]')?.content
})
```

---

## Error Recovery

### Tab Unresponsive

```
Problem erkannt
     │
     ▼
tabs_create_mcp (neuer Tab)
     │
     ▼
navigate(same_url, new_tab)
     │
     ▼
Alte Tab-ID ignorieren
```

### Modal Dialog

```
Operation blockiert
     │
     ▼
User: Dismiss Dialog manuell
     │
     ▼
Claude: "continue"
```

### Network Error

```
Timeout/Error erkannt
     │
     ▼
wait(2)
     │
     ▼
navigate(url) (Retry)
```

---

## Wann NICHT verwenden

| Situation | Alternative |
|-----------|-------------|
| Einfache statische Seite | `WebFetch` (native) |
| API verfügbar | Direkte API-Calls |
| Login nicht möglich | `Puppeteer MCP` mit Credentials |
| Headless erforderlich | `Puppeteer MCP` |

---

## Performance-Charakteristiken

| Tabs | URLs | Geschätzte Zeit | Speedup |
|------|------|-----------------|---------|
| 1 | 10 | ~30s | 1x |
| 4 | 10 | ~8s | 3.75x |
| 8 | 10 | ~5s | 6x |

---

## Beispiel: Online-Shop Scrapen

```python
# 1. Shop-Seite laden
navigate("https://example-shop.com", tab_1)

# 2. Listing-URLs extrahieren
urls = javascript_tool("""
  Array.from(document.querySelectorAll('a[href*="/product/"]'))
    .slice(0, 10)
    .map(a => a.href.split('?')[0])
""", tab_1)

# 3. Zusätzliche Tabs erstellen
tabs_create_mcp × 3

# 4. Parallel laden (4 Tabs, 10 URLs in Batches)
# Batch 1
navigate(urls[0], tab_1)
navigate(urls[1], tab_2)
navigate(urls[2], tab_3)
navigate(urls[3], tab_4)

# 5. Parallel extrahieren
javascript_tool(listing_details_script, tab_1)
javascript_tool(listing_details_script, tab_2)
javascript_tool(listing_details_script, tab_3)
javascript_tool(listing_details_script, tab_4)

# 6. Wiederholen für Batch 2, 3...
```

---

## Neue Patterns (aus Experimenten 2025-12-19)

### Cross-Tab Messaging Pattern

Tabs der gleichen Domain können über localStorage kommunizieren:

```javascript
// Tab 1: Nachricht senden
const msg = { from: 'tab1', action: 'scrape_complete', data: { count: 5 } };
localStorage.setItem('cross_tab_msg', JSON.stringify(msg));

// Tab 2: Nachricht empfangen
const received = JSON.parse(localStorage.getItem('cross_tab_msg'));
```

**Use Case**: Koordination bei Multi-Site Scraping (z.B. "Tab 1 fertig, Tab 2 kann weiter").

### Console Debugging Pattern

Statt `alert()` (blockiert Tab!) immer `console.log` nutzen:

```javascript
// NICHT: alert('Debug info');  // ❌ Tab blockiert!

// STATTDESSEN:
console.log('[DEBUG] Extraction done:', result);
console.error('[ERROR] Failed:', error);

// Dann auslesen mit:
read_console_messages(tabId, pattern='DEBUG')
```

### Form Automation Pattern

Alle Standard-Formulartypen mit `form_input`:

```javascript
// Text/Email/Tel
form_input(ref_1, "Claude Test User")

// Radio Button (Value des gewünschten)
form_input(ref_5, "medium")

// Checkbox (Boolean)
form_input(ref_7, true)

// Time Input (Format HH:MM)
form_input(ref_11, "18:30")

// Textarea
form_input(ref_12, "Long text...")
```

### Context Optimization Pattern

Output-Größen beachten:

| Operation | Output | Wann nutzen |
|-----------|--------|-------------|
| `javascript_tool` | Minimal | Gezielte Daten |
| `read_page` (interactive) | ~2KB | Navigation |
| `get_page_text` | ~4KB | Content |
| `read_page` (full) | ~15KB+ | Komplette Struktur |

---

## Verifizierte Grenzen

| Feature | Status |
|---------|--------|
| Max Tabs getestet | 12+ (stabil) |
| Modal Dialogs | ❌ Blockieren Tab |
| Cookies | ❌ Blockiert |
| Cross-Origin Fetch | ✅ Funktioniert |
| Screenshots | ⚠️ Nur Viewport |

---

## Related Patterns

- **Batch Processing Pattern** - Große Datenmengen verarbeiten
- **Error Recovery Pattern** - Robuste Fehlerbehandlung
- **Context Optimization Pattern** - Token-Verbrauch minimieren

---

## Related Documentation

- `knowledge/learnings/chrome-experiments-results.md` - 10 Experimente
- `knowledge/learnings/chrome-automation-best-practices.md` - Best Practices

---

**Version**: 1.1
**Erstellt**: 2025-12-19
**Updated**: 2025-12-19 (Neue Patterns aus Experimenten)
