# Workflow Detection

Automatische Erkennung von Slash-Command Triggern aus natürlicher Sprache.

## Referenzen

- Alle Workflows & Trigger: @.claude/COMMANDS.md
- Trigger-Patterns: @.claude/workflow-patterns.md

## Confidence-basierte Erkennung

| Confidence | Aktion |
|------------|--------|
| **9-10 (High)** | Trigger erkannt → Frage "Soll ich /workflow nutzen?" |
| **6-8 (Medium)** | Vorsichtig fragen "Meinst du /workflow?" |
| **1-5 (Low)** | Ignorieren, normal antworten |

## Regeln

1. **NIEMALS automatisch ausführen** ohne explizite Bestätigung
2. **Bei Multi-Match**: User fragen welcher Workflow passt
3. **Konservativ**: Lieber nicht triggern als falsch triggern

## Beispiele

```
User: "Ich habe eine neue Idee"
→ Confidence 9 → "Soll ich /idea-new nutzen?"

User: "Zeig mir meine Ideen"
→ Confidence 10 → "Soll ich /idea-list nutzen?"

User: "Ich muss mal schauen..."
→ Confidence 2 → Normal antworten
```
