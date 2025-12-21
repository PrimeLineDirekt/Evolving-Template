# Workflow Auto-Detection Patterns

Dieses Dokument definiert alle Erkennungsmuster für Plain Text Workflow-Triggers.

## Wie funktioniert es?

Wenn der User im normalen Chat schreibt (ohne `/command`), analysiere ich den Text auf diese Patterns.

**Flow:**
1. User schreibt normalen Text
2. Ich prüfe gegen alle Patterns
3. Bei Match → Frage: "Soll ich `/{workflow}` nutzen?"
4. User bestätigt → Workflow wird ausgeführt
5. Kein Match → Normale Antwort

**Wichtig**: IMMER fragen vor Ausführung, nie automatisch triggern!

---

## Pattern-Definitionen

### `/idea-new` - Neue Idee erfassen

**Trigger-Keywords:**
- `idee`
- `neue idee`
- `konzept`
- `geschäftsidee`
- `ich habe eine idee`
- `was hältst du von`
- `startup idee`

**Pattern-Beispiele:**
```
✓ "Ich habe eine Idee: Ein Tool das..."
✓ "Neue Idee - Automatisierung für..."
✓ "Was hältst du von diesem Konzept: ..."
✓ "Geschäftsidee: Ein Service der..."
✓ "Ich denke über eine Startup-Idee nach: ..."
```

**Anti-Patterns (NICHT triggern):**
```
✗ "Ich habe keine Idee was das bedeutet" (negativ)
✗ "Die Idee in diesem Projekt ist..." (referenziert bestehend)
✗ "Gute Idee!" (Zustimmung)
```

**Confirmation:**
```
"Soll ich /idea-new nutzen um diese Idee zu erfassen und zu analysieren?"
```

---

### `/idea-work` - An Idee arbeiten

**Trigger-Keywords:**
- `an [idee] arbeiten`
- `[idee] weiterentwickeln`
- `brainstorming zu [idee]`
- `sparring für [idee]`
- `idee ausarbeiten`

**Pattern-Beispiele:**
```
✓ "Lass uns an meiner E-Commerce-Idee arbeiten"
✓ "Ich möchte die Business Idee weiterentwickeln"
✓ "Brainstorming zu idea-2024-001"
✓ "Kannst du mir bei Idee XYZ helfen?"
```

**Confirmation:**
```
"Soll ich /idea-work starten für {erkannte Idee}?"
```

---

### `/idea-list` - Ideen-Übersicht

**Trigger-Keywords:**
- `zeig mir meine ideen`
- `ideen übersicht`
- `welche ideen habe ich`
- `liste ideen`
- `alle ideen`
- `ideen status`

**Pattern-Beispiele:**
```
✓ "Zeig mir alle meine Ideen"
✓ "Welche Ideen habe ich aktuell?"
✓ "Gib mir eine Übersicht über die Ideen"
✓ "Liste alle aktiven Ideen"
```

**Confirmation:**
```
"Soll ich /idea-list ausführen?"
```

---

### `/idea-connect` - Verbindungen finden

**Trigger-Keywords:**
- `verbindungen`
- `synergien`
- `ideen verbinden`
- `passen zusammen`
- `kombinieren`
- `welche ideen passen`

**Pattern-Beispiele:**
```
✓ "Finde Verbindungen zwischen meinen Ideen"
✓ "Welche Ideen haben Synergien?"
✓ "Können Ideen kombiniert werden?"
✓ "Zeig mir welche Ideen zusammenpassen"
```

**Confirmation:**
```
"Soll ich /idea-connect ausführen um Synergien zu finden?"
```

---

### `/knowledge-add` - Wissen hinzufügen

**Trigger-Keywords:**
- `ich habe gelernt`
- `wissen hinzufügen`
- `notiere`
- `speichere`
- `merke dir`
- `wichtige erkenntnis`
- `best practice`

**Pattern-Beispiele:**
```
✓ "Ich habe gelernt dass..."
✓ "Notiere dir: SEO funktioniert am besten wenn..."
✓ "Wichtige Erkenntnis aus dem Projekt: ..."
✓ "Merke dir diese Best Practice: ..."
✓ "Ich möchte Wissen hinzufügen über..."
```

