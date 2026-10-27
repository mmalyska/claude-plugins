# development-lifecycle

Shared specification, implementation, testing, review, and delivery workflows
for Claude Code and Codex. External workflow plugins are optional.

## Lifecycle

[Spec → Plan → Build → Test → Review → Simplify → Ship](rules/common/workflow.md)

The [workflow contract](rules/common/workflow.md) defines independent execution
profiles QUICK/STANDARD/DEEP and topologies SOLO/HANDOFF/PARALLEL/REVIEW. The
default is STANDARD + SOLO. Other topologies require explicit user authorization;
DEEP alone does not authorize delegation. Plan and Build are stages performed
through existing procedures, not new command names. Ship assesses readiness and
performs only authorized delivery actions.

Load the contract through `development-lifecycle-rules`; rules are on demand,
not automatic interception of every user request. T03–T08 align profile-sized
procedures, actor/delivery authorization and optional-provider packaging. Portable
artifact resources and complete compatibility/scenario evidence remain T09–T11;
full workflow conformance is not claimed yet. Native discovery/installation checks
require separate authorized execution, not merely a passing static suite.

Claude's existing command entrypoints link to the shared skill procedures. In
Codex invoke the same skill names, for example `$development-lifecycle:spec`, `$development-lifecycle:test fix: login bug`,
`$development-lifecycle:review`, or `$development-lifecycle:ship`. Commands are skill inputs, not executable shell syntax.

| Skill | Purpose |
| --- | --- |
| `spec` | Repository-grounded requirements and design with acceptance criteria |
| `test` | Profile-sized verification, with selected TDD/reproducer modes and project gates |
| `review` | Correctness, readability, architecture, security, performance |
| `code-review` | Local changes or a GitHub PR; external review actions follow user authorization |
| `ship` | Verify checks, review delivery readiness, and execute the authorized delivery action |
| `aside` | Answer a side question while preserving the active task |
| `learn-eval` | Extract and evaluate reusable session knowledge |
| `skill-create` | Extract patterns from git history into shared skills |
| `update-docs` / `update-codemaps` | Maintain documentation and architecture maps |

Role skills include `architect`, `build-error-resolver`, `code-reviewer`,
`doc-updater`, `docs-lookup`, and `tdd-guide`. Claude also retains native agent
entrypoints. Codex uses available authorized delegation or applies the role in
the current session. Delegation is not required to complete a workflow.

Domain skills include `ai-regression-testing`, `architecture-decision-records`,
`e2e-testing`, and `simplify`. `claude-devfleet` is an optional external service
integration: either host can call it, but the service runs Claude workers.

Use `development-lifecycle-rules` to read relevant common standards on demand;
plugin rule files are not automatically loaded. New workflow reports default to
`.reports/agent-workflows/`, preserving established locations for existing work.

## Optional providers and local paths

Superpowers is optional and is not a declared plugin dependency. Removing that
manifest dependency does not uninstall or disable a user's existing provider.
Select a discovered provider technique only within task authority; if absent,
use the local/manual procedure rather than invoke a phantom `superpowers:*` skill.

| Stage | Existing local/manual path without an external workflow provider |
| --- | --- |
| Spec | `spec` records relevant requirements and acceptance |
| Plan | Current agent uses the `architect` guidance and task/file/check dependencies |
| Build | Current agent implements only the authorized scope in an isolated worktree |
| Test | `test` / selected `tdd-guide` technique and actual project checks |
| Review | `review`, `code-review` or `code-reviewer` applied locally in SOLO |
| Simplify | Existing `simplify`; no-op assessment is valid |
| Ship | `ship` readiness and exact authorized delivery, no automatic commit/PR/merge |

Plan and Build remain stages, not new commands/skills. The optional toolkit
blueprint is useful when installed but not required for this plugin to work.
Preserve established plan/report directories and historical Superpowers/PRP
artifacts; no history or user host configuration is migrated.

Claude keeps native command/agent metadata and entrypoint links. Codex discovers
these same skill bodies through its manifest, with `hooks: []`; rule loading and
worktree preflight are procedural. Neither host may infer permission from an agent
being present. Scheduling, memory, scanners and DevFleet need actual capability
and authority; missing features yield honest prerequisites or compatible local
paths. Native OpenCode parity is deferred, not provided by another adapter copy.

## Install

After registering the repository marketplace, select one host:

```sh
# Claude Code
claude plugin install development-lifecycle@mmalyska-claude-plugins
# Codex
codex plugin add development-lifecycle@mmalyska-claude-plugins
```
