---
title: "Test-Driven Development (TDD)"
type: reference
category: claude-skill
domain: [testing, development, methodology]
source: obra/superpowers
source_date: 2025-12-13
completeness: complete
tags: [tdd, testing, red-green-refactor, test-first, quality]
---

# Test-Driven Development (TDD)

## TL;DR

RED-GREEN-REFACTOR: Write failing test → Write minimal code to pass → Refactor. Never write production code before watching its test fail. Tests prove behavior by requiring observable failure first.

## When to Use

**Mandatory for:**
- New features
- Bug fixes
- Refactoring
- Behavior changes

**Exceptions (require explicit approval):**
- Throwaway prototypes
- Generated/scaffolded code
- Pure configuration files

---

## The Red-Green-Refactor Cycle

### RED Phase: Create Failing Test

Write ONE minimal test demonstrating required behavior.

**Good Test Characteristics:**
- Tests single behavior
- Uses descriptive name
- Uses real code when possible (minimize mocks)
- Fails for the right reason (missing feature, not syntax error)

```typescript
// Example: Testing retry functionality
describe('retryOperation', () => {
  it('retries failed operations up to 3 times', async () => {
    // Arrange
    let attempts = 0;
    const operation = jest.fn(() => {
      attempts++;
      if (attempts < 3) throw new Error('Transient failure');
      return 'success';
    });

    // Act
    const result = await retryOperation(operation);

    // Assert
    expect(result).toBe('success');
    expect(attempts).toBe(3);
    expect(operation).toHaveBeenCalledTimes(3);
  });
});
```

**Verify RED:**
```bash
npm test -- --grep "retries failed operations"
# Should fail with: "retryOperation is not defined"
```

### GREEN Phase: Write Minimal Passing Code

Write the SIMPLEST code that makes the test pass.

**Rules:**
- No extra features
- No premature optimization
- No "while I'm here" improvements
- Just make the test pass

```typescript
// Minimal implementation - just enough to pass
async function retryOperation<T>(
  fn: () => T | Promise<T>
): Promise<T> {
  for (let attempt = 0; attempt < 3; attempt++) {
    try {
      return await fn();
    } catch (error) {
      if (attempt === 2) throw error;
    }
  }
  throw new Error('unreachable');
}
```

**Verify GREEN:**
```bash
npm test -- --grep "retries failed operations"
# Should pass
```

### REFACTOR Phase: Clean Up

Only after tests pass, improve code quality.

**Allowed:**
- Remove duplication
- Improve naming
- Extract helpers
- Simplify logic

**Not Allowed:**
- Add new features
- Change behavior
- Break existing tests

```typescript
// Refactored: Configurable retry count
async function retryOperation<T>(
  fn: () => T | Promise<T>,
  maxAttempts: number = 3
): Promise<T> {
  let lastError: Error | undefined;

  for (let attempt = 1; attempt <= maxAttempts; attempt++) {
    try {
      return await fn();
    } catch (error) {
      lastError = error as Error;
      if (attempt === maxAttempts) break;
    }
  }

  throw lastError;
}
```

**Verify still GREEN:**
```bash
npm test
# All tests should still pass
```

---

## Bug Fix Workflow

### Problem: Empty email passes validation

**Step 1: RED - Write failing test**
```typescript
describe('form validation', () => {
  it('rejects empty email with descriptive error', async () => {
    const result = await submitForm({ email: '' });

    expect(result.success).toBe(false);
    expect(result.error).toBe('Email is required');
  });

  it('rejects whitespace-only email', async () => {
    const result = await submitForm({ email: '   ' });

    expect(result.success).toBe(false);
    expect(result.error).toBe('Email is required');
  });
});
```

**Step 2: GREEN - Add validation**
```typescript
interface FormResult {
  success: boolean;
  error?: string;
}

function submitForm(data: { email: string }): FormResult {
  if (!data.email?.trim()) {
    return { success: false, error: 'Email is required' };
  }

  // ... rest of implementation
  return { success: true };
}
```

**Step 3: REFACTOR - Extract if needed**
```typescript
// If validation logic used elsewhere
function validateRequired(value: string, fieldName: string): string | null {
  if (!value?.trim()) {
    return `${fieldName} is required`;
  }
  return null;
}

function submitForm(data: { email: string }): FormResult {
  const emailError = validateRequired(data.email, 'Email');
  if (emailError) {
    return { success: false, error: emailError };
  }
  // ...
}
```

---

## Common Rationalizations vs Reality

