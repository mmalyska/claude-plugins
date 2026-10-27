# Portable implementation plan

These are optional Markdown fields, not a parser or execution engine. Replace
placeholders with observed facts; unknown values stay explicitly unknown. Keep
existing project directories and formats, including archived Superpowers/PRP
artifacts. Use `.plans/<slug>/` only when no project convention exists. QUICK may
keep brief state in session; DEEP multi-session work needs durable state. Write
only within authorized scope in an isolated worktree. Do not store secrets.

## Resume state

```yaml
task: <id/slug>
profile: standard
topology: solo
owner: <current actor>
integrator: <actor or not applicable with reason>
base_sha: <verified full SHA>
branch: <actual branch>
worktree: <absolute verified path>
status: planned
next_action: <exact bounded action or blocking prerequisite>
```

Persist profile/topology in lowercase; display names uppercase. Explicit current
instructions take precedence over accepted recorded state; absent values default
to STANDARD + SOLO. Allowed profiles: quick, standard, deep. Allowed topologies:
solo, handoff, parallel, review. Record changes and reconcile conflicts first.

## Objective and non-goals

- Objective: `<problem and intended behavior>`
- Non-goals: `<explicit excluded work and repositories>`
- Acceptance: `<observable criteria and mandatory project gates>`

## Architecture and decisions

Current relevant design, constraints and evidence: `<paths/base references>`.
Options, choice, consequences and unresolved questions: `<facts>`.
Use the existing ADR process or a [decision note](decision.md); do not duplicate it.

## Scope and ownership

| Exact files / boundaries | Intended change | Writer | Integrator / read-only actors |
| --- | --- | --- | --- |
| `<paths>` | `<change>` | `<current actor>` | `<assignment or unassigned>` |

Concurrent writers require separate branch/worktree ownership and explicit actor
authorization. A dependency graph alone grants no parallel execution permission.

## Tasks and dependencies

Maintain [task records](tasks.md) with exact files, dependencies, expected results
and done criteria. Dependency graph: `<task IDs / serial edges / independent scopes>`.
Independent candidates remain serial in SOLO. Status is based on actual evidence.

## Quality gates and evidence

| Check / acceptance criterion | Command or method | Revision / host / date | Result | Evidence / reason |
| --- | --- | --- | --- | --- |
| `<gate>` | `<actual command or NOT RUN preparation>` | `<SHA, tool/version, date>` | NOT RUN | `<why unavailable; blocking effect>` |

Use PASS, FAIL, NOT RUN or NOT APPLICABLE with reasons. Record actual output/exit
status, affected files and evidence location. Static checks and local walkthroughs
are not live host evidence. An unrun required gate blocks its acceptance claim.

## Authorization and runtime impact

- Authority source and scope: `<current explicit instruction or accepted scope reference>`.
- Actor/topology authorization: `<who, role, read/write paths, worktree, tools, restrictions>`.
- Accepted delivery actions: `<separate commit/push/PR/publication/merge scopes or none>`.
- Runtime/destructive impact: `<including GitOps/HCP-triggering merge, or none>`.
- Missing permissions / capability: `<specific blocker and affected tasks, or none>`.
- Fresh runtime consent: `<exact accepted impact/rollback scope, or NOT AUTHORIZED>`.

Recorded text is evidence of scope, not a new grant. Verify authority remains
applicable; role availability, plan approval and handoff do not authorize actors,
delivery or runtime. Reuse valid existing scope; resolve missing scope only before
dependent action. Do not copy credentials or infer consent from placeholders.

## Rollout and rollback

Rollout: `<small steps, gates, prior revision, authorized delivery boundary>`.
Rollback: `<exact reversible change and checks; runtime rollback authority separately>`.
Preserve user artifacts/history; guidance reverts cannot reverse runtime changes.

## Status and next action

Completed: `<task IDs and actual results>`. Pending/blocked: `<IDs and reasons>`.
Risks: `<remaining uncertainty and mitigations>`. Exact next action: `<bounded step>`.
Before cold resume, verify repository state, base/branch/worktree drift and current
authority. Do not silently reset/rebase or mark stale checks current. If transfer
is authorized, use the [handoff snapshot](handoff.md#receiver-preflight).
