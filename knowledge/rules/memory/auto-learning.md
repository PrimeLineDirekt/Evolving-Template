# Auto-Learning

**Priorität**: HOCH
**Trigger**: Kontinuierlich während jeder Session

---

## Konzept

System erkennt und speichert Learnings automatisch. {USER} muss nicht `/remember` sagen - das System wächst von selbst.

---

## Learning-Trigger

| Trigger | Learning-Typ | Beispiel |
|---------|--------------|----------|
| Problem gelöst nach Debugging | `solution` | "Supabase RLS braucht auch SELECT Policy" |
| Wiederholtes Pattern erkannt | `pattern` | "Bei Next.js immer App Router nutzen" |
| Entscheidung getroffen | `decision` | "Tailwind statt CSS Modules für dieses Projekt" |
| Fehler gemacht + korrigiert | `gotcha` | "npm ci statt npm install in CI" |
| User-Korrektur erhalten | `preference` | "{USER} will kurze Antworten" |
| Workaround gefunden | `workaround` | "Chrome MCP braucht Neustart nach Update" |

---

## Auto-Save Flow

```
Situation erkannt (z.B. Bug gefixt)
    │
    ▼
Learning-Classifier prüft:
  - Ist das neu? (nicht in Experiences)
  - Ist das generalisierbar? (nicht zu spezifisch)
  - Hat es Wert? (würde wieder helfen)
    │
    ▼
  JA zu allen?
    │
    ├─ Experience erstellen
    │   └─ _memory/experiences/exp-YYYY-NNN.json
    │
    ├─ Index aktualisieren
    │   └─ _memory/experiences/index.json
    │
    ├─ Graph vernetzen
    │   └─ Relevante Edges zu Projekten/Patterns
    │
    └─ Kurze Info (nicht fragen!):
        "📚 Gelernt: {summary}"
```

---

## Qualitätsfilter

### NICHT speichern

- Zu spezifische Fixes (nur für diese eine Datei)
- Bereits bekannte Learnings (Duplikate)
- Triviales (offensichtliche Syntax-Fehler)
- User-spezifische Einmal-Aktionen
- Temporäre Workarounds ohne Lernwert

### SPEICHERN

- Generalisierbares Wissen
- Wiederkehrende Patterns
- Architektur-Entscheidungen mit Begründung
- Projekt-übergreifende Erkenntnisse
- Nicht-offensichtliche Lösungen
- User-Korrekturen (→ preferences)

---

## Duplikat-Check

Vor dem Speichern prüfen:

```python
# Pseudo-Code
def is_duplicate(new_learning):
    for exp in existing_experiences:
        if similarity(exp.summary, new_learning.summary) > 0.8:
            return True
        if exp.problem == new_learning.problem:
            return True
    return False
```

---

## Auto-Vernetzung

Neue Experience wird automatisch verknüpft mit:

```json
{
  "projects": ["aktuelles-projekt"],
  "related_experiences": ["exp-2026-001"],
  "patterns": ["systematic-debugging"],
  "tags": ["typescript", "exports", "dashboard"]
}
```

**Vernetzungs-Logik:**
1. Aktives Projekt aus `_memory/index.json`
2. Ähnliche Experiences via Keyword-Match
3. Relevante Patterns aus `knowledge/patterns/`
4. Tags auto-generiert aus Inhalt

---

## Experience-Format

```json
{
  "id": "exp-2026-017",
  "type": "solution",
  "created": "2026-01-03",
  "summary": "Dashboard TypeScript Errors oft durch fehlende Exports",
  "problem": "TypeScript Error: Cannot find module",
  "solution": "Export in index.ts hinzufügen",
  "root_cause": "Barrel-Export Pattern nicht vollständig",
  "tags": ["typescript", "exports", "dashboard"],
  "projects": ["evolving-dashboard"],
  "relevance_score": 75,
  "access_count": 0,
  "last_accessed": null
}
```

---

## Trigger-Erkennung

### Nach Debugging-Session

```
Problem erkannt → Analysiert → Gefixt → Verifiziert
                                            │
                                            ▼
                            War das nicht-trivial?
                                            │
                                           JA
                                            │
                                            ▼
                                    Auto-Learning:
                            - Problem dokumentieren
                            - Lösung dokumentieren
                            - Root Cause wenn bekannt
```

### Nach User-Korrektur

```
User: "Nein, mach X statt Y"
           │
           ▼
    Auto-Learning:
    type: "preference"
    summary: "{USER} bevorzugt X über Y"
    confidence: 85
           │
           ▼
    User-Profile updaten:
    learned_from_corrections += 1
```

### Nach Entscheidung

```
Entscheidung getroffen (z.B. "Nutzen wir Supabase")
           │
           ▼
    Auto-Learning:
    type: "decision"
    question: "Welche DB für {Projekt}?"
    decision: "Supabase"
    reasoning: "Einfache Auth, RLS, kostenfrei"
    revisit_if: "Performance-Probleme"
```

---

## Reporting

Kurz und nicht-invasiv:

```
📚 Gelernt: "Supabase RLS braucht SELECT + INSERT Policy"
```

**Nicht:**
```
Ich habe gerade etwas Wichtiges gelernt! Soll ich es speichern?
Hier ist was ich gelernt habe: [langer Text]
Möchtest du das in der Knowledge Base haben?
```

---

## Integration

- Experience Memory: `_memory/experiences/`
- Index: `_memory/experiences/index.json`
- Schema: `_memory/experiences/SCHEMA.md`
- Decay: `memory-decay.md` Rule
- Suggest: `experience-suggest.md` Rule

---

## Wachstums-Metriken

Track in `_memory/experiences/index.json`:

```json
{
  "total_count": 25,
  "auto_learned_count": 10,
  "this_week": 3,
  "top_tags": ["typescript", "supabase", "next.js"]
}
```
