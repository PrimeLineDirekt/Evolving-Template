# Hook Templates

Hook templates provide event-driven automation structures for Claude Desktop hooks (PostToolUse, Stop).

## What are Hook Templates?

Hooks are bash scripts triggered by Claude Desktop events. They enable automation like auto-cross-referencing, session summaries, and logging without user intervention.

## When to Use Hook Templates

- Automating cross-references between files
- Creating session summaries
- Logging tool usage
- Triggering workflows based on events
- Background processing tasks

## Available Templates

### 1. Post-Tool-Use Hook (`post-tool-use.sh`)

**Event**: After Claude uses a tool (Write, Edit, etc.)

**Use for**: Automatic cross-referencing, index updates, logging

**Examples**:
- Auto-link ideas when creating knowledge
- Update indexes when adding files
- Log all file modifications

**Key Features**:
- Non-blocking (must exit 0)
- JSON I/O
- Tool filtering
- Error resilience

### 2. Stop Hook (`stop-hook.sh`)

**Event**: When conversation ends (session stop)

**Use for**: Session summaries, cleanup, final processing

**Examples**:
- Generate session summary
- Create conversation log
- Update daily journal
- Cleanup temporary files

**Key Features**:
- Session context access
- File creation
- Summary generation
- Graceful error handling

## Quick Start

### Creating a Post-Tool-Use Hook

```bash
# 1. Copy template
cp .claude/templates/hooks/post-tool-use.sh .claude/hooks/post-tool-use.sh

# 2. Customize logic
# Edit the process_tool_use() function
# Add your automation logic

# 3. Test hook
# Use a tool in Claude and check hook execution
# Debug with logs if needed

# 4. Make executable
chmod +x .claude/hooks/post-tool-use.sh
```

### Creating a Stop Hook

```bash
# 1. Copy template
cp .claude/templates/hooks/stop-hook.sh .claude/hooks/stop.sh

# 2. Define summary logic
# Customize what to include in session summary

# 3. Set output location
# Where to save summaries

# 4. Test hook
# End a conversation and verify summary creation

# 5. Make executable
chmod +x .claude/hooks/stop.sh
```

## Hook Structure

### Post-Tool-Use Hook

```bash
#!/bin/bash

# Read JSON input from stdin
input=$(cat)

# Parse tool name and arguments
tool=$(echo "$input" | jq -r '.tool')
args=$(echo "$input" | jq -r '.arguments')

# Filter for specific tools
if [[ "$tool" == "Write" ]] || [[ "$tool" == "Edit" ]]; then
  # Your automation logic here
  process_file_change "$args"
fi

# MUST exit 0 (non-blocking)
exit 0
```

### Stop Hook

```bash
#!/bin/bash

# Read session context from stdin
input=$(cat)

# Generate summary
summary="Session Summary: $(date)"

# Create summary file
output_file="summaries/session-$(date +%Y%m%d-%H%M%S).md"
echo "$summary" > "$output_file"

# Exit gracefully
exit 0
```

## Best Practices

### 1. Always Exit 0
Hooks MUST exit 0 to avoid blocking Claude:

```bash
# At end of script
exit 0

# Even after errors
trap 'exit 0' ERR
```

### 2. Use JSON Parsing
Input is JSON. Use `jq` for parsing:

```bash
tool=$(echo "$input" | jq -r '.tool')
file_path=$(echo "$input" | jq -r '.arguments.file_path')
```

### 3. Filter Events
Don't process every event. Filter for relevance:

```bash
# Only process Write and Edit
[[ "$tool" != "Write" ]] && [[ "$tool" != "Edit" ]] && exit 0

# Only process specific paths
[[ ! "$file_path" =~ ^ideas/ ]] && exit 0
```

### 4. Error Resilience
Hooks should never crash Claude:

```bash
# Set error trap
trap 'exit 0' ERR

# Validate before processing
[[ -z "$file_path" ]] && exit 0
[[ ! -f "$file_path" ]] && exit 0
```

### 5. Background Processing
For expensive operations, fork to background:

```bash
# Process in background
(expensive_operation "$file_path" &)

# Exit immediately
exit 0
```

## Common Patterns

### Pattern 1: Auto Cross-Reference

```bash
# When idea file created, link to related ideas
if [[ "$tool" == "Write" ]] && [[ "$file_path" =~ ideas/ ]]; then
  idea_id=$(basename "$file_path" .md)

  # Find related ideas
  related=$(grep -l "similar_topic" ideas/**/*.md)

  # Update cross-references
  for rel in $related; do
    echo "- Related: $idea_id" >> "$rel"
  done
fi
```

### Pattern 2: Index Auto-Update

```bash
# When new file added, update index
if [[ "$tool" == "Write" ]]; then
  category=$(dirname "$file_path")

  # Update index with new entry
  update_index "$category" "$file_path"
fi
```

### Pattern 3: Session Logging

```bash
# Log all tool usage
log_file="logs/tool-usage-$(date +%Y%m%d).log"
echo "$(date +%H:%M:%S) $tool $file_path" >> "$log_file"
```

### Pattern 4: Backup on Change

```bash
# Backup files on edit
if [[ "$tool" == "Edit" ]]; then
  backup_dir=".backups/$(date +%Y%m%d)"
  mkdir -p "$backup_dir"
  cp "$file_path" "$backup_dir/"
fi
```

## Troubleshooting

### Hook Not Executing?

**Check file location**: Must be `.claude/hooks/post-tool-use.sh` or `.claude/hooks/stop.sh`

**Check permissions**: Run `chmod +x .claude/hooks/*.sh`

**Check syntax**: Run `bash -n .claude/hooks/post-tool-use.sh` to check for errors

### Hook Blocking Claude?

**Check exit code**: MUST exit 0, always

**Check error handling**: Add `trap 'exit 0' ERR`

**Background expensive ops**: Fork to background with `&`

### Hook Not Working as Expected?

**Add logging**: Write debug info to log file

```bash
echo "Debug: tool=$tool path=$file_path" >> /tmp/hook-debug.log
```

**Test JSON parsing**: Verify `jq` commands work

**Check filters**: Ensure event filters are correct

## Advanced Topics

### Conditional Logic
Hooks can implement complex routing:

```bash
case "$tool" in
  "Write")
    handle_file_creation "$file_path"
    ;;
  "Edit")
    handle_file_modification "$file_path"
    ;;
  "Bash")
    handle_command "$args"
    ;;
esac
```

### State Management
Hooks can maintain state in files:

```bash
# Track processed items
state_file=".claude/hooks/state.json"

# Read state
state=$(cat "$state_file")

# Update state
echo "$new_state" > "$state_file"
```

### Integration with External Tools
Hooks can call external scripts or APIs:

```bash
# Trigger external workflow
curl -X POST "https://api.example.com/webhook" \
  -H "Content-Type: application/json" \
  -d "$input"
```

## Security Considerations

### Path Validation
Always validate file paths:

```bash
# Check path is within workspace
[[ "$file_path" != /* ]] && file_path="$(pwd)/$file_path"
[[ ! "$file_path" =~ ^$(pwd) ]] && exit 0
```

### Input Sanitization
Sanitize all inputs before use:

```bash
# Sanitize for shell commands
safe_path=$(printf '%q' "$file_path")
```

### Permissions
Hooks run with user permissions. Be careful with:
- File modifications
- External commands
- Network requests

## Related Documentation

- **Claude Desktop Hooks**: Official documentation
- **Event Types**: PostToolUse, Stop events
- **JSON Parsing**: `jq` documentation

---

**Navigation**: [← Templates](./../README.md)
