# Prompt Pro Framework - Complete Reference

Diese Datei enthält die vollständige Dokumentation des Prompt Pro Frameworks.

---

## Übersicht

**Prompt Pro** ist ein Meta-Prompt-System das beliebige Anfragen in optimale, Claude-spezifische Prompts transformiert.

**Kernphilosophie**:
- Niemals das Problem lösen - NUR den perfekten Prompt erstellen
- Start simple, escalate smart
- Kontext ist König

---

## Die 5-Level Technique Hierarchy

### Level 1: Foundation (70% aller Fälle)

**Wann verwenden**:
- Einfache, klare Anfragen
- Faktenfragen
- Direkte Instruktionen

**Techniken**:

#### Clear & Direct
```xml
<context>
  Vollständige Hintergrundinformationen.
  Wer fragt? Warum? Was ist der Kontext?
</context>

<task>
  Klare, unmissverständliche Aufgabe.
  Was genau soll getan werden?
</task>

<output_format>
  Exaktes gewünschtes Format.
</output_format>
```

#### XML Structure
Semantische Tags für Klarheit:
- `<context>` - Hintergrund
- `<task>` - Aufgabe
- `<constraints>` - Einschränkungen
- `<output_format>` - Gewünschtes Format

**Beispiel**:
```xml
<context>
  Ich betreibe einen Online-Shop für digitale Produkte.
  Zielgruppe: Millennials, Design-interessiert.
</context>

<task>
  Erstelle 5 Titel-Varianten für ein minimalistisches digitales Produkt.
  Maximale Länge: 140 Zeichen.
</task>

<output_format>
  Nummerierte Liste mit Zeichenanzahl pro Titel.
</output_format>
```

---

### Level 2: Enhanced

**Wann verwenden**:
- Wenn Level 1 nicht ausreicht
- Komplexere Analysen
- Wenn Konsistenz wichtig ist

**Techniken**:

#### Multishot Examples (Few-Shot)
```xml
<examples>
  <example>
    <input>Minimalist mountain poster, earth tones</input>
    <output>
      1. "Serene Peak | Modern Mountain Wall Art | Earthy Minimalist Print" (62 chars)
      2. "Mountain Solitude | Contemporary Nature Decor | Warm Tones" (58 chars)
    </output>
  </example>

  <example>
    <input>Abstract ocean waves, blue palette</input>
    <output>
      1. "Ocean Rhythm | Abstract Wave Art | Coastal Blue Print" (54 chars)
      2. "Tidal Dreams | Modern Sea Wall Decor | Navy Abstract" (52 chars)
    </output>
  </example>
</examples>

<task>
  Erstelle Titel für: {USER_INPUT}
  Folge dem Stil der Beispiele.
</task>
```

#### Structured Chain-of-Thought
```xml
<task>Analysiere die Konkurrenz für {NICHE}</task>

<thinking_process>
  Arbeite diese Schritte durch:

  1. IDENTIFIZIEREN
     - Wer sind die Top 5 Konkurrenten?
     - Was macht sie erfolgreich?

  2. ANALYSIEREN
     - Preisstruktur
     - Produktangebot
     - Unique Selling Points

  3. BEWERTEN
     - Stärken und Schwächen
     - Marktlücken

  4. EMPFEHLEN
     - Konkrete Handlungsempfehlungen
</thinking_process>

<output_format>
  Strukturierter Report mit allen 4 Sections.
</output_format>
```

#### Role Assignment
```xml
<role>
  Du bist ein Senior E-Commerce Strategist mit 15 Jahren Erfahrung
  im digitalen Produktvertrieb. Du hast hunderte Online-Shops analysiert
  und weißt genau, was funktioniert und was nicht.

  Dein Expertise-Level: Branchenexperte
  Deine Perspektive: Datengetrieben, aber kreativ
  Dein Kommunikationsstil: Direkt, actionable
</role>
```

---

### Level 3: Complex

**Wann verwenden**:
- Multi-Step Aufgaben
- Wenn Zwischenergebnisse nötig
- Qualitätskontrolle wichtig

