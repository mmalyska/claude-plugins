---
description: "Review delivery readiness, verify checks, and perform the authorized commit, PR, or branch-finishing workflow"
argument-hint: "[PR title, or blank to use task/spec name]"
---

Load the canonical procedure from the active installation before doing this task:

@${CLAUDE_PLUGIN_ROOT}/skills/ship/SKILL.md

Source navigation: [shared ship workflow](../skills/ship/SKILL.md).

Resolve runtime files from `${CLAUDE_PLUGIN_ROOT}`, never from the project cwd or a filesystem-wide first
match. If the root or required file is unavailable, report the loading blocker
and stop dependent work; do not substitute a fallback procedure. Follow the
loaded procedure with this input:

$ARGUMENTS
