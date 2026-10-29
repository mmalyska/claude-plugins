# Portable handoff snapshot

These are optional Markdown fields, not a parser or execution engine. Replace
placeholders with observed facts; unknown values stay explicitly unknown. Keep
existing project directories and formats, including archived Superpowers/PRP
artifacts. Use `.plans/<slug>/` only when no project convention exists. QUICK may
keep brief state in session; DEEP multi-session work needs durable state. Write
only within authorized scope in an isolated worktree. Do not store secrets.

Store a handoff in the active plan folder; use `.ai/handoffs/` only for a task
without an active plan. Preserve an established project convention first.

A snapshot supports cold resume without chat; it is not a transcript, automatic
memory or actor authorization. Link the existing [plan](plan.md) and [tasks](tasks.md)
at their actual project locations when using this structure. Defaults in the
example are not consent to transfer responsibility.

## Transfer state

```yaml
task: <id/slug>
from: <harness/actor>
to: unassigned
base_sha: <verified full SHA>
branch: <actual branch>
worktree: <absolute verified path>
profile: standard
topology: solo
status: planned
```

For an explicitly authorized transfer record topology: handoff and the assigned
receiver. Other accepted topology/profile values remain valid; do not change them
merely to fill this template. Status: planned, in_progress, review or blocked.

## Completed changes and affected files

`<Exact paths, changes/commits, staged/unstaged/untracked state and completed tasks>`.

## Decisions and context

<Objective/non-goals, acceptance, constraints, decision links, rejected options,
unresolved questions and essential source paths; no dependence on chat history>.

## Tests and results

| Check | Command / method | Revision / host / date | Result | Evidence / reason |
| --- | --- | --- | --- | --- |
| `<gate>` | `<actual command or prepared-only>` | `<SHA/tool/version/date>` | NOT RUN | `<blocker and acceptance impact>` |

Keep PASS, FAIL, NOT RUN and NOT APPLICABLE distinct. Static/manual walkthroughs
are not live trials. Do not inherit a PASS after relevant changes without review.

## Risks and missing permissions

- Risks / blockers: `<what remains uncertain and how to resolve>`.
- Authority source: `<accepted instruction and current scope reference>`.
- Actor authorization: `<assigned receiver, role, read/write paths, branch/worktree, tools, exclusions>`.
- Delivery authority: `<exact authorized actions or none>`.
- Runtime impact and fresh consent: `<specific impact/rollback authorization or NOT AUTHORIZED>`.
- Missing permissions/capabilities: `<what is absent and which action it blocks>`.

The snapshot grants no permission. It cannot override current instructions,
revocation, project gates or host restrictions. An unassigned receiver cannot
claim a transfer or start a worker; preserve SOLO when no transfer is authorized.

## Exact next step

`<Single bounded action and expected result; or precise prerequisite if blocked>`.
Remaining tasks/dependencies: `<IDs and paths>`. Rollback: `<scoped plan and checks>`.

## Receiver preflight

1. Read current policy and linked task state; confirm assignment, profile/topology,
   writer ownership and actor/tool/file scope. If unauthorized, no dispatch follows.
2. Run the [shared Git preflight](../../rules/common/workflow.md#safety-and-worktree-first)
   before any write; snapshot observations are historical. Stale base, branch drift
   or missing state blocks dependent writes until reconciled; preserve user work.
3. Review gates against the actual revision; required NOT RUN/FAIL is not PASS.
   Resume only the exact authorized next action, with no inferred delivery/runtime
   authority. Ask only for genuinely missing scope.
