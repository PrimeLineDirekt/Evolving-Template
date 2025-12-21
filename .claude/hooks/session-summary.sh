#!/bin/bash
#
# Session Summary Hook
# Creates session summary file on session end
#
# Trigger: Stop
# Purpose: Automatic documentation of work sessions
#

set -euo pipefail

# Read stdin (hook input JSON)
input=$(cat)

# Parse session metadata
session_id=$(echo "$input" | jq -r '.session_id // "unknown"')
cwd=$(echo "$input" | jq -r '.cwd // "."')

# Generate timestamp (YYYY-MM-DD-HHMMSS)
timestamp=$(date +%Y-%m-%d-%H%M%S)

# Create sessions directory if it doesn't exist
mkdir -p "$cwd/knowledge/sessions"

# Generate summary file path
summary_file="$cwd/knowledge/sessions/session-$timestamp.md"

# Output valid JSON for Stop hook (empty object = allow normal stop)
cat << EOF
{}
EOF

# Note: Session summary file path created at: $summary_file
# Claude will see this in logs but won't block on it

exit 0
