---
description: Synchronizes generic content from Evolving to Evolving-Template with privacy protection
model: sonnet
argument-hint: [--dry-run|--force|--rollback|--history|--audit]
allowed-tools: [Read, Write, Edit, Bash, Glob, Grep, Task, AskUserQuestion]
---

# Template Sync Command

Du orchestrierst den Template-Sync-Workflow zwischen Evolving (Source) und Evolving-Template (Target).

## Argumente

| Argument | Beschreibung |
|----------|--------------|
| `--dry-run` | Nur Preview, keine Änderungen |
| `--force` | Keine interaktiven Prompts |
| `--rollback` | Letzten Sync rückgängig machen |
| `--history` | Sync-Historie anzeigen |
| `--audit` | Vollständiger Privacy-Audit des Templates |

## Workflow

### Phase 0: Setup & Validation

```
1. Lade Manifest: .claude/config/template-sync-manifest.json
2. Prüfe Pfade:
   - Source: $EVOLVING_SOURCE oder $PWD
   - Target: $EVOLVING_TEMPLATE oder manifest.paths.target
3. Falls Target nicht konfiguriert:
   → Frage User nach Pfad
   → Speichere in Manifest
4. Prüfe ob Target existiert und git repo ist
```

### Phase 1: Template Inventory Agent

Starte Task mit `template-inventory-agent`:
```
Analysiere beide Repos und erstelle Inventar:
- Zähle Komponenten (Agents, Commands, Skills, etc.)
- Identifiziere NEW, UPDATED, TEMPLATE-ONLY
- Zeige Summary
```

Output:
```
📦 TEMPLATE INVENTORY:
├── Agents: 19 (Source: 23 → 4 neu)
├── Commands: 34 (Source: 39 → 5 neu)
├── Patterns: 12 (Source: 15 → 3 neu)
└── Template-Only: 8 (geschützt)
```

### Phase 2: Template Diff Agent

Starte Task mit `template-diff-agent`:
```
Kategorisiere alle Dateien:
- NEW: Nur in Source
- UPDATED: Source neuer
- DIVERGED: Beide geändert
- TEMPLATE-ONLY: Geschützt
- IDENTICAL: Keine Änderung
```

Output:
```
📊 DIFF ANALYSE:
├── NEW: 12 Dateien
├── UPDATED: 8 Dateien
├── DIVERGED: 1 Datei (Review nötig)
├── TEMPLATE-ONLY: 8 Dateien (skip)
└── IDENTICAL: 45 Dateien
```

### Phase 3: Privacy Scanner Agent (Pre-Sync)

Starte Task mit `privacy-scanner-agent` im `pre-sync` Modus:
```
Scanne alle zu synchronisierenden Dateien:
- CRITICAL: API Keys, Secrets → BLOCK
- HIGH: Persönliche Namen, Projekte → ANONYMIZE
- MEDIUM: Pfade, Locations → ANONYMIZE
```

Output:
```
🔒 PRIVACY SCAN:
├── CRITICAL: 0 (keine API Keys)
├── HIGH: 3 Dateien mit persönlichen Referenzen
└── MEDIUM: 5 Dateien mit lokalen Pfaden
```

**Bei CRITICAL Findings: STOP und User informieren!**

### Phase 4: Content Anonymizer Agent

Für jede Datei mit Privacy-Findings:
```
Starte Task mit `content-anonymizer-agent`:
- Ersetze persönliche Referenzen mit Placeholdern
- Zeige Vorher/Nachher Preview
- Frage bei unklaren Fällen
```

Output:
```
🔄 ANONYMISIERUNG:
├── .claude/agents/xyz-agent.md
│   └── "{USER}" → "{USER}"
├── knowledge/patterns/example.md
│   └── "{PROJECT}" → "{PROJECT}"
└── .claude/CONTEXT.md
    └── "{HOME}" → "{HOME}"
```

### Phase 5: DIVERGED Handling

Für jede DIVERGED Datei:
```
DIVERGED: .claude/agents/example.md

Source: 2026-01-04 10:30
Target: 2026-01-03 14:15

Optionen:
  [S] Source übernehmen
  [T] Target behalten
  [M] Manuell mergen
  [D] Diff anzeigen
```

### Phase 6: Sync Preview & Confirmation

```
═══════════════════════════════════════
SYNC PREVIEW
═══════════════════════════════════════
NEW (12):        ████████████ sync
UPDATED (8):     ████████ sync
ANONYMIZED (3):  ███ transform + sync
DIVERGED (1):    █ [User-Entscheidung]
SKIP (8):        ████████ template-only
═══════════════════════════════════════

Proceed with sync? [Y/n/details]
```

### Phase 7: Backup & Sync Execution

```
1. Erstelle Backup-Commit im Template:
   git commit -m "backup: Pre-sync state"

2. Kopiere NEW Dateien:
   cp -r $SOURCE/$FILE $TARGET/$FILE

3. Update UPDATED Dateien:
   cp $SOURCE/$FILE $TARGET/$FILE

4. Schreibe anonymisierte Versionen:
   (transformierte Inhalte aus Phase 4)

5. Überspringe TEMPLATE-ONLY Dateien
```

### Phase 8: Post-Sync Validation

