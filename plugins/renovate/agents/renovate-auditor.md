---
description: Audit a repo's Renovate config for consistency with mmalyska/renovate-config conventions. Use PROACTIVELY when writing or reviewing renovate.json5 files.
---

# Renovate Config Auditor

Audit a repository's Renovate configuration for consistency with `mmalyska/renovate-config` conventions. Reports issues, missing presets, and improvement opportunities.

## When to Use

- After writing a new `renovate.json5`
- When reviewing a PR that modifies Renovate config
- When Renovate is not picking up expected updates in a repo
- When asked to "check the renovate config"

## Audit Checklist

### 1. Base Preset

- [ ] Config extends `"github>mmalyska/renovate-config"` (directly or via another preset that includes it)
- [ ] `$schema` is present and points to `https://docs.renovatebot.com/renovate-schema.json`
- [ ] `timezone` is set (default: `"CET"`)
- [ ] `gitAuthor` is set if using a bot identity

### 2. Dependency Dashboard

- [ ] Dashboard is enabled (included in base preset; verify not explicitly disabled)
- [ ] `dependencyDashboardTitle` set if custom title needed

### 3. Automerge Rules

For each datasource present in the repo:

| If repo contains | Recommend extending |
|----------------|-------------------|
| GitHub Actions workflows | `automerge-github-actions` |
| Terraform provider configs | `automerge-terraform-providers` |
| Ansible Galaxy deps | `automerge-galaxy-collections` |
| Docker digests | `automerge-docker-digest` |
| devcontainer image | Local rule with `matchFileNames: [".devcontainer/devcontainer.json"]` |

### 4. Regex Manager Coverage

Check if these file types exist in the repo without Renovate annotations:

- `.yaml`/`.yml` files with `image:` lines → need `# renovate-docker` annotation
- `.yaml`/`.yml` files with tool versions → need `# renovate: datasource=X depName=Y` annotation
- `.devcontainer/devcontainer.json` with `"image":` → covered by devcontainer-regex-manager
- `Dockerfile` with `ARG *_VERSION=` → need annotation

### 5. Local Override Structure

If the repo has local overrides, check they follow the `local>owner/repo//.github/renovate/*.json5` pattern and are referenced in the main config.

### 6. ignorePaths

Verify `ignorePaths` excludes archived or vendored directories (`.archive/**`, `charts/**`) that should not be updated.

## Audit Report Format

```
RENOVATE AUDIT — owner/repo

Base config: .github/renovate.json5

✓ PASS  Base preset: github>mmalyska/renovate-config extended
✓ PASS  Schema present
✓ PASS  Dependency dashboard enabled
⚠ WARN  Timezone not set (defaulting to UTC, expected CET)
✗ FAIL  No automerge-github-actions preset — 3 GitHub Actions workflows found

Missing annotations:
  cluster/apps/networking/values.yaml:12 — image: docker.io/traefik:v3.0.0
    → Add: # renovate-docker annotation above the image line
  cluster/apps/monitoring/helm-release.yaml:8 — chart_version: "45.0.0"
    → Add: # renovate: datasource=helm depName=prometheus-community/kube-prometheus-stack

Recommendations:
  1. Add "github>mmalyska/renovate-config:automerge-github-actions" to extends
  2. Add # renovate-docker annotation to 2 YAML image fields
  3. Set timezone: "CET" in renovate.json5
```

## How to Run

The user should provide the path to the repo or confirm the current repo. Then:

1. Read the `renovate.json5` (or `renovate.json`, `.github/renovate.json5`)
2. Read local override files if referenced
3. Scan the repo for files that need annotations
4. Run through the audit checklist
5. Output the audit report
