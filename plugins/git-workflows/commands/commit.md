---
description: "Quick commit with natural language file targeting — describe what to commit in plain English"
argument-hint: [target description] (blank = all changes)
---

Load the canonical procedure from the active installation before doing this task:

@${CLAUDE_PLUGIN_ROOT}/skills/commit/SKILL.md

Source navigation: [shared commit workflow](../skills/commit/SKILL.md).

Resolve runtime files from `${CLAUDE_PLUGIN_ROOT}`, never from the project cwd or a filesystem-wide first
match. If the root or required file is unavailable, report the loading blocker
and stop dependent work; do not substitute a fallback procedure. Follow the
loaded procedure with this input:

$ARGUMENTS
