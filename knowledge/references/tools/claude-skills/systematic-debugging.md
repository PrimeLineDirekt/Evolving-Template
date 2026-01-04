---
title: "Systematic Debugging"
type: reference
category: claude-skill
domain: [debugging, methodology, problem-solving]
source: obra/superpowers
source_date: 2025-12-13
completeness: complete
tags: [debugging, root-cause, systematic, four-phase, diagnostic]
---

# Systematic Debugging

## TL;DR

4-Phase Root Cause Analysis: Investigation → Pattern Analysis → Hypothesis Testing → Implementation. NO FIXES WITHOUT ROOT CAUSE. 15-30 min resolution vs 2-3h trial-and-error. 95% first-time fix rate.

## When to Use

- Bugs that don't have obvious causes
- Issues that return after "fixing"
- Multi-component system failures
- Performance regressions
- Intermittent failures
- When 3+ quick fixes have failed

## The Core Principle

**"NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST"**

This is non-negotiable. Quick patches create technical debt and often mask deeper issues.

---

## Phase 1: Root Cause Investigation

Complete ALL five steps before proposing ANY fix:

### Step 1: Read Error Information
```
- Carefully read ENTIRE error message
- Note error codes and their meanings
- Examine full stack trace (not just first line)
- Check for related warnings
- Look for timing/sequence clues
```

### Step 2: Reproduce Consistently
```markdown
## Reproduction Steps
1. [Exact step to reproduce]
2. [Next step]
3. [Final step]

**Expected:** [What should happen]
**Actual:** [What happens]
**Frequency:** [Always / 80% / Random]
**Environment:** [OS, Node version, etc.]
```

### Step 3: Review Recent Changes
```bash
# Check git history for recent changes
git log --oneline -20

# See what changed in specific file
git log -p --follow -- path/to/problematic/file.ts

# Find when a line was introduced
git blame path/to/file.ts

# Check dependency changes
git diff HEAD~5 package.json
git diff HEAD~5 package-lock.json
```

### Step 4: Add Diagnostic Instrumentation

For multi-component systems, add logging at EVERY boundary:

```typescript
// Example: Workflow → Build → Signing pipeline

// Boundary 1: Workflow entry
console.log('[DIAG] Workflow input:', JSON.stringify({
  trigger: event.type,
  payload: event.payload,
  timestamp: new Date().toISOString()
}));

// Boundary 2: Build step entry
console.log('[DIAG] Build input:', JSON.stringify({
  config: buildConfig,
  env: process.env.NODE_ENV,
  dependencies: Object.keys(pkg.dependencies)
}));

// Boundary 3: Build step exit
console.log('[DIAG] Build output:', JSON.stringify({
  success: result.success,
  artifacts: result.artifacts,
  duration: result.duration
}));

// Boundary 4: Signing step
console.log('[DIAG] Signing input:', JSON.stringify({
  artifactPath: artifact.path,
  signatureType: config.signatureType,
  certValid: cert.isValid()
}));
```

### Step 5: Trace Data Flow Backward

Start from the error and work backwards:

```
Error: "Invalid signature on artifact"
  ↑
Signing step received: { artifact: "/path/to/file", cert: null }
  ↑
Build step output: { artifacts: ["/path/to/file"] }  // No cert passed!
  ↑
Config loading: { signing: { enabled: true, cert: undefined } }  // Missing!
  ↑
ENV: SIGNING_CERT not set in CI environment  // ROOT CAUSE FOUND
```

---

## Phase 2: Pattern Analysis

Before proposing solutions:

### Find Working Reference
```bash
# Search for similar working code
grep -r "similar_function_name" src/

# Find tests for working functionality
grep -r "describe.*similar" tests/

# Check if there's a working version in another branch
git log --all --oneline -- "path/to/file"
```

### Document Differences

```markdown
## Working vs Broken Comparison

| Aspect | Working Version | Broken Version |
|--------|-----------------|----------------|
| Input validation | Validates before processing | No validation |
| Error handling | Catches and logs | Throws unhandled |
| Dependencies | Uses v2.1.0 | Uses v3.0.0 |
| Config | Explicit settings | Defaults assumed |
| Environment | Runs in Docker | Runs locally |
```

### List ALL Assumptions

```markdown
## Implicit Assumptions in Broken Code
1. Assumes `config.timeout` is always defined
2. Assumes network is available
3. Assumes file exists before reading
4. Assumes user has write permissions
5. Assumes database connection is active
```

---

## Phase 3: Hypothesis Testing

Apply scientific method:

### State Hypothesis Clearly

```markdown
## Hypothesis 1
**Claim:** The build fails because NODE_ENV is not propagated to child process
**Evidence:**
- Parent process has NODE_ENV=production
- Child process logs show NODE_ENV=undefined
**Test:** Add explicit env passing to spawn() call
**Expected Result:** Child process will show NODE_ENV=production
```

### Make Minimal Changes

