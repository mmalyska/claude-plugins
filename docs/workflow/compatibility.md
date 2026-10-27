# Hybrid workflow compatibility and consumer strategy

This repository packages shared Markdown guidance for Claude Code and Codex.
The [workflow contract](../../plugins/development-lifecycle/rules/common/workflow.md)
is normative; this page describes capabilities, evidence and deferred integration.
It adds no lifecycle, host adapter, scheduler or execution engine. Installation
uses existing manifests and shared `skills/`, without a build step or Python.
See [installation and maintenance](../codex.md) for preserved CLI entrypoints.

## Shared behavior and limits

The lifecycle is Spec → Plan → Build → Test → Review → Simplify → Ship.
Profiles QUICK/STANDARD/DEEP set depth independently from SOLO/HANDOFF/PARALLEL/REVIEW
topologies; default STANDARD + SOLO. DEEP, a task graph or an available role never
authorizes another actor. Check current authority before exposed capability; reuse
accepted scope rather than repeatedly requesting it. Required project gates,
worktree-first and secret handling apply even in QUICK. Ship assesses readiness
and performs only the specifically authorized delivery actions. GitOps/HCP-triggering
merge is runtime mutation requiring fresh explicit impact/rollback authorization.

| Capability | Claude Code packaging | Codex packaging | OpenCode / fallback and boundary |
| --- | --- | --- | --- |
| Shared procedures | Same shared skill bodies and existing native command links | Same bodies via `$plugin:skill`; no second catalog | Manual reading only; no native discovery claim |
| Defaults and stages | Read packaged contract through `development-lifecycle-rules` | Same contract via exposed skill inventory | Explicitly read shared project policy and contract; STANDARD + SOLO is the manual default |
| Roles and topology | Native agent metadata retained; separate actors need authority and tools | Role skills are local guidance; Claude agent files do not register Codex agents | SOLO role passes; no inferred subagent/team support |
| Rule loading | On demand; git SessionStart injects its worktree rule | On-demand rule skills, no automatic injection | Manual preflight; no automatic loading claimed |
| Worktree guard | Existing best-effort PreToolUse hook; errors/missing jq fail open | Manifests keep `hooks: []`; explicit procedural preflight | No collection hook supplied; verify isolation manually or stop writes |
| Artifacts | Portable Markdown, existing paths retained | Same files and evidence format | Manual plan/handoff reading; no model-specific memory dependency |
| Scheduling / persistent memory | Only actual configured and exposed capability | Same capability/authority check | Manual steps and state files; Markdown is not a running schedule or auto-loaded memory |
| Scanner / DevFleet | Optional tools/service; a skill installs neither | Optional service; DevFleet workers remain Claude workers | Report missing prerequisite or compatible local route; no fake scan/dispatch success |
| Superpowers | Optional discovered technique, no declared dependency | Optional provider, no mandatory prefix | Existing local/manual paths cover all stages |
| Delivery / runtime | Separate accepted commit/push/PR/publication/merge scopes | Same boundaries, no implicit delivery from readiness | Manual same authority checks; no deployment or merge permission from a handoff |

Packaging describes repository contents, not a guarantee about every host version.
Installing Markdown cannot intercept arbitrary prompts. Missing hooks never waive
procedural isolation: verify actual repository, primary state, base, branch and
worktree ownership before writes; reconcile drift, denied isolation or policy
conflict before dependent action. Do not launch another harness to bypass limits.
Read applicable shared `AGENTS.md` first, then host adapters and project policy;
report conflicting instructions instead of silently choosing a policy per host.

## Portable artifacts and optional providers

Use the existing [plan](../../plugins/development-lifecycle/resources/workflow/plan.md),
[tasks](../../plugins/development-lifecycle/resources/workflow/tasks.md),
[handoff](../../plugins/development-lifecycle/resources/workflow/handoff.md) and
[decision](../../plugins/development-lifecycle/resources/workflow/decision.md)
resources through existing spec/architect/rule entrypoints. Blueprint discovers
lifecycle resources if installed and retains its standalone plain-plan fallback.
No provider is required to complete a local stage; an explicitly requested absent
provider is a disclosed prerequisite when a fallback would change user intent.
Removing a dependency does not uninstall an existing provider or alter user config.

