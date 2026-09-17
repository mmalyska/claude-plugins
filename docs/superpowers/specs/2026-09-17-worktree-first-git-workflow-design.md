# Worktree-First Git Workflow

Date: 2026-09-17
Status: Approved, not yet implemented
Plugin: `git-workflows`

## Problem

All work currently happens in the primary checkout by default. Worktrees exist
as an opt-in path in the `using-git-worktrees` skill, gated behind a consent
question with a "work in place" escape. Nothing keeps the main checkout clean,
nothing keeps it on the default branch, and nothing tells subagents where to
work.

## Invariant

**The primary checkout is never a workspace.** It stays on the default branch
with a clean tree. Every change — yours, Claude's, or a subagent's — happens in
a linked worktree.

Note the strictness: the guard intercepts writes to the primary checkout
regardless of which branch it is on, not only when it is on the default branch.
(Intercept means `ask` for the main session, `deny` for subagents — see
Component 1.) The invariant is "never a workspace", not "never dirty on main".
This closes `git switch feature && edit` as a silent bypass.

## Decisions

| Question | Decision |
|---|---|
| Enforcement | A real blocking `PreToolUse` hook, not advisory rules alone |
| Subagent scope | Own worktree only for concurrent independent writers; otherwise share the parent's |
| Escape hatch | `CLAUDE_ALLOW_MAIN_EDITS=1` environment variable |
| Rollout | Plugin-wide, active in every repo where `git-workflows` is installed |
| Bash coverage | Narrow git-mutation list only, not aggressive shell parsing |
| Primary-checkout writes | `ask` (human decides in the moment), except subagents which get `deny` |
| Worktree location | `.worktrees/<branch>` at repo root |

## Component 1: The guard hook

New files under `plugins/git-workflows/hooks/`:

- `hooks.json` — one `PreToolUse` entry, matcher `Edit|Write|NotebookEdit|Bash`,
  command `${CLAUDE_PLUGIN_ROOT}/hooks/guard-main-checkout.sh`
- `guard-main-checkout.sh` — the guard
- `test-guard.sh` — the test harness

### Contract

Reads hook JSON on stdin (`tool_name`, `tool_input`, `cwd`, `session_id`).
Allows by exiting 0 silently. Otherwise emits
`hookSpecificOutput.permissionDecision` of `ask` or `deny` with a
`permissionDecisionReason`. Never mutates anything.

### Decision order

First match wins. The bias is toward allowing.

1. `CLAUDE_ALLOW_MAIN_EDITS=1` → **allow**, silently. Pre-authorization for a
   session of deliberate main-checkout work.
2. Resolve the target. For `Edit`/`Write`/`NotebookEdit` it is `file_path`. For
   `Bash` the target is `cwd`, but only after the command matches the mutation
   list below — non-matching Bash is allowed without any git inspection, so
   `git status`, `grep`, and `npm test` pay no cost.
3. Target not inside a git repo → **allow**. Covers `/tmp`, scratchpads.
4. Target inside the repo's `.git/` directory → **allow**. Not a working-tree
   write. This is what lets the skill write `.git/info/exclude`.
5. Target inside a git submodule → **allow**.
6. `git-dir != git-common-dir` → linked worktree → **allow**. This is what makes
   everything under `.worktrees/` pass.
7. Call originated from a subagent → **deny**, with a reason naming the fix:
   re-dispatch with `isolation: "worktree"`.
8. Otherwise the target is in the primary checkout → **ask**, with a reason
   naming the file, the repo, the current branch, and a suggested worktree
   branch name.

### Bash mutation list

Deny-eligible only. Everything else on `Bash` passes at step 2.

`git commit`, `git merge`, `git rebase`, `git cherry-pick`, `git revert`,
`git apply`, `git stash pop`, `git stash apply`, and `git checkout` / `git switch`
to a branch other than the default.

Default branch resolved from `origin/HEAD`, falling back to `main`, then `master`.

`git worktree add`, `git pull`, and `git fetch` are deliberately absent — they
are how the primary checkout stays current and how worktrees get created.

### Known gap

The guard does not intercept `sed -i`, heredoc writes, or shell redirection into
repo paths. Aggressive shell parsing was rejected: regex over shell is
unreliable, and false positives would drive constant use of the escape hatch
until the guard stopped meaning anything. The `worktree-workflow.md` rule carries
this weight instead by stating the invariant to Claude directly.

### Behavioral checks (verified 2026-09-17, Claude Code 2.1.274)

Captured by registering a probe hook that logged raw stdin, then driving it with
a headless session that made one main-session write and dispatched one subagent.

1. **Is a subagent-originated call identifiable from hook input? Yes —
   `agent_id` and `agent_type`.** Both are `null` for a main-session call and
   populated for a subagent call (`agent_id: "a445e9a59c7959b42"`,
   `agent_type: "general-purpose"`). Step 7 tests `agent_id` for non-emptiness.

   **The planned fallback would have been wrong.** `session_id` and
   `transcript_path` are *identical* between parent and subagent — a subagent
   shares its parent's session. Inferring from their divergence would have
   produced a branch that silently never fires.

   Full key set on `PreToolUse` input: `agent_id`, `agent_type`, `cwd`,
   `effort`, `hook_event_name`, `permission_mode`, `prompt_id`,
   `scratchpad_dir`, `session_id`, `tool_input`, `tool_name`, `tool_use_id`,
   `transcript_path`.

