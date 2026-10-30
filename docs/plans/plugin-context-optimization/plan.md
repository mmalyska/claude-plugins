# Plugin context optimization plan

## Resume state

```yaml
task: plugin-context-optimization
profile: standard
topology: solo
owner: current Codex operator
integrator: current Codex operator
base_sha: d82efc568f29c3b6dbd7f1ded7726474820d0a3a
branch: docs/plugin-context-audit
worktree: /workspaces/claude-plugins/.worktrees/docs/plugin-context-audit
status: complete
next_action: prepare the user-requested PR with offline results
```

This is the existing `docs/plans/` convention, not a new `.plans` directory.
The user requested a plan for all fixes in the [context audit](../../audits/plugin-context/README.md).
The pinned base is the PR #37 publication head; GitHub verified its merge as
`ae10c049c4e0d1667d7544199a980854d96794c3`. Do not use the older uncommitted
campaign-evidence worktree as implementation source. Do not update primary.

## Objective and acceptance

Reduce the instructions/examples a task must read while preserving existing
capability, stable entrypoints and campaign safety fixes. Optimize useful reads,
not disk size, line counts or an invented token quota.

- All C01–C07 findings receive an implemented correction or evidence-based
  no-change disposition under an explicit task criterion below.
- The 70 canonical skills, 23 native adapters, native role names/tools/models,
  standalone owner behavior and Codex import opt-outs remain intact.
- Extracted examples/templates remain reachable through plugin-local references;
  no new SKILL.md catalog entries, cross-plugin hard dependencies or automatic
  read-all expansion. Account for every original section/example before moving it.
- Compare initial core and representative single-topic read sets using exact
  characters/bytes and the same rough estimator as the audit. Show full expansion
  cost too. Do not report the aggregate source reduction as baseline/session or
  billing savings. A split must lower its declared normal read set, not only its
  entrypoint size; if it does not, revise it or retain the original.
- Required first complete contract loading, policy conflict handling, current
  pre-write facts, actor/permission boundaries, actual check status, DEEP draft
  review and independent/runtime evidence distinctions remain enforceable in text.
- Static packaging/content/link/invariant checks pass. No native host/model call
  is required or claimed. Live compliance and remaining release gates stay qualified.

Non-goals: changing guard decisions, shrinking context through weaker project
gates, rewriting every skill, altering framework behavior, installing/uninstalling
plugins, touching user/home configuration, another live campaign, changing models,
editing historical evidence, runtime operations or publication in this Plan stage.

## Architecture and decisions

Keep SKILL.md as a useful bounded procedure with applicability, essentials and a
topic selector. Keep material needed on every branch inline. Put conditional
examples and optional detail inside the same skill's `references/` directory.
A selector identifies when each reference is needed;
referenced content is not a mandatory checklist of files to read.

Review policy/procedure/transport/domain detail get distinct owners. Use direct
bounded scope selection without a review↔reviewer loading cycle. Retain per-mode
gate behavior until an explicitly accepted policy change says otherwise; this
plan does not silently standardize warning versus blocking semantics.

Keep standalone inline boundaries, shortening only when all mapped meanings
survive and a useful read-set reduction remains. Do not centralize them in a new
global rule. Keep the workflow contract and startup rule content unchanged;
same-revision reuse clarification belongs in entrypoints, never a first-load bypass.

See [decisions](decisions.md), [exact task scopes](tasks.md) and the
[review of this plan](plan-review.md). Proposed designs are not implementation grants.

## Writing guidance applied to the skills and this plan

