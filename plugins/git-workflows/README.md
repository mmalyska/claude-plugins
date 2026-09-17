# git-workflows

Git discipline and automation for Claude Code.

## What installing this does

**This plugin installs a hook that runs before every file write and every git mutation, in every repo you use Claude Code in.** Nothing else in this marketplace ships executable code; this does.

The hook enforces one rule: **the primary checkout is never a workspace.** It stays on the default branch with a clean tree, and work happens in `.worktrees/<branch>`.

- Writing to the primary checkout **asks you first**, naming the repo and branch.
- A **subagent** writing to the primary checkout is **denied** outright, and told to re-dispatch with `isolation: "worktree"`.
- Writes inside a worktree, inside `.git/`, inside a submodule, or outside any repo are untouched. So are read-only commands — `git status`, `grep`, and test runs never pay a cost.
- On `Bash` it only intercepts unambiguous git mutations: `commit`, `merge`, `rebase`, `cherry-pick`, `revert`, `apply`, `stash pop`/`apply`, and `checkout`/`switch` to a non-default branch. `git pull`, `git fetch`, and `git worktree add` are deliberately left alone — they are how the primary checkout stays current and how worktrees get made.
- It does **not** see shell writes (`sed -i`, heredocs, `>` redirection). The `worktree-workflow.md` rule covers those; the hook is a backstop, not a fence.
- It **fails open**. If `jq` is missing or anything errors, the write proceeds. A broken guard must never brick every write on your machine — but it does mean no `jq` means no enforcement.

To work in the primary checkout deliberately, start the session with `CLAUDE_ALLOW_MAIN_EDITS=1`.

### Requirements

macOS and Linux. Windows is not supported.

| Tool | Minimum | Note |
| --- | --- | --- |
| `bash` | 3.2 | The floor is Apple's `/bin/bash`; nothing here needs bash 4+ |
| `git` | 2.28 | Needs `rev-parse --absolute-git-dir` and `init -b` |
| `jq` | 1.6 | Bundled with macOS 15+. On Linux, install it — without `jq` the guard fails open and enforces nothing |

The hook uses only shell builtins, `git`, and `jq`. It deliberately avoids `sed`, `awk`, and `grep`, whose BSD and GNU versions differ enough to make a guard behave differently on the two platforms.

## Commands

- `/pr` — Create a GitHub PR from the current branch with unpushed commits
- `/commit` — Quick commit with natural language file targeting

## Skills

- `using-git-worktrees` — Creates the isolated workspace. Worktrees are the default, not an opt-in.
- `finishing-a-development-branch` — Merge, PR, keep, or discard; always leaves the primary checkout on the default branch.

## Rules

- `worktree-workflow.md` — The invariant, branch naming, subagent policy
- `git-workflow.md` — Commit message format, PR workflow
- `development-workflow.md` — Full feature pipeline (research → worktree → plan → TDD → review → commit)

## Hooks

- `hooks/guard-main-checkout.sh` — The guard described above
- `hooks/test-guard.sh` — Its tests. Run it directly; no framework needed.
- `hooks/test-linux-container.sh` — Runs the same suite on Linux in Docker:

  ```sh
  docker run --rm -v "$PWD:/w" -w /w debian:stable-slim \
    sh /w/plugins/git-workflows/hooks/test-linux-container.sh
  ```

  The runner lives in the repo rather than being piped in, because Docker Desktop on macOS does not share `/tmp` — mounting a script from there yields an empty directory, and the suite silently "passes" without running.

## Install

```sh
claude plugin install git-workflows@mmalyska/claude-plugins
```
