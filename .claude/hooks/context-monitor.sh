#!/bin/bash
# Context Monitor - Statusline with Cost & Token Usage Display
# SIMPLIFIED: Just use the API cost data, don't parse transcript
#
# Display Format: Evolving 🟢 $0.0234 | API Data | 45.3s
#                          │   │                  └─ Session Duration
#                          │   └─ Real API Cost in USD
#                          └─ Status based on cost
#
# NOTE: Token counting from JSONL transcript is extremely complex:
# - Multiple agent transcripts exist
# - Cache tokens counted differently
# - No single source of truth for session total
#
# Solution: Display cost (accurate from API) + duration instead

# Read JSON input from stdin
json=$(cat)

# Extract metrics using jq (fallback to grep/sed if jq not available)
if command -v jq &> /dev/null; then
  cost=$(echo "$json" | jq -r '.cost.total_cost_usd // 0')
  duration=$(echo "$json" | jq -r '.cost.total_duration_ms // 0')
  model=$(echo "$json" | jq -r '.model.display_name // "sonnet-4.5"')
else
  # Fallback: basic parsing without jq
  cost=$(echo "$json" | grep -o '"total_cost_usd":[^,}]*' | cut -d: -f2 | tr -d ' ' || echo "0")
  duration=$(echo "$json" | grep -o '"total_duration_ms":[^,}]*' | cut -d: -f2 | tr -d ' ' || echo "0")
  model="sonnet-4.5"
fi

# Color coding based on cost
cost_float=$(awk "BEGIN {print $cost}")
if awk "BEGIN {exit !($cost_float >= 1.0)}"; then
  STATUS="🔴"  # High cost (>$1)
elif awk "BEGIN {exit !($cost_float >= 0.50)}"; then
  STATUS="🟠"  # Medium cost ($0.50-$1)
elif awk "BEGIN {exit !($cost_float >= 0.10)}"; then
  STATUS="🟡"  # Low cost ($0.10-$0.50)
else
  STATUS="🟢"  # Minimal cost (<$0.10)
fi

# Format cost
cost_display=$(awk "BEGIN {printf \"%.4f\", $cost}" 2>/dev/null || echo "$cost")

# Convert duration to seconds if > 1000ms
if [ "${duration%.*}" -gt 1000 ] 2>/dev/null; then
  duration_sec=$(awk "BEGIN {printf \"%.1f\", $duration/1000}")
  duration_display="${duration_sec}s"
else
  duration_display="${duration}ms"
fi

# Format model name (shorten if needed)
model_short=$(echo "$model" | sed 's/claude-//' | sed 's/-202[0-9].*//')

# Output statusline: Cost + Model + Duration (no token count - too complex/unreliable)
echo "Evolving ${STATUS} \$${cost_display} | ${model_short} | ${duration_display}"
