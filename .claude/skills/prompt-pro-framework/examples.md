# Prompt Pro Framework - Practical Examples

Konkrete Beispiele für jeden Level und verschiedene Anwendungsfälle.

---

## Level 1 Examples: Foundation

### Example 1.1: Faktenfrage

**Input**: "Was sind die besten Zeiten um neue Produkte zu veröffentlichen?"

**Generierter Prompt**:
```xml
<context>
  Plattform: E-Commerce Marktplatz (Online-Shop für digitale/physische Produkte)
  Ziel: Maximale Sichtbarkeit für neue Angebote
</context>

<task>
  Liste die optimalen Veröffentlichungszeiten für neue Produkte auf.
  Berücksichtige:
  - Zeitzonen (primär Zielmarkt)
  - Wochentage vs. Wochenende
  - Saisonale Unterschiede
</task>

<output_format>
  - Tabelle: Wochentag | Beste Zeit | Warum
  - Zusätzliche Tipps als Bullets
</output_format>
```

**Technique Level**: 1 (Clear & Direct)
**Warum**: Faktenfrage, keine Analyse nötig

---

### Example 1.2: Einfache Übersetzung/Umwandlung

**Input**: "Wandle diese Produktbeschreibung in Bullets um: [text]"

**Generierter Prompt**:
```xml
<task>
  Wandle folgenden Fließtext in prägnante Bullet Points um.
</task>

<input_text>
  {USER_TEXT}
</input_text>

<constraints>
  - Maximal 6 Bullets
  - Jeder Bullet: 5-10 Wörter
  - Wichtigstes zuerst
  - Aktive Sprache
</constraints>

<output_format>
  • Bullet 1
  • Bullet 2
  ...
</output_format>
```

**Technique Level**: 1 (XML Structure)

---

## Level 2 Examples: Enhanced

### Example 2.1: Mit Few-Shot Examples

**Input**: "Erstelle SEO-Titel für meine Produkte"

**Generierter Prompt**:
```xml
<role>
  Du bist ein E-Commerce SEO Spezialist mit Fokus auf digitale Produkte.
  Du kennst die aktuellen Trends und weißt welche Keywords ranken.
</role>

<context>
  Shop: {your-shop} (Digitale Produkte)
  Stil: Modern, minimalistisch
  Zielgruppe: 25-40 Jahre, interessiert an {niche}
</context>

<examples>
  <example>
    <product>Minimalist mountain landscape, earth tones</product>
    <title>Mountain Serenity Print | Minimalist Nature Wall Art | Earth Tone Landscape | Digital Download | Modern Home Decor</title>
    <why_it_works>
      - Primary keyword vorne (Mountain)
      - Style keywords (Minimalist, Modern)
      - Format keywords (Print, Digital Download, Wall Art)
      - 13 Wörter, 127 Zeichen
    </why_it_works>
  </example>

  <example>
    <product>Abstract ocean waves, blue gradient</product>
    <title>Ocean Waves Abstract Art | Blue Gradient Wall Print | Coastal Home Decor | Downloadable Art | Modern Beach House</title>
    <why_it_works>
      - Beschreibend + Abstract
      - Farbe genannt (Blue)
      - Lifestyle keywords (Coastal, Beach House)
      - 14 Wörter, 119 Zeichen
    </why_it_works>
  </example>
</examples>

<task>
  Erstelle einen SEO-optimierten Titel für:
  {PRODUCT_DESCRIPTION}

  Folge dem Muster der Beispiele.
</task>

<output_format>
  <title>Der optimierte Titel</title>
  <character_count>Anzahl Zeichen</character_count>
  <keywords_used>Liste der Keywords</keywords_used>
</output_format>
```

**Technique Level**: 2 (Few-Shot + Role)

---

### Example 2.2: Structured Chain-of-Thought

**Input**: "Analysiere ob ich in die neue Nische einsteigen soll"