**Techniken**:

#### Prompt Chaining
```xml
<phase_1>
  <objective>Recherche</objective>
  <task>Sammle alle relevanten Informationen zu {TOPIC}</task>
  <output>Strukturierte Faktensammlung</output>
</phase_1>

<phase_2>
  <input>{{phase_1.output}}</input>
  <objective>Analyse</objective>
  <task>Analysiere die gesammelten Informationen</task>
  <output>Analyse-Report mit Insights</output>
</phase_2>

<phase_3>
  <input>{{phase_2.output}}</input>
  <objective>Empfehlungen</objective>
  <task>Leite konkrete Handlungsempfehlungen ab</task>
  <output>Priorisierte Action Items</output>
</phase_3>
```

#### Verification Loops
```xml
<process>
  <step_1>GENERATE - Erstelle ersten Entwurf</step_1>
  <step_2>REVIEW - Prüfe gegen Kriterien</step_2>
  <step_3>REFINE - Verbessere basierend auf Review</step_3>
  <step_4>VALIDATE - Finale Qualitätsprüfung</step_4>
</process>

<quality_criteria>
  - Vollständigkeit: Alle Anforderungen erfüllt?
  - Klarheit: Verständlich für Zielgruppe?
  - Actionability: Konkret umsetzbar?
</quality_criteria>
```

#### Conditional Branching
```xml
<task>Analysiere {INPUT}</task>

<branching>
  IF input_type == "quantitative":
    → Nutze statistische Analyse
    → Output: Zahlen, Trends, Visualisierungen

  ELIF input_type == "qualitative":
    → Nutze thematische Analyse
    → Output: Themes, Patterns, Quotes

  ELSE:
    → Nutze Mixed-Methods
    → Output: Kombinierte Insights
</branching>

<fallback>
  Bei unklarem Input:
  → Frage nach Klärung
  → Oder: Behandle als qualitativ
</fallback>
```

---

### Level 4: Advanced

**Wann verwenden**:
- Research-Grade Aufgaben
- Komplexe Problemlösung
- Wenn maximale Qualität nötig

**Techniken**:

#### Extended Thinking
```xml
<thinking_budget>
  Complexity: research-grade
  Recommended tokens: 8000-16000

  Nutze extended thinking für:
  - Tiefe Analyse
  - Multiple Perspektiven
  - Selbst-Korrektur
</thinking_budget>

<task>
  Entwickle eine Go-to-Market Strategie für {PRODUCT}.

  Denke umfassend nach über:
  - Marktanalyse
  - Wettbewerbslandschaft
  - Positionierung
  - Pricing
  - Channels
  - Messaging
</task>
```

#### Least-to-Most Decomposition
```xml
<decomposition>
  Zerlege das Problem in Teilprobleme.
  Löse vom Einfachsten zum Komplexesten.

  <level_1>Grundlegende Fakten sammeln</level_1>
  <level_2>Einfache Zusammenhänge identifizieren</level_2>
  <level_3>Komplexe Patterns erkennen</level_3>
  <level_4>Synthese und Empfehlungen</level_4>

  Jedes Level baut auf dem vorherigen auf.
</decomposition>
```

#### Tree of Thought
```xml
<problem>{COMPLEX_PROBLEM}</problem>

<exploration>
  Exploriere DREI verschiedene Lösungsansätze parallel:

  <path_a>
    <approach>Konservativer Ansatz</approach>
    <steps>...</steps>
    <evaluation>Pros, Cons, Risiken</evaluation>
  </path_a>

  <path_b>
    <approach>Innovativer Ansatz</approach>
    <steps>...</steps>
    <evaluation>Pros, Cons, Risiken</evaluation>
  </path_b>

  <path_c>
    <approach>Hybrid Ansatz</approach>
    <steps>...</steps>
    <evaluation>Pros, Cons, Risiken</evaluation>
  </path_c>
</exploration>

<selection>
  Wähle den besten Pfad basierend auf:
  - Machbarkeit
  - Impact
  - Risiko
</selection>
```

