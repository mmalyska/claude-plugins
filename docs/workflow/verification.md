# Workflow verification and release gates

## Scope and decision

This record accompanies T11 of the [implementation plan](../plans/hybrid-ai-workflow/plan.md).
The [specification](specification.md) supplies requirements and the
[packaged contract](../../plugins/development-lifecycle/rules/common/workflow.md)
is the instruction source. [Compatibility](compatibility.md) distinguishes host
packaging, manual OpenCode and deferred consumers. There is no new execution
engine, evaluator service, model runner, scheduler or orchestrator.

Local implementation and static preparation are complete. **Release acceptance
is BLOCKED by required failed/unrun gates.** No full workflow conformance is claimed.
A successful static suite, local walkthrough or copied filesystem is not proof of
native installation, model obedience, independent review or runtime safety.

## Post-merge native metadata update

The user subsequently authorized isolated Claude/Codex CLI installation and
metadata discovery, without model turns or other actors. See the
[native evidence](evidence/2026-10-27-native-metadata.md) for trials against merged
T11 SHA `5d3703739ffff207cdc98f606a32c260794bc6f8` and the temporary-config fixture fix.
Claude metadata validation/install checks passed. Both hosts completed actual
fresh/remove/reinstall content checks; all 70 canonical skills were discovered
in Codex. Strict Codex discovery remains FAIL due to extra host-generated aliases,
whose relative source links fail containment/target validation. No gate is waived.
Earlier NOT RUN entries below describe the original T11 session, not this later
metadata authorization. All live scenario columns remain NOT RUN.

The user then included locally installed OpenCode. The
[OpenCode 2.2.0 evidence](evidence/2026-10-27-opencode-metadata.md) records PASS for
70/70 shared-skill discovery/body/link checks through explicit temporary sources,
including detach/reattach. Asynchronous metadata readiness is required. No
production adapter or namespace parity is claimed; live behavior remains NOT RUN.

### Codex alias fix and current metadata status

A later explicit fix/PR instruction authorized Codex manifest command-import
opt-outs and paired patch versions. See [post-fix evidence](evidence/2026-10-27-codex-alias-fix.md):
all three native methods PASS; actual fresh/remove/reinstall checks PASS for both
hosts; exact full-catalog Codex discovery is 70 canonical skills with zero aliases.
Earlier FAIL and NOT RUN snapshots are retained below and in dated evidence.
The observed alias blocker is resolved for Codex 0.164.0. Release remains blocked
by required live/platform/prior-version rollback gates; no full conformance claim.

## Revision and environment of observed checks

