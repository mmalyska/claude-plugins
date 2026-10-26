# Hooks and Progress Tracking

Use hooks only when the active host supports the required event and the hook is
installed, configured, and trusted. A rule document does not install a hook.

Claude Code can use configured PreToolUse, PostToolUse, and Stop hooks. Inspect
the installed version's schema before changing settings. This collection's
Codex manifests explicitly disable bundled hooks; perform checks manually there.
Do not copy Claude tool matchers or permission settings into Codex configuration.

Use the current host's plan/task tool to track multi-step work, or a Markdown
checklist when no such tool is available. Record dependencies, completed work,
verification, and blockers. Respect the active sandbox and approval rules; do
not disable them to make an automation workflow run without supervision.