**Confirmation:**
```
"Soll ich das mit /knowledge-add zur Knowledge Base hinzufügen?"
```

---

### `/knowledge-search` - Wissen suchen

**Trigger-Keywords:**
- `suche nach`
- `finde`
- `was weiß ich über`
- `habe ich wissen über`
- `gibt es informationen zu`

**Pattern-Beispiele:**
```
✓ "Suche nach API Integration"
✓ "Was weiß ich über SEO?"
✓ "Finde Informationen zu E-Commerce"
✓ "Habe ich Wissen über n8n gespeichert?"
```

**Confirmation:**
```
"Soll ich /knowledge-search nutzen um nach '{topic}' zu suchen?"
```

---

### `/project-add` - Projekt dokumentieren

**Trigger-Keywords:**
- `projekt dokumentieren`
- `neues projekt`
- `projekt hinzufügen`
- `hier ist mein projekt`
- `readme für projekt`

**Pattern-Beispiele:**
```
✓ "Ich möchte mein E-Commerce-Projekt dokumentieren"
✓ "Neues Projekt: API Integration Tool"
✓ "Hier ist die README für mein Projekt: ..."
```

**Confirmation:**
```
"Soll ich /project-add nutzen um das Projekt zu dokumentieren?"
```

---

### `/inbox-process` - Inbox verarbeiten

**Trigger-Keywords:**
- `inbox`
- `verarbeite die inbox`
- `neue dateien`
- `schau in _inbox`
- `dateien in inbox`

**Pattern-Beispiele:**
```
✓ "Verarbeite die Inbox"
✓ "Ich habe neue Dateien in der Inbox"
✓ "Schau mal in _inbox"
✓ "Kannst du die Inbox durchgehen?"
```

**Confirmation:**
```
"Soll ich /inbox-process ausführen und die Dateien verarbeiten?"
```

---

### `/sparring` - Brainstorming

**Trigger-Keywords:**
- `brainstorming`
- `lass uns denken über`
- `sparring`
- `was denkst du über`
- `input zu`
- `diskutieren wir`

**Pattern-Beispiele:**
```
✓ "Lass uns brainstormen über E-Commerce Trends"
✓ "Ich brauche dein Sparring zu..."
✓ "Was denkst du über diese Strategie?"
✓ "Lass uns über meine Zukunftspläne diskutieren"
```

**Confirmation:**
```
"Soll ich /sparring starten für '{topic}'?"
```

---

### `/onboard-process` - Onboarding verarbeiten

**Trigger-Keywords:**
- `onboarding`
- `verarbeite das onboarding`
- `fragebogen ausgefüllt`
- `onboarding fertig`
- `ich habe den fragebogen`

**Pattern-Beispiele:**
```
✓ "Verarbeite das Onboarding"
✓ "Ich habe den Fragebogen ausgefüllt"
✓ "Onboarding fertig"
✓ "Der Fragebogen ist ausgefüllt"
```

**Confirmation:**
```
"Soll ich /onboard-process ausführen und deine Informationen ins System einpflegen?"
```

---

## Pattern-Matching Algorithmus

### Priority-Order (bei mehreren Matches)

1. **Spezifisch vor Allgemein**
   - `/inbox-process` vor `/knowledge-add`
   - `/idea-work {id}` vor `/idea-new`

2. **Context-Aware**
   - Wenn Ideen-ID erwähnt → `/idea-work`
   - Wenn "neue/neue" dabei → `/idea-new`

3. **Intent-basiert**
   - Frage? → Eher `/knowledge-search`
   - Statement? → Eher `/knowledge-add`

### Confidence-Levels

**High (9-10)**: Eindeutige Keywords + Context
- Triggern + fragen

**Medium (6-8)**: Keywords vorhanden, Context unklar
- Fragen: "Meinst du {workflow}?"

**Low (1-5)**: Schwache Übereinstimmung
- Ignorieren, normal antworten

### Multi-Match Handling

Falls mehrere Workflows matchen:
```
"Ich könnte hier mehrere Workflows nutzen:
[1] /idea-new - Neue Idee erfassen
[2] /knowledge-add - Als Wissen speichern

Welcher passt besser?"
```

---

## Implementation Guidelines

### Wann NICHT auto-detect