Starte Task mit `privacy-scanner-agent` im `post-sync` Modus:
```
Vollständiger Audit des GESAMTEN Templates:
- Scanne alle Dateien
- Prüfe auf Leaks
- Validiere Ergebnis
```

Output:
```
[8/8] Post-Sync Validation...

✓ Git-Status: clean
✓ Keine CRITICAL Privacy-Findings
✓ Template-Protected Dateien: unverändert
✓ JSON-Dateien: valid
⚠ 1 MEDIUM Warning (akzeptabel)

Validation: PASSED
```

**Bei FAILED: Rollback anbieten!**

### Phase 9: Commit & Update Manifest

```
1. Erstelle Commit im Template:
   git commit -m "sync: Add X new, update Y (DATE)"

2. Update Manifest:
   - last_sync: { date, backup_commit, sync_commit, stats }
   - sync_history: append entry
```

## Spezielle Modi

### --dry-run

Führe alle Phasen aus OHNE tatsächliche Änderungen:
- Kein Backup-Commit
- Keine Dateien kopiert
- Keine Manifest-Updates
- Zeige nur was passieren würde

### --rollback

```
Letzter Sync: 2026-01-04 10:45
Backup-Commit: abc1234
Sync-Commit: def5678

Rollback durchführen?
→ git reset --hard abc1234 im Template

[Y/n]
```

### --history

```
SYNC HISTORY (letzte 5):

2026-01-04 10:45  +12 ~8 ✓3  abc1234 → def5678
2026-01-03 14:20  +2 ~3 ✓1   xyz789 → uvw012
2026-01-01 09:00  +15 ~0 ✓0  (initial sync)
```

### --audit

Führe nur Privacy Scanner im `full-audit` Modus aus:
- Scannt gesamtes Template
- Keine Sync-Operationen
- Zeigt detaillierten Report

## Error Handling

### Target nicht gefunden
```
Template-Pfad nicht konfiguriert.

Wo liegt dein Evolving-Template Repository?
> [User gibt Pfad ein]

Pfad gespeichert.
```

### CRITICAL Privacy Finding
```
🚨 CRITICAL: API Key gefunden!

Datei: .claude/agents/xyz.md
Zeile 42: sk-xxxxxxx

Sync wird BLOCKIERT.
Bitte entferne den Key aus der Source-Datei.
```

### Git nicht clean im Template
```
⚠ Uncommitted changes im Template!

Optionen:
  [C] Commit current state first
  [S] Stash and continue
  [A] Abort
```

## Agent Orchestration

```
┌─────────────────────────────────────────────────────────┐
│                    /template-sync                        │
└─────────────────────┬───────────────────────────────────┘
                      │
        ┌─────────────┴─────────────┐
        ▼                           ▼
┌───────────────────┐    ┌───────────────────┐
│ Template Inventory │    │   Template Diff    │
│      Agent         │    │      Agent         │
└────────┬──────────┘    └────────┬──────────┘
         │                        │
         └──────────┬─────────────┘
                    ▼
         ┌───────────────────┐
         │  Privacy Scanner  │
         │   (pre-sync)      │
         └────────┬──────────┘
                  │
                  ▼ (wenn Findings)
         ┌───────────────────┐
         │ Content Anonymizer│
         └────────┬──────────┘
                  │
                  ▼
         ┌───────────────────┐
         │   Sync Execution  │
         └────────┬──────────┘
                  │
                  ▼
         ┌───────────────────┐
         │  Privacy Scanner  │
         │   (post-sync)     │
         └────────┬──────────┘
                  │
                  ▼
         ┌───────────────────┐
         │ Commit & Manifest │
         └───────────────────┘
```

## Manifest Referenz

Pfad: `.claude/config/template-sync-manifest.json`

Wichtige Felder:
- `paths.target`: Template-Pfad
- `sync_rules.include`: Was synchronisieren
- `sync_rules.exclude_always`: Was nie synchronisieren
- `template_protected`: Was im Template schützen
- `anonymization`: Ersetzungsregeln
- `last_sync`: Letzter Sync-Status
- `sync_history`: Historie

## Beispiel-Ausführung

```
User: /template-sync

Claude:
  Lade Manifest...
  Source: {EVOLVING_PATH}
  Target: {EVOLVING_PATH}-Template

  [1/8] Template Inventory Agent...
  📦 Agents: 19→23 (+4) | Commands: 34→39 (+5)

  [2/8] Template Diff Agent...
  📊 NEW: 12 | UPDATED: 8 | DIVERGED: 1

  [3/8] Privacy Scanner (pre-sync)...
  🔒 CRITICAL: 0 | HIGH: 3 | MEDIUM: 5

  [4/8] Content Anonymizer...
  🔄 3 Dateien anonymisiert

  [5/8] DIVERGED Review...
  → example.md: [S]ource gewählt

  [6/8] Sync Preview...
  Proceed? [Y]

  [7/8] Syncing...
  ✓ 20 Dateien synchronisiert
  ✓ 3 Dateien anonymisiert

  [8/8] Post-Sync Validation...
  ✓ Template Audit: PASSED

  Commit erstellen? [Y]
  ✓ Commit: sync: Add 12 new, update 8

  ✅ Sync erfolgreich abgeschlossen!
```
