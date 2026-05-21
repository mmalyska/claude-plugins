# development-lifecycle

Extension to [superpowers](https://github.com/obra/superpowers) — agents, commands, and rules for Claude Code. Relies on superpowers for the core workflow; adds project-specific agents, quality commands, and coding standards.

## Lifecycle

Skill-driven (superpowers handles the flow; these commands are entry points and quality gates):

```text
/spec → superpowers execution → /ship
```

| Command       | Stage                   | Delegates to                                                               |
|---------------|-------------------------|----------------------------------------------------------------------------|
| `/spec`       | Define the problem      | `superpowers:brainstorming` → `superpowers:writing-plans`                  |
| _(execution)_ | Implement task-by-task  | `superpowers:subagent-driven-development` or `superpowers:executing-plans` |
| `/ship`       | Quality gate + delivery | `superpowers:finishing-a-development-branch`                               |

## Quality Commands

Standalone commands that add value on top of the superpowers flow:

| Command            | Description                                                                           |
|--------------------|---------------------------------------------------------------------------------------|
| `/review`          | Five-axis code review — correctness, readability, architecture, security, performance |
| `/test fix: {bug}` | Bug fix TDD — Prove-It pattern (write reproducing test, fix, coverage check)          |
| `/code-review`     | GitHub PR review via `gh` — posts inline comments and approve/request-changes         |
| `/aside`           | Answer a quick side question without losing current task context                      |

## Utility Commands

| Command            | Description                                                   |
|--------------------|---------------------------------------------------------------|
| `/learn-eval`      | Extract reusable patterns from the session and save as skills |
| `/skill-create`    | Analyze git history to generate SKILL.md files                |
| `/update-docs`     | Sync documentation with codebase                              |
| `/update-codemaps` | Generate token-lean architecture docs in `docs/CODEMAPS/`     |

## Agents

Specialized subagents invoked by commands and skills:

| Agent                  | Description                                  |
|------------------------|----------------------------------------------|
| `architect`            | System design and architectural decisions    |
| `build-error-resolver` | Fix build/type errors with minimal diffs     |
| `code-reviewer`        | Code quality, security, maintainability      |
| `doc-updater`          | Update codemaps and documentation            |
| `docs-lookup`          | Fetch current library docs via Context7      |
| `tdd-guide`            | Test-driven development enforcement          |

## Skills

| Skill                           | Description                                                                   |
|---------------------------------|-------------------------------------------------------------------------------|
| `ai-regression-testing`         | AI-specific regression test patterns                                          |
| `architecture-decision-records` | Write and maintain ADRs                                                       |
| `claude-devfleet`               | Multi-agent fleet coordination                                                |
| `e2e-testing`                   | End-to-end testing patterns                                                   |
| `simplify`                      | Auto-applied after review or before ship — guard clauses, helpers, constants  |

## Rules

Common coding standards loaded into every session: coding style, testing, security, performance, hooks, patterns, code review, agent orchestration.

## Install

```sh
claude plugin install development-lifecycle@mmalyska/claude-plugins
```