---

### Level 5: Specialized

**Wann verwenden**:
- Spezifische Edge Cases
- Repetitive Tasks
- Strikte Format-Requirements

**Techniken**:

#### Prefilling (Assistant Prefill)
```xml
<task>Erstelle JSON Output</task>

<assistant_prefill>
{
  "analysis": {
</assistant_prefill>

<!-- Claude vervollständigt ab hier im exakten Format -->
```

#### Prompt Caching
```xml
<cached_context>
  <!-- Dieser Teil wird gecached (1h) -->
  <domain_knowledge>
    Umfangreiches Domänenwissen hier...
    (Kann sehr lang sein - wird nur einmal verarbeitet)
  </domain_knowledge>

  <examples>
    Viele Beispiele hier...
  </examples>
</cached_context>

<dynamic_query>
  <!-- Nur dieser Teil ändert sich -->
  Aktuelle Anfrage: {USER_INPUT}
</dynamic_query>
```

#### Maieutic Prompting (Sokratisch)
```xml
<task>Finde die beste Lösung für {PROBLEM}</task>

<socratic_process>
  Führe dich selbst durch Fragen zur Lösung:

  1. "Was weiß ich sicher über dieses Problem?"
  2. "Welche Annahmen mache ich?"
  3. "Was würde passieren wenn Annahme X falsch ist?"
  4. "Welche Perspektive fehlt mir?"
  5. "Was ist die einfachste Erklärung?"

  Beantworte jede Frage ehrlich bevor du weitermachst.
</socratic_process>
```

---

## Technique Selection Guide

### Quick Decision Tree

```
START
  │
  ├─ Einfache Faktenfrage?
  │   └─ YES → Level 1 (Clear & Direct)
  │
  ├─ Braucht Beispiele für Konsistenz?
  │   └─ YES → Level 2 (Few-Shot)
  │
  ├─ Multi-Step mit Zwischenergebnissen?
  │   └─ YES → Level 3 (Chaining)
  │
  ├─ Research-Grade, maximale Tiefe?
  │   └─ YES → Level 4 (Extended Thinking)
  │
  └─ Spezialfall (Format, Caching)?
      └─ YES → Level 5 (Specialized)
```

### Matrix nach Aufgabentyp

| Aufgabe | Level | Primärtechnik | Sekundär |
|---------|-------|---------------|----------|
| Faktenfrage | 1 | Clear & Direct | - |
| Übersetzung | 1 | XML Structure | Examples |
| Analyse | 2 | Structured CoT | Role |
| Kreativ | 2 | Role + Context | Few-Shot |
| Code | 2-3 | Examples | Chaining |
| Recherche | 4 | Extended Thinking | Decomposition |
| Strategie | 4 | Tree of Thought | Verification |
| Entscheidung | 3-4 | Branching | Contrastive |

---

## Output Templates

### Für Analyse-Prompts
```xml
<output_structure>
  <executive_summary>
    3-5 Bullet Points der wichtigsten Findings
  </executive_summary>

  <detailed_analysis>
    <section_1>
      <finding>Was wurde gefunden</finding>
      <evidence>Belege/Daten</evidence>
      <implication>Was bedeutet das</implication>
    </section_1>
    <!-- Weitere Sections -->
  </detailed_analysis>

  <recommendations>
    Priorisierte, actionable Empfehlungen
  </recommendations>

  <limitations>
    Was wurde nicht berücksichtigt
  </limitations>
</output_structure>
```

### Für Kreative Prompts
```xml
<output_structure>
  <options>
    <option_1>
      <content>Der kreative Output</content>
      <rationale>Warum diese Variante</rationale>
    </option_1>
    <!-- 2-3 weitere Optionen -->
  </options>

  <recommendation>
    Welche Option für welchen Kontext
  </recommendation>
</output_structure>
```

