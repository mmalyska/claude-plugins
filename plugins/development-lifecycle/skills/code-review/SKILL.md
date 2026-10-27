---
name: code-review
description: "Code review — local uncommitted changes or GitHub PR (pass PR number/URL for PR mode)"
---

# Code Review

Read [the workflow contract](../../rules/common/workflow.md) first. Select profile
and topology independently; default STANDARD + SOLO. Apply mandatory project
policy in every profile. This procedure does not authorize another actor or
work beyond the requested stage.

Use the current user request as input. In a Claude command invocation, `$ARGUMENTS` carries that input; in Codex, use the text accompanying the skill.
Command-style examples below name workflows: in Codex select the corresponding
installed skill (`$plugin:skill`); do not execute slash commands in a shell.

> PR review mode adapted from PRPs-agentic-eng by Wirasm. Part of the PRP workflow series.

**Input**: $ARGUMENTS

---

## Mode Selection

If `$ARGUMENTS` contains a PR number, PR URL, or `--pr`:
→ Jump to **PR Review Mode** below.

Otherwise:
→ Use **Local Review Mode**.

---

## Local Review Mode

Use [review](../review/SKILL.md) for profile-sized scope selection and axes and
[common review policy](../../rules/common/code-review.md) for project gates. This
entrypoint adds local/PR transport and reports; it does not require another actor.

### Phase 1 — GATHER

```bash
git diff --name-only
git diff --cached --name-only
git ls-files --others --exclude-standard
```

Inspect task-relevant untracked files without staging them. For a clean working
tree use the actual base comparison or explicit revision as described in
[review](../review/SKILL.md); report no changes if no target matches.

### Phase 2 — REVIEW

Read each changed file in full. Check for:

**Security Issues (CRITICAL):**

- Hardcoded credentials, API keys, tokens
- SQL injection vulnerabilities
- XSS vulnerabilities
- Missing input validation
- Insecure dependencies
- Path traversal risks

**Code Quality (HIGH):**

- Functions > 50 lines
- Files > 800 lines
- Nesting depth > 4 levels
- Missing error handling
- console.log statements
- TODO/FIXME comments
- Missing JSDoc for public APIs

**Best Practices (MEDIUM):**

- Mutation patterns (use immutable instead)
- Emoji usage in code/comments
- Missing tests for new code
- Accessibility issues (a11y)

### Phase 3 — REPORT

Generate report with:

- Severity: CRITICAL, HIGH, MEDIUM, LOW
- File location and line numbers
- Issue description
- Suggested fix

Block commit if CRITICAL or HIGH issues found.
Never approve code with security vulnerabilities.

---

## PR Review Mode

PR review fetches diff, reads relevant full files, runs permitted validation and
produces a local report. A PR number alone does not authorize publication.

### Phase 1 — FETCH

Parse input to determine PR:

| Input | Action |
| --- | --- |
| Number (e.g. `42`) | Use as PR number |
| URL (`github.com/.../pull/42`) | Extract PR number |
| Branch name | Find PR via `gh pr list --head <branch>` |

```bash
gh pr view <NUMBER> --json number,title,body,author,baseRefName,headRefName,changedFiles,additions,deletions
gh pr diff <NUMBER>
```

If PR not found, stop with error. Store PR metadata for later phases.

### Phase 2 — CONTEXT

Build review context:

1. **Project rules** — Read applicable shared `AGENTS.md` first in either host, then host adapters, project documentation and contributing guidelines; surface conflicts
2. **PRP artifacts** — Check existing `.reports/agent-workflows/` artifacts, `.claude/PRPs/reports/`, and `.claude/PRPs/plans/` for implementation context related to this PR
3. **PR intent** — Parse PR description for goals, linked issues, test plans
4. **Changed files** — List all modified files and categorize by type (source, test, config, docs)

### Phase 3 — REVIEW

Read each changed file **in full** (not just the diff hunks — you need surrounding context).

For PR reviews, fetch the full file contents at the PR head revision:

```bash
gh pr diff <NUMBER> --name-only | while IFS= read -r file; do
  gh api "repos/{owner}/{repo}/contents/$file?ref=<head-branch>" --jq '.content' | base64 -d
done
```

Apply the review checklist across 7 categories:

| Category | What to Check |
| --- | --- |
| **Correctness** | Logic errors, off-by-ones, null handling, edge cases, race conditions |
| **Type Safety** | Type mismatches, unsafe casts, `any` usage, missing generics |
| **Pattern Compliance** | Matches project conventions (naming, file structure, error handling, imports) |
| **Security** | Injection, auth gaps, secret exposure, SSRF, path traversal, XSS |
| **Performance** | N+1 queries, missing indexes, unbounded loops, memory leaks, large payloads |
| **Completeness** | Missing tests, missing error handling, incomplete migrations, missing docs |
| **Maintainability** | Dead code, magic numbers, deep nesting, unclear naming, missing types |

Assign severity to each finding:

