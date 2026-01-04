# Security Review Pattern

> **Source**: Piebald-AI/claude-code-system-prompts (agent-prompt-security-review-slash.md)
> **Type**: Code Analysis Pattern
> **Confidence Threshold**: 80%+

## Konzept

Strukturierter Sicherheitsreview von Code-Änderungen mit Fokus auf HIGH-CONFIDENCE exploitable vulnerabilities. Minimiert False Positives durch mehrstufige Filterung.

## 3-Phasen-Ansatz

### Phase 1: Repository Context Research

```
1. Repository-Struktur verstehen
2. Bestehende Security-Patterns identifizieren
3. Framework/Library-spezifische Schutzmechanismen erkennen
4. Coding Standards und Conventions erfassen
```

### Phase 2: Comparative Analysis

```
1. Diff/Changes analysieren (git diff main..HEAD)
2. Gegen bestehende Patterns vergleichen
3. Abweichungen von etablierten Praktiken identifizieren
4. Data Flow tracing für sensitive Daten
```

### Phase 3: Vulnerability Assessment

```
1. OWASP Top 10 Kategorien prüfen
2. Confidence Score pro Finding (1-10)
3. Nur Findings mit Score ≥ 8 reporten
4. False-Positive Filtering anwenden
```

## Focus Areas (Was prüfen)

| Kategorie | Beispiele | Severity |
|-----------|-----------|----------|
| **Input Validation** | SQL Injection, Command Injection, XXE, Template Injection | CRITICAL |
| **Auth & AuthZ** | Authentication Bypass, Authorization Flaws, Session Issues | CRITICAL |
| **Cryptography** | Weak Algorithms, Hardcoded Keys, Improper Key Management | HIGH |
| **Code Execution** | Deserialization, Eval, Dynamic Code | CRITICAL |
| **Data Exposure** | Sensitive Data Leaks, PII Exposure, Logging Secrets | HIGH |
| **Access Control** | IDOR, Path Traversal, Privilege Escalation | HIGH |

## Hard Exclusions (Automatisch ignorieren)

Diese Kategorien NICHT als Vulnerabilities reporten:

1. **Memory Safety in Rust** - Compiler garantiert
2. **Unit Test Files** - Nicht Production Code
3. **Regex Injection** - Selten exploitable
4. **Client-Side Validation** - Sollte Server-seitig geprüft werden
5. **Rate Limiting** - Availability, nicht Security
6. **DoS Vulnerabilities** - Separater Review-Prozess
7. **Disk-Stored Secrets** - Separates Secret-Management
8. **Missing HTTPS** - Infrastructure, nicht Code
9. **CORS Configuration** - Kontextabhängig
10. **Generic Error Messages** - UX Entscheidung
11. **Missing Security Headers** - Infrastructure
12. **Outdated Dependencies** - Separater Audit
13. **Code Complexity** - Quality, nicht Security
14. **Missing Logging** - Compliance, nicht Security
15. **Commented Code** - Quality, nicht Security
16. **TODO Comments** - Tracking, nicht Security
17. **Missing Documentation** - Quality, nicht Security

## Output Format

```markdown
## Security Finding: {TITLE}

**Location:** `{file}:{line}`
**Severity:** CRITICAL | HIGH | MEDIUM | LOW
**Category:** {OWASP Category}
**Confidence:** {8-10}/10

### Description
{Was das Problem ist}

### Vulnerable Code
```{language}
{betroffener Code}
```

### Exploit Scenario
{Wie ein Angreifer das ausnutzen könnte}

### Recommendation
{Wie es gefixt werden sollte}

### Fixed Code
```{language}
{korrigierter Code}
```
```

## Confidence Scoring

| Score | Bedeutung | Aktion |
|-------|-----------|--------|
| 10 | Definitiv exploitable, PoC möglich | REPORT |
| 9 | Sehr wahrscheinlich exploitable | REPORT |
| 8 | Wahrscheinlich exploitable | REPORT |
| 7 | Möglicherweise exploitable | SKIP (unter Threshold) |
| 6 | Theoretisch möglich | SKIP |
| 1-5 | Unwahrscheinlich/False Positive | SKIP |

## Workflow

```
1. Git Diff holen
   └─ git diff main..HEAD --name-only
   └─ git diff main..HEAD -- {files}

2. Pro geänderte Datei
   └─ Context verstehen (was macht die Datei?)
   └─ Changes analysieren
   └─ Security-relevante Änderungen identifizieren

3. Pro potentielles Finding
   └─ Confidence Score vergeben
   └─ Gegen Hard Exclusions prüfen
   └─ Falls Score ≥ 8: Dokumentieren

4. Report erstellen
   └─ Findings nach Severity sortieren
   └─ Recommendations hinzufügen
```

## Integration mit Evolving

### Als Command: `/security-review`
- Model: Opus (für tiefe Analyse)
- Input: Git Branch oder Commit Range
- Output: Strukturierter Security Report

### Als Agent: `security-reviewer-agent`
- Spezialisiert auf Code Security
- Nutzt dieses Pattern als Basis
- Kann in Scenarios integriert werden

## Beispiel-Ausführung

```
User: /security-review feature/user-auth

Claude:
1. Analysiere Branch feature/user-auth vs main
2. Finde 12 geänderte Dateien
3. Identifiziere 3 potentielle Issues
4. Nach False-Positive Filter: 1 Finding

## Security Report: feature/user-auth

### Finding 1: SQL Injection in User Search

**Location:** `src/api/users.py:45`
**Severity:** CRITICAL
**Category:** Injection (A03:2021)
**Confidence:** 9/10

**Description:**
User input wird direkt in SQL Query interpoliert ohne Parameterisierung.

**Vulnerable Code:**
```python
query = f"SELECT * FROM users WHERE name LIKE '%{search_term}%'"
```

**Exploit Scenario:**
Angreifer kann `'; DROP TABLE users; --` als search_term senden.

**Recommendation:**
Parameterisierte Queries verwenden.

**Fixed Code:**
```python
query = "SELECT * FROM users WHERE name LIKE ?"
cursor.execute(query, (f"%{search_term}%",))
```
```

---

## Related

- OWASP Top 10
- CWE Database
- `.claude/commands/security-review.md` - Der Command
