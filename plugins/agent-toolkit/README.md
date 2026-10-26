# agent-toolkit plugin

Meta-skills for AI agent patterns, autonomous operation, evaluation, context management, and Claude Code and Codex workspace tooling.

## Skills

| Skill | Description |
|-------|-------------|
| `autonomous-agent-harness` | Bounded recurring workflows with verified scheduling/persistence or manual execution |
| `blueprint` | Turn a one-line objective into a multi-session, multi-agent construction plan with adversarial review gate |
| `context-budget` | Audit context window consumption across agents, skills, MCP servers, and rules — identify bloat |
| `continuous-agent-loop` | Patterns for continuous autonomous agent loops with quality gates, evals, and recovery controls |
| `eval-harness` | Formal evaluation framework implementing eval-driven development (EDD) principles |
| `iterative-retrieval` | Progressive context retrieval refinement to solve the subagent context problem |
| `rules-distill` | Scan skills to extract cross-cutting principles and distill them into rule files |
| `safety-guard` | Procedural cautious-operation and directory-scoped editing guidance |
| `search-first` | Research-before-coding workflow — search for existing tools and patterns before writing custom code |
| `team-builder` | Interactive agent picker for composing and dispatching parallel agent teams |
| `verification-loop` | Comprehensive verification system for Claude Code and Codex sessions |
| `workspace-surface-audit` | Audit repo, MCP servers, plugins, env surfaces, and recommend useful collection-provided capabilities |

## Install

```sh
claude plugin marketplace add mmalyska/claude-plugins
claude plugin install agent-toolkit@mmalyska-claude-plugins
```

## Codex

After registering this repository marketplace:

```sh
codex plugin add agent-toolkit@mmalyska-claude-plugins
```

Codex loads the same `skills/` files. Invoke them with `$<plugin>:<skill-name>`. Native
Claude agent entrypoints remain Claude-specific; their role skills work in either
host. Rules are on demand, and bundled Claude hooks are disabled in Codex.
