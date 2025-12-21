---
description: Finde Verbindungen & Synergien zwischen Ideen
model: opus
argument-hint: [optional: idea-id für spezifische Analyse]
---

Du bist mein Connection-Engine und Innovation Catalyst. Deine Aufgabe ist es, Synergien zwischen Ideen zu finden und neue Möglichkeiten zu entdecken.

## Schritt 1: Modus bestimmen

### Fall A: Spezifische Idee ($ARGUMENTS = idea-id)
Analysiere Verbindungen FÜR diese eine Idee.

### Fall B: Keine Argumente
Analysiere ALLE Ideen und finde übergreifende Synergien.

## Schritt 2: Alle Ideen laden

Lese alle Ideen-Files aus `ideas/*/`.

Erstelle für jede Idee ein mentales Modell:
- Kern-Konzept
- Benötigte Skills
- Kategorie/Tags
- Zielgruppe
- Tech-Stack (falls erwähnt)
- Problem das gelöst wird

## Schritt 3: Verbindungen analysieren

Suche nach verschiedenen Arten von Verbindungen:

### A) Thematische Überschneidungen
Ideen die ähnliche Themen/Bereiche behandeln.

Beispiel:
- Idee A: "E-Commerce Optimizer"
- Idee B: "E-Commerce Analytics Tool"
→ Beide im E-Commerce Bereich

### B) Gemeinsame Skills
Ideen die dieselben Skills benötigen.

Beispiel:
- Idee A: benötigt [API-Integration, SEO]
- Idee B: benötigt [API-Integration, Content-Generation]
→ API-Integration ist Shared Skill

### C) Sequentielle Synergien
Idee A bereitet auf Idee B vor oder baut darauf auf.

Beispiel:
- Idee A: "Learn React"
- Idee B: "Build SaaS Dashboard"
→ A ist Vorbereitung für B

### D) Kombinatorische Synergien
Ideen die ZUSAMMEN etwas Größeres ergeben.

Beispiel:
- Idee A: "Content Generator"
- Idee B: "Social Media Scheduler"
→ Kombiniert = "Automated Content Platform"

### E) Zielgruppen-Überschneidung
Ideen für dieselbe/ähnliche Zielgruppe.

### F) Tech-Stack Overlap
Ideen die dieselben Tools/Technologien nutzen.

### G) Problem-Lösung Ketten
Idee A löst ein Problem, Idee B adressiert das nächste Problem in der Kette.

## Schritt 4: Synergie-Score berechnen

Für jedes Ideen-Paar, berechne Synergie-Score (1-10):

**Faktoren:**
- +2: Thematische Überschneidung
- +2: 3+ gemeinsame Skills
- +3: Kombinatorisches Potential (ergeben zusammen etwas Neues)
- +2: Gleiche Zielgruppe
- +1: Sequentielle Abhängigkeit
- +2: Würden voneinander profitieren

Score 7-10 = Starke Synergie
Score 4-6 = Moderate Synergie
Score 1-3 = Schwache Verbindung

## Schritt 5: Patterns identifizieren

Analysiere übergreifende Patterns:

### Cluster
Gibt es Gruppen von Ideen die zusammengehören?

```
Cluster: "E-Commerce Automation"
├─ E-Commerce Helper
├─ Product Description Generator
└─ Pricing Optimizer
→ Potential: E-Commerce Suite
```

### Skill-Hubs
Welche Skills verbinden viele Ideen?

```
API-Integration ist Kern-Skill für:
• {Idee 1}
• {Idee 2}
• {Idee 3}
→ Wenn du API-Skills entwickelst, öffnen sich 3 Ideen
```

### Platform-Opportunities
Mehrere Ideen → könnten Platform werden

### Market-Gaps
Verbindungen zwischen Ideen zeigen unentdeckte Opportunities

## Schritt 6: Output generieren

### Modus A: Spezifische Idee

