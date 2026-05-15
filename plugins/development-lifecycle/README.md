# development-lifecycle

Full development lifecycle agents, commands, and rules for Claude Code.

## Agents

- `architect` — System design and architectural decisions
- `build-error-resolver` — Fix build/type errors
- `code-reviewer` — Code quality, security, maintainability
- `doc-updater` — Update codemaps and documentation
- `docs-lookup` — Fetch current library docs via Context7
- `planner` — Implementation planning for complex features
- `tdd-guide` — Test-driven development enforcement

## Commands

- `/prp-prd` — Interactive PRD generator
- `/prp-plan` — Create feature implementation plan
- `/prp-implement` — Execute an implementation plan
- `/code-review` — Review local changes or a GitHub PR
- `/plan` — Restate requirements and create implementation plan
- `/aside` — Simplify and refine recently changed code
- `/update-docs` — Update project documentation
- `/update-codemaps` — Update CODEMAPS files
- `/skill-create` — Create a new skill
- `/learn-eval` — Evaluate and learn from session

## Lifecycle Commands

A structured 7-stage workflow for feature development:

```
/spec → /plan → loop(/build → /test → /review → /simplify) → /ship
```

| Command | Stage | Description |
|---------|-------|-------------|
| `/spec` | 1 | Define the problem — interactive spec with verification gate |
| `/plan` | 2 | Break work into tasks (existing command) |
| `/build` | loop | Implement one task — TDD red/green cycle, commit |
| `/test` | loop | TDD workflow — red/green for features, Prove-It for bugs |
| `/review` | loop | Five-axis code review — correctness, readability, arch, security, perf |
| `/simplify` | loop | Reduce complexity — guard clauses, extract helpers, name constants |
| `/ship` | 7 | Delivery gate — parallel review, GO/NO-GO, PR creation |

## Rules

Common coding standards loaded into every session: coding style, testing, security, performance, hooks, patterns, code review, agent orchestration.

## Install

```sh
claude plugin install development-lifecycle@mmalyska/claude-plugins
```
