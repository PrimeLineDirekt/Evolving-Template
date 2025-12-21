#!/bin/bash
# ---
# template_version: "1.0"
# template_type: hook
# template_name: "Stop Hook"
# description: "Session summary generation on conversation end"
# use_cases: [session-summary, conversation-log, cleanup]
# complexity: low
# created: 2024-11-26
# ---

# Stop Hook Template
# Triggered when conversation ends (user closes chat or starts new conversation)

# CRITICAL: Hook must ALWAYS exit 0 to avoid blocking Claude
trap 'exit 0' ERR

# Read session context from stdin (if available)
input=$(cat)

# ============================================
# CONFIGURATION
# ============================================

# Summary output directory
SUMMARY_DIR="{SUMMARY_OUTPUT_PATH}"  # e.g., "knowledge/sessions" or ".sessions"

# Summary filename pattern
SUMMARY_FILENAME="session-$(date +%Y%m%d-%H%M%S).md"

# Summary format
SUMMARY_FORMAT="{markdown|json|text}"  # Choose format

# Include in summary
INCLUDE_TIMESTAMP=true
INCLUDE_TOOLS_USED=true
INCLUDE_FILES_MODIFIED=true
INCLUDE_TOPICS=true

# ============================================
# HELPER FUNCTIONS
# ============================================

# Extract session metadata
extract_metadata() {
  # Parse JSON input if available
  local session_id=$(echo "$input" | jq -r '.session_id // empty' 2>/dev/null)
  local started_at=$(echo "$input" | jq -r '.started_at // empty' 2>/dev/null)

  # Use defaults if not available
  [[ -z "$session_id" ]] && session_id="unknown"
  [[ -z "$started_at" ]] && started_at=$(date -I)

  echo "$session_id|$started_at"
}

# Collect tool usage statistics
collect_tool_stats() {
  # Read tool usage log if exists
  local log_file=".claude/hooks/logs/post-tool-use.log"

  if [[ -f "$log_file" ]]; then
    # Count tools used today
    local today=$(date +%Y-%m-%d)
    grep "$today" "$log_file" | awk '{print $4}' | sort | uniq -c
  fi
}

# Collect files modified
collect_files_modified() {
  local log_file=".claude/hooks/logs/modifications.log"

  if [[ -f "$log_file" ]]; then
    local today=$(date +%Y-%m-%d)
    grep "$today" "$log_file" | awk '{print $3}' | sort -u
  fi
}

# Identify session topics (placeholder)
identify_topics() {
  # Analyze modified files to infer topics
  # This is a simple heuristic - customize for your needs

  local files=$(collect_files_modified)
  local topics=()

  if echo "$files" | grep -q "ideas/"; then
    topics+=("Ideas")
  fi

  if echo "$files" | grep -q "knowledge/"; then
    topics+=("Knowledge")
  fi

  if echo "$files" | grep -q "projects/"; then
    topics+=("Projects")
  fi

  # {CUSTOM_TOPIC_DETECTION}

  # Return topics as comma-separated
  IFS=','; echo "${topics[*]}"
}

# ============================================
# SUMMARY GENERATION
# ============================================

# Generate Markdown summary
generate_markdown_summary() {
  local session_id="$1"
  local started_at="$2"

  cat <<EOF
# Session Summary

**Session ID**: $session_id
**Date**: $(date +%Y-%m-%d)
**Time**: $(date +%H:%M:%S)
**Started**: $started_at

## Overview

{SESSION_DESCRIPTION}

## Activity

### Tools Used
$(if [[ "$INCLUDE_TOOLS_USED" == true ]]; then collect_tool_stats; else echo "Not tracked"; fi)

### Files Modified
$(if [[ "$INCLUDE_FILES_MODIFIED" == true ]]; then collect_files_modified | sed 's/^/- /'; else echo "Not tracked"; fi)

### Topics
$(if [[ "$INCLUDE_TOPICS" == true ]]; then identify_topics | tr ',' '\n' | sed 's/^/- /'; else echo "Not tracked"; fi)

## Key Actions

{PLACEHOLDER_FOR_KEY_ACTIONS}

## Insights

{PLACEHOLDER_FOR_INSIGHTS}

## Next Steps

- [ ] {NEXT_STEP_1}
- [ ] {NEXT_STEP_2}

---

**Generated**: $(date +%Y-%m-%d\ %H:%M:%S)
EOF
}

# Generate JSON summary
generate_json_summary() {
  local session_id="$1"
  local started_at="$2"

  cat <<EOF
{
  "session_id": "$session_id",
  "date": "$(date -I)",
  "timestamp": "$(date +%Y-%m-%d\ %H:%M:%S)",
  "started_at": "$started_at",
  "tools_used": $(collect_tool_stats | jq -R -s -c 'split("\n")[:-1]'),
  "files_modified": $(collect_files_modified | jq -R -s -c 'split("\n")[:-1]'),
  "topics": $(identify_topics | tr ',' '\n' | jq -R -s -c 'split("\n")[:-1]')
}
EOF
}

# Generate text summary
generate_text_summary() {
  local session_id="$1"
  local started_at="$2"

  cat <<EOF
Session Summary - $(date +%Y-%m-%d\ %H:%M:%S)
===============================================

Session ID: $session_id
Started: $started_at

Tools Used:
$(collect_tool_stats)

Files Modified:
$(collect_files_modified)

Topics: $(identify_topics)

---
End of Session
EOF
}

# ============================================
# MAIN LOGIC
# ============================================

main() {
  # Extract metadata
  IFS='|' read -r session_id started_at <<< "$(extract_metadata)"

  # Ensure summary directory exists
  mkdir -p "$SUMMARY_DIR"

  # Generate summary based on format
  local summary_file="$SUMMARY_DIR/$SUMMARY_FILENAME"

  case "$SUMMARY_FORMAT" in
    "markdown")
      generate_markdown_summary "$session_id" "$started_at" > "$summary_file"
      ;;
    "json")
      summary_file="${summary_file%.md}.json"
      generate_json_summary "$session_id" "$started_at" > "$summary_file"
      ;;
    "text")
      summary_file="${summary_file%.md}.txt"
      generate_text_summary "$session_id" "$started_at" > "$summary_file"
      ;;
    *)
      # Default to markdown
      generate_markdown_summary "$session_id" "$started_at" > "$summary_file"
      ;;
  esac

  # Optional: Cleanup old summaries (keep last N)
  # {CLEANUP_LOGIC}

  # Optional: Trigger additional workflows
  # {POST_SESSION_WORKFLOWS}
}

# ============================================
# EXECUTION
# ============================================

# Run main logic
main

# CRITICAL: Always exit 0
exit 0
