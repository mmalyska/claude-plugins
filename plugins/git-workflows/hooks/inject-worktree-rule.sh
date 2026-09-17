#!/usr/bin/env bash
# Puts rules/worktree-workflow.md into the model's context at session start.
#
# Why this exists: Claude Code has no plugin-rules loader. The plugin manifest
# schema accepts commands, agents, skills, hooks, workflows, themes,
# outputStyles, monitors and mcpServers -- there is no `rules` key and no
# rules/ auto-scan. A rules/ directory in a plugin is therefore inert: readable
# on demand, never loaded. Verified against Claude Code 2.1.274.
#
# That made the guard's whole premise unreachable. The hook would intercept a
# write and name a convention (`.worktrees/<type>/<slug>`) that the model had
# never been told, so the correction arrived only after the mistake, if at all.
# A SessionStart hook emitting additionalContext is the supported way to state
# a standing rule up front, so that is what this does.
#
# Fails open, like the guard: any problem exits 0 and injects nothing. A session
# that starts without the rule is worse than one that does not start.
set -u

SCRIPT_DIR=$(cd "$(dirname "$0")" 2>/dev/null && pwd) || exit 0
PLUGIN_ROOT=$(cd "$SCRIPT_DIR/.." 2>/dev/null && pwd) || exit 0
RULE="$PLUGIN_ROOT/rules/worktree-workflow.md"

[ -r "$RULE" ] || exit 0
command -v jq >/dev/null 2>&1 || exit 0
command -v git >/dev/null 2>&1 || exit 0

HOOK_INPUT=$(cat 2>/dev/null) || exit 0
CWD=$(printf '%s' "$HOOK_INPUT" | jq -r '.cwd // ""' 2>/dev/null) || exit 0
[ -n "$CWD" ] || CWD=$PWD

# The rule is about git repositories. Injecting it into a session that is not in
# one spends context on advice that cannot apply.
git -C "$CWD" rev-parse --git-dir >/dev/null 2>&1 || exit 0

PREAMBLE='The git-workflows plugin enforces the rule below with a PreToolUse hook. It is
a standing constraint on this session, not reference material -- follow it
without being asked and without reading any further file.'

if [ "${CLAUDE_ALLOW_MAIN_EDITS:-}" = "1" ]; then
  PREAMBLE="$PREAMBLE

NOTE: CLAUDE_ALLOW_MAIN_EDITS=1 is set, so the hook is disabled for this
session and will not stop you. The conventions below still stand; you are
simply the only thing enforcing them."
fi

# jq does the JSON escaping. The alternative -- hand-rolled bash substitution --
# is what every other plugin does and it breaks on the first backslash.
jq -n --rawfile rule "$RULE" --arg preamble "$PREAMBLE" \
  '{hookSpecificOutput:{hookEventName:"SessionStart",
    additionalContext:($preamble + "\n\n" + $rule)}}' 2>/dev/null || exit 0

exit 0
