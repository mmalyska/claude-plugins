---
description: Implement the next task — TDD red/green cycle, then commit
argument-hint: [task name or number, or blank to pick next pending]
---

# Build Command

Implement one task using test-driven development. Pick the next pending task, write a failing test (RED), implement the minimal code (GREEN), verify the full test suite passes, ensure the build compiles, then commit.

**Input**: $ARGUMENTS (optional task name or number; blank to pick next pending)

---

## Phase 1 — LOAD TASK

Locate the plan file:
1. Check `docs/superpowers/plans/*.md` for the most recent plan
2. If not found, check `tasks/todo.md` or similar task files
3. If neither exists, stop with: "No plan found. Run `/plan` to create one first."

If `$ARGUMENTS` is provided:
- Search the plan for a task matching the name or number
- If found, load that task
- If not found, stop: "Task '{$ARGUMENTS}' not found in plan."

If `$ARGUMENTS` is blank:
- Scan the plan for the first task marked as `[ ]` (unchecked)
- Load that task

Show the task to the user:

> **Task**: {task_name}
> 
> **Acceptance Criteria**:
> {acceptance_criteria_from_plan}
> 
> **Files**: {files_list}
> 
> Starting implementation...

**GATE**: If no pending tasks remain, stop with:

> All tasks complete. Run `/ship` to finish.

Otherwise, proceed to Phase 2.

---

## Phase 2 — LOAD CONTEXT

Read each file listed in the task's "Files:" section. For each file:
- If it exists, read it in full
- Note the language/framework (TypeScript, Python, Go, Rust, etc.)
- Check the project structure for existing patterns (test framework, directory layout, naming conventions)

**Fallback if no Files section**: If the task has no "Files:" section or it is empty, search the codebase for files likely related to the task name and acceptance criteria. Show the candidates to the user and ask for confirmation before proceeding.

Detect the test framework:
- JavaScript/TypeScript: Check `package.json` for test script, look for `jest`, `vitest`, `mocha`, `playwright`
- Python: Look for `pytest.ini`, `setup.cfg`, or `pyproject.toml`
- Go: Look for `*_test.go` files (standard `testing` package)
- Rust: Look for `#[cfg(test)]` or `tests/` directory
- Other: Ask the user: "What test framework does this project use?"

Store the test command for later (e.g. `npm test`, `pytest`, `go test ./...`, `cargo test`).

**Regression Baseline**: Run the full test suite once and record which tests are currently passing. Store this as the baseline. Phase 5 will compare against this baseline to detect regressions.

```
{test_command}
```

> Baseline recorded: {pass_count} tests passing

---

## Phase 3 — RED (Write Failing Test)

Write a test that validates the task's acceptance criteria. Place it in the appropriate test location:
- For TypeScript/JavaScript: `src/` or `tests/` directory, matching the source file name with `.test.ts` or `.spec.ts` suffix
- For Python: Same directory or `tests/` folder with `test_` prefix
- For Go: `*_test.go` file in the same package
- For Rust: `#[cfg(test)]` module or `tests/` directory

**Match existing conventions**: If the project has existing tests, match the directory and naming convention of the nearest existing test file instead of applying the default placement rules above.

The test must:
- Be specific to the acceptance criteria
- Exercise the exact behavior the task requests
- Fail with a clear error message when run

Run the test with the detected test command:

```
{test_command}
```

Confirm the failure:

> Test failed as expected (RED phase complete):
> 
> {failure_output}

**Verify the failure is semantic**: Confirm the test failure is due to missing behavior (the feature does not exist yet), not a compilation error, import error, or test setup error. If it's a setup error (missing imports, broken test framework config), fix the import or setup first before considering RED complete.

**GATE**: If the test passes unexpectedly, skip to Phase 5:

> Test already passes — behavior exists. Skipping to Phase 5.

Otherwise, proceed to Phase 4.

---

## Phase 4 — GREEN (Implement)

Write the minimal code required to make the test pass. Do NOT:
- Add features beyond the acceptance criteria
- Over-engineer or refactor
- Write code you don't need yet

Implement the code in the file(s) listed in the task. Run the test again:

```
{test_command}
```

Confirm the pass:

> Test passes (GREEN phase complete):
> 
> {test_output_showing_pass}

**GATE**: If the test still fails, show the failure and ask:

> Test still failing. Revise the implementation or test?

Wait for the user to clarify, then fix and rerun.

---

## Phase 5 — REGRESSION CHECK

Run the full test suite to ensure no pre-existing tests broke. Compare against the baseline from Phase 2:

```
{test_command}
```

Report results:

> Full suite status:
> - {pass_count} tests passing
> - {fail_count} tests failing

**GATE**: If any test fails that was passing before (regression), stop:

> Regression detected: {failing_test_names}
> 
> Fix the implementation to restore the test(s).

**Do NOT modify existing tests**: Do NOT modify or delete a previously-passing test to clear the regression gate. Fix the implementation instead. If the existing test appears wrong, stop and ask the user before proceeding.

Fix the implementation, rerun the full suite, then proceed to Phase 6 only when all tests pass.

---

## Phase 6 — BUILD CHECK

Detect the build command from the project:
- Node.js/TypeScript: `npm run build` or `pnpm build` or `yarn build`
- Python: `python -m build` (or project-specific command; if `pyproject.toml` has no `[build-system]` section, skip the build check for Python projects)
- Go: `go build ./...`
- Rust: `cargo build`
- Other: Ask the user: "What is the build command?"

Run the build:

```
{build_command}
```

Report results:

> Build status: ✓ Success

**GATE**: If the build fails, show the error:

> Build failed:
> 
> {build_error_output}
> 
> Fix the error, rerun tests, then rerun build.

Fix the code, rerun the full test suite (Phase 5), then rerun build. Once the build passes, proceed to Phase 7.

---

## Phase 7 — COMMIT

Update the plan file to mark the task as complete. Find the task line and change:

```
- [ ] Task Name
```

to:

```
- [x] Task Name
```

Stage the task files and the updated plan file:

```bash
git add {files_changed_for_this_task} {plan_file_path}
```

Commit with a descriptive message following conventional commits format. Infer the type from the task intent:
- `fix:` for bug fixes
- `test:` for test-only tasks
- `refactor:` for cleanup/refactoring
- `feat:` (default) for new behavior

```bash
git commit -m "{type}: {task_name_in_lower_case}"
```

Example commit messages:
```
feat: add user authentication with jwt tokens
fix: correct off-by-one error in pagination
test: add integration tests for user service
refactor: extract validation logic to utility
```

Show the user:

> Committed:
> 
> {git_commit_output}
>
> Files staged: {list_of_files}
> 
> Message: {type}: {task_name}

---

## Phase 8 — FINAL STATUS

Print final status:

> Task complete.
> 
> - Run `/build` again for the next task
> - Run `/test` to run the full test suite
> - Run `/review` to review the code quality
> - Run `/simplify` to clean up after multiple tasks

Do NOT auto-continue to the next task. Wait for the user to run `/build` again.

---

## Lifecycle Position

```
/spec → /plan → loop(/build → /test → /review → /simplify) → /ship
```

This command implements one task using TDD (red → green → regression → build → commit). Run `/build` again for the next pending task. After a batch of tasks, run `/review` for quality check, `/simplify` to clean up, then `/ship` when all tasks are complete.
