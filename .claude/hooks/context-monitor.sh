#!/bin/bash
# Context Monitor v2 - StatusLine with Context Budget Awareness
#
# Format: 145K 72% | Evolving | Opus | main *3 | ✓ Last → Current
# Colors: Green (<60%) | Yellow (60-79%) | Red (≥80%)
# Writes context % to /tmp for hooks

input=$(cat)

project_dir="${CLAUDE_PROJECT_DIR:-$(pwd)}"
cwd=$(echo "$input" | jq -r '.workspace.current_dir // ""' 2>/dev/null)
[[ -z "$cwd" || "$cwd" == "null" ]] && cwd="$project_dir"
dir=$(basename "$cwd")

# ─────────────────────────────────────────────────────────────────
# MODEL - Shorten display name
# ─────────────────────────────────────────────────────────────────
model=$(echo "$input" | jq -r '.model.display_name // "Claude"')
if [[ "$model" =~ Opus ]]; then
  m="Opus"
elif [[ "$model" =~ Sonnet ]]; then
  m="Sonnet"
elif [[ "$model" =~ Haiku ]]; then
  m="Haiku"
else
  m="${model%% *}"
fi

# ─────────────────────────────────────────────────────────────────
# CONTEXT % - Token usage with color coding
# ─────────────────────────────────────────────────────────────────
input_tokens=$(echo "$input" | jq -r '.context_window.current_usage.input_tokens // 0' 2>/dev/null)
cache_read=$(echo "$input" | jq -r '.context_window.current_usage.cache_read_input_tokens // 0' 2>/dev/null)
cache_creation=$(echo "$input" | jq -r '.context_window.current_usage.cache_creation_input_tokens // 0' 2>/dev/null)

# Fallback to old field names if new ones are empty
[[ "$input_tokens" == "0" || "$input_tokens" == "null" ]] && \
  input_tokens=$(echo "$input" | jq -r '.context_window.total_input_tokens // 0' 2>/dev/null)

# Dynamic system overhead based on project structure
# Base: Claude Code system prompt (~25K) + Tool definitions (~10K)
base_overhead=35000

# CLAUDE.md size (chars / 4 ≈ tokens)
claude_md="$project_dir/CLAUDE.md"
if [[ -f "$claude_md" ]]; then
  claude_md_chars=$(wc -c < "$claude_md" 2>/dev/null | tr -d ' ')
  claude_md_tokens=$((claude_md_chars / 4))
else
  claude_md_tokens=0
fi

# Rules overhead: count active rules × ~800 tokens avg
rules_dir="$project_dir/.claude/rules"
if [[ -d "$rules_dir" ]]; then
  rules_count=$(find "$rules_dir" -name "*.md" -type f 2>/dev/null | wc -l | tr -d ' ')
  rules_tokens=$((rules_count * 800))
else
  rules_tokens=0
fi

# Total overhead (capped at 100K to prevent runaway)
system_overhead=$((base_overhead + claude_md_tokens + rules_tokens))
[[ "$system_overhead" -gt 100000 ]] && system_overhead=100000

total_tokens=$((input_tokens + cache_read + cache_creation + system_overhead))
context_size=$(echo "$input" | jq -r '.context_window.context_window_size // 200000' 2>/dev/null)

# Fallback if context_size is empty or invalid
[[ -z "$context_size" || "$context_size" == "null" || "$context_size" -lt 1 ]] && context_size=200000

# Calculate percentage
context_pct=$((total_tokens * 100 / context_size))
[[ "$context_pct" -gt 100 ]] && context_pct=100
[[ "$context_pct" -lt 0 ]] && context_pct=0

# Write for hooks (per-session to avoid conflicts)
session_id="${CLAUDE_SESSION_ID:-$PPID}"
echo "$context_pct" > "/tmp/claude-context-pct-${session_id}.txt"

# Format as K
if [[ "$total_tokens" -gt 1000 ]]; then
  token_display=$(awk "BEGIN {printf \"%.0fK\", $total_tokens/1000}")
else
  token_display="${total_tokens}"
fi

# Color based on threshold
if [[ "$context_pct" -ge 80 ]]; then
  # CRITICAL - Red with warning
  ctx_display="\033[31m⚠ ${token_display} ${context_pct}%\033[0m"
elif [[ "$context_pct" -ge 60 ]]; then
  # WARNING - Yellow
  ctx_display="\033[33m${token_display} ${context_pct}%\033[0m"
else
  # NORMAL - Green
  ctx_display="\033[32m${token_display} ${context_pct}%\033[0m"
fi

# ─────────────────────────────────────────────────────────────────
# GIT - Branch + status indicator
# ─────────────────────────────────────────────────────────────────
git_info=""
if git -C "$cwd" rev-parse --git-dir &>/dev/null 2>&1; then
  branch=$(git -C "$cwd" --no-optional-locks branch --show-current 2>/dev/null)
  [[ -z "$branch" ]] && branch="detached"
  [[ ${#branch} -gt 12 ]] && branch="${branch:0:10}.."

  # Count changes
  staged=$(git -C "$cwd" --no-optional-locks diff --cached --name-only 2>/dev/null | wc -l | tr -d ' ')
  unstaged=$(git -C "$cwd" --no-optional-locks diff --name-only 2>/dev/null | wc -l | tr -d ' ')
  added=$(git -C "$cwd" --no-optional-locks ls-files --others --exclude-standard 2>/dev/null | wc -l | tr -d ' ')

  total_changes=$((staged + unstaged + added))

  if [[ "$total_changes" -gt 0 ]]; then
    git_info="$branch \033[33m*$total_changes\033[0m"
  else
    git_info="\033[32m$branch ✓\033[0m"
  fi
fi

# ─────────────────────────────────────────────────────────────────
# LEDGER - Last done + Current focus (Evolving format)
# ─────────────────────────────────────────────────────────────────
ledger="$project_dir/_ledgers/CURRENT.md"
continuity=""

if [[ -f "$ledger" ]]; then
  # Get current focus (Now: or [→])
  now_focus=$(grep -E '^\s*-\s*Now:|\[→\]' "$ledger" 2>/dev/null | head -1 | \
    sed 's/^[[:space:]]*-[[:space:]]*Now:[[:space:]]*//' | \
    sed 's/^[[:space:]]*-[[:space:]]*\[→\][[:space:]]*//')

  # Truncate
  [[ ${#now_focus} -gt 30 ]] && now_focus="${now_focus:0:28}.."

  [[ -n "$now_focus" ]] && continuity="→ $now_focus"
fi

# ─────────────────────────────────────────────────────────────────
# OUTPUT - Build final status line
# ─────────────────────────────────────────────────────────────────
output="$ctx_display | \033[38;5;6m$dir\033[0m | $m"
[[ -n "$git_info" ]] && output="$output | $git_info"
[[ -n "$continuity" ]] && output="$output | $continuity"

echo -e "$output"