- User stellt allgemeine Fragen
- User chattet normal ohne Action-Intent
- Kontext ist zu vague
- User korrigiert mich gerade

### Best Practices

1. **Sei konservativ**: Lieber nicht triggern als falsch
2. **Context nutzen**: Vorherige Nachrichten beachten
3. **Natürlich bleiben**: Detection soll helfen, nicht nerven
4. **Learn from feedback**: Wenn User oft ablehnt → Pattern zu aggressiv

### Response-Template

```
[Pattern erkannt]

"Ich erkenne dass du {intent}. Soll ich `/{workflow}` nutzen?"

[Falls User zustimmt]
→ Workflow ausführen mit erkannten Parametern

[Falls User ablehnt]
→ Normal weitermachen, Pattern mental als "false positive" merken
```

---

## Testing Examples

### Positive Tests

| User Input | Soll Triggern | Workflow |
|-----------|---------------|----------|
| "Ich habe eine Idee für ein SaaS Tool" | ✓ | `/idea-new` |
| "Zeig mir alle meine Ideen" | ✓ | `/idea-list` |
| "Suche nach API Best Practices" | ✓ | `/knowledge-search` |
| "Verarbeite die Inbox" | ✓ | `/inbox-process` |
| "Lass uns über Strategie brainstormen" | ✓ | `/sparring` |
| "Ich habe den Fragebogen ausgefüllt" | ✓ | `/onboard-process` |

### Negative Tests (NICHT triggern)

| User Input | Soll NICHT Triggern | Warum |
|-----------|---------------------|-------|
| "Gute Idee!" | ✗ | Zustimmung, keine neue Idee |
| "Was bedeutet dieses Wort?" | ✗ | Frage, kein Workflow-Intent |
| "Die Suche hat nicht funktioniert" | ✗ | Über Suche reden, nicht suchen |
| "Wie geht es dir?" | ✗ | Small talk |

---

## Template Creation (Meta-Agent Commands)

### `/create-agent` - Agent erstellen

**Trigger-Keywords**:
- `erstelle einen agent`
- `neuer agent`
- `create agent`
- `agent für {domain}`
- `i need an agent`
- `make an agent`

**Pattern-Beispiele**:
```
✓ "Erstelle einen SEO Agent"
✓ "Neuer Agent für Legal Compliance"
✓ "Create an agent for market research"
✓ "Ich brauche einen Agent für Content-Strategie"
✓ "Make an agent that analyzes websites"
```

**Anti-Patterns (NICHT triggern)**:
```
✗ "agent läuft" (Status, nicht Creation)
✗ "welcher agent" (Discovery, nicht Creation)
✗ "agent status" (Monitoring, nicht Creation)
✗ "dieser agent macht" (Discussion, nicht Creation)
```

**Pattern**: Intention einen Agent zu erstellen

**Confidence**: High (9-10) - Klare Creation-Keywords

**Confirmation**:
```
"Ich erkenne die Intention einen Agent zu erstellen. Soll ich /create-agent nutzen oder direkt den template-creator Skill aktivieren?"
```

---

### `/create-command` - Command erstellen

**Trigger-Keywords**:
- `erstelle einen command`
- `neuer command`
- `create command`
- `command für {workflow}`
- `slash command`
- `neuer workflow`

**Pattern-Beispiele**:
```
✓ "Erstelle einen Command für Projekt-Initialisierung"
✓ "Neuer Command: Code Review"
✓ "Create a command for data export"
✓ "Ich brauche einen Command der Reports generiert"
✓ "Slash command für deployment check"
```

**Anti-Patterns (NICHT triggern)**:
```
✗ "command läuft" (Execution, nicht Creation)
✗ "welche commands" (Listing, nicht Creation)
✗ "/help" (Using commands, nicht Creation)
✗ "dieser command macht" (Discussion, nicht Creation)
```

**Pattern**: Intention einen Command zu erstellen

**Confidence**: High (9-10) - Klare Creation-Keywords

**Confirmation**:
```
"Ich erkenne die Intention einen Command zu erstellen. Soll ich /create-command nutzen oder direkt den template-creator Skill aktivieren?"
```

---

### `/create-hook` - Hook erstellen

