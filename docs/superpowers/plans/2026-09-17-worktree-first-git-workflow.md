# Worktree-First Git Workflow Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make every change — yours, Claude's, or a subagent's — happen in a git worktree, enforced by a hook, so the primary checkout stays on the default branch with a clean tree.

**Architecture:** One `PreToolUse` hook shipped in the `git-workflows` plugin classifies the target path of every write and denies, asks, or allows. Around it, the `using-git-worktrees` skill flips from opt-in to mandatory, a new global rule states the invariant in prose (covering the shell-write gap the hook cannot see), and `finishing-a-development-branch` gains a postcondition that restores the primary checkout.

**Tech Stack:** POSIX-ish shell targeting **bash 3.2**, `jq` for JSON, `git` for repo inspection. No test framework; the test harness is plain shell.

## Requirements

The guard must run identically on **macOS and Linux**. These are the floors, set by the oldest thing each platform ships:

| Requirement | Floor | Why |
|---|---|---|
| `bash` | 3.2 | Apple ships 3.2.57 as `/bin/bash`. No associative arrays, no `${var,,}`, no `mapfile`, no `[[ ... ]] =~` reliance |
| `git` | 2.28 | `rev-parse --absolute-git-dir` (2.13), `init -b` in the test harness (2.28) |
| `jq` | 1.6 | Ships with macOS 15+; on Linux it is usually an explicit install |
| Platform | macOS, Linux | No Windows support; paths and `pwd -P` assume POSIX |

**Portability rules for every line in `hooks/`:**

- **No GNU-only tool flags.** BSD and GNU `sed` disagree on alternation (`\|` is GNU-only), `-i` semantics, and `-E`/`-r`. The guard avoids `sed`, `awk`, and `grep` entirely — everything is shell builtins plus `git` and `jq`.
- **No `readlink -f`** (absent on older macOS). Use `cd ... && pwd -P`.
- **No `mktemp` templates** — bare `mktemp -d` behaves the same on both; `mktemp -d -t foo` does not.
- Both platforms must be exercised before merge. See Task 5, Step 4.

**Spec:** `docs/superpowers/specs/2026-09-17-worktree-first-git-workflow-design.md`

## Global Constraints

- Target **bash 3.2**. No bash 4+ syntax anywhere in `hooks/`.
- The guard **fails open**. Any internal error — `jq` missing, malformed input, `git` failure — exits 0 silently. A broken guard must never brick every write on the machine.
- The guard **never mutates anything**. No writes, no `git` state changes, read-only inspection only.
- Decision output is `hookSpecificOutput.permissionDecision` ∈ {`ask`, `deny`}, with `permissionDecisionReason`. Allow is a silent `exit 0`.
- Escape hatch is exactly `CLAUDE_ALLOW_MAIN_EDITS=1`. No path allowlist, no marker file.
- Worktrees live at `.worktrees/<branch>`; branches are `<type>/<slug>` using the conventional-commit types in `rules/git-workflow.md`.
- `.worktrees/` is ignored via `.git/info/exclude`, never `.gitignore`.
- Default branch resolution order: `origin/HEAD` → `main` → `master`.

---

## File Structure

| File | Responsibility |
|---|---|
| `plugins/git-workflows/hooks/hooks.json` | Registers the `PreToolUse` entry |
| `plugins/git-workflows/hooks/guard-main-checkout.sh` | The guard: classify target, emit decision |
| `plugins/git-workflows/hooks/test-guard.sh` | Fixture-based test harness for the guard |
| `plugins/git-workflows/skills/using-git-worktrees/SKILL.md` | Worktree creation, now mandatory |
| `plugins/git-workflows/rules/worktree-workflow.md` | The invariant, naming, subagent policy |
| `plugins/git-workflows/skills/finishing-a-development-branch/SKILL.md` | Adds restore-primary-checkout postcondition |
| `plugins/git-workflows/README.md` | States plainly what installing this plugin does |
| `plugins/git-workflows/.claude-plugin/plugin.json` | Version 1.1.0, `worktree` keyword |
| `README.md`, `.claude-plugin/marketplace.json` | Description names the enforcement |

Task 1 is a verification spike whose findings gate Task 4. Tasks 2–5 build the hook bottom-up. Tasks 6–9 are documentation and can be reviewed independently of the hook.

---

### Task 1: Verify hook behavioral assumptions

The spec records three assumptions as unverified. Task 4 cannot be written correctly without the first one. **Do this task first and record real answers — do not guess.**

**Files:**
- Modify: `docs/superpowers/specs/2026-09-17-worktree-first-git-workflow-design.md` (the "Behavioral checks" section)
- Create (throwaway, not committed): `/tmp/hook-probe/probe.sh`, `/tmp/hook-probe/.claude/settings.json`

**Interfaces:**
- Consumes: nothing
- Produces: three recorded answers. Task 4 consumes answer (1) to decide how it detects subagents; Task 5 consumes answer (2).

- [ ] **Step 1: Build a probe hook that captures raw hook input**

```bash
mkdir -p /tmp/hook-probe/.claude
cat > /tmp/hook-probe/probe.sh <<'EOF'
#!/usr/bin/env bash
INPUT=$(cat)
printf '%s\n' "$INPUT" >> /tmp/hook-probe/capture.jsonl
exit 0
EOF
chmod +x /tmp/hook-probe/probe.sh
```

