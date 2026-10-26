# Development Workflow

> This file extends [common/git-workflow.md](./git-workflow.md) with the full feature development process that happens before git operations.

The Feature Implementation Workflow describes the development pipeline: research, planning, TDD, code review, and then committing to git.

Use available connected tools for research; if GitHub CLI, Context7, or Exa is
absent, use local code search and accessible primary documentation. Do not
install external tools implicitly. Keep commit, push, and review-request actions
within the user's explicit delivery scope.

## Feature Implementation Workflow

0. **Research & Reuse** _(mandatory before any new implementation)_
   - **GitHub code search first:** Run `gh search repos` and `gh search code` to find existing implementations, templates, and patterns before writing anything new.
   - **Library docs second:** Use Context7 or primary vendor docs to confirm API behavior, package usage, and version-specific details before implementing.
   - **Exa only when the first two are insufficient:** Use Exa for broader web research or discovery after GitHub search and primary docs.
   - **Check package registries:** Search npm, PyPI, crates.io, and other registries before writing utility code. Prefer battle-tested libraries over hand-rolled solutions.
   - **Search for adaptable implementations:** Look for open-source projects that solve 80%+ of the problem and can be forked, ported, or wrapped.
   - Prefer adopting or porting a proven approach over writing net-new code when it meets the requirement.

1. **Create the Worktree** _(before any implementation)_
   - Use the `using-git-worktrees` skill. The primary checkout is never a
     workspace — see [worktree-workflow.md](./worktree-workflow.md).
   - Branch as `<type>/<slug>`; the worktree lands at `.worktrees/<type>/<slug>`.

2. **Plan First**
   - Create an implementation plan; use an available authorized planner role when helpful
   - Generate planning docs before coding: PRD, architecture, system_design, tech_doc, task_list
   - Identify dependencies and risks
   - Break down into phases

3. **TDD Approach**
   - Use available TDD guidance or perform RED-GREEN-REFACTOR directly
   - Write tests first (RED)
   - Implement to pass tests (GREEN)
   - Refactor (IMPROVE)
   - Verify the project's established coverage target and relevant changed behavior

4. **Code Review**
   - Use an available authorized code-reviewer role or perform a separate local review pass
   - Address CRITICAL and HIGH issues
   - Fix MEDIUM issues when possible

5. **Commit & Push**
   - Detailed commit messages
   - Follow conventional commits format
   - See [git-workflow.md](./git-workflow.md) for commit message format and PR process

6. **Pre-Review Checks**
   - Verify all automated checks (CI/CD) are passing
   - Resolve any merge conflicts
   - Ensure branch is up to date with target branch
   - Only request review after these checks pass
