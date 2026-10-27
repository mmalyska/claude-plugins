# Codex generated-command alias fix — 2026-10-27

## Problem and supported fix

[Earlier native metadata trials](2026-10-27-native-metadata.md) found 11 generated
`source-command-*` aliases in the full Codex catalog. Migration copied Claude
command templates into `.codex-plugin/migrated-command-skills/`; relative links
then resolved from the generated directory to missing targets. All 70 canonical
shared skills were intact, but strict discovery correctly failed on extra names.

The user explicitly requested a fix and PR. The change sets `commands: []` in the
Codex manifests of development-lifecycle, git-workflows and personal-essentials,
the three plugins with legacy command directories. This prevents default legacy
command import into Codex. `skills: "./skills/"` and empty hooks remain unchanged.
Claude manifests retain normal command discovery; all 23 wrapper files and 70
shared skill bodies/names remain byte-for-byte unchanged. No generated skill
catalog, runtime alias resolver or lifecycle is added.

Upstream code resolves an explicit commands path array before falling back to
`commands/`: [manifest loader](https://github.com/openai/codex/blob/fab1a5754558ec90f27efa9b3bc4a1159802bc03/codex-rs/core-plugins/src/manifest.rs)
and [command migration](https://github.com/openai/codex/blob/fab1a5754558ec90f27efa9b3bc4a1159802bc03/codex-rs/core-plugins/src/command_migration/plugin.rs).
That source reference supports the mechanism; actual support in installed Codex
0.164.0 was confirmed by a disposable lifecycle probe yielding exactly 22 skills,
then the complete strict native suite and actual reinstall trials below.

## Candidate and authority

- Source/base: `5d3703739ffff207cdc98f606a32c260794bc6f8` (main after T11 PR #19).
- Branch/worktree: `test/hybrid-ai-workflow-native-verification`,
  `/workspaces/claude-plugins/.worktrees/test/hybrid-ai-workflow-native-verification`.
- Test state: candidate working tree; manifest SHA-256 values and versions are in
  [structured evidence](2026-10-27-codex-alias-fix.json). The PR identifies the
  published commit. No clean committed-release or live-behavior run is implied.
- Versions aligned across Claude/Codex: lifecycle 1.2.7, git-workflows 1.3.5,
  personal-essentials 1.0.2. Patch increments select new installed cache versions;
  consumers must reinstall/update and start a fresh session rather than assume
  an already loaded old package changed in place.
- Environment: Linux x86_64, Python 3.15.0, Claude 2.1.312, Codex 0.164.0.
- Execution: DEEP + SOLO. User authorization includes the fix, bounded native
  metadata verification, commit/push/PR; no model, additional actor, merge,
  runtime mutation, consumer migration or release/tag is authorized.

## Native test result

The earlier CODEX_HOME fixture correction is included: create its temporary
config directory before invoking Codex. The strict `actual == expected` discovery
assertion is unchanged. Tests use temporary config/workspaces; no real user plugin
is removed or host user configuration edited. No model turn is issued.

Actual command:

```sh
WORKFLOW_NATIVE_TESTS=1 python3 -B -m unittest discover -s tests -p test_host_discovery.py -v
```

Actual output:

```text
test_claude_accepts_marketplace_and_plugin_contents (test_host_discovery.HostDiscoveryTest.test_claude_accepts_marketplace_and_plugin_contents) ... ok
test_claude_installs_owners_without_external_workflow_provider (test_host_discovery.HostDiscoveryTest.test_claude_installs_owners_without_external_workflow_provider) ... ok
test_codex_discovers_shared_skills_after_direct_install (test_host_discovery.HostDiscoveryTest.test_codex_discovers_shared_skills_after_direct_install) ... ok

----------------------------------------------------------------------
Ran 3 tests in 66.347s

OK
```

All three methods PASS with no skips. This covers marketplace/all-plugin Claude
validation, standalone owners/combined owners/all-catalog install and repeat
requests, contained source resources and actual exact Codex skill discovery.
The whole catalog exposes exactly 70 canonical skills in Codex, zero generated
aliases. No extra-name allowance or relaxed link gate was introduced.

## Actual remove/reinstall result

The same diagnostic procedure recorded in the earlier native evidence was rerun
against the fixed candidate, now requiring exact Codex equality and zero aliases.
It executes serially for both hosts with fully copied disposable marketplaces,
not real worktree source removal. For each selection it installs, checks content,
removes only trial-owned entries, asserts the installed list is empty, and installs
again. Source/manifest/wrapper/resource byte checks and actual Codex discovery run
after each install. Metadata RPCs are initialize, initialized and skills/list.

| Host | Selection | Phase | Canonical skills | Content / registration | Extra aliases |
| --- | --- | --- | --- | --- | --- |
| claude | development-lifecycle | fresh | 22 | PASS | not applicable |
| claude | development-lifecycle | remove-reinstall | 22 | PASS | not applicable |
| claude | git-workflows | fresh | 5 | PASS | not applicable |
| claude | git-workflows | remove-reinstall | 5 | PASS | not applicable |
| claude | agent-toolkit | fresh | 14 | PASS | not applicable |
| claude | agent-toolkit | remove-reinstall | 14 | PASS | not applicable |
| claude | owners combined | fresh | 41 | PASS | not applicable |
| claude | owners combined | remove-reinstall | 41 | PASS | not applicable |
| claude | all 12 plugins | fresh | 70 | PASS | not applicable |
| claude | all 12 plugins | remove-reinstall | 70 | PASS | not applicable |
| codex | development-lifecycle | fresh | 22 | PASS | 0 |
| codex | development-lifecycle | remove-reinstall | 22 | PASS | 0 |
| codex | git-workflows | fresh | 5 | PASS | 0 |
| codex | git-workflows | remove-reinstall | 5 | PASS | 0 |
| codex | agent-toolkit | fresh | 14 | PASS | 0 |
| codex | agent-toolkit | remove-reinstall | 14 | PASS | 0 |
| codex | owners combined | fresh | 41 | PASS | 0 |
| codex | owners combined | remove-reinstall | 41 | PASS | 0 |
| codex | all 12 plugins | fresh | 70 | PASS | 0 |
| codex | all 12 plugins | remove-reinstall | 70 | PASS | 0 |

All 20 phase records PASS; Codex full-catalog counts are 70 after both fresh install
and actual remove/reinstall, with zero aliases and no alias link errors. Final
observed diagnostic output:

```text
PASS: content and fresh/remove-reinstall for both hosts; exact canonical Codex discovery with zero aliases
```

Transient logs are `/tmp/hybrid-native-alias-fixed.log` and
`/tmp/hybrid-native-fixed-reinstall.log`; the output above and structured phase
records preserve the durable summary. Earlier failure observations remain intact
as pre-fix evidence. These local-marketplace trials do not establish Git-backed
marketplace update behavior or rollback to a prior revision.

## Regression, review and remaining acceptance

Static verification: 68 PASS via `WORKFLOW_NATIVE_TESTS=0 python3 -B -m unittest
discover -s tests`; three native skips in that separate static run are not the
native result above. New manifest regression checks all command-owning plugins
explicitly disable Codex command migration and retain Claude command scanning.
Existing identity, metadata, links, wrapper and source-body checks stay enabled.
Markdown lint and local links/structured-evidence checks pass.

A separate local review checked manifest-only scope, paired versions, preserved
wrappers/skills/Claude command registration, missing directory correction, exact
native discovery and honest pre-/post-fix evidence. This is self-review; no worker
or independent reviewer was started. [OpenCode metadata evidence](2026-10-27-opencode-metadata.md)
remains a separate prior explicit-source result, not a new production adapter
trial. Shared source bodies/resources consumed there are unchanged by this fix.

The observed Codex alias blocker is resolved for the tested version. Release
still requires live S01–S16 with explicit model/actor authority, Bash 3.2 and actual
prior-revision rollback smoke; consumer/OpenCode production work stays deferred.
Do not convert metadata success into full workflow or model-obedience acceptance.
Rollback reverts the paired manifest changes, test guard and follow-up references;
reinstall the selected previous revision in a fresh session and retain user
artifacts/providers/config. A revert restores the earlier alias behavior and is
not a runtime rollback. PR creation does not authorize merge or release.
