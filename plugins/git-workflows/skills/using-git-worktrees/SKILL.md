---
name: using-git-worktrees
description: "Use when starting feature work that needs isolation from current workspace or before executing implementation plans - ensures an isolated workspace exists via native tools or git worktree fallback"
---

# Using Git Worktrees

Ensure an isolated checkout before writes. Detect existing isolation first, then
use a suitable native tool actually exposed in the current session, otherwise
manual git worktrees. Follow [worktree policy](../../rules/worktree-workflow.md).
Default STANDARD + SOLO; a worktree tool does not authorize another actor.

## Step 0: Inspect current state

Announce use of this skill, then inspect without altering checkout state:

```bash
git rev-parse --show-toplevel
git rev-parse --absolute-git-dir
git rev-parse --git-common-dir
git rev-parse --show-superproject-working-tree
git branch --show-current
git status --porcelain
git worktree list --porcelain
```

Resolve git/common directories to absolute physical paths before comparing them.
A linked worktree has distinct git and common directories, but this difference
alone is not proof of isolation: inspect the superproject result for submodules.
For a submodule, verify actual submodule and superproject isolation/ownership;
do not confuse submodule metadata layout with an independent linked worktree or
silently mutate its superproject. If isolation cannot be established, stop writes.

Before any write, perform the primary/base checks below even if isolation already
exists. A `.worktrees` path, feature branch or silent guard is not verification.
If already in a suitable linked worktree, reuse it rather than nesting another.
Record absolute path, branch (or detached HEAD), base SHA and ownership. A detached
or externally managed checkout is not permission to create a branch, reset state
or remove that checkout; use only the requested scoped work there.

If in primary, create isolation before writes. There is no sandbox exception to
this rule. Explicitly authorized primary maintenance is a separate operation,
not a fallback when isolation fails. Preserve all existing dirty state.

## Step 1: Select the isolation mechanism

Use native worktree creation only if the actual exposed tool is suitable:

1. Verify its destination and local exclude behavior; it must not dirty primary.
2. Verify its base revision includes required accepted/unpushed task state.
3. Verify it creates only a checkout, not another harness/worker or unauthorized
   cleanup. A CLI flag is not an in-session transition tool.

If no suitable native tool is exposed, use manual git worktree creation. Do not
start a second CLI session to imitate a missing tool or bypass a restriction.

### Local directory and exclude

Respect an explicit directory preference, otherwise reuse `.worktrees/`, then
`worktrees/` when that is the established choice; default to `.worktrees/`.
Check local exclusion before creating a project-local directory:

```bash
git check-ignore .worktrees/
```

If needed, add `.worktrees/` to the common repository's `.git/info/exclude` using
normal authorized metadata writes. Never edit tracked `.gitignore` merely to
hide a worktree. The slash in `<type>/<slug>` nests under that directory. If the
exclude or creation write is blocked, use the host's normal permission mechanism
when available; do not route around it or dirty primary instead.

### Verify base without silently changing primary

Locate the actual primary checkout from git worktree metadata; resolve the
default branch from `origin/HEAD` or verified repository policy. Read its branch,
status and local/remote revision relationship before mutation. Do not switch a
dirty or non-default primary merely to satisfy a postcondition. Preserve it and
report the discrepancy; obtain missing maintenance scope before dependent writes.

If origin/HEAD is absent, inspect verified project default policy. For a no-remote
fixture without such policy, report the unavailable remote default and record the
actual verified primary branch as the local task base when consistent with scope.
`init.defaultBranch` is only a creation preference, never existing-default proof.
Check primary with `git -C <verified-primary> branch --show-current`,
`rev-parse HEAD` and `status --porcelain`, and check the writer HEAD against the
accepted base. Missing origin/HEAD alone does not invalidate verified local state;
ambiguous state blocks dependent writes. Record the facts before editing.

A denied preflight query is not a missing ref or a successful check. Keep any
already verified facts, then identify and verify each unresolved prerequisite
before editing. Use only permitted read-only recovery or normal host permissions
within scope; do not bypass a denial or retry an action the host forbids. A partial
fallback must not silently omit the default/base checks. Equivalent actual Git
output is sufficient; no particular command spelling is required. If verification
remains unavailable, stop dependent writes and report the blocker, even when
Edit/Write tools are allowed. Follow the shared contract's pre-write requirements.

For an already clean primary on its default branch, update the intended remote
base only within task authority, using fetch and `git pull --ff-only`. Stop on a
failed fetch/update or divergence; never auto-rebase, reset or discard local work.
If required unpushed task commits exist, explicitly record and use that verified
base instead of silently omitting them. Base selection must not erase user work.

### Create and verify the worktree

Use a branch `<type>/<slug>` following [git conventions](../../rules/git-workflow.md)
and an explicit verified base. These placeholders must be resolved, not run
literally:

```bash
git worktree add -b <type>/<slug> <primary>/.worktrees/<type>/<slug> <verified-base>
```

Reinspect the resulting git/common directories, superproject, status, branch and
HEAD before writing. Record creation provenance and owner in task state.

### Blocked isolation

If worktree creation fails, stop writes and report the permission prerequisite.
Use normal host permission escalation only when available and within scope; if
it is unavailable or denied, finish read-only inspection or report the blocker.
Never silently fall back to editing primary. Do not claim a worktree exists from
an attempted tool call; verify creation actually succeeded before setup/tests.

## Step 2: Setup and baseline in isolation

Discover required project setup and checks from instructions/configuration. Run
only applicable installed commands within authorized scope; do not automatically
install dependencies, fetch tools or run another harness/service. A failed setup
must not trigger a fallback to primary.

Run meaningful baseline checks in the isolated checkout and record commands,
exit status and PASS/FAIL/NOT RUN/NOT APPLICABLE. Distinguish existing failures
from changes introduced later; do not claim a clean baseline when required checks
are unavailable. Report unresolved failures before dependent implementation.

Verify primary remains as observed. Do not clean, stash, switch or reset it to
make a report look clean. A missing jq or failed-open hook does not waive this
procedural invariant; Codex bundled hooks remain disabled.

## Actor scope

SOLO uses the current agent only. HANDOFF, PARALLEL and REVIEW require explicit
user authorization before adding actors. An authorized read-only reviewer may
share the owner's isolated worktree; an authorized sequential writer may reuse
it within scope. Every concurrent writer needs a distinct branch/worktree and a
named integrator. Creating isolation grants neither delegation nor delivery.

## Quick reference

| Situation | Action |
| --- | --- |
| Existing suitable linked worktree | Verify and reuse; do not nest another |
| Submodule or ambiguous git metadata | Verify real isolation/ownership before writes |
| Suitable native tool exposed | Verify destination, base and side effects |
| No suitable native tool | Manual git worktree from explicit verified base |
| Blocked creation or local exclude | Stop writes; normal permission path or blocker |
| Dirty/non-default primary | Preserve/report; no implicit switch, reset or cleanup |
| Detached/external checkout | Preserve host ownership; no implicit branch or cleanup |
| Missing jq/native hook | Procedural checks still apply; never claim enforcement |