**Generierter Prompt**:
```xml
<role>
  Du bist ein E-Commerce Marktanalyst spezialisiert auf digitale Produkte
  und Online-Marktplätze.
</role>

<context>
  Aktueller Shop: {your-shop} ({current-style})
  Überlegung: Expansion in {new-niche}
  Budget für neue Produkte: Begrenzt
</context>

<task>
  Analysiere die {target-niche} für digitale Produkte.
  Gib eine fundierte Empfehlung ob Markteintritt sinnvoll ist.
</task>

<thinking_process>
  Arbeite diese Schritte explizit durch:

  SCHRITT 1: MARKTGRÖSSE
  - Wie groß ist die Ziel-Nische?
  - Suchvolumen-Indikatoren?
  - Wachstumstrend?

  SCHRITT 2: WETTBEWERB
  - Wie viele etablierte Anbieter?
  - Was sind deren Stärken?
  - Gibt es Marktlücken?

  SCHRITT 3: FIT-ANALYSE
  - Passt die neue Nische zu meinem aktuellen Stil?
  - Skill-Transfer möglich?
  - Kannibalisierung bestehender Produkte?

  SCHRITT 4: RISIKO-BEWERTUNG
  - Investition (Zeit/Geld) vs. Potential
  - Downside wenn es nicht funktioniert?

  SCHRITT 5: EMPFEHLUNG
  - Go / No-Go / Modifizierter Ansatz?
</thinking_process>

<output_format>
  <executive_summary>
    Empfehlung in 2-3 Sätzen
  </executive_summary>

  <analysis>
    Für jeden Schritt: Finding + Begründung
  </analysis>

  <recommendation>
    Konkrete nächste Schritte wenn Go
    ODER Alternativen wenn No-Go
  </recommendation>

  <confidence>
    Wie sicher ist diese Einschätzung? (1-10)
    Was würde mehr Sicherheit geben?
  </confidence>
</output_format>
```

**Technique Level**: 2 (Structured CoT + Role)

---

## Level 3 Examples: Complex

### Example 3.1: Prompt Chaining

**Input**: "Entwickle eine Content-Strategie für meinen Online-Shop"

**Generierter Prompt**:
```xml
<objective>
  Entwickle eine vollständige Content-Strategie für {your-shop}.
</objective>

<phase_1>
  <name>AUDIT</name>
  <task>
    Analysiere den aktuellen Stand:
    - Welche Content-Typen existieren?
    - Was performt gut/schlecht?
    - Welche Lücken gibt es?
  </task>
  <output>
    Strukturierter Audit-Report
  </output>
</phase_1>

<phase_2>
  <name>RESEARCH</name>
  <input>{{phase_1.output}}</input>
  <task>
    Basierend auf dem Audit:
    - Was machen erfolgreiche Konkurrenten?
    - Welche Content-Trends gibt es?
    - Was sucht die Zielgruppe?
  </task>
  <output>
    Research Findings mit Opportunities
  </output>
</phase_2>

<phase_3>
  <name>STRATEGIE</name>
  <input>{{phase_1.output}} + {{phase_2.output}}</input>
  <task>
    Entwickle die Content-Strategie:
    - Content Pillars definieren
    - Formate und Frequenz
    - Channel-Strategie ({your-platforms})
  </task>
  <output>
    Strategie-Dokument
  </output>
</phase_3>

<phase_4>
  <name>ACTION PLAN</name>
  <input>{{phase_3.output}}</input>
  <task>
    Erstelle konkreten Umsetzungsplan:
    - Erste 30 Tage
    - Content-Kalender Template
    - Ressourcen-Planung
  </task>
  <output>
    Actionable 30-Tage Plan
  </output>
</phase_4>

<synthesis>
  Fasse alle Phasen zusammen in einem
  Executive Summary + Full Strategy Document.
</synthesis>
```

**Technique Level**: 3 (Prompt Chaining)

---

### Example 3.2: Verification Loop

**Input**: "Schreibe eine Produktbeschreibung für mein neues Produkt"

