---
title: "Prompt Library - High-Performance Prompt Patterns"
type: library-index
category: prompt-engineering
tags: [prompts, patterns, best-practices, inspiration, reusable]
created: 2024-11-22
status: active-collection
---

# Prompt Library - High-Performance Prompt Patterns

**Kuratierte Sammlung hocheffizienter, production-erprobter Prompts als Inspiration und Muster für zukünftige Projekte**

## Zweck dieser Sammlung

Diese Prompt Library ist **keine Code-Bibliothek zum direkten Copy-Paste**, sondern eine **Inspirationsquelle und Lern-Ressource** für effektives Prompt Engineering.

### Was du hier findest:
✅ **Production-Ready Prompts** - Alle Prompts sind in echten Projekten erprobt
✅ **Best Practices** - Patterns die nachweislich funktionieren
✅ **Strukturierungs-Vorlagen** - Wie man Prompts aufbaut
✅ **Domain-Expertise** - Wie man Fach-Autorität etabliert
✅ **Multi-Agent Patterns** - Koordination mehrerer Agents

### Was du NICHT hier findest:
❌ Fertige Prompts zum 1:1 Übernehmen ohne Anpassung
❌ Generische "One-Size-Fits-All" Templates
❌ Ungetestete experimentelle Ansätze

## Philosophie: Learn, Adapt, Create

**Der richtige Workflow:**

1. **Learn** - Studiere die Patterns, verstehe die Struktur
2. **Adapt** - Passe an deine Domain und Use Case an
3. **Create** - Erstelle deinen eigenen, optimierten Prompt

**Nicht:** Copy-Paste ohne Verständnis → Wird nicht funktionieren!

## Kategorien

### 📚 Frameworks (`frameworks/`)
**Meta-Level Prompt Engineering Systeme**

Prompts die **andere Prompts erstellen** oder **Prompt-Engineering-Prozesse** definieren.

**Aktuell:**
1. **Prompt Pro 2.0** - 5-Level Hierarchie, Claude-optimiert, XML-Struktur
   - Use Case: Systematisch Prompts für verschiedene Aufgaben erstellen
   - Key Learning: Hierarchische Technique Selection, Performance Trade-offs
   - Confidence: 95%

2. **Idea Forge** - Adaptives Ideenentwicklungssystem
   - Use Case: Systematische Ideenentwicklung durch iterative Expertenanalyse
   - Key Learning: Divergence → Convergence → Roadmap Process
   - Confidence: 90%

**Wann verwenden:**
- Du brauchst einen strukturierten Prozess für Prompt-Erstellung
- Du willst Ideen systematisch entwickeln und validieren
- Du entwickelst mehrere Prompts und brauchst Konsistenz

### 🔬 Research Agents (`research-agents/`)
**Spezialisierte Research & Data Collection Prompts**

Prompts für **tiefe Recherche**, **Daten-Aggregation** und **Multi-Source Validation**.

**Aktuell:**
- **Research Orchestrator** - Multi-Domain E-Commerce Optimization
  - Use Case: E-Commerce SEO Research mit Confidence Scoring
  - Key Learning: Multi-Domain Workflows, Source Validation, Structured Output

**Wann verwenden:**
- Du brauchst strukturierte Research-Workflows
- Du musst Daten aus mehreren Quellen validieren
- Du willst Confidence Scores für Research-Ergebnisse

### 🎭 Pattern Library (`patterns/`)
**Production-Proven Agent Prompts aus echten Projekten**

Spezialisierte Agent-Prompts die in **Production-Systemen** laufen.

**Aktuell:**
_Keine Patterns im Template. Füge deine eigenen hinzu via /inbox-process._

**Wann verwenden:**
- Du entwickelst Multi-Agent Systeme
- Du brauchst Inspiration für spezialisierte Agents
- Du willst verstehen wie Production-Agents strukturiert sind

### 🛠️ Skills (`skills/`)
**Spezialisierte Workflow Prompts**

Wiederverwendbare Prompts für konkrete, wiederkehrende Workflows.

**Aktuell:**
_Keine Skills im Template. Füge deine eigenen hinzu via /inbox-process._

**Wann verwenden:**
- Du hast einen spezifischen, wiederholbaren Workflow
- Du brauchst domain-spezifische Automation
- Du willst production-ready Tools nutzen

## Wie du diese Library verwendest

### Für neue Projekte

**Schritt 1: Identifiziere deine Anforderung**
- Brauchst du einen Meta-Prozess? → `frameworks/`
- Brauchst du Research-Workflows? → `research-agents/`
- Brauchst du spezialisierte Agents? → `patterns/`

**Schritt 2: Studiere relevante Prompts**
- Lies den kompletten Prompt
- Achte auf Struktur und Patterns
- Verstehe WHY bestimmte Formulierungen gewählt wurden

**Schritt 3: Extrahiere Patterns**
```
Beispiel aus profil-analyse.md:

STRUKTUR-PATTERN:
- Identity Establishment ("Du bist...")
- Core Capabilities (Bulletpoints)
- Input Specification (Was bekommst du)
- Output Format (Strukturierte Sections)
- Quality Criteria (Self-Validation)

→ Übertrage auf deine Domain!
```

**Schritt 4: Adaptiere für deinen Use Case**
- Ersetze Domain-Expertise mit deiner Expertise
- Passe Output-Formate an deine Bedürfnisse an
- Behalte bewährte Strukturen bei

**Schritt 5: Teste und Iteriere**
- Starte mit adaptiertem Prompt
- Teste mit echten Use Cases
- Verfeinere basierend auf Ergebnissen

### Für Prompt Engineering Learning

