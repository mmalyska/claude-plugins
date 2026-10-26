# Shared Claude Code and Codex workflows

Both hosts load the same `skills/` files directly. Installation requires no
build step or Python. Codex uses `.codex-plugin/plugin.json`; Claude retains its
existing manifests, native command and agent entrypoints, and hook configuration.
The marketplace identifier remains `mmalyska-claude-plugins`.

## Install

```sh
codex plugin marketplace add mmalyska/claude-plugins
codex plugin add personal-essentials@mmalyska-claude-plugins
```

Start a new session and use `$personal-essentials:personal-setup` to install the individual plugins,
or install only what you need with, for example:

```sh
codex plugin add frontend@mmalyska-claude-plugins
```

For local changes, register the checkout root with
`codex plugin marketplace add .`. To update a Git-backed marketplace, run
`codex plugin marketplace upgrade mmalyska-claude-plugins`, reinstall affected
plugins, and start a new session. Re-register a local marketplace if its path moves.

The shared skill format and plugin layout follow the
[official OpenAI skill documentation](https://learn.chatgpt.com/docs/build-skills)
and [plugin documentation](https://developers.openai.com/plugins/build/plugins).

## Invocation and migration

Codex exposes installed plugin skills as `$<plugin>:<skill-name>`; Claude retains its existing native command and agent
entrypoints and can load the same shared skills. The former prefixed Codex
adapter names are removed in this PR:

| Former Codex adapter | Shared skill |
| --- | --- |
| `$git-workflows-commit` | `$git-workflows:commit` |
| `$development-lifecycle-spec` | `$development-lifecycle:spec` |
| `$frontend-frontend-patterns` | `$frontend:frontend-patterns` |
| `$development-lifecycle-architect` | `$development-lifecycle:architect` |
| `$devcontainer-devcontainer-ghcr-image-pipeline` | `$devcontainer:devcontainer-ghcr-image-pipeline` |

Existing shared skill names are preserved, including `claude-devfleet` and
`renovate-automerge-rules`. Skill directories match their names. Rule indexes
remain `<plugin>-rules`. No duplicate host adapter catalog is maintained.

## Capability differences

| Capability | Shared behavior |
| --- | --- |
| Planning and file operations | Use tools exposed by the active host |
| Agent roles | Native Claude agents or available Codex delegation; sequential role passes when delegation is absent/disallowed |
| Rules | On-demand rule skills; no automatic Codex injection |
| Hooks | Claude hooks remain host-specific; Codex manifests explicitly use `hooks: []` |
| Configuration audit | Inspect the requested host's real configuration, regardless of which host runs the audit |
| Scheduling and memory | Verify available tools; otherwise provide manual execution and explicit state files |
| DevFleet | Optional MCP service callable by either host; its workers remain Claude agents |
| Third-party skills/tools | Discover before use; self-contained workflow or explicit missing-dependency result |

Skills do not install sandbox enforcement, schedules, or services by themselves.
New reports default to `.reports/agent-workflows/`; resuming work preserves its
established artifact directory. Creating installed skills uses the target host's
verified skill locations. Do not rewrite Claude configuration paths when Claude
configuration is the object being inspected.

## Maintenance and verification

Edit the shared skill body once. Claude command and agent files only link to the
shared procedure; host-only model/tool metadata stays in the native agent file.
Use common `name`/`description` frontmatter and put provenance under `metadata`.
Keep resources and local links inside the installed plugin. Keep the two manifests'
identity and version aligned. No generator or build step is required.

Optional maintainer tests require Python 3.10+; scanner tests additionally require
Bash and jq. Native discovery tests run when the corresponding Claude/Codex CLI
is installed, using temporary configuration and no model requests. Python is not required to install or use the plugins:

```sh
python3 -m unittest discover -s tests
claude plugin validate . --json
bash plugins/git-workflows/hooks/test-guard.sh
```

Validate each plugin with `claude plugin validate plugins/<name> --json`. Native
validation checks discovery/format, not every interactive workflow. For behavior
review, cover both hosts with specification, TDD, review, and worktree scenarios;
include missing delegation/scheduling, an unavailable scanner, and absent DevFleet.
Verify that missing capabilities produce a manual path or a clear prerequisite
instead of fabricated tool calls or successful background work.
