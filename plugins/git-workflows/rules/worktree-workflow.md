# Worktree Workflow

**The primary checkout is never a workspace.** It stays on the default branch with a clean tree. Every change — yours, mine, or a subagent's — happens in a linked worktree.

This holds even when the primary checkout is already on a feature branch. The rule is "never a workspace", not "never dirty on the default branch".

## Layout

| Thing | Convention |
| --- | --- |
| Worktree path | `.worktrees/<branch>` at the repo root |
| Branch name | `<type>/<slug>` — the commit types from [git-workflow.md](./git-workflow.md) |
| Ignore mechanism | `.worktrees/` in `.git/info/exclude`, never `.gitignore` |

`feat/worktree-guard` lives at `.worktrees/feat/worktree-guard`. Worktree directory, branch name, and commit prefix all agree.

Create worktrees with the `using-git-worktrees` skill; finish with `finishing-a-development-branch`.

## Actor authorization and ownership

Default STANDARD + SOLO uses the current agent only. HANDOFF, PARALLEL and REVIEW
require explicit user authorization before adding actors. Verify actual exposed
capability after authority; do not start another CLI to bypass a restriction.

| Authorized situation | Isolation |
| --- | --- |
| Read-only reviewer/explorer | May share the owner's isolated worktree |
| Sequential implementer | May share it only within authorized scope |
| Concurrent writers | Distinct branch/worktree for each writer and a named integrator |

These are isolation rules, not delegation permission. The integrator owns final
integration and gates; failed/partial work must be reported honestly.

## Before the first write

Use Step 0 of this plugin's [using-git-worktrees skill](../skills/using-git-worktrees/SKILL.md)
even when already in a feature worktree. Inspect actual Git/common directories,
superproject, worktree metadata and writer state; locate primary and verify its
actual branch, HEAD and clean status against the accepted base/default policy.
A `.worktrees` path, feature branch, preconfigured fixture or silent guard is not
proof of isolation. Record the verified facts before editing. Missing or ambiguous
checks block dependent writes; preserve user state instead of repairing it.

## Isolation failure and primary state

If isolation is blocked, stop writes and report the permission prerequisite.
Use the host's normal permission path when available; never silently fall back
to editing primary. Detect linked/submodule/detached/external state before
mutation. Preserve dirty or non-default primary state and report it; do not
switch, reset, stash or clean merely to satisfy a postcondition.

Explicitly authorized primary maintenance is a separate scoped exception, not
permission to treat primary as a workspace. Runtime-triggering merge still needs
separate fresh runtime authority with impact/rollback. Readiness does not grant
delivery or cleanup permissions.

Directory location alone is not proof of cleanup ownership. Verify recorded
creation provenance, current ownership/state and active consumers; cleanup needs
explicit authority for that target. Keep external, unknown or active worktrees.
A successful merge alone does not authorize removing its branch/worktree.

## The guard

In Claude Code, a configured `PreToolUse` hook in this plugin enforces the invariant.
Codex manifests explicitly disable that hook; in Codex these are procedural
worktree rules, not enforced interception. The permission-mode table below is
Claude-specific. A subagent writing to the primary checkout is always denied. For the main session the verdict depends on whether anyone is there to answer it:

| Permission mode | Verdict | Why |
| --- | --- | --- |
| `default`, `plan` | `ask` | A prompt actually reaches a human |
| `auto`, `acceptEdits`, `dontAsk`, `bypassPermissions` | `deny` | These answer their own prompts, so an `ask` is granted silently and enforces nothing |

It sees the edit tools and the common shell writes — `>`, `>>`, `tee`, `sed -i`, heredoc redirects, `cp`, `mv`, `rm`, `mkdir`. It classifies the *target*, not the working directory, so a write from a worktree to an absolute path inside the primary checkout is caught too, and a write to `/tmp` from a primary-checkout cwd is not.

**It still cannot see every write.** `python -c "open('f','w')"`, an editor invocation, anything that writes from inside a program it would have to run to understand. Do not treat silence from the guard as permission. The invariant above is the rule; the hook is a backstop for the cases it can see, not a fence around the ones it can't.

For deliberately authorized primary maintenance, `CLAUDE_ALLOW_MAIN_EDITS=1`
disables the Claude hook for that session. The variable is a technical escape
hatch, not user authorization; it cannot waive scope or safety. Do not set it
as a workaround for denied isolation or delegate primary edits through a parent.

## When the guard stops you

It is telling you the target is the primary checkout. The fix is almost never to get past it — it is to create a worktree and redo the write there. Approve (or set the escape hatch) only when you actually intend to change the primary checkout, such as pulling the default branch or fixing something in `.git/`.

When the guard denies a subagent, do not work around it by having the parent perform the write. Either use the active host's supported worktree isolation, or point the subagent
at the parent's existing worktree. Routing around the denial defeats the isolation it exists to provide.

A missing jq or failed-open hook removes technical enforcement, not procedural
requirements. Codex hooks remain disabled; the same checks still apply.
