# /preferences [action] [category]

Zeige und verwalte User-Praeferenzen.

## Model: haiku

## Arguments
- `action` (optional): show (default), add, edit, remove
- `category` (optional): workflow, code_style, communication, architecture

## Workflow

### Show (Default)
```
/preferences
/preferences show
/preferences show code_style
```

1. Lies `_memory/preferences/user-preferences.json`
2. Zeige Praeferenzen gruppiert nach Kategorie:

```
User Preferences (Robin)
========================

Workflow:
  - TodoWrite bei 3+ Schritten (100%)
  - Chain of Thought vor Umsetzung (95%)
  - Radikale Ehrlichkeit statt Hoeflichkeit (100%)

Code Style:
  - TypeScript mit strict mode (90%)
  - Keine Default Exports in React (85%)

Communication:
  - Sparring statt Ja-Sagen (100%)
  - 80/20 Fokus (95%)
  - Cross-Checking bei wichtigen Fakten (90%)

Architecture:
  - AI-First Development (100%)
```

### Add
```
/preferences add
/preferences add code_style
```

1. Falls keine Kategorie: Frage nach Kategorie
2. Frage nach Praeferenz
3. Frage nach Quelle (woher kommt diese Praeferenz?)
4. Frage nach applies_to (wo gilt sie?)
5. Setze initiale Confidence auf 80%
6. Speichere in user-preferences.json

### Edit
```
/preferences edit pref-code-001
```

1. Lade Praeferenz
2. Zeige aktuelle Werte
3. Frage was geaendert werden soll
4. Update und speichere

### Remove
```
/preferences remove pref-code-001
```

1. Zeige Praeferenz
2. Bestaetigung einholen
3. Entferne aus user-preferences.json

## Confidence System

Confidence wird automatisch angepasst:
- +5% wenn Praeferenz bestaetigt wird (User folgt ihr)
- -10% wenn Praeferenz ignoriert wird (User macht es anders)
- Max: 100%, Min: 0%
- Bei 0%: Praeferenz wird als "uncertain" markiert

## Plain Text Triggers
- "zeig meine praeferenzen"
- "was bevorzuge ich"
- "meine einstellungen"
- "add preference"
