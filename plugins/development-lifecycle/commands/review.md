---
description: Five-axis code review — correctness, readability, architecture, security, performance
argument-hint: "[file or directory to review, or blank to review recent changes]"
---

# /review - Five-Axis Code Review

Run a comprehensive review across five quality dimensions: correctness, readability, architecture, security, and performance. Produces prioritized findings, then waits for your decision on which to fix.

---

## Phase 1 — SCOPE

### Determine Target Files

**If `$ARGUMENTS` is provided:**
- Check if it names a file or directory
- If file: include only that file
- If directory: include all source files in that directory (recursively); exclude `node_modules`, `dist`, `.git`, build artifacts, and binary files — include files with source extensions (`.ts`, `.js`, `.py`, `.go`, `.rs`, `.cs`, etc.)

**If `$ARGUMENTS` is empty or unspecified:**
- Run: `git diff HEAD~1..HEAD` to get files changed in the last commit
- If that returns nothing, try: `git diff --cached` to get staged changes
- If still nothing, ask the user to specify a file or commit a change first

### Present Scope to User

> Files to review:
> - [list each file with line count]
>
> Total: [N] files

**GATE**: If no changed files are found:

> No changed files found. Please provide:
> - A file path (e.g., `src/mycomponent.ts`)
> - A directory (e.g., `src/services/`)
> - Or commit some changes and run `/review` again

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

```
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

**If no findings exist:**

> No issues found. Code looks good.

### Ordering Within Each Severity

Order findings within each severity group by:
1. Axis (Correctness first, then Readability, Architecture, Security, Performance)
2. Line number (ascending)

---

## Phase 4 — DECISION GATE

After presenting the findings, ask:

> How would you like to proceed?
>
> - **Fix all CRITICAL/HIGH** — I'll apply the recommended fixes
> - **Fix specific items** — List the line numbers or item numbers (e.g., "1, 3, 5")
> - **Skip** — Proceed without making changes

**GATE**: Wait for the user's explicit decision. Do not proceed until they respond.

### Apply Fixes (if user selects fix option)

For each item the user approves:

1. Re-read the current file (line numbers may have shifted from earlier edits)
2. Locate the relevant code by searching for the context, not relying on the original line number
3. Apply the fix based on the review finding
3. Follow the coding style rules in `~/.claude/rules/`

After all fixes are applied:

4. Run the project's test suite to verify nothing broke
5. Show a summary of what changed:

```
## Applied Fixes

- [file:line] [Axis] — Description of the fix applied
- [file:line] [Axis] — Description of the fix applied

### Test Results
[Test suite output or "All tests passed"]
```

---

## Lifecycle Position

```text
/spec → superpowers execution → /review → /ship
```

After review, fix findings and run `/ship` when ready.
