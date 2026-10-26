---
name: personal-setup
description: Install this collection's development plugins in the requested Claude Code or Codex environment.
---

# Personal Setup

Install plugins in the host the user requested; default to the active host. Do
not install into both hosts implicitly. Check that the marketplace is registered
with the name below. If it is missing, use the repository source or local checkout
provided by the user. For GitHub, register it with the selected host:

```sh
# Claude Code
claude plugin marketplace add mmalyska/claude-plugins
# Codex
codex plugin marketplace add mmalyska/claude-plugins
```

## Claude Code

```sh
claude plugin install agent-toolkit@mmalyska-claude-plugins
claude plugin install backend@mmalyska-claude-plugins
claude plugin install devcontainer@mmalyska-claude-plugins
claude plugin install development-lifecycle@mmalyska-claude-plugins
claude plugin install devops@mmalyska-claude-plugins
claude plugin install dotnet@mmalyska-claude-plugins
claude plugin install frontend@mmalyska-claude-plugins
claude plugin install git-workflows@mmalyska-claude-plugins
claude plugin install renovate@mmalyska-claude-plugins
claude plugin install security@mmalyska-claude-plugins
```

## Codex

```sh
codex plugin add agent-toolkit@mmalyska-claude-plugins
codex plugin add backend@mmalyska-claude-plugins
codex plugin add devcontainer@mmalyska-claude-plugins
codex plugin add development-lifecycle@mmalyska-claude-plugins
codex plugin add devops@mmalyska-claude-plugins
codex plugin add dotnet@mmalyska-claude-plugins
codex plugin add frontend@mmalyska-claude-plugins
codex plugin add git-workflows@mmalyska-claude-plugins
codex plugin add renovate@mmalyska-claude-plugins
codex plugin add security@mmalyska-claude-plugins
```

Run only the selected host's commands. Stop on an installation error and report
which plugins succeeded and which remain. Ask the user to start a new session
after installation. Android is a placeholder and is intentionally omitted.
This does not install external MCP services or enable Codex hooks.
