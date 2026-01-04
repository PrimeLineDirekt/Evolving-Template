# /loop-until-done

Task mit klarem Completion-Kriterium iterativ ausführen bis fertig.

## Konzept

Inspiriert vom Ralph-Wiggum Pattern: Iteriere bis ein klares Erfolgskriterium erfüllt ist.

## Parameter

- **task**: Die Aufgabe (required)
- **verify**: Verification Command (optional, empfohlen)
- **max**: Maximum Iterationen (default: 10)
- **completion**: Explizites Completion-Signal (optional)

## Beispiele

```bash
# TypeScript Errors fixen bis Build grün
/loop-until-done "Fix alle TypeScript errors" --verify "npx tsc --noEmit" --max 15

# Tests grün machen
/loop-until-done "Alle Tests müssen passen" --verify "npm test" --max 10

# Linter-Warnings fixen
/loop-until-done "Fix ESLint warnings" --verify "npm run lint" --max 20

# Custom Completion-Signal
/loop-until-done "Implementiere Feature X" --completion "DONE" --max 25
```

## Workflow

```
1. Task ausführen
   ↓
2. Verify-Command laufen lassen (falls angegeben)
   ↓
3. Erfolgreich?
   │
   ├─ JA → Fertig, Report
   │
   └─ NEIN → Iteration++
              │
              ├─ Max erreicht? → Stopp, Report mit Status
              │
              └─ Weiter zu Schritt 1
```

## Best Practices

### Klare Erfolgskriterien

```bash
# GUT: Klares Verify-Command
/loop-until-done "Fix types" --verify "npx tsc --noEmit"

# SCHLECHT: Kein Verify
/loop-until-done "Verbessere den Code"
```

### Sinnvolle Max-Limits

| Task-Typ | Empfohlenes Max |
|----------|-----------------|
| TypeScript Errors | 15-20 |
| Test Fixes | 10-15 |
| Linter | 20-25 |
| Feature Implementation | 30-50 |

### Completion-Signal für komplexe Tasks

```bash
/loop-until-done "Build REST API:
  - CRUD Endpoints
  - Input Validation
  - Tests
  Output <DONE> when complete" --completion "DONE" --max 40
```

## Safety Features

1. **Max-Iterations**: Verhindert Endlosschleifen
2. **Progress-Report**: Nach jeder Iteration Info was passiert ist
3. **Escape**: "stop" oder "halt" unterbricht sofort
4. **Checkpoint**: Bei 50% Max-Iterations kurzes Status-Update

## Report-Format

```
🔄 Loop-Until-Done: {task}
━━━━━━━━━━━━━━━━━━━━━━━━━━━

Iteration 1/15:
  - Aktion: {was gemacht}
  - Verify: ❌ 5 errors remaining

Iteration 2/15:
  - Aktion: {was gemacht}
  - Verify: ❌ 2 errors remaining

Iteration 3/15:
  - Aktion: {was gemacht}
  - Verify: ✅ PASSED

━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Completed in 3 iterations
```

## Wann nutzen?

| Situation | Loop-Until-Done? |
|-----------|------------------|
| TypeScript Errors (viele) | ✅ JA |
| Ein einzelner Bug | ❌ Direkt fixen |
| Tests grün machen | ✅ JA |
| Feature implementieren | ✅ JA (mit max 30+) |
| Exploration/Research | ❌ NEIN |

## Integration

- Nutzt `proactive-behavior.md` für autonomes Fixen
- Nutzt `auto-learning.md` für Learnings aus der Loop
- Nutzt `token-sustainability.md` für Sub-Agent Delegation bei Komplexität
