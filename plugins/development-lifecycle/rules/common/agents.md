# Agent Roles and Authorization

Read [the workflow contract](workflow.md) first. A role describes expertise;
a topology assigns actors. Default STANDARD + SOLO means the current session
applies roles locally. Naming a role, planning a task, choosing DEEP or exposing
an agent never grants permission to launch one.

## Authority before capability

HANDOFF, PARALLEL and REVIEW require explicit user authorization before changing
actors. Reuse existing authorization for its stated scope; do not ask repeatedly
for the same authorized action. Record owner, permitted roles/scopes, side effects
and integrator where relevant. Keep task, tool and permission limits intact.

Only after authority is established, inspect actual exposed agents/tools:

- **Claude Code:** use exposed native agents when authorized. Definitions under
  `agents/` retain host metadata and link to shared role instructions. Inventory
  CLI calls are also subject to the session's no-other-harness restriction.
- **Codex:** use configured types through exposed delegation tools when authorized.
  Markdown native-agent files do not automatically register Codex agents.
- If the requested capability is missing, disclose it. Use sequential local role
  passes only if consistent with the user's intent; do not call them independent
  review or silently change an explicitly requested topology.

Never launch another CLI, worker or orchestrator to bypass a restriction. Keep the
configured model unless a model change is explicitly authorized; native model
metadata does not instruct the current session to switch its model for a role pass.

## Scoped work and evidence

Choose architecture, TDD guidance, review or build resolution for the actual
problem. Brief an authorized actor with objective, relevant context, constraints,
permitted scope, expected evidence and done condition. SOLO uses those same briefs
locally without adding actors. DEEP + SOLO includes a separate local review pass,
with its lack of independent review disclosed.

Parallel read-only work requires explicit topology authorization and actual
capability. Read-only reviewers can share the owner's isolated worktree; every
concurrent writer needs a distinct branch/worktree and a named integrator. A
sequential writer can share an isolated checkout only within its authorized scope.
Collect findings before dependent changes; disclose failed or partial results.

Read applicable shared `AGENTS.md` first, then host adapters and project policy.
Report conflicting instructions and pause dependent actions until reconciled;
do not select different security rules by host. Local role application does not
authorize implementation, external publication, delivery or runtime mutation.
