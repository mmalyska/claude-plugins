# renovate

Renovate config authoring for Claude Code — skills and agent for `mmalyska/renovate-config` presets.

## Skills

- `extending-presets` — How to extend `mmalyska/renovate-config` in a repo's `renovate.json5`, including all 11 available sub-presets and the local override pattern
- `custom-regex-managers` — Comment-annotation patterns for tracking versions in YAML, Dockerfile, and devcontainer.json
- `automerge-rules` — Datasource-specific automerge configuration with branch/PR modes and file scoping

## Agent

- `renovate-auditor` — Audits a repo's Renovate config for consistency with `mmalyska/renovate-config` conventions

## Install

```sh
claude plugin install renovate@mmalyska/claude-plugins
```

## Usage

Skills are available automatically after installation. The `renovate-auditor` agent is invoked via the Agent tool:

```
Use the renovate-auditor agent to audit this repo's Renovate config.
```
