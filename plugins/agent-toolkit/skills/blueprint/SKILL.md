---
name: blueprint
description: "Create profile-sized, resumable implementation plans with exact file scopes, dependencies, checks and rollback. Planning does not authorize workers or delivery."
metadata:
  origin: "community"
---

# Blueprint — Construction Plan Generator

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

## Profile-sized planning

Use for a complex change, multi-session resume or requested implementation plan.
A Plan-only instruction stops with the plan; it does not authorize Build, workers,
commit/push/PR or runtime. The procedure below serves the existing Plan stage,
not another engineering lifecycle.

- QUICK: brief goal, scope, success and next step; no mandatory durable dossier.
- STANDARD: relevant files/dependencies, acceptance and project checks; durable
  state for multi-session work.
- DEEP: repository-grounded decisions, risks, ownership/integrator, exact tasks,
  verification, impact and rollout/rollback, plus a distinct local review pass.

## Prepare a resumable plan

1. Inspect repository/task state, relevant architecture, prior accepted plans and
   available project checks. GitHub authentication is not a prerequisite to local
   planning. Research only unresolved questions at the selected depth.
2. Break work into small verifiable tasks: exact paths, intended change, dependencies,
   tests/expected results, done criterion and rollback. Identify independent scopes
   as candidates, not permission to run them in parallel. SOLO stays serial.
3. Preserve the existing artifact directory. If none exists, use
   `.plans/<slug>/plan.md` and `tasks.md`. Do not move historical Superpowers/PRP
   plans or create another catalog of procedure copies. Record objective/non-goals,
   acceptance, profile/topology, owner, base SHA, branch/worktree, permissions,
   decisions, status, actual evidence and exact next action.
4. Review completeness, dependencies, overlapping writers, missing authority,
   mandatory gates and rollback in a separate local pass. Independent review
   needs explicit actor authority and suitable capability; disclose self-review.
5. Write a resume brief. Update an existing memory index only if configured and
   within accepted write scope; a Markdown state file is not automatic memory
   loading. Do not invent a new user-level memory location or background service.

## Isolation and missing tools

Inspect existing isolation before writing a plan. Reuse a suitable linked worktree,
otherwise use actual native creation or manual git with a verified base and local
exclude. If isolation is blocked, stop writes and report the permission prerequisite.
Missing git/gh is not an edit-in-place bypass: provide read-only/session planning
or disclose the missing prerequisite when durable repository writes are needed.
Normal host permission handling may resolve a scoped block; no second CLI fallback.

## Example

For a requested DEEP + SOLO database migration plan, record behavior/constraints,
current schema owners, staged migration/backfill/check/rollback tasks, permissions
and resume state. A dependency graph may show independent components, but no worker
starts and no migration runs merely because the graph or plan is approved.

The existing blueprint skill is shared in both hosts (Codex uses
`$agent-toolkit:blueprint`). Use exposed host planning/file tools; no generator,
external executor or Superpowers installation is required.

## Plan changes

On new evidence, revise affected tasks/edges/acceptance with rationale and retain
actual completed evidence. Do not silently broaden scope, hide blocked work or
mark a task done because a plan proposed it. Stop at the requested boundary.

## Source

Inspired by antbotlab/blueprint and the Everything Claude Code collection.
