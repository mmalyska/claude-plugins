#!/usr/bin/env bash
# Fixture-based tests for guard-main-checkout.sh. Bash 3.2 compatible.
set -u

GUARD="$(cd "$(dirname "$0")" && pwd)/guard-main-checkout.sh"
FIXTURE=$(mktemp -d)
PASS=0
FAIL=0

cleanup() { rm -rf "$FIXTURE"; }
trap cleanup EXIT

# --- preflight ------------------------------------------------------------
# The guard fails open by design: on any internal error it exits 0 silently.
# That means a missing, non-executable, or syntactically broken guard would make
# every "allow" assertion below pass for the wrong reason. Check liveness first.
if [ ! -f "$GUARD" ]; then
  printf 'FATAL: guard not found at %s\n' "$GUARD" >&2; exit 1
fi
if [ ! -x "$GUARD" ]; then
  printf 'FATAL: guard is not executable: %s\n' "$GUARD" >&2; exit 1
fi
if ! bash -n "$GUARD" 2>/dev/null; then
  printf 'FATAL: guard has a syntax error: %s\n' "$GUARD" >&2
  bash -n "$GUARD"; exit 1
fi
for dep in jq git; do
  command -v "$dep" >/dev/null 2>&1 || {
    printf 'FATAL: %s is required to run these tests\n' "$dep" >&2; exit 1; }
done

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
# awkward paths: the guard eval's jq @sh output, so these must not break it
mkdir -p "$FIXTURE/primary/dir with space"
mkdir -p "$FIXTURE/plain/it's \$HOME \`x\` here"

# --- helpers --------------------------------------------------------------
# run_guard <tool> <file_path-or-empty> <command-or-empty> <cwd>
# Sets GUARD_OUT and GUARD_RC rather than echoing, so a nonzero exit from the
# guard is distinguishable from a silent allow.
GUARD_OUT=''
GUARD_RC=0
run_guard() {
  GUARD_OUT=$(jq -n --arg t "$1" --arg f "$2" --arg c "$3" --arg d "$4" \
     '{tool_name:$t, cwd:$d, tool_input:({} + (if $f=="" then {} else {file_path:$f} end)
                                             + (if $c=="" then {} else {command:$c} end))}' \
  | "$GUARD" 2>/dev/null)
  GUARD_RC=$?
}

# run_guard_sub <tool> <file_path-or-empty> <command-or-empty> <cwd>
# Same, but shaped like a subagent-originated call. Verified 2026-09-17: a
# subagent carries a populated agent_id/agent_type, while session_id and
# transcript_path are IDENTICAL to the parent's -- so agent_id is the only
# reliable discriminator.
run_guard_sub() {
  GUARD_OUT=$(jq -n --arg t "$1" --arg f "$2" --arg c "$3" --arg d "$4" \
     '{tool_name:$t, cwd:$d, agent_id:"a445e9a59c7959b42", agent_type:"general-purpose",
       tool_input:({} + (if $f=="" then {} else {file_path:$f} end)
                      + (if $c=="" then {} else {command:$c} end))}' \
  | "$GUARD" 2>/dev/null)
  GUARD_RC=$?
}

# run_guard_mode <permission_mode> <tool> <file_path-or-empty> <command-or-empty> <cwd>
# Same as run_guard but stamps a permission_mode. The guard escalates ask->deny
# in the modes that answer their own prompts, so these two cannot share a helper.
run_guard_mode() {
  GUARD_OUT=$(jq -n --arg m "$1" --arg t "$2" --arg f "$3" --arg c "$4" --arg d "$5" \
     '{tool_name:$t, cwd:$d, permission_mode:$m,
       tool_input:({} + (if $f=="" then {} else {file_path:$f} end)
                      + (if $c=="" then {} else {command:$c} end))}' \
  | "$GUARD" 2>/dev/null)
  GUARD_RC=$?
}

# reason_has <description> <substring>
# Some assertions are about what the model is told, not just the verdict.
reason_has() {
  desc=$1; want=$2
  got=$(printf '%s' "$GUARD_OUT" | jq -r '.hookSpecificOutput.permissionDecisionReason // ""' 2>/dev/null)
  case "$got" in
    *"$want"*) PASS=$((PASS+1)); printf '  ok   %s\n' "$desc" ;;
    *) FAIL=$((FAIL+1)); printf '  FAIL %s (reason lacks %s)\n' "$desc" "$want" ;;
  esac
}

# expect <description> <expected: allow|ask|deny>
# Reads GUARD_OUT/GUARD_RC set by the preceding run_guard call.
expect() {
  desc=$1; want=$2
  if [ "$GUARD_RC" -ne 0 ]; then
    got="error(rc=$GUARD_RC)"
  elif [ -z "$GUARD_OUT" ]; then
    got=allow
  else
    got=$(printf '%s' "$GUARD_OUT" | jq -r '.hookSpecificOutput.permissionDecision // "malformed"')
  fi
  if [ "$got" = "$want" ]; then
    PASS=$((PASS+1)); printf '  ok   %s\n' "$desc"
  else
    FAIL=$((FAIL+1)); printf '  FAIL %s (want %s, got %s)\n' "$desc" "$want" "$got"
  fi
}

