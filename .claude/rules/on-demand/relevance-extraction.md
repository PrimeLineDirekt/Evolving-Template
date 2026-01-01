# Relevance Extraction Rule

**Prio**: HOCH
**Trigger**: Bei /analyze-repo, Ext-Repo-Analyse, Knowledge-Integration

---

## Kernprinzip

```
Für jede Komponente aus ext. Repo:

1. DIREKT NUTZBAR?
   → Ja: Ext nach external/{repo}/
   → Nein: Weiter zu 2.

2. INTERESSANTES FRAMEWORK?
   → Ja: Tpl erstellen (Thema abstrahieren)
   → Nein: Skip + kurze Notiz warum
```

---

## Entscheidungsbaum

```
Komponente gefunden
       │
       ▼
┌──────────────────┐
│ Für UNS nutzbar? │
└────────┬─────────┘
    Ja   │   Nein
    ▼    │    ▼
  EXT    │  ┌──────────────────┐
         │  │ Framework        │
         │  │ interessant?     │
         │  └────────┬─────────┘
         │      Ja   │   Nein
         │      ▼    │    ▼
         │    TPL    │  SKIP
         │           │
         └───────────┘
```

---

## Beispiele

### Direkt Nutzbar → EXT

```
Agent: "context-manager-agent"
├── Use-Case: Context Management → Relevant für uns
├── Framework: Solid Patterns
└── Aktion: Ext nach .claude/agents/external/{repo}/
```

### Interessantes Framework → TPL

```
Agent: "kubernetes-deployment-validator"
├── Use-Case: K8s-spezifisch → Irrelevant
├── Framework: Validation-Checklist Pattern → INTERESSANT
└── Aktion: Tpl "validation-checklist-agent.md" erstellen
            (K8s-Referenzen durch Platzhalter ersetzen)
```

### Irrelevant → SKIP

```
Agent: "discord-bot-moderator"
├── Use-Case: Discord Moderation → Irrelevant
├── Framework: Standard Bot Pattern → Nichts Neues
└── Aktion: Skip + Notiz "Discord-spezifisch, Standard-Pattern"
```

---

## Template-Abstraktion

Bei Tpl-Erstellung:

1. **Themen-Referenzen entfernen**
   - "kubernetes" → "{domain}"
   - "deployment" → "{task}"

2. **Framework behalten**
   - Struktur
   - Validation-Logik
   - Output-Format

3. **Placeholders einfügen**
   ```
   statt: "Validate K8s deployment YAML"
   schreibe: "Validate {artifact_type} for {quality_criteria}"
   ```

---

## Output-Struktur

```
.claude/*/external/{repo}/
├── {rel-komponenten}.md     # Direkt nutzbar (EXT)
└── _index.json              # Tags + Beschreibungen

.claude/templates/
└── {abstrahierte-tpls}.md   # Aus interessanten Frameworks (TPL)

knowledge/learnings/
└── {repo}-skip-notes.md     # Was geskipped + warum (SKIP)
```

---

## Skip-Notes Format

```markdown
# {Repo} Skip Notes

## Geskippte Komponenten

| Komponente | Grund |
|------------|-------|
| discord-bot | Discord-spezifisch |
| aws-lambda | AWS-spezifisch, kein neues Framework |
| ... | ... |
```

---

## Related

- [no-reference-only.md](no-reference-only.md) - Warum echte Ext nötig
- [token-efficiency.md](token-efficiency.md) - Abkürzungen (A, S, C, H, M...)
- [knowledge-linking.md](knowledge-linking.md) - Ext mit bestehendem Wissen verknüpfen
- [cross-reference-sync.md](cross-reference-sync.md) - Master-Dok nach Ext updaten
