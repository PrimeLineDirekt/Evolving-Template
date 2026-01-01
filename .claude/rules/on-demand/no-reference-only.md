# No Reference-Only Rule

**Prio**: KRITISCH
**Trigger**: Bei /analyze-repo, Knowledge-Erstellung, Ext-Integration

---

## Regel

**Keine URL-only Dateien. Echte Integration erforderlich.**

```
VERBOTEN:
- "15 relevante Prompts: {URL}"
- "Siehe {URL} für Details"
- "Quelle: {URL}" ohne Inhalt
- Reference-Files die nur URLs listen
```

---

## Warum?

Wahrscheinlichkeit, dass eine URL-Referenz später gelesen wird: **<5%**

```
Nutzlos:
"Es gibt interessante Patterns unter github.com/..."
→ Wird nie aufgerufen

Nützlich:
Pattern tatsächlich extrahiert + in System integriert
→ Wird automatisch gefunden via Graph/Search
```

---

## Stattdessen

| Situation | Aktion |
|-----------|--------|
| Rel Komponente | Ext nach `.claude/*/external/{repo}/` |
| Interessantes Framework | Tpl abstrahieren |
| Nicht rel | Skip + kurze Notiz warum |

---

## Ext-Format

```yaml
---
source: {url}
extracted: {date}
tags: [domain, type]
status: extracted|adapted|integrated
---
# {VOLLSTÄNDIGER INHALT}
```

---

## Bestehende Reference-Only Files

Bei Entdeckung:
1. Rel-Scan durchführen
2. Rel → Ext
3. Interessant → Tpl
4. Rest → Skip-Notiz
5. Reference-File entfernen/ersetzen

---

## Ausnahme

Nur bei SEHR großen Ressourcen (1000+ Dateien):
→ Index mit Top-10 Ext + Link zum Rest
→ Aber: Top-10 MÜSSEN extrahiert sein

---

## Related

- [relevance-extraction.md](relevance-extraction.md) - Rel-Check + Tpl Framework
- [token-efficiency.md](token-efficiency.md) - Abkürzungen für Ext-Dok
- [command-creation.md](command-creation.md) - /analyze-repo nutzt diese Rule
- [cross-reference-sync.md](cross-reference-sync.md) - Master-Dok Sync nach Ext
