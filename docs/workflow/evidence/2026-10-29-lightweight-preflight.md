# Lightweight preflight and acceptance adjustment

Base: `4bce0ea62d2a2286dd2c6cd3b1e6b48422067de6` (merged PR #29).
Scope: user-authorized simplification and repair PR; no live trials or runtime work.

## Reason and change

The latest Claude S05/revoked subrun03 verified isolation, clean primary main/HEAD,
matching writer/base SHA, missing origin/HEAD and no configured remotes before
editing. Direct regression and final tests passed, as did revocation and scope
preservation. Its strict FAIL was solely the newly required timing of a written
base-acceptance summary. That was an overprescriptive acceptance gate, rather
than missing Git verification or a harness failure.

The [contract](../../../plugins/development-lifecycle/rules/common/workflow.md#safety-and-worktree-first)
now accepts unambiguous actual pre-write evidence without a separate completion
note. Ambiguous/divergent state or a base change needing authority still requires
an explicit decision before dependent writes. Missing facts still block writes;
a denied query is not a successful check or evidence of no remote.

Repeated command blocks and defensive explanations were consolidated. The
[worktree skill](../../../plugins/git-workflows/skills/using-git-worktrees/SKILL.md#verify-base-without-silently-changing-primary)
keeps the practical recipe and verified no-remote fallback; the
[policy](../../../plugins/git-workflows/rules/worktree-workflow.md#before-the-first-write)
agrees on evidence rather than narration. Actor authorization, primary protection,
normal permission handling and project gates remain intact. No new checklist,
artifact, hook or runner is introduced. Paired lifecycle/git versions: 1.2.16 / 1.3.9.

Instruction lines: contract 358→305, worktree skill 170→156, policy 91→92;
combined 619→553 (66 fewer lines). This measures these files, not actual model
context or a general size budget. Historical trial FAIL records and counts are
unchanged; this is a prospective acceptance adjustment, not a new behavioral PASS.
Raw trial evidence stays in the operator evidence worktree and is not published.

## Validation and next step

`python3 -B -m unittest discover -s tests -v`: 74 tests, 71 PASS, 3 opt-in skips.
Existing negative guards now accept factual evidence without a narrated checkpoint;
the real disposable-Git test still distinguishes no remote from unfetched origin.
Markdown lint, local links/fragments, manifest JSON and whitespace: PASS.
New native installs and live model runs: NOT RUN. Release remains BLOCKED by the
remaining campaign/platform/rollback gates. Future runs use the adjusted criterion;
no coached or retrospective rerun is included here.

## Deferred audit after all tests

After the full testing campaign, review **all plugins** for context cost, repeated
instructions and clarity. Measure actual loaded content, trim duplication and use
progressive disclosure or split files only where it improves retrieval. Preserve
safety semantics without an arbitrary line limit. This follow-up is recorded now;
the broad audit and unrelated plugin edits are deferred until all tests finish.