| What You Tell Yourself | The Truth |
|------------------------|-----------|
| "I'll write tests after" | Post-implementation tests pass immediately, proving nothing about correctness |
| "Manual testing is enough" | Can't repeat, can't catch regressions, misses edge cases |
| "This code is too simple to test" | Simple code still fails; tests provide regression protection |
| "Deleting this code wastes my work" | Keeping unverified code creates debt exceeding rewrite costs |
| "TDD is too slow" | Debugging time saved > test writing time invested |
| "Mocks are necessary" | Real implementations catch more bugs than mocks |

---

## Verification Checklist

After each phase, confirm:

```markdown
## RED Phase Check
- [ ] Test executes (no syntax errors)
- [ ] Test fails for correct reason (missing functionality)
- [ ] Error message is descriptive
- [ ] Only testing ONE behavior

## GREEN Phase Check
- [ ] Test now passes
- [ ] Implementation is minimal
- [ ] No extra features added
- [ ] All related tests still pass

## REFACTOR Phase Check
- [ ] All tests still pass
- [ ] Code is cleaner/clearer
- [ ] No behavior changes
- [ ] No new tests needed
```

---

## Critical Rules

### Never Write Production Code Before Seeing Test Fail

```typescript
// WRONG: Wrote code first, then wrote passing test
function add(a: number, b: number): number {
  return a + b;  // Code exists before test
}

test('adds numbers', () => {
  expect(add(2, 3)).toBe(5);  // This passes immediately - proves nothing!
});
```

```typescript
// RIGHT: Test first, see it fail, then implement
test('adds two numbers', () => {
  expect(add(2, 3)).toBe(5);
});
// Run test - FAILS: add is not defined
// Then implement:
function add(a: number, b: number): number {
  return a + b;
}
// Run test - PASSES: behavior verified
```

### Pre-Written Code Must Be Deleted

If you already wrote code without tests:
1. **Delete** the implementation
2. Write the test
3. Watch it fail
4. Reimplement from scratch

### One Behavior Per Test

```typescript
// BAD: Multiple behaviors
test('handles user registration', () => {
  expect(validate(email)).toBe(true);
  expect(hash(password)).toHaveLength(64);
  expect(createUser(data)).resolves.toHaveProperty('id');
  expect(sendEmail(email)).resolves.toBe(true);
});

// GOOD: Separate tests
test('validates email format', () => { ... });
test('hashes password to 64 chars', () => { ... });
test('creates user with id', () => { ... });
test('sends welcome email', () => { ... });
```

### Keep Tests Green During Refactor

```bash
# Watch mode during refactoring
npm test -- --watch

# Every save should keep tests green
# If any test fails, undo last change immediately
```

---

## Test Quality Indicators

### Good Test

```typescript
describe('PasswordValidator', () => {
  describe('validate', () => {
    it('rejects passwords shorter than 8 characters', () => {
      const validator = new PasswordValidator();

      const result = validator.validate('short');

      expect(result.valid).toBe(false);
      expect(result.errors).toContain('Password must be at least 8 characters');
    });
  });
});
```

**Why it's good:**
- Descriptive name explains behavior
- Arrange-Act-Assert structure
- Tests real behavior, not implementation
- Clear expected vs actual

### Bad Test

```typescript
test('password', () => {
  const v = new PasswordValidator();
  expect(v.validate('test').valid).toBe(false);
});
```

**Why it's bad:**
- Vague name
- No structure
- Unclear what behavior is tested
- Unclear why it should fail

---

## Edge Case Testing Template

```typescript
describe('functionName', () => {
  // Happy path
  it('handles normal input correctly', () => { ... });

  // Edge cases
  it('handles empty input', () => { ... });
  it('handles null/undefined', () => { ... });
  it('handles maximum values', () => { ... });
  it('handles special characters', () => { ... });

  // Error cases
  it('throws on invalid input', () => { ... });
  it('provides descriptive error message', () => { ... });

  // Boundary conditions
  it('handles exactly minimum valid input', () => { ... });
  it('handles one below minimum', () => { ... });
});
```

---

## Related Skills

- **systematic-debugging** - Root cause analysis before fixing
- **verification-before-completion** - Confirm fix actually works
- **condition-based-waiting** - Async test patterns
- **testing-anti-patterns** - What to avoid

---

## Quick Reference

```markdown
## TDD Checklist

### Before Writing Any Code
- [ ] Wrote test first
- [ ] Test fails for right reason
- [ ] Test name describes behavior

### After Each Test
- [ ] Minimal implementation
- [ ] All tests pass
- [ ] No extra features

### After Each Refactor
- [ ] Tests still pass
- [ ] Code is cleaner
- [ ] Behavior unchanged

### Rules
- Never code before failing test
- One behavior per test
- Real implementations > mocks
- Delete untested code, rewrite with tests
```

---

**Source:** obra/superpowers
**Navigation:** [← Claude Skills](index.md) | [← References](../../index.md)
