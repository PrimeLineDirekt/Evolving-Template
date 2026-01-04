# Subagent-Driven Development Examples

## Example 1: Feature Implementation

**Plan**: Add user authentication to API

### Task Extraction
```
Task 1: Create User model with password hashing
Task 2: Implement login/logout endpoints
Task 3: Add JWT token generation
Task 4: Create auth middleware
Task 5: Write integration tests
```

### Implementer Report (Task 1)
```
What I implemented:
- User model with email, password_hash, created_at
- Password hashing via bcrypt (12 rounds)
- Model validation for email format

Test results: 5/5 passing
Files changed: models/user.py, tests/test_user.py

Self-review:
- [x] All requirements met
- [x] Clear naming
- [x] Follows existing patterns
- [x] No overbuild

Issues: None
```

### Spec Reviewer Response
```
✅ SPEC COMPLIANT

Verified:
- [x] User model exists: models/user.py:1-45
- [x] Password hashing: uses bcrypt, verified
- [x] Validation: email regex at line 23
```

### Quality Reviewer Response
```
Strengths:
- Clean model structure
- Good test coverage

Issues:
**Minor**: Consider adding index on email field

Assessment: ✅ APPROVED
```

---

## Example 2: Spec Reviewer Catches Missing Feature

### Implementer Report
```
What I implemented:
- Login endpoint at /auth/login
- Returns JWT token

Test results: 3/3 passing
```

### Spec Reviewer Response
```
❌ SPEC ISSUES FOUND

Missing:
- [ ] Logout endpoint not implemented (spec line 12)
- [ ] Token refresh endpoint missing (spec line 15)

Verified:
- [x] Login endpoint works

Required Fixes:
1. Implement POST /auth/logout
2. Implement POST /auth/refresh
```

---

## Example 3: Quality Reviewer Catches Issues

### Quality Reviewer Response
```
Issues:

**Critical** (must fix):
- SQL injection risk at auth/routes.py:34
  `query = f"SELECT * FROM users WHERE email='{email}'"`
  → Use parameterized queries

**Important** (should fix):
- Magic number at auth/utils.py:12
  `token_expiry = 3600`
  → Extract to config constant

**Minor** (nice to have):
- Consider adding docstring to verify_token()

Assessment: ❌ NEEDS WORK
```

---

## Workflow Example

```
[Main Agent]
├─ Load plan from knowledge/plans/auth-feature.md
├─ Extract 5 tasks → TodoWrite
│
├─ Task 1: User Model
│   ├─ Spawn Implementer → implements + reports
│   ├─ Spawn Spec Reviewer → ✅ COMPLIANT
│   ├─ Spawn Quality Reviewer → ✅ APPROVED
│   └─ Mark Complete ✓
│
├─ Task 2: Login/Logout
│   ├─ Spawn Implementer → implements + reports
│   ├─ Spawn Spec Reviewer → ❌ MISSING LOGOUT
│   │   └─ Implementer fixes → ✅ COMPLIANT
│   ├─ Spawn Quality Reviewer → ⚠️ APPROVED WITH NOTES
│   └─ Mark Complete ✓
│
└─ Final Review
    ├─ Run full test suite: 23/23 passing
    └─ Summary to user
```

---

## Anti-Patterns

### ❌ Trusting Implementer Report
```
Implementer: "All done, tests pass!"
Reality: Only 2/5 requirements implemented

→ Spec Reviewer MUST read code, not report
```

### ❌ Skipping Quality Review
```
"Spec is compliant, ship it!"
Reality: SQL injection vulnerability

→ Quality review catches non-spec issues
```

### ❌ No Self-Review
```
Implementer submits without checking:
- Left TODO comments
- Added unrequested features
- Didn't run tests

→ Self-review checklist prevents this
```