```typescript
// BAD: Multiple changes at once
spawn('node', ['build.js'], {
  env: { ...process.env },     // Change 1
  cwd: projectRoot,            // Change 2
  stdio: 'inherit',            // Change 3
  timeout: 30000               // Change 4
});

// GOOD: One change to test hypothesis
spawn('node', ['build.js'], {
  env: { ...process.env }      // Only testing env propagation
});
```

### Verify Before Proceeding

```markdown
## Hypothesis 1 Result
**Status:** CONFIRMED / REJECTED
**Actual Result:** [What happened]
**Conclusion:** [Next step based on result]
```

If rejected, form NEW hypothesis - don't add more fixes!

---

## Phase 4: Implementation

Only after root cause is understood:

### Step 1: Create Failing Test

```typescript
describe('environment propagation', () => {
  it('passes NODE_ENV to child process', async () => {
    // Arrange
    process.env.NODE_ENV = 'production';

    // Act
    const result = await runBuild();

    // Assert
    expect(result.childEnv.NODE_ENV).toBe('production');
  });
});
```

### Step 2: Implement Single Fix

```typescript
// Fix ONLY the root cause
function runBuild(): Promise<BuildResult> {
  return new Promise((resolve) => {
    const child = spawn('node', ['build.js'], {
      env: { ...process.env }  // Single fix for root cause
    });
    // ...
  });
}
```

### Step 3: Verify No Regressions

```bash
# Run full test suite
npm test

# Run specific affected tests
npm test -- --grep "build"

# Check for new warnings
npm run lint
```

---

## Critical Checkpoint: The 3-Fix Rule

**If 3+ fixes fail, STOP and question architectural soundness.**

```markdown
## 3-Fix Checkpoint Analysis

### Failed Fixes:
1. Added null check → Still fails with different error
2. Added retry logic → Times out instead of failing
3. Added fallback → Falls back but with corrupted data

### Questions to Answer:
- Is the fundamental approach correct?
- Are we solving the right problem?
- Is there a design flaw we're working around?
- Should we step back and redesign?

### Decision:
[ ] Continue debugging (with justification)
[ ] Escalate to design review
[ ] Revert and try different approach
```

---

## Red Flags: Reset to Phase 1

Recognize these patterns as signals to restart:

| Red Flag | What You're Thinking | What You Should Do |
|----------|---------------------|-------------------|
| "Let me just try..." | Proposing fix before understanding | Return to Phase 1 |
| "And also while I'm here..." | Multiple simultaneous changes | Make ONE change |
| "I don't need a test for this" | Skipping test creation | Write failing test first |
| "This is similar to..." | Adapting pattern without comprehension | Read reference fully |
| "Fourth time's the charm" | Attempting fix #4+ | Stop, reassess architecture |

---

## Multi-Layer Diagnostic Template

```markdown
## Diagnostic Report: [Issue Description]

### Layer 1: [Component Name]
- Input: [What enters]
- Output: [What exits]
- Config: [Relevant settings]
- Status: OK / SUSPECT / FAILED

### Layer 2: [Component Name]
- Input: [What enters]
- Output: [What exits]
- Config: [Relevant settings]
- Status: OK / SUSPECT / FAILED

### Layer 3: [Component Name]
- Input: [What enters]
- Output: [What exits]
- Config: [Relevant settings]
- Status: OK / SUSPECT / FAILED

### Failure Point Identified
Layer: [Number]
Specific Issue: [Description]
Root Cause: [Why it happens]
```

---

## Performance Comparison

| Approach | Avg Resolution Time | First-Time Fix Rate |
|----------|---------------------|---------------------|
| Trial and Error | 2-3 hours | 40% |
| Systematic Method | 15-30 minutes | 95% |

---

## Related Skills

- **root-cause-tracing** - Backward data flow analysis
- **test-driven-development** - Create failing tests before fixes
- **verification-before-completion** - Ensure fixes genuinely resolved

---

## Quick Reference Checklist

```markdown
## Debugging Checklist

### Phase 1: Investigation
- [ ] Read complete error message and stack trace
- [ ] Documented reproduction steps
- [ ] Reviewed git history for recent changes
- [ ] Added diagnostic instrumentation
- [ ] Traced data flow backward to root cause

### Phase 2: Pattern Analysis
- [ ] Found similar working code
- [ ] Listed all differences
- [ ] Documented assumptions

### Phase 3: Hypothesis
- [ ] Stated clear hypothesis with reasoning
- [ ] Made minimal single-variable change
- [ ] Verified result before proceeding

### Phase 4: Implementation
- [ ] Created failing test first
- [ ] Implemented single fix
- [ ] Verified no regressions
- [ ] Confirmed issue resolved

### 3-Fix Checkpoint
- [ ] If 3 fixes failed: stopped to reassess
```

---

**Source:** obra/superpowers
**Navigation:** [← Claude Skills](index.md) | [← References](../../index.md)