**Trigger-Keywords**:
- `erstelle einen hook`
- `neuer hook`
- `create hook`
- `hook für {event}`
- `automation`
- `trigger when`
- `automatisch wenn`

**Pattern-Beispiele**:
```
✓ "Erstelle einen Hook für Markdown-Validierung"
✓ "Neuer Hook: Session Summary"
✓ "Create a hook that runs after file edits"
✓ "Ich brauche Automation wenn Dateien erstellt werden"
✓ "Hook der automatisch cross-references"
```

**Anti-Patterns (NICHT triggern)**:
```
✗ "webhook" (HTTP webhook, nicht Claude hook)
✗ "git hook" (Git-spezifisch, nicht Claude)
✗ "hook läuft" (Status, nicht Creation)
```

**Pattern**: Intention einen Hook zu erstellen

**Confidence**: Medium (7-8) - "Hook" ist technischer Begriff, kann verwechselt werden

**Confirmation**:
```
"Ich erkenne die Intention einen Hook zu erstellen. Meinst du einen Claude Hook für Automation? Falls ja, soll ich /create-hook nutzen?"
```

---

### `/create-skill` - Skill erstellen

**Trigger-Keywords**:
- `erstelle einen skill`
- `neuer skill`
- `create skill`
- `skill für {domain}`
- `expertise in {domain}`
- `dokumentiere {pattern/process}`

**Pattern-Beispiele**:
```
✓ "Erstelle einen Skill für PDF-Verarbeitung"
✓ "Neuer Skill: API Rate Limiting"
✓ "Create a skill for SEO optimization"
✓ "Ich brauche Expertise in Data Visualization"
✓ "Dokumentiere das Code Review Pattern als Skill"
```

**Anti-Patterns (NICHT triggern)**:
```
✗ "welche skills" (Listing, nicht Creation)
✗ "skill level" (Proficiency, nicht Skill-System)
✗ "meine skills sind" (Personal skills, nicht System)
✗ "dieser skill macht" (Discussion, nicht Creation)
```

**Pattern**: Intention einen Skill zu erstellen

**Confidence**: Medium (7-8) - "Skill" kann mehrdeutig sein

**Confirmation**:
```
"Ich erkenne die Intention einen Skill zu erstellen. Meinst du einen wiederverwendbaren Skill für das System? Falls ja, soll ich /create-skill nutzen?"
```

---

## Template Creation - Special Cases

### Multi-Component Creation

Falls User mehrere Components will:
```
User: "Create an SEO system with agent, commands, and hooks"

Response:
"Ich erkenne dass du ein SEO-System erstellen möchtest mit mehreren Components:
1. Agent für SEO-Expertise
2. Commands für SEO-Workflows
3. Hooks für Automation

Soll ich nacheinander erstellen?
→ /create-agent seo
→ /create-command seo-analyze
→ /create-hook seo-validator
"
```

### Skill vs. Agent Disambiguation

Falls unklar ob Skill oder Agent:
```
User: "Create expertise in PDF processing"

Frage:
"Soll das ein:
[1] Agent - Aktive Verarbeitung von PDFs (analysiert, extrahiert)
[2] Skill - Passives Wissen über PDF-Verarbeitung (Guidelines, Best Practices)
sein?"
```

**Guideline**:
- Agent = Aktive Tasks (analysieren, verarbeiten, generieren)
- Skill = Passives Wissen (Guidelines, Patterns, Best Practices)

---

---

## Szenario-System Commands

### `/scenario` - Szenario aktivieren

**Trigger-Keywords**:
- `aktiviere szenario`
- `wechsle zu`
- `switch to`
- `öffne projekt`
- `starte szenario`
- `lade szenario`
- `context wechseln`

**Pattern-Beispiele**:
```
✓ "Aktiviere das Dashboard Szenario"
✓ "Wechsle zu web-development"
✓ "Switch to evolving-dashboard"
✓ "Öffne das Dashboard Projekt"
✓ "Lade das Web Development Szenario"
✓ "Context wechseln zu Dashboard"
```

**Anti-Patterns (NICHT triggern)**:
```
✗ "was ist ein szenario" (Frage, nicht Aktivierung)
✗ "zeig mir die szenarien" (List, nicht Switch)
✗ "szenario erstellen" (Create, nicht Switch)
```

