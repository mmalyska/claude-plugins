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
not automatic interception of every user request. This contract is the first
implementation increment. Existing procedure diagrams, unconditional testing
requirements, actor triggers and delivery defaults remain to be aligned in the
planned T03–T08 tasks; full workflow conformance is not claimed yet.

Claude's existing command entrypoints link to the shared skill procedures. In
Codex invoke the same skill names, for example `$development-lifecycle:spec`, `$development-lifecycle:test fix: login bug`,
`$development-lifecycle:review`, or `$development-lifecycle:ship`. Commands are skill inputs, not executable shell syntax.

| Skill | Purpose |
| --- | --- |
| `spec` | Repository-grounded requirements and design with acceptance criteria |
| `test` | RED-GREEN-REFACTOR for features and reproducing tests for bug fixes |
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

## Install

After registering the repository marketplace, select one host:

```sh
# Claude Code
claude plugin install development-lifecycle@mmalyska-claude-plugins
# Codex
codex plugin add development-lifecycle@mmalyska-claude-plugins
```
