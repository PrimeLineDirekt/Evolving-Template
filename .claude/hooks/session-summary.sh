#!/bin/bash
#
# Session Summary Hook (Enhanced)
# Creates session summary with actual session data
#
# Trigger: Stop
# Purpose: Automatic documentation of work sessions
#
# Erfasst:
# - Git commits der Session
# - Geänderte Dateien
# - Handoff-Referenz (falls erstellt)
# - Projekt-Memory Status
#

set -euo pipefail

# Read stdin (hook input JSON)
input=$(cat)

# Parse session metadata using jq (with fallback)
if command -v jq &> /dev/null; then
    session_id=$(echo "$input" | jq -r '.session_id // "unknown"')
    cwd=$(echo "$input" | jq -r '.cwd // "."')
    stop_reason=$(echo "$input" | jq -r '.stop_hook_active // "user_initiated"')
else
    session_id="unknown"
    cwd="."
    stop_reason="unknown"
fi

# Generate timestamps
timestamp=$(date +%Y-%m-%d-%H%M%S)
date_readable=$(date +"%Y-%m-%d %H:%M:%S")
date_short=$(date +%Y-%m-%d)

# Create sessions directory if it doesn't exist
mkdir -p "$cwd/knowledge/sessions"

# Generate summary file path
summary_file="$cwd/knowledge/sessions/session-$timestamp.md"

# =============================================================================
# GATHER SESSION DATA
# =============================================================================

# Get commits from today (likely this session)
commits_today=""
if git -C "$cwd" rev-parse --git-dir &>/dev/null 2>&1; then
    commits_today=$(git -C "$cwd" log --oneline --since="6 hours ago" 2>/dev/null | head -10) || true
fi

# Get current git status (uncommitted changes)
git_status=""
if git -C "$cwd" rev-parse --git-dir &>/dev/null 2>&1; then
    git_status=$(git -C "$cwd" status --short 2>/dev/null | head -20) || true
fi

# Count changes (ensure single number output)
modified_count=$(echo "$git_status" | grep -c "^ M\|^M " 2>/dev/null || true)
[ -z "$modified_count" ] && modified_count=0
new_count=$(echo "$git_status" | grep -c "^??" 2>/dev/null || true)
[ -z "$new_count" ] && new_count=0
staged_count=$(echo "$git_status" | grep -c "^A \|^M " 2>/dev/null || true)
[ -z "$staged_count" ] && staged_count=0

# Check for handoff from today
handoff_today=""
if [ -d "$cwd/_handoffs" ]; then
    handoff_today=$(ls -1 "$cwd/_handoffs/" 2>/dev/null | grep "^$date_short" | tail -1) || true
fi

# Get active project from memory
active_project="Nicht gesetzt"
if [ -f "$cwd/_memory/index.json" ] && command -v jq &> /dev/null; then
    active_project=$(jq -r '.active_context.project // "Nicht gesetzt"' "$cwd/_memory/index.json" 2>/dev/null) || true
fi

# =============================================================================
# CREATE SUMMARY
# =============================================================================

cat > "$summary_file" << SUMMARY
# Session Summary - $date_short

**Session ID**: \`${session_id:0:8}...\`
**Zeit**: $date_readable
**Projekt**: $active_project

---

## Git Activity

SUMMARY

# Add commits section
if [ -n "$commits_today" ]; then
    echo "### Commits (letzte 6h)" >> "$summary_file"
    echo "\`\`\`" >> "$summary_file"
    echo "$commits_today" >> "$summary_file"
    echo "\`\`\`" >> "$summary_file"
else
    echo "*Keine Commits in dieser Session*" >> "$summary_file"
fi

echo "" >> "$summary_file"

# Add uncommitted changes
if [ -n "$git_status" ]; then
    echo "### Uncommitted Changes" >> "$summary_file"
    echo "" >> "$summary_file"
    echo "| Typ | Anzahl |" >> "$summary_file"
    echo "|-----|--------|" >> "$summary_file"
    echo "| Modified | $modified_count |" >> "$summary_file"
    echo "| New | $new_count |" >> "$summary_file"
    echo "| Staged | $staged_count |" >> "$summary_file"
    echo "" >> "$summary_file"

    if [ "$modified_count" -gt 0 ] || [ "$new_count" -gt 0 ]; then
        echo "<details>" >> "$summary_file"
        echo "<summary>Details anzeigen</summary>" >> "$summary_file"
        echo "" >> "$summary_file"
        echo "\`\`\`" >> "$summary_file"
        echo "$git_status" >> "$summary_file"
        echo "\`\`\`" >> "$summary_file"
        echo "</details>" >> "$summary_file"
    fi
else
    echo "*Working directory clean*" >> "$summary_file"
fi

echo "" >> "$summary_file"
echo "---" >> "$summary_file"
echo "" >> "$summary_file"

# Add handoff reference
echo "## Handoff" >> "$summary_file"
echo "" >> "$summary_file"
if [ -n "$handoff_today" ]; then
    echo "**Erstellt**: [\`$handoff_today\`](_handoffs/$handoff_today)" >> "$summary_file"
else
    echo "*Kein Handoff erstellt. Nutze \`/whats-next\` für detaillierte Übergabe.*" >> "$summary_file"
fi

echo "" >> "$summary_file"
echo "---" >> "$summary_file"
echo "" >> "$summary_file"

# Evaluation marker (for session-evaluation rule)
cat >> "$summary_file" << EVAL_MARKER

---

## Evaluation

**Status**: Pending

*Diese Session wurde noch nicht bewertet. Bei der nächsten Session wird eine Rubric-Evaluation angeboten.*

EVAL_MARKER

# Footer
cat >> "$summary_file" << FOOTER

---

## Quick Resume

Für die nächste Session:
\`\`\`
@START.md - Neue Session
\`\`\`

Oder lies den Handoff falls vorhanden.

---

*Auto-generated by session-summary hook*
FOOTER

# Output valid JSON for Stop hook
cat << EOF
{
  "stopReason": "Session summary: $summary_file"
}
EOF

exit 0
