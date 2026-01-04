# Token Efficiency Rule

**Prio**: STANDARD
**Trigger**: Bei internen Notizen, Plänen, Zusammenfassungen

---

## Regel

**Abkürzungen für interne Nutzung verwenden.**

Dies gilt für:
- Pläne & Roadmaps
- Interne Zusammenfassungen
- Batch-Listen & Checklisten
- Alles was NUR Claude liest

---

## Standard-Abkürzungen

| Abk | Bedeutung |
|-----|-----------|
| Prio | Priorität |
| Ext | Extraktion |
| Tpl | Template |
| Rel | Relevant |
| Cfg | Config |
| Impl | Implementation |
| Dok | Dokumentation |
| Dep | Dependencies |
| Cmd | Command |

---

## Komponenten-Abkürzungen

| Abk | Bedeutung |
|-----|-----------|
| A | Agent |
| S | Skill |
| C | Command |
| H | Hook |
| M | MCP |
| R | Rule |
| P | Pattern |
| L | Learning |

---

## Beispiel

```
LANG (Token-Verschwendung):
"Es gibt 163 Agents, 1023 Skills, 216 Commands und 59 MCP-Server
 die auf Relevanz geprüft werden müssen."

KOMPAKT:
"Rel-Scan: 163A, 1023S, 216C, 59M"
```

---

## NICHT abkürzen

- User-facing Output (Antworten an User)
- Code & Kommentare
- Knowledge Base Inhalte
- Alles was User liest

---

## Related

- [no-reference-only.md](no-reference-only.md) - Echte Integration statt URLs
- [relevance-extraction.md](relevance-extraction.md) - Ext-Framework
- [context-optimization.md](context-optimization.md) - Token-Budget Management
