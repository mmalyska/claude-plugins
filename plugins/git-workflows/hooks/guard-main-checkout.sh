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

# Every field in one jq call. This runs before every tool call, so spawning a
# separate jq per field is a cost paid on the hot path for no reason.
# @sh quotes the values so the eval is safe against paths with spaces or quotes.
TOOL='' CWD='' FILE_PATH='' COMMAND='' AGENT_ID='' PERMISSION_MODE=''
eval "$(printf '%s' "$HOOK_INPUT" | jq -r '@sh "
  TOOL=\(.tool_name // "")
  CWD=\(.cwd // "")
  FILE_PATH=\(.tool_input.file_path // "")
  COMMAND=\(.tool_input.command // "")
  AGENT_ID=\(.agent_id // "")
  PERMISSION_MODE=\(.permission_mode // "")
"' 2>/dev/null)" 2>/dev/null || exit 0

decide() {
  jq -n --arg d "$1" --arg r "$2" \
    '{hookSpecificOutput:{hookEventName:"PreToolUse",permissionDecision:$d,permissionDecisionReason:$r}}' \
    2>/dev/null
  exit 0
}

# `ask` is only a fence when a human is there to answer it.
#
# Verified 2026-09-17 on Claude Code 2.1.274: in an interactive session running
# permission mode `auto`, a hook `ask` is routed to the auto-approval classifier
# and granted silently -- no prompt, no reason text, nothing reaches the model.
# The write lands. Headless (`claude -p`) degrades the other way, to deny,
# because there is nobody to answer; that is the case the design spec recorded,
# and generalizing from it was the error.
#
# So in every mode that answers its own prompts, escalate to `deny`, which is
# always delivered to the model verbatim. `default` and `plan` really do put the
# question in front of a human, so they keep the softer `ask`.
#
# An unknown or absent mode keeps `ask`: older hosts may not send the field, and
# a guard that hard-denies on a field it cannot read is worse than one that asks.
ask_or_deny() {
  case "$PERMISSION_MODE" in
    auto|acceptEdits|bypassPermissions|dontAsk) decide deny "$1" ;;
  esac
  decide ask "$1"
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

default_branch() {
  d=$1
  b=$(git -C "$d" symbolic-ref --quiet --short refs/remotes/origin/HEAD 2>/dev/null)
  if [ -n "$b" ]; then printf '%s' "${b#origin/}"; return; fi
  if git -C "$d" show-ref --verify --quiet refs/heads/main 2>/dev/null; then printf 'main'; return; fi
  if git -C "$d" show-ref --verify --quiet refs/heads/master 2>/dev/null; then printf 'master'; return; fi
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
  # set -f stops the unquoted expansion from globbing on a command like
  # `git switch main && git add *.md`.
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

# --- shell writes ---------------------------------------------------------
# Edit/Write/NotebookEdit are not the only way to change a file. `> file`,
# `tee`, `sed -i` and a heredoc redirect all reach the filesystem through Bash,
# and a host that tells the model to prefer Bash for file edits routes the
# majority of writes straight past a guard that only matches the edit tools.
#
# This cannot be exhaustive -- `python -c "open('f','w')"` is undetectable
# without running the command -- so it stays a backstop, not a fence. The
# invariant in rules/worktree-workflow.md remains the actual rule.

# Cheap pre-filter. Runs on every Bash call, so it is builtins only: no
# subprocesses, no git, no jq. Most commands are reads and leave here.
has_write_construct() {
  case "$1" in
    *'>'*) return 0 ;;
    *"sed -i"*|*"sed --in-place"*|*"perl -i"*|*"perl -pi"*|*"perl -ni"*) return 0 ;;
  esac
  for k in tee cp mv rm mkdir rmdir touch ln install truncate patch dd; do
    case " $1 " in
      *" $k "*|*"|$k "*|*";$k "*|*"&$k "*) return 0 ;;
    esac
  done
  return 1
}

# Resolves a token to an absolute path in RESOLVED_TARGET and reports whether it
# lands in a primary checkout. Anything it cannot resolve is a "no": an
# unexpanded $VAR or a glob is a guess, and the guard does not block on guesses.
RESOLVED_TARGET=''
target_is_primary() {
  t=$1 base=$2
  [ -n "$t" ] || return 1
  # '~/'* is a literal pattern, not an attempt to expand: the token arrives from
  # JSON unexpanded, so the expansion is ours to do.
  # shellcheck disable=SC2088
  case $t in
    -*|'&'*|'$'*|'*'*|'`'*) return 1 ;;
    '~/'*) RESOLVED_TARGET="$HOME/${t#'~/'}" ;;
    /*)    RESOLVED_TARGET=$t ;;
    *)     RESOLVED_TARGET="$base/$t" ;;
  esac
  [ "$(classify_target "$RESOLVED_TARGET")" = "primary" ]
}

# 0 = this command writes into a primary checkout; WRITE_TARGET names the path.
#
# Classifying the *target* rather than the cwd is what makes this work in both
# directions: a write from a worktree to an absolute path inside the primary
# checkout is caught, and a write to /tmp from a primary cwd is not.
WRITE_TARGET=''
writes_into_primary() {
  cmd=$1 base=$2
  has_write_construct "$cmd" || return 1

  # `sed`/`perl` are overwhelmingly used to read. Only an in-place flag makes
  # their operands write targets -- otherwise `sed -n 1,50p file` would flag.
  inplace=1
  case "$cmd" in
    *"sed -i"*|*"sed --in-place"*|*"perl -i"*|*"perl -pi"*|*"perl -ni"*) inplace=0 ;;
  esac

  # set -f so a glob in the command cannot expand against the real filesystem
  # while we are merely inspecting it.
  set -f
  # shellcheck disable=SC2086
  set -- $cmd
  set +f

  expect=0 takes=0 cdnext=0
  for w in "$@"; do
    # `cd` inside the command moves the base that relative paths resolve
    # against. Without this, `cd /tmp && echo x > f` looks like a write to the
    # repo. An absolute path is still classified on its own, so this is not a
    # way around the guard.
    if [ "$cdnext" = "1" ]; then
      cdnext=0
      # shellcheck disable=SC2088  # literal pattern; see target_is_primary
      case $w in
        -*)    ;;
        '~/'*) base="$HOME/${w#'~/'}" ;;
        /*)    base=$w ;;
        *)     base="$base/$w" ;;
      esac
      continue
    fi

    case $w in
      '|'|'||'|'&&'|';'|'&'|'('|')') takes=0; expect=0; continue ;;
      cd) cdnext=1; takes=0; continue ;;
    esac

    if [ "$expect" = "1" ]; then
      expect=0
      target_is_primary "$w" "$base" && { WRITE_TARGET=$RESOLVED_TARGET; return 0; }
      continue
    fi

    case $w in
      *'>&'*) continue ;;                               # 2>&1, >&2: fd dup
      '>'|'>>'|'1>'|'1>>'|'2>'|'2>>') expect=1; continue ;;
      '>'*|'1>'*|'2>'*)                                 # >file, >>file, 2>>file
        t=${w#[12]}; t=${t#'>'}; t=${t#'>'}              # strip fd, then > or >>
        target_is_primary "$t" "$base" && { WRITE_TARGET=$RESOLVED_TARGET; return 0; }
        continue ;;
    esac

    if [ "$takes" = "1" ]; then
      case $w in -*) continue ;; esac
      target_is_primary "$w" "$base" && { WRITE_TARGET=$RESOLVED_TARGET; return 0; }
      continue
    fi

    case $w in
      tee|cp|mv|rm|mkdir|rmdir|touch|ln|install|truncate|patch|dd) takes=1 ;;
      sed|perl|gsed) [ "$inplace" = "0" ] && takes=1 ;;
    esac
  done
  return 1
}

[ "${CLAUDE_ALLOW_MAIN_EDITS:-}" = "1" ] && exit 0

case "$TOOL" in
  Edit|Write|NotebookEdit) TARGET=$FILE_PATH ;;
  Bash)
    BASH_DIR=$(nearest_dir "$CWD")
    if is_mutating_command "$COMMAND" "$BASH_DIR"; then
      TARGET=$CWD
    elif writes_into_primary "$COMMAND" "$BASH_DIR"; then
      TARGET=$WRITE_TARGET
    else
      exit 0
    fi ;;
  *) exit 0 ;;
esac

[ -n "$TARGET" ] || exit 0

KIND=$(classify_target "$TARGET")
case "$KIND" in
  not-repo|git-internal|submodule|worktree) exit 0 ;;
esac

TARGET_DIR=$(nearest_dir "$TARGET")
BRANCH=$(git -C "$TARGET_DIR" rev-parse --abbrev-ref HEAD 2>/dev/null)
REPO=$(basename "$(git -C "$TARGET_DIR" rev-parse --show-toplevel 2>/dev/null)")

# Verified 2026-09-17: agent_id/agent_type are null for a main-session call and
# populated for a subagent call. session_id and transcript_path are identical
# between the two, so they cannot be used to tell them apart.
if [ -n "$AGENT_ID" ]; then
  decide deny "Subagents may not write to the primary checkout of '$REPO'. Re-dispatch this agent with isolation: \"worktree\", or have it write inside the parent's existing worktree."
fi

ask_or_deny "The primary checkout of '$REPO' is not a workspace (currently on '$BRANCH'). Create a worktree and redo this there: git worktree add .worktrees/<type>/<slug> -b <type>/<slug>, then repeat the write against that path. To work in the primary checkout for a whole session on purpose, restart with CLAUDE_ALLOW_MAIN_EDITS=1."
