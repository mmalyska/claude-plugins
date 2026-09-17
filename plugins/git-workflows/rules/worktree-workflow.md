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

A `PreToolUse` hook in this plugin enforces the invariant. A subagent writing to the primary checkout is always denied. For the main session the verdict depends on whether anyone is there to answer it:

| Permission mode | Verdict | Why |
|---|---|---|
| `default`, `plan` | `ask` | A prompt actually reaches a human |
| `auto`, `acceptEdits`, `dontAsk`, `bypassPermissions` | `deny` | These answer their own prompts, so an `ask` is granted silently and enforces nothing |

It sees the edit tools and the common shell writes — `>`, `>>`, `tee`, `sed -i`, heredoc redirects, `cp`, `mv`, `rm`, `mkdir`. It classifies the *target*, not the working directory, so a write from a worktree to an absolute path inside the primary checkout is caught too, and a write to `/tmp` from a primary-checkout cwd is not.

**It still cannot see every write.** `python -c "open('f','w')"`, an editor invocation, anything that writes from inside a program it would have to run to understand. Do not treat silence from the guard as permission. The invariant above is the rule; the hook is a backstop for the cases it can see, not a fence around the ones it can't.

To work in the primary checkout deliberately for a whole session, start it with `CLAUDE_ALLOW_MAIN_EDITS=1`.

## When the guard stops you

It is telling you the target is the primary checkout. The fix is almost never to get past it — it is to create a worktree and redo the write there. Approve (or set the escape hatch) only when you actually intend to change the primary checkout, such as pulling the default branch or fixing something in `.git/`.

When the guard denies a subagent, do not work around it by having the parent perform the write. Either re-dispatch with `isolation: "worktree"`, or point the subagent at the parent's existing worktree. Routing around the denial defeats the isolation it exists to provide.
