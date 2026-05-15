---
description: Simplify recently changed code — guard clauses, extract helpers, name constants
argument-hint: "[file or directory, or blank to simplify recent changes]"
---

> Reduce unnecessary complexity in recently changed code without changing behavior. Techniques include: deep nesting → guard clauses, long functions → smaller helpers, duplicated logic → shared utility, magic literals → named constants, verbose conditions → named booleans.

# Simplify

After a code review, simplify the revised code to reduce complexity. Every simplification is tested immediately — if tests fail, that change is reverted and we continue.

**Core Philosophy**: Simplification only reduces noise. If it breaks tests, undo it. If code is already clean, leave it alone.

**Golden Rule**: Never change behavior. Only change structure. Always test after every change.

---

## Phase 1 — SCOPE

### Detect Changed Files

**If $ARGUMENTS is provided:**
```bash
# User specified a file or directory
SCOPE="$ARGUMENTS"
```

**If $ARGUMENTS is blank:**
```bash
# Use recent changes: staged + unstaged
git diff --cached --name-only 2>/dev/null | sort -u > /tmp/staged.txt
git diff HEAD --name-only 2>/dev/null | sort -u > /tmp/unstaged.txt
cat /tmp/staged.txt /tmp/unstaged.txt 2>/dev/null | sort -u | grep -E '\.(js|ts|tsx|jsx|py|go|rs|rb|java|cs|php)$' > /tmp/changed_files.txt
SCOPE=$(cat /tmp/changed_files.txt)
```

### Display Scope

```
## Simplification Scope

Files to simplify:
```bash
echo "$SCOPE"
```
```

**GATE**: If no changed files found and no $ARGUMENTS provided:
```
> Error: No changed files detected and no target specified.
> Please provide a file or directory: /simplify src/utils
> Or commit/stage changes first, then run /simplify
```

### Detect Test Command

Detect the project's test runner:

| Marker | Test Command |
|---|---|
| `package.json` exists | `npm test` (or `pnpm test`, `yarn test`, `bun test` based on lockfile) |
| `pytest.ini` or `pyproject.toml` | `pytest` |
| `go.mod` exists | `go test ./...` |
| `Cargo.toml` exists | `cargo test` |
| `Makefile` has `test` target | `make test` |

If ambiguous, ask:
```
> Which command runs your tests?
> (e.g., npm test, pytest, go test ./..., cargo test)
```

Store detected command as `$test_command`.

**CHECKPOINT**: Scope identified. Test command detected.

---

## Phase 2 — SIMPLIFICATION PASSES

Run the following passes sequentially on scoped files. After each change, run `$test_command`.

### Pass 1 — Guard Clauses

**Goal**: Flatten deep nesting by inverting conditions and returning early.

**Find**: Functions with nesting depth > 3 (typically if/else chains with 4+ levels)

**Example Transformation**:
```javascript
// BEFORE (3+ levels)
function validate(user) {
  if (user) {
    if (user.email) {
      if (isValidEmail(user.email)) {
        return processUser(user);
      }
    }
  }
}

// AFTER (guard clauses)
function validate(user) {
  if (!user) return null;
  if (!user.email) return null;
  if (!isValidEmail(user.email)) return null;
  return processUser(user);
}
```

**Per function**:
1. Identify the deepest nested block
2. Invert its condition; add early return or continue
3. Unindent subsequent code
4. Run `$test_command`
5. If tests fail → revert this function and continue to next
6. If tests pass → keep and move to next function

**Track**: For each modified function, note `[file:line] — inverted [N] conditions`

---

### Pass 2 — Extract Helpers

**Goal**: Reduce function length by extracting cohesive sub-tasks to named helpers.

**Find**: Functions longer than ~50 lines

**Example Transformation**:
```javascript
// BEFORE (long function)
function processOrder(order) {
  // Validate order items (10 lines)
  // Calculate tax and shipping (8 lines)
  // Apply discounts (10 lines)
  // Save to database (5 lines)
  // Send confirmation email (7 lines)
  // ... 50+ lines total
}

// AFTER (extracted helpers)
function processOrder(order) {
  const validated = validateOrderItems(order);
  const priced = calculateTaxAndShipping(validated);
  const discounted = applyDiscounts(priced);
  saveToDatabase(discounted);
  sendConfirmationEmail(discounted);
}

// New helper functions
function validateOrderItems(order) { /* ... */ }
function calculateTaxAndShipping(order) { /* ... */ }
```

