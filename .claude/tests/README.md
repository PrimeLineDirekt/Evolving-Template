# Agent Testing Framework

**Basiert auf**: Better Agents Testing Pyramid Pattern
**Erstellt**: 2025-12-01

---

## Übersicht

Dieses Framework ermöglicht strukturiertes Testing unserer AI Agents.

```
.claude/tests/
├── README.md           ← Du bist hier
├── scenarios/          ← End-to-End Agent Tests
│   ├── example-scenario.md
│   └── {agent-name}-scenario.md
└── evaluations/        ← Performance-Messungen (TODO)
```

---

## Scenario Tests

### Was sind Scenario Tests?

Scenario Tests simulieren echte Konversationen mit einem Agent und validieren:
- Dass der Agent korrekt auf Inputs reagiert
- Dass die Outputs dem erwarteten Format entsprechen
- Dass Edge Cases behandelt werden

### Struktur eines Scenario Tests

```markdown
# Scenario: {Name}

## Agent
{agent-name}-agent

## Beschreibung
Was wird getestet?

## Setup
Welcher Kontext wird benötigt?

## Test Cases

### Case 1: {Name}
**Input**: {User Input}
**Expected**: {Erwartetes Verhalten/Output}
**Validation**: {Wie wird validiert?}

### Case 2: {Name}
...

## Erfolgskriterien
- [ ] Kriterium 1
- [ ] Kriterium 2
```

---

## Wie man Tests ausführt

### Manuell
1. Öffne den Scenario Test
2. Führe die Test Cases manuell durch
3. Dokumentiere Ergebnisse

### Mit Claude Code
```
"Führe die Scenario Tests für {agent-name} aus"
```

---

## Bestehende Agents zum Testen

| Agent | Scenario File | Status |
|-------|--------------|--------|
| idea-validator-agent | idea-validator-scenario.md | TODO |
| research-analyst-agent | research-analyst-scenario.md | TODO |
| github-repo-analyzer-agent | github-repo-analyzer-scenario.md | Created |
| codebase-analyzer-agent | codebase-analyzer-scenario.md | TODO |

---

## Template

Nutze `.claude/templates/tests/scenario-test.md` für neue Tests.

---

## Referenzen

- [Better Agents Testing Pyramid](https://github.com/langwatch/better-agents)
- [Scenario Testing Best Practices](https://scenario.langwatch.ai/)
