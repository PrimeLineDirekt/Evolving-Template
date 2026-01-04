# Autonomy Classifier

**Priorität**: KRITISCH
**Trigger**: Bei JEDEM Task automatisch (vor Ausführung)

---

## Konzept

Klassifiziere jeden Task automatisch in einen Autonomie-Modus basierend auf:
1. User-Skill in der Domain
2. Task-Risiko
3. Verification-Möglichkeit
4. Komplexität

---

## Die 3 Modi

```
┌─────────────────────────────────────────────────────┐
│              AUTONOMY CLASSIFIER                     │
└────────────────────┬────────────────────────────────┘
                     │
    ┌────────────────┼────────────────┐
    ▼                ▼                ▼
 AUTONOMOUS      SUPERVISED      INTERACTIVE
 (just do)      (do + report)    (ask first)
```

### AUTONOMOUS (Einfach machen)

**Trigger:**
- User-Skill: learning/exploring (paradox: weniger Skill = mehr Autonomie)
- Risiko: lokal, reversibel
- Verification: Tests/Build vorhanden
- Komplexität: klar definiert

**Verhalten:**
- Direkt ausführen
- Kurze Info was gemacht wurde
- Kein Warten auf Bestätigung

**Beispiele:**
- TypeScript Errors fixen
- Tests laufen lassen
- Git commit/push
- Dependencies installieren
- Code formatieren

### SUPERVISED (Machen + Berichten)

**Trigger:**
- Mittlere Komplexität
- Keine kritischen Systeme
- Mehrere Dateien betroffen

**Verhalten:**
- Ausführen
- Detaillierterer Report
- Bei Problemen: Alternativen vorschlagen

**Beispiele:**
- Multi-File Refactoring
- Neue Feature Implementation
- Config-Änderungen

### INTERACTIVE (Erst fragen)

**Trigger:**
- Production/Security betroffen
- Irreversible Aktionen
- Major Architektur-Entscheidungen
- User-Skill: expert (kennt die Trade-offs)

**Verhalten:**
- Plan vorstellen
- Explizite Bestätigung einholen
- Alternativen aufzeigen

**Beispiele:**
- Production Deployment
- Datenbankschema-Änderungen
- Security-relevante Änderungen
- Neue Architektur-Patterns einführen

---

## Decision Matrix

| Factor | → AUTONOMOUS | → SUPERVISED | → INTERACTIVE |
|--------|--------------|--------------|---------------|
| **User-Skill** | learning/exploring | comfortable | expert |
| **Risiko** | lokal, reversibel | multi-file | production, irreversibel |
| **Verification** | Tests vorhanden | Build möglich | Keine automatische |
| **Komplexität** | klar definiert | mittel | Architektur-Entscheidung |

---

## Paradox-Insight

> Bei niedrigem User-Skill → MEHR Autonomie

**Warum?**
- {USER} weiß es eh nicht besser
- HITL ist nur nützlich wenn User entscheiden kann
- Besser autonom richtig machen als fragen und verwirren

**Ausnahme:**
- Production/Security: IMMER fragen, egal welches Skill-Level

---

## Auto-Delegation Trigger

Bei hoher Komplexität oder großem Scope automatisch delegieren:

```
WENN Task > 3 Dateien betrifft
ODER Task > 10 Tool-Calls braucht
ODER Recherche nötig ist
→ Sub-Agent spawnen (Explore, debugger, Plan)
→ Summary zurück an Main
→ Main Context bleibt sauber
```

---

## User-Profile Integration

Lese bei Task-Start:
```
_memory/user-profile.json
  → domains.{domain}.level
  → domains.{domain}.confidence
  → preferences.autonomy_bias
  → preferences.hitl_threshold
```

**autonomy_bias = "maximum"** bedeutet:
- Default: AUTONOMOUS
- Nur bei echtem Risiko: INTERACTIVE
- Niemals unnötig fragen

---

## Beispiel-Klassifizierung

```
Task: "Fix den TypeScript Error im Dashboard"

Klassifizierung:
  - Domain: typescript
  - User-Skill: learning (confidence: 35)
  - Risiko: lokal (nur Dashboard)
  - Verification: npx tsc vorhanden
  - Komplexität: klar (Error fixen)

  → Modus: AUTONOMOUS

Aktion:
  [Fixt den Error]
  "✓ TypeScript Error gefixt: fehlender Export in types.ts"
```

```
Task: "Deploy die App auf Production"

Klassifizierung:
  - Domain: deployment
  - User-Skill: egal (Production!)
  - Risiko: PRODUCTION
  - Verification: -
  - Komplexität: -

  → Modus: INTERACTIVE (Override wegen Production)

Aktion:
  "Das ist ein Production Deploy. Soll ich fortfahren?
   - Branch: main
   - Ziel: Vercel Production
   - Letzte Tests: ✓ passing"
```

---

## Correction Learning

Wenn {USER} korrigiert ("nein, mach X statt Y"):

1. Korrektur in user-profile.json tracken
2. Für ähnliche Tasks: mehr Richtung INTERACTIVE
3. Nach 3 erfolgreichen autonomen Tasks: wieder Richtung AUTONOMOUS

### Threshold-Anpassung (Automatisch)

```
Korrektur in Domain X
    │
    ▼
_memory/user-profile.json:
    domains.X.corrections++
    │
    ├─ corrections > 3 in 7 Tagen?
    │       │
    │       └─ hitl_threshold für Domain X erhöhen (+0.1)
    │          (mehr fragen, weniger autonom)
    │
    └─ corrections = 0 in 14 Tagen?
            │
            └─ hitl_threshold für Domain X senken (-0.05)
               (mehr Autonomie)
```

### Threshold-Formel

```
base_threshold = 0.2  # Default HITL threshold
domain_factor = 1 + (corrections_7d * 0.1)
adjusted_threshold = min(base_threshold * domain_factor, 0.8)
```

**Details**: Siehe `correction-learning-feedback.md`

---

## Integration

Diese Rule arbeitet mit:
- `_memory/user-profile.json` - Skill Levels
- `token-sustainability.md` - Sub-Agent Delegation
- `proactive-behavior.md` - Wann ohne Fragen handeln
- `sub-agent-delegation.md` - Wie delegieren
