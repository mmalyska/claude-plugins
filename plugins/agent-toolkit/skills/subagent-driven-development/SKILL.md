---
name: subagent-driven-development
description: "Execute accepted task scope with explicitly authorized workers or local sequential role passes, preserving topology, verification and delivery limits."
---

# Subagent-Driven Development

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

## Selected execution technique

This existing name is retained for compatibility. Explicitly authorized workers
are optional; SOLO uses the same task/spec-review/quality-review role passes in
the current session. This technique operates inside the existing lifecycle; it
is not a mandatory new sequence or an external plan-executor dependency.

```text
Accepted task scope -> check stage/actor authority
  SOLO -> local implementation and separate local review passes
  Authorized actors -> verify actual capability and bounded worker scope
  Missing capability -> disclose; compatible local fallback or stop
  Result/failure -> evidence, dependent gates, next authorized task or stop
```

## Per-task procedure

1. Read the accepted task and current repository state. Record profile/topology,
   allowed files/actions, base/branch/worktree, owner/integrator, verification and
   attempt/runtime bounds. A plan is state, not authority to execute all its tasks.
2. If work is authorized, implement locally in SOLO or brief an explicitly authorized
   worker using actual exposed tooling. Include sufficient context, restrictions,
   done condition and required evidence; do not depend on a host inheritance flag.
3. Check spec compliance and relevant quality/security/test completeness as distinct
   local passes, or authorized independent reviews. Do not claim actor independence
   from a role label. TDD is selected when useful/requested or required by project
   policy, not a universal instruction for every task.
4. Resolve in-scope findings, rerun affected checks and record actual results.
   A failed worker or required gate blocks dependent integration. Missing evidence
   is not success; do not dispatch downstream work to conceal a failure.
5. Continue only through currently authorized task scope and bounds. A single-task
   or stage-only instruction stops there, not at the end of the whole plan.
   Final review is local in SOLO; no automatic final reviewer dispatch.

Every concurrent writer has its own branch/worktree and a named integrator.
An authorized read-only reviewer can share the owner's isolation; sequential
writers can share it only within explicit scope. Preserve existing primary and
external worktree ownership. Readiness does not authorize commit/push/PR, merge,
cleanup or runtime; use existing finishing guidance only for a selected action.

## Brief and status

Give objective, exact task scope, relevant files/decisions, profile/topology,
authority/exclusions, isolation, checks, done criteria and an output contract.
Status is DONE, DONE_WITH_CONCERNS, NEEDS_CONTEXT or BLOCKED with evidence.
Read concerns before accepting DONE; supply missing context only within scope.
On repeated failure without new evidence or exhausted bounds, stop/report the
blocker. Do not increase model, privileges or actor count as an implicit retry.

For spec review, compare actual changes to acceptance and non-goals. For quality
review, assess correctness, maintainability, security and test evidence. Use local
checklists or existing installed skills; no absent provider is required.