- [ ] **Step 2: Register the probe in a scratch project**

```bash
cat > /tmp/hook-probe/.claude/settings.json <<'EOF'
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Edit|Write|Bash",
        "hooks": [{ "type": "command", "command": "/tmp/hook-probe/probe.sh" }]
      }
    ]
  }
}
EOF
```

- [ ] **Step 3: Capture a main-session call and a subagent call**

Start a Claude Code session with `/tmp/hook-probe` as the working directory. In it: make one `Write` to a file in that directory, then dispatch a subagent that also makes one `Write` there.

- [ ] **Step 4: Answer check (1) — is a subagent call identifiable?**

```bash
jq -r 'keys | join(",")' /tmp/hook-probe/capture.jsonl | sort -u
jq -r '{session_id, transcript_path, cwd, permission_mode}' /tmp/hook-probe/capture.jsonl
```

Compare the two captured records. Look for an explicit subagent/sidechain field. If none, check whether `session_id` or `transcript_path` differs between the parent call and the subagent call.

Record verbatim in the spec one of: the field name to use; the divergence to infer from; or "no reliable signal".

**If the answer is "no reliable signal", stop and report.** Task 4 as specified is unimplementable and the design needs revisiting — do not ship a branch that silently never fires.

- [ ] **Step 5: Answer check (2) — how does `ask` degrade with no human?**

Change the probe to always ask:

```bash
cat > /tmp/hook-probe/probe.sh <<'EOF'
#!/usr/bin/env bash
cat >/dev/null
jq -n '{hookSpecificOutput:{hookEventName:"PreToolUse",permissionDecision:"ask",permissionDecisionReason:"probe"}}'
exit 0
EOF
```

Run a headless invocation against that directory and observe whether the write is denied or silently allowed:

```bash
cd /tmp/hook-probe && claude -p 'Create a file called probe-result.txt containing the word hello' ; ls probe-result.txt 2>&1
```

`ls` failing means `ask` degraded to denial — the required behavior. `probe-result.txt` existing means it degraded to allow, which is a hole; record that, because Task 4 must then use `deny` for subagents unconditionally rather than relying on degradation.

- [ ] **Step 6: Answer check (3) — is there a persistent "don't ask again"?**

In an interactive session in `/tmp/hook-probe`, trigger two writes in a row. Record whether the second prompted again, and whether the first prompt offered a session-scoped option.

- [ ] **Step 7: Record all three answers in the spec and commit**

Replace the three bullets under "Behavioral checks to run before writing the scripts" with the findings, keeping the numbering, and retitle the section to "Behavioral checks (verified 2026-09-17)".

```bash
rm -rf /tmp/hook-probe
git add docs/superpowers/specs/2026-09-17-worktree-first-git-workflow-design.md
git commit -m "docs: record verified hook behavior for worktree guard"
```

---

### Task 2: Guard path classification + the allow rules

Builds steps 1–6 of the decision order. Every outcome here is **allow**; asking and denying arrive in Task 4. This task is done when the guard correctly allows everything it should allow and exits non-silently for nothing.

**Files:**
- Create: `plugins/git-workflows/hooks/guard-main-checkout.sh`
- Create: `plugins/git-workflows/hooks/test-guard.sh`

**Interfaces:**
- Consumes: nothing
- Produces: `classify_target <path>` echoing exactly one of `not-repo`, `git-internal`, `submodule`, `worktree`, `primary`. Tasks 3 and 4 branch on these five strings. Also `decide <ask|deny> <reason>` and `hook_input_field <jq-filter>`.

- [ ] **Step 1: Write the failing test harness**

