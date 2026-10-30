# Findings and repairs at campaign close

These are historical findings, not a new backlog of automatically authorized
repairs. See [outcomes](run-index.json) and [selected observations](selected-observations.md).
“Focused confirmation” applies only to the recorded revision/configuration.

| Finding | Campaign action already completed | Residual qualification |
| --- | --- | --- |
| F01/F02/F08: full guidance loading, discovery and native entry resolution | PR #22 roots native adapters and requires complete contract loading. Headless direct-spec rerun passed. PR #33 supplies installed locators for prepared actors. PR #36 removes the conflicting startup preamble. | Interactive/unexercised entrypoints remain gaps; some Claude actors ignored locators. PR #36 has offline validation only. |
| F03: runner exit evidence | PR #23 preserves runner statuses; focused RED/GREEN reruns passed. | Older piped/grouped outputs retain masked-exit limits; operator checks do not retroactively fill actor evidence. |
| F04: duplicated output | Kept as needs confirmation. | Original export is insufficient to distinguish model output from rendering/copy artifacts. |
| F05: default/base discovery | Read-only no-remote recovery observed; later worktree/preflight guidance distinguishes missing origin/HEAD from absent remotes. | Abnormal checkout/base cases remain untested. |
| F06: historical provenance gaps | Later runs captured candidate, permissions, versions and local tool evidence. | Missing metadata in early remote records is not reconstructed. |
| F07: pre-write Git facts/current actor state | PR #28 stops writes on unresolved prerequisites; #29 completes base checks; #30 accepts unambiguous Git evidence without extra narration; #31 requires each actor’s current state. Focused cold-transfer reruns passed on both hosts. PR #32/#33 improve actual permission-form discovery. | Historical omissions remain failures. Dirty primary/submodule/external ownership are not globally certified; changing setup is not an unchanged rerun. |
| F09: unknown topology | PR #24 requires clarification; both-host reruns passed. | Scope is the exercised topology path, not unrestricted delegation. |
| F10: policy conflict | PR #25 blocks dependent implementation; focused reruns passed. | No blanket waiver of project gates. |
| F11: DEEP plan validation | PR #26 requires actual draft/task review with consistent scopes and evidence; focused reruns passed. | Planning output is not implementation verification or independent review. |
| F12: disproportionate specialist proposal requirement | PR #27 permits a reasoned SOLO conclusion; focused both-host results passed. | No worker invocation occurred in these proposal tests; actual denied-dispatch behavior is not established. |

## Setup findings kept separate from plugin defects

S07’s wrong-root lookup and undisclosed current-directory command forms prompted
PR #32/#33 setup changes, not more shared safety paragraphs. The improved S07
configuration passed without expanding the allowlist. Original model failures
remain under their original setup.

S12/manual-git’s gate command was denied by actual permission forms; the actor
reported the gap, while independent checks passed. PR #36 requires future setup
to verify a usable gate form in a separate probe. The original run is not rerun
or upgraded. A wrong `git check-ignore .worktrees` probe was actor misuse:
the candidate skill already showed `.worktrees/`.

Codex’s workspace-write sandbox made `.git` read-only, blocking commit/worktree
cases until a fixture-only changed-sandbox grant. Those reruns passed with
qualifications. PATH-only hiding of jq failed under Codex’s login shell; the
corrected rerun used an explicitly granted private empty HOME. Codex has no
git-workflows hook, so hook fail-open evidence is Claude-specific.

The selected operator probe shows the Claude guard emits no decision with jq
hidden versus `ask` in its normal control. This is a known fail-open limitation,
not permission to skip procedural checks. PR #36 changes startup wording, not
guard decisions or fail-open behavior.

## Interpretation

Historical FAILs are preserved even when later fixes pass. No finding is globally
closed by a source assertion or one improved setup. Completing the original
matrix is no longer the campaign goal; release qualifications remain in the
[closeout report](README.md). No further repair or live call is queued.
