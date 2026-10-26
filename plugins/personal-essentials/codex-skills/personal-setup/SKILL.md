---
name: personal-setup
description: Install the mmalyska development plugin collection in Codex when the user requests personal plugin setup.
---

Install the following plugins from the already configured marketplace. If the
marketplace is missing, ask the user for their checkout or repository source.
Do not run Claude plugin installation commands.

```sh
codex plugin add git-workflows@mmalyska-claude-plugins
codex plugin add development-lifecycle@mmalyska-claude-plugins
codex plugin add dotnet@mmalyska-claude-plugins
codex plugin add frontend@mmalyska-claude-plugins
codex plugin add backend@mmalyska-claude-plugins
codex plugin add devops@mmalyska-claude-plugins
codex plugin add security@mmalyska-claude-plugins
codex plugin add agent-toolkit@mmalyska-claude-plugins
codex plugin add renovate@mmalyska-claude-plugins
codex plugin add devcontainer@mmalyska-claude-plugins
```

Stop and report an installation failure rather than continuing blindly. Report
which plugins were installed and ask the user to start a new Codex session.
Android is a placeholder and is intentionally omitted. No hooks or third-party
MCP servers are configured by this setup.
