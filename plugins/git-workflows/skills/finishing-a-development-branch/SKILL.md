---
name: finishing-a-development-branch
description: "Use when implementation is complete, all tests pass, and you need to decide how to integrate the work - guides completion of development work by presenting structured options for merge, PR, or cleanup"
---

# Finishing a Development Branch

Verify readiness, inspect provenance and execute only the selected authorized
operation. Preserve existing primary/worktree state. Follow
[worktree policy](../../rules/worktree-workflow.md) and
[git conventions](../../rules/git-workflow.md). This procedure grants no implicit
delivery, primary maintenance or cleanup authority.

## Step 1: Verify readiness and scope

Announce use of this skill and read the current requested action, task state and
verification evidence. Run applicable required checks in the isolated workspace;
use project commands and report actual results. Failed required gates block
readiness; missing ones remain NOT RUN. Do not fetch tools or start another
harness outside session authority. A readiness-only instruction stops here.

## Step 2: Inspect checkout and ownership

Record these facts before any switch, merge, branch creation or cleanup:

```bash
git rev-parse --show-toplevel
git rev-parse --absolute-git-dir
git rev-parse --git-common-dir
git rev-parse --show-superproject-working-tree
git branch --show-current
git status --porcelain
git worktree list --porcelain
```

Resolve git/common paths and primary location from metadata, and distinguish a
submodule from a linked checkout. Inspect actual default/base revision and the
primary's branch/status. Do not infer task ownership from directory name.

- Named, task-owned worktree: only requested operations are candidates.
- Detached/external worktree: preserve host ownership. Branch creation/push needs
  its own scope; no automatic branch attachment or local merge from ambiguity.
- Primary or unclear isolation: stop dependent writes; establish isolation using
  the existing using-git-worktrees procedure unless primary maintenance itself
  is explicitly authorized.
- Dirty/non-default primary: report and preserve it. Do not switch, stash, reset,
  clean or merge merely to satisfy a clean-default postcondition.

## Step 3: Honor the requested action

An already selected authorized action does not require another fixed menu.
If no delivery action is selected, report readiness and preserve the branch;
options can include local merge, PR, keep or explicitly requested discard. Do not
infer cleanup, external publication, merge or deployment from readiness or PR.

### Authorized local merge

Local merge requires explicit authorization, including its primary maintenance
scope. If merge triggers GitOps/HCP auto-apply or other runtime effects, obtain
separate fresh runtime permission with impact and rollback before mutation.

Only proceed when the intended primary is clean and already on the verified
base/default branch. Respect normal host permissions; a hook exception is not
itself authorization. Inspect local versus remote base state. Update the base
with `git pull --ff-only` when authorized; stop on divergence or failed update.
Then perform only the authorized merge, using fast-forward where possible:

```bash
git -C <verified-primary> pull --ff-only
git -C <verified-primary> merge --ff-only <verified-task-branch>
```

If fast-forward is impossible, report the divergence and agree on an allowed
integration strategy; do not silently rebase, reset or force a merge. Verify the
merged revision using appropriate checks in an isolated checkout rather than
running state-generating tests in primary. Record merged SHA and results.
Successful merge does not itself authorize deleting a worktree or branch.

### Authorized PR

Verify intended base, branch, diff and delivery scope, then use the existing PR
procedure or the current host's available GitHub tool. A PR request may cover its
necessary branch push; it does not cover merge, discard or cleanup. Inspect a
pre-existing PR before creating another. Preserve the worktree for feedback.

### Keep

Report current branch/HEAD, worktree path and readiness/remaining uncertainty.
Keep all work and leave primary untouched. Do not force a return to default.

### Explicit discard

Before destructive discard, identify exact branch, commits, local changes and
worktree to remove. Require explicit authorization covering those targets; do
not infer it from “finish”, merge, PR creation or a path under `.worktrees/`.
Apply the ownership/cleanup checks below; if scope or provenance is unclear,
preserve work and report the blocker. Never use forced cleanup as a default.

## Step 4: Optional authorized cleanup

Directory location alone is not proof of cleanup ownership. A worktree under
`.worktrees/` or `worktrees/` may belong to another task, session or harness.
Verify recorded creation provenance, current ownership, branch/HEAD, all local
changes (including untracked files), and active consumers before removal.

Cleanup requires explicit authorization for the verified owned target. Preserve
external, unknown or active worktrees. For a merged branch, verify successful
integration and checks first; for discard, verify scope covers lost commits and
local changes. Stop if dirty state is not covered, ownership changed, another
session is using it, or any check cannot be established. Do not force removal.

Run a targeted worktree removal from a safe location outside that worktree only
after those checks. Avoid broad pruning of other worktree metadata. Branch
removal is separate: verify no worktree uses it and remove only the authorized
branch; use a safe merged-branch deletion after integration. Unmerged deletion
needs explicit destructive authority and must not be inferred from cleanup.

## Step 5: Read-only primary verification

Reinspect primary branch, HEAD and status and compare them with the initial
observation. Report any discrepancy; do not restore primary by switching,
stashing, resetting, cleaning or merging to hide it. If it was initially clean
on default and no authorized maintenance occurred, it must remain so. If the
user authorized primary maintenance, report the exact permitted change and
result; do not widen that exception. Preserve and report unrelated existing state.

## Quick reference

| Requested action | Primary mutation | Worktree/branch removal |
| --- | --- | --- |
| Readiness / keep | None | None |
| PR creation | No implicit primary mutation | None; keep for feedback |
| Local merge | Explicit scoped primary maintenance only | Separate cleanup authority/provenance required |
| Discard | No implicit primary mutation | Exact destructive scope and provenance required |

Missing jq, absent native hooks or a failed-open guard never waive procedural
isolation, task ownership or user permissions. Codex follows these checks with
bundled hooks disabled. Never claim an action, cleanup or test result not observed.
