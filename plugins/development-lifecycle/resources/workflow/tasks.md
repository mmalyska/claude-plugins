# Portable task records

These are optional Markdown fields, not a parser or execution engine. Replace
placeholders with observed facts; unknown values stay explicitly unknown. Keep
existing project directories and formats, including archived Superpowers/PRP
artifacts. Use `.plans/<slug>/` only when no project convention exists. QUICK may
keep brief state in session; DEEP multi-session work needs durable state. Write
only within authorized scope in an isolated worktree. Do not store secrets.

Use alongside the [plan](plan.md). Copy this record per bounded task; dependency
edges describe order, not permission to launch workers. Do not mark completion
from a proposed command or a checkbox alone.

## Task TNN — bounded outcome

- Status: planned | in_progress | review | blocked | complete.
- Exact files: `<repository-relative paths to create/modify; explicit exclusions>`.
- Intended change: `<small concrete before/after behavior>`.
- Dependencies: `<task IDs and external prerequisites, or none>`.
- Owner / integrator: `<actor, branch/worktree; other actors unassigned unless authorized>`.
- Authority and missing permissions: `<accepted task/tool/delivery/runtime limits>`.
- Tests and checks: `<commands/methods; mandatory project gates>`.
- Expected result: `<observable assertion/output for each check>`.
- Actual evidence: `<PASS/FAIL/NOT RUN/NOT APPLICABLE, exit/result, revision, host/version/date, reason>`.
- Completion criterion: `<specific observable done condition and blocking gates>`.
- Risks: `<remaining uncertainty and mitigation>`.
- Rollback: `<scoped reversal, validation, preserved artifacts; runtime authority separately>`.
- Next action: `<exact bounded step or missing prerequisite>`.

Keep failed/unrun checks visible. A task may finish a bounded preparation step
while a required live check remains NOT RUN; explicitly state that release or
conformance is blocked. Changes to scope/dependencies require rationale, not
silent broadening. Record decisions via the [existing decision process](decision.md).
