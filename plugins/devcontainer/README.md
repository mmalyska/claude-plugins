# devcontainer

Dev container setup skills for Claude Code and Codex — GHCR image pipelines, secrets injection, and Renovate digest pinning.

## Skills

- `devcontainer-ghcr-image-pipeline` — GitHub Actions workflow for building and publishing a custom devcontainer image to GHCR using `devcontainers/ci`, with tag transformation and Renovate trigger
- `devcontainer-secrets-injection` — Two-mechanism secret injection: Codespaces `"secrets"` block and local `devcontainer.env` file, with WireGuard VPN capabilities
- `devcontainer-renovate-digest-pinning` — How to pin a devcontainer image to a digest and keep it automatically updated by Renovate

## Agent

- `devcontainer-auditor` — Audits a repo's devcontainer configuration for unpinned images, missing secrets, and missing Renovate integration

## Install

```sh
claude plugin install devcontainer@mmalyska-claude-plugins
```

## Usage

Shared skills are discovered after installation in either host. In Claude, the `devcontainer-auditor` native agent can be invoked through the available Agent tool; in Codex use `$devcontainer:devcontainer-auditor` or an authorized configured subagent:

```
Use the devcontainer-auditor agent to audit this repo's devcontainer config.
```

Skills can be loaded on demand for specific tasks:

```
Use the devcontainer-ghcr-image-pipeline skill to set up a GHCR build pipeline for this repo's devcontainer.
```

## Codex

After registering this repository marketplace:

```sh
codex plugin add devcontainer@mmalyska-claude-plugins
```

Codex loads the same `skills/` files. Invoke them with `$<plugin>:<skill-name>`. Native
Claude agent entrypoints remain Claude-specific; their role skills work in either
host. Rules are on demand, and bundled Claude hooks are disabled in Codex.
