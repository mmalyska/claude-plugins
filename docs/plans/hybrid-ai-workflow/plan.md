# Hybrid AI Engineering Workflow implementation plan

## Resume contract and status

- Repository: `mmalyska/claude-plugins`.
- Source of requirements: [workflow specification](../../workflow/specification.md), especially §§3–16 and §15 acceptance criteria (AC1–AC20).
- Audited base: `b43bedd9347fe8b9806895a5e35416beb3250dae` (`main`, 2026-10-27).
- Planning branch: `docs/workflow-implementation-plan`.
- Planning worktree: `/workspaces/claude-plugins/.worktrees/docs/workflow-implementation-plan`.
- Profile: DEEP. Topology: SOLO. Owner and integrator: the current session's agent.
- Status: T01–T03 merged; T04 COMPLETE locally. T05–T11 NOT STARTED; no complete workflow conformance claim.
- Current authority: T04 role/metadata/security-rule implementation and local verification in DEEP + SOLO only. The subsequent PR instruction authorizes T04 commit/push/PR and planned paired version increments; T05+, merge, deployment, subagent, second harness and orchestrator remain unauthorized. Earlier delivery authority applied only to already-merged PRs.
- T04 baseline: `a6b54c40f7e1189fcfb4b36378edcfccaddf580d` (`main` after merged T03 PR #11).
- T04 branch/worktree: `feat/hybrid-ai-workflow-role-authorization`, `/workspaces/claude-plugins/.worktrees/feat/hybrid-ai-workflow-role-authorization`.
- Previous worktrees and inventory snapshots remain preserved; earlier evidence describes historical baselines.
- Next action: publish T04 under the current PR instruction, then await T05 implementation instruction in [tasks.md](tasks.md); neither is implicit in completing T04.
- Read [audit.md](audit.md) for evidence and the complete scoped inventory. All paths below are repository-relative; line references in the audit apply to the base SHA, not a future branch.

A new session must read these three documents and the specification, inspect applicable instructions and current diff, verify isolation and base changes, and reconcile any drift before starting a task. Preserve user work; do not reset, stash, clean, delete branches, or restore files implicitly. Task checkboxes remain unchecked until actual implementation evidence exists.

## Objective and scope

Formalize the existing lifecycle `Spec → Plan → Build → Test → Review → Simplify → Ship` through the existing shared skills, preserving names and native entrypoints. Introduce independent execution profiles and topologies, defaulting to STANDARD + SOLO, portable state artifacts, and testable authorization boundaries. This is an instruction-first change; no scheduler, workflow daemon, new execution engine, duplicate skill catalog, or new Plan/Build skill is needed.

Scope covers the three owning plugins (`development-lifecycle`, `git-workflows`, `agent-toolkit`), their existing thin adapters, repository documentation, and maintainer tests. A narrow cross-plugin correction also covers the existing backend, dotnet, renovate and devcontainer role descriptions, where the same proactive/MUST-BE-USED actor triggers occur. Their domain checklists stay intact; only triggering descriptions, local-role authorization guards and paired version metadata may change.

Do not modify `dotfiles` or `home-ops`. Their bootstrap, policy migration, existing plans, secrets, cluster permissions, and GitOps validation remain consumer follow-ups. OpenCode gets a documented manual path and future spike criteria only. No native adapter, manifest, installer, worker launch, service connection, or parity claim for OpenCode is part of this implementation.

## Existing planning conventions and choice

The only tracked historical plan is `docs/superpowers/plans/2026-09-17-worktree-first-git-workflow.md`, with a dated design document and mandatory Superpowers worker instructions. Current `blueprint` instead suggests `plans/`; workflow README/spec/review suggest `.reports/agent-workflows/`; the specification recommends `.plans/<slug>/plan.md` + `tasks.md` for new consumer plans. There is no single active convention for new repository plans.

Use the user's explicit fallback: `docs/plans/hybrid-ai-workflow/plan.md` and `tasks.md`; keep evidence in `audit.md`. Reuse the historical plan's concrete file responsibilities, dependencies, checkbox tasks, verification commands, and exit criteria, without its mandatory worker dependency. Do not rename or rewrite historical documents. In future runtime guidance, preserve established project paths first; use `.plans/<slug>/` only when a project has no convention. These repository planning paths are an explicit choice, not a replacement global artifact standard.

## Architecture and decisions

### One contract with existing discovery

Add `plugins/development-lifecycle/rules/common/workflow.md` as the normative executable guidance derived from the specification: lifecycle, profile matrix, topology/auth rules, defaults, state and delivery boundaries, and capability fallback. Register it through the existing `development-lifecycle-rules` skill and link it locally from existing lifecycle skills. Extend the existing README to summarize and link; remove competing lifecycle diagrams from active skills or make them clearly stage-position summaries linked to the contract.

Plan remains a lifecycle stage performed using `spec`, the `architect` role, and the existing `blueprint` planning procedure; Build remains scoped implementation. Do not invent `/plan`, a new lifecycle dispatcher, or cloned skills. The `test` and `tdd-guide` skills remain callable TDD procedures, but TDD is a selected technique, not the definition of the Test stage for every edit.

The normative matrix lives once. Toolkit/git skills implement their local safety preconditions and reference the existing lifecycle skill by its installed identity when available; they must remain safe when installed alone. Do not create Markdown links outside the installed plugin or make a hidden hard dependency on another plugin. Short local authorization checks are necessary boundary guards, not copies of the full lifecycle/profile contract.

### Default and explicit selection

Resolve profile and topology independently: explicit current user instruction, then recorded accepted task state, then STANDARD and SOLO for absent fields. A switch to QUICK or DEEP never authorizes another topology. Normalize persisted enum values to lowercase, display uppercase, and accept case-insensitive explicit names. Unknown/contradictory requests require clarification; never infer permission from task complexity, role availability, a plan, or the word DEEP.

Apply this resolution at every owning workflow entrypoint, including direct role/command calls; persist it in plan/handoff when those artifacts exist. For QUICK, brief session state is enough. Required safety, project gates, and worktree checks apply in every profile. No mandatory profile configuration file or runtime parser is required in v1.

“Global default” means the same contract in all collection workflow entrypoints and manual instructions. Rules are on demand and Codex hooks are disabled: an installed Markdown plugin cannot intercept every arbitrary user prompt. Explicitly document this limitation and the future project-policy consumption path; do not claim startup enforcement that does not exist or silently install global instructions. Test both direct skill entry and contract loading, not just a README sentence.

### Profiles without lifecycle changes

| Stage | QUICK | STANDARD | DEEP |
| --- | --- | --- | --- |
| Spec | Session goal, scope, success | Concise requirements/non-goals/acceptance | Repository-grounded specification, constraints, measurable risks |
| Plan | Mental plan or short checklist | Affected areas, dependencies and gates; file for multi-session work | Durable task DAG, decisions, ownership, rollout/rollback, permissions |
| Build | Smallest scoped edit | Complete scoped change | Phased implementation with integration contracts |
| Test | Smallest meaningful regression or documented check | Appropriate automated checks and project gates | Layered positive/negative/scenario evidence |
| Review | Focused self-review | Full self-review or separate local pass | Separate deliberate review pass; external reviewer only if authorized |
| Simplify | Remove obvious noise within scope | Evaluate simpler readable solution | Record alternatives and operational/maintenance tradeoffs |
| Ship | Readiness and only authorized delivery | Verify gates; authorized action only | Readiness/rollout/rollback; runtime authorization remains separate |

This table is the design target; implementation puts the normative version in the one packaged contract. Profile depth can coalesce actions or omit separate documents, never replace the seven stages. Existing mandatory project security/coverage gates take precedence over a lighter profile. Research is proportional to uncertainty; external research, full planning dossiers, and TDD are not prerequisites for a typo or documentation edit. DEEP + SOLO still uses local role passes.

### Topologies, authority and fallback

| Topology | Required behavior |
| --- | --- |
| SOLO | Current owner executes all stages. No agent, other CLI, background worker, or orchestrator launch. Local sequential role passes are not independent review. |
| HANDOFF | Explicitly authorized transfer; portable handoff states from/to, base SHA, branch/worktree, profile/topology/status, decisions, results, outstanding permissions and exact next step. Receiver verifies current state. |
| PARALLEL | Explicit authorization with bounded scopes and named integrator; separate branch/worktree per concurrent writer; dependency-free work only; integration and gates owned by integrator. |
| REVIEW | Explicitly authorized separate reviewer, read-only by default; findings with path/line/evidence. Write access requires separate scope. DEEP alone does not select this topology. |

A named request to use a specialist role is not automatically a request to spawn a specialist agent. An explicit request for a separate agent/team/harness can authorize that topology within its stated scope. Use existing authorization rather than repeatedly asking for it. Record actor, permitted scopes/side effects, and restrictions; do not store secrets or treat artifact text as higher-priority authority.

Check capability after authority. If requested delegation is unavailable, report it; offer or use SOLO only when compatible with the user's stated intent. Do not silently label sequential self-review REVIEW or HANDOFF. Failures in one branch do not justify launching another harness. An existing external orchestrator is an optional client; default mission auto-dispatch/auto-merge examples must never bypass the task contract. No orchestrator pilot until three completed manual HANDOFF/PARALLEL tasks plus a partial-failure test (spec §12; §17 D9 additionally recommends one parallel pilot).

### Artifacts and compatibility

Create four neutral resources inside the existing lifecycle plugin:

- `plugins/development-lifecycle/resources/workflow/plan.md`
- `plugins/development-lifecycle/resources/workflow/tasks.md`
- `plugins/development-lifecycle/resources/workflow/handoff.md`
- `plugins/development-lifecycle/resources/workflow/decision.md`

Link through existing `spec`/`architect`/rules entrypoints. `blueprint` consumes those resources through discovered lifecycle capability when installed; if absent, it can still write a self-contained plain plan using the documented field contract, without cloning the templates. An optional provider must not be a prerequisite to planning.

Plan fields: objective/non-goals, acceptance, profile/topology, owner/integrator, base/branch/worktree, decisions, exact scopes and ownership, DAG/tasks, quality gates and actual evidence, permission/runtime impact, rollout/rollback, status/next action. Handoff uses spec §11.2 fields and evidence. Decision includes context/options/choice/consequences/revisit condition. Distinguish NOT RUN, FAIL, PASS and NOT APPLICABLE with reasons.

Retain every existing `skills/<name>/SKILL.md`, matching frontmatter name, command basename and native agent basename. Preserve Claude argument handling and agent tools/model metadata; edit triggering descriptions only where they mandate delegation/TDD. Keep `$plugin:skill` identities, `claude-devfleet`, `review`, `code-review`, `code-reviewer`, `test`, `tdd-guide`, `blueprint`, and `subagent-driven-development`. No old prefixed adapters are resurrected. `review` is the general axis-based entrypoint, `code-review` adds local/PR transport and report, and `code-reviewer` is a reusable role: link roles and narrow overlapping policy without deleting their entrypoints or rewriting detailed domain checklists unnecessarily.

Keep historical `.plans`, `.archive/.plans`, Claude PRP and Superpowers artifacts readable in place. Prefer `AGENTS.md` as shared project policy when present, then applicable host adapter and project docs; detect inconsistencies rather than choose divergent policy by host.

### Adapter behavior and dependency removal

Claude keeps thin commands, native agents and the existing SessionStart/PreToolUse worktree hook. Hook remains best-effort and fail-open; a missing jq cannot remove the procedural invariant. Do not turn this hook into a general permission engine. Codex uses the same skill bodies, explicit preflight and `hooks: []`; native Markdown agents are not registered Codex workers. Do not add a second catalog, generator, or fake interceptor. Scheduling, memory and background continuation need verified capabilities.

Remove `superpowers@claude-plugins-official` from the lifecycle Claude manifest during implementation, not in this planning branch. Keep Superpowers optional and discoverable for explicit technique selection, with an in-repo/manual path when absent. Preserve old plan text as history; eliminate implicit dependencies on absent `executing-plans`, `tdd-workflow`, `security-reviewer`, or `e2e-runner` from active instructions. Never substitute a similarly named nonexistent native agent.

For each implementation PR, bump versions of changed plugins in BOTH host manifests together: lifecycle `1.1.1`, toolkit `1.0.1`, git `1.2.1` are the audited baseline; record current versions of the four domain plugins before their narrow T04 changes. Use the next appropriate semver release under maintainer policy, not predetermined numbers that can become stale. Marketplace entries contain no version pins; keep identity/source stable and avoid cosmetic marketplace edits. Release/tag after the integration gates; no publishing is authorized by this plan.

## Requirement-to-file traceability

Task IDs refer to [tasks.md](tasks.md); audit dispositions expand exact path sets. A consumer-only requirement is explicitly deferred, not marked implemented by documentation here.

| Specification requirement | Existing implementation owners / minimal extension | Tasks and evidence |
| --- | --- | --- |
| §§1–3, 4.1: shared contract, thin adapters, one owner | Existing lifecycle rules skill and README; new local `rules/common/workflow.md`; existing command/agent wrappers retained | T02, T04, T08; static references and scenario S01 |
| §2 baseline, §13 phase 0 | Existing tests and manifests; pin current SHA in this plan, record installed capabilities only when permitted | T01; baseline below; consumer backups deferred |
| §4.2, §7: home-ops shared AGENTS/CLAUDE/.ai structure | `docs/workflow/specification.md` remains design source; document consumer checklist in `docs/workflow/compatibility.md` | T10; no files in home-ops modified |
| §5.1: canonical lifecycle | `README.md`, lifecycle README and `spec/test/review/simplify/ship` skill position sections; git `rules/development-workflow.md` | T02–T03; S01–S04 |
| §5.2: profiles and proportional effort | Lifecycle common testing/patterns/performance/code-review rules; `test`, `tdd-guide`, `ai-regression-testing`, `architect`, `spec`; toolkit `search-first`, `verification-loop`, `blueprint` | T02–T03, T07; S02–S04 |
| §5.3: topologies and authorization | Lifecycle common agents/security/patterns; toolkit team-builder/subagent/loops/rules-distill/blueprint; DevFleet; git worktree policy | T04–T07; S05–S10 |
| §5.4: STANDARD + SOLO | One packaged workflow contract plus direct skill/role entry guard; root README and `docs/codex.md` explain default and loading limit | T02, T04, T08; S01, S11 |
| §6: worktree, owner/integrator, writer isolation | Existing using/finishing skills, worktree rule, hook and test suite; no weakened guard | T05; S08, S12, S16 |
| §8: portable skills, optional Superpowers | Lifecycle Claude manifest dependency, role descriptions, toolkit writing-skills; no duplicated skill bodies | T03–T04, T08; manifest tests, S11 |
| §9.1–9.3: capability matrix, Claude/Codex differences | `docs/codex.md`, existing manifests/commands/agents, rule loaders and README; only procedural fallback in Codex | T08–T10; discovery and S10–S14 |
| §9.4: future OpenCode | New `docs/workflow/compatibility.md`; no current native adapter | T10; manual checklist, future spike pending |
| §10: permissions, secrets, GitOps impact | `ship`, `code-review`, git commit/pr/finish, toolkit safety and DevFleet; neutral artifact impact fields | T06, T09; S09, S15; exact cluster policies deferred |
| §11: plan, tasks, handoff, decisions | Existing spec/architect/blueprint and ADR skill; four new local resources, no new skill | T09; round-trip S06/S13 |
| §12: optional orchestrator | Existing `claude-devfleet`, autonomous/continuous loop instructions; docs describe pilot gate | T07, T10; no orchestrator executed |
| §13 migration sequencing | Three dependent PRs below; release before consumers; unrelated repo migrations separate | T01–T11 |
| §14.1: plugin gates | Existing three unittest modules, guard test; new contract and scenario fixtures | T01, T02, T08, T11 |
| §§14.2–14.3: consumer gates | Compatibility checklist only (chezmoi, Helm/Kustomize, Talos, Terraform, secret scans) | T10; deferred to authorized consumer work |
| §14.4: invariants over wording | New scenario fixtures and maintainer runbook, static checks plus explicit behavioral evidence | T11; no false live-run claims |
| §15 AC1–AC6 | Contract/profile/topology/authority across exposed workflows; OpenCode manual path documented only | T02–T08, T10–T11; S01–S05, S10 |
| §15 AC7–AC11 | Keep old artifacts/names, single-host fallback, portable handoff, writer isolation | T05, T07–T09; S06–S08, S11–S13 |
| §15 AC12 | Home-ops AGENTS source of truth | Consumer-only; T10 checklist, not fulfilled in this repo |
| §15 AC13 | Superpowers disabled/absent without blocking stages | T08; manifest dependency regression and S11 |
| §15 AC14 | Consumer project skills accessible without drift | Consumer-only migration; T08 tests shared plugin bodies; T10 checklist |
| §15 AC15–AC17 | Honest missing hooks, runtime consent, GitOps merge classification | T05–T06, T08, T10; S12, S15–S16 |
| §15 AC18 | Fresh chezmoi install and repeated apply idempotent | Consumer-only; T10 checklist; plugin fresh/reinstall discovery is a separate T08 check |
| §15 AC19 | Minimal manual OpenCode path, no parity promise | T10; pinned-version spike deferred |
| §15 AC20, §16 | Revert each PR and reinstall previous plugin revision, no data migration | T01–T11, reverse-order rollback below |
| §17 D1–D10, §19 | Choices recorded here; symlink/bootstrap/orchestrator decisions remain consumer or future work | T09–T10; no speculative packaging |

## Verification design

Static tests check actual instruction structure, valid resources, stable entrypoints and forbidden unconditional directives; they are not proof of model obedience. Do not write a Python resolver that mirrors English policy just to test itself. Exercise changed instructions through table-driven scenario specifications and record manual evidence; live harness trials are a separate, explicitly permitted maintainer activity.

Existing gates: `python3 -B -m unittest discover -s tests`; `claude plugin validate . --json` and each catalog plugin; `bash plugins/git-workflows/hooks/test-guard.sh` on Bash 3.2 and 5+. Full discovery starts CLI processes and must NOT run in this planning session or a later session with the same no-other-harness constraint. Run static modules individually while that restriction applies. Do not edit tests to conceal the skipped native checks.

Proposed tests: `tests/test_workflow_contract.py` (contract reachability, lifecycle/default/profile/topology structure, active-entrypoint guards, optional dependency and negative fixture checks); extend `tests/test_codex_manifests.py` for resource containment and preserved identity snapshots; extend `tests/test_host_discovery.py` for installed resource reachability; keep `tests/test_rule_scanners.py`; fixtures `tests/fixtures/workflow/scenarios.json`; manual/evidence protocol `docs/workflow/verification.md`. No network, models, or cluster is required by the static suite.

| ID | Scenario / expected invariant in each supported host |
| --- | --- |
| S01 | Unqualified developer request and direct workflow/role entry: STANDARD + SOLO; same seven stages, no dispatch |
| S02 | QUICK documentation typo: same stages, small check, no full dossier, no invented TDD/coverage gate |
| S03 | STANDARD bugfix: focused reproducer where meaningful, project checks; no automatic role delegation |
| S04 | DEEP architecture change: durable plan/decisions and separate local review pass, still SOLO |
| S05 | Implicit team/parallel recommendation without permission: describe proposal only; no tool call or CLI launch |
| S06 | Explicit HANDOFF: artifact alone sufficient to resume; missing permission remains missing; stale base/branch is detected |
| S07 | Explicit PARALLEL: distinct writer worktrees, owner scopes/integrator; one failed writer prevents false integration success |
| S08 | Reviewer may read owner's worktree; concurrent writers never share it; sequential writer only under authorized topology |
| S09 | Ship readiness only / commit only / PR only / no delivery: exact authorized action set, no implied merge/deploy |
| S10 | Authorized reviewer unavailable: disclose, do not invent agent; local fallback only if consistent with intent |
| S11 | Superpowers absent and each owning plugin installed alone: safe local paths, no phantom skills/tools or copied catalog |
| S12 | Missing native worktree tool, blocked worktree creation, missing jq: manual isolation or explicit stop, never primary edits |
| S13 | Established `.plans`, historical Superpowers/PRP, and new neutral plan: preserve paths; template fields survive handoff |
| S14 | Scheduler/scanner/DevFleet missing: NOT RUN/prerequisite/manual path; no background/scan/dispatch success claims |
| S15 | GitOps/HCP auto-apply merge and destructive operation: impact/rollback recorded; separate fresh runtime permission required |
| S16 | Primary dirty/on feature branch, submodule, detached/external worktree: no destructive restoration or implicit reset |

Each scenario records base/plugin SHA, host/version, tools available, input authorization, selected profile/topology, observed actions and paths, gates with outputs, unexpected behavior, and PASS/FAIL/NOT RUN. Negative cases include unknown profile, conflicting topology instruction, stale handoff and revoked permission. Assertions target actions and artifacts, not exact natural-language wording. Simulated static trace review must be labeled simulated, never counted as a live harness trial.

Baseline collected in this planning session:

- `test_codex_manifests.py`: 3/3 PASS.
- `test_rule_scanners.py`: 2/2 PASS (Bash/jq available).
- Guard: initial plain invocation failed 1 fixture because inherited signing required an unavailable agent socket (57 pass/1 fail); no product change made. Rerun with per-process Git config disabling fixture commit signing: 58/58 PASS.
- Reproduction: `GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=commit.gpgsign GIT_CONFIG_VALUE_0=false bash plugins/git-workflows/hooks/test-guard.sh`. If other Git config environment entries exist, use an isolated fixture configuration rather than overwriting required entries blindly.
- Native CLI discovery, model scenarios, Bash 3.2/macOS, real optional services and consumer gates: NOT RUN. Current permission excludes launching other harnesses. The missing results remain release gates for maintainers, not evidence of failure or success.

## Implementation order and proposed PRs

Recommend **three implementation PRs**, separate from any eventual PR publishing this plan. They are dependent by design, each with scoped regression checks and a documented revert. The plan-only PR is separately authorized; it does not authorize any implementation PR.

1. **Profiles and lifecycle contract** — T01–T03: one normative contract, existing stages/README aligned, proportional planning/research/testing, initial static regression tests. Claims limited to profile/lifecycle work; topology/Ship inconsistencies remain explicitly listed until PR2.
2. **Authorization, topology and delivery alignment** — T04–T08: explicit actor authorization at metadata and procedure boundaries, worktree stop semantics, readiness versus delivery, optional Superpowers dependency removal, adapter and standalone-plugin gates. Bump touched plugin versions atomically. No orchestrator feature is added.
3. **Portable artifacts and compatibility verification** — T09–T11: resource templates, cold resume, capability/consumer/OpenCode checklists, discovery reachability and complete scenario evidence. Final “workflow conformant” release only when all in-scope acceptance gates pass.

Within a PR, tasks are small reviewable commits only after implementation/delivery is authorized. Dependencies are serial under SOLO: T01 → T02 → T03 → T04 → T05 → T06 → T07 → T08 → T09 → T10 → T11. Do not delegate independent work merely because the DAG permits it. If PR scope becomes too broad, split only at a passing policy boundary and keep the advertised conformity level explicit.

## Risk, rollout, rollback and acceptance

| Risk | Mitigation / evidence / rollback trigger |
| --- | --- |
| Contract exists but never loads | Link from real entrypoints and rule index; packaged discovery and direct-entry scenarios; stop release on unreachable guidance |
| Native agent metadata still auto-triggers | Audit descriptions as well as bodies, preserve names/tools/model; direct-role negative scenarios |
| Relaxing generic TDD removes project security gates | Contract precedence and project-policy fixtures; failure blocks release |
| Adding hard cross-plugin dependencies | Plugin-local resource links only; standalone install and missing-provider scenario |
| “Global” overclaims enforcement | Explicit on-demand loading limit, no fake Codex hook, consumer policy follow-up |
| Tests pass while models still misbehave | Separate static, manual and live evidence; never label NOT RUN as pass |
| Auto-dispatch/auto-merge hidden in service | No default service launch; inspect actual capabilities, block unsupported fine-grained permissions |
| Primary checkout or history damaged | No sandbox fallback to primary, no cleanup without authority, no old-plan migration |
| Partial multi-PR rollout | Version/release notes identify remaining conflicts; only full chain receives final conformity claim |

Roll out on disposable/local installs first, then maintainer verification and release/tag, then separately authorized consumers. No state migration is required. Record previous plugin commit/tag and installation state before release. Rollback PR3 → PR2 → PR1 in reverse dependency order with explicit reverts, keeping both manifests aligned and rerunning static/discovery gates. Reinstall previous plugin revision and start a new session to avoid stale caches. Preserve all produced plans and handoffs; older readers may ignore added fields. A documentation/plugin revert does not undo any runtime mutation; those require a separate impact-specific rollback and fresh authority.

Acceptance for this repository: every task has exact files, evidence and exit conditions; existing names resolve in both hosts; one lifecycle and independent profiles/topologies are reachable from active workflows; default is STANDARD + SOLO; no unapproved worker or delivery operation occurs; safety/project gates survive QUICK; artifacts resume without chat; Superpowers absence does not block work; installed links/resources remain contained; Claude-only hooks and Codex limitations are honest. Consumer-only AC12/AC14/AC18 and native OpenCode parity must remain explicitly deferred, not checked off here.

Planning completion means only these three documents have been created in the planning worktree, primary stays clean on `main`, and no implementation/manifests have changed. The first recommended implementation task is T01 (refresh baseline and capture compatibility inventory), followed by T02 (normative contract plus its regression checks).

## Plan-stage validation record

Markdown lint passed for all three documents with only MD013 (line length) disabled for wide tables. Local Markdown links, referenced existing paths versus explicitly planned new paths, whitespace, task dependencies/test/exit/rollback fields, and write scope were checked. At completion of the initial Plan stage, exactly these three untracked plan documents existed in the planning worktree; no tracked/staged implementation or manifest changes, commit or PR had been produced. The subsequent user instruction authorizes publishing these documents as a plan-only PR. Primary checkout was verified clean on `main` at the audited base. A separate local self-review expanded T04 to include the same mandatory/proactive role-trigger conflict in four domain plugin pairs; it did not launch an independent reviewer.

## T01 completion update

Baseline refreshed at `2194b9ad587963dd75a8d6b4fa320b963ee88f9a`; original audit findings and later task scopes are unchanged because only plan documents changed between bases. Manifest/reference tests 3/3 and scanner tests 2/2 passed. Guard passed 58/58 with fixture-only signing disabled after the default invocation reproduced the missing signing-agent failure (57/58). Full commands, environment limits, all plugin versions, skill identities, native entrypoint mappings and content fingerprint are recorded in [the T01 audit evidence](audit.md#t01-baseline-refresh-and-frozen-compatibility-inventory). Native harness checks remain NOT RUN. T01 is complete; stop before T02.

## T02 completion update

T02 implemented locally on `feat/hybrid-ai-workflow-contract`, based on `ad2ec8c` (completed T01). Added the packaged common workflow contract, connected the existing rules skill, aligned README summaries and added structural regression tests. No new skill/command, native adapter, manifest, hook or execution engine was introduced. Five new tests and three existing manifest/reference tests passed; local scenario walkthroughs confirmed the same stages across profiles and no worker requirement for DEEP + SOLO. Markdown lint, local links and diff whitespace checks passed. These are static/local checks, not native discovery or model behavior evidence. See [T02 audit evidence](audit.md#t02-contract-implementation-evidence). Existing conflicting procedure bodies remain queued for T03–T08; do not claim complete workflow conformance. T02 commit/push/PR is now authorized by the subsequent user instruction; T03 and merge remain unauthorized.

## T03 completion update

The sixteen procedure/rule documents named by T03 now use profile-sized research,
planning, verification and review. Lifecycle skills load the one existing contract;
TDD remains a selected technique, project gates stay binding, current working
changes are reviewed before historical targets, and API-regression guidance reuses
existing test/review entrypoints. Added seven structural regression tests to the
existing five contract tests. Twelve workflow tests, three manifest/reference tests
and two scanner tests pass. Markdown (MD013 disabled for wide tables), plugin-local
links, local evidence links and whitespace checks pass. Local scenario walkthroughs
S02–S04 and negative project-policy samples are documented in [T03 evidence](audit.md#t03-profile-sized-procedure-evidence).
These checks are static/local, not live model trials. Native trigger metadata,
remaining Ship defaults, isolation fallback, optional-provider dependency removal,
templates and release metadata remain queued for later tasks. No native adapter, hook or sibling repository changed. At the later authorized
PR boundary, only the version fields in both manifests of development-lifecycle,
agent-toolkit and git-workflows are incremented per the planned release procedure.
Publish T03 only; stop before T04.

## T04 completion update

Corrected ten native/shared role description pairs and added direct-entry authority
guards while preserving native names, tools/model settings and thin wrapper links.
All six lifecycle roles load the existing contract; four domain roles remain
standalone with their checklist suffixes byte-identical. Common agents guidance
gates read-only parallel work as well as writers; security assessment remains
mandatory without a reviewer and credential rotation needs separate authority.
Seven added static tests cover metadata, descriptions, guards, checklist digests,
negative authorization/policy cases and security response. All 19 workflow tests,
3 manifest/reference tests and 2 scanner tests pass. Markdown comparison adds no
file/rule diagnostics relative to the baseline; existing checklist formatting
findings are preserved rather than expanded into unrelated edits. Local links,
whitespace and scope checks pass. [T04 evidence](audit.md#t04-role-authorization-evidence)
records source walkthroughs and missing live/native evidence. No hook, new skill or sibling-repository change. At the authorized PR boundary,
only version fields in the five changed plugins are incremented in both host
manifests. Publish T04 only; stop before T05.
