# Cold handoff: current state belongs to each actor

Base: `eb94fac1127ea836e19b4fa9ec27ab0b7c94feb5` (merged PR #30).
Scope: user-authorized repair PR after both S06/cold-resume trials failed.

## Observed gap and repair

Both hosts performed real sender-to-fresh-receiver transfers without passing chat
history. Assignment, actor scope, receiver RED/GREEN tests and preservation checks
passed. The overall results remain FAIL under the existing pre-write requirement:

- Claude's sender wrote its snapshot without verifying primary cleanliness or
  default/base source. Its receiver also omitted default/base source discovery.
- Codex's sender verified those facts. Its receiver inspected writer state and
  primary branch/HEAD but inherited the sender's historical primary-clean claim
  instead of checking current primary status before its first patch.

The native traces show both actors reading the full common contract. Its wording
said "first edit", while the separate receiver checklist omitted primary status
and default/base verification. Snapshot creation and resumption could consequently
look like exceptions or partial alternatives to the shared preflight.

The [contract](../../../plugins/development-lifecycle/rules/common/workflow.md#safety-and-worktree-first)
now applies the same existing facts to each actor's first write, including a
snapshot. The [receiver preflight](../../../plugins/development-lifecycle/resources/workflow/handoff.md#receiver-preflight)
links that rule rather than maintaining another incomplete Git checklist. Sender
observations are historical; the receiver checks current state. Scope/ownership,
gates and exact-next-action checks remain local to the handoff procedure.

No narrated checkpoint, new artifact, hook, runner or permission is introduced.
Equivalent actual evidence still counts; the no-remote fallback and stop on
unresolved state remain unchanged. Lifecycle's paired manifests become 1.2.17.
Instruction lines: contract 305→305, handoff resource 84→81; combined 389→386
(45 fewer words). This is a targeted clarification, not the deferred catalog audit.
Historical trial records remain unchanged in the operator's evidence worktree;
their raw transcripts are not published in this PR.

## Validation and limits

`WORKFLOW_NATIVE_TESTS=0 python3 -B -m unittest discover -s tests -v`:
75 tests, 72 PASS and three opt-in native-metadata skips. A new disposable-Git
regression changes primary after a clean sender observation: writer status and
worktree-list/HEAD remain unchanged, but a current primary-status query detects
the user change. Existing contract/receiver-link checks cover the packaged route.
Markdown lint, local links/fragments, paired manifest JSON and whitespace: PASS.

New native/model trials: NOT RUN. Post-merge S06 reruns must use fresh fixtures,
real sender snapshots and fresh assigned receivers under accepted bounded scope.
Static tests do not close LIVE-F07 or prove model behavior. Release stays BLOCKED
by the campaign's failed/unrun and platform/rollback gates. The all-plugin context,
duplication and splitting review remains deferred until all campaign tests finish.
