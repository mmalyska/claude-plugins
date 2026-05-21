---
description: TDD workflow — delegates to superpowers:test-driven-development for features; Prove-It pattern for bug fixes
argument-hint: [feature name, or "fix: <bug description>"]
---

# Test Command

**Input**: $ARGUMENTS

---

## Mode Detection

If `$ARGUMENTS` starts with `fix:` or `bug:`:
→ Enter **Bug Fix Mode** (Prove-It pattern) below.

Otherwise:
→ Invoke `superpowers:test-driven-development` skill. That skill runs the full RED-GREEN-REFACTOR cycle.

If `$ARGUMENTS` is blank, ask:

> Are you adding a new feature or fixing a bug?
>
> Reply: "feature" or "fix: {description}"

---

## Bug Fix Mode — Prove-It Pattern

**Detect test command** from project config (`package.json`, `pytest.ini`, `go.mod`, `Cargo.toml`). If not found, ask the user.

### Phase 1 — PROVE IT (RED)

Write a test that reproduces the bug. It MUST fail. Run it:

```bash
{test_command}
```

Confirm the test fails with the expected error.

**GATE**: If the test passes, STOP:

> Test passes — bug may already be fixed or the test is wrong. Confirm: (a) revise the test, (b) treat as already fixed, or (c) abandon.

### Phase 2 — FIX (GREEN)

Implement the fix. Run the reproducing test:

```bash
{test_command}
```

Confirm it passes. Do NOT modify pre-existing tests — fix the implementation.

Then run the full suite to detect regressions:

```bash
{test_command}
```

**GATE**: If any previously-passing test now fails, stop and fix the regression before continuing.

### Phase 3 — COVERAGE CHECK

Run coverage for the project type:

| Stack              | Command                   |
|--------------------|---------------------------|
| Node.js/TypeScript | `npm test -- --coverage`  |
| Python             | `pytest --cov`            |
| Go                 | `go test -cover ./...`    |
| Rust               | `cargo tarpaulin`         |

If coverage tool is unavailable, warn and skip.

**GATE**: If coverage is below 80%, identify untested branches, add tests, and recheck before proceeding.

### Done

> Suite is green. Run `/review` for code quality or `/ship` when ready to deliver.

---

## Lifecycle Position

```text
/spec → superpowers execution → /ship
                    ↑ superpowers:test-driven-development runs here ↑
/test fix: {bug}  ← standalone bug fix entry point
```
