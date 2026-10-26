# Codex support

The builder reads the Claude marketplace and plugin manifests and creates a
self-contained local Codex marketplace in `build/codex`. Python 3.10+ is the only
build dependency. Generated files are ignored by Git; edit the shared sources in
`plugins/`, then rebuild. Run the builder from any directory using its full path.
The printed output path is the directory to register with Codex.

The package layout follows the [official OpenAI plugin documentation](https://developers.openai.com/plugins/build/plugins).
It uses `.codex-plugin/plugin.json`, a `skills/` directory, and a marketplace at
`.agents/plugins/marketplace.json` inside the generated root. No changes to your
personal Codex configuration happen until you run the install commands.

| Claude component | Codex behavior |
| --- | --- |
| Skills | Small Codex entrypoints link to the original workflows and resources |
| Slash commands | Skills named `<plugin>-<command>`; accompanying user text replaces `$ARGUMENTS` |
| Agent definitions | Role skills named `<plugin>-<agent>`, not configured Codex subagents |
| Rules | On-demand `<plugin>-rules` skills; no automatic injection |
| Hooks | Excluded; no automatic worktree enforcement |
| `personal-essentials` | Bundles all workflows instead of running Claude installation commands |
| Android | Empty placeholder, matching the existing plugin |

All workflow skill names have a plugin prefix to avoid collisions in the bundle.
Existing skill names are preserved after the prefix, including names that differ
from their source folder. The original content hierarchy is copied under
`content/<plugin>/`, preserving relative links and supporting files. This is build
output, not a second maintained copy.

Adapters explain Claude-to-Codex tool mapping and dependency limitations. Workflows
that inspect Claude configuration remain Claude-specific reference material;
packaging them does not implement those features in Codex. Claude-native runtime
features, third-party skills such as superpowers, and MCP servers are not installed
by the builder. Missing dependencies must be reported when a workflow needs them.
The adapter layer provides reuse, not a guarantee of behavioral parity.

After pulling changes or editing sources:

```sh
python3 scripts/build_codex.py
codex plugin marketplace upgrade mmalyska-codex-plugins
codex plugin add personal-essentials@mmalyska-codex-plugins
```

Restart your Codex session. Keep `build/codex` available at its registered path;
after moving the checkout, remove and re-add the marketplace using its new path.
For desktop versions without CLI installation, select the registered marketplace
in the Plugins Directory and install there.

Validate packaging without installing anything:

```sh
python3 -m unittest discover -s tests
```

The checks cover catalog resolution, bundled entrypoints, resource containment,
aggregate coverage, hook exclusion, and reproducible rebuilds. They do not test
every workflow in an interactive Codex session.