```bash
cat > plugins/git-workflows/hooks/test-guard.sh <<'EOF'
#!/usr/bin/env bash
# Fixture-based tests for guard-main-checkout.sh. Bash 3.2 compatible.
set -u

GUARD="$(cd "$(dirname "$0")" && pwd)/guard-main-checkout.sh"
FIXTURE=$(mktemp -d)
PASS=0
FAIL=0

cleanup() { rm -rf "$FIXTURE"; }
trap cleanup EXIT

# --- build fixtures -------------------------------------------------------
# primary checkout on default branch
mkdir -p "$FIXTURE/primary"
git -C "$FIXTURE/primary" init -q -b main
echo seed > "$FIXTURE/primary/seed.txt"
git -C "$FIXTURE/primary" add -A
git -C "$FIXTURE/primary" -c user.email=t@t -c user.name=t commit -qm seed
# linked worktree
git -C "$FIXTURE/primary" worktree add -q -b feat/x "$FIXTURE/primary/.worktrees/feat/x"
# submodule
mkdir -p "$FIXTURE/subsrc"
git -C "$FIXTURE/subsrc" init -q -b main
echo s > "$FIXTURE/subsrc/s.txt"
git -C "$FIXTURE/subsrc" add -A
git -C "$FIXTURE/subsrc" -c user.email=t@t -c user.name=t commit -qm s
git -C "$FIXTURE/primary" -c protocol.file.allow=always -c user.email=t@t -c user.name=t \
    submodule add -q "$FIXTURE/subsrc" sub
git -C "$FIXTURE/primary" -c user.email=t@t -c user.name=t commit -qm sub
# plain directory, no repo
mkdir -p "$FIXTURE/plain"

# --- helpers --------------------------------------------------------------
# run_guard <tool> <file_path-or-empty> <command-or-empty> <cwd>
run_guard() {
  jq -n --arg t "$1" --arg f "$2" --arg c "$3" --arg d "$4" \
     '{tool_name:$t, cwd:$d, tool_input:({} + (if $f=="" then {} else {file_path:$f} end)
                                             + (if $c=="" then {} else {command:$c} end))}' \
  | "$GUARD" 2>/dev/null
}

# expect <description> <expected: allow|ask|deny> <actual-json>
expect() {
  desc=$1; want=$2; out=$3
  if [ -z "$out" ]; then got=allow
  else got=$(printf '%s' "$out" | jq -r '.hookSpecificOutput.permissionDecision // "malformed"'); fi
  if [ "$got" = "$want" ]; then
    PASS=$((PASS+1)); printf '  ok   %s\n' "$desc"
  else
    FAIL=$((FAIL+1)); printf '  FAIL %s (want %s, got %s)\n' "$desc" "$want" "$got"
  fi
}

echo "classification (allow rules):"
expect "non-repo path is allowed" allow \
  "$(run_guard Write "$FIXTURE/plain/a.txt" "" "$FIXTURE/plain")"
expect "path inside .git is allowed" allow \
  "$(run_guard Write "$FIXTURE/primary/.git/info/exclude" "" "$FIXTURE/primary")"
expect "submodule path is allowed" allow \
  "$(run_guard Write "$FIXTURE/primary/sub/s.txt" "" "$FIXTURE/primary")"
expect "linked worktree path is allowed" allow \
  "$(run_guard Write "$FIXTURE/primary/.worktrees/feat/x/seed.txt" "" "$FIXTURE/primary/.worktrees/feat/x")"
expect "escape hatch allows primary checkout" allow \
  "$(CLAUDE_ALLOW_MAIN_EDITS=1 run_guard Write "$FIXTURE/primary/seed.txt" "" "$FIXTURE/primary")"
expect "missing file_path is allowed" allow \
  "$(run_guard Write "" "" "$FIXTURE/primary")"
expect "nonexistent file in worktree is allowed" allow \
  "$(run_guard Write "$FIXTURE/primary/.worktrees/feat/x/new/deep/file.txt" "" "$FIXTURE/primary")"

printf '\n%d passed, %d failed\n' "$PASS" "$FAIL"
[ "$FAIL" -eq 0 ]
EOF
chmod +x plugins/git-workflows/hooks/test-guard.sh
```

- [ ] **Step 2: Run it to verify it fails**

Run: `plugins/git-workflows/hooks/test-guard.sh`
Expected: FAIL — `guard-main-checkout.sh: No such file or directory`, every case reported as a failure.

- [ ] **Step 3: Write the guard**

```bash
cat > plugins/git-workflows/hooks/guard-main-checkout.sh <<'EOF'
#!/usr/bin/env bash
# Worktree guard. Keeps the primary checkout from being used as a workspace.
# Bash 3.2 compatible. Fails open: any internal problem exits 0 (allow).
set -u

HOOK_INPUT=$(cat 2>/dev/null) || exit 0
command -v jq >/dev/null 2>&1 || exit 0
command -v git >/dev/null 2>&1 || exit 0

field() { printf '%s' "$HOOK_INPUT" | jq -r "$1 // \"\"" 2>/dev/null; }

decide() {
  jq -n --arg d "$1" --arg r "$2" \
    '{hookSpecificOutput:{hookEventName:"PreToolUse",permissionDecision:$d,permissionDecisionReason:$r}}' \
    2>/dev/null
  exit 0
}

# Walk up until we hit a directory that exists, so unwritten files classify by
# their intended parent rather than failing.
nearest_dir() {
  d=$1
  [ -n "$d" ] || { printf ''; return; }
  case $d in */) d=${d%/} ;; esac
  while [ -n "$d" ] && [ "$d" != "/" ] && [ ! -d "$d" ]; do d=$(dirname "$d"); done
  printf '%s' "$d"
}

# Echoes exactly one of: not-repo git-internal submodule worktree primary
classify_target() {
  raw=$1
  dir=$(nearest_dir "$raw")
  [ -n "$dir" ] && [ -d "$dir" ] || { printf 'not-repo'; return; }

  gitdir=$(git -C "$dir" rev-parse --absolute-git-dir 2>/dev/null) || { printf 'not-repo'; return; }
  top=$(git -C "$dir" rev-parse --show-toplevel 2>/dev/null) || { printf 'not-repo'; return; }
  common=$(cd "$top" 2>/dev/null && cd "$(git rev-parse --git-common-dir 2>/dev/null)" 2>/dev/null && pwd -P) \
    || { printf 'not-repo'; return; }

  abs=$(cd "$dir" 2>/dev/null && pwd -P) || { printf 'not-repo'; return; }

  # Inside the git directory itself is not a working-tree write.
  case "$abs/" in
    "$common"/*|"$gitdir"/*) printf 'git-internal'; return ;;
  esac

  if [ -n "$(git -C "$dir" rev-parse --show-superproject-working-tree 2>/dev/null)" ]; then
    printf 'submodule'; return
  fi

  if [ "$gitdir" != "$common" ]; then printf 'worktree'; return; fi
  printf 'primary'
}

[ "${CLAUDE_ALLOW_MAIN_EDITS:-}" = "1" ] && exit 0

TOOL=$(field '.tool_name')
CWD=$(field '.cwd')
FILE_PATH=$(field '.tool_input.file_path')

case "$TOOL" in
  Edit|Write|NotebookEdit) TARGET=$FILE_PATH ;;
  Bash)                    TARGET=$CWD ;;
  *)                       exit 0 ;;
esac

[ -n "$TARGET" ] || exit 0

KIND=$(classify_target "$TARGET")
case "$KIND" in
  not-repo|git-internal|submodule|worktree) exit 0 ;;
esac

exit 0   # primary: decisions arrive in Task 4
EOF
chmod +x plugins/git-workflows/hooks/guard-main-checkout.sh
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `plugins/git-workflows/hooks/test-guard.sh`
Expected: `7 passed, 0 failed`

- [ ] **Step 5: Commit**

```bash
git add plugins/git-workflows/hooks/guard-main-checkout.sh plugins/git-workflows/hooks/test-guard.sh
git commit -m "feat: add worktree guard path classification"
```

---

### Task 3: Bash mutation list

Teaches the guard which `Bash` commands count as mutations. Until now `Bash` classified by `cwd` unconditionally; after this it classifies only when the command matches.

**Files:**
- Modify: `plugins/git-workflows/hooks/guard-main-checkout.sh`
- Modify: `plugins/git-workflows/hooks/test-guard.sh`

**Interfaces:**
- Consumes: `classify_target` from Task 2
- Produces: `is_mutating_command <command>` returning 0 (mutating) or 1. Task 4 relies on non-mutating `Bash` never reaching a decision.

- [ ] **Step 1: Add failing tests**

Append before the final `printf` in `test-guard.sh`:

```bash
echo ""
echo "bash mutation list:"
expect "git status in primary is allowed" allow \
  "$(run_guard Bash "" "git status --short" "$FIXTURE/primary")"
