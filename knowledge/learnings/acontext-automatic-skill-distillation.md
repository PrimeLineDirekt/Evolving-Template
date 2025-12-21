# Automatic Skill Distillation Pattern

**Quelle**: Acontext (github.com/memodb-io/Acontext)
**Analysiert**: 2025-12-12
**Relevanz**: Hoch - Adaptiert für Evolving

## Kontext

Acontext ist eine Context Data Platform für Cloud-Native AI Agents. Das System beobachtet Agent-Tasks automatisch und extrahiert wiederverwendbare "Skills" (SOPs - Standard Operating Procedures).

## Das Pattern

### Kernkonzept

```
Task abgeschlossen
       ↓
Complexity Score berechnen
       ↓
Score >= Threshold?
   ├── Nein → Keine Extraktion
   └── Ja → Skill/SOP extrahieren
              ↓
         Im Repository speichern
              ↓
         Bei neuen Tasks retrieven
```

### Complexity Scoring (Original)

| Kriterium | Punkte |
|-----------|--------|
| Falsche Tool-Parameter | 1-2 |
| Strategie-Retries | 1-2 |
| User Feedback zur Korrektur | 1-2 |
| User Preferences beachtet | 1-2 |

**Threshold**: Score < 2 = einfache Aufgabe, keine Extraktion nötig.

### 4 Background Agents

1. **Task Agent**: Beobachtet Konversationen, trackt Status
2. **Task SOP Agent**: Extrahiert SOPs aus komplexen Tasks
3. **Space Construct Agent**: Strukturiert & speichert in DB
4. **Space Search Agent**: Retrieval für neue Tasks

## Adaption für Evolving

### Constraint: Subscription statt API

Evolving läuft über Claude Code Subscription - keine Background Workers mit LLM-Calls möglich.

### Lösung: In-Session Learning Prompt

Statt Background Agent → Prompt am Ende komplexer Sessions via `/whats-next`:

```
Complexity Score >= 3?
   └── Ja → "Soll ich ein Learning/Pattern extrahieren?"
```

### Evolving Complexity Score

| Indikator | Punkte |
|-----------|--------|
| Mehrere Retries/Korrekturen | +2 |
| User-Feedback zur Korrektur | +2 |
| Neuer Ansatz entwickelt | +2 |
| Multi-Step Problemlösung (5+) | +1 |
| Externe Recherche nötig | +1 |

**Threshold**: Score < 3 = Standard-Session, keine Extraktion.

## Key Insights

1. **Nicht jede Session verdient ein Learning** - Complexity Scoring filtert Noise
2. **Automatisierung ohne API** - Prompts in Commands statt Background Workers
3. **User-in-the-Loop** - Extraktion mit Bestätigung, nicht vollautomatisch
4. **Strukturierte Speicherung** - Learnings/Patterns mit konsistentem Template

## Implementierung in Evolving

**Umgesetzt in**: `/whats-next` Command (Schritt 5: Learning-Extraktion)

**Speicherorte**:
- `knowledge/learnings/{topic}.md` - Projekt-spezifische Erkenntnisse
- `knowledge/patterns/{topic}.md` - Wiederverwendbare Muster

## Was NICHT übernommen wurde

| Acontext Feature | Grund für Skip |
|------------------|----------------|
| Background Workers | Braucht API, nicht Subscription-kompatibel |
| Vector DB (Space) | Over-Engineering, Grep reicht |
| Automatische Extraktion | User-Kontrolle wichtiger |
| PostgreSQL/Redis/RabbitMQ | Zu komplex für lokales System |

## Zukünftige Evolution

Falls Evolving später Cloud-basiert wird:
1. FastAPI Backend für Session Persistence
2. Vector DB (ChromaDB) für semantische Suche
3. Background Learning Worker mit Complexity Scoring

Aber: Erst wenn der Mehrwert klar ist. Aktuell funktioniert die lokale Lösung.

---

**Related**:
- [12-Factor Agents](12-factor-agents-framework.md)
- [Context Window Ownership Pattern](../patterns/context-window-ownership-pattern.md)
- [/whats-next Command](../../.claude/commands/whats-next.md)
