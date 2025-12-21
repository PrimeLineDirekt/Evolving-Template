# Evolving Knowledge Hub

Ein lokales Informations-Dashboard das KI-Neulinge in die Welt der künstlichen Intelligenz und das Evolving System einführt.

## Features

### Drei Hauptbereiche

1. **Schnellstart** - In 3 Schritten loslegen
   - Onboarding starten
   - Erste Idee erfassen
   - System erkunden

2. **KI-Grundlagen** - Alles was du über KI wissen musst
   - Was sind Prompts?
   - Effektive Prompts schreiben
   - Was sind Agents?
   - Was sind Skills?
   - Was sind LLMs?
   - Was sind Tools?

3. **System-Guide** - Das Evolving System verstehen
   - Was ist Evolving?
   - Erste Schritte
   - Commands (Befehle)
   - Agents im System
   - Skills im System
   - System erweitern
   - Anpassung & Präferenzen
   - Inbox-Workflow

### Design

- **Light Theme** - Einladendes, freundliches Design
- **Progressive Content** - Kurze Übersicht + "Mehr erfahren" für Details
- **Responsive** - Funktioniert auf Desktop, Tablet und Mobile
- **Animationen** - Sanfte Übergänge und Hover-Effekte

## Quick Start

```bash
# Dependencies installieren
npm install

# Development Server starten
npm run dev

# Browser öffnen
open http://localhost:3000
```

## Projekt-Struktur

```
dashboard/
├── src/
│   ├── app/
│   │   ├── page.tsx          # Hauptseite (Knowledge Hub)
│   │   ├── layout.tsx        # Root Layout
│   │   └── globals.css       # Globale Styles
│   │
│   ├── components/
│   │   └── KnowledgeHub/
│   │       ├── InfoCard.tsx      # Info-Kachel Komponente
│   │       ├── DetailModal.tsx   # Detail-Popup
│   │       ├── SectionGrid.tsx   # Kachel-Grid
│   │       ├── QuickStart.tsx    # Schnellstart-Bereich
│   │       └── index.ts
│   │
│   └── data/
│       └── knowledge-content.ts  # Alle Inhalte (zentral)
│
├── package.json
└── README.md
```

## Tech Stack

- **Next.js 16** - React Framework
- **React 19** - UI Library
- **TypeScript** - Type Safety
- **Tailwind CSS 4** - Styling

## Content erweitern

Alle Inhalte sind in `src/data/knowledge-content.ts` definiert. Du kannst:

1. **Neue Karten hinzufügen** - Einfach ein neues `InfoCard` Objekt zum Array
2. **Inhalte ändern** - Texte, Beispiele, Tipps anpassen
3. **Neue Sektionen** - Neue `Section` mit eigenen Karten

```typescript
// Beispiel: Neue Karte hinzufügen
{
  id: 'new-topic',
  title: 'Neues Thema',
  icon: '📌',
  shortDescription: 'Kurze Beschreibung',
  fullContent: {
    introduction: 'Ausführliche Einleitung...',
    keyPoints: ['Punkt 1', 'Punkt 2'],
    examples: [...],
    tips: [...]
  }
}
```

## Lizenz

Private - Für persönlichen Gebrauch