### Für Research-Prompts
```xml
<output_structure>
  <key_findings>
    Nummerierte Liste der Haupterkenntnisse
  </key_findings>

  <evidence_map>
    | Finding | Source | Confidence |
    |---------|--------|------------|
  </evidence_map>

  <knowledge_gaps>
    Was konnte nicht beantwortet werden
  </knowledge_gaps>

  <next_steps>
    Empfohlene weitere Recherche
  </next_steps>
</output_structure>
```

---

## Quality Checklist

Vor Abschluss jedes Prompts prüfen:

### Must-Have
- [ ] **Colleague Test**: Würde ein Fachfremder verstehen was zu tun ist?
- [ ] **Context Complete**: Ist ALLES nötige Wissen im Prompt?
- [ ] **Success Defined**: Ist klar wann die Aufgabe erfüllt ist?
- [ ] **Output Specified**: Ist das gewünschte Format eindeutig?

### Should-Have
- [ ] **Right Level**: Nicht über- oder unter-engineered?
- [ ] **Examples Present**: Bei Level 2+ passende Beispiele?
- [ ] **Thinking Guided**: Bei Analyse Denkschritte vorgegeben?

### Nice-to-Have
- [ ] **Fallbacks**: Was passiert bei Edge Cases?
- [ ] **Performance**: Token-Budget angemessen?
- [ ] **Alternatives**: Andere Approaches angeboten?

---

## Common Pitfalls

### Over-Engineering
```
❌ FALSCH: Level 4 Extended Thinking für "Was ist die Hauptstadt von Frankreich?"
✅ RICHTIG: Level 1 Clear & Direct
```

### Under-Specifying
```
❌ FALSCH: "Analysiere das"
✅ RICHTIG: "Analysiere die Verkaufszahlen Q3 2024 nach Produktkategorie,
            identifiziere Top 3 Performer und Underperformer,
            erkläre mögliche Gründe"
```

### Missing Context
```
❌ FALSCH: "Schreibe bessere Produkttitel"
✅ RICHTIG: "Schreibe Produkttitel für E-Commerce Plattform, Zielgruppe: 25-40 Jahre,
            Stil: minimalistisch modern, max 140 Zeichen,
            inkludiere relevante Keywords"
```

### Ambiguous Output
```
❌ FALSCH: "Gib mir eine Analyse"
✅ RICHTIG: "Erstelle eine Analyse mit:
            1. Executive Summary (max 100 Wörter)
            2. 3-5 Key Findings als Bullets
            3. Empfehlungen als nummerierte Liste"
```

---

## Performance Considerations

### Token Budget Guidelines

| Task Type | Input | Thinking | Output | Total |
|-----------|-------|----------|--------|-------|
| Simple | 500 | 0 | 200 | ~700 |
| Standard | 1000 | 0 | 500 | ~1500 |
| Analysis | 2000 | 2000 | 1000 | ~5000 |
| Research | 3000 | 8000 | 2000 | ~13000 |
| Deep | 5000 | 16000 | 3000 | ~24000 |

### Latency Expectations

- Level 1: < 5 Sekunden
- Level 2: 5-15 Sekunden
- Level 3: 15-30 Sekunden
- Level 4: 30-90 Sekunden
- Level 5: Variabel

---

## Integration mit Evolving

### Verfügbare Kontexte

Der Prompt kann auf Evolving-Ressourcen verweisen:

```xml
<evolving_context>
  - Knowledge Base: knowledge/
  - Prompts Library: knowledge/prompts/
  - Project Docs: knowledge/projects/
  - Patterns: knowledge/patterns/
  - Personal: knowledge/personal/
</evolving_context>
```

### Empfohlene Agents

Für Prompt-Ausführung können diese Agents relevant sein:
- `research-analyst-agent` - Für Research-Prompts
- `idea-validator-agent` - Für Validierungs-Prompts
- `knowledge-synthesizer-agent` - Für Synthese-Prompts

---

**Version**: 1.0
**Basiert auf**: Prompt Pro 2.0 Framework
**Letzte Aktualisierung**: 2025-12-01
