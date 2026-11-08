---
description: "Define requirements before planning or coding, sized to the profile, with a separate specification and verification gate for DEEP. Use for a requested spec or when planning work that is or may be DEEP."
argument-hint: [feature idea, or blank to start with questions]
---

Load the canonical procedure from the active installation before doing this task:

@${CLAUDE_PLUGIN_ROOT}/skills/spec/SKILL.md

Source navigation: [shared spec workflow](../skills/spec/SKILL.md).

Resolve runtime files from `${CLAUDE_PLUGIN_ROOT}`, never from the project cwd or a filesystem-wide first
match. If the root or required file is unavailable, report the loading blocker
and stop dependent work; do not substitute a fallback procedure. Follow the
loaded procedure with this input:

$ARGUMENTS
