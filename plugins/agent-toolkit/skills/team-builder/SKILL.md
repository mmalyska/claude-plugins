---
name: team-builder
description: "Compose a team of available agent roles for a user-requested task in Claude Code or Codex."
metadata:
  origin: "community"
---

# Team Builder

Discover available roles, let the user choose, and synthesize their findings.

## Discover roles in the active host

- **Claude Code:** inspect the session's exposed agents. When shell access is
  available, `claude agents` lists installed agents. Read project/user agent
  definitions and plugin role skills as needed; do not assume every listed role
  is enabled in this session.
- **Codex:** inspect the exposed delegation tools and configured agent types.
  Read applicable `AGENTS.md` and available role skills. Markdown files under
  `agents/` are role references, not automatically registered Codex agents.
- In either host, include a user-specified role directory. Read frontmatter
  names/descriptions, falling back to the first heading/paragraph. Group by
  plugin or parent folder, preserving source identities when names collide.
- If no native agents are available, offer bundled role skills or user-supplied
  role descriptions for sequential analysis. Do not invent an agent registry.

## Select and execute

1. Show available domains and one-line role summaries. Accept role names or
   menu numbers. Use the task already supplied; ask only for missing intent.
2. Limit a team to five roles unless the user explicitly needs more. Explain
   overlap before adding redundant reviewers.
3. Read each chosen role and give it the task, relevant context, constraints,
   expected output, and a clear completion condition.
4. If delegation is available and authorized, use the host's actual tool:
   Claude's Agent tool or the Codex delegation tool exposed in the session.
   Parallelize independent read-only reviews. Concurrent writers need separate
   worktrees; do not send multiple writers into the same checkout.
5. If delegation is unavailable or disallowed, perform each role sequentially in
   the current session and label the results as role passes, not independent
   agents. Do not start a second CLI process to bypass that restriction.
6. Report failures per role and synthesize successful results: agreements,
   conflicting recommendations, unresolved questions, and next actions.

Do not select a different model unless the user or active instructions authorize
that choice. Do not install agents or modify host configuration during discovery.
