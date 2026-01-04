# Claude Code Rules

## Tiered Structure (Token-optimiert)

```
.claude/rules/                    # CORE: Auto-load bei Session-Start (~2K Tokens)
├── core-principles.md            # Arbeitsweise
├── workflow-detection.md         # Command-Erkennung
├── domain-memory-bootup.md       # Session-Start
└── README.md                     # Diese Datei

knowledge/rules/                  # ON-DEMAND: Nur via Context Router (~0 Tokens default)
├── debugging/                    # observe-before-editing, evidence-before-claims
├── memory/                       # experience-suggest, memory-decay, auto-learning
├── creation/                     # command-creation, ultrathink
├── context/                      # context-optimization, clear-dont-compact
├── automation/                   # proactive-behavior, autonomy-classifier
├── workflow/                     # auto-archival, session-evaluation
├── sync/                         # cross-reference-sync, knowledge-linking
├── misc/                         # no-reference-only, relevance-extraction
└── scenarios/                    # {PROJECT_ID}, evolving-dashboard
```

## Loading-Verhalten

| Ordner | Auto-Load | Wann |
|--------|-----------|------|
| `.claude/rules/*.md` | JA | Session-Start |
| `knowledge/rules/**/*.md` | NEIN | Via Context Router bei Keyword-Match |

## Warum diese Struktur?

Claude Code lädt ALLE `.md` Dateien unter `.claude/rules/` rekursiv.
Die alte `on-demand/` Struktur funktionierte NICHT - alle Rules wurden trotzdem geladen.

**Lösung**: On-Demand Rules nach `knowledge/rules/` verschoben.
- Session-Start: ~2K Tokens (nur 4 Core Rules)
- Bei Bedarf: Context Router lädt relevante Rules
- Ersparnis: ~25K Tokens pro Session

## On-Demand Rules laden

Context Router in `_graph/cache/context-router.json` bestimmt welche Rules bei welchen Keywords geladen werden.

**Beispiel**: User sagt "debug" → Router lädt `knowledge/rules/debugging/*.md`

## Neue Regel erstellen

1. Datei in `knowledge/rules/{kategorie}/` erstellen
2. Context Router Route hinzufügen (wenn keyword-basiert)
3. Optional: Summary in `.claude/summaries/rules/` erstellen

**NICHT** in `.claude/rules/` erstellen - das erhöht den Session-Start Token-Verbrauch!