Apply [writing-for-agents](https://github.com/mattpocock/skills/blob/main/skills/productivity/writing-for-agents/SKILL.md)
and its [skill mechanics](https://github.com/mattpocock/skills/blob/main/skills/productivity/writing-for-agents/SKILL-MECHANICS.md)
as authoring guidance. [All-skill review matrix](writing-assessment.json) assigns
all 70 audited identities to T11, including ones outside the initial size hotspots.
The matrix records the observed Git blob IDs for both external documents.

- Give each pointer a clear subject and distinct trigger branches. Fix weak
  routing before adding always-loaded text; omit synonyms that name the same case.
- Keep every-branch prerequisites inline. Disclose conditional reference only
  when branch selection and human discoverability justify another file. A flat
  checklist is valid; fenced examples and file length alone are not split tests.
- Keep a concept's definition, constraint and caveat together. Give each policy
  one owner while retaining essential standalone/direct-entry safety boundaries.
- End each actionable step with observable, exhaustive completion evidence.
  Sharpen vague criteria before splitting a sequence. Linking a later step does
  not create a real context boundary or prevent premature completion.
- Use familiar task vocabulary and direct positive actions. Keep explicit hard
  exclusions where they protect consent, secrets, isolation or required gates.
  A shorter slogan is not an equivalent safety boundary.
- Read discoverable commands/configuration from the environment when needed;
  preserve non-obvious conventions, reasons and gotchas. Treat possible default
  restatements as review candidates, not proven no-ops without behavioral evidence.
- Assess invocation reach, but retain the supported shared frontmatter and all
  current identities. The guide's invocation flags/visibility claims are not
  assumed portable to Codex or verified for current host versions. No new router
  skill or manual-only conversion is included in this plan.

For execution, read this plan, the shared task contract and the current task's
section, plus its prerequisite evidence. Read other task sections when resolving
a dependency/conflict. The full sequence remains a human-reviewable index; this
navigation convention is not a claim that earlier context disappears.

## Order and dependencies

Execute serially in SOLO. Dependencies describe prerequisite evidence, not actor
permission. Suggested reviewable implementation slices:

| Slice | Tasks | Purpose |
| --- | --- | --- |
| 1 | T01 → T02 → T03 | Baseline/invariants, small routing corrections, frontend/backend pilot split |
| 2 | T04 → T05 | Apply the proven split approach to other domain and lifecycle example libraries |
| 3 | T06 | Consolidate review routing without changing gate semantics |
| 4 | T07 → T08 | Reduce meta-workflow reads, then evaluate boundary compression |
| 5 | T09 → T11 → T10 | Improve descriptions/setup choices, review all 70 skills for authoring quality, integrate results |

T04/T05 require T03's content/read-set proof. T06 requires T01 and the policy map;
it follows T05 to avoid conflicting lifecycle edits. T07 requires T01/T05;
T08 requires T06/T07 and may retain exact wording when not worth changing.
T09 requires T02/T08, preserving any safety wording found necessary there.
T11 reviews every skill after T09; T10 consumes every task's final disposition.
A failed slice blocks dependent changes; it does not authorize silently
broadening scope or fetching tools.

Each slice produces local reviewable changes and evidence. Separate commits/PRs
are a delivery proposal only; user approval is needed before publication.

## Files, ownership and measurement

The current operator owns all plan/artifact writes. Each implementation task in
[tasks.md](tasks.md) lists exact existing files, new reference paths, outputs,
dependencies, evidence, completion and rollback. No concurrent writers or actors.

Keep the audit's `inventory.json` immutable as baseline. Extend the measurement
script with an explicit output argument so after-results cannot overwrite it.
Track each initial read, selected reference set and all-detail expansion separately.
Representative cases include React component composition, a backend repository
pattern, C# async/disposal, one test framework example, one Docker topic, one
deployment recipe, a local review, a PR review, a rules-distillation match and a
core-plus-one-domain setup request. These are static read-set scenarios, not new
LIVE scores or simulated model obedience.

## Checks and evidence

Task evidence is written beneath this plan as named in tasks.md. Record command,
content revision/hashes, host-independent/offline nature, numeric exit/result and
reason for NOT RUN/NOT APPLICABLE. Do not lose a test-runner exit in a pipeline.

| Gate | Planned command/method | Current status |
| --- | --- | --- |
| Baseline source and all moved-content accounting | Source hashes + section/example manifest; verify destination coverage and identity | NOT RUN for implementation; audit baseline exists |
| Reference packaging and topic read sets | Proposed `tests/test_context_layout.py`, standalone path containing spaces; no host CLI | NOT RUN; T01 creates check |
| Existing workflow/permission invariants | `WORKFLOW_NATIVE_TESTS=0 python3 -B -m unittest discover -s tests -p test_workflow_contract.py -v` | NOT RUN on future implementation |
| Catalog/native adapter/manifest parity | `WORKFLOW_NATIVE_TESTS=0 python3 -B -m unittest discover -s tests -p test_codex_manifests.py -v` | NOT RUN on future implementation |
| New layout coverage | `python3 -B -m unittest discover -s tests -p test_context_layout.py -v` | NOT RUN; test does not exist yet |
| Other affected static tests | Inspect test side effects and run only applicable existing tests | NOT RUN, determine per slice |
| Markdown/JSON/secret/whitespace integrity | Local link/fragment/JSON checks; installed Gitleaks; `git diff --check` | NOT RUN on implementation; plan checks separate |
| Actual native loading and token usage | No host/model launch; preserve unknowns | NOT RUN by design; no compliance or billing claim |

Run relevant checks once per meaningful slice; repeat after new changes/failures,
not by ritual. No dependency download or scanner fetch. Existing offline tests may
create/remove their own fresh ephemeral fixtures; future implementation scope
must explicitly cover that normal test lifecycle. Never remove prior campaign
fixtures, worktrees or evidence. Do not run unrelated cleanup/guard suites merely
to increase counts when guard source and registrations remain unchanged.

## Versioning, rollout and rollback

Within each completed slice, synchronize the Claude/Codex patch version for each
actually changed plugin. Exact baseline versions are in T01's output; do not bump
unmodified owners or repeatedly bump a plugin during one unpublished slice.
Keep Android and already-narrow Renovate domain content unchanged. T08 may
evaluate only the Renovate auditor's mapped inline boundary; no preset or
automerge checklist rewrite is included.

Before each later slice, inspect current branch/base/content to account for earlier
accepted slices. Do not merge main, rebase, reset or rebuild existing worktrees
without scope. Preserve the pinned original audit and campaign evidence.

Rollback is a reviewed patch restoring that slice's previous plugin files,
references, paired versions and associated checks together. Do not use destructive
reset/cleanup, delete shared historical artifacts or auto-remove worktrees. New
reference removal needs verified ownership and an applicable explicit grant.
Documentation rollback cannot reverse any external runtime state; none is planned.

## Authority and next action

The user subsequently authorized execution and PR preparation. The staged tasks
are complete with offline results and explicit retain decisions. Commit, branch
push and draft PR preparation are now within scope; model trials, host installs,
global configuration, merge/deploy and prior-fixture cleanup remain excluded.
Previous campaign grants do not carry over.

Suggested future implementation grant: all 11 tasks in staged order
T01–T09 → T11 → T10 under the exact scopes in tasks.md, fresh local offline test
fixtures with their ordinary self-owned cleanup, paired version updates and
plan/evidence recording. Preserve primary, existing
worktrees and original archives; no live trials or delivery. This is reviewable
proposed scope, not permission to execute it.

Next action: prepare the requested PR with [outcome](results.md) and
[implementation review](implementation-review.md). State 47 remains unused.
The campaign remains closed with qualifications. The future-grant paragraph
above is retained as the original scope proposal, now accepted for this execution.
