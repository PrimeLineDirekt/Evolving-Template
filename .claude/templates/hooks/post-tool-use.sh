#!/bin/bash
# ---
# template_version: "1.0"
# template_type: hook
# template_name: "Post-Tool-Use Hook"
# description: "Event-driven automation after tool usage"
# use_cases: [auto-cross-reference, index-update, logging]
# complexity: medium
# created: 2024-11-26
# ---

# Post-Tool-Use Hook Template
# Triggered after Claude uses a tool (Write, Edit, Read, etc.)

# CRITICAL: Hook must ALWAYS exit 0 to avoid blocking Claude
trap 'exit 0' ERR

# Read JSON input from stdin
input=$(cat)

# Parse tool information
tool=$(echo "$input" | jq -r '.tool // empty')
arguments=$(echo "$input" | jq -r '.arguments // empty')

# Validate input
[[ -z "$tool" ]] && exit 0

# ============================================
# CONFIGURATION
# ============================================

# Define which tools to process
MONITORED_TOOLS=("Write" "Edit")

# Define which paths to monitor
MONITORED_PATHS=(
  "ideas/"
  "knowledge/"
  "{PATH_PATTERN_1}"
  "{PATH_PATTERN_2}"
)

# Log file location (optional)
LOG_FILE=".claude/hooks/logs/post-tool-use.log"

# Enable debug logging (set to 1 for debugging)
DEBUG=0

# ============================================
# HELPER FUNCTIONS
# ============================================

# Log debug messages
debug_log() {
  if [[ $DEBUG -eq 1 ]]; then
    echo "[$(date +%Y-%m-%d\ %H:%M:%S)] DEBUG: $*" >> "$LOG_FILE"
  fi
}

# Log info messages
info_log() {
  echo "[$(date +%Y-%m-%d\ %H:%M:%S)] INFO: $*" >> "$LOG_FILE"
}

# Check if tool should be processed
should_process_tool() {
  local tool="$1"
  for monitored in "${MONITORED_TOOLS[@]}"; do
    [[ "$tool" == "$monitored" ]] && return 0
  done
  return 1
}

# Check if path should be processed
should_process_path() {
  local path="$1"
  for pattern in "${MONITORED_PATHS[@]}"; do
    [[ "$path" =~ $pattern ]] && return 0
  done
  return 1
}

# ============================================
# PROCESSING FUNCTIONS
# ============================================

# Process Write tool events
process_write() {
  local file_path="$1"
  local content="$2"

  debug_log "Processing Write event for: $file_path"

  # Example: Auto-cross-reference ideas
  if [[ "$file_path" =~ ideas/ ]]; then
    cross_reference_idea "$file_path"
  fi

  # Example: Update index
  if [[ "$file_path" =~ knowledge/ ]]; then
    update_knowledge_index "$file_path"
  fi

  # {CUSTOM_WRITE_LOGIC}

  info_log "Write processed: $file_path"
}

# Process Edit tool events
process_edit() {
  local file_path="$1"
  local old_string="$2"
  local new_string="$3"

  debug_log "Processing Edit event for: $file_path"

  # Example: Track modifications
  log_modification "$file_path" "$old_string" "$new_string"

  # {CUSTOM_EDIT_LOGIC}

  info_log "Edit processed: $file_path"
}

# ============================================
# AUTOMATION LOGIC
# ============================================

# Auto-cross-reference ideas
cross_reference_idea() {
  local idea_file="$1"
  local idea_id=$(basename "$idea_file" .md)

  debug_log "Cross-referencing idea: $idea_id"

  # {CROSS_REFERENCE_LOGIC}
  # Example:
  # 1. Extract tags/category from idea
  # 2. Find related ideas with similar tags
  # 3. Add bidirectional references

  # This is a placeholder - implement your logic
  # related=$(grep -l "similar_tag" ideas/**/*.md)
  # for rel in $related; do
  #   echo "- Related: $idea_id" >> "$rel"
  # done
}

# Update knowledge index
update_knowledge_index() {
  local knowledge_file="$1"

  debug_log "Updating knowledge index for: $knowledge_file"

  # {INDEX_UPDATE_LOGIC}
  # Example:
  # 1. Read knowledge/index.md
  # 2. Add new entry under appropriate category
  # 3. Update stats

  # This is a placeholder - implement your logic
}

# Log file modification
log_modification() {
  local file_path="$1"
  local old_string="$2"
  local new_string="$3"

  local mod_log=".claude/hooks/logs/modifications.log"
  echo "[$(date +%Y-%m-%d\ %H:%M:%S)] $file_path: '$old_string' → '$new_string'" >> "$mod_log"
}

# ============================================
# MAIN PROCESSING LOGIC
# ============================================

main() {
  debug_log "Hook triggered: tool=$tool"

  # Check if tool should be processed
  if ! should_process_tool "$tool"; then
    debug_log "Tool $tool not monitored, skipping"
    exit 0
  fi

  # Parse tool-specific arguments
  case "$tool" in
    "Write")
      file_path=$(echo "$arguments" | jq -r '.file_path // empty')
      content=$(echo "$arguments" | jq -r '.content // empty')

      # Validate
      [[ -z "$file_path" ]] && exit 0

      # Check if path should be processed
      if ! should_process_path "$file_path"; then
        debug_log "Path $file_path not monitored, skipping"
        exit 0
      fi

      # Process in background to avoid blocking
      (process_write "$file_path" "$content" &)
      ;;

    "Edit")
      file_path=$(echo "$arguments" | jq -r '.file_path // empty')
      old_string=$(echo "$arguments" | jq -r '.old_string // empty')
      new_string=$(echo "$arguments" | jq -r '.new_string // empty')

      # Validate
      [[ -z "$file_path" ]] && exit 0

      # Check if path should be processed
      if ! should_process_path "$file_path"; then
        debug_log "Path $file_path not monitored, skipping"
        exit 0
      fi

      # Process in background
      (process_edit "$file_path" "$old_string" "$new_string" &)
      ;;

    *)
      debug_log "Unhandled tool: $tool"
      ;;
  esac
}

# ============================================
# EXECUTION
# ============================================

# Ensure log directory exists
mkdir -p "$(dirname "$LOG_FILE")"

# Run main logic
main

# CRITICAL: Always exit 0
exit 0
