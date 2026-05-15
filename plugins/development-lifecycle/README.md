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

## Rules

Common coding standards loaded into every session: coding style, testing, security, performance, hooks, patterns, code review, agent orchestration.

## Install

```sh
claude plugin install development-lifecycle@mmalyska/claude-plugins
```