| Severity | Meaning | Action |
| --- | --- | --- |
| **CRITICAL** | Security vulnerability or data loss risk | Must fix before merge |
| **HIGH** | Bug or logic error likely to cause issues | Should fix before merge |
| **MEDIUM** | Code quality issue or missing best practice | Fix recommended |
| **LOW** | Style nit or minor suggestion | Optional |

### Phase 4 — VALIDATE

Run available validation commands:

Detect the project type from config files (`package.json`, `Cargo.toml`, `go.mod`, `pyproject.toml`, etc.), then run the appropriate commands:

**Node.js / TypeScript** (configured `package.json` scripts, run only those present):

```bash
npm run typecheck  # Existing configured script; no implicit package fetch
npm run lint                                                    # Lint
npm test                                                        # Tests
npm run build                                                   # Build
```

**Rust** (has `Cargo.toml`):

```bash
cargo clippy -- -D warnings  # Lint
cargo test                   # Tests
cargo build                  # Build
```

**Go** (has `go.mod`):

```bash
go vet ./...    # Lint
go test ./...   # Tests
go build ./...  # Build
```

**Python** (has `pyproject.toml` / `setup.py`):

```bash
pytest  # Tests
```

For a repository unittest suite, use its documented discovery command, such as
`python3 -B -m unittest discover -s tests`. Inspect side effects and session scope
first: some discovery tests start other harnesses. Run only installed/configured
commands applicable to the changed behavior and project gates. Record real exit
status; report unavailable checks as NOT RUN and unrelated ones NOT APPLICABLE.
Never fetch tools implicitly or run a forbidden harness to validate a review.

### Phase 5 — DECIDE

Form recommendation based on findings:

| Condition | Decision |
| --- | --- |
| Zero CRITICAL/HIGH issues, validation passes | **APPROVE** |
| Only MEDIUM/LOW issues, validation passes | **APPROVE** with comments |
| Any HIGH issues or validation failures | **REQUEST CHANGES** |
| Any CRITICAL issues | **BLOCK** — must fix before merge |

Special cases:

- Draft PR → Always use **COMMENT** (not approve/block)
- Only docs/config changes → Lighter review, focus on correctness
- `--approve` / `--request-changes` cannot override mandatory gates. Determine
  whether the user requested an external event or only a local recommendation
  before publication; report all findings.

### Phase 6 — REPORT

Preserve the existing review directory when resuming. Otherwise create the
review artifact at `.reports/agent-workflows/reviews/pr-<NUMBER>-review.md`:

```markdown
# PR Review: #<NUMBER> — <TITLE>

**Reviewed**: <date>
**Author**: <author>
**Branch**: <head> → <base>
**Decision**: APPROVE | REQUEST CHANGES | BLOCK

## Summary
<1-2 sentence overall assessment>

## Findings

### CRITICAL
<findings or "None">

### HIGH
<findings or "None">

### MEDIUM
<findings or "None">

### LOW
<findings or "None">

## Validation Results

| Check | Result |
|---|---|
| Type check | Pass / Fail / Skipped |
| Lint | Pass / Fail / Skipped |
| Tests | Pass / Fail / Skipped |
| Build | Pass / Fail / Skipped |

## Files Reviewed
<list of files with change type: Added/Modified/Deleted>
```

### Phase 7 — PUBLISH

Only publish when the current user request explicitly authorizes external review
publication. A local report, PR number, GO recommendation or PR-creation request
is not that authority. An explicit request to post this review or approve/request
changes on the verified PR can supply it; reuse accepted authority for the same
event/target/content without another permission menu. If not authorized, stop with
the local artifact. No publication implies merge or deployment.

Readiness alone authorizes no commit, push, PR, review publication, merge or runtime mutation.
No blanket override may bypass mandatory safety or project gates.
A GitOps/HCP auto-apply merge is runtime mutation and needs separate fresh explicit authorization with impact and rollback.

Use an available sufficient GitHub tool, otherwise the configured CLI. Prepare the
actual findings and event for review before requesting missing authority, without
changing code or publishing as an implicit side effect. For an authorized CLI
review, use a body file and inspect the response:

```bash
gh pr review <verified-PR> --approve --body-file <prepared-review-file>
# Or the specifically authorized --request-changes / --comment event.
```

The example is not a command to execute automatically. Report the actual review
identifier/result, or failure/NOT RUN; never claim publication from local readiness.

### Phase 8 — OUTPUT

Report to user:

```text
PR #<NUMBER>: <TITLE>
Decision: <APPROVE|REQUEST_CHANGES|BLOCK>

Issues: <critical_count> critical, <high_count> high, <medium_count> medium, <low_count> low
Validation: <pass_count>/<total_count> checks passed

Artifacts:
  Review: .reports/agent-workflows/reviews/pr-<NUMBER>-review.md
  GitHub: <PR URL>

Next steps:
  - <contextual suggestions based on decision>
```

---

## Edge Cases

- **No `gh` CLI**: Fall back to local-only review (read the diff, skip GitHub publish). Warn user.
- **Diverged branches**: Suggest `git fetch origin && git rebase origin/<base>` before review.
- **Large PRs (>50 files)**: Warn about review scope. Focus on source changes first, then tests, then config/docs.
