# Test runner exit-status repair

Base: `f3025394e5ce6f10c3e61db5621b59028c0d1f96`.
Branch/worktree: `fix/workflow-test-exit-status`,
`.worktrees/fix/workflow-test-exit-status`.
Profile/topology: STANDARD + SOLO. Scope: guidance repair, regression verification
and the user-requested fix PR. Model reruns remain pending; no merge or runtime
action is included.

## Problem and change

LIVE-F03 persisted in the post-merge focused trials: Claude did not read the
optional testing rule and still piped tests through tail. Codex read the rule but
grouped the GREEN test with later Git commands. Final functional results were
independently verified; those model shell exits did not isolate the runner exit.

The mandatory core workflow now states the exit-capture requirement directly.
Short checks run in their own tool call, with Git diagnostics in another call.
The contract covers RED and GREEN, filters and semicolon groups, and an explicit
status-capture/return example that also works under shell errexit. Lost status
requires a properly captured rerun before claiming verified success.
The optional testing rule links to that canonical procedure instead of duplicating
it. Paired development-lifecycle manifests advance to 1.2.9; skill identities,
commands, hook policy, default profile and topology are unchanged.

## Checks

- PASS: `python3 -B -m unittest discover -s tests -v` returned exit 0.
  73 tests total: 70 passed, three opt-in native metadata tests skipped (NOT RUN).
- PASS: the new executable documentation regression used actual passing/failing
  unittest fixtures with shell errexit both enabled and disabled. The succeeding
  report command preserved runner exit 0 or 1 respectively in all four variants.
- PASS: a negative contract sample detects removal of the runner-status boundary.
- PASS: `git diff --check` and changed Markdown local file/fragment checks.
- NOT RUN: native metadata and actual Claude/Codex model reruns on this repair.
  These are distinct from testing the shell example or source reachability.

## Closure and rollback

LIVE-F03 remains pending live verification. Fresh loaded-contract trials must
show both hosts using a separate runner call or explicit capture/return, for
observed failing and passing checks. Retain the old outputs and independent
verification; do not relabel historical compound shell exits as runner exits.

Rollback is a scoped revert of this repair and reinstall of the prior package
in disposable profiles, preserving evidence and user worktrees. No new wrapper
service, copied skill or testing dependency is introduced. Primary stays clean
on main; release acceptance remains subject to the existing unrun gates.
