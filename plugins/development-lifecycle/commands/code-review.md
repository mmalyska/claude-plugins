---
description: "Code review — local uncommitted changes or GitHub PR (pass PR number/URL for PR mode)"
argument-hint: [pr-number | pr-url | blank for local review]
---

Load the canonical procedure from the active installation before doing this task:

@${CLAUDE_PLUGIN_ROOT}/skills/code-review/SKILL.md

Source navigation: [shared code-review workflow](../skills/code-review/SKILL.md).

Resolve runtime files from `${CLAUDE_PLUGIN_ROOT}`, never from the project cwd or a filesystem-wide first
match. If the root or required file is unavailable, report the loading blocker
and stop dependent work; do not substitute a fallback procedure. Follow the
loaded procedure with this input:

$ARGUMENTS
