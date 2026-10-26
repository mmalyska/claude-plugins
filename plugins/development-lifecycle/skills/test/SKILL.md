---
name: test
description: "TDD workflow for features and reproducible bug fixes in Claude Code or Codex"
---

Use the current user request as input. In a Claude command invocation, `$ARGUMENTS` carries that input; in Codex, use the text accompanying the skill.
Command-style examples below name workflows: in Codex select the corresponding
installed skill (`$plugin:skill`); do not execute slash commands in a shell.

# Test Command

**Input**: $ARGUMENTS

---

## Mode Detection

If `$ARGUMENTS` starts with `fix:` or `bug:`:
→ Enter **Bug Fix Mode** (Prove-It pattern) below.

Otherwise:
→ Enter Feature Mode: derive a focused behavior from the accepted requirements;
write and run a test that fails for the expected missing behavior; implement
the smallest working change; rerun the focused test; refactor with tests green;
then run relevant regression checks. Repeat per behavior. Use an installed TDD
skill if helpful, but no external skill is required.

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

Use installed project tooling; do not fetch a coverage package implicitly. If
coverage is unavailable, report NOT RUN and the remaining uncertainty.

**GATE**: Apply the project's established coverage target. Report uncovered
changed behavior and fix relevant gaps; do not invent a global percentage gate.

### Done

> Suite is green. Run `/review` for code quality or `/ship` when ready to deliver.

---

## Lifecycle Position

```text
spec → implementation and tests → ship
                    ↑ RED-GREEN-REFACTOR runs here ↑
/test fix: {bug}  ← standalone bug fix entry point
```
