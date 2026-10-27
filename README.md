# mmalyska/claude-plugins

Personal plugin collection for Claude Code and Codex. Both use the shared
workflows in `plugins/`. No build step or Python installation is required.

## Install in Claude Code

```sh
claude plugin marketplace add mmalyska/claude-plugins
claude plugin install personal-essentials@mmalyska-claude-plugins
```

## Install in Codex

With a Codex version that supports plugins:

```sh
codex plugin marketplace add mmalyska/claude-plugins
codex plugin add personal-essentials@mmalyska-claude-plugins
```

Start a new Codex session and invoke `$personal-essentials:personal-setup` to install the development
plugins. You can also install individual plugins directly, for example
`codex plugin add frontend@mmalyska-claude-plugins`.

To try an unmerged change from this checkout, use
`codex plugin marketplace add .` instead of the GitHub source above.

Invoke workflows as skills, for example `$git-workflows:commit`,
`$development-lifecycle:spec`, or `$frontend:frontend-patterns`. Agent roles are
also exposed as skills, such as `$development-lifecycle:architect`.

See [installation and maintenance](docs/codex.md) and the
[host capability matrix and consumer strategy](docs/workflow/compatibility.md).
OpenCode has a documented manual path; native integration is deferred. STANDARD +
SOLO is the workflow default; other actor topologies require explicit authorization.
Native installation/discovery and live acceptance evidence remain NOT RUN in this
implementation session; no full workflow conformance or release readiness is claimed.

## Plugins

| Plugin | Description |
| --- | --- |
| `git-workflows` | Worktree-first enforcement (ships a hook), PR creation, commit conventions |
| `development-lifecycle` | [Spec→Plan→Build→Test→Review→Simplify→Ship](plugins/development-lifecycle/rules/common/workflow.md); STANDARD + SOLO by default |
| `dotnet` | .NET/C# agents and coding rules |
| `frontend` | React/Next.js and TypeScript rules |
| `renovate` | Renovate config authoring skills |
| `devcontainer` | Dev container setup skills |
| `backend` | API, database, NestJS, architecture, and MCP patterns |
| `devops` | Docker and deployment patterns |
| `security` | Code and host configuration security reviews |
| `agent-toolkit` | Planning, delegation, evaluations, and bounded automation |
| `android` | Android development (coming soon) |
| `personal-essentials` | Installs all plugins above |
