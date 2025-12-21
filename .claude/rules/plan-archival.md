# Plan-Archivierung

Regeln für das Archivieren abgeschlossener Implementierungspläne.

## Trigger

Nach Implementation ALLER Features aus einem Plan in `knowledge/plans/`.

## Workflow

1. **Status setzen** in der Plan-Datei:
   ```markdown
   ## Status: ARCHIVED
   **Archiviert**: YYYY-MM-DD
   ```

2. **VERSCHIEBEN** (nicht kopieren!):
   ```bash
   mv knowledge/plans/plan-name.md knowledge/plans/archive/
   ```

3. **Index aktualisieren** in `knowledge/plans/index.md`:
   - Aus "Aktive Pläne" entfernen
   - In "Archivierte Pläne" eintragen

## Wichtig

- **mv, NICHT cp** - Plan darf nur an einer Stelle existieren
- Archivierungsdatum immer dokumentieren
- Index muss konsistent bleiben
