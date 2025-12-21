---
description: Bearbeitet ein Szenario (Components hinzufügen/entfernen)
model: sonnet
argument-hint: [scenario-name]
---

Du bearbeitest ein bestehendes Szenario.

## Ablauf

### 1. Szenario ermitteln
Falls `$ARGUMENTS` gegeben → nutze als Szenario-Name
Falls nicht → Zeige Liste und frage welches

### 2. Szenario laden
Lies `.claude/scenarios/{name}/scenario.json`

### 3. Aktuelle Konfiguration zeigen
```
## Szenario: {display_name}

### Agents ({count})
{Liste aller Agents mit kurzer Beschreibung}

### Commands ({count})
{Liste aller Commands mit kurzer Beschreibung}

### Skills ({count})
{Liste aller Skills}

### Knowledge ({count})
{Liste der Knowledge-Dateien}

### Status
{status} | Tech: {tech_stack kurz}
```

### 4. Aktion abfragen
Frage den User was er tun möchte:
- **Agent hinzufügen** - Neuen Agent erstellen
- **Agent entfernen** - Agent aus Szenario entfernen
- **Command hinzufügen** - Neuen Command erstellen
- **Command entfernen** - Command entfernen
- **Skill hinzufügen** - Skill zum Szenario hinzufügen
- **Knowledge hinzufügen** - Wissen hinzufügen
- **Konfiguration ändern** - scenario.json editieren
- **Fertig** - Bearbeitung beenden

### 5. Aktion ausführen

#### Agent hinzufügen
1. Frage nach Domain/Expertise
2. Erstelle Agent-Datei basierend auf Template-Struktur
3. Speichere in `.claude/scenarios/{name}/agents/`
4. Aktualisiere scenario.json

#### Agent entfernen
1. Zeige Liste der Agents
2. Bestätigung einholen
3. Aus scenario.json entfernen (Datei bleibt optional erhalten)

#### Command hinzufügen
1. Frage nach Command-Name und Zweck
2. Erstelle Command-Datei
3. Speichere in `.claude/scenarios/{name}/commands/`
4. Aktualisiere scenario.json
5. Füge Plain-Text Trigger zu workflow-patterns.md hinzu

#### Konfiguration ändern
1. Zeige aktuelle scenario.json (formatiert)
2. Frage was geändert werden soll
3. Aktualisiere Datei

### 6. Loop
Zurück zu Schritt 3 bis User "Fertig" wählt.

### 7. Zusammenfassung
```
Szenario "{name}" aktualisiert!

## Änderungen
{Liste der vorgenommenen Änderungen}

Nutze /scenario {name} zum Aktivieren.
```

## Plain-Text Trigger
- "szenario bearbeiten"
- "szenario anpassen"
- "agent hinzufügen"
- "command hinzufügen"
