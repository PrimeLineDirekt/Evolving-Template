# Risk Zone Classification Prompt Template

## Standard Risk Zone Classification

Include this in ALL specialist agent system prompts that provide recommendations:

```markdown
## RISIKO-ZONEN KLASSIFIZIERUNG

WICHTIG: Alle Optionen müssen LEGAL sein. Keine illegalen Strategien anbieten.

### 🟢 GRÜN (Sicher) - PFLICHT: Mind. 2 Optionen
- Standard-Verfahren, von Behörden/Experten akzeptiert
- Etablierte Praxis vorhanden
- Kein besonderes Prüfungsrisiko
- Beispiele: {DOMAIN_GREEN_EXAMPLES}

### 🟡 GELB (Moderate Grauzone) - Optional
- Legal, aber nicht Standard-Weg
- Erhöhtes Prüfungsrisiko
- Dokumentation ZWINGEND erforderlich
- Expertenberatung empfohlen
- Beispiele: {DOMAIN_YELLOW_EXAMPLES}
- OUTPUT: Dokumentationspflicht explizit nennen

### 🟠 ORANGE (Aggressive Grauzone) - Optional
- Legal, aber am absoluten Limit der Auslegung
- Hohes Prüfungsrisiko
- Expertenberatung ZWINGEND
- Detaillierte Dokumentation unerlässlich
- Beispiele: {DOMAIN_ORANGE_EXAMPLES}
- OUTPUT: Risiken klar benennen, Expertenberatung als Pflicht markieren

### ❌ VERBOTEN (Niemals anbieten)
- Illegale Strategien
- Missbrauchskonstrukte
- Täuschung oder Verschleierung
- Nicht-deklarierte Aktivitäten
- Beispiele: {DOMAIN_FORBIDDEN_EXAMPLES}

### MINDEST-ANFORDERUNGEN
- Mind. 2 Optimierungen in 🟢 GRÜN (Pflicht)
- Mind. 3 Optimierungen GESAMT (🟢 + optional 🟡/🟠)
```

## Domain-Specific Examples

### Tax/Finance Domain
```python
DOMAIN_GREEN_EXAMPLES = """
- Standard Wohnsitz-Ummeldung
- Reguläre DBA-Anwendung
- Standard-Versicherungskündigung
"""

DOMAIN_YELLOW_EXAMPLES = """
- 183-Tage-Optimierung mit Puffer
- Holding-Struktur mit echter Substanz
- Steuer-Timing über Jahreswechsel
"""

DOMAIN_ORANGE_EXAMPLES = """
- Aggressive DBA-Interpretation
- Komplexe Umstrukturierungen kurz vor Stichtag
- Grenzfälle bei Ansässigkeitsbestimmung
"""

DOMAIN_FORBIDDEN_EXAMPLES = """
- Scheinwohnsitz ohne echte Substanz
- Nicht deklarierte Vermögen/Einkünfte
- Gestaltungsmissbrauch-Konstrukte
- Steuerhinterziehung
"""
```

### Legal Domain
```python
DOMAIN_GREEN_EXAMPLES = """
- Standard-Vertragskündigung nach Frist
- Regelkonforme Dokumentation
- Etablierte Rechtswege
"""

DOMAIN_YELLOW_EXAMPLES = """
- Alternative Vertragsauslegung
- Verhandlungsspielräume nutzen
- Kulanz-Anfragen
"""

DOMAIN_ORANGE_EXAMPLES = """
- Grenzfälle bei Vertragsinterpretation
- Aggressive Verhandlungstaktiken
- Rechtliche Grauzonen ausnutzen
"""

DOMAIN_FORBIDDEN_EXAMPLES = """
- Vertragsbruch
- Täuschung
- Illegale Umgehung
"""
```

## Output Format for Recommendations

```markdown
### OPTIMIERUNGS-OPTIONEN

| Option | Risiko | Benefit | Aufwand | Empfehlung |
|--------|--------|---------|---------|------------|
| Option A: [Name] | 🟢 | [Benefit] | Niedrig | ⭐⭐⭐⭐⭐ |
| Option B: [Name] | 🟢 | [Benefit] | Mittel | ⭐⭐⭐⭐ |
| Option C: [Name] | 🟡 | [Benefit] | Mittel | ⭐⭐⭐ |
| Option D: [Name] | 🟠 | [Benefit] | Hoch | ⭐⭐ |

### RISIKO-MARKIERUNGEN

🟢 **SICHERE STRATEGIEN:**
- Option A: [Kurzbeschreibung]
- Option B: [Kurzbeschreibung]

🟡 **MODERATE GRAUZONE:**
- Option C: [Kurzbeschreibung]
  - ⚠️ **Dokumentationspflicht**: [Was dokumentieren]
  - 👤 **Empfehlung**: Fachberater konsultieren

🟠 **AGGRESSIVE GRAUZONE:**
- Option D: [Kurzbeschreibung]
  - ⚠️ **Risiken**: [Klare Risikobenennung]
  - 👤 **PFLICHT**: Expertenberatung vor Umsetzung
```

## Validation Rules

1. **Minimum Green Options**: Every recommendation set MUST include at least 2 green options
2. **Total Minimum**: At least 3 options total (green + optional yellow/orange)
3. **No Red Options**: NEVER include forbidden/illegal options
4. **Documentation for Yellow**: Always specify what needs to be documented
5. **Expert Requirement for Orange**: Always mandate expert consultation

## Usage

```python
RISK_ZONE_PROMPT = """
## RISIKO-ZONEN KLASSIFIZIERUNG
[Full content with domain-specific examples]
"""

# Add to system prompt
system_prompt = f"""
{agent_content}

{RISK_ZONE_PROMPT}
"""
```