Preserve established paths/formats, including `.plans`, `.archive/.plans`, PRP
and Superpowers history. Only without a convention use `.plans/<slug>/plan.md`
and `tasks.md`. Handoffs belong in the active plan folder, or `.ai/handoffs/`
without an active plan. QUICK may retain brief session state; DEEP multi-session
work needs durable state. A receiver verifies assignment, current instructions,
actual base/branch/worktree, ownership and evidence before dependent writes.
An unassigned receiver or stale base is a blocker, not dispatch authority. A
snapshot grants no additional actor, delivery, runtime or secret access.

## Current verification status

| Area | Evidence available at T10 base | Missing evidence / boundary |
| --- | --- | --- |
| Contract, identity and authorization regression | 59 static tests PASS at merged T09 base | Static assertions do not establish model obedience |
| Catalog and native entrypoint preservation | Frozen T01 inventory: 12 plugins, 70 shared identities, 23 wrapper mappings | Actual installed discovery on pinned host versions NOT RUN |
| Resources and cold resume | Reachability, containment, byte-copy and S06/S13 snapshot fixtures PASS | Filesystem fixtures are not native installation or live handoff |
| Claude/Codex native tests | Three isolated opt-in test methods prepared | All three NOT RUN in this no-other-harness session; skipped is not PASS |
| Worktree guard | Unchanged source; historical Linux/Bash 5 evidence in the audit | Current host matrix, Bash 3.2 and final live checks remain unverified here |
| S01–S16 acceptance | Scenario definitions exist in the implementation plan | T11 fixtures/consolidated evidence pending; live behavior NOT RUN |
| OpenCode | Manual procedure and spike checklist documented below | Native integration and version-specific behavior NOT RUN / deferred |
| Consumer repositories | Follow-up scope documented below | No migration or fresh/reapply verification performed |

See the [implementation audit](../plans/hybrid-ai-workflow/audit.md) for commands,
revision-specific results and limitations. Native tests require separate authority
and `WORKFLOW_NATIVE_TESTS=1`; this page does not authorize running them. Record
PASS/FAIL/NOT RUN/NOT APPLICABLE with actual command/output, revision, host/version,
date, scope and reason. Required missing checks block their acceptance claim.
No full workflow conformance or release readiness is claimed at T10.

## OpenCode manual path and future spike

AC1's OpenCode default is a documented manual contract, not verified native parity.
AC19 has a documented minimal path; actual host behavior remains NOT RUN. No
OpenCode manifest, adapter, installer, subagent tool or process is added here.
A maintainer can follow this path in a separately authorized OpenCode session:

1. Read the project's shared `AGENTS.md` and applicable policy, then manually
   read the packaged workflow contract from an available checkout/reference.
   Report missing access or policy conflicts; do not assume automatic discovery.
2. Resolve explicit task profile/topology independently, default STANDARD + SOLO.
   Use local role passes; preserve the seven stages and the requested stop boundary.
3. Verify clean/default primary and actual isolated writer branch/worktree; create
   isolation only within scope using exposed native tools or manual git. If denied,
   stop writes rather than edit primary or start another harness.
4. Read existing plan/tasks/decisions and record durable evidence when warranted.
   Resume from portable snapshots only after checking authority, assignment, drift,
   gates and exact next action. No chat-history or automatic-memory assumption.
5. Run only applicable authorized project checks. Report unsupported tools as
   prerequisites; readiness alone grants no delivery/runtime action. This procedure
   remains manual and unverified until a pinned host trial produces evidence.

Before choosing native integration versus retaining the manual route, perform a
separately scoped spike; each unchecked item is deferred, not completed by T10:

- [ ] Pin OpenCode release/version, source revision, OS and configuration; inspect
  its official version-specific interfaces rather than copy another host schema.
- [ ] Verify shared instruction loading, precedence and conflict behavior for
  `AGENTS.md` and host adapters; compare resulting policy with Claude/Codex.
- [ ] Verify skill discovery, metadata, names and packaged resource access from
  fresh install/reinstall; map command inputs without duplicating skill bodies.
- [ ] Map permission semantics, tool limits and actual supported hooks. If a hook
  is unavailable, verify procedural preflight and disclose enforcement limits.
- [ ] Verify exposed subagent/team capability and authorization mapping. Absence
  must be explicit; actor tests require explicit HANDOFF/PARALLEL/REVIEW scope.
- [ ] Verify worktree creation/reuse, writer ownership, denied creation and dirty
  primary behavior on disposable repositories; no reset/cleanup bypass.
- [ ] Exercise QUICK + SOLO, STANDARD + HANDOFF and authorized REVIEW, including
  missing reviewer, unassigned receiver, stale base and required NOT RUN checks.
