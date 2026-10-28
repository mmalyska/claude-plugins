# DEEP plan validation repair — LIVE-F11

Base: `917acd6dc306e16268ac3d36031299a705b90c1c` (PR #25).
Branch/worktree: `fix/workflow-deep-plan-validation`,
`.worktrees/fix/workflow-deep-plan-validation`.
Profile/topology: STANDARD + HANDOFF. The user explicitly requested one repair
subagent; the original session remains owner/integrator and handles Git metadata
and publication. No further delegation or live model trial is included.

## Observed gap

In S04/plan-only, both hosts preserved the source files, produced durable artifacts
and stopped before Build, workers or delivery. Those boundaries passed separately.
Claude wrote plan/tasks/decision files without an observable separate current-plan
review. Its task T1 said Files none while directing an update to decision.md;
other durable findings outputs and decision-conditional tasks were underspecified.
Codex loaded blueprint and ran a real local Unicode comparison probe, then wrote
stronger plan/tasks artifacts in one shell batch. They asserted a distinct local
review, followed only by status/diff-stat/line-count checks in the visible trace.
That assertion did not establish the required separate pass. This is an evidence
qualification, not a claim about hidden deliberation or intent.

The baseline candidate was 917acd6. Claude 2.1.312 configured opusplan observed
Sonnet 5.5; Codex 0.164.0 used configured gpt-6.1-sol. Original records and artifacts
remain in the separate operator ledger/worktree and are not relabeled. Neither
proposed Unicode policy is accepted or certified correct by this repair.

## Change and compatibility

The single common workflow now requires a distinct local validation of the actual
completed DEEP multi-session draft before Plan is marked complete. Record scope
and revision, concrete findings and corrections or a reasoned no-change result,
with evidence and limitations. A sentence, line count or future implementation
Review task is insufficient. Unfinished validation stays NOT RUN/draft.

Existing blueprint step 4 keeps profile-sized completeness review generally and
makes the DEEP pass operational: inspect drafted contents, reconcile write/output
paths, dependencies, decision branches, checks, expected/done/rollback criteria,
ownership/base/worktree, authority and next action. Files none is valid for a true
no-write task, not recording decisions or findings. Accepted decisions remain
reusable and uncertainty explicit. This is validation inside Plan, not a new
lifecycle stage or authority to invoke Build, product Review or another actor.
QUICK remains a short session plan/check without a forced dossier or ceremony.

The existing S04 case and source/negative guards encode the missing boundary.
All 34 case IDs and shared skill/command identities remain unchanged. No copied
skill, evaluator, extra dependency or Unicode implementation is introduced.
Paired manifest versions: development-lifecycle 1.2.12 and agent-toolkit 1.1.5.
Codex hook/command policy, defaults and optional providers remain unchanged.

## Verification and next evidence

- PASS: `python3 -B -m unittest discover -s tests -v`, exit 0: 73 tests total,
  70 passed and three opt-in native metadata checks skipped (NOT RUN).
- PASS: negative samples detect replacing incomplete/draft review status with a
  completion assertion or removing the durable task-output requirement. Existing
  scenario source-guard deletion checks cover core and blueprint references.
- PASS: changed Markdown local file/fragment checks and whitespace checks.
- NOT RUN: native metadata and actual Claude/Codex model reruns on this repair.

LIVE-F11 remains OPEN pending post-merge trials. Retain the same artifact-only
DEEP + SOLO task, inspect actual post-draft local content-review evidence and
findings/corrections or reasoned no-change, and verify exact task/output and
conditional-decision consistency. A plan review must not cause source edits,
workers or premature lifecycle advancement. Separately retain proportional
STANDARD/QUICK behavior. Static instructions alone do not establish obedience.

Rollback is a scoped revert and reinstall of the prior package in disposable
profiles, preserving failed evidence and user worktrees. It restores the known
planning gap rather than release acceptance. Primary remains clean on main;
remaining required live/platform/rollback evidence and release authority still apply.
