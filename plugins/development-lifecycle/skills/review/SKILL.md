---
name: review
description: "Five-axis code review — correctness, readability, architecture, security, performance"
---

# /review - Five-Axis Code Review

Read [the workflow contract](../../rules/common/workflow.md) first. Select profile
and topology independently; default STANDARD + SOLO. Apply mandatory project
policy in every profile. This procedure does not authorize another actor or
work beyond the requested stage.

Use the current user request as input. In a Claude command invocation, `$ARGUMENTS` carries that input; in Codex, use the text accompanying the skill.
Command-style examples below name workflows: in Codex select the corresponding
installed skill (`$plugin:skill`); do not execute slash commands in a shell.

Use the five axes below at the depth selected by the workflow contract: QUICK
focused self-review, STANDARD full self-review or separate local pass, DEEP a
separate deliberate pass with evidence. SOLO does not add a reviewer agent.
Apply [common review policy](../../rules/common/code-review.md). For a relevant
security/language/framework check, read the matching section of
[domain checks](../code-reviewer/references/domain-checks.md); the reviewer
procedure is not a prerequisite. Preserve task scope and project gates. Produce findings first; edits require existing or new fix authority.

---

## Phase 1 — SCOPE

### Determine Target Files

Honor an explicit file, directory, revision, range or PR target first. Include
relevant documentation/configuration as well as source; exclude binaries, build
outputs and vendored/generated files unless explicitly in scope.

Without an explicit target, inspect current work before commit history:

```bash
git diff --name-only
git diff --cached --name-only
git ls-files --others --exclude-standard
```

Read both unstaged and staged diffs; an aggregate `git diff HEAD` alone can hide
opposing staged/unstaged edits. Inspect task-relevant untracked files without
staging them. If the working tree is clean, resolve the actual base branch and
use `git diff <base>...HEAD` for committed task changes. Only inspect a recent
commit when it is the intended task target. If nothing matches, report no changes
or ask for a target; never require a commit merely to conduct review.

### Present Scope to User

> Files to review:
>
> - [list each file with line count]
>
> Total: [N] files

**GATE**: If no changed files are found:

> No changed files found. Please provide:
>
> - A file path (e.g., `src/mycomponent.ts`)
> - A directory (e.g., `src/services/`)
> - Or a revision/range to inspect

---

## Phase 2 — FIVE-AXIS REVIEW

Run each axis in sequence. For every issue found, assign **one severity** (`[CRITICAL]`, `[HIGH]`, `[MEDIUM]`, `[LOW]`) and the **axis name**. Collect all findings as you go.

### Axis 1 — Correctness

Look for logic bugs, off-by-one errors, type mismatches, null/undefined handling, and edge cases.

**Focus areas:**

- Branching logic that may miss cases
- Array/collection indexing that could go out of bounds
- Null checks missing where data could be undefined
- Assumptions about data types that API contracts don't guarantee
- Edge cases not covered by existing tests

**Example findings:**

- `[CRITICAL] file.ts:45` — condition never true due to precedence error
- `[HIGH] file.ts:120` — array access without bounds check
- `[MEDIUM] file.ts:87` — missing null check before property access

### Axis 2 — Readability

Look for unclear variable names, overly complex logic, deep nesting, and missing comments where intent is not obvious.

**Focus areas:**

- Variable and function names that obscure intent
- Functions longer than ~50 lines (suggest splitting)
- Nesting depth greater than 4 levels (suggest early returns or helper functions)
- Complex boolean expressions that could be extracted to a named variable
- Magic numbers that should be named constants
- Comments that are missing where code intent is unclear

**Example findings:**

- `[MEDIUM] file.ts:30-60` — function is 31 lines, consider splitting by responsibility
- `[LOW] file.ts:15` — variable `x` is not descriptive; suggest `remainingRetries`
- `[MEDIUM] file.ts:88` — nested if/else is 5 levels deep; suggest early return pattern

### Axis 3 — Architecture

Look for tight coupling, misplaced responsibilities, and patterns that diverge from codebase conventions without good reason.

**Focus areas:**

