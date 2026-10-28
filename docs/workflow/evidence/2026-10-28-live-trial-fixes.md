# Live-trial loading and isolation fixes

## Scope and baseline

Baseline candidate: `c0137fdc30a7ed0a0f2b639ce57c695a5d79ecd2`.
The user authorized fixes and a PR, with actual Claude/Codex reruns after merge.
This record summarizes observed defects; it does not replace original trial logs
or claim that proposed repairs have passed live verification.

Four local, non-interactive trials used fresh disposable configurations and
fixtures. Claude 2.1.312 configured with `opusplan` resolved to Sonnet 5.5;
Codex 0.164.0 used configured `gpt-6.1-sol`. Both loaded-contract bugfixes passed
independent two-test checks and preserved primary. Both spec-only trials left
source unchanged, with one baseline test passing independently.

| Host / path | Baseline verdict | Relevant observation |
| --- | --- | --- |
| Claude / loaded contract | FAIL | Before Edit, checked pwd/status/branch but omitted actual primary/base and Git isolation metadata |
| Claude / direct spec | FAIL | Relative command link searched from fixture; missing canonical spec led to an invented fallback without loading the contract |
| Codex / loaded contract | PASS | Recovered from absent origin/HEAD and unset init.defaultBranch; verified actual clean primary main before writing |
| Codex / direct spec | PASS | Loaded complete contract and produced conversation-only requirements with STANDARD + SOLO |

Earlier remote Claude direct-spec evidence also showed a contract read limited
to its first 80 lines. Claude test commands used tail pipelines without preserving
the test runner's exit code; independent direct checks established final results.
Duplicate bullets in pasted remote output remain unconfirmed and are not a basis
for an implementation change. Remote provenance gaps cannot be repaired retroactively.

## Changes

- Existing Claude command adapters load the same canonical skill through
  `@${CLAUDE_PLUGIN_ROOT}/skills/<name>/SKILL.md`, retain source-navigation links,
  pass task arguments and stop dependent work if required guidance is unavailable.
  Apply the correction across all 13 command wrappers to avoid retaining the same
  defect in adjacent commands. Native agent wrappers are unchanged.
- The spec and rules skills require complete initial contract reads, continuation
  after truncation and paths relative to the actual installed skill. No global
  first-match search, copied skill catalog or fallback procedure is introduced.
- The common contract states the first-write metadata checks explicitly, including
  existing worktrees, actual primary branch/HEAD/status and accepted base. The
  existing git-workflows rule/skill reinforce that procedure. A no-remote fixture
  uses verified local state explicitly; init.defaultBranch is not default proof.
- Testing guidance requires the original runner exit status and complete log when
  filtering output. Direct execution remains preferable for short checks.
- Paired Claude/Codex patch versions: development-lifecycle 1.2.8, git-workflows
  1.3.6, personal-essentials 1.0.3. Codex still imports shared skills with
  `commands: []` and `hooks: []`; existing identities and defaults are retained.

Claude's installed-root/file-reference syntax follows Anthropic's
[command-development reference](https://github.com/anthropics/claude-plugins-official/blob/main/plugins/plugin-dev/skills/command-development/references/plugin-features-reference.md).
This adapter-specific syntax stays outside shared skill bodies.

## Validation and limits

- PASS: `python3 -B -m unittest discover -s tests -v`: 72 tests, 69 passed,
  three opt-in native metadata tests skipped (NOT RUN).
- Packaging regression checks cover all existing identities/descriptions, rooted
  command targets, explicit arguments and missing-guidance boundaries. A standalone
  temporary installation with spaces covers valid, missing and escaping native
  file references; a consumer lookalike cannot satisfy a missing installed target.
- Contract negative samples detect removal of full-load, missing-guidance-stop,
  first-write and actual-primary declarations. Existing hook/scenario/static
  checks remain applicable; these do not prove model compliance.
- PASS: `git diff --check` and local Markdown file/fragment links.
- NOT RUN: post-fix native metadata and actual model trials. Live behavior is
  deliberately deferred until the merged candidate exists. Findings remain open
  pending affected reruns; no release gate is waived.

## Post-merge retest and rollback

1. Record the merged candidate SHA. Prepare fresh isolated profiles/fixtures and
   confirm the updated package versions; retain old failures as separate records.
2. Rerun Claude loaded-contract and direct-spec paths, then their Codex equivalents.
   Capture actual models, permission modes, complete canonical reads, tool calls,
   original exit statuses and independent before/after state.
3. For Claude direct spec, exercise headless and interactive entry. Require the
   installed canonical spec and complete contract, STANDARD + SOLO and no writes.
4. Before a loaded-contract fix writes, require actual writer/primary/base metadata
   checks. A `.worktrees` path or successful controller setup is insufficient.
   Require scoped edits, original test exit status, clean primary and unchanged refs.
5. Recheck canonical discovery with no Codex command aliases; continue abnormal
   worktree/default cases and the wider live matrix after focused reruns pass.

Rollback is a scoped revert of this PR and reinstall of the known-good package
revision in disposable profiles. Preserve evidence and user worktrees. The revert
would restore known guidance defects and is not release acceptance or permission
for runtime changes. No merge, deployment or live rerun occurs in this fix task.
