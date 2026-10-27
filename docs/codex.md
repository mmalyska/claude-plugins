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
adapter names were replaced by the shared identities:

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

## Shared workflow and capability differences

Read the [packaged workflow contract](../plugins/development-lifecycle/rules/common/workflow.md)
through the existing `development-lifecycle-rules` skill. It owns the single seven
stages and independent QUICK/STANDARD/DEEP profiles and SOLO/HANDOFF/PARALLEL/REVIEW
topologies. Default STANDARD + SOLO applies; availability, DEEP or a plan alone
never authorizes another actor. Existing explicit scope is reused without repeated
permission menus. Readiness, delivery, external publication and runtime are distinct.

| Capability | Claude Code | Codex | Missing capability / boundary |
| --- | --- | --- | --- |
| Shared procedures | Same `skills/` bodies, native command links | Same bodies via `$plugin:skill` | Local/manual guidance; no second catalog or build generator |
| Agent roles | Native definitions keep name/tools/model | Markdown files do not register native Codex agents | Local SOLO role passes; separate actors require authorization and actual exposed tools |
| Rule loading | On demand; existing git SessionStart injects worktree rule | On-demand rule skills, no automatic injection | Installing Markdown cannot intercept every arbitrary prompt |
| Worktree enforcement | Existing best-effort PreToolUse guard | Explicit procedural preflight; manifests keep `hooks: []` | Blocked isolation stops writes; missing jq cannot waive the invariant |
| Scheduling / persistent memory | Only actually exposed configured features | Only actually exposed configured features | Manual run/state files, no invented schedule or auto-loaded memory |
| Scanner / DevFleet | Optional tools/service, not installed by a skill | Same optional service; DevFleet workers remain Claude workers | Prerequisite or compatible local path, no fake scan/dispatch success |
| Superpowers | Optional discovered technique provider | No mandatory provider/prefix | Local Spec/Plan/Build/Test/Review/Simplify/Ship paths remain available |
| Runtime / delivery | Exact accepted action scope | Same authority boundaries | Fresh runtime consent for GitOps/HCP-triggering merge; no blanket override |

Prefer applicable shared `AGENTS.md` policy in either host, then host adapters;
report conflicts before dependent actions. When auditing configuration, inspect the
requested host's real settings without rewriting paths for the running host.
Preserve established artifact locations; new reports can use `.reports/agent-workflows/`
and durable plans without a project convention use `.plans/<slug>/`. Templates and
full OpenCode/consumer strategy remain later work, not an installed native adapter.

Superpowers is not a declared dependency. Removing the declaration does not uninstall
an existing user's provider, alter their host settings or rewrite historical plans.
If an explicitly selected optional technique is absent, use the existing local
procedure or report a prerequisite where intent requires that provider. A single
owning plugin can be used without installing the other workflow owners.

## Maintenance and verification

Edit the shared skill body once. Claude command and agent files only link to the
shared procedure; host-only model/tool metadata stays in the native agent file.
Use common `name`/`description` frontmatter and put provenance under `metadata`.
Keep resources and local links inside the installed plugin. Keep the two manifests'
identity and version aligned. No generator or build step is required.

Optional maintainer tests require Python 3.10+; scanner/guard checks additionally
need Bash and jq. Installing plugins requires no Python. Static checks compare the
T01 catalog, all 70 shared identities and 23 wrapper mappings; paired manifest
identity/version and plugin-local links remain regression gates.

```sh
python3 -B -m unittest discover -s tests -p test_workflow_contract.py
python3 -B -m unittest discover -s tests -p test_codex_manifests.py
python3 -B -m unittest discover -s tests -p test_rule_scanners.py
```

Native CLI tests require explicit `WORKFLOW_NATIVE_TESTS=1` and an available CLI.
They launch host processes but no model turns, and are prohibited in a session
that forbids other harnesses. Without opt-in their skipped results mean NOT RUN,
not PASS. A separately authorized maintainer can run:

```sh
WORKFLOW_NATIVE_TESTS=1 python3 -B -m unittest discover -s tests -p test_host_discovery.py -v
```

Prepared tests validate the marketplace/all plugins and fresh standalone/combined
owning-plugin installs with temporary host configuration and an empty temporary
workspace. Expected installed names come from source/T01 evidence, never from
whatever happened to install. Codex checks actual skill discovery; Claude checks
installed enabled content and wrappers. No provider is installed for these cases.
Claude isolation uses the documented [configuration directory override](https://code.claude.com/docs/en/settings),
and its [plugin CLI JSON listing](https://code.claude.com/docs/en/plugins/cli-reference#plugin-list)
supplies installed metadata. No user configuration directory or HOME is repurposed
as scratch storage. Verify installed CLI versions and these test interfaces before
claiming native compatibility; preparation/format validation is not execution proof.

Native installation/discovery and behavioral scenarios remain release gates until
actually run with evidence. Test standalone owners, combined owners, missing
Superpowers/delegation/scheduling/scanner/DevFleet and permitted local fallbacks;
static text checks cannot prove model behavior. Preserve previous versions for
rollback, reinstall an explicitly selected prior revision and start a fresh session;
never remove optional providers or user data as automatic rollback.
