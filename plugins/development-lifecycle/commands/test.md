---
description: TDD workflow — red/green for new features, Prove-It pattern for bug fixes
argument-hint: [feature name, or "fix: <bug description>"]
---

# Test Command

Focused TDD workflow: for NEW features, write tests first (RED → GREEN → REFACTOR). For BUG FIXES, use the Prove-It pattern — write a reproducing test (must FAIL), confirm failure, implement fix, confirm pass, run full suite.

**Input**: $ARGUMENTS (optional feature name or "fix: <bug description>"; blank to ask)

---

## Phase 1 — MODE DETECTION

If `$ARGUMENTS` starts with `fix:` or `bug:`:
→ Enter **Bug Fix Mode** (Prove-It pattern)

Otherwise if `$ARGUMENTS` is not blank:
→ Enter **Feature Mode**

Otherwise if `$ARGUMENTS` is blank:
**GATE**: Ask the user:

> Are you adding a new feature or fixing a bug?
> 
> Reply: "feature" or "fix: <description>"

Wait for clarification, then proceed to the appropriate mode.

---

## Feature Mode — Phase 2 (RED)

Write test(s) that describe the expected behavior. Place tests in the project's standard test location:
- **TypeScript/JavaScript**: `src/` or `tests/` with `.test.ts`/`.spec.ts` suffix
- **Python**: `tests/` or same directory with `test_` prefix
- **Go**: `*_test.go` in the same package
- **Rust**: `#[cfg(test)]` module or `tests/` directory

**Match existing conventions**: If the project has existing tests, use the same directory and naming pattern.

Write tests specific to the feature's behavior. Run the test suite:

```bash
{detected_test_command}
```

Confirm the tests FAIL:

> Tests failed as expected (RED phase complete):
> 
> {failure_output}

**GATE**: If tests pass unexpectedly:

> Tests already pass — feature may already exist. Confirm this is intentional?

Otherwise, proceed to Phase 3.

---

## Feature Mode — Phase 3 (GREEN)

Implement the minimal code to make the tests pass. Do NOT over-engineer or add features beyond what the tests require.

Run the tests again:

```bash
{detected_test_command}
```

Confirm the tests PASS:

> Tests pass (GREEN phase complete):
> 
> {test_output}

**GATE**: If tests still fail:

> Tests still failing. Fix implementation or test?

Clarify with the user, fix, and rerun.

---

## Feature Mode — Phase 4 (REFACTOR)

Improve clarity and remove duplication while keeping tests green. After each change, run the full test suite:

```bash
{detected_test_command}
```

If any test goes red after a refactor, undo the change:

> Regression detected during refactor. Reverting change.

When the suite is green and the code is clean, proceed to coverage check.

---

## Bug Fix Mode — Phase 2 (PROVE IT)

Write a test that reproduces the bug (it must FAIL). The test should demonstrate the exact failure described:

```bash
{detected_test_command}
```

Confirm the test FAILS with the expected error:

> Reproducing test fails (PROVE IT phase complete):
> 
> {failure_output}

**GATE**: If the test passes:

> Test passes — bug may already be fixed. Verify this with the user?

Otherwise, proceed to Phase 3.

---

## Bug Fix Mode — Phase 3 (FIX)

Implement the fix. Run the reproducing test:

```bash
{detected_test_command}
```

Confirm the test PASSES:

> Reproducing test passes (FIX phase complete):
> 
> {test_output}

Do NOT modify pre-existing tests to make them pass. Fix the implementation instead.

Then run the full test suite to detect regressions:

```bash
{detected_test_command}
```

Report results:

> Full suite status:
> - {pass_count} tests passing
> - {fail_count} tests failing

**GATE**: If any previously-passing test now fails:

> Regression detected: {failing_tests}
> 
> Fix the implementation to restore the test(s).

Once all tests pass, proceed to coverage check.

---

## Coverage Check (Both Modes)

Detect the project type and run coverage:

**Node.js/TypeScript**:
```bash
npm test -- --coverage
# or: jest --coverage, vitest --coverage
```

**Python**:
```bash
pytest --cov
```

**Go**:
```bash
go test -cover ./...
```

**Rust**:
```bash
cargo tarpaulin
# or: cargo llvm-cov
```

Report coverage:

> Coverage: {coverage_percent}%

**GATE**: If coverage is below 80%, identify untested paths and add tests:

> Coverage below 80%. Identify untested branches and add tests?

Add tests for uncovered paths, rerun the full suite to confirm green, then complete.

Otherwise, proceed to final status.

---

## Final Status

Print:

> Test suite complete and green. Run `/review` for code quality check, or `/build` for the next task.

---

## Lifecycle Position

/spec → /plan → loop(/build → /test → /review → /simplify) → /ship

Run this command after implementing a feature with `/build`, or use it to validate bug fixes before committing. Run `/review` next for code quality check.