**Generierter Prompt**:
```xml
<context>
  Produkt: {product-description}
  Shop: {your-shop}
  Zielgruppe: {target-audience}
</context>

<process>
  <step_1_generate>
    Schreibe eine erste Version der Produktbeschreibung.
    Länge: 150-200 Wörter
    Inkludiere: Features, Benefits, Use Cases
  </step_1_generate>

  <step_2_review>
    Prüfe die erste Version gegen diese Kriterien:

    SEO-Check:
    □ Primäres Keyword in ersten 50 Wörtern?
    □ Sekundäre Keywords natürlich eingebaut?
    □ Nicht keyword-stuffed?

    Conversion-Check:
    □ Emotional ansprechend?
    □ Benefits klar kommuniziert?
    □ Call-to-Action vorhanden?

    Clarity-Check:
    □ Leicht zu scannen?
    □ Keine Rechtschreibfehler?
    □ Professioneller Ton?

    Dokumentiere was fehlt oder verbessert werden muss.
  </step_2_review>

  <step_3_refine>
    Verbessere die Beschreibung basierend auf dem Review.
    Adressiere jeden identifizierten Punkt.
  </step_3_refine>

  <step_4_validate>
    Finale Prüfung:
    - Erfüllt alle Kriterien?
    - Besser als Konkurrenz?
    - Bereit für Veröffentlichung?
  </step_4_validate>
</process>

<output_format>
  <final_description>
    Die fertige, optimierte Beschreibung
  </final_description>

  <revision_notes>
    Was wurde zwischen V1 und Final geändert
  </revision_notes>
</output_format>
```

**Technique Level**: 3 (Verification Loop)

---

## Level 4 Examples: Advanced

### Example 4.1: Extended Thinking Research

**Input**: "Recherchiere die beste Preisstrategie für digitale Produkte"

**Generierter Prompt**:
```xml
<thinking_budget>
  Complexity: research-grade
  Recommended: 8000-12000 tokens thinking
  Reason: Multi-Faktor Analyse, keine einfache Antwort
</thinking_budget>

<role>
  Du bist ein Pricing Strategy Consultant spezialisiert auf
  digitale Produkte und E-Commerce Marktplätze.
</role>

<research_task>
  Entwickle eine fundierte Preisstrategie für digitale Produkte auf Online-Marktplätzen.

  Denke umfassend nach über:

  MARKTANALYSE
  - Wie sind digitale Produkte typischerweise gepreist?
  - Gibt es Preissegmente? (Budget, Mid, Premium)
  - Korrelation Preis ↔ Verkaufszahlen?

  KOSTENSTRUKTUR
  - Plattform-Gebühren (Listing, Transaction, Payment)
  - Zeitaufwand pro Produkt
  - Marketing-Kosten

  PSYCHOLOGISCHE FAKTOREN
  - Preiswahrnehmung bei digitalen Produkten
  - Ankoring-Effekte
  - Bundle vs. Einzelpreis

  STRATEGISCHE OPTIONEN
  - Penetration Pricing (niedrig starten)
  - Premium Pricing (Qualität signalisieren)
  - Tiered Pricing (verschiedene Versionen/Lizenzen)
  - Dynamic Pricing (Saison, Nachfrage)

  WETTBEWERBSKONTEXT
  - Was verlangen Top-Seller?
  - Gibt es einen "Sweet Spot"?
  - Race to the bottom Risiko?
</research_task>

<output_format>
  <executive_summary>
    Empfohlene Preisstrategie in 3 Sätzen
  </executive_summary>

  <research_findings>
    Für jeden Bereich: Key Insights
  </research_findings>

  <pricing_recommendation>
    <base_price>$X.XX</base_price>
    <price_range>$X - $X</price_range>
    <rationale>Warum diese Preise</rationale>
  </pricing_recommendation>

  <implementation>
    - Sofort-Maßnahmen
    - Test-Strategie (A/B Testing)
    - Wann anpassen
  </implementation>

  <confidence_assessment>
    Confidence: X/10
    Hauptunsicherheiten: ...
    Weitere Research nötig: ...
  </confidence_assessment>
</output_format>
```