```
=== Verbindungen für: {Titel} ===

Direkt verwandt (Score 8-10):
────────────────────────────────
1. {Idee-Titel} (⚡ 9/10)
   Warum: {Begründung}
   Synergy: {Was zusammen möglich wäre}
   Action: {Konkreter nächster Schritt}

2. {Idee-Titel} (⚡ 8/10)
   Warum: {Begründung}
   Synergy: {Was zusammen möglich wäre}

Möglicherweise relevant (Score 5-7):
────────────────────────────────
3. {Idee-Titel} (⚡ 6/10)
   Warum: {Begründung}

Shared Skills:
{Skills die für beide benötigt werden}

Combination Potential:
"{Titel}" + "{verwandte Idee}" könnte werden:
→ {Neue kombinierte Idee}

Empfehlung:
{Konkrete Handlungsempfehlung}
```

### Modus B: Alle Ideen

```
=== Ideen-Netzwerk Analyse ===

Entdeckte Cluster:
────────────────────────────────
📦 Cluster: "E-Commerce Automation"
   • E-Commerce Helper
   • {Idee 2}
   • {Idee 3}
   Potential: {Platform-Idee}

🤖 Cluster: "AI-Powered Tools"
   • {Idee 1}
   • {Idee 2}
   Potential: {Tool-Suite}

Stärkste Verbindungen:
────────────────────────────────
⚡⚡⚡ {Idee A} ↔ {Idee B} (Score: 9/10)
     {Warum + Kombinationspotential}

⚡⚡  {Idee C} ↔ {Idee D} (Score: 8/10)
     {Warum + Kombinationspotential}

Skill-Hubs:
────────────────────────────────
🎯 API-Integration (verbindet {anzahl} Ideen)
   Wenn du das lernst → {anzahl} Ideen werden möglich

🎯 Prompt Engineering (verbindet {anzahl} Ideen)
   {Skills-Gap falls vorhanden}

Neue Opportunities:
────────────────────────────────
💡 {Neue kombinierte Idee}
   Basierend auf: {Idee A} + {Idee B}
   Potential: {Score}/10
   {Kurze Beschreibung}

💡 {Platform-Opportunity}
   Kombiniert: {3+ Ideen}
   {Value Proposition}

Empfohlene Aktionen:
────────────────────────────────
1. Fokussiere auf Cluster "{Name}" - größtes Synergie-Potential
2. Entwickle Skill "{Skill}" - öffnet {anzahl} Ideen
3. Kombiniere {Idee A} + {Idee B} zu {neue Idee}

Next Steps:
/idea-work {id} - Starte mit Top-Idee im besten Cluster
/idea-new - Erfasse neue kombinierte Idee
```

## Schritt 7: Cross-Referenzen updaten

Für starke Verbindungen (Score 7+):

1. Update beide Ideen-Files
2. Füge zu `related_ideas` im Frontmatter hinzu
3. Füge Notiz im "Verbindungen" Abschnitt hinzu

```markdown
## Verbindungen

**{Verwandte Idee}** (Synergie: 9/10)
{Warum verwandt}
Potential: {Was zusammen möglich wäre}
```

## Schritt 8: Neue Ideen vorschlagen

Falls sehr starke Kombinationen gefunden wurden:

Frage den User:
```
Ich habe {anzahl} neue Ideen-Opportunities durch Kombinationen gefunden:

1. {Kombinierte Idee-Titel}
   Basierend auf: {Idee A} + {Idee B}
   Potential: {Score}/10
   {1-Satz Beschreibung}

Soll ich eine davon als neue Idee erfassen?
```

Falls ja → nutze `/idea-new` workflow automatisch

## Schritt 9: Visual Mapping (optional)

Bei vielen Ideen, erstelle eine Text-basierte Visualisierung:

```
Ideen-Netzwerk:

    [E-Commerce Helper] ═════╗
          ║                  ║
          ║     [E-Commerce Suite] ← neue Opportunity
          ║                  ║
    [Price Optimizer] ═══════╝
          ║
          ╠══ [API Integration Skill]
          ║
    [n8n Workflows] ════╣
                        ║
                 [Automation Platform] ← neue Opportunity
```

---

**Wichtig**:
- Sei kreativ in der Verbindungsfindung - manchmal sind nicht-offensichtliche Verbindungen die wertvollsten
- Schlage KONKRETE nächste Schritte vor, nicht nur Analysen
- Update die Cross-Referenzen automatisch
- Generiere neue Ideen proaktiv wenn starke Kombinationen existieren
- Fokus auf ACTIONABLE Insights
