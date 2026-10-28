---
name: skill-create
description: "Analyze local git history to extract coding patterns and generate SKILL.md files. Local version of the Skill Creator GitHub App."
allowed_tools: ["Bash", "Read", "Write", "Grep", "Glob"]
---

Load the canonical procedure from the active installation before doing this task:

@${CLAUDE_PLUGIN_ROOT}/skills/skill-create/SKILL.md

Source navigation: [shared skill-create workflow](../skills/skill-create/SKILL.md).

Resolve runtime files from `${CLAUDE_PLUGIN_ROOT}`, never from the project cwd or a filesystem-wide first
match. If the root or required file is unavailable, report the loading blocker
and stop dependent work; do not substitute a fallback procedure. Follow the
loaded procedure with this input:

$ARGUMENTS
