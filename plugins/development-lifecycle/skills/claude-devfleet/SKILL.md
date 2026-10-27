---
name: claude-devfleet
description: "Plan or use bounded, explicitly authorized DevFleet work after verifying service side effects and controls; local planning remains available without the service."
metadata:
  origin: "community"
---

# Claude DevFleet — Optional Execution Client

Read [the workflow contract](../../rules/common/workflow.md) first. Default
STANDARD + SOLO, preserving explicit accepted task profile/topology and exclusions.
Check authority before capability. Planning or selecting roles does not authorize
a worker; HANDOFF, PARALLEL and REVIEW require explicit user authorization before
changing actors. Never launch another CLI, worker or orchestrator to bypass a
restriction. SOLO performs local planning/role passes without calling a worker
service. A request for a plan or generic implementation is not service-launch scope.

## Host and prerequisites

DevFleet is an optional external service whose workers are Claude workers even
when the calling host is Codex. Do not describe them as Codex native agents.
Inspect actual exposed tool schemas and verified service behavior within authorized
service scope; the names below are illustrative existing operations, not guaranteed
API signatures or permission to invoke them. No service is required for correctness.

If the service/tool is absent, report the prerequisite and offer local planning or
execution only if compatible with user intent. Do not invent a mission, success,
connection or tool name. Connecting/configuring a service is separate setup scope;
do not install it or start another host CLI implicitly.

Before an orchestrator pilot, record at least three completed manual
HANDOFF/PARALLEL tasks and a partial-execution failure test. Include evidence from
a parallel pilot when available. This task/skill does not itself run that pilot.

## Verify inert planning before any service mutation

A service planning call can create queued or active missions. Do not call
`plan_project` until verified controls prevent unauthorized launch and merge.
Automatic dispatch and merge must be disabled by verified service controls before
creating jobs. Do not assume that a parameter exists or that changing a flag
after creation can undo workers already launched.

If safe controls cannot be verified before the call, report incompatibility and
use no service. This includes a service that cannot keep created jobs inert or
cannot separate launch, integration and merge authority. A user approving a plan
is not authorizing auto-dispatch, automatic merge or runtime effects.

## Bounded manual execution when explicitly authorized

1. Prepare a local task graph in the existing project artifact location. Record
   objective, acceptance, profile/topology, owner/integrator, base/branch/worktree,
   exact writer/reviewer scopes, permissions/exclusions, gates, attempt/time bounds,
   stop/cancel controls, impact and rollback. Keep secrets out of briefs/reports.
2. Verify actor/service authority and prerequisites, then actual exposed capability
   and inert-job controls. Reuse existing specific authorization without another
   menu. Explicit no-other-harness restrictions still prohibit external workers.
3. Create only inert bounded jobs under verified schemas. Each concurrent writer
   has a separate branch/worktree; reviewers are read-only unless scope says
   otherwise. A named integrator owns final checks and any authorized integration.
4. Dispatch only the individually authorized ready work. Dependency readiness is
   not automatic permission to launch downstream work. Record actual job IDs,
   limits, scope and control state, not hypothetical service defaults.
5. Use short nonblocking status/report calls within the task's monitoring scope.
   A failed worker blocks dependent integration and further dependent dispatch.
   Report partial results and missing checks honestly; do not claim a whole graph
   completed from one success. Repeated failure or exhausted bounds stops the work.
6. Integration, branch delivery, remote merge and runtime mutations are separate
   actions. A GitOps/HCP auto-apply merge requires fresh explicit permission with
   impact/rollback. Runtime consent is not granted by the job graph or actor scope.
   Do not allow an uncontrolled auto-merge chain.
7. Preserve artifacts/worktrees for review. Cancel/retry only jobs in accepted
   control scope; do not cancel unrelated jobs or increase actors/privileges/model
   as a hidden retry. A plugin rollback does not undo external jobs/runtime effects.

## Operations to inspect, not blindly invoke

| Existing operation name | Required precondition |
| --- | --- |
| `plan_project` | Verify planning is inert, bounded and within explicit service scope before calling |
| `create_project` / `create_mission` | Verified schemas and no creation-time dispatch/merge side effect |
| `dispatch_mission` | Explicit actor/work scope, actual capability, limits and isolated writers |
| `get_mission_status` / `get_report` / `get_dashboard` | Accepted monitoring scope; report actual observed state |
| `cancel_mission` | Exact job/control authority, no cancellation of unrelated work |

No automatic launch example or assumed concurrency count is a default. The service
DAG is a transport/execution mechanism inside the shared lifecycle, not another
engineering lifecycle or a hard dependency. Scheduling/background continuation
must be verified, not inferred from these Markdown instructions.
