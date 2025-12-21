#!/bin/bash
#
# Auto Cross-Reference Hook
# Reminds Claude to synchronize Master Documents after changes
#
# Trigger: PostToolUse (Write|Edit)
# Purpose: Ensures consistency across 4 Master Documents
#

set -euo pipefail

# Read stdin (hook input JSON)
input=$(cat)

# Parse tool_input for file_path
file_path=$(echo "$input" | jq -r '.tool_input.file_path // empty')

# Master Documents (4 documents that must stay in sync)
MASTER_DOCS=(
  "README.md"
  ".claude/CONTEXT.md"
  "knowledge/index.md"
  "START.md"
)

# Check if edited file is a Master Document
is_master=false
for doc in "${MASTER_DOCS[@]}"; do
  if [[ "$file_path" == *"$doc" ]]; then
    is_master=true
    break
  fi
done

# Output reminder if Master Document was changed
if [ "$is_master" = true ]; then
  cat << 'EOF'
{
  "hookSpecificOutput": {
    "hookEventName": "PostToolUse",
    "additionalContext": "⚠️ CROSS-REFERENCE SYNCHRONIZATION RULE:\n\nMaster Document geändert. Prüfe ob diese 4 Dokumente synchron sind:\n1. README.md\n2. .claude/CONTEXT.md\n3. knowledge/index.md\n4. START.md\n\nAktualisiere alle relevanten Stats, Counts, Strukturen."
  }
}
EOF
fi

exit 0