- Tight coupling that will make future changes hard (e.g., mixing concerns)
- Responsibilities that belong in a different layer or module
- Imports or dependencies that break layering
- Patterns that diverge from the rest of the codebase without clear justification
- Circular dependencies or reverse dependencies

**Example findings:**

- `[HIGH] file.ts:12` — UI component imports business logic directly; should use a service abstraction
- `[MEDIUM] file.ts:50` — controller performs database query; should delegate to repository layer
- `[HIGH] file.ts:5-8` — circular dependency with `module-b`

### Axis 4 — Security

Look for unvalidated inputs, hardcoded secrets, injection vulnerabilities, and missing authentication checks.

**Focus areas:**

- User input that reaches external systems without validation
- Hardcoded credentials, API keys, tokens, or secrets
- SQL injection risk (string concatenation in queries)
- XSS risk (unescaped HTML or unsanitized user input)
- Path traversal risk (unsanitized file paths)
- SSRF risk (unvalidated URLs)
- Over-broad permissions or missing auth checks
- Deserialization of untrusted data

**Example findings:**

- `[CRITICAL] file.ts:35` — hardcoded API key found; move to environment variable
- `[CRITICAL] file.ts:60` — user input passed directly to SQL query; use parameterized query
- `[HIGH] file.ts:90` — missing CSRF token validation on state-changing endpoint
- `[HIGH] file.ts:15` — file path not validated before use; risk of directory traversal

### Axis 5 — Performance

Look for N+1 queries, repeated expensive operations in loops, missing pagination, and inefficient algorithms.

**Focus areas:**

- N+1 queries (loop with database query inside)
- Repeated expensive operations in loops (API calls, file reads, parsing)
- Missing pagination on unbounded result sets
- Blocking I/O in async/event-driven code
- Memory leaks or unbounded buffer growth
- Inefficient algorithms with high time complexity
- Unused imports or dead code that could slow build/parse time

**Example findings:**

- `[HIGH] file.ts:40-45` — loop makes database query on each iteration; use batch query or JOIN
- `[MEDIUM] file.ts:78` — missing pagination on results; could fetch millions of rows
- `[MEDIUM] file.ts:120` — blocking I/O in async function; use Promise-based API
- `[LOW] file.ts:5` — unused import `lodash` slows build time

---

## Phase 3 — PRIORITISED FINDINGS

After reviewing all axes, produce a summary with findings grouped by severity and tagged with axis name.

### Format

```text
## Review findings

### CRITICAL
- [file:line] [Axis] — Description and why it matters

### HIGH
- [file:line] [Axis] — Description and why it matters

### MEDIUM
- [file:line] [Axis] — Description

### LOW
- [file:line] [Axis] — Description
```

**If no findings exist:** report no findings in the reviewed scope and state
verification limits; do not imply unrun checks passed.

### Ordering Within Each Severity

Order findings within each severity group by:

1. Axis (Correctness first, then Readability, Architecture, Security, Performance)
2. Line number (ascending)

---

## Phase 4 — DECISION GATE

Present the findings. If fixes are already authorized, apply only those within
the accepted scope; otherwise ask which findings to fix and wait before edits.
Review-only requests produce a report without implicit remediation or delivery.
A user's choice to skip fixes cannot waive mandatory security/project gates.

### Apply Fixes (if user selects fix option)

For each item the user approves:

1. Re-read the current file (line numbers may have shifted from earlier edits)
2. Locate the relevant code by searching for the context, not relying on the original line number
3. Apply the fix based on the review finding
4. Follow applicable project instructions and the active host's loaded rules

After all fixes are applied:

1. Run affected checks and mandatory project gates; report NOT RUN where unavailable
2. Show a summary of what changed:

```text
## Applied Fixes

- [file:line] [Axis] — Description of the fix applied
- [file:line] [Axis] — Description of the fix applied

### Test Results
[Test suite output or "All tests passed"]
```

---

## Lifecycle Position

Follow [the workflow contract](../../rules/common/workflow.md). Review informs
Simplify; rerun affected checks after edits before Ship readiness. Review alone
does not authorize delivery.

## Reuse loaded guidance

Reuse a complete contract already read from this installed revision while its
content remains available. After compaction/context loss or a relevant source or
policy change, read it fully again before dependent work. A summary or partial
read does not establish first-use loading.
