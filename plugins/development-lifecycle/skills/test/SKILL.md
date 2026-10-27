---
name: test
description: "TDD workflow for features and reproducible bug fixes in Claude Code or Codex"
---

# Test

Read [the workflow contract](../../rules/common/workflow.md) first. Select profile
and topology independently; default STANDARD + SOLO. Apply mandatory project
policy in every profile. This procedure does not authorize another actor or
work beyond the requested stage.

Use the current user request as input. In a Claude command invocation, `$ARGUMENTS` carries that input; in Codex, use the text accompanying the skill.
Command-style examples below name workflows: in Codex select the corresponding
installed skill (`$plugin:skill`); do not execute slash commands in a shell.

## Select the verification technique

Use the profile and project policy from the workflow contract. The Test stage
requires meaningful verification, not universal test-first development.

- QUICK: the smallest useful regression or documented check; a documentation
  change may need Markdown/link validation, not a failing code test.
- STANDARD: appropriate automated behavior tests and project gates; prefer a
  reproducer for an observable bug.
- DEEP: layered positive/negative/integration scenarios appropriate to impact,
  with evidence and known gaps. It remains SOLO unless another actor is authorized.

Explicit `feature`, `tdd`, `fix:` and `bug:` inputs select the TDD/reproducer
procedures below when meaningful for the changed behavior. Project policy can
also require TDD. A verification-only request does not authorize Build: report
failures and proposed fixes rather than silently editing implementation. Infer
feature/fix intent from the existing task; ask only if missing intent changes
what can safely be verified.

## Discover project commands

Read repository instructions, tests and configuration, not only language markers.
Examples apply only when installed and configured:

| Evidence | Candidate command |
| --- | --- |
| Repository unittest suite under `tests/` | `python3 -B -m unittest discover -s tests` |
| Configured pytest suite | `pytest` |
| `package.json` scripts | Existing package-manager test script |
| `go.mod` / `Cargo.toml` | `go test ./...` / `cargo test` |
| Makefile or repository instructions | Documented test target |

Inspect test side effects before running them: discovery tests may launch other
harnesses or services. If a command exceeds session authority, run permitted
focused checks and report the rest NOT RUN. If no automated check fits, document
a meaningful manual check or ask for the missing project command. Never fabricate
success or fetch a runner, coverage package or dependency implicitly.

## Feature Mode — selected TDD

1. Derive a focused behavior from accepted requirements.
2. Write and run a test that fails for the expected missing behavior (RED).
3. If Build is authorized, implement the smallest change to pass it (GREEN).
4. Refactor within scope with tests green, then run relevant regressions.

Repeat per meaningful behavior. This is a technique, not another lifecycle.
Use the local guidance here or [tdd-guide](../tdd-guide/SKILL.md); an external
provider is optional.

## Bug Fix Mode — reproducer

1. Write or identify a reproducing check. Run it and confirm the expected failure.
   If it already passes, investigate whether the bug is fixed or the reproducer is
   wrong; report the evidence before assuming a fix is needed.
2. When implementation is authorized, fix the defect and rerun the reproducer.
   Do not weaken valid pre-existing expectations to obtain a pass. Correct an
   invalid test only with a demonstrated requirement mismatch.
3. Run affected regression checks and required project gates. Fix regressions
   introduced by the change within authorized scope, otherwise report a blocker.

If a code reproducer is unsuitable, explain the reason and record the meaningful
alternative check; do not manufacture RED for a wording-only change.

## Coverage and evidence

Apply the project's established coverage target, if one exists; never invent a
global percentage or require every test type for every edit. Run the configured
coverage tool only when applicable and installed. Required but unavailable checks
are NOT RUN and limit readiness; failed required gates block readiness. Record
commands, exit codes, changed behavior, results and uncovered risks.

## Lifecycle Position

Follow [the workflow contract](../../rules/common/workflow.md). Test verifies
Build; selected RED-GREEN-REFACTOR can guide Build without changing the lifecycle.
Review and Simplify follow, with affected checks rerun before Ship readiness.
No passing result authorizes commit, push, PR or runtime mutation.
