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

## Select the requested owners

When the user names a subset, install only those owners using the selected host's
commands below. A requested core setup means development-lifecycle + git-workflows;
add only the named domain owners. Toolkit and security are independent optional
owners, not new dependencies. With no requested subset, keep the existing all-owner
setup below. Ask only when the requested subset is ambiguous.

These are task choices, not host CLI flags. Keep installed owners in place;
this setup request does not authorize uninstalling plugins or changing global
profiles. Installation success does not establish which metadata a session exposes.
Finish with the selected/succeeded/remaining owner list and request a fresh session.

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