- Date: 2026-10-27; OS: Linux x86_64.
- Implementation/plugin base: `9b53f84fc53aae20ee03ecfd2a4f22638d841cf6`
  (main after merged T10 PR #18). No plugin source or manifest changes in T11.
- Candidate branch: `test/hybrid-ai-workflow-acceptance`; linked worktree:
  `/workspaces/claude-plugins/.worktrees/test/hybrid-ai-workflow-acceptance`.
- Testing state: checks ran against T11 test/docs/fixture changes on that base.
  Subsequent delivery is authorized; the PR commit identifies the published
  candidate. These results are not a committed-release/native acceptance run.
  A changed implementation invalidates affected evidence.
- Fixture: [S01–S16 data](../../tests/fixtures/workflow/scenarios.json), SHA-256:
  `8722331e50774544280f67ca6bcb71758fadf4d6e9dfe85c2cac045f0fda06a5`.
- Tools actually used: Python 3.15.0; GNU Bash 5.3.20; git 2.56.0; jq 1.8.2.
- Current owner/integrator: this session; DEEP + SOLO. No subagent, second harness,
  service connection, orchestrator or model turn was launched. Host versions are
  NOT RUN, because even version discovery through their CLIs is outside this scope.
- Primary checkout remains clean on main at the base above; prior worktrees and
  user state are preserved. No dotfiles/home-ops inspection or mutation occurred.

## Observed commands and results

| Check | Command / method | Exit / observed result | Meaning |
| --- | --- | --- | --- |
| Pre-edit baseline | `WORKFLOW_NATIVE_TESTS=0 python3 -B -m unittest discover -s tests` | 0; 59 PASS, 3 SKIPPED | Merged T10 baseline |
| T11 static suite | Same command on T11 candidate | 0; 67 PASS, 3 SKIPPED | 58 workflow, 7 manifest/source-copy, 2 scanner tests |
| Native CLI checks | Three gated methods in `test_host_discovery.py`, opt-in off | NOT RUN; all three SKIPPED | No native acceptance credit |
| Linux/Bash 5 guard | `bash plugins/git-workflows/hooks/test-guard.sh` with child-only signing config below | 0; 58 passed, 0 failed | Actual fixture shell execution; not model behavior |
| Bash 3.2 / macOS guard | Same guard suite on target platform | NOT RUN | Required platform gate remains blocked |
| Markdown, links, task scope and whitespace | Existing markdownlint-cli with MD013 disabled; source/own-repository targets and `git diff --check` | PASS | Local documentation integrity only |
| Native fresh/reinstall and live S01–S16 trials | Protocol below, no execution authorized here | NOT RUN | Required host and behavior gates remain blocked |

Guard fixtures make temporary commits. This session appended `commit.gpgsign=false`
to the child process Git config without overwriting inherited entries or changing
user/repository signing settings. Reproduce the configuration safely in an
isolated worktree with installed tools:

```python
import os
import subprocess

environment = dict(os.environ)
count = int(environment.get('GIT_CONFIG_COUNT', '0'))
environment[f'GIT_CONFIG_KEY_{count}'] = 'commit.gpgsign'
environment[f'GIT_CONFIG_VALUE_{count}'] = 'false'
environment['GIT_CONFIG_COUNT'] = str(count + 1)
subprocess.run(['bash', 'plugins/git-workflows/hooks/test-guard.sh'],
               env=environment, check=True)
```

Observed output ended with `58 passed, 0 failed`; the temporary local run log is
`/tmp/hybrid-t11-guard.log`. That path is ephemeral and is not release archival
storage. Preserve a redacted durable transcript when collecting release evidence.
The guard source is unchanged and its frozen-source regression check also passes.
Bash 3.2 compatibility is not inferred from Bash 5 success or historical evidence.

## Scenario specifications and local trace review

The fixture contains 16 scenarios and 34 named cases, each with both target hosts,
input/profile/topology, explicit authority/exclusions, available/missing capability,
required/forbidden actions, artifact expectations and actual instruction references.
It is **data only**: no command evaluation, subprocess dispatch or model call reads
action text as executable code. There is no Python implementation of English
workflow policy. Static validators check shape, source guards and reachability;
negative samples delete real source guards or data fields and must fail validation.

A separate SOLO trace review compared every case with the referenced instructions
and relevant existing guards. Each row below is a static/manual trace result,
not a live trial. For example: S07 partial failure requires a blocked dependent
integration record; no workers were started to demonstrate it. S06/S13 fixtures
exercise state fields/paths, not a real cross-harness transfer. A future live PASS
requires every named case on that host, including negative variants.

| Scenario | Cases | Local walkthrough | Claude live | Codex live | Static coverage / trace reviewed |
| --- | --- | --- | --- | --- | --- |
| S01 | 4 | PASS — static trace only | NOT RUN | NOT RUN | Default/direct-entry guidance; unknown enum and policy conflict variants |
| S02 | 1 | PASS — static trace only | NOT RUN | NOT RUN | Profile matrix, local checks, no forced QUICK dossier |
| S03 | 1 | PASS — static trace only | NOT RUN | NOT RUN | Profile/test/project-gate guards and reproducer case |
| S04 | 1 | PASS — static trace only | NOT RUN | NOT RUN | Blueprint Plan-only stop and durable DEEP SOLO artifacts |
| S05 | 2 | PASS — static trace only | NOT RUN | NOT RUN | Authority-before-capability and revoked-state guards |
| S06 | 3 | PASS — static trace only | NOT RUN | NOT RUN | Portable fields, stale base, unassigned receiver, missing authority/gates |
| S07 | 2 | PASS — static trace only | NOT RUN | NOT RUN | Distinct writer isolation, integrator scope and partial failure |
| S08 | 2 | PASS — static trace only | NOT RUN | NOT RUN | Read-only review and authorized sequential writer reuse |
| S09 | 4 | PASS — static trace only | NOT RUN | NOT RUN | Separate readiness/commit/PR/publication/merge/runtime scopes |
| S10 | 1 | PASS — static trace only | NOT RUN | NOT RUN | Unavailable reviewer and honest compatible local fallback |
| S11 | 1 | PASS — static trace only | NOT RUN | NOT RUN | 12/70/23 snapshot, standalone fallbacks, no provider dependency |
| S12 | 3 | PASS — static trace only | NOT RUN | NOT RUN | Denied creation, missing native tool and missing jq direct guards |
| S13 | 2 | PASS — static trace only | NOT RUN | NOT RUN | Historical path preservation and portable snapshot roundtrip |
| S14 | 2 | PASS — static trace only | NOT RUN | NOT RUN | Missing services/scanner/scheduler, no fake success, inert planning |
| S15 | 2 | PASS — static trace only | NOT RUN | NOT RUN | GitOps/HCP merge classification, fresh runtime consent |
| S16 | 3 | PASS — static trace only | NOT RUN | NOT RUN | Dirty primary, submodule and detached/external ownership |

Source-level checks preserve the frozen 12-plugin / 70-shared-skill / 23-wrapper
inventory. Filesystem copies of all catalog plugins exercise installed-content
assertions without starting hosts; corrupt manifest/resource samples are rejected.
Resource/fragment/path/symlink containment and existing entrypoint reachability
remain checked. These fixtures do not prove a host installs or discovers content.
Missing jq and denied worktree creation have direct instruction-deletion checks;
the existing real missing-jq shell fixture remains part of the static test suite.

## Evidence protocol for a separately authorized session

For executable preparation, operator task inputs for all 34 cases, scoring and
evidence templates, use the [live-trial guide](live-trials.md). It adds no execution
authority and records no live results.

Do not run this protocol under the current no-other-harness restriction. A future
maintainer must obtain actual authority for host processes and separately for
model turns or HANDOFF/PARALLEL/REVIEW actors; a metadata-test opt-in is not actor
or delivery consent. Preserve existing scope; ask only for missing action authority.
Use disposable repositories/worktrees, temporary host config and no production
runtime, credentials or services. Do not point a trial at home-ops/dotfiles.

### Required record per trial

Store a redacted Markdown transcript in the authorized evidence location and link
it from an updated verification record. Prefer an established project location;
without one use a task evidence subdirectory under its existing plan folder.
Every trial must record:

- Scenario/case IDs, actual input, expected required/forbidden actions and artifacts.
- Candidate/plugin full commit SHA, fixture digest, base SHA, branch/worktree, OS,
  exact host and tool versions, installed package versions and selected profile/topology.
- Current actor identities, accepted authority source and exact allowed tools,
  paths, read/write scopes, exclusions, side effects, owner and integrator.
- Available/missing tools and actual host configuration isolation; no secret values.
- Observed tool calls/actions and repository state before/after, produced artifact
  paths, gate commands, actual outputs/exit codes and timestamps. Redact secrets
  before persisting; do not redact facts needed to assess an authorization failure.
- PASS, FAIL, NOT RUN or NOT APPLICABLE with reason, unexpected behavior, blocking
  impact, exact next action, and links to preserved evidence. A proposed command or
  invented job ID is not output. NOT APPLICABLE cannot waive a required gate.
- Separate identity of reviewer only when a real authorized reviewer performed it;
  otherwise label a distinct local pass as self-review. Record stale/revoked scope
  and revalidation rather than treating snapshot text as a new grant.

### Native discovery and actual reinstall

1. Verify current official version-specific interfaces and installed CLI versions
   before using prepared tests. Their schemas are assumptions until exercised;
   confirm config overrides isolate the host without repurposing user HOME.
2. With metadata-process authority, a maintainer may run:

   ```sh
   WORKFLOW_NATIVE_TESTS=1 python3 -B -m unittest discover -s tests -p test_host_discovery.py -v
   ```

   Record real results for marketplace/plugin validation and each owning plugin
   standalone, owners combined, and all catalog plugins without Superpowers.
   The prepared tests use temporary `CLAUDE_CONFIG_DIR`/`CODEX_HOME` and an empty
   workspace; they compare source/T01 identities, manifests, wrappers, resources,
   links and actual Codex skill discovery. They issue metadata RPCs, no model turns.
3. The prepared install tests request install twice and verify each result. The
   second request may be an idempotent no-op: **it is not proof of actual reinstall**.
   Any repeated-install error is a FAIL to investigate, not silently accepted.
4. In the same disposable host config, use that pinned host's documented, verified
   remove/reinstall mechanism to remove only trial-owned plugin entries and install
   again. Record commands/output, before/after registration and cache state, enabled
   status, installed byte content/resource links, stable identity counts and actual
   discovery after a new session. If safe removal or isolation cannot be verified,
   leave actual reinstall NOT RUN. Never delete the checkout or a real user cache.
5. Preserve redacted logs and versions; update this evidence with an actual tested
   commit. Fresh, repeat-request and actual remove/reinstall results remain separate.
   Native metadata success alone does not establish any behavioral scenario PASS.

### Live behavior and rollback gates

Run all 34 cases for each of Claude and Codex under explicitly permitted scope.
Use real exposed tools and record actual calls; do not manufacture hypothetical
host transcripts. Non-SOLO cases need actor authorization before execution. If a
capability is absent, record the limitation and expected blocked/manual behavior;
mark any required unexercised independent-actor path NOT RUN. Do not silently turn
REVIEW into self-review or HANDOFF into local execution to claim the same result.

Exercise actual guard tests on Bash 3.2 and 5+ target environments with tool versions
and outputs. For S12 observe denied isolation, missing native worktree tooling and
missing jq without writing primary. For S07 use disposable disjoint writer scopes
and a real partial failure; record blocked integration. For S15 use disposable
simulated runtime targets, verify refusal/permission behavior and never touch real
GitOps/HCP. Runtime mutation tests need fresh separate consent; authorization
handling can be observed without causing production runtime effects.

Record a disposable reinstall of the known-good prior revision as rollback smoke,
then recheck identities, contained resource links and discovery. Preserve trial
artifacts and state. No real merge, publication, release or cleanup outside the
accepted trial scope follows from success. Reject release if required checks fail,
are missing, have stale revisions, lose discovery, write primary or damage history.

## Acceptance decision and deferred work

The [plan acceptance matrix](../plans/hybrid-ai-workflow/plan.md#t11-current-acceptance-evidence)
maps AC1–AC20 to evidence and limitations. Collection guidance/static checks are
prepared; Claude/Codex native and behavioral release acceptance is **NOT RUN**.
AC12/AC14/AC18 remain consumer-only follow-ups. OpenCode AC1/AC19 are limited to
the documented manual route; native parity and spike execution are deferred.
No optional service/orchestrator pilot was run; real pilot prerequisites remain.

T11 completes bounded local preparation, not release approval. Before a conformance
release, collect all required host/platform/behavior/rollback evidence on the exact
candidate and obtain separate delivery/release authority. Publish a verified
release/tag before consumers depend on it. Current results authorize no consumer
migration, merge, runtime action, tag or additional actor.
