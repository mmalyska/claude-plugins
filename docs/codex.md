# Codex support

Install directly from GitHub with a Codex version that supports plugins:

```sh
codex plugin marketplace add mmalyska/claude-plugins
codex plugin add personal-essentials@mmalyska-claude-plugins
```

Start a new Codex session and invoke `$personal-setup` to install the individual
development plugins. Alternatively, install only the plugins you need:

```sh
codex plugin add frontend@mmalyska-claude-plugins
codex plugin add git-workflows@mmalyska-claude-plugins
```

For a local checkout, register its root with `codex plugin marketplace add .`.
The existing marketplace name stays `mmalyska-claude-plugins` for both hosts.
There is no generated directory, build command, or Python requirement for use.

The layout follows the [official OpenAI plugin documentation](https://developers.openai.com/plugins/build/plugins).
Codex reads the existing `.claude-plugin/marketplace.json` catalog and each
plugin's `.codex-plugin/plugin.json` manifest. That manifest selects the static
`codex-skills/` entrypoints. Each entrypoint links to its shared skill, command,
or agent source inside the same plugin, so the installed copy is self-contained.
Claude continues to use its existing manifests and components.

| Shared component | Codex behavior |
| --- | --- |
| Skills | Static entrypoints link to the original workflows and resources |
| Slash commands | Skills named `<plugin>-<command>`; accompanying user text replaces `$ARGUMENTS` |
| Agent definitions | Role skills named `<plugin>-<agent>`, not configured Codex subagents |
| Rules | On-demand `<plugin>-rules` skills; no automatic injection |
| Hooks | Explicitly disabled in Codex manifests; no automatic worktree enforcement |
| `personal-essentials` | `$personal-setup` installs individual plugins using Codex commands |
| Android | Empty placeholder, omitted from personal setup |

For example, use `$git-workflows-commit`, `$development-lifecycle-spec`, or
`$development-lifecycle-architect`. Workflow entrypoints retain the existing
skill name after the plugin prefix. Shared `CODEX.md` guidance in each plugin
explains tool mapping, Claude configuration paths, and absent dependencies.
Claude runtime features, superpowers skills, and MCP servers are not installed
by these manifests. Workflows inspecting Claude configuration remain specific
to that environment; adapters do not guarantee behavioral parity.

To refresh a Git-backed marketplace and update an installed plugin:

```sh
codex plugin marketplace upgrade mmalyska-claude-plugins
codex plugin add frontend@mmalyska-claude-plugins
```

Reinstall each plugin you want to update, then start a new Codex session. For
local marketplaces, edit or pull the checkout and reinstall the affected plugins.
If you move the checkout, remove and re-add the marketplace with its new path.

When maintaining this repo, edit shared workflows in place. Add or update the
matching static entrypoint when adding, renaming, or changing the description of
a workflow. Keep Codex identity/version metadata aligned with the Claude manifest.
Do not add Claude tool or model frontmatter to Codex entrypoints. Keep `hooks: []`
explicit so Codex does not discover the Claude hook configuration by default.

Optional maintainer checks use Python's standard-library test runner:

```sh
python3 -m unittest discover -s tests
```

These checks validate the checked-in manifests, workflow coverage, resource
containment, and disabled hooks; Python is not needed to install or run plugins.
