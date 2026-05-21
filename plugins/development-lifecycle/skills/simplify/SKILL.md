---
name: simplify
description: Reduce complexity in recently changed code — guard clauses, extract helpers, deduplicate, name constants and conditions. Apply after code review or before shipping. Never changes behavior; reverts any change that breaks tests.
---

# Simplify

Reduce unnecessary complexity in recently changed code without changing behavior.

**Golden Rule**: Never change behavior. Only change structure. Revert any change that breaks tests.

## When to Activate

- After `/review` or `code-reviewer` agent identifies complexity issues (deep nesting, long functions, magic values, duplicated logic)
- Before `/ship` when code passes tests but has structural noise
- After implementing a feature — as a final cleanup pass before the quality gate
- When you spot nesting depth ≥ 4, functions > 50 lines, or repeated 3-line blocks while writing code

Do **not** activate:
- On code outside the current change scope
- When all complexity findings are intentional (performance-critical tight loops, generated code, migrations)
- When tests are failing — fix tests first

---

## Phase 1 — SCOPE

**If a specific file or directory was requested**, use that as the scope.

**Otherwise**, detect recent changes:

```bash
git diff HEAD~1..HEAD --name-only 2>/dev/null | grep -E '\.(js|ts|tsx|jsx|py|go|rs|rb|java|cs|php)$'
# If empty, fall back to staged:
git diff --cached --name-only 2>/dev/null | grep -E '\.(js|ts|tsx|jsx|py|go|rs|rb|java|cs|php)$'
```

If no files found, skip this skill — nothing to simplify.

**Detect test command** from project config:

| Marker                          | Command                                   |
|---------------------------------|-------------------------------------------|
| `package.json`                  | `npm test` (or `pnpm`/`yarn`/`bun test`)  |
| `pytest.ini` or `pyproject.toml`| `pytest`                                  |
| `go.mod`                        | `go test ./...`                           |
| `Cargo.toml`                    | `cargo test`                              |
| `Makefile` with `test` target   | `make test`                               |

---

## Phase 2 — SIMPLIFICATION PASSES

Run passes sequentially. After each individual change, run the test command. If tests fail, revert that change and continue to the next.

### Pass 1 — Guard Clauses

**Target**: Functions with nesting depth ≥ 4.

Invert conditions and return early to flatten nesting:

```javascript
// BEFORE
function validate(user) {
  if (user) {
    if (user.email) {
      if (isValidEmail(user.email)) {
        return processUser(user);
      }
    }
  }
}

// AFTER
function validate(user) {
  if (!user) return null;
  if (!user.email) return null;
  if (!isValidEmail(user.email)) return null;
  return processUser(user);
}
```

Per function: identify deepest block → invert condition → add early return → unindent → run tests → revert on failure.

---

### Pass 2 — Extract Helpers

**Target**: Functions longer than ~50 lines.

Extract cohesive sub-tasks to named helpers (name describes WHAT, not HOW):

```javascript
// BEFORE: processOrder() — 50+ lines
// AFTER
function processOrder(order) {
  const validated = validateOrderItems(order);
  const priced    = calculatePricing(validated);
  saveToDatabase(priced);
  sendConfirmation(priced);
}
```

Per function: find logical groupings → extract to named helper → replace with call → run tests → revert on failure.

---

### Pass 3 — Deduplicate

**Target**: Repeated code blocks (3+ similar lines, 2+ occurrences) within the change scope.

Extract to a shared utility function. Do not reach outside the scope to deduplicate with unrelated code.

Per duplication: identify pattern → extract utility → replace both occurrences → run tests → revert on failure.

---

### Pass 4 — Name Magic Values

**Target**: Hardcoded literals used in logic conditions (`if (status === "PENDING")`, `if (count > 100)`).

```javascript
// BEFORE
if (items.length > 50) { ... }
// AFTER
const MAX_BATCH_SIZE = 50;
if (items.length > MAX_BATCH_SIZE) { ... }
```

Per literal: identify usage context → choose descriptive name → define constant at file/module top → replace → run tests → revert on failure.

---

### Pass 5 — Name Complex Conditions

**Target**: Boolean expressions with 3+ operators.

```javascript
// BEFORE
if (user.isActive && user.hasSubscription && !user.isBlocked || user.isAdmin) { ... }
// AFTER
const canAccess = (user.isActive && user.hasSubscription && !user.isBlocked) || user.isAdmin;
if (canAccess) { ... }
```

Name describes intent, not logic. Per condition: identify intent → extract to named variable or helper → replace → run tests → revert on failure.

---

## Phase 3 — SUMMARY

```
## Simplification Summary

### Changes
- [file:line] — guard clauses: inverted N conditions in functionName
- [file:line] — extracted helper: helperName
- [file:line] — named constant: CONSTANT_NAME = value
- ...

### Skipped
- [file] — reason (e.g., "No deep nesting", "All changes reverted — tests failed")

### Tests
All N tests passing.
```

If nothing was simplified: `Code is already clean — no simplifications applied.`

---

## Lifecycle Position

```text
/spec → /plan → superpowers execution → [simplify activates here] → /ship
```

Simplify runs after implementation and review, before the `/ship` quality gate.
