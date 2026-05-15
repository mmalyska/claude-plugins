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

## Phase 1.5 — TEST-RUNNER DETECTION

Before proceeding to the mode-specific phases, detect the test command:

**Check for test scripts/configs:**
1. If `package.json` exists: look for `test`, `vitest`, or `jest` in scripts
2. If `pytest.ini`, `setup.cfg`, or `pyproject.toml` exist: use `pytest`
3. If `go.mod` exists: use `go test ./...`
4. If `Cargo.toml` exists: use `cargo test`

**If no test command detected:**
**GATE**: Ask the user:

> What command runs your tests in this project?
> 
> Examples: `npm test`, `pytest`, `go test ./...`, `cargo test`

Wait for the user's response. Store the result as `test_command`.

**Throughout this workflow**, use `test_command` in all bash code blocks (previously shown as `test_command`).

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
test_command
```

Confirm the tests FAIL:

> Tests failed as expected (RED phase complete):
> 
> {failure_output}

**GATE**: If the tests pass unexpectedly, STOP:

> Tests already pass — this feature may already exist.
> Confirm whether to: (a) revise the tests, (b) treat this as already implemented, or (c) abandon.

Wait for user response before proceeding.

Otherwise, proceed to Phase 3.

---

## Feature Mode — Phase 3 (GREEN)

Implement the minimal code to make the tests pass. Do NOT over-engineer or add features beyond what the tests require.

Run the tests again:

```bash
test_command
```

Confirm the tests PASS:

> Tests pass (GREEN phase complete):
> 
> {test_output}

**GATE**: If tests still fail:

Fix the implementation to make the test pass. Do NOT modify or delete the failing test.

If the test itself appears incorrect, STOP and ask the user.

---

## Feature Mode — Phase 4 (REFACTOR)

Improve clarity and remove duplication while keeping tests green. **Limit refactoring to code written or modified in this feature. Do not refactor pre-existing unrelated code.**

After each change, run the full test suite:

```bash
test_command
```

If any test goes red after a refactor, undo the change:

> Regression detected during refactor. Reverting change.

**GATE**: When the test suite is green and the code is clean, confirm with the user:

> Refactoring complete. Suite is green. Proceed to coverage check?

Wait for user confirmation before proceeding.

---

## Bug Fix Mode — Phase 2 (PROVE IT)

Write a test that reproduces the bug (it must FAIL). The test should demonstrate the exact failure described:

```bash
test_command
```

Confirm the test FAILS with the expected error:

> Reproducing test fails (PROVE IT phase complete):
> 
> {failure_output}

**GATE**: If the test passes, STOP and tell the user:

> Test passes — bug may already be fixed or the test is incorrect. Confirm whether to continue or revise the test.

Wait for user response before proceeding.

---

## Bug Fix Mode — Phase 3 (FIX)

Implement the fix. Run the reproducing test:

```bash
test_command
```

Confirm the test PASSES:

> Reproducing test passes (FIX phase complete):
> 
> {test_output}

Do NOT modify pre-existing tests to make them pass. Fix the implementation instead.

Then run the full test suite to detect regressions:

```bash
test_command
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

Bug Fix Mode does not include a REFACTOR phase — proceed directly to Coverage Check.

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

**Fallback**: If the coverage tool is not installed or not configured, warn the user and skip the coverage gate, noting that coverage was not verified.

Report coverage:

> Coverage: {coverage_percent}%

**GATE**: If coverage is below 80%:

Identify untested branches and add tests for them.

Then re-run the coverage tool and check the percentage again. Only proceed to Final Status when coverage is at or above 80% (or the user explicitly accepts the current level).

---

## Final Status

Print:

> Suite is green. Run `/review` for code quality, `/simplify` to clean up, or `/build` for the next task.

---

## Lifecycle Position

/spec → /plan → loop(/build → /test → /review → /simplify) → /ship

Run this command after implementing a feature with `/build`, or use it to validate bug fixes before committing. Run `/review` next for code quality check.
