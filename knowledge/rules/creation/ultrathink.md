# Ultrathink: System-weite Qualitätsprinzipien

**Priorität**: STANDARD
**Trigger**: Bei komplexen Aufgaben, System-Erweiterungen, Architektur-Entscheidungen

## Philosophie

> "Das Ziel ist nicht nur funktionierende Arbeit, sondern wartbare, elegante und intentionale Gestaltung."

Ultrathink gilt für ALLES im Evolving-System: Code, Knowledge, Agents, Workflows, Dokumentation.

---

## Die 5 Prinzipien

### 1. Foundation First

**Erst verstehen, dann handeln.**

| Kontext | Anwendung |
|---------|-----------|
| Session-Start | Memory lesen, Kontext verstehen |
| Neue Feature | Bestehende Patterns prüfen |
| Problem lösen | Root Cause finden, nicht Symptome |
| Code schreiben | Design System nutzen, nicht neu erfinden |

```
FALSCH: Sofort lostippen
RICHTIG:
  1. Was existiert bereits?
  2. Was ist das eigentliche Ziel?
  3. Welche Constraints gibt es?
  4. Dann erst: Implementieren
```

### 2. Single Source of Truth

**Eine Quelle, keine Duplikation.**

| Was | Wo |
|-----|-----|
| Farben & Styles | `lib/design-system/tokens.ts` |
| System-Status | `_memory/index.json` |
| Projekt-Wissen | `knowledge/projects/{name}/` |
| Patterns | `knowledge/patterns/` |
| Agent-Definitionen | `.claude/agents/` |

```
FALSCH: colorMap in 5 verschiedenen Dateien
RICHTIG: accentColors in tokens.ts, überall importieren

FALSCH: Projekt-Info in Chat, Notizen, und Memory
RICHTIG: _memory/projects/{name}.json als Master
```

### 3. Composition over Configuration

**Kleine, fokussierte Einheiten kombinieren.**

| Statt | Besser |
|-------|--------|
| 1 Mega-Agent mit 50 Fähigkeiten | 5 spezialisierte Agents orchestrieren |
| 1 Command mit 20 Parametern | 3 fokussierte Commands |
| 1 Skill für alles | Skill für eine Sache, gut gemacht |

```
FALSCH: /do-everything --mode=a --type=b --format=c
RICHTIG: /idea-new, /idea-work, /idea-connect
```

### 4. Semantic Naming

**Namen kommunizieren Intent.**

| Schlecht | Gut | Warum |
|----------|-----|-------|
| `/in` | `/idea-new` | Klar was passiert |
| `agent1.md` | `idea-validator-agent.md` | Rolle im Namen |
| `getStyles()` | `getAccentClasses(color, variant)` | Parameter erklären sich |
| `data.json` | `domain-memory.json` | Zweck erkennbar |

### 5. Progressive Enhancement mit Roadmap

**Start simple, dokumentiere Erweiterungen, implementiere bei Bedarf.**

```
Phase 1: Minimal Viable (IMPLEMENTIEREN)
  - Grundfunktion funktioniert
  - Kern-Use-Case abgedeckt

Phase 2: Roadmap (DOKUMENTIEREN)
  - Welche Features wären sinnvoll?
  - Welche Edge Cases könnten kommen?
  - Was würde Power-User wollen?
  → In Plan/TODO festhalten!

Phase 3: Iterieren (BEI BEDARF)
  - Features aus Roadmap umsetzen
  - User-Feedback einarbeiten
  - Optimierungen
```

**Wichtig:** Die Roadmap wird PROAKTIV erstellt, nicht erst wenn der User fragt!

```
FALSCH:
  "Feature fertig!" → User muss selbst auf Ideen kommen

RICHTIG:
  "Kern implementiert. Mögliche Erweiterungen:
   - [ ] Dark Mode Support
   - [ ] Keyboard Shortcuts
   - [ ] Export-Funktion
   Soll ich eine davon als nächstes umsetzen?"
```

**Wo dokumentieren:**
- Kleine Features: Im Code als TODO-Kommentar
- Größere Features: `knowledge/plans/{feature}-roadmap.md`
- Projekt-bezogen: `_memory/projects/{name}.json` unter `roadmap`

---

## Anwendungsbeispiele

### Bei Code-Arbeit

1. Design System Tokens nutzen, nicht eigene Farben
2. Bestehende UI Components verwenden
3. `cn()` für Tailwind-Klassen
4. Type-safe Props mit TypeScript
5. **Roadmap:** Weitere sinnvolle Props/Variants notieren

### Bei Knowledge-Arbeit

1. Prüfen ob Thema schon existiert
2. In richtige Kategorie einordnen
3. Cross-References setzen
4. Index aktualisieren
5. **Roadmap:** Verwandte Themen für später notieren

### Bei Agent-Erstellung

1. Bestehende Agent-Patterns prüfen
2. Fokussierte Rolle definieren
3. Klare Inputs/Outputs
4. Template nutzen, nicht from scratch
5. **Roadmap:** Mögliche Agent-Erweiterungen dokumentieren

### Bei Workflow-Design

1. Bestehende Commands als Inspiration
2. Ein Command = Eine Sache
3. Plain-Text Trigger definieren
4. In COMMANDS.md dokumentieren
5. **Roadmap:** Varianten und Erweiterungen notieren

---

## Checkliste vor Abschluss

- [ ] Folgt das der Single Source of Truth?
- [ ] Ist es komponierbar (nicht monolithisch)?
- [ ] Ist der Name selbsterklärend?
- [ ] Ist es minimal aber vollständig?
- [ ] Wurde Bestehendes wiederverwendet?
- [ ] **Wurde eine Roadmap mit möglichen Erweiterungen erstellt?**

---

## Related

- `core-principles.md` - Grundlegende Arbeitsweise
- `auto-enhancement.md` - Automatische Prompt-Verbesserung
- `knowledge/learnings/ultrathink-software-craftsmanship.md` - Code-spezifische Details