expect "npm test in primary is allowed" allow \
  "$(run_guard Bash "" "npm test -- --watch=false" "$FIXTURE/primary")"
expect "git worktree add in primary is allowed" allow \
  "$(run_guard Bash "" "git worktree add .worktrees/feat/y -b feat/y" "$FIXTURE/primary")"
expect "git pull in primary is allowed" allow \
  "$(run_guard Bash "" "git pull --ff-only" "$FIXTURE/primary")"
expect "git switch to default branch is allowed" allow \
  "$(run_guard Bash "" "git switch main" "$FIXTURE/primary")"
expect "git commit in primary is flagged" ask \
  "$(run_guard Bash "" "git commit -m 'x'" "$FIXTURE/primary")"
expect "git rebase in primary is flagged" ask \
  "$(run_guard Bash "" "git rebase origin/main" "$FIXTURE/primary")"
expect "git switch to feature branch is flagged" ask \
  "$(run_guard Bash "" "git switch feat/x" "$FIXTURE/primary")"
expect "git commit in worktree is allowed" allow \
  "$(run_guard Bash "" "git commit -m 'x'" "$FIXTURE/primary/.worktrees/feat/x")"
expect "git switch -c to new branch is flagged" ask \
  "$(run_guard Bash "" "git switch -c feat/z" "$FIXTURE/primary")"
expect "git checkout with flags before default branch is allowed" allow \
  "$(run_guard Bash "" "git checkout --quiet main" "$FIXTURE/primary")"
expect "glob in command does not break parsing" allow \
  "$(run_guard Bash "" "git add *.md && echo done" "$FIXTURE/primary")"
```

The last three exist because the branch name is extracted by pure shell word
splitting rather than `sed`. They pin the flag-skipping and confirm `set -f`
stops an unquoted `*` from globbing mid-parse.

- [ ] **Step 2: Run to verify the new cases fail**

Run: `plugins/git-workflows/hooks/test-guard.sh`
Expected: the four `ask` cases FAIL (guard still exits 0 for everything); the eight `allow` cases pass incidentally.

- [ ] **Step 3: Implement the mutation list and the primary-checkout decision**

Insert before `[ "${CLAUDE_ALLOW_MAIN_EDITS:-}" = "1" ]`:

```bash
default_branch() {
  d=$1
  b=$(git -C "$d" symbolic-ref --quiet --short refs/remotes/origin/HEAD 2>/dev/null)
  if [ -n "$b" ]; then printf '%s' "${b#origin/}"; return; fi
  if git -C "$d" show-ref --verify --quiet refs/heads/main; then printf 'main'; return; fi
  if git -C "$d" show-ref --verify --quiet refs/heads/master; then printf 'master'; return; fi
  printf 'main'
}