**Confidence**: High (9-10) - Klare Switch-Intention

**Confirmation**:
```
"Soll ich /scenario {name} ausführen um das Szenario zu aktivieren?"
```

---

### `/scenario-list` - Szenarien anzeigen

**Trigger-Keywords**:
- `zeig mir szenarien`
- `welche szenarien`
- `alle szenarien`
- `verfügbare szenarien`
- `szenarien übersicht`
- `list scenarios`

**Pattern-Beispiele**:
```
✓ "Zeig mir alle verfügbaren Szenarien"
✓ "Welche Szenarien habe ich?"
✓ "Übersicht über Szenarien"
✓ "List all scenarios"
```

**Confidence**: High (9-10)

**Confirmation**:
```
"Soll ich /scenario-list ausführen um alle Szenarien anzuzeigen?"
```

---

### `/scenario-create` - Szenario erstellen

**Trigger-Keywords**:
- `neues szenario`
- `szenario erstellen`
- `create scenario`
- `projekt setup`
- `neues projekt mit agents`

**Pattern-Beispiele**:
```
✓ "Erstelle ein neues Szenario für E-Commerce"
✓ "Neues Szenario: Mobile App Development"
✓ "Create scenario for API development"
✓ "Ich brauche ein Projekt-Setup mit spezialisierten Agents"
```

**Anti-Patterns (NICHT triggern)**:
```
✗ "szenario aktivieren" (Switch, nicht Create)
✗ "welches szenario" (Question, nicht Create)
```

**Confidence**: High (9-10)

**Confirmation**:
```
"Soll ich /scenario-create nutzen um ein neues Szenario mit Agents und Commands zu erstellen?"
```

---

## Dashboard-Szenario Commands

### `/dashboard-dev` - Development Server

**Trigger-Keywords**:
- `starte dashboard`
- `dev server`
- `development starten`
- `run dashboard`
- `dashboard starten`

**Pattern-Beispiele**:
```
✓ "Starte den Dashboard Dev Server"
✓ "Run the dashboard"
✓ "Development Server starten"
✓ "Starte das Dashboard lokal"
```

**Requires**: Szenario `evolving-dashboard` aktiv

**Confirmation**:
```
"Soll ich /dashboard-dev ausführen um den Development Server zu starten?"
```

---

### `/dashboard-build` - Production Build

**Trigger-Keywords**:
- `build dashboard`
- `production build`
- `dashboard builden`
- `compile dashboard`

**Pattern-Beispiele**:
```
✓ "Build the dashboard for production"
✓ "Erstelle einen Production Build"
✓ "Dashboard builden"
```

**Requires**: Szenario `evolving-dashboard` aktiv

**Confirmation**:
```
"Soll ich /dashboard-build ausführen um einen Production Build zu erstellen?"
```

---

### `/dashboard-deploy` - Railway Deployment

**Trigger-Keywords**:
- `deploy dashboard`
- `dashboard deployen`
- `zu railway pushen`
- `live schalten`
- `deployment starten`

**Pattern-Beispiele**:
```
✓ "Deploy the dashboard to Railway"
✓ "Dashboard deployen"
✓ "Push zu Railway"
✓ "Schalte das Dashboard live"
```

**Requires**: Szenario `evolving-dashboard` aktiv

**Confirmation**:
```
"Soll ich /dashboard-deploy ausführen um zu Railway.app zu deployen?"
```

---

### `/dashboard-test` - Tests ausführen

**Trigger-Keywords**:
- `teste dashboard`
- `run tests`
- `dashboard tests`
- `tests ausführen`

**Pattern-Beispiele**:
```
✓ "Führe die Dashboard Tests aus"
✓ "Run all tests"
✓ "Teste das Dashboard"
✓ "E2E Tests starten"
```

**Requires**: Szenario `evolving-dashboard` aktiv

**Confirmation**:
```
"Soll ich /dashboard-test ausführen? (Quick/Full/E2E/Coverage)"
```

---

## Maintenance

Dieses Dokument sollte erweitert werden wenn:
- Neue Workflows hinzukommen
- User-Feedback zeigt dass Patterns fehlen
- False Positives häufig auftreten
- Neue Use-Cases entstehen

---

**Last Updated**: 2025-12-22
