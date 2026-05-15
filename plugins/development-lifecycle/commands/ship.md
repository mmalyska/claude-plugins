---
description: Delivery gate — parallel review, GO/NO-GO decision, PR creation
argument-hint: "[PR title, or blank to use task/spec name]"
---

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

Detect the project's test command (same as `/build` and `/test`):

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
> - Check `git status` above
> - Staged changes will be committed in Phase 4
> - Untracked files will be included if you confirm
>
> Proceed to review? (yes/no)

Wait for explicit confirmation.

---

## Phase 2 — PARALLEL REVIEW

Dispatch three independent review passes. Each review focuses on a specific dimension and reports only [CRITICAL] and [HIGH] issues.

**Run all three reviews simultaneously as parallel sub-tasks, then collect all findings before proceeding to Phase 3.**

### Review 1 — Code Quality and Correctness

Run the code quality review:
- Re-run the **Correctness** axis from `/review`
- Re-run the **Readability** axis from `/review`
- Focus on logic bugs, type mismatches, null handling, variable naming, and function length

Output format:

```
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

```
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
- Confirm coverage is ≥80%
- Report any untested public interfaces as [HIGH]

Output format:

```
## Review 3 — Test Completeness

Coverage: [%] (target: ≥80%)

[findings or "All public interfaces are tested"]

### Severity: [GO / NO-GO]
```

If any [HIGH] findings exist (untested public interfaces) or coverage is <80%, mark this review as NO-GO.

---

## Phase 3 — GO/NO-GO DECISION

Synthesize all three reviews into a decision summary:

```
## Ship Readiness

### Review 1 — Code Quality: [GO / NO-GO]
[summary or "No blocking issues"]

### Review 2 — Security: [GO / NO-GO]
[summary or "No blocking issues"]

### Review 3 — Tests: [GO / NO-GO]
[summary or "All public interfaces tested, ≥80% coverage"]

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

**GATE**: Wait for explicit user response.

---

## Phase 4 — SHIP (if GO or Override)

If the user chooses **Proceed** (and decision is GO) or **Override** (and decision is NO-GO), proceed with shipping.

### Ensure All Changes Are Committed

Run `git status` to check the current state:

```bash
git status
```

Show the user what will be staged:

> Current staged changes:
> [output of git status]

**GATE**: Check for untracked files. If any exist, ask the user:

> Include untracked files in this commit? (yes/no)

If **yes**: run `git add -A` to stage all files (tracked and untracked).
If **no**: run `git add -u` to stage only tracked files.

Then run:

```bash
git status
```

Show the user what will be committed:

> Files to commit:
> [output of git status]

### Derive Commit Message

If `$ARGUMENTS` is provided (PR title), use it as the commit summary. Otherwise, check if a spec exists:

1. Look for recent `/spec` output or a `spec.md` file in the project
2. If found, extract the feature name and use it as the commit summary
3. If not found, ask the user:

> Describe this feature in one sentence (for the commit message):

Store as `commit_message`.

Use the standard commit format:

```bash
git commit -m "feat: {commit_message}"
```

(or `fix:` if the commit is a bug fix)

### Push to Remote

Push the current branch to the remote:

```bash
git push -u origin HEAD
```

Output:

> Pushed to origin/{branch_name}

### Create PR

Attempt to create a PR using `gh`:

```bash
gh pr create --title "{PR_title}" --body "{PR_body}"
```

**PR Title**: Use `$ARGUMENTS` if provided, otherwise use the commit message.

**PR Body**: Include:
- Summary of what was built
- Test plan checklist (sample: "[ ] Run full test suite", "[ ] Verify coverage ≥80%", "[ ] Manual testing on [platform]")
- Link to spec if it exists (e.g., "See /spec output for requirements")

**If `gh` is unavailable or fails**, print the manual push command instead:

> GitHub CLI not available. To create a PR manually:
> 
> ```bash
> {output from git push}
> ```
> 
> Then open: https://github.com/{owner}/{repo}/compare/{branch_name}

### Final Confirmation

> PR created: {PR_URL}
> 
> Feature shipped. Run `/spec` to start the next feature.

---

## Lifecycle Position

/spec → /plan → loop(/build → /test → /review → /simplify) → /ship

/ship is the final stage. After shipping, run /spec to start the next feature.