# 0 = mutating, 1 = not.
# Pure shell: no sed/awk/grep, because BSD and GNU disagree on all three.
is_mutating_command() {
  cmd=$1 dir=$2
  case "$cmd" in
    *"git commit"*|*"git merge"*|*"git rebase"*|*"git cherry-pick"*|\
    *"git revert"*|*"git apply"*|*"git stash pop"*|*"git stash apply"*) return 0 ;;
  esac
  case "$cmd" in
    *"git checkout "*|*"git switch "*) ;;
    *) return 1 ;;
  esac

  # First non-flag word after `checkout`/`switch` is the branch.
  # set -f stops the unquoted expansion from globbing on a command like `git add *`.
  set -f
  # shellcheck disable=SC2086
  set -- $cmd
  set +f
  target='' seen=0
  for w in "$@"; do
    if [ "$seen" = "1" ]; then
      case "$w" in
        -*) continue ;;
        *)  target=$w; break ;;
      esac
    fi
    case "$w" in checkout|switch) seen=1 ;; esac
  done

  [ -n "$target" ] || return 1
  [ "$target" = "$(default_branch "$dir")" ] && return 1
  return 0
}
```

Then replace the `Bash)` case and the trailing `exit 0`:

```bash
case "$TOOL" in
  Edit|Write|NotebookEdit) TARGET=$FILE_PATH ;;
  Bash)
    COMMAND=$(field '.tool_input.command')
    BASH_DIR=$(nearest_dir "$CWD")
    is_mutating_command "$COMMAND" "$BASH_DIR" || exit 0
    TARGET=$CWD ;;
  *) exit 0 ;;
esac
```

and, at the bottom:

```bash
BRANCH=$(git -C "$(nearest_dir "$TARGET")" rev-parse --abbrev-ref HEAD 2>/dev/null)
REPO=$(basename "$(git -C "$(nearest_dir "$TARGET")" rev-parse --show-toplevel 2>/dev/null)")
decide ask "The primary checkout of '$REPO' is not a workspace (currently on '$BRANCH'). Create a worktree instead: git worktree add .worktrees/<type>/<slug> -b <type>/<slug>. To work in the primary checkout for this whole session, restart with CLAUDE_ALLOW_MAIN_EDITS=1."
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `plugins/git-workflows/hooks/test-guard.sh`
Expected: `19 passed, 0 failed`

- [ ] **Step 5: Commit**

```bash
git add plugins/git-workflows/hooks/
git commit -m "feat: flag git mutations and primary-checkout writes"
```

---

### Task 4: Subagent deny

**Blocked on Task 1 step 4.** Implement using the signal recorded there. If that answer was "no reliable signal", do not invent one — stop and report.

**Files:**
- Modify: `plugins/git-workflows/hooks/guard-main-checkout.sh`
- Modify: `plugins/git-workflows/hooks/test-guard.sh`

**Interfaces:**
- Consumes: `classify_target`, `decide`, the Task 1 finding
- Produces: nothing downstream

- [ ] **Step 1: Add failing tests**

Extend `run_guard` to take an optional sixth argument carrying the subagent marker, using the exact field name recorded in Task 1. Written here as `SUBAGENT_FIELD` — substitute the real one:

```bash
# run_guard_sub <tool> <file_path> <command> <cwd>
run_guard_sub() {
  jq -n --arg t "$1" --arg f "$2" --arg c "$3" --arg d "$4" \
     '{tool_name:$t, cwd:$d, SUBAGENT_FIELD:true,
       tool_input:({} + (if $f=="" then {} else {file_path:$f} end)
                      + (if $c=="" then {} else {command:$c} end))}' \
  | "$GUARD" 2>/dev/null
}

echo ""
echo "subagent policy:"
expect "subagent write to primary is denied" deny \
  "$(run_guard_sub Write "$FIXTURE/primary/seed.txt" "" "$FIXTURE/primary")"
expect "subagent write to worktree is allowed" allow \
  "$(run_guard_sub Write "$FIXTURE/primary/.worktrees/feat/x/seed.txt" "" "$FIXTURE/primary/.worktrees/feat/x")"
expect "main-session write to primary still asks" ask \
  "$(run_guard Write "$FIXTURE/primary/seed.txt" "" "$FIXTURE/primary")"
```

- [ ] **Step 2: Run to verify the deny case fails**

Run: `plugins/git-workflows/hooks/test-guard.sh`
Expected: `subagent write to primary is denied (want deny, got ask)`.

- [ ] **Step 3: Implement the branch**

Replace the final `decide ask ...` line with:

```bash
IS_SUBAGENT=$(field '.SUBAGENT_FIELD')
if [ "$IS_SUBAGENT" = "true" ]; then
  decide deny "Subagents may not write to the primary checkout of '$REPO'. Re-dispatch this agent with isolation: \"worktree\", or have it write inside the parent's existing worktree."
fi
decide ask "The primary checkout of '$REPO' is not a workspace (currently on '$BRANCH'). Create a worktree instead: git worktree add .worktrees/<type>/<slug> -b <type>/<slug>. To work in the primary checkout for this whole session, restart with CLAUDE_ALLOW_MAIN_EDITS=1."
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `plugins/git-workflows/hooks/test-guard.sh`
Expected: `22 passed, 0 failed`

- [ ] **Step 5: Commit**

```bash
git add plugins/git-workflows/hooks/
git commit -m "feat: deny subagent writes to the primary checkout"
```

---

### Task 5: Register the hook and smoke-test it live

**Files:**
- Create: `plugins/git-workflows/hooks/hooks.json`

**Interfaces:**
- Consumes: `guard-main-checkout.sh`
- Produces: the plugin's active hook registration

- [ ] **Step 1: Write the registration**

```bash
cat > plugins/git-workflows/hooks/hooks.json <<'EOF'
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Edit|Write|NotebookEdit|Bash",
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/hooks/guard-main-checkout.sh"
          }
        ]
      }
    ]
  }
}
EOF
```

- [ ] **Step 2: Verify it parses and the referenced file is executable**

```bash
jq -e '.hooks.PreToolUse[0].hooks[0].command' plugins/git-workflows/hooks/hooks.json
test -x plugins/git-workflows/hooks/guard-main-checkout.sh && echo executable
```

Expected: the command string prints, then `executable`.

- [ ] **Step 3: Smoke-test against a real session**

Install the plugin from this branch, open a session in a scratch repo's primary checkout on `main`, and attempt one `Write`. Confirm the prompt appears and its text names the repo and branch. Then create a worktree, `cd` into it, and confirm writes there are silent.

Confirm too that the guard adds no perceptible latency to ordinary `Bash` calls — `git status` should not pause.

- [ ] **Step 4: Run the test suite on the other platform**

The guard ships to both; it gets tested on both. From macOS, exercise Linux in a
container:

```bash
docker run --rm -v "$PWD:/w" -w /w debian:stable-slim sh -c \
  'apt-get update -qq && apt-get install -y -qq git jq >/dev/null && \
   git config --global --add safe.directory /w && \
   bash plugins/git-workflows/hooks/test-guard.sh'
