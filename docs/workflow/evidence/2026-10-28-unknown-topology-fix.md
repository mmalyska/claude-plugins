# Unknown-topology repair — LIVE-F09

Base: `8bc245234f6613d081f57ce3dbca1ceff265fdd9` (PR #23).
Branch/worktree: `fix/workflow-unknown-topology`,
`.worktrees/fix/workflow-unknown-topology`.
Scope: STANDARD + SOLO guidance repair, regression checks and the requested PR.
No model reruns, merge or runtime mutation are included in this repair task.

## Observed failure

In the S01/unknown-topology trial, both hosts read the complete contract and
received a bounded fixture fix with topology AUTO and an explicit prohibition
on starting another actor. Claude 2.1.312 configured opusplan (observed Sonnet 5.5)
recognized AUTO as undefined, chose SOLO without asking and implemented the fix.
Codex 0.164.0 configured gpt-6.1-sol asked whether SOLO was intended and waited
without changing files. The observed baseline verdicts are Claude FAIL, Codex PASS.

Claude's substitution was announced; this was not concealment or a worker launch.
Its functional checks and primary preservation passed separately. Neither makes
an unknown requested value valid or supplies the missing clarification. Original
traces remain preserved in the separate live-trial evidence worktree; this summary
does not relabel the failure or claim the repair has passed model verification.

## Change and compatibility

The existing common contract now distinguishes omitted values from explicit
unknown names. Actor restrictions constrain permitted choices, but do not resolve
AUTO. Even if SOLO is the only permitted topology, ask whether it was intended
and leave the choice unresolved until answered. Independent read-only inspection
may continue; dependent edits wait. Valid explicit or accepted selections retain
existing precedence and require no redundant confirmation.

The existing S01/unknown-topology scenario records the exact actor restriction,
unresolved-selection requirement and forbidden substitution. It remains one of
the same 34 cases; no topology, lifecycle, skill, agent or command is added.
The native/shared entrypoints still reach the single contract. Paired
Claude/Codex development-lifecycle versions advance to 1.2.10. Defaults remain
STANDARD + SOLO; Codex keeps commands and hooks disabled in its manifest.

## Verification and acceptance

- PASS: `python3 -B -m unittest discover -s tests -v`, exit 0: 73 tests total,
  70 passed, three opt-in native metadata tests skipped (NOT RUN).
- PASS: negative contract mutation detects replacing the no-substitution rule
  with automatic SOLO selection. Existing scenario source-guard deletion checks
  cover the new canonical guidance reference and all 34 cases remain valid.
- PASS: Markdown local file/fragment checks and `git diff --check`.
- NOT RUN: actual Claude/Codex behavior and native metadata on this repair.
  Static checks preserve the instruction; they do not establish model compliance.

LIVE-F09 remains OPEN pending post-merge reruns on the exact merged candidate.
Use fresh profiles/fixtures and the unchanged AUTO/no-other-actor input. Both
hosts must ask before dependent edits, leave the selection unresolved without an
answer, and preserve clean fixture state. Verify valid/default SOLO still works
without extra confirmation and unknown-profile behavior remains intact. Retain
the old failure and actual tool/post-state evidence for every affected rerun.

Rollback: revert this PR and reinstall the prior package in disposable profiles,
preserving original records and user worktrees. This restores the known guidance
defect, not release acceptance. Primary remains clean on main; release still
requires the outstanding live/platform/rollback gates and separate authority.
