# devcontainer

Dev container setup skills for Claude Code — GHCR image pipelines, secrets injection, and Renovate digest pinning.

## Skills

- `ghcr-image-pipeline` — GitHub Actions workflow for building and publishing a custom devcontainer image to GHCR using `devcontainers/ci`, with tag transformation and Renovate trigger
- `secrets-injection` — Two-mechanism secret injection: Codespaces `"secrets"` block and local `devcontainer.env` file, with WireGuard VPN capabilities
- `renovate-digest-pinning` — How to pin a devcontainer image to a digest and keep it automatically updated by Renovate

## Agent

- `devcontainer-auditor` — Audits a repo's devcontainer configuration for unpinned images, missing secrets, and missing Renovate integration

## Install

```sh
claude plugin install devcontainer@mmalyska/claude-plugins
```

## Usage

Skills are available automatically after installation. The `devcontainer-auditor` agent is invoked via the Agent tool:

```
Use the devcontainer-auditor agent to audit this repo's devcontainer config.
```

Skills can be loaded on demand for specific tasks:

```
Use the ghcr-image-pipeline skill to set up a GHCR build pipeline for this repo's devcontainer.
```
