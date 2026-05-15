# agent-toolkit plugin

Meta-skills for AI agent patterns, autonomous operation, evaluation, context management, and Claude Code workspace tooling.

## Skills

| Skill | Description |
|-------|-------------|
| `autonomous-agent-harness` | Persistent memory, scheduled ops, computer use, and task queuing for fully autonomous Claude Code operation |
| `blueprint` | Turn a one-line objective into a multi-session, multi-agent construction plan with adversarial review gate |
| `context-budget` | Audit context window consumption across agents, skills, MCP servers, and rules — identify bloat |
| `continuous-agent-loop` | Patterns for continuous autonomous agent loops with quality gates, evals, and recovery controls |
| `eval-harness` | Formal evaluation framework implementing eval-driven development (EDD) principles |
| `iterative-retrieval` | Progressive context retrieval refinement to solve the subagent context problem |
| `rules-distill` | Scan skills to extract cross-cutting principles and distill them into rule files |
| `safety-guard` | Prevent destructive operations when working on production systems or running agents autonomously |
| `search-first` | Research-before-coding workflow — search for existing tools and patterns before writing custom code |
| `team-builder` | Interactive agent picker for composing and dispatching parallel agent teams |
| `verification-loop` | Comprehensive verification system for Claude Code sessions |
| `workspace-surface-audit` | Audit repo, MCP servers, plugins, env surfaces, and recommend highest-value ECC-native capabilities |

## Install

```sh
claude plugin add marketplace github:mmalyska/claude-plugins
claude plugin install agent-toolkit@mmalyska/claude-plugins
```
