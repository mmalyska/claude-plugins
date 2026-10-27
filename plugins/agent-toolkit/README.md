# agent-toolkit plugin

Meta-skills for AI agent patterns, autonomous operation, evaluation, context management, and Claude Code and Codex workspace tooling.

## Execution contract

Default STANDARD + SOLO: use local role passes and the existing shared engineering
lifecycle. Profiles change depth; HANDOFF/PARALLEL/REVIEW change actors only after
explicit user authorization. Check authority before actual exposed capability.
Planning, a role selection or an independent task graph is not launch authority.
No other CLI/service may bypass a restriction; disclose missing capability and
use local/manual paths only when compatible with intent. External service jobs,
schedules, auto-dispatch, integration, merge and runtime require their own scope.

The toolkit remains usable alone; consult the existing development-lifecycle-rules
contract when installed, without copying skills or requiring Superpowers. Preserve
project artifact conventions, isolation and mandatory gates. Background work or
independent review is a claim that needs real evidence. DevFleet is optional and
must have verified inert planning and bounded manual launch/merge controls.

## Compatibility and artifacts

Blueprint discovers lifecycle resources through `development-lifecycle-rules` when
available and otherwise uses its existing plain-plan contract. Keep established
artifact paths; a handoff does not grant actor, delivery or runtime permission.
See the repository's [capability matrix and deferred-consumer strategy](https://github.com/mmalyska/claude-plugins/blob/main/docs/workflow/compatibility.md)
for loading limits, manual OpenCode, release evidence and orchestrator prerequisites.
This external maintainer reference adds no installed-plugin dependency. Native
integration and consumer migration remain deferred; no pilot is started by install.

## Skills

| Skill | Description |
| --- | --- |
| `autonomous-agent-harness` | Bounded recurring workflows with verified scheduling/persistence or manual execution |
| `blueprint` | Profile-sized resumable plan; local review, no implied workers/delivery |
| `context-budget` | Audit context window consumption across agents, skills, MCP servers, and rules — identify bloat |
| `continuous-agent-loop` | Patterns for continuous autonomous agent loops with quality gates, evals, and recovery controls |
| `eval-harness` | Formal evaluation framework implementing eval-driven development (EDD) principles |
| `iterative-retrieval` | Bounded local or authorized-worker context search |
| `rules-distill` | Scan skills to extract cross-cutting principles and distill them into rule files |
| `safety-guard` | Procedural cautious-operation and directory-scoped editing guidance |
| `search-first` | Research-before-coding workflow — search for existing tools and patterns before writing custom code |
| `team-builder` | Select role proposals; local passes by default, authorized actors only |
| `subagent-driven-development` | Accepted task execution with authorized workers or local sequential role passes |
| `writing-skills` | Portable skill authoring including profile/topology and example authorization checks |
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
