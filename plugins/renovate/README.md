# renovate

Renovate config authoring for Claude Code and Codex — skills and agent for `mmalyska/renovate-config` presets.

## Skills

- `renovate-extending-presets` — How to extend `mmalyska/renovate-config` in a repo's `renovate.json5`, including all 11 available sub-presets and the local override pattern
- `renovate-custom-regex-managers` — Comment-annotation patterns for tracking versions in YAML, Dockerfile, and devcontainer.json
- `renovate-automerge-rules` — Datasource-specific automerge configuration with branch/PR modes and file scoping

## Agent

- `renovate-auditor` — Audits a repo's Renovate config for consistency with `mmalyska/renovate-config` conventions

## Install

```sh
claude plugin install renovate@mmalyska-claude-plugins
```

## Usage

Shared skills are discovered after installation in either host. In Claude, the `renovate-auditor` native agent can be invoked through the available Agent tool; in Codex use `$renovate:renovate-auditor` or an authorized configured subagent:

```
Use the renovate-auditor agent to audit this repo's Renovate config.
```

## Codex

After registering this repository marketplace:

```sh
codex plugin add renovate@mmalyska-claude-plugins
```

Codex loads the same `skills/` files. Invoke them with `$<plugin>:<skill-name>`. Native
Claude agent entrypoints remain Claude-specific; their role skills work in either
host. Rules are on demand, and bundled Claude hooks are disabled in Codex.