**Technique Level**: 4 (Extended Thinking)

---

### Example 4.2: Tree of Thought

**Input**: "Soll ich einen zweiten Online-Shop eröffnen oder den bestehenden erweitern?"

**Generierter Prompt**:
```xml
<decision_context>
  Aktuelle Situation: {your-shop} ({current-style})
  Überlegung: Neue Nische (z.B. {niche-examples})
  Optionen: Zweiter Shop vs. Erweiterung
</decision_context>

<task>
  Exploriere beide Optionen systematisch und gib eine
  fundierte Empfehlung.
</task>

<tree_of_thought>
  <path_a>
    <option>ZWEITER SHOP</option>

    <exploration>
      Denke durch:
      - Brand Separation: Vorteile klarer Fokus
      - SEO: Separate Keyword-Optimierung möglich
      - Aufwand: Doppelte Verwaltung
      - Gebühren: Zusätzliche Plattform-Fees
      - Risiko: Kannibalisierung? Überforderung?
    </exploration>

    <scenarios>
      Best Case: Beide Shops erfolgreich, diversifiziertes Einkommen
      Likely Case: Mehr Arbeit, moderate Zusatzeinnahmen
      Worst Case: Zweiter Shop floppt, Zeit verschwendet
    </scenarios>

    <requirements>
      Was bräuchte es für Erfolg?
    </requirements>
  </path_a>

  <path_b>
    <option>BESTEHENDEN SHOP ERWEITERN</option>

    <exploration>
      Denke durch:
      - Brand Kohärenz: Passt neue Nische zum Image?
      - Cross-Selling: Können Kunden beides kaufen?
      - SEO: Verwässerung oder Verstärkung?
      - Aufwand: Einfacher zu managen
      - Risiko: Brand Confusion?
    </exploration>

    <scenarios>
      Best Case: Breiteres Angebot, mehr Kunden
      Likely Case: Langsames Wachstum, Learning
      Worst Case: Verwirrt bestehende Kunden
    </scenarios>

    <requirements>
      Was bräuchte es für Erfolg?
    </requirements>
  </path_b>

  <path_c>
    <option>HYBRID / PILOT</option>

    <exploration>
      Denke durch:
      - Pilot in bestehendem Shop (5-10 Produkte)
      - Basierend auf Performance: Entscheidung
      - Daten sammeln vor großer Investition
    </exploration>

    <scenarios>
      Best Case: Klare Daten für Entscheidung
      Likely Case: Moderate Insights, Richtung klarer
      Worst Case: Inconclusive, aber wenig verloren
    </scenarios>
  </path_c>
</tree_of_thought>

<synthesis>
  Vergleiche alle drei Pfade:

  | Kriterium | Shop 2 | Erweitern | Pilot |
  |-----------|--------|-----------|-------|
  | Aufwand   |        |           |       |
  | Risiko    |        |           |       |
  | Potential |        |           |       |
  | Reversibilität |   |           |       |

  Empfehlung mit Begründung.
</synthesis>

<output_format>
  <recommendation>Klare Empfehlung</recommendation>
  <reasoning>Warum dieser Pfad</reasoning>
  <next_steps>Konkrete erste Schritte</next_steps>
  <decision_reversibility>Wie einfach umkehrbar?</decision_reversibility>
</output_format>
```

**Technique Level**: 4 (Tree of Thought)

---

## Level 5 Examples: Specialized

### Example 5.1: Prefilling für JSON Output

**Input**: "Generiere Produkt-Metadaten als JSON"

**Generierter Prompt**:
```xml
<task>
  Generiere strukturierte Metadaten für dieses Produkt:
  {PRODUCT_DESCRIPTION}
</task>

<schema>
  {
    "title": "string (max 140 chars)",
    "description": "string (150-200 words)",
    "tags": ["array", "of", "13", "tags"],
    "category": "string",
    "price_suggestion": {
      "min": number,
      "max": number,
      "recommended": number
    },
    "seo_keywords": {
      "primary": "string",
      "secondary": ["array"]
    }
  }
</schema>

<assistant_prefill>
{
  "title": "</assistant_prefill>

<!-- Claude vervollständigt ab hier exakt im Schema -->
```

