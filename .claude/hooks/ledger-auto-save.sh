#!/bin/bash
#
# Ledger Auto-Save Hook
# Updates the current ledger with session activity
#
# Trigger: Stop (runs at session end)
# Purpose: Ensure ledger is always up-to-date before session ends
#
# Based on: Continuous-Claude "Clear, don't compact" philosophy
#

set -euo pipefail

# Read stdin (hook input JSON)
input=$(cat)

# Parse session metadata
if command -v jq &> /dev/null; then
    session_id=$(echo "$input" | jq -r '.session_id // "unknown"')
    cwd=$(echo "$input" | jq -r '.cwd // "."')
else
    session_id="unknown"
    cwd="."
fi

# Paths
ledger_dir="$cwd/_ledgers"
current_ledger="$ledger_dir/CURRENT.md"
timestamp=$(date +"%Y-%m-%d %H:%M")
date_short=$(date +%Y-%m-%d)

# Skip if no ledger directory
if [ ! -d "$ledger_dir" ]; then
    exit 0
fi

# Skip if no current ledger
if [ ! -f "$current_ledger" ]; then
    exit 0
fi

# =============================================================================
# GATHER SESSION ACTIVITY
# =============================================================================

# Get commits from this session (last 6 hours)
commits=""
if git -C "$cwd" rev-parse --git-dir &>/dev/null 2>&1; then
    commits=$(git -C "$cwd" log --oneline --since="6 hours ago" 2>/dev/null | head -5) || true
fi

# Get modified files
modified_files=""
if git -C "$cwd" rev-parse --git-dir &>/dev/null 2>&1; then
    modified_files=$(git -C "$cwd" status --short 2>/dev/null | head -10) || true
fi

# Get active project from memory
active_project="unknown"
if [ -f "$cwd/_memory/index.json" ] && command -v jq &> /dev/null; then
    active_project=$(jq -r '.active_context.project // "unknown"' "$cwd/_memory/index.json" 2>/dev/null) || true
fi

# =============================================================================
# UPDATE LEDGER
# =============================================================================

# Only update if there's activity to report
if [ -n "$commits" ] || [ -n "$modified_files" ]; then

    # Create session activity block
    activity_block="
---

## Session Activity ($timestamp)

**Session ID**: \`${session_id:0:8}...\`
**Projekt**: $active_project
"

    if [ -n "$commits" ]; then
        activity_block+="
### Commits
\`\`\`
$commits
\`\`\`
"
    fi

    if [ -n "$modified_files" ]; then
        activity_block+="
### Modified Files
\`\`\`
$modified_files
\`\`\`
"
    fi

    # Append to ledger (before Quick Resume section)
    if grep -q "## Quick Resume" "$current_ledger"; then
        # Insert before Quick Resume
        sed -i.bak "/## Quick Resume/i\\
$activity_block
" "$current_ledger" 2>/dev/null || true
        rm -f "$current_ledger.bak"
    else
        # Append to end
        echo "$activity_block" >> "$current_ledger"
    fi
fi

# =============================================================================
# OUTPUT
# =============================================================================

# Return valid JSON for Stop hook
cat << EOF
{
  "continue": true,
  "message": "Ledger updated with session activity"
}
EOF

exit 0
