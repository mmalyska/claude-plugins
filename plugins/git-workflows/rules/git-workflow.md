# Git Workflow

## Action authorization

Readiness alone authorizes no commit, push, PR, review publication, merge or runtime mutation.
Use the current request and accepted task scope to identify the exact action set;
explicit exclusions constrain every row. Reuse existing authorization within scope;
do not ask again for the same action. Missing authority is a boundary, not a
reason to start an alternate CLI/worker or silently expand delivery.

| Action | Allowed scope when authorized | Does not imply |
| --- | --- | --- |
| Readiness | Inspect/validate and report | Commit, push, PR, external review, merge or runtime |
| Commit | Exact verified task content and index handling | Push, PR, review publication, merge or cleanup |
| Push | Selected task branch/remote and authorized commits | New commits, PR, history rewrite or default-branch push |
| PR | Requested PR and necessary task-branch push; commit only within accepted task scope | Review publication, merge, deployment or cleanup |
| Review publication | Requested external review event for the verified PR/content | Code changes, merge or deployment |
| Local/remote merge | Exact authorized integration target and scope | Cleanup or separate runtime mutations |
| Runtime/destructive mutation | Separate fresh permission for operation/target with impact and rollback | Further mutations or secret disclosure |

Prepare concrete reviewable work before requesting missing authority. Preserve
unrelated staged/unstaged/untracked content; never silently include it or reset,
stash or discard it. Stage/commit only authorized paths/hunks. Use task branches;
ordinary delivery must not push directly to main/default. Readiness/commit/PR
requests do not authorize branch cleanup or removing external worktrees.

Do not automatically rebase, reset, merge or force-push after divergence.
Such history changes need explicit scope, actual state inspection and subsequent
verification; force-with-lease alone grants no authority. Failed or required but
unrun checks limit readiness. No blanket override may bypass mandatory safety or project gates.

A GitOps/HCP auto-apply merge is runtime mutation and needs separate fresh explicit authorization with impact and rollback.
The same applies to credential rotation and destructive actions. Plan approval,
GO, a PR, actor permission or a plugin rollback is not runtime consent/rollback.

## Commit conventions

Use conventional `type: imperative description`, optionally a body for context.
Types: feat, fix, refactor, docs, test, chore, perf, ci. Respect attribution and
signing policy in the current host; do not assume global Claude configuration.
Verify selected content and result rather than staging everything by default.

## PR preparation and evidence

Analyze full task history and `git diff <verified-base>...HEAD`, inspect actual
requested base/head/repo and existing PR, honor templates and prepare title/body
with meaningful checks, scope, risks and rollback. Report PASS/FAIL/NOT RUN/NOT
APPLICABLE honestly and read back the actual external result. Pending CI is not
passed CI. Review publication requires its own scope; a PR number is only context.

See [development-workflow](./development-workflow.md) for the shared stage
responsibilities and [worktree policy](./worktree-workflow.md) for isolation,
provenance and explicit primary-maintenance boundaries. Both apply even when
Claude's hook fails open or Codex's bundled hooks are disabled.
