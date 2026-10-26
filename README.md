# mmalyska/claude-plugins

Personal plugin collection for Claude Code and Codex. Shared workflows live in
`plugins/`; Codex packages are generated from those same sources.

## Install in Claude Code

```sh
claude plugin add marketplace github:mmalyska/claude-plugins
claude plugin install personal-essentials@mmalyska/claude-plugins
```

## Install in Codex

Requires Python 3.10+ and a Codex version with plugin support. From this checkout:

```sh
python3 scripts/build_codex.py
codex plugin marketplace add ./build/codex
codex plugin add personal-essentials@mmalyska-codex-plugins
```

Start a new Codex session after installation. You can install individual plugins
instead, for example `codex plugin add frontend@mmalyska-codex-plugins`.
Install either the bundle or individual plugins to avoid duplicate skills.

Invoke workflows as skills, for example `$git-workflows-commit`,
`$development-lifecycle-spec`, or `$frontend-frontend-patterns`. Agent roles are
also exposed as skills, such as `$development-lifecycle-architect`.

See [Codex compatibility and maintenance](docs/codex.md) for differences and updates.

## Plugins

| Plugin | Description |
|---|---|
| `git-workflows` | Worktree-first enforcement (ships a hook), PR creation, commit conventions |
| `development-lifecycle` | Spec→Plan→Build→Test→Review→Simplify→Ship workflow |
| `dotnet` | .NET/C# agents and coding rules |
| `frontend` | React/Next.js and TypeScript rules |
| `renovate` | Renovate config authoring skills |
| `devcontainer` | Dev container setup skills |
| `android` | Android development (coming soon) |
| `personal-essentials` | Installs all plugins above |
