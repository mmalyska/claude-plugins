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
To adapt another repository, follow the
[repository adoption guide](docs/workflow/repository-adoption-guide.md).
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

## Changing a plugin

Installed copies are keyed by plugin version, so a changed plugin must bump it:

```sh
scripts/bump_version.py <plugin> [patch|minor|major]
```

This updates both manifests and refreshes the fixture hashes of any protected file
you changed. CI fails a PR that changes a plugin without a bump. Merging to `main`
tags the commit `ai-workflow-vX.Y.Z`; accepting it is a separate PR in
`mmalyska/dotfiles` (see the [release sequence](docs/workflow/compatibility.md#release-sequence-and-rollback)).

## Optional scoped setup

Ask personal-setup for core (development-lifecycle + git-workflows) plus the
specific domain owners you need, or request the existing all-owner setup. An
unspecified setup retains the all-owner behavior. These are skill task inputs,
not extra CLI flags. Existing plugins are not removed; actual exposed catalog
cost depends on the host/session and has not been measured here.
