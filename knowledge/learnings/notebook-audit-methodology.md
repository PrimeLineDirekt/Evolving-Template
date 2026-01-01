# Notebook Audit Methodology

**Quelle**: anthropic-cookbook/.claude/skills/cookbook-audit/SKILL.md
**Extrahiert**: 2025-12-28
**Tags**: audit, notebooks, pedagogy, quality, documentation

---

## Überblick

Strukturierte Methodik für die Bewertung von Jupyter Notebooks basierend auf dem Anthropic Cookbook Style Guide.

---

## 4-Dimensionen Scoring

| Dimension | Gewicht | Fokus |
|-----------|---------|-------|
| **Narrative Quality** | 5 Punkte | Storytelling, Flow, Klarheit |
| **Code Quality** | 5 Punkte | Best Practices, Lesbarkeit |
| **Technical Accuracy** | 5 Punkte | Korrektheit, aktuelle APIs |
| **Actionability** | 5 Punkte | Umsetzbarkeit, Wissenstransfer |

**Total**: 20 Punkte

---

## Learning Objectives Framework

### Terminal Learning Objectives (TLOs)

Was der Leser am ENDE können sollte:
- 2-4 pro Notebook
- Action Verbs: Build, Implement, Deploy, Configure
- Spezifisch und messbar

**Beispiel**:
```
By the end of this cookbook, you'll be able to:
- Build a multi-agent research system with parallel execution
- Implement effective delegation patterns for complex queries
- Deploy production-ready orchestration workflows
```

### Enabling Learning Objectives (ELOs)

Zwischen-Schritte um TLOs zu erreichen:
- Feinere Granularität
- Pro Section definiert

---

## Struktur-Checkliste

### 1. Introduction (Required)

- [ ] **Problem Hook** (1-2 Sätze): Welches Problem lösen wir?
- [ ] **Why it matters** (1-2 Sätze): Warum ist das wichtig?
- [ ] **Learning Objectives** (2-4 Bullets): "By the end..."
- [ ] **Fokus auf Value**, nicht Machinery
- [ ] Optional: Broader Applications

**Anti-Pattern**:
```
❌ "We will build a research agent using the Claude SDK..."
✅ "Your team spends hours triaging CI failures..."
```

### 2. Prerequisites & Setup (Required)

- [ ] Required Knowledge klar gelistet
- [ ] Python Version spezifiziert
- [ ] API Keys mit Links
- [ ] `%%capture` für pip install
- [ ] `dotenv.load_dotenv()` statt `os.environ`
- [ ] `MODEL` Konstante am Anfang
- [ ] Grouped installs

### 3. Core Content

- [ ] Logische Section-Progression
- [ ] **Text VOR Code** (was wir tun werden)
- [ ] **Text NACH Code** (was wir gelernt haben)
- [ ] Headers für Sections
- [ ] Demonstration > Documentation

### 4. Conclusion (Recommended)

- [ ] Mapping zurück zu TLOs
- [ ] Zusammenfassung der Erkenntnisse
- [ ] Anwendung auf User's Context
- [ ] Next Steps / Related Resources

---

## Code Quality Checklist

- [ ] Explanatory text vor jedem Code Block
- [ ] Keine hardcoded API Keys
- [ ] Meaningful variable names
- [ ] Comments erklären "why" nicht "what"
- [ ] Model name als Konstante
- [ ] Type hints auf Funktionen
- [ ] Modern Python (`str | None` statt `Optional[str]`)
- [ ] Early returns over nested conditionals

---

## Anti-Patterns

### Introduction
- ❌ Leading with machinery ("We will build...")
- ❌ Feature dumps ohne Context
- ❌ Vague learning objectives ("Learn about agents")

### Setup
- ❌ Noisy pip install output
- ❌ Multiple separate pip commands
- ❌ `os.environ["API_KEY"] = "your_key"`
- ❌ Hardcoding model names throughout

### Code Presentation
- ❌ Code ohne vorherigen Text
- ❌ Keine Erklärung nach Code-Ausführung
- ❌ Comments die "what" erklären (selbsterklärend!)

### Conclusion
- ❌ Generic summaries ("We've demonstrated...")
- ❌ Nur Wiederholung ohne Guidance
- ❌ Kein Mapping zu TLOs

---

## Audit Workflow

```
1. Style Guide lesen (style_guide.md)
2. validate_notebook.py ausführen
   → Automatische Checks (Secrets, Structure)
   → Markdown-Export für Review
3. Markdown-Version reviewen
4. Jede Dimension scoren
5. Report erstellen (Format unten)
6. Spezifische Verbesserungen mit Line References
```

---

## Audit Report Format

```markdown
### Executive Summary
- **Overall Score**: X/20
- **Key Strengths** (2-3 bullets)
- **Critical Issues** (2-3 bullets)

### Detailed Scoring

#### 1. Narrative Quality: X/5
[Justification mit Beispielen]

#### 2. Code Quality: X/5
[Justification mit Beispielen]

#### 3. Technical Accuracy: X/5
[Justification mit Beispielen]

#### 4. Actionability & Understanding: X/5
[Justification mit Beispielen]

### Specific Recommendations
[Priorisierte, actionable Liste]

### Examples & Suggestions
[Konkrete Excerpts mit Verbesserungsvorschlägen]
```

---

## Content Philosophy: Action + Understanding

> "Cookbooks are primarily action-oriented but strategically incorporate understanding."

**Core Principles**:
1. **Practical focus** - Working code für spezifische Tasks
2. **Problem-first framing** - Value delivered, nicht machinery
3. **Builder's perspective** - Echte Probleme lösen
4. **Agency-building** - Verstehen warum, nicht nur wie
5. **Transferable knowledge** - Patterns über Beispiel hinaus
6. **Critical thinking** - Limitations erkennen
7. **Learning contracts** - TLOs → Mapping in Conclusion

---

## Related

- [Session Evaluation Rule](../.claude/rules/session-evaluation.md)
- [Technical Code Review Pattern](technical-code-review-pattern.md)
- [Self-Improving Rules Pattern](patterns/self-improving-rules-pattern.md)