echo "classification (allow rules):"
run_guard Write "$FIXTURE/plain/a.txt" "" "$FIXTURE/plain"
expect "non-repo path is allowed" allow
run_guard Write "$FIXTURE/primary/.git/info/exclude" "" "$FIXTURE/primary"
expect "path inside .git is allowed" allow
run_guard Write "$FIXTURE/primary/sub/s.txt" "" "$FIXTURE/primary"
expect "submodule path is allowed" allow
run_guard Write "$FIXTURE/primary/.worktrees/feat/x/seed.txt" "" "$FIXTURE/primary/.worktrees/feat/x"
expect "linked worktree path is allowed" allow
CLAUDE_ALLOW_MAIN_EDITS=1 run_guard Write "$FIXTURE/primary/seed.txt" "" "$FIXTURE/primary"
expect "escape hatch allows primary checkout" allow
run_guard Write "" "" "$FIXTURE/primary"
expect "missing file_path is allowed" allow
run_guard Write "$FIXTURE/primary/.worktrees/feat/x/new/deep/file.txt" "" "$FIXTURE/primary"
expect "nonexistent file in worktree is allowed" allow

# Liveness canary: this MUST produce a decision. If the guard is broken and
# failing open, everything above goes green while this goes red.
run_guard Write "$FIXTURE/primary/seed.txt" "" "$FIXTURE/primary"
expect "CANARY: primary checkout write produces a decision" ask

echo ""
echo "bash mutation list:"
run_guard Bash "" "git status --short" "$FIXTURE/primary"
expect "git status in primary is allowed" allow
run_guard Bash "" "npm test -- --watch=false" "$FIXTURE/primary"
expect "npm test in primary is allowed" allow
run_guard Bash "" "git worktree add .worktrees/feat/y -b feat/y" "$FIXTURE/primary"
expect "git worktree add in primary is allowed" allow
run_guard Bash "" "git pull --ff-only" "$FIXTURE/primary"
expect "git pull in primary is allowed" allow
run_guard Bash "" "git switch main" "$FIXTURE/primary"
expect "git switch to default branch is allowed" allow
run_guard Bash "" "git commit -m 'x'" "$FIXTURE/primary"
expect "git commit in primary is flagged" ask
run_guard Bash "" "git rebase origin/main" "$FIXTURE/primary"
expect "git rebase in primary is flagged" ask
run_guard Bash "" "git switch feat/x" "$FIXTURE/primary"
expect "git switch to feature branch is flagged" ask
run_guard Bash "" "git commit -m 'x'" "$FIXTURE/primary/.worktrees/feat/x"
expect "git commit in worktree is allowed" allow
run_guard Bash "" "git switch -c feat/z" "$FIXTURE/primary"
expect "git switch -c to new branch is flagged" ask
run_guard Bash "" "git checkout --quiet main" "$FIXTURE/primary"
expect "git checkout with flags before default branch is allowed" allow
run_guard Bash "" "git switch main && git add *.md" "$FIXTURE/primary"
expect "glob in command does not break parsing" allow

echo ""
echo "subagent policy:"
run_guard_sub Write "$FIXTURE/primary/seed.txt" "" "$FIXTURE/primary"
expect "subagent write to primary is denied" deny
run_guard_sub Write "$FIXTURE/primary/.worktrees/feat/x/seed.txt" "" "$FIXTURE/primary/.worktrees/feat/x"
expect "subagent write to worktree is allowed" allow
run_guard_sub Bash "" "git commit -m 'x'" "$FIXTURE/primary"
expect "subagent git commit in primary is denied" deny
run_guard_sub Bash "" "git status --short" "$FIXTURE/primary"
expect "subagent read-only bash is allowed" allow
run_guard Write "$FIXTURE/primary/seed.txt" "" "$FIXTURE/primary"
expect "main-session write to primary still asks" ask
CLAUDE_ALLOW_MAIN_EDITS=1 run_guard_sub Write "$FIXTURE/primary/seed.txt" "" "$FIXTURE/primary"
expect "escape hatch also frees subagents" allow

echo ""
echo "hostile paths (guard eval's jq @sh output):"
run_guard Write "$FIXTURE/primary/dir with space/a.txt" "" "$FIXTURE/primary"
expect "path with spaces still classifies as primary" ask
run_guard Write "$FIXTURE/plain/it's \$HOME \`x\` here/a.txt" "" "$FIXTURE/plain"
expect "path with quote, \$var and backticks is allowed and inert" allow
run_guard Bash "" "git commit -m \"it's \$USER \`whoami\`\"" "$FIXTURE/primary"
expect "command with quotes and backticks is flagged, not executed" ask

