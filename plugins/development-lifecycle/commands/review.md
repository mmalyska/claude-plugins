---
description: "Five-axis code review — correctness, readability, architecture, security, performance"
argument-hint: "[file or directory to review, or blank to review recent changes]"
---

Load the canonical procedure from the active installation before doing this task:

@${CLAUDE_PLUGIN_ROOT}/skills/review/SKILL.md

Source navigation: [shared review workflow](../skills/review/SKILL.md).

Resolve runtime files from `${CLAUDE_PLUGIN_ROOT}`, never from the project cwd or a filesystem-wide first
match. If the root or required file is unavailable, report the loading blocker
and stop dependent work; do not substitute a fallback procedure. Follow the
loaded procedure with this input:

$ARGUMENTS
