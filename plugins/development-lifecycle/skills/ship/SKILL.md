---
name: ship
description: "Review delivery readiness, verify checks, and perform the authorized commit, PR, or branch-finishing workflow"
---

# Ship — Readiness and Authorized Delivery

Read [the workflow contract](../../rules/common/workflow.md) first. Ship is the
final stage of the single lifecycle, not an automatic commit/push/PR pipeline.
Default STANDARD + SOLO; QUICK/DEEP change depth, not actors or permissions.
Use the current request as input (`$ARGUMENTS` in a Claude command, accompanying
skill text in Codex). Existing names remain; do not execute slash names in a shell.

## Step 1: Establish action and scope

Read the current request, accepted task state and applicable project policy.
List the exact authorized actions and exclusions before any side effect.
Readiness alone authorizes no commit, push, PR, review publication, merge or runtime mutation.
A generic “ship” or GO recommendation is readiness-only unless the request or
existing accepted delivery scope names an action. Reuse explicit authorization
for that action and scope; do not ask again for an already authorized action.
If an action is missing authority, finish the reviewable readiness result first,
then request only the missing decision. No compulsory Proceed/Override menu.

Inspect branch/isolation, unstaged/staged changes and task-relevant untracked
files. Honor an explicit target first; when clean use the actual task-base diff,
not an unrelated last commit. Review current changes without staging them:

```bash
git status --short
git diff --name-only
git diff --cached --name-only
git ls-files --others --exclude-standard
```

Preserve unrelated work, including staged changes. Do not automatically include untracked files.
Readiness does not require staging or committing. If task boundaries or staged
content are ambiguous, report them before dependent delivery operations.

## Step 2: Verify evidence appropriate to the change

Reuse valid Test/Review evidence for the same content, scope and configuration.
New changes invalidate affected evidence; rerun those checks, not every check by
ritual. QUICK uses the smallest meaningful check, STANDARD appropriate automated
checks/project gates, and DEEP layered risk-based evidence plus rollout/rollback.
Docs-only work may use Markdown/link checks; do not invent a code-test requirement.
Mandatory project security/coverage gates still apply in every profile.

Discover installed project commands from instructions, tests and configuration,
including a repository unittest suite (`python3 -B -m unittest discover -s tests`).
Inspect runner side effects before running: some discovery tests launch other
harnesses. Run only permitted applicable checks, no implicit installs or forbidden
CLI/service launches. A required but unavailable check is NOT RUN and limits
readiness; an unrelated check is NOT APPLICABLE with a reason. Record commands,
exit codes and actual results; never fabricate a green suite or scanner outcome.

## Step 3: Review and readiness decision

Use [review](../review/SKILL.md), [code-review](../code-review/SKILL.md) or the local
review role as appropriate. Assess correctness/readability, relevant security and
test completeness at the selected depth; reuse valid prior review evidence.
SOLO performs review passes sequentially in the current session. A separate
reviewer or parallel passes require explicit authorized topology and exposed
capability; do not launch another agent merely because Ship was selected.
Disclose when review is not independent. Review changes need fix scope and reruns
of affected checks; a no-op Simplify assessment is valid.

GO means required gates for the assessed scope passed and no blocking findings
remain; it grants no additional authority. NO-GO identifies failures, unrun
required checks and missing decisions. No blanket override may bypass mandatory safety or project gates.
A justified finding reassessment needs evidence; calling it an override is not
permission to ship a vulnerability or waive required verification.

Report scope/content revision, selected profile/topology, evidence reused/rerun,
readiness, impact/rollback, outstanding limitations and the exact action set.
When no action is authorized, stop with that report and preserve the worktree.

## Step 4: Execute only the authorized action

Keep commit, push, PR creation, external review publication, local/remote merge,
runtime mutation and discard distinct. A PR request may cover its necessary
branch push; a task commit is allowed only when the request/accepted delivery
scope includes committing those changes. Explicit exclusions always constrain it.
Commit-only does not authorize push/PR. Creating or approving a PR does not
authorize merge. Review-only does not authorize publication.

Use the existing commit/pr/finishing procedures when installed, otherwise follow
these same scoped checks with actual host tools. No hard provider dependency or
new skill is required. Stage only task scope and protect the default branch;
never push directly to main/default as part of ordinary task delivery. Do not
silently rebase or force-push after divergence; those need explicit history-change
authority. Preserve prior staged/untracked content and external worktree ownership.
Cleanup/discard requires its own exact target authority and provenance.

A GitOps/HCP auto-apply merge is runtime mutation and needs separate fresh explicit authorization with impact and rollback.
The same applies to destructive actions and credential rotation. Plan approval,
GO, commit/PR authority or delegation permission is not runtime consent. Prepare
all reviewable work before asking for missing authority, then stop until it arrives.

## Step 5: Verify and report

Read back the actual resulting SHA/branch/PR/review identifier when an action was
performed, and compare it with the approved target and content. Report unexpected
results and stop dependent actions. Do not claim an external operation from a
prepared command, and do not mutate primary or remove a worktree to tidy status.
Preserve artifacts for resumption. Plugin/document rollback cannot undo runtime
changes; any runtime rollback requires its own scope and authorization.
