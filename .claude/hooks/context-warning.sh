#!/bin/bash
# Context Warning Hook - PreToolUse
# Warnt bei hohem Context % bevor Auto-Compact zuschlägt
#
# WICHTIG: Nutzt systemMessage im JSON (nicht stderr!)
# stderr wird nur in verbose mode (Ctrl+O) angezeigt

session_id="${CLAUDE_SESSION_ID:-$PPID}"
pct_file="/tmp/claude-context-pct-${session_id}.txt"

# Lese Input für Tool-Name Check
input=$(cat)
tool_name=$(echo "$input" | jq -r '.tool_name // ""' 2>/dev/null)
skill_name=$(echo "$input" | jq -r '.tool_input.skill // ""' 2>/dev/null)

# Lese Context % (geschrieben von context-monitor.sh / statusline.sh)
if [[ -f "$pct_file" ]]; then
  pct=$(cat "$pct_file" 2>/dev/null)

  if [[ "$pct" -ge 90 ]]; then
    # Erlaubte Tools für Handoff: Read, Write, Bash, Skill, Glob, Grep, TodoWrite
    allowed_tools="Read|Write|Bash|Skill|Glob|Grep|TodoWrite"
    if [[ "$tool_name" =~ ^($allowed_tools)$ ]]; then
      # Warnung aber erlauben (für Handoff)
      echo "{\"systemMessage\": \"🛑 Context bei ${pct}% - NUR Handoff-Aktionen erlaubt! Führe /whats-next aus!\", \"continue\": true}"
      exit 0
    fi
    # Schwere Tools blockieren: Task, Edit, WebSearch, WebFetch, etc.
    echo "{\"systemMessage\": \"🛑 BLOCKED: Context bei ${pct}%. Tool '$tool_name' blockiert. Führe /whats-next aus, dann /clear!\", \"continue\": false}"
    exit 0
  elif [[ "$pct" -ge 80 ]]; then
    # KRITISCH: Dringende Warnung
    echo "{\"systemMessage\": \"⚠️ KRITISCH: Context bei ${pct}% - Führe JETZT /whats-next aus!\", \"continue\": true}"
    exit 0
  elif [[ "$pct" -ge 70 ]]; then
    # WARNING: Handoff erwägen
    echo "{\"systemMessage\": \"⚠️ Context bei ${pct}% - Handoff mit /whats-next erwägen\", \"continue\": true}"
    exit 0
  fi
fi

# Kein Warning nötig
echo '{}'