**Studiere diese Aspekte:**

1. **Tone & Authority**
   - Wie wird Expertise etabliert?
   - Welche Sprache schafft Autorität?
   - Wie wird Domain-Knowledge vermittelt?

2. **Strukturierung**
   - Wie sind Prompts aufgebaut?
   - Welche Sections gibt es?
   - Warum diese Reihenfolge?

3. **Output Control**
   - Wie werden strukturierte Outputs erzwungen?
   - Welche Formate funktionieren?
   - Wie wird Konsistenz sichergestellt?

4. **Quality Gates**
   - Wie validieren Prompts sich selbst?
   - Welche Kriterien werden verwendet?
   - Wie wird schlechter Output verhindert?

5. **Context Management**
   - Wie wird verfügbarer Kontext genutzt?
   - Wie werden Dependencies dokumentiert?
   - Wie wird Cross-Agent Koordination ermöglicht?

## Best Practices aus dieser Library

### ✅ DO's (aus allen Prompts extrahiert)

**1. Klare Identität etablieren**
```markdown
GOOD: "Du bist ein Senior Tax Advisor mit 20+ Jahren Erfahrung in internationaler Steuerplanung..."
BAD:  "Du bist ein Berater."
```

**2. Strukturierte Outputs fordern**
```markdown
GOOD:
AUSGABE-FORMAT:
1. EXECUTIVE SUMMARY (200 Wörter)
2. DETAILLIERTE ANALYSE
3. ACTION ITEMS (Priorisiert)

BAD: "Erstelle eine Analyse."
```

**3. Domain-Language verwenden**
```markdown
GOOD: "Analysiere §6 AStG Wegzugsbesteuerung, DBA-Implikationen..."
BAD:  "Schau dir Steuergesetze an."
```

**4. Quality Criteria einbauen**
```markdown
GOOD:
QUALITÄTS-CHECKS:
✓ Alle kritischen Punkte adressiert
✓ Keine Widersprüche
✓ Mindestens 3 konkrete Action Items

BAD: (keine Quality Gates)
```

**5. Kontext explizit machen**
```markdown
GOOD:
INPUT: 126-Felder User-Profil mit [spezifische Felder]
DEPENDENCIES: Nutze Output von [other_agent]

BAD: (implizite Annahmen)
```

### ❌ DON'Ts (zu vermeiden)

1. **Vage Instruktionen** - "Analysiere die Situation" (zu unspezifisch)
2. **Fehlende Struktur** - Unstrukturierte Outputs sind nicht aggregierbar
3. **Zu generisch** - "Sei ein Experte" (welche Art Experte?)
4. **Ignorieren von Edge Cases** - "Falls Daten fehlen..." muss adressiert werden
5. **Keine Self-Validation** - Ungeprüfte Outputs = schlechte Qualität

## Verwendungs-Matrix

| Use Case | Empfohlene Prompts | Key Learning |
|----------|-------------------|--------------|
| Prompt-Erstellung systematisieren | Prompt Pro 2.0 | Technique Hierarchy, Performance Trade-offs |
| Ideenentwicklung | Idea Forge | Divergence → Convergence → Roadmap Process |
| Research-Workflows | Research Orchestrator | Multi-Domain Workflows, Confidence Scoring |

## Qualitäts-Standards

**Alle Prompts in dieser Library erfüllen:**

✅ **Production-Proven** - Mindestens in einem echten Projekt eingesetzt
✅ **Documented** - Kontext, Use Case, Key Learnings dokumentiert
✅ **Structured** - Klare Sections, konsistente Formate
✅ **Domain-Specific** - Echte Fach-Expertise, nicht generisch
✅ **Quality-Controlled** - Self-Validation Mechanismen eingebaut

**Confidence Levels:**
- ⭐⭐⭐ 95%+ - Battle-tested, mehrere Monate Production
- ⭐⭐ 85-94% - Proven in Production, kürzere Laufzeit
- ⭐ 75-84% - Tested, noch in Optimierung

## Beiträge zu dieser Library

**Wenn du einen Prompt hinzufügen möchtest:**

1. **Production-Ready**: Muss in echtem Projekt verwendet worden sein
2. **Dokumentiert**: Frontmatter mit Use Case, Tags, Confidence
3. **Strukturiert**: Konsistente Sections, klare Formate
4. **Lern-Wert**: Muss spezifische Patterns demonstrieren
5. **Kein Duplicate**: Nicht redundant zu existierenden Prompts

**Kategorien-Auswahl:**
- `frameworks/` - Meta-Level Prompt Engineering
- `research-agents/` - Research & Data Collection
- `patterns/` - Spezialisierte Production Agents
- (Neue Kategorien nach Bedarf)

## Weiterführende Ressourcen

**Projekt-Kontext:**
_Deine Projekte werden hier erscheinen, nachdem du sie mit /project-add hinzufügst._

**Externe Ressourcen:**
- Anthropic Prompt Engineering Guide
- Claude Best Practices

## Statistiken

**Aktuelle Library:**
- **3 Production-Ready Prompts**
- **3 Kategorien** (Frameworks, Research Agents, Skills)
- **Confidence**: 90-95% average across all prompts

**Kategorien-Verteilung:**
- Frameworks: 2 (Prompt Pro 2.0, Idea Forge)
- Research Agents: 1 (Research Orchestrator)
- Skills: 0
- Patterns: 0

**Letzte Aktualisierung:** 2024-11-22

---

**Prompt Library v1.0**
*Learn, Adapt, Create - Production-Proven Prompt Patterns für AI-Assisted Development*

**Knowledge Base**: [← Back to Index](../index.md)
