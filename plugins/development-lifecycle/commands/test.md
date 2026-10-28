---
description: "TDD workflow for features and reproducible bug fixes in Claude Code or Codex"
argument-hint: [feature name, or "fix: <bug description>"]
---

Load the canonical procedure from the active installation before doing this task:

@${CLAUDE_PLUGIN_ROOT}/skills/test/SKILL.md

Source navigation: [shared test workflow](../skills/test/SKILL.md).

Resolve runtime files from `${CLAUDE_PLUGIN_ROOT}`, never from the project cwd or a filesystem-wide first
match. If the root or required file is unavailable, report the loading blocker
and stop dependent work; do not substitute a fallback procedure. Follow the
loaded procedure with this input:

$ARGUMENTS