```

Expected: `22 passed, 0 failed`, identical to the macOS run.

If Docker is unavailable, run the suite on any Linux host with `git` 2.28+ and
`jq` 1.6+ and record the result. Do not merge on a single platform's green —
the BSD/GNU differences this guard avoids are exactly the kind that pass on one
and fail on the other.

- [ ] **Step 5: Commit**

```bash
git add plugins/git-workflows/hooks/hooks.json
git commit -m "feat: register the worktree guard hook"
```

---

### Task 6: Rewrite `using-git-worktrees`

**Files:**
- Modify: `plugins/git-workflows/skills/using-git-worktrees/SKILL.md`

**Interfaces:**
- Consumes: the guard's behavior (worktrees allowed, primary checkout asks)
- Produces: the skill Task 7's rule points at

- [ ] **Step 1: Remove the opt-in gate**

In Step 0, delete the consent paragraph, the quoted question ("Would you like me to set up an isolated worktree? It protects your current branch from changes."), and the sentence "If the user declines consent, work in place and skip to Step 3."

Replace with:

```markdown
**If `GIT_DIR == GIT_COMMON` (or in a submodule):** You are in the primary
checkout. The primary checkout is never a workspace — create a worktree. Do not
ask permission; this is the default, not an option. The only path that works in
place is a sandbox permission failure (Step 1b), which is a can't, not a won't.
```

- [ ] **Step 2: Replace the gitignore step with `.git/info/exclude`**

Replace the "Safety Verification" block wholesale:

````markdown
#### Safety Verification (project-local directories only)

**MUST verify the directory is ignored before creating the worktree:**

```bash
git check-ignore -q .worktrees 2>/dev/null || \
  echo '.worktrees/' >> "$(git rev-parse --git-common-dir)/info/exclude"
