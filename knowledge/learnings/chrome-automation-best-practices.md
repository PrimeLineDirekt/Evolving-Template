# Chrome Automation Best Practices

> **Source**: Stresstest + Community Research (Dez 2025)
> **Relevanz**: Hoch - Effektive Browser-Automation mit Claude Code

---

## Zusammenfassung

Chrome-Integration ist leistungsfähiger als erwartet:
- **Parallele Operationen funktionieren** (8+ Tabs getestet)
- **Multi-Tab Navigation + Extraktion** in einem Schritt möglich
- **Speedup ~4x** bei 4 parallelen Tabs vs. sequentiell

---

## Performance-Optimierungen

### 1. Multi-Tab Parallelisierung (EMPFOHLEN)

```
Statt: 1 Tab × 10 URLs sequentiell (~30s)
Besser: 4 Tabs × 10 URLs parallel (~8s)
```

**Pattern:**
1. N Tabs erstellen mit `tabs_create_mcp`
2. Parallel navigieren (alle `navigate` Calls in einem Block)
3. Kurz warten (1-2s)
4. Parallel extrahieren (alle `get_page_text` oder `javascript_tool` Calls in einem Block)

**Getestet:** 8 Tabs stabil, wahrscheinlich mehr möglich.

### 2. JavaScript-Extraktion statt get_page_text

Für strukturierte Daten ist `javascript_tool` effizienter:

```javascript
// Extrahiert nur was gebraucht wird
Array.from(document.querySelectorAll('a')).slice(0,10).map(a => ({
  title: a.textContent.trim(),
  url: a.href
}))
```

**Vorteil:** Weniger Token-Verbrauch, präzisere Daten.

### 3. Fresh Tabs statt Reuse

Bei Problemen:
- Neuen Tab erstellen
- Alten Tab ignorieren
- Nicht versuchen unresponsive Tabs zu reparieren

### 4. Console-Filter nutzen

```
Statt: "Check the console"
Besser: "Check the console for TypeError or network errors"
```

Spart Context-Tokens bei verbose Logs.

---

## Bekannte Limitierungen

| Problem | Impact | Workaround |
|---------|--------|------------|
| Modal Dialogs (alert/confirm/prompt) | Blockiert komplett | User dismiss + "continue" |
| Kein Headless Mode | Browser sichtbar | Puppeteer MCP für Headless |
| WSL nicht supported | Windows-User | Native Windows oder VM |
| chrome:// URLs | Kein JS möglich | Erst zu echter URL navigieren |
| Context-Verbrauch | Tokens | `--chrome` nur wenn nötig |

---

## Decision Matrix: Welches Tool wann?

| Situation | Tool | Grund |
|-----------|------|-------|
| Einfache Seite, kein Login | `WebFetch` (native) | Am schnellsten, bereits verfügbar |
| Mehrere einfache Seiten | `Fetch MCP` | Batch-fähig |
| JS-heavy Seite, kein Login | `Puppeteer MCP` | Headless, schnell |
| Login erforderlich | `Chrome Extension` | Nutzt Browser Login-State |
| Interaktive Automation | `Chrome Extension` | Screenshot, Klick, Form |
| Strukturiertes Scraping | `Firecrawl MCP` | AI-optimierte Extraktion |

---

## Code-Snippets

### Paralleles Scraping (4 Tabs)

```python
# 1. Tabs erstellen (parallel)
tabs_create_mcp × 4

# 2. URLs parallel navigieren
navigate(url1, tab1)
navigate(url2, tab2)
navigate(url3, tab3)
navigate(url4, tab4)

# 3. Warten
wait(2)

# 4. Parallel extrahieren
get_page_text(tab1)
get_page_text(tab2)
get_page_text(tab3)
get_page_text(tab4)
```

### Effiziente Datenextraktion

```javascript
// Top 10 Links von einer Seite
Array.from(document.querySelectorAll('a[href]'))
  .slice(0, 10)
  .map(a => ({
    text: a.textContent.trim(),
    href: a.href
  }))

// Tabellen-Daten
Array.from(document.querySelectorAll('table tr'))
  .map(row => Array.from(row.cells).map(cell => cell.textContent.trim()))

// Formulare auslesen
Object.fromEntries(
  Array.from(document.querySelectorAll('input, select, textarea'))
    .map(el => [el.name || el.id, el.value])
)
```

### Error Recovery

```
Bei Tab-Problem:
1. tabs_create_mcp (neuer Tab)
2. navigate zu URL
3. Alte Tab-ID ignorieren
```

---

## Performance-Benchmarks (Stresstest)

| Operation | Single Tab | 4 Tabs Parallel | Speedup |
|-----------|------------|-----------------|---------|
| 4 URLs laden | ~8s | ~2s | 4x |
| 4 Seiten extrahieren | ~4s | ~1s | 4x |
| Screenshot | ~1s | - | - |
| JS Execution | <0.5s | <0.5s | - |

---

## Empfohlene Defaults

```
Max Tabs: 4-8 (getestet stabil)
Wait nach Navigation: 1-2s
JS Execution: Für strukturierte Daten
Screenshot: Nur wenn visuell nötig
```

---

## Related

- `knowledge/patterns/browser-automation-pattern.md` - Implementierungs-Pattern
- `.mcp.json` - MCP Server Konfiguration
- `knowledge/learnings/claude-code-dec-2025-features.md` - Chrome Features

---

**Getestet**: 2025-12-19
**Verifiziert durch**: Hands-on Experimente (siehe chrome-experiments-results.md)
**Status**: Production Ready

---

## VERIFIZIERTE Findings (Eigene Experimente)

Die folgenden Erkenntnisse wurden durch eigene Tests verifiziert:

### Tab Parallelisierung (BESTÄTIGT)
- 4 Tabs: 100% stabil (Tab-Erstellung, Navigation, JS-Extraktion)
- 8 Tabs: 100% stabil
- 12 Tabs: 11/12 erfolgreich (1 blockiert durch externe Faktoren)
- **Empfehlung bestätigt**: 4-8 Tabs optimal

### Security-Grenzen (NEU ENTDECKT)

| Feature | Status | Details |
|---------|--------|---------|
| DOM Manipulation | ✅ | Vollständig funktional |
| LocalStorage | ✅ | Lesen & Schreiben |
| Cookies | ❌ BLOCKIERT | `[BLOCKED: Cookie access]` |
| Cross-Origin Fetch | ✅ | Funktioniert! (überraschend) |
| window.open() | ❌ BLOCKIERT | Popup-Blocker aktiv |
| Große Datenmengen | ⚠️ | Repeated strings werden sanitized |

### Site-Blocklist (NEU ENTDECKT)
- reddit.com: Blockiert ("Safety restrictions")
- Weitere Sites: Noch nicht vollständig getestet

### SSL Error Pages (NEU ENTDECKT)
- Navigation erfolgreich
- JS-Zugriff: ❌ "Cannot attach to this target"
- Keine Workaround möglich (by design)