**Per function**:
1. Identify cohesive code blocks (look for comments or logical groupings)
2. Extract each block to a named helper function (name describes WHAT, not HOW)
3. Replace block with a call to the helper
4. Run `$test_command`
5. If tests fail → revert this extraction and continue
6. If tests pass → keep and move to next block

**Track**: For each extraction, note `[file:line] — extracted helper [function_name]`

---

### Pass 3 — Deduplicate

**Goal**: Extract repeated code blocks to a shared function.

**Find**: Repeated code blocks (3+ similar lines appearing 2+ times in the same file or adjacent files)

**Example Transformation**:
```javascript
// BEFORE (duplicated)
// in userService.js
const user = parseJSON(response.body);
if (!user.email) throw new Error("Invalid email");

// in productService.js
const product = parseJSON(response.body);
if (!product.id) throw new Error("Invalid id");

// AFTER (shared utility)
// in utils/validation.js
function parseAndValidate(body, requiredFields) {
  const data = parseJSON(body);
  for (const field of requiredFields) {
    if (!data[field]) throw new Error(`Invalid ${field}`);
  }
  return data;
}
```

**Per duplication**:
1. Identify the repeated pattern
2. Extract to a shared utility function (at module or file level)
3. Replace both occurrences with calls to the utility
4. Run `$test_command`
5. If tests fail → revert and continue
6. If tests pass → keep and move to next duplication

**Track**: For each deduplication, note `[file:line] — deduplicated [pattern_description]`

---

### Pass 4 — Name Magic Values

**Goal**: Extract literal strings, numbers, or booleans to named constants.

**Find**: Hardcoded literals used in logic conditions (e.g., `if (status === "PENDING")`, `if (count > 100)`)

**Example Transformation**:
```javascript
// BEFORE (magic values)
function processBatch(items) {
  if (items.length > 50) {
    // batch is too large
  }
  if (item.status === "SHIPPED") {
    // handle shipped
  }
}

// AFTER (named constants)
const MAX_BATCH_SIZE = 50;
const STATUS_SHIPPED = "SHIPPED";

function processBatch(items) {
  if (items.length > MAX_BATCH_SIZE) {
    // batch is too large
  }
  if (item.status === STATUS_SHIPPED) {
    // handle shipped
  }
}
```

**Per literal**:
1. Identify magic value and its usage context
2. Choose a descriptive constant name
3. Define constant at the top of the file or module
4. Replace literal with constant reference
5. Run `$test_command`
6. If tests fail → revert and continue
7. If tests pass → keep and move to next literal

**Track**: For each constant, note `[file:line] — named constant [CONSTANT_NAME] = [value]`

---

### Pass 5 — Name Complex Conditions

**Goal**: Extract complex boolean conditions to named variables or helper functions.

**Find**: Boolean conditions with 3+ operators (e.g., `if (a && b || c && d)`)

**Example Transformation**:
```javascript
// BEFORE (complex condition)
if (user.isActive && user.hasSubscription && !user.isBlocked || user.isAdmin) {
  // allow access
}

// AFTER (named boolean)
const isUserEligible = user.isActive && user.hasSubscription && !user.isBlocked || user.isAdmin;
if (isUserEligible) {
  // allow access
}

// OR as helper function
function isUserEligible(user) {
  return (user.isActive && user.hasSubscription && !user.isBlocked) || user.isAdmin;
}
if (isUserEligible(user)) {
  // allow access
}
```

**Per complex condition**:
1. Identify the condition and its intent
2. Extract to a named variable or helper function
3. The name should describe the intent, not the logic
4. Replace condition with variable/function call
5. Run `$test_command`
6. If tests fail → revert and continue
7. If tests pass → keep and move to next condition

**Track**: For each extraction, note `[file:line] — named condition [variable_or_function_name]`

---

## Phase 3 — SUMMARY

After all passes complete, generate:

```
## Simplification Summary

### Changed
[List all changes made across all passes, one per line]
- [file:line] — description of simplification

### Unchanged (no changes needed or all changes reverted)
[List files where no changes were made]
- [file] — reason (e.g., "No deep nesting", "No duplicates found")

### Test Results
[Summary of test status]
All [N] tests passing.
```

If nothing was simplified:
```
> Code is already clean. No simplifications needed.
```

---

## Phase 4 — CONFIRM

Display:

```
Simplification complete. Run /ship to finish the feature, or /build for the next task.
```

Do not gate on user response — this is informational.

---

## Lifecycle Position

/spec → /plan → loop(/build → /test → /review → /simplify) → /ship

After simplifying, run /ship to deliver the feature or /build for the next task.