**Technique Level**: 5 (Prefilling)
**Use Case**: Strikte JSON-Formatierung garantieren

---

### Example 5.2: Maieutic (Sokratisches Prompting)

**Input**: "Hilf mir herauszufinden warum meine Verkäufe stagnieren"

**Generierter Prompt**:
```xml
<context>
  Situation: Verkäufe stagnieren trotz regelmäßiger neuer Angebote
  Ziel: Root Cause finden
</context>

<socratic_process>
  Führe mich durch gezielte Fragen zur Erkenntnis.
  Beantworte jede Frage ehrlich und vollständig bevor
  du zur nächsten gehst.

  FRAGE 1: FAKTEN SAMMELN
  "Was genau meine ich mit 'stagnieren'?
   - Seit wann?
   - Wie viele Verkäufe vorher vs. jetzt?
   - Welche Produkte betroffen?"

  FRAGE 2: VERÄNDERUNGEN
  "Was hat sich geändert in diesem Zeitraum?
   - An meinen Produkten?
   - An meinem Marketing?
   - Am Markt/Wettbewerb?
   - An Plattform-Updates oder Algorithmen?"

  FRAGE 3: ANNAHMEN PRÜFEN
  "Welche Annahmen mache ich?
   - 'Mehr Angebote = mehr Verkäufe'?
   - 'Meine Qualität ist gut genug'?
   - 'Meine Sichtbarkeit ist ausreichend'?"

  FRAGE 4: PERSPEKTIVWECHSEL
  "Wenn ich ein Kunde wäre:
   - Würde ich meine Produkte finden?
   - Würde ich sie kaufen? Warum (nicht)?
   - Was fehlt?"

  FRAGE 5: EINFACHSTE ERKLÄRUNG
  "Was ist die wahrscheinlichste Ursache?
   Nicht die komplexeste - die naheliegendste."
</socratic_process>

<output_format>
  <self_discovery>
    Erkenntnisse aus jeder Frage
  </self_discovery>

  <likely_root_cause>
    Die wahrscheinlichste Hauptursache
  </likely_root_cause>

  <test_hypothesis>
    Wie kann ich diese Hypothese testen?
  </test_hypothesis>

  <first_action>
    Was ist der kleinste erste Schritt?
  </first_action>
</output_format>
```

**Technique Level**: 5 (Maieutic Prompting)
**Use Case**: Selbst-Erkenntnis fördern statt direkte Antwort

---

## Quick Reference: Input → Level

| Input-Typ | Empfohlenes Level | Beispiel |
|-----------|-------------------|----------|
| "Was ist X?" | 1 | Faktenfrage |
| "Liste Y auf" | 1 | Aufzählung |
| "Erstelle Z wie Beispiel" | 2 | Few-Shot |
| "Analysiere A" | 2-3 | Structured CoT |
| "Entwickle Strategie für B" | 3-4 | Chaining + ToT |
| "Recherchiere C umfassend" | 4 | Extended Thinking |
| "Output als JSON" | 5 | Prefilling |
| "Hilf mir verstehen warum" | 5 | Maieutic |

---

## Template zum Kopieren

```xml
<!-- Level 1-2 Basic -->
<context>
  [Hintergrund]
</context>

<task>
  [Aufgabe]
</task>

<output_format>
  [Format]
</output_format>

<!-- Level 3+ Advanced -->
<phase_1>
  <objective>[Ziel]</objective>
  <output>[Zwischenergebnis]</output>
</phase_1>

<phase_2>
  <input>{{phase_1.output}}</input>
  <objective>[Ziel]</objective>
  <output>[Ergebnis]</output>
</phase_2>

<synthesis>
  [Finale Zusammenführung]
</synthesis>
```

---

**Version**: 1.0
**Examples**: 10 (2 pro Level)
**Letzte Aktualisierung**: 2025-12-01
