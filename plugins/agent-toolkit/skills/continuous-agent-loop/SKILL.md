---
name: continuous-agent-loop
description: "Execute bounded agent iterations with verification, persistent progress, and recovery in Claude Code or Codex."
metadata:
  origin: "ECC"
---

# Continuous Agent Loop

## Execution boundary

Check authority before capability. Default STANDARD + SOLO; preserve explicit
accepted task profile/topology and current exclusions. Planning or selecting
roles does not authorize a worker. HANDOFF, PARALLEL and REVIEW require explicit
user authorization before changing actors. Never launch another CLI, worker or
orchestrator to bypass a restriction. Check actual exposed tools/schemas only
after authority; availability alone grants no action.

If requested capability is missing, disclose it and use SOLO/manual execution only
when consistent with user intent. Do not relabel local role passes as independent
review or fabricate tool/background success. Reuse existing specific authority
within scope; no repeated permission menu. Keep the configured model unless a
change is authorized. Mandatory project gates and worktree-first always apply.
Consult the existing development-lifecycle-rules contract when installed; this
plugin's safe local path requires no other plugin or copied skill catalog.

Use for a task that needs repeated implement/check iterations. Establish the
objective, profile/topology, owner/integrator, actor permissions/exclusions,
acceptance checks, allowed actions, and attempt/runtime limit first.
Use the project's current tracking location, or
`.reports/agent-workflows/loop.md` for a new progress record.

## Iteration

1. Read progress, profile/topology/permissions and current restrictions. Preserve
   narrower/revoked authority and choose only a ready task within accepted scope.
2. Implement within scope in SOLO. Under explicit actor authority, verify actual
   tools before delegation; if absent, use local execution only when compatible
   with user intent, otherwise report the prerequisite.
3. Run the relevant checks and compare their result with acceptance criteria.
4. Record changes, evidence, attempts consumed, blocker, and next action.
5. Continue only within authorized stage/task scope while measurable progress
   and bounds remain. A failed worker/gate blocks dependent integration.

Stop on completion, cancellation, a permission block, an unmet external
prerequisite, or the configured limit. On a repeated failure without new evidence,
reduce the problem to a reproducer and report the blocker. Do not increase
privileges, install a loop framework, or invent an unavailable audit command.

Only under explicitly authorized parallel topology use a dependency graph,
isolated branch/worktrees per writer and a named integrator. No actor, scheduler
or service launch follows from a loop instruction or plan approval.
For CI/PR workflows inspect actual checks; keep merge, push, and deployment
within explicit task authorization. Use the available `eval-harness` skill or
write concrete pass/fail checks directly.

This loop runs in the current session. For recurring/background execution use
`autonomous-agent-harness` to establish and verify a supported external runner;
do not claim that Markdown instructions keep running after the session ends.
