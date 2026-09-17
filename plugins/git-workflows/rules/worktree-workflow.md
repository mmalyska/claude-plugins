# Worktree Workflow

**The primary checkout is never a workspace.** It stays on the default branch with a clean tree. Every change — yours, mine, or a subagent's — happens in a linked worktree.

This holds even when the primary checkout is already on a feature branch. The rule is "never a workspace", not "never dirty on the default branch".

## Layout

| Thing | Convention |
|---|---|
| Worktree path | `.worktrees/<branch>` at the repo root |
| Branch name | `<type>/<slug>` — the commit types from [git-workflow.md](./git-workflow.md) |
| Ignore mechanism | `.worktrees/` in `.git/info/exclude`, never `.gitignore` |

`feat/worktree-guard` lives at `.worktrees/feat/worktree-guard`. Worktree directory, branch name, and commit prefix all agree.

Create worktrees with the `using-git-worktrees` skill; finish with `finishing-a-development-branch`.

## Subagents

| Situation | Where the subagent works |
|---|---|
| Reviewer, explorer, anything read-only | The parent's worktree |
| A single sequential implementer | The parent's worktree |
| Two or more agents writing concurrently | One worktree each, via `isolation: "worktree"` |

Once the parent is in a worktree the blast radius is already off the default branch, so sharing it is fine and avoids merging branches for a one-file fix. Isolation exists to prevent one specific failure: two agents writing the same tree at once, each overwriting work it never saw. When agents fan out, the parent merges their branches afterward.

## The guard

A `PreToolUse` hook in this plugin enforces the invariant. It asks before any write to the primary checkout, and denies subagent writes outright.

**It does not see shell writes** — `sed -i`, heredocs, `>` redirection. Those reach the filesystem without the hook ever being consulted. Do not treat silence from the guard as permission. The invariant above is the rule; the hook is a backstop for the cases it can see, not a fence around the ones it can't.

To work in the primary checkout deliberately for a whole session, start it with `CLAUDE_ALLOW_MAIN_EDITS=1`.

## When the guard asks

It is telling you the target is the primary checkout. The fix is almost never to approve — it is to create a worktree and redo the write there. Approve only when you actually intend to change the primary checkout, such as pulling the default branch or fixing something in `.git/`.

When the guard denies a subagent, do not work around it by having the parent perform the write. Either re-dispatch with `isolation: "worktree"`, or point the subagent at the parent's existing worktree. Routing around the denial defeats the isolation it exists to provide.