2. **How does `ask` degrade with no human? It denies.** A headless run against a
   probe returning `ask` was blocked and the target file was never created. The
   required behavior holds.

3. **Does the permission prompt offer a persistent "don't ask again"?** Pending —
   this is a UI behavior that cannot be observed headlessly and needs a human at
   an interactive prompt. It affects only the wording of the guard's reason text,
   not its logic, so implementation proceeded. If each edit re-prompts, the
   reason text should surface `CLAUDE_ALLOW_MAIN_EDITS=1` on the first ask rather
   than as a trailing note.

**Consequence for the deferred session marker.** Because a subagent shares its
parent's `session_id`, a marker keyed on `session_id` would be armed by the
parent and then honored for every subagent — silently defeating the
subagent-deny rule. If that design is ever revisited, it must key on something
that distinguishes them, or refuse to read the marker whenever `agent_id` is
set.

**One incidental finding.** `tool_input.file_path` arrives unnormalized: the
main-session write reported `/private/tmp/...` while the subagent reported
`/tmp/...` for the same directory. Path classification must resolve symlinks
(`cd ... && pwd -P`) rather than compare strings.

### Testing

`test-guard.sh`, plain shell, no dependencies. Builds throwaway repos in a temp
directory — a primary checkout, a linked worktree, a submodule, a non-repo
directory — pipes fixture JSON at the guard, and asserts the decision for every
step above. Explicitly covers `git status` allowed and `git commit` denied in the
primary checkout.

Checks 1–3 above are behavioral and cannot be covered deterministically here.

## Component 2: Rewrite `using-git-worktrees`

Worktrees stop being opt-in.

- Remove the consent question and the "user declines → work in place" branch.
  The only remaining in-place path is sandbox permission failure, which is a
  can't, not a won't.
- Keep Step 0 detection and the native-tool-first preference (`EnterWorktree`
  before `git worktree add`) — both already correct.
- Ignore `.worktrees/` via `.git/info/exclude`, not `.gitignore` plus a commit.
  Under the guard, editing `.gitignore` in the primary checkout is the exact
  thing being blocked, and it needs a commit on the default branch. Writing to
  `.git/info/exclude` requires no working-tree change and no commit, is allowed
  by guard step 4, and is correctly scoped — `.worktrees/` is a personal
  workflow artifact, not a team convention.
- Before branching, confirm the primary checkout is on the default branch and
  current, since that is what the worktree branches from.

## Component 3: New rule `rules/worktree-workflow.md`

Global; no `paths:` frontmatter.

Contents: the invariant in one line; worktree location and branch naming; the
subagent policy; what to do when the guard asks.

**Branch naming:** `<type>/<slug>` reusing the conventional-commit types already
in `git-workflow.md` — `feat/worktree-guard`, `fix/hook-submodule-detection`.
Worktree directory, branch name, and commit prefix all agree. The slash nests on
disk: branch `feat/worktree-guard` lives at `.worktrees/feat/worktree-guard`.
`git worktree add` creates intermediate directories, and the single
`.worktrees/` entry in `.git/info/exclude` covers every depth beneath it.

**Subagent policy:** reviewers, explorers, and any single sequential implementer
share the parent's worktree — the blast radius is already off the default branch.
Only concurrent independent writers get `isolation: "worktree"` each, with the
parent merging their branches afterward. The rule names the failure this
prevents: two agents writing the same tree at once.

## Component 4: Update `finishing-a-development-branch`

Largely aligned already — it `cd`s to the main root and checks out the base
branch. Add one explicit postcondition: **every path through this skill leaves
the primary checkout on the default branch with a clean tree.** Today that is
incidental; it is the other half of the invariant and should be a stated
guarantee.

## Component 5: Documentation

READMEs state plainly what the plugin adds, rather than listing the hook as a
bullet among features.

- `plugins/git-workflows/README.md` — a section saying directly: installing this
  plugin installs a hook that runs before every file write and every git
  mutation, in every repo; what it blocks; how to get past it with
  `CLAUDE_ALLOW_MAIN_EDITS=1`; that subagents are denied outright.
- Root `README.md` and `.claude-plugin/marketplace.json` — the `git-workflows`
  description names the enforcement, not just "git discipline".
- `rules/git-workflow.md` — pointer to the new rule.
- `rules/development-workflow.md` — worktree creation as an explicit step
  between research and planning.
- `plugin.json` — version 1.1.0, add `worktree` keyword.

## Rollout risk

Nothing in `plugins/` ships executable code today; it is entirely markdown. This
adds a shell script that runs before every write in every repo where the plugin
is installed. That is a step up in what installing `git-workflows` means, and
the READMEs say so.

`personal-essentials` installs everything, so this reaches every repo — including
work repos mid-task — the moment it merges.

The change should land via a worktree itself. After it does, this repo stops
being editable on its default branch like any other.

## Deferred

Written down, not built:

- **Session-scoped allow marker.** A paired `PostToolUse` hook writing
  `$TMPDIR/claude-worktree-guard/<session_id>`, checked by the guard, so one
  approval covers the session. Dropped for now: re-prompting may not be annoying
  enough to justify it, and the marker is forgeable — it lives outside the repo,
  so a blocked Claude writing to it via Bash is allowed by step 3. Revisit only
  if prompt fatigue is real.
- A `/worktree` command. The skill and the guard's deny text cover creation.
- A path allowlist exemption. Rejected: it drifts and becomes a bypass.
- Aggressive Bash parsing. See "Known gap".
