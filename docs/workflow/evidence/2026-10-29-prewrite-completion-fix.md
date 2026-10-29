# Pre-write completion repair — LIVE-F07 recurrence

Base: `6d1ad2e9411c4c843dfc210e35acadb5bc18005d` (merged PR #28).
Branch/worktree: `fix/workflow-prewrite-completion`,
`.worktrees/fix/workflow-prewrite-completion`.
Profile/topology: STANDARD + HANDOFF. User requested a repair PR and assigned this
subagent; no further actors, live model trials, merge or cleanup are included.

## Evidence and root cause

Claude S05/revoked `2026-10-29-local-revoked-02` read the complete installed
contract, verified linked isolation and actual primary main/HEAD/clean state,
then declared isolation verified and edited. It never queried a default source
or recorded a verified local-base fallback. Equivalent primary/writer HEAD
facts were present; default policy was not. Fixture AGENTS.md specified gates
and isolation, not a default branch. The previous denied-query clarification
was not exercised: this run never attempted the missing query.

The loaded contract's prominent command block covered writer/isolation facts.
Primary/default/base requirements followed in prose; completing the visible
block and primary diagnostics was mistaken for completing preflight. This is
an instruction-organization diagnosis from the observable sequence, not proof
of hidden reasoning or a platform defect. Merely repeating denied-command
recovery would not address this skipped requirement. Existing equivalent-fact
acceptance remains correct; no literal command spelling is a behavioral gate.

The same run attempted a status-printing unittest wrapper even though the exact
direct project runner was allowlisted. Normal permissions denied the wrapper;
the model respected the no-retry instruction and accurately marked tests NOT RUN.
Independent operator tests passed, but cannot supply model verification. The
contract already preferred separate check calls, yet its concrete shell example
made an unnecessary wrapper easy to select. This repair improves the initial
choice rather than authorizing retry against a host denial.

Raw streams and historical FAIL remain in the existing operator evidence worktree.
They are not copied into this PR. Revocation handling and scope preservation
passed; this repair does not regrade history or claim overall behavioral closure.

## Repair

- Organize the existing [common contract](../../../plugins/development-lifecycle/rules/common/workflow.md#safety-and-worktree-first)
  into writer isolation, primary state, and default/task-base parts. Require a
  brief completed-facts record before mutation; missing parts block writes.
- Show read-only remote-default and remote-name queries. An absent origin/HEAD
  alone cannot establish no-remote state. Verified policy and equivalent output
  remain valid; the verified no-remote/local-primary fallback is retained.
- Align the existing [worktree skill](../../../plugins/git-workflows/skills/using-git-worktrees/SKILL.md#verify-base-without-silently-changing-primary)
  with that completion boundary. No new contract, artifact, hook or runner.
- Prefer the exact direct project check when native tool status suffices. Shell
  wrapping remains optional when necessary. Keep normal permissions, no-retry
  instructions and NOT RUN reporting; no harness allowance is broadened.
- Advance paired lifecycle manifests to 1.2.15 and git-workflows to 1.3.8.
  Catalog identities and Codex disabled bundled hooks remain unchanged.

## Validation and limits

Baseline: 73 tests, 70 PASS and three opt-in native metadata skips.
Repaired: `python3 -B -m unittest discover -s tests -v`, exit0; 74 tests,
71 PASS and the same three skips. The added test executes the documented default
queries in disposable Git repositories: no origin/HEAD with no remote versus
no origin/HEAD with an unfetched origin. It verifies real output distinguishes
the fallback conditions without network, commits or a policy engine. Existing
negative source guards protect completion and direct-runner declarations.

Changed Markdown lint (MD013 disabled), local links/fragments, paired manifest
JSON and `git diff --check`: PASS. New native installs and LIVE model behavior:
NOT RUN. Static output cannot establish that models will follow this layout.
LIVE-F07 remains OPEN; release acceptance remains BLOCKED.

After merge, rerun the failed Claude S05/revoked on a fresh profile/fixture with
unchanged task, model and normal permission boundary. Require successful or
recorded verified default/base facts before first mutation, and direct check
results or honest unavailability. Preserve this failure and report actor scope,
primary/refs/source preservation and independent checks separately. No worker,
second CLI, delivery or automatic repair is included in that trial instruction.
Codex/S16/other entrypoint coverage retains its separate provenance and gates.

Rollback is a scoped revert and disposable prior-plugin reinstall, preserving
all user state and trial records. It would restore the known skipped-preflight
layout, not approve release. Primary remains clean on the base SHA.
