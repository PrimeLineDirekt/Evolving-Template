# Session Notes Template

> **Source**: Piebald-AI/claude-code-system-prompts (v2.0.58)
> **Purpose**: Strukturierte Dokumentation von Coding-Sessions

## Template

```markdown
# {SESSION_TITLE}

**Datum**: YYYY-MM-DD
**Projekt**: {project_name}
**Dauer**: ~Xh

---

## 1. Current State

**Laufende Arbeiten:**
- {was gerade in Bearbeitung ist}

**Nächste Schritte:**
- {was als nächstes getan werden sollte}

**Blockiert durch:**
- {falls etwas blockiert}

---

## 2. Task Specification

**User-Anforderung:**
> {originale Anfrage des Users}

**Design-Entscheidungen:**
- {Entscheidung 1}: {Begründung}
- {Entscheidung 2}: {Begründung}

**Constraints:**
- {technische oder business Einschränkungen}

---

## 3. Files and Functions

| Datei | Zweck | Status |
|-------|-------|--------|
| `path/to/file.ts` | {was die Datei macht} | modified/created/reviewed |

**Kern-Funktionen:**
- `functionName()` in `file.ts:123` - {was sie macht}

---

## 4. Workflow

**Ausgeführte Commands:**
```bash
# {Beschreibung was dieser Command macht}
{command}

# Output-Interpretation:
# {was das Ergebnis bedeutet}
```

---

## 5. Errors & Corrections

### Error 1: {Error-Titel}
**Symptom:** {was passiert ist}
**Root Cause:** {warum es passiert ist}
**Fix:** {wie es gelöst wurde}
**Lesson:** {was wir gelernt haben}

### Fehlgeschlagene Ansätze
- {Ansatz 1}: Warum es nicht funktioniert hat
- {Ansatz 2}: Warum es nicht funktioniert hat

---

## 6. Codebase & System Documentation

**Architektur-Erkenntnisse:**
- {Pattern oder Struktur die entdeckt wurde}

**Dependencies:**
- {wichtige Abhängigkeiten}

**Konfiguration:**
- {relevante Config-Änderungen}

---

## 7. Learnings

**Was funktioniert hat:**
- {erfolgreicher Ansatz 1}
- {erfolgreicher Ansatz 2}

**Was NICHT funktioniert hat:**
- {fehlgeschlagener Ansatz 1}
- {fehlgeschlagener Ansatz 2}

**Für zukünftige Sessions:**
- {Empfehlung für später}

---

## 8. Key Results

**Outputs:**
- {konkretes Ergebnis 1}
- {konkretes Ergebnis 2}

**Metriken:**
- Tests: X passing, Y failing
- Files changed: Z
- Lines added/removed: +A/-B

---

## 9. Worklog

| Zeit | Aktivität | Ergebnis |
|------|-----------|----------|
| 10:00 | {was gemacht wurde} | {Ergebnis} |
| 10:30 | {was gemacht wurde} | {Ergebnis} |

---

## 10. Handoff Summary

**Für die nächste Session:**

1. **Weitermachen mit:** {konkreter nächster Schritt}
2. **Beachten:** {wichtige Hinweise}
3. **Offen:** {offene Fragen}

**Quick-Start Command:**
```
{command um schnell weiterzumachen}
```
```

---

## Wann nutzen

- Nach komplexen Sessions (3+ Stunden)
- Bei wichtigen Architektur-Entscheidungen
- Wenn Session unterbrochen wird
- Für Wissenstransfer zwischen Sessions

## Unterschied zu Standard-Handoff

| Standard Handoff | Enhanced Session Notes |
|------------------|------------------------|
| Was wurde erreicht | + Current State tracking |
| Nächste Schritte | + Workflow mit Commands |
| - | + Errors & Corrections |
| - | + Worklog mit Zeitstempeln |
| - | + Key Results mit Metriken |

## Integration

Dieses Template wird von `/whats-next` genutzt wenn:
- `--detailed` Flag gesetzt ist
- Session länger als 2h war
- Mehrere Errors aufgetreten sind
