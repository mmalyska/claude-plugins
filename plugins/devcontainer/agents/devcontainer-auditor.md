---
description: Audit a repo's devcontainer configuration for unpinned images, missing secrets declarations, and missing Renovate integration. Use PROACTIVELY when writing or reviewing devcontainer.json.
---

# Devcontainer Config Auditor

Audit a repository's devcontainer setup for best-practice compliance — digest pinning, secret management, lifecycle hooks, and Renovate integration.

## When to Use

- After creating or modifying `.devcontainer/devcontainer.json`
- When reviewing a PR that touches devcontainer configuration
- When a devcontainer is broken or has unexpected behavior
- When asked to "check the devcontainer config"

## Audit Checklist

### 1. Image Pinning

- [ ] The `"image"` field includes a digest (`@sha256:...`)
- [ ] The digest is not `sha256:` followed by zeroes or placeholder text
- [ ] Tag is meaningful (e.g. `main`, `latest`, a version) not just a digest with no tag

**Finding:** If image has no digest — flag as HIGH. Tag-only images rebuild silently when the upstream tag is updated, causing non-reproducible environments.

### 2. Secrets Management

- [ ] All required credentials have entries in the `"secrets"` block (for Codespaces)
- [ ] `.devcontainer/devcontainer.env.sample` exists with commented keys
- [ ] `.devcontainer/devcontainer.env` is in `.gitignore`
- [ ] `runArgs` includes `--env-file .devcontainer/devcontainer.env` (for local)
- [ ] `initializeCommand` creates `devcontainer.env` from sample if missing

**Finding:** Missing `"secrets"` block — MEDIUM. Missing `devcontainer.env.sample` — HIGH (developers won't know what secrets are needed). `devcontainer.env` not in `.gitignore` — CRITICAL (would leak credentials).

### 3. WireGuard Capabilities (if applicable)

If the container uses WireGuard:
- [ ] `--cap-add=NET_ADMIN` in `runArgs`
- [ ] `--device=/dev/net/tun` in `runArgs`

### 4. Lifecycle Hooks

Check whether these lifecycle script hooks are appropriate for the repo:
- [ ] `initializeCommand` — environment setup that must run before container starts
- [ ] `onCreateCommand` — one-time setup after container is created
- [ ] `updateContentCommand` — runs after a code update (e.g. install deps)
- [ ] `postStartCommand` — runs every time the container starts

**Finding:** If significant setup logic is in `postStartCommand` that should only run once — suggest moving to `onCreateCommand`.

### 5. Renovate Integration

- [ ] `renovate.json5` extends `github>mmalyska/renovate-config` (includes devcontainer-regex-manager)
- [ ] A `packageRule` with `matchFileNames: [".devcontainer/devcontainer.json"]` exists for digest automerge
- [ ] The image build workflow triggers Renovate after publishing (if using a custom image)

**Finding:** Missing Renovate integration — MEDIUM. The digest will become stale and the environment will drift.

### 6. User Identity

- [ ] `"remoteUser"` and `"containerUser"` are set (typically `"vscode"`)
- [ ] Correct permissions for the user to access mounted files

## Audit Report Format

```
DEVCONTAINER AUDIT — owner/repo

Config: .devcontainer/devcontainer.json

✓ PASS  Image pinned to digest: ghcr.io/owner/repo-devcontainer:main@sha256:abc123
✓ PASS  Secrets block present (5 secrets declared)
✓ PASS  devcontainer.env.sample exists
✓ PASS  devcontainer.env in .gitignore
⚠ WARN  No updateContentCommand — consider adding dep install on content update
✗ FAIL  No Renovate automerge rule for .devcontainer/devcontainer.json
✗ FAIL  devcontainer.env.sample not found in repo

Required actions (FAIL):
  1. Add packageRule with matchFileNames: [".devcontainer/devcontainer.json"] to renovate config
     (see renovate-digest-pinning skill)
  2. Create .devcontainer/devcontainer.env.sample with commented secret keys
     (see secrets-injection skill)

Suggestions (WARN):
  1. Add updateContentCommand: "bash .devcontainer/scripts/updateContentCommand.sh"
```

## How to Run

1. Read `.devcontainer/devcontainer.json`
2. Check for `.devcontainer/devcontainer.env.sample`
3. Check `.gitignore` for `devcontainer.env` entry
4. Read `renovate.json5` for Renovate integration
5. Run through the audit checklist
6. Output the audit report