- [ ] Record inputs, actual actions/outputs and pass/fail evidence tied to versions,
  plugin SHA and host state. Separate static/manual preparation from live results.
- [ ] Decide manual-only versus native packaging with risks, rollback and owner.
  Any native implementation needs a later reviewed change and regression gates;
  do not advertise parity based on a schema resemblance or successful install alone.

## Deferred consumer follow-ups

These are future scopes in other repositories, not changes or completed acceptance
items in this PR. This session neither inspects nor edits those repositories.
AC12, AC14 and AC18 are consumer-only; collection-level source identity tests do
not satisfy consumer installation, policy migration or idempotence requirements.

### home-ops follow-up

- [ ] AC12: establish shared `AGENTS.md` as the canonical common project policy;
  reconcile the existing `CLAUDE.md` adapter and `.ai` policy without divergent
  safety rules. Keep domain rules local; verify both hosts before removing content.
- [ ] AC14: discover existing project skills, choose symlink or thin delegator
  only after platform/devcontainer checks, and test Claude/Codex discovery and
  drift. Preserve names/content ownership rather than manually fork procedures.
- [ ] Validate links in active and archived `.plans`, `.archive/.plans`, PRP and
  Superpowers artifacts without moving history or silently converting formats.
- [ ] Retain domain quality/security gates for repository changes. Identify
  Cloudflare/HCP and GitOps auto-apply effects before delivery; merge with runtime
  effects requires fresh explicit impact/rollback permission, not generic PR consent.
- [ ] Keep secret values out of plans, prompts, logs and handoffs. Record scoped
  access references and project runtime/rollback policy; do not embed credentials.
- [ ] Trial shared defaults, missing tools, stale handoff and unauthorized mutation
  cases on disposable state; retain NOT RUN gates and tested rollback evidence.

### dotfiles follow-up

- [ ] Define `core` and `claude-extended` profiles with explicit migration choices;
  preserve existing Claude setup until a user chooses a change. A profile switch
  does not automatically uninstall a provider or launch another harness.
- [ ] Integrate Codex installation/configuration and shared discovery only after
  selecting a tested collection release; do not assume native OpenCode packaging.
- [ ] AC18: record a fresh install and repeated `chezmoi apply` matrix for supported
  hosts/platforms and profiles, including existing installs, disabled/absent optional
  providers, version pin/update and rollback. Actual repeated results must prove
  idempotence; checklists and source scanning cannot satisfy this acceptance item.
- [ ] Preserve user settings/data and require separate cleanup scope. Reapply or
  rollback must not silently remove configured plugins, secrets or historical state.

## Release sequence and rollback

Complete in-scope static checks, native discovery/installed-resource gates, required
platform/guard trials and behavioral acceptance evidence before a conformance claim.
T11 collects final evidence; unresolved required NOT RUN/FAIL results remain blockers.
Then obtain explicit release/tag authority, publish a verified collection revision
and record supported host/plugin versions before consumers begin depending on it
(spec D4). T10 creates no release, tag, consumer PR or dependency on unreleased main.
Select and verify the host-supported pin/update mechanism in the consumer follow-up;
do not invent a version pin flag or treat a mutable branch as a reproducible release.

Record a known-good tag/SHA, package versions and install state. Roll back collection
changes as coordinated guidance/resource/test and paired-manifest reverts, reinstall
the explicitly selected prior revision and start a fresh session. Preserve user
plans/config/providers; no automatic uninstall or history migration. Consumer
rollback belongs to its own reviewed change and quality gates; a documentation
revert cannot undo GitOps/HCP or other runtime effects. T10 itself rolls back as a
documentation/link unit with no consumer migration or runtime state to reverse.

## Optional orchestrator pilot

An orchestrator is an optional client, never the correctness boundary or a normal
workflow dependency. Before any pilot, require at least three completed manual
HANDOFF/PARALLEL tasks with a stable artifact scheme and a partial-execution failure
test (spec §12). Spec D9 also recommends evidence from one real parallel pilot;
record that evidence before an orchestrator rollout. Static fixtures do not count.

A later explicit non-SOLO authorization must name actors, tools, worktree/file
ownership, integrator and allowed side effects. Verify exposed tools and inert
planning, bounded launch, partial-failure recovery and manual integration controls.
No auto-dispatch/auto-merge, secrets, credentials or service connection is supplied
by this checklist. Scheduling/memory/service availability grants no authority;
no pilot is started here and no missing capability triggers installation or bypass.