```

Use `.git/info/exclude`, never `.gitignore`. Editing `.gitignore` is a write to
the primary checkout — exactly what the guard hook blocks — and it would need a
commit on the default branch. `.git/info/exclude` needs no working-tree change
and no commit, and `.worktrees/` is a personal workflow artifact rather than a
team convention. One entry covers every nesting depth, so `feat/foo` at
`.worktrees/feat/foo` is covered.
````

- [ ] **Step 3: Require a current default branch before branching**

Insert immediately before "#### Create the Worktree":

````markdown
#### Verify the Base

The worktree branches from the primary checkout's HEAD, so confirm it is on the
default branch and current first:

```bash
DEFAULT=$(git symbolic-ref --quiet --short refs/remotes/origin/HEAD 2>/dev/null)
DEFAULT=${DEFAULT#origin/}
DEFAULT=${DEFAULT:-main}
git -C "$(git rev-parse --git-common-dir)/.." switch "$DEFAULT"
git -C "$(git rev-parse --git-common-dir)/.." pull --ff-only
```

If the pull fails, report it and ask — do not branch from a stale base.
````

- [ ] **Step 4: Update the branch-naming and quick reference**

In "Create the Worktree", replace `path=".worktrees/$BRANCH_NAME"` guidance with a note that `BRANCH_NAME` is `<type>/<slug>` using the conventional-commit types from `rules/git-workflow.md`, and that the slash nests on disk.

In the Quick Reference table, replace the row `Directory not ignored | Add to .gitignore + commit` with `Directory not ignored | Append to .git/info/exclude`.

In Red Flags, under **Never**, replace "Create worktree without verifying it's ignored (project-local)" with two entries: "Ask permission to create a worktree — it is the default" and "Add `.worktrees/` to `.gitignore` — use `.git/info/exclude`".

- [ ] **Step 5: Verify no opt-in language survives**

```bash
grep -niE 'would you like|declines|work in place|\.gitignore' \
  plugins/git-workflows/skills/using-git-worktrees/SKILL.md
```

Expected: only the sandbox-failure mention of working in place, and the `.gitignore` references inside the explanation of why it is not used.

- [ ] **Step 6: Commit**

```bash
git add plugins/git-workflows/skills/using-git-worktrees/SKILL.md
git commit -m "refactor: make worktrees the default, not an opt-in"
```

---

### Task 7: New `worktree-workflow` rule

Carries the invariant in prose. This is what covers the guard's blind spot: `sed -i`, heredocs, and shell redirection are not intercepted, so the rule must state the invariant directly.

**Files:**
- Create: `plugins/git-workflows/rules/worktree-workflow.md`

**Interfaces:**
- Consumes: naming and policy decisions from the spec
- Produces: the rule Task 9 links from `git-workflow.md` and `development-workflow.md`

- [ ] **Step 1: Write the rule**

````markdown
# Worktree Workflow

**The primary checkout is never a workspace.** It stays on the default branch
with a clean tree. Every change — yours, mine, or a subagent's — happens in a
linked worktree.

This holds even when the primary checkout is already on a feature branch. The
rule is "never a workspace", not "never dirty on the default branch".

## Layout

| Thing | Convention |
|---|---|
| Worktree path | `.worktrees/<branch>` at the repo root |
| Branch name | `<type>/<slug>` — the commit types from [git-workflow.md](./git-workflow.md) |
| Ignore mechanism | `.worktrees/` in `.git/info/exclude`, never `.gitignore` |

`feat/worktree-guard` lives at `.worktrees/feat/worktree-guard`. Worktree
directory, branch name, and commit prefix all agree.

Create worktrees with the `using-git-worktrees` skill; finish with
`finishing-a-development-branch`.

## Subagents

| Situation | Where the subagent works |
|---|---|
| Reviewer, explorer, anything read-only | The parent's worktree |
| A single sequential implementer | The parent's worktree |
| Two or more agents writing concurrently | One worktree each, via `isolation: "worktree"` |

The blast radius is already off the default branch once the parent is in a
worktree, so sharing it is fine and avoids merging branches for a one-file fix.
Isolation exists to prevent one specific failure: two agents writing the same
tree at once, where each overwrites work it never saw. When agents fan out, the
parent merges their branches afterward.

## The guard

A `PreToolUse` hook in this plugin enforces the invariant. It asks before any
write to the primary checkout and denies subagent writes outright.

It does **not** see shell writes — `sed -i`, heredocs, `>` redirection. Do not
treat silence from the guard as permission. The invariant above is the rule; the
hook is only a backstop for the cases it can see.

To work in the primary checkout deliberately for a whole session, start it with
`CLAUDE_ALLOW_MAIN_EDITS=1`.
````

- [ ] **Step 2: Verify it has no `paths:` frontmatter**

```bash
head -1 plugins/git-workflows/rules/worktree-workflow.md
```

Expected: `# Worktree Workflow` — this rule is global and must not be
path-scoped like `rules/csharp/*.md`.

- [ ] **Step 3: Commit**

```bash
git add plugins/git-workflows/rules/worktree-workflow.md
git commit -m "docs: add worktree workflow rule"
```

---

### Task 8: `finishing-a-development-branch` postcondition

**Files:**
- Modify: `plugins/git-workflows/skills/finishing-a-development-branch/SKILL.md`

**Interfaces:**
- Consumes: the invariant from Task 7
- Produces: nothing downstream

- [ ] **Step 1: Add the postcondition to the overview**

Change the Core principle line to:

```markdown
**Core principle:** Verify tests → Detect environment → Present options → Execute choice → Clean up → Restore the primary checkout.

**Postcondition — every path through this skill:** the primary checkout ends on
the default branch with a clean tree. Options 2 and 3 keep the worktree alive,
but the primary checkout is still left on the default branch.
```

- [ ] **Step 2: Add the explicit restore step**

After Step 6 (Cleanup Workspace), add:

````markdown
### Step 7: Restore the Primary Checkout

Runs for **all four options**, including the ones that keep the worktree.

```bash
MAIN_ROOT=$(git -C "$(git rev-parse --git-common-dir)/.." rev-parse --show-toplevel)
DEFAULT=$(git -C "$MAIN_ROOT" symbolic-ref --quiet --short refs/remotes/origin/HEAD 2>/dev/null)
DEFAULT=${DEFAULT#origin/}
git -C "$MAIN_ROOT" switch "${DEFAULT:-main}"
git -C "$MAIN_ROOT" status --short
```

`git status --short` must print nothing. If it does not, report the dirty files
and stop — do not clean them up unprompted.
````

- [ ] **Step 3: Update the Quick Reference and Red Flags**

Add a `Restore primary` column to the options table, `yes` for all four rows.

Under **Always**, add: "Leave the primary checkout on the default branch, clean".

- [ ] **Step 4: Verify the table is consistent**

```bash
grep -A7 '| Option |' plugins/git-workflows/skills/finishing-a-development-branch/SKILL.md
```

Expected: five columns, four option rows, `Restore primary` = `yes` on every row.

- [ ] **Step 5: Commit**

```bash
git add plugins/git-workflows/skills/finishing-a-development-branch/SKILL.md
git commit -m "docs: guarantee the primary checkout is restored on finish"
```

---

### Task 9: Documentation

The plugin now ships executable code that runs before every write. The READMEs say that plainly rather than listing it as a feature bullet.

**Files:**
- Modify: `plugins/git-workflows/README.md`
- Modify: `plugins/git-workflows/.claude-plugin/plugin.json`
- Modify: `plugins/git-workflows/rules/git-workflow.md`
- Modify: `plugins/git-workflows/rules/development-workflow.md`
- Modify: `README.md`
- Modify: `.claude-plugin/marketplace.json`

**Interfaces:**
- Consumes: everything above
- Produces: nothing downstream

- [ ] **Step 1: Rewrite the plugin README**

Replace the whole file:

````markdown
# git-workflows

Git discipline and automation for Claude Code.

## What installing this does

**This plugin installs a hook that runs before every file write and every git
mutation, in every repo you use Claude Code in.** Nothing else in this
marketplace ships executable code; this does.

The hook enforces one rule: **the primary checkout is never a workspace.** It
stays on the default branch with a clean tree, and work happens in
`.worktrees/<branch>`.

- Writing to the primary checkout **asks you first**, naming the repo and branch.
- A **subagent** writing to the primary checkout is **denied** outright, and told
  to re-dispatch with `isolation: "worktree"`.
- Writes inside a worktree, inside `.git/`, inside a submodule, or outside any
  repo are untouched. So are read-only commands — `git status`, `grep`, and test
  runs never pay a cost.
- It does **not** see shell writes (`sed -i`, heredocs, `>` redirection). The
  `worktree-workflow.md` rule covers those; the hook is a backstop, not a fence.
- It fails open. If `jq` is missing or anything errors, the write proceeds.

To work in the primary checkout deliberately, start the session with
`CLAUDE_ALLOW_MAIN_EDITS=1`.

### Requirements

macOS and Linux. Windows is not supported.

| | Minimum | Note |
|---|---|---|
| `bash` | 3.2 | The floor is Apple's `/bin/bash`; nothing here needs bash 4+ |
| `git` | 2.28 | |
| `jq` | 1.6 | Bundled with macOS 15+. On Linux, install it — without `jq` the guard fails open and enforces nothing |

The hook uses only shell builtins, `git`, and `jq`. It deliberately avoids
`sed`, `awk`, and `grep`, whose BSD and GNU versions differ enough to make a
guard behave differently on the two platforms.

## Commands

- `/pr` — Create a GitHub PR from the current branch with unpushed commits
- `/commit` — Quick commit with natural language file targeting

## Skills

- `using-git-worktrees` — Creates the isolated workspace. Worktrees are the
  default, not an opt-in.
- `finishing-a-development-branch` — Merge, PR, keep, or discard; always leaves
  the primary checkout on the default branch.

## Rules

- `worktree-workflow.md` — The invariant, branch naming, subagent policy
- `git-workflow.md` — Commit message format, PR workflow
- `development-workflow.md` — Full feature pipeline (research → worktree → plan
  → TDD → review → commit)

## Hooks

- `hooks/guard-main-checkout.sh` — The guard described above
- `hooks/test-guard.sh` — Its tests. Run it directly; no framework needed.

## Install

```sh
claude plugin install git-workflows@mmalyska/claude-plugins
```
````

- [ ] **Step 2: Bump the plugin manifest**

In `plugins/git-workflows/.claude-plugin/plugin.json`, set `"version": "1.1.0"`, append `"worktree"` and `"hooks"` to `keywords`, and change `description` to:

```
Git discipline and automation — enforces worktree-first development with a pre-write hook, plus PR creation and commit conventions
```

- [ ] **Step 3: Link the new rule from the existing rules**

In `rules/git-workflow.md`, append:

```markdown
> Work never happens in the primary checkout. See
> [worktree-workflow.md](./worktree-workflow.md) for the invariant, branch
> naming, and the guard hook.
```

In `rules/development-workflow.md`, insert a new step between 0 and 1:

```markdown
0.5. **Create the Worktree** _(before any implementation)_
   - Use the `using-git-worktrees` skill. The primary checkout is never a
     workspace — see [worktree-workflow.md](./worktree-workflow.md).
   - Branch as `<type>/<slug>`; the worktree lands at `.worktrees/<type>/<slug>`.
```

- [ ] **Step 4: Update the marketplace and root README**

In `.claude-plugin/marketplace.json`, set the `git-workflows` description to the same string used in Step 2.

In `README.md`, change the `git-workflows` table row description to:

```
Worktree-first enforcement (ships a hook), PR creation, commit conventions
```

- [ ] **Step 5: Verify the JSON still parses and descriptions agree**

```bash
jq -e . .claude-plugin/marketplace.json > /dev/null && echo marketplace ok
jq -e . plugins/git-workflows/.claude-plugin/plugin.json > /dev/null && echo plugin ok
diff <(jq -r '.description' plugins/git-workflows/.claude-plugin/plugin.json) \
     <(jq -r '.plugins[] | select(.name=="git-workflows") | .description' .claude-plugin/marketplace.json) \
  && echo "descriptions match"
```

Expected: `marketplace ok`, `plugin ok`, `descriptions match`.

- [ ] **Step 6: Run the full test suite once more**

Run: `plugins/git-workflows/hooks/test-guard.sh`
Expected: `22 passed, 0 failed`

- [ ] **Step 7: Commit**

```bash
git add README.md .claude-plugin/marketplace.json plugins/git-workflows/
git commit -m "docs: state the worktree guard plainly across READMEs"
```

---

## Finishing

Use the `finishing-a-development-branch` skill. This change should land as a PR
rather than a local merge — it alters behavior in every repo the moment
`personal-essentials` picks it up, and it is worth reading once more as a diff.

After it merges, this repo stops being editable on its default branch like any
other. That is the intended outcome, not a regression.
