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

printf '\n%d passed, %d failed\n' "$PASS" "$FAIL"
[ "$FAIL" -eq 0 ]
