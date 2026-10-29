# Prepared trial actors: installed guidance and command context

Base: `d0a96c795afcd01ef841dd0630fa3180a1d52ddc` (merged PR #32).
Scope: user-requested repair after Claude S07/isolated-writers subrun01.

## Diagnosis

The two real writers overlapped and stayed in disjoint worktrees; the integrator
consumed their actual outputs and passed the final gate. The overall FAIL remains:
writer B proceeded without required lifecycle guidance, and the integrator edited
with unresolved own-worktree Git facts. Independent checks do not fill these gaps.

Each task requested the installed development-lifecycle-rules skill by name, but
provided no verified installed entry path. Writer A found its isolated profile's
cache; the integrator used the namespaced native Skill entry. Writer B guessed
`/root/.claude`, received EACCES, and explicitly continued without the contract.
Installation was verified independently; that does not prove actor discovery.

The integrator's allowlist permitted current-directory `git status*`,
`git rev-parse *` and branch queries. Absolute `git -C` forms covered primary and
source writers, not its own worktree. The actor-visible inventory rendered only
those external forms. Its own absolute-path queries were denied; it disclosed the
gap but did not use the already permitted current-directory checks before editing.
The inventory was accurate but incomplete as a concise guide to command context.

Existing runtime guidance already requires loading the contract and stopping
writes when prerequisites remain unresolved. These observed model failures are
not excused by setup discoverability, and another safety paragraph is unwarranted.
Writer B's piped test output also lacked an isolated runner exit; no successful
native gate is inferred from that group. The direct integrator and independent
gates remain separate evidence. Raw transcripts stay in the evidence worktree.

## Setup repair

The [operator guide](../live-trials.md#3-isolate-the-host-and-load-the-actual-candidate)
now supplies verified per-actor installed entry locators for prepared-entry trials.
The locator comes from actual installation metadata and candidate-content checks;
it supplies no workflow answer, state claim or contract body. Actual actor loading
must still be captured. Native direct-entry/discovery cases retain their original
entrypoints; the locator must not hide a discovery failure in those cases.

The [permission inventory](../live-trials.md#actor-visible-permission-metadata)
example includes already configured current-directory forms, distinguished from
external-worktree forms. Generate each actor's inventory from actual launch
settings; do not add permissions to make the example work. This changes no
allowlist, sandbox, model, budget, actor/file authority or runtime rule/skill.
No plugin version bump is needed; loaded runtime instructions gain zero lines.

A fresh Claude S07 run must record this as a changed setup configuration, with
new profiles/logs and preserved historical FAIL. No LIVE run or behavioral closure
is claimed here. The all-plugin context audit remains after all campaign tests.

## Validation

`WORKFLOW_NATIVE_TESTS=0 python3 -B -m unittest discover -s tests -v`: 75 tests,
72 PASS and three opt-in native-metadata skips. Markdown lint, local links/fragments
and whitespace: PASS. No synthetic permission matcher or prose-only test was
added. Release remains BLOCKED by remaining failed/unrun/platform/rollback gates.
