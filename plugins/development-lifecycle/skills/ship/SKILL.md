---
name: ship
description: "Review delivery readiness, verify checks, and perform the authorized commit, PR, or branch-finishing workflow"
---

Use the current user request as input. In a Claude command invocation, `$ARGUMENTS` carries that input; in Codex, use the text accompanying the skill.
Command-style examples below name workflows: in Codex select the corresponding
installed skill (`$plugin:skill`); do not execute slash commands in a shell.

# /ship - Delivery Gate

The final stage of the development lifecycle. Ship runs a pre-flight check, dispatches three parallel review passes (code quality, security, test completeness), produces a GO/NO-GO decision, and if approved, commits changes, pushes to a branch, and creates a PR.

---

## Phase 1 — PRE-FLIGHT

### Show Current Status

Run `git status` to display staged, unstaged, and untracked files:

```bash
git status
```

Output:

> Current branch status:
> [output of git status]

### Run Full Test Suite

Detect the project's test command:

1. If `package.json` exists: look for `test`, `vitest`, or `jest` in scripts
2. If `pytest.ini`, `setup.cfg`, or `pyproject.toml` exist: use `pytest`
3. If `go.mod` exists: use `go test ./...`
4. If `Cargo.toml` exists: use `cargo test`
5. If `Makefile` exists with test target: use `make test`

If no test command detected, ask the user:

> What command runs your tests in this project?
>
> Examples: `npm test`, `pytest`, `go test ./...`, `cargo test`

Run the full test suite:

```bash
{test_command}
```

### Gate on Test Failures

If any tests fail, **STOP immediately**:

> Tests are failing. Fix them before shipping. Run `/test` to debug.
>
> Failures:
> {failure_output}

Do not proceed to Phase 2.

### Confirm All Changes Are Ready

**GATE**: Ask the user to confirm:

> Are all changes committed or staged? Show what will be shipped:
>
> - Check `git status` above
> - Staged changes will be committed in Phase 4
> - Untracked files will be included if you confirm
>
> Proceed to review? (yes/no)

Wait for explicit confirmation.

---

## Phase 2 — PARALLEL REVIEW

Dispatch three independent review passes. Each review focuses on a specific dimension and reports only [CRITICAL] and [HIGH] issues.

Use available authorized delegation for independent reviews. If delegation is
unavailable, perform the three passes sequentially and disclose that the review
was not independent. Collect all findings before Phase 3.

### Review 1 — Code Quality and Correctness

Run the code quality review:

- Re-run the **Correctness** axis from `/review`
- Re-run the **Readability** axis from `/review`
- Focus on logic bugs, type mismatches, null handling, variable naming, and function length

Output format:

```md
## Review 1 — Code Quality

### Correctness
[findings or "No issues found"]

### Readability
[findings or "No issues found"]

### Severity: [GO / NO-GO]
```

If any [CRITICAL] or [HIGH] findings exist, mark this review as NO-GO.

### Review 2 — Security Audit

Run a deep security review:

- Re-run the **Security** axis from `/review` with extra depth
- Check for: hardcoded secrets (API keys, passwords, tokens), injection vectors, auth bypasses, CSRF/SSRF risks, path traversal, XSS vulnerabilities
- Additionally, run `git diff HEAD~1..HEAD` (or `git diff --cached` if no recent commit) and search for patterns like `password`, `secret`, `api_key`, `token`, `credential`, `.env`:

```bash
git diff HEAD~1..HEAD 2>/dev/null | grep -iE '(password|secret|api_key|token|credential|\.env|key\s*=)' || true
```

Report only [CRITICAL] and [HIGH] issues.

Output format:

```md
## Review 2 — Security Audit

[findings or "No security issues found"]

### Severity: [GO / NO-GO]
```

If any [CRITICAL] or [HIGH] findings exist, mark this review as NO-GO.

### Review 3 — Test Completeness

Verify test coverage:

- Check that every public function/method in changed files has at least one test
- Run the project's coverage tool if available:
  - Node: `npm run coverage` or similar
  - Python: `coverage run -m pytest && coverage report`
  - Go: `go test -cover ./...`
  - Rust: `cargo tarpaulin` or `cargo llvm-cov`
- Confirm the project's established coverage target is met, if one exists
- Report any untested public interfaces as [HIGH]

Output format:

```md
## Review 3 — Test Completeness

Coverage: [%] (target: project policy)

[findings or "All public interfaces are tested"]

### Severity: [GO / NO-GO]
```

If any [HIGH] findings exist (untested public interfaces) or coverage is below the project's established target, mark this review as NO-GO.

---

## Phase 3 — GO/NO-GO DECISION

Synthesize all three reviews into a decision summary:

```md
## Ship Readiness

### Review 1 — Code Quality: [GO / NO-GO]
[summary or "No blocking issues"]

### Review 2 — Security: [GO / NO-GO]
[summary or "No blocking issues"]

### Review 3 — Tests: [GO / NO-GO]
[summary or "All public interfaces tested, project coverage target met"]

### Overall Decision: [GO / NO-GO]
```

**Rules for Overall Decision:**

- If ANY review is NO-GO: overall decision is **NO-GO**
- If all reviews are GO: overall decision is **GO**

### Decision Gate

Present the decision and wait for the user's choice:

> **Decision: [GO / NO-GO]**
>
> Choose one:
>
> - **Proceed** → Commit, push, and create PR (if decision is GO)
> - **Fix and re-ship** → Address the findings, run `/test` and `/review`, then `/ship` again
> - **Override** → Ship anyway, bypassing the NO-GO decision (not recommended)

**GATE**: Confirm any delivery action not already authorized by the user.
Existing explicit authorization can satisfy the gate; do not ask again for the
same action after preparing the reviewable result.

---

## Phase 4 — SHIP (if GO or Override)

If the user chooses **Proceed** (GO) or **Override** (NO-GO), use the installed
`finishing-a-development-branch` skill when available. Otherwise verify tests,
inspect the branch and diff, and execute only the selected authorized delivery
action: commit/push/PR, local merge, or keep the branch. Do not discard work or
remove worktrees without explicit authorization.

That skill handles: verify tests → detect environment → present merge/PR/keep/discard options → execute → clean up worktree.

---

## Lifecycle Position

```text
/spec → implementation → /ship
```

`/ship` is the final stage. After shipping, run `/spec` to start the next feature.
