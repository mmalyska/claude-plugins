# personal-essentials

Setup skill that installs the development plugins into the requested host.

## Usage

After installing this plugin, run `/personal-setup` in Claude Code to install all remaining plugins.

## Quick start (new machine)

```sh
claude plugin marketplace add mmalyska/claude-plugins
claude plugin install personal-essentials@mmalyska-claude-plugins
# Then in Claude Code: /personal-setup
```

## Codex

After registering this repository marketplace:

```sh
codex plugin add personal-essentials@mmalyska-claude-plugins
```

Codex loads the same `skills/` files. Invoke them with `$<plugin>:<skill-name>`. Native
Claude agent entrypoints remain Claude-specific; their role skills work in either
host. Rules are on demand, and bundled Claude hooks are disabled in Codex.

After installation, start a new session and invoke
`$personal-essentials:personal-setup`. The shared procedure selects Codex commands
when running in Codex and Claude commands when running in Claude.
