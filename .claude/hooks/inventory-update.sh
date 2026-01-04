#!/bin/bash
# Inventory Update Hook
# Trigger: Nach Write/Edit in .claude/ oder knowledge/rules/
# Aktion: component-counts.json + ANALYSIS.md aktualisieren (debounced, sektions-spezifisch)

input=$(cat)
project_dir="${CLAUDE_PROJECT_DIR:-$(pwd)}"

# Prüfe ob die geänderte Datei relevant ist
file_path=$(echo "$input" | jq -r '.tool_input.file_path // ""' 2>/dev/null)

# Bestimme welche Sektion aktualisiert werden muss
section=""
if [[ "$file_path" == *".claude/commands/"* ]]; then
    section="commands"
elif [[ "$file_path" == *".claude/agents/"* ]]; then
    section="agents"
elif [[ "$file_path" == *".claude/skills/"* ]]; then
    section="skills"
elif [[ "$file_path" == *".claude/hooks/"* ]]; then
    section="hooks"
elif [[ "$file_path" == *".claude/rules/"* ]] || [[ "$file_path" == *"knowledge/rules/"* ]]; then
    section="rules"
fi

# Nur bei relevanten Änderungen triggern
if [[ -n "$section" ]] || [[ "$file_path" == *".claude/"* ]]; then
    # Debounce: Nur alle 2 Minuten updaten (pro Sektion)
    lock_file="/tmp/inventory-update-${section:-general}"

    if [[ -f "$lock_file" ]]; then
        last_update=$(cat "$lock_file")
        now=$(date +%s)
        diff=$((now - last_update))

        # Skip wenn letztes Update < 2 Minuten her
        if [[ $diff -lt 120 ]]; then
            exit 0
        fi
    fi

    # Lock setzen
    date +%s > "$lock_file"

    # Update im Hintergrund (non-blocking)
    (
        cd "$project_dir"

        # Counts immer updaten
        python3 scripts/update-system-inventory.py > /dev/null 2>&1

        # ANALYSIS.md Sektion updaten (wenn spezifische Sektion erkannt)
        if [[ -n "$section" ]]; then
            python3 scripts/update-system-inventory.py --section "$section" > /dev/null 2>&1
        fi
    ) &
fi

exit 0
