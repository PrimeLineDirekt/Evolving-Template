# CC Workflow Studio Reference

**Typ**: VSCode Extension
**Status**: Tool Reference (nicht extrahiert)
**Checked**: 2025-12-29

---

## Was ist das?

VSCode Extension für visuelles Workflow-Design für Claude Code.

## Key Features

- **Visual Drag-and-Drop Canvas** - React Flow basiert
- **Node Types**: Prompt Templates, Sub-Agent Tasks, Skills, MCP Tools, Conditionals
- **One-Click Export** → `.claude/agents/` + `.claude/commands/`
- **AI-Assisted Refinement** - Natural Language Workflow-Verbesserung
- **Slack Integration** - Workflow-Sharing

## Tech Stack

- TypeScript, React, React Flow
- Vite, Biome
- VSCode Extension API

## Warum nicht extrahiert?

- Ist eine Extension, kein Agent/Command/Skill
- Output-Format ist das was wir bereits haben (.claude/*)
- Nutzen: Für User die visuelles Design bevorzugen

## Wann relevant?

- Wenn komplexe Multi-Step Workflows visuell designed werden sollen
- Für User die nicht direkt Markdown schreiben wollen
- Für Team-Collaboration (Slack Sharing)

## Installation

```bash
# VSCode Extension Marketplace
# oder
git clone https://github.com/breaking-brake/cc-wf-studio
cd cc-wf-studio
npm install
npm run build
```
