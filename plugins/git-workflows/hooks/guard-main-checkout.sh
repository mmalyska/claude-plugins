#!/usr/bin/env bash
# Worktree guard. Keeps the primary checkout from being used as a workspace.
#
# Bash 3.2 compatible (Apple's /bin/bash). Uses only shell builtins, git, and jq
# -- no sed/awk/grep, whose BSD and GNU versions differ enough to make a guard
# behave differently per platform.
#
# Fails open: any internal problem exits 0 (allow). A broken guard must never
# brick every write on the machine.
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

  # Resolve symlinks: hook input is not normalized (/tmp vs /private/tmp on
  # macOS), so string comparison is not enough.
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
  *)                       exit 0 ;;
esac

[ -n "$TARGET" ] || exit 0

KIND=$(classify_target "$TARGET")
case "$KIND" in
  not-repo|git-internal|submodule|worktree) exit 0 ;;
esac

TARGET_DIR=$(nearest_dir "$TARGET")
BRANCH=$(git -C "$TARGET_DIR" rev-parse --abbrev-ref HEAD 2>/dev/null)
REPO=$(basename "$(git -C "$TARGET_DIR" rev-parse --show-toplevel 2>/dev/null)")

decide ask "The primary checkout of '$REPO' is not a workspace (currently on '$BRANCH'). Create a worktree instead: git worktree add .worktrees/<type>/<slug> -b <type>/<slug>. To work in the primary checkout for this whole session, restart with CLAUDE_ALLOW_MAIN_EDITS=1."