echo ""
echo "permission_mode escalation (ask is only a fence where a human answers):"
run_guard_mode default Write "$FIXTURE/primary/seed.txt" "" "$FIXTURE/primary"
expect "default mode asks" ask
run_guard_mode plan Write "$FIXTURE/primary/seed.txt" "" "$FIXTURE/primary"
expect "plan mode asks" ask
run_guard_mode auto Write "$FIXTURE/primary/seed.txt" "" "$FIXTURE/primary"
expect "auto mode denies (its classifier would swallow an ask)" deny
reason_has "auto-mode denial still names the worktree convention" ".worktrees/"
run_guard_mode acceptEdits Write "$FIXTURE/primary/seed.txt" "" "$FIXTURE/primary"
expect "acceptEdits denies" deny
run_guard_mode bypassPermissions Write "$FIXTURE/primary/seed.txt" "" "$FIXTURE/primary"
expect "bypassPermissions denies" deny
run_guard_mode dontAsk Write "$FIXTURE/primary/seed.txt" "" "$FIXTURE/primary"
expect "dontAsk denies" deny
run_guard_mode wharrgarbl Write "$FIXTURE/primary/seed.txt" "" "$FIXTURE/primary"
expect "unknown mode falls back to ask, never to deny" ask
run_guard_mode auto Write "$FIXTURE/primary/.worktrees/feat/x/seed.txt" "" "$FIXTURE/primary/.worktrees/feat/x"
expect "auto mode does not over-trigger inside a worktree" allow
CLAUDE_ALLOW_MAIN_EDITS=1 run_guard_mode auto Write "$FIXTURE/primary/seed.txt" "" "$FIXTURE/primary"
expect "escape hatch still wins over auto mode" allow

echo ""
echo "shell writes (the path Edit/Write never sees):"
run_guard Bash "" "echo hi > notes.md" "$FIXTURE/primary"
expect "redirect into primary is flagged" ask
run_guard Bash "" "echo hi >> notes.md" "$FIXTURE/primary"
expect "append into primary is flagged" ask
run_guard Bash "" "cat seed.txt | tee notes.md" "$FIXTURE/primary"
expect "tee into primary is flagged" ask
run_guard Bash "" "sed -i '' s/a/b/ seed.txt" "$FIXTURE/primary"
expect "sed -i in primary is flagged" ask
run_guard Bash "" "cat <<'EOF' > notes.md" "$FIXTURE/primary"
expect "heredoc redirect into primary is flagged" ask
run_guard Bash "" "rm -rf build" "$FIXTURE/primary"
expect "rm in primary is flagged" ask
run_guard Bash "" "cp seed.txt copy.txt" "$FIXTURE/primary"
expect "cp in primary is flagged" ask
run_guard Bash "" "mkdir -p generated/deep" "$FIXTURE/primary"
expect "mkdir in primary is flagged" ask
run_guard_sub Bash "" "echo hi > notes.md" "$FIXTURE/primary"
expect "subagent shell write to primary is denied" deny
run_guard_mode auto Bash "" "echo hi > notes.md" "$FIXTURE/primary"
expect "shell write under auto mode denies" deny

echo ""
echo "shell writes that must stay out of the way:"
run_guard Bash "" "sed -n '1,5p' seed.txt" "$FIXTURE/primary"
expect "read-only sed is allowed" allow
run_guard Bash "" "ls -la > /dev/null" "$FIXTURE/primary"
expect "redirect to /dev/null is allowed" allow
run_guard Bash "" "npm test > /dev/null 2>&1" "$FIXTURE/primary"
expect "fd duplication is not read as a file target" allow
run_guard Bash "" "echo hi > /tmp/scratch-guard-test.txt" "$FIXTURE/primary"
expect "redirect to an absolute path outside the repo is allowed" allow
run_guard Bash "" "cd /tmp && echo hi > scratch-guard-test.txt" "$FIXTURE/primary"
expect "cd out of the repo rebases relative targets" allow
run_guard Bash "" "echo hi > w.txt" "$FIXTURE/primary/.worktrees/feat/x"
expect "redirect inside a worktree is allowed" allow
run_guard Bash "" 'echo "a>b"' "$FIXTURE/primary"
expect "a > inside a quoted argument is not a redirect" allow
run_guard Bash "" "grep -rn todo ." "$FIXTURE/primary"
expect "read-only search is allowed" allow
# The cross-direction case: correct cwd, wrong target. Classifying the target
# rather than the cwd is the whole reason this one is catchable.
run_guard Bash "" "echo hi > $FIXTURE/primary/notes.md" "$FIXTURE/primary/.worktrees/feat/x"
expect "absolute write from a worktree into the primary is flagged" ask

printf '\n%d passed, %d failed\n' "$PASS" "$FAIL"
[ "$FAIL" -eq 0 ]
