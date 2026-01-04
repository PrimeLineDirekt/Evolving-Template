#!/bin/bash
# Template Sync Reminder Hook
# Triggers when new generic content is created that might be relevant for template sync

# Read input from stdin
input=$(cat)

# Extract file path from tool input
file_path=$(echo "$input" | jq -r '.tool_input.file_path // .tool_input.path // empty')

# Exit if no file path
if [ -z "$file_path" ]; then
    exit 0
fi

# Paths
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
MANIFEST="$PROJECT_ROOT/config/template-sync-manifest.json"

# Get target path
if [ -n "${EVOLVING_TEMPLATE:-}" ]; then
    TARGET="$EVOLVING_TEMPLATE"
elif [ -f "$MANIFEST" ]; then
    TARGET=$(jq -r '.paths.target // empty' "$MANIFEST")
    if [ -z "$TARGET" ] || [ "$TARGET" = "null" ]; then
        TARGET="$(dirname "$(dirname "$PROJECT_ROOT")")/Evolving-Template"
    fi
else
    TARGET="$(dirname "$(dirname "$PROJECT_ROOT")")/Evolving-Template"
fi

# Patterns that indicate generic content (should be synced)
INCLUDE_PATTERNS=(
    ".claude/agents/"
    ".claude/commands/"
    ".claude/skills/"
    ".claude/blueprints/"
    ".claude/rules/"
    "knowledge/patterns/"
    "knowledge/rules/"
    "knowledge/prompts/"
    "knowledge/references/"
)

# Patterns that are always excluded (personal content)
EXCLUDE_PATTERNS=(
    "_memory/"
    "_handoffs/"
    "_ledgers/"
    "knowledge/personal/"
    "knowledge/projects/"
    "knowledge/external-projects/"
    "knowledge/sessions/"
    "ideas/"
)

# Check if file matches exclude patterns (skip reminder)
for pattern in "${EXCLUDE_PATTERNS[@]}"; do
    if [[ "$file_path" == *"$pattern"* ]]; then
        exit 0
    fi
done

# Check if file matches include patterns (potential sync candidate)
match_found=false
for pattern in "${INCLUDE_PATTERNS[@]}"; do
    if [[ "$file_path" == *"$pattern"* ]]; then
        match_found=true
        break
    fi
done

# Exit if not a sync-relevant file
if [ "$match_found" = false ]; then
    exit 0
fi

# Check if file exists in template
rel_path="${file_path#*Evolving/}"
template_file="$TARGET/$rel_path"

if [ ! -f "$template_file" ]; then
    # New file not in template - show reminder
    filename=$(basename "$file_path")
    dirname=$(dirname "$rel_path")

    cat << EOF
{
  "hookSpecificOutput": {
    "hookEventName": "PostToolUse",
    "additionalContext": "📦 Template Sync: Neue Datei '$filename' in '$dirname' könnte für Evolving-Template relevant sein. Nutze /template-sync wenn bereit."
  }
}
EOF
fi

exit 0
