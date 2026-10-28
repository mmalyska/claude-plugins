---
description: "Create a GitHub PR from current branch with unpushed commits — discovers templates, analyzes changes, pushes"
argument-hint: [base-branch] (default: main)
---

Load the canonical procedure from the active installation before doing this task:

@${CLAUDE_PLUGIN_ROOT}/skills/pr/SKILL.md

Source navigation: [shared pr workflow](../skills/pr/SKILL.md).

Resolve runtime files from `${CLAUDE_PLUGIN_ROOT}`, never from the project cwd or a filesystem-wide first
match. If the root or required file is unavailable, report the loading blocker
and stop dependent work; do not substitute a fallback procedure. Follow the
loaded procedure with this input:

$ARGUMENTS
