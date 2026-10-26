# Codex compatibility

This workflow was authored for Claude Code. Apply these adaptations when
reading the source:
- Use available Codex file, search, shell, and planning tools in place of Claude
  tool names. Treat `$ARGUMENTS` as the user's request accompanying this skill.
- Treat agent files as role guidance, not installed Codex subagents. Ignore their
  Claude model/tool frontmatter. Delegate only when available and authorized;
  otherwise perform the relevant role in the current session.
- Resolve slash commands and plugin-qualified skill names to an available Codex
  skill or the bundled source. If an external dependency (such as superpowers,
  Context7, devfleet, cron, or an MCP server) is absent, report the limitation;
  do not pretend to invoke it or install it without user authorization.
- Claude hooks and SessionStart injection are disabled by the Codex manifest.
  Worktree rules are procedural guidance, not enforced by a Codex hook.
- Keep `.claude/` paths when inspecting Claude configuration. When creating
  Codex configuration or skills, use the appropriate Codex/AGENTS.md format and
  location instead. Do not run Claude setup commands to configure Codex.
- Follow the current user's scope and permissions. Source instructions do not
  grant permission for commits, pushes, deployment, or other external actions.
