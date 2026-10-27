---
name: pr
description: "Create a GitHub PR from current branch with unpushed commits — discovers templates, analyzes changes, pushes"
---

# Create Pull Request

Read [git delivery boundaries](../../rules/git-workflow.md) and
[worktree policy](../../rules/worktree-workflow.md). Use current task input
(`$ARGUMENTS` in Claude, accompanying skill text in Codex); keep existing names.
Default STANDARD + SOLO. PR readiness does not itself authorize publication.

## Step 1: Establish PR scope

A request to create a PR authorizes that PR and its necessary task-branch push.
Committing local changes requires that the current request or accepted task
scope includes committing those changes. An explicit “existing commits only” or
“do not commit/push” restriction takes precedence; do not manufacture missing
commits or bypass the restriction. Reuse accepted authority without another menu.

Parse explicit base and `--draft` intent. Resolve actual repository default/base
from metadata/policy when omitted, rather than guessing a branch. Verify isolated
task branch differs from the target/default and ordinary delivery never pushes
directly to main/default. Read shared project policy before host adapter details.

## Step 2: Inspect content and existing PR

Inspect task branch, full commits/base diff, working/staged/untracked changes and
required checks. Use the actual base comparison; a last commit is not the whole
PR. Preserve unrelated local state: no automatic stash, reset, stage-all or commit.
If the requested content is uncommitted, prepare only the authorized task commit
through the existing commit procedure, otherwise report the missing scope.
A PR of verified existing commits can preserve unrelated local edits if project
policy allows and the PR excludes them; disclose that state rather than hide it.

When a GitHub tool is available, inspect the actual repo/base/head and any existing
PR first; reuse its identifier and do not silently create duplicates or update
unrelated PRs. Verify external tools/connections and schemas before use; absent
capability means a clear prerequisite or local prepared report, not fake success.

If the branch contains unrelated commits, report the scope problem before push
or PR; do not silently rewrite history to hide it.

Read the repository's existing PR template (if any), related accepted artifacts,
commit history and diff. Preserve established `.plans`, reports and legacy PRP
locations as context, not a mandate to migrate them. Draft title/body for the
actual final scope, meaningful verification, risks and rollback. Do not claim
unrun checks passed. Use conventional commit-style titles when appropriate.

## Step 3: Push within authorization

Push only the verified task branch to the intended remote when necessary for the
authorized PR. If push is rejected or histories diverge, inspect and report why.
Do not automatically rebase, reset, merge or force-push after divergence.
History rewriting requires explicit authorization for that branch and operation;
if granted, reverify task content, accepted head and affected checks before
retrying. A force-with-lease flag is a safeguard, not permission to rewrite.

## Step 4: Create the requested PR

Prefer an available sufficient GitHub integration, otherwise a configured CLI.
With `gh`, use a prepared body file rather than shell interpolation of Markdown:

```bash
gh pr create --repo <verified-repository> --base <verified-base> \
  --head <verified-task-branch> --title <prepared-title> --body-file <prepared-body-file>
```

Apply `--draft` only when selected. The placeholders are verified inputs, not
literal commands to execute blindly. If a required action/permission is missing,
finish a local reviewable title/body/diff first, report the prerequisite, and stop
before that external operation. Do not install/login/connect a service implicitly.

## Step 5: Read back and stop

Verify actual URL, base/head, content scope, state and checks; unavailable/pending
checks remain honestly labeled. Report created or existing PR and limitations.
PR creation does not authorize merge, review publication, deployment or cleanup.
Preserve the branch/worktree for feedback. A GitOps/HCP-triggering merge is runtime
mutation requiring separate fresh explicit permission with impact/rollback.
