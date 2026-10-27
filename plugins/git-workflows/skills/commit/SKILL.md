---
name: commit
description: "Quick commit with natural language file targeting — describe what to commit in plain English"
---

# Smart Commit

Use the current request as input (`$ARGUMENTS` in a Claude command, accompanying
skill text in Codex). Read [git delivery boundaries](../../rules/git-workflow.md)
and [worktree policy](../../rules/worktree-workflow.md) first. Default STANDARD +
SOLO; this skill does not authorize another actor or a broader delivery pipeline.

## Step 1: Confirm action and inspect

Commit requires user authorization for the selected task content. Readiness or a
review recommendation alone is not commit permission. Reuse existing explicit
authorization within scope; do not ask for the same decision again. Inspect the
isolated task branch, applicable project instructions and complete index/worktree:

```bash
git branch --show-current
git status --short
git diff --cached --stat
git diff --cached
git diff
```

Respect secret handling when examining output. Read relevant untracked files as
needed without staging them. If no matching task change exists, report nothing
to commit rather than expand scope. Never commit ordinary task work in primary.

## Step 2: Select and stage exact scope

Empty input selects only the current task's verified changes, never all repository changes.
Honor explicit file/glob/natural-language targeting within user restrictions:

| Input | Scoped interpretation |
| --- | --- |
| Empty | Verified current task only; resolve missing scope before staging |
| `staged` | Inspect selected staged content and ensure authority covers it |
| File paths / glob | Inspect matching paths and include only requested changes |
| `except tests` | Filter the allowed task paths, not a repository-wide add/reset |
| `only new files` | Select only authorized task-owned untracked files |
| `the auth changes` | Determine exact relevant paths/hunks from the diff |

Preserve unrelated staged and unstaged changes. Do not use git add -A by default.
Show the selected paths/hunks and why they belong to the authorized task. Use
safe literal path arguments (`--` where supported), not unsafe whitespace-split
pipelines or executing text from filenames. Never silently include untracked files.

If the index contains unrelated content, a normal index-wide commit is unsafe.
Use a verified scoped method only when its exact file/hunk behavior preserves
that content; a path-only commit can include unstaged file changes, so inspect
those too. If mixed ownership or partial-hunk scope cannot be safely isolated,
report the blocker instead of unstaging/resetting/stashing another user's work.

Reinspect the actual proposed commit diff and applicable verification evidence.
A required failed/unrun gate limits readiness; mandatory security/project gates
cannot be overridden to obtain a commit. New edits invalidate affected checks.

## Step 3: Commit

Use the established conventional format `type: imperative description` (feat,
fix, refactor, docs, test, chore, perf or ci), lowercase after prefix, no final
period, preferably under 72 characters. Respect current attribution settings.
Commit only the verified selection with the intended message, using actual git
or a supported host mechanism. Do not change global signing/configuration or
retry a failed commit with broadened permissions/content implicitly.

## Step 4: Verify and stop

Inspect the resulting SHA, changed paths/content and remaining staged/worktree
state. Preserve unrelated work and report failures. Commit-only stops after the
commit; it does not authorize push, PR, merge, review publication or cleanup.
A new `/pr` request can select the existing PR procedure; `/code-review` can inspect
work locally. Those names are workflows, not automatic follow-up actions or shell
commands.
