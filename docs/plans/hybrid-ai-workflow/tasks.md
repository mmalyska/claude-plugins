# Implementation tasks — Hybrid AI Engineering Workflow

Read [plan.md](plan.md), [audit.md](audit.md), and [the specification](../../workflow/specification.md) first. Base: `b43bedd9347fe8b9806895a5e35416beb3250dae`. These are proposed future tasks, not authorization to execute Build or Ship. Current status: T01 COMPLETE at `2194b9ad587963dd75a8d6b4fa320b963ee88f9a`; T02–T11 NOT STARTED. The user authorized T01 and subsequently its commit/push/PR; later product changes and merge remain unauthorized. Execution stays DEEP + SOLO unless the user explicitly changes it; no other harness/subagent/orchestrator may be started under the current instruction.

All file paths are repository-relative. A task's listed files are its allowed proposed scope; do not add unrelated cleanup. Every task must record changed paths, exact commands, exit status, results/limitations, unresolved findings, and next action before checking its box. Native discovery/behavioral trials below are future maintainer gates and require a session in which launching the target CLI is permitted. Static instruction review is not a live model trial.

## Common verification commands

Run from the authorized implementation worktree, never the primary checkout:

```sh
python3 -B -m unittest discover -s tests -p test_codex_manifests.py -v
python3 -B -m unittest discover -s tests -p test_rule_scanners.py -v
# Once introduced by T02:
python3 -B -m unittest discover -s tests -p test_workflow_contract.py -v
# Fixture-only signing override; do not change global/repository Git config:
GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=commit.gpgsign GIT_CONFIG_VALUE_0=false bash plugins/git-workflows/hooks/test-guard.sh
git diff --check
git status --short
```

For future CLI-enabled maintainer verification only:

```sh
python3 -B -m unittest discover -s tests -v
claude plugin validate . --json
# Validate every plugin path listed in .claude-plugin/marketplace.json:
claude plugin validate plugins/development-lifecycle --json
claude plugin validate plugins/git-workflows --json
claude plugin validate plugins/agent-toolkit --json
```

The full suite validates all marketplace plugins through the existing discovery test, but skips unavailable CLIs; record skips as NOT RUN. CLI validation/discovery does not call a model, but still launches another harness process and is excluded from this planning session. Live behavior trials are separately gated. Run Markdown lint with installed tooling and explicit configuration; for wide tables MD013 can be disabled, but do not disable structural checks. Check local links outside fences, optional fragments, and installed-resource containment; external failures need actual HTTP/API evidence, not inferred success.

## T01 — Revalidate baseline and freeze compatibility inventory

- [x] Complete T01.

**PR:** 1. **Dependencies:** implementation instruction; none of the later tasks.

**Files:** read `README.md`, `docs/codex.md`, `docs/workflow/specification.md`, `.claude-plugin/marketplace.json`, all paths enumerated in the audit's manifest and adapter inventories, and existing `tests/test_codex_manifests.py`, `tests/test_host_discovery.py`, `tests/test_rule_scanners.py`, `plugins/git-workflows/hooks/test-guard.sh`. Update only this plan's `plan.md`, `tasks.md`, `audit.md` if the base has drifted. No product edit in T01.

**Change/procedure:** verify `git rev-parse --git-dir` differs from `--git-common-dir`, no superproject confusion, exact branch/worktree, primary clean on `main`, and baseline commit relationship. Read relevant new instructions. Snapshot catalog identities, plugin versions, all existing skill/frontmatter names, command→skill and agent→skill pairs in task evidence. Capture diff/working state before tests. Run existing static/scanner and guard gates; record the signing-fixture workaround only if needed. Do not run native discovery or version commands that launch another harness while prohibited.

**Tests/expected:** 3 manifest tests, 2 scanner tests, 58 guard assertions pass at the audited base; changes since then require explanation. No model calls or real repository commits from fixture tests. Missing native capabilities remain NOT RUN.

**Done:** inventory and reproducible baseline recorded; failures classified as fixture/environment or regression with evidence; affected task scopes refreshed before continuing. Do not proceed past a genuine unexplained baseline failure. Preserve the planning worktree; use a separately authorized implementation branch/worktree for future production edits.

**Evidence:** [T01 baseline and frozen inventory](audit.md#t01-baseline-refresh-and-frozen-compatibility-inventory). Execution branch `feat/hybrid-ai-workflow`; manifest tests 3/3, scanner tests 2/2, guard 58/58 with per-process signing override. Initial guard failure was reproduced and classified as fixture signing, not a product regression. No source drift beyond merged plan documents; T02–T11 scopes unchanged. Only plan.md, tasks.md and audit.md updated; no unresolved baseline regression. Next action: await T02 instruction; the subsequent user instruction authorizes commit/push/PR of T01 evidence only.

**Rollback:** no product change; retain evidence and remove no user data.

## T02 — Establish the single lifecycle/profile/topology contract

- [ ] Complete T02.

**PR:** 1. **Dependencies:** T01.

**Exact files:**

- Create `plugins/development-lifecycle/rules/common/workflow.md`.
- Modify `plugins/development-lifecycle/skills/development-lifecycle-rules/SKILL.md`.
- Modify `plugins/development-lifecycle/README.md`.
- Modify `README.md`.
- Create `tests/test_workflow_contract.py`.

**Change:** encode the specification's seven stages exactly once as authoritative runtime guidance; profiles modify depth, topologies modify actors. Include independent resolution, STANDARD + SOLO defaults, user authority/recorded state, capability-before-use and safety precedence, stage-only stopping, permission boundaries and honest on-demand loading limits. No new Plan/Build skill/command. Register the rule in the existing rule index; README links/summaries replace its incomplete lifecycle. Keep root lifecycle display as a linked summary. Add table-driven structural tests covering missing fields, presence of all contract sections, registry reachability, and invalid/negative sample documents; do not create an artificial workflow engine.

**Tests/expected:** new contract tests and existing manifest/reference checks pass; tests fail against a fixture missing a stage, default or auth boundary. Manual read of QUICK/STANDARD/DEEP confirms same ordered lifecycle; DEEP + SOLO does not request workers. All new rule links resolve within the installed plugin.

**Done:** one discoverable contract owns policy; all seven stages and four topology/fallback rules are clear; no blanket claim that installation intercepts arbitrary prompts. Remaining consumers of competing policy are explicitly queued for T03–T08.

**Rollback:** revert contract, its index references, README summary and tests together.

## T03 — Make planning, research, TDD and reviews proportional

- [ ] Complete T03.

**PR:** 1. **Dependencies:** T02.

**Exact files and minimum edits:**

- `plugins/development-lifecycle/skills/spec/SKILL.md`: load the local contract; profile-sized spec output and Plan transition; replace three-stage diagram; preserve established output paths.
- `plugins/development-lifecycle/skills/architect/SKILL.md`: profile-sized architecture analysis, plan tasks/dependencies/gates; role remains usable locally, not required full design for every edit.
- `plugins/development-lifecycle/skills/ai-regression-testing/SKILL.md`: reuse the existing `test` and review entrypoints for API-regression examples; replace the instruction to create another `bug-check` skill, retain domain checks as optional techniques and use project commands.
- `plugins/development-lifecycle/skills/test/SKILL.md`: retain explicit feature/fix TDD modes; distinguish lifecycle Test from mandatory RED for any change; discover repository unittest checks as well as application markers; no forced coverage package or global percentage; full lifecycle reference.
- `plugins/development-lifecycle/skills/tdd-guide/SKILL.md`: keep RED-GREEN-REFACTOR when TDD is selected; remove all universal 80%/all-types/always-on/eval-run requirements; retain actual project policy; replace absent `tdd-workflow` prerequisite with in-skill guidance or optional discovered provider.
- `plugins/development-lifecycle/skills/review/SKILL.md`: full lifecycle reference and profile-sized review; prefer explicitly selected diff, then working/staged changes and base comparison before unrelated last commit; include docs/config when in scope.
- `plugins/development-lifecycle/skills/code-review/SKILL.md`: use shared review policy/role where suitable, preserve local and PR transport/report; prefer shared AGENTS policy; separate local artifact from external publish; avoid implicit package fetch in validation example.
- `plugins/development-lifecycle/skills/code-reviewer/SKILL.md`: clarify scoped reusable local role; project AGENTS-first policy; preserve checklist, severity and confidence filtering; do not mandate another model or actor.
- `plugins/development-lifecycle/skills/simplify/SKILL.md`: scope current uncommitted changes correctly; replace invented `/plan` diagram with stage reference; no-op is valid; rerun relevant checks after edits and roll back only owned simplification.
- `plugins/development-lifecycle/rules/common/testing.md`: remove universal mandatory TDD, all test types and 80%; project gates plus profile/risk-based selection.
- `plugins/development-lifecycle/rules/common/code-review.md`: project coverage, local security-review fallback, no required phantom specialist, findings first; preserve meaningful security blocking.
- `plugins/development-lifecycle/rules/common/patterns.md`: local-first reuse research; parallel agents only under explicit authorized topology, no implicit clone/adopt operation.
- `plugins/development-lifecycle/rules/common/performance.md`: point planning depth to the contract; retain configured-model and relevant-check guidance.
- `plugins/git-workflows/rules/development-workflow.md`: replace competing research→worktree→plan→TDD→commit pipeline with shared stages and local responsibilities; no mandatory web/registry sweep or five-document dossier; delivery authorized only.
- `plugins/agent-toolkit/skills/search-first/SKILL.md`: proportional local-first uncertainty checks; remove “parallel researcher” as default from diagram; provider/dependency installation is a separate authorized action.
- `plugins/agent-toolkit/skills/verification-loop/SKILL.md`: remove contradictory “80% minimum” example; relevant checks, preserve exit statuses and NOT RUN, current diff selection.
- `tests/test_workflow_contract.py`: add explicit audited-file checks and negative cases for universal planning/TDD/research directives outside examples/history. Match meaningful sections, not every occurrence of “mandatory”.

**Tests/expected:** S02–S04 static/manual instruction traces: QUICK docs change can complete with Markdown checks; STANDARD bugfix still uses a meaningful reproducer; DEEP planning records decisions/gates without workers. Mandatory project coverage/security fixture still blocks when unmet. Manifest/link checks pass; no names deleted and no external tool installed. S09 external review publishing remains unauthorized until T06 aligns final delivery boundaries.

**Done:** no live rule or changed skill forces the same full research/dossier/test process regardless of risk/profile. Stage references no longer contradict the seven-stage contract. Diff-based review includes current work.

**Rollback:** revert T03 with its regression tests; do not weaken repository-specific gates to satisfy tests. Before PR1 delivery, bump versions of changed lifecycle, toolkit and git plugins in both manifests as specified in T08's version procedure; this future PR bookkeeping does not authorize edits now.

## T04 — Gate metadata and direct role/agent entrypoints

- [ ] Complete T04.

**PR:** 2. **Dependencies:** T03.

**Exact files:**

- `plugins/development-lifecycle/rules/common/agents.md`
- `plugins/development-lifecycle/rules/common/security.md`
- `plugins/development-lifecycle/agents/architect.md`
- `plugins/development-lifecycle/agents/build-error-resolver.md`
- `plugins/development-lifecycle/agents/code-reviewer.md`
- `plugins/development-lifecycle/agents/doc-updater.md`
- `plugins/development-lifecycle/agents/docs-lookup.md`
- `plugins/development-lifecycle/agents/tdd-guide.md`
- `plugins/development-lifecycle/skills/architect/SKILL.md`
- `plugins/development-lifecycle/skills/build-error-resolver/SKILL.md`
- `plugins/development-lifecycle/skills/code-reviewer/SKILL.md`
- `plugins/development-lifecycle/skills/doc-updater/SKILL.md`
- `plugins/development-lifecycle/skills/docs-lookup/SKILL.md`
- `plugins/development-lifecycle/skills/tdd-guide/SKILL.md`
- `plugins/backend/agents/database-reviewer.md`
- `plugins/backend/skills/database-reviewer/SKILL.md`
- `plugins/dotnet/agents/csharp-reviewer.md`
- `plugins/dotnet/skills/csharp-reviewer/SKILL.md`
- `plugins/renovate/agents/renovate-auditor.md`
- `plugins/renovate/skills/renovate-auditor/SKILL.md`
- `plugins/devcontainer/agents/devcontainer-auditor.md`
- `plugins/devcontainer/skills/devcontainer-auditor/SKILL.md`
- `tests/test_workflow_contract.py`

**Change:** remove “MUST BE USED” and proactive actor-trigger interpretations in descriptions; describe role applicability without permission to spawn. Keep exact names, tools, models, argument handling, wrapper links and useful procedures. Shared roles load the local contract and run in current session for SOLO. For the four domain role pairs, change only actor-trigger descriptions and the local SOLO/explicit-delegation guard; preserve domain checklists and add no dependency on lifecycle. Common agents rule names topologies and explicit authority; its unconditional parallel sentence becomes gated. Security response remains mandatory assessment/remediation within scope, with a discovered role/local checklist rather than required absent `security-reviewer`; rotation remains a separately authorized sensitive operation.

**Tests/expected:** entrypoint mapping and names unchanged; thin wrappers remain thin. Direct role in S01/S04 creates no worker. Native metadata no longer instructs unconditional spawning/TDD; security issue fixture cannot pass because a reviewer is absent. Conflicting host project-policy fixture is surfaced.

**Done:** descriptions and bodies agree on authority; a native agent's availability is not permission to launch it, and naming a role need not change topology.

**Rollback:** revert paired description/body and tests together; retain actor authorization in downstream tasks until full dependent rollback.

## T05 — Enforce isolation without silent primary fallback

- [ ] Complete T05.

**PR:** 2. **Dependencies:** T04.

**Exact files:**

- `plugins/git-workflows/skills/using-git-worktrees/SKILL.md`
- `plugins/git-workflows/skills/finishing-a-development-branch/SKILL.md`
- `plugins/git-workflows/rules/worktree-workflow.md`
- `plugins/git-workflows/README.md`
- `tests/test_workflow_contract.py`

**Change:** remove sandbox failure → work-in-place fallback from procedure, quick reference and red flags. On blocked creation stop writes and report permission prerequisite; use normal authorized permission escalation when provided by host. Detect existing isolation/submodule first; native tools only when actually exposed, manual git fallback otherwise. Keep `.git/info/exclude` ignoring and safe base verification. Require authorized actor topology before using shared reviewer/sequential writer exceptions; every parallel writer has separate branch/worktree and integrator. Finish must respect selected delivery scope, external worktree ownership and existing primary state, not switch/merge/reset merely to fulfill a postcondition. Local merge requires explicit authorization and no runtime side effect without fresh permission; use ff-only update of base where applicable. Preserve intentional user-approved primary maintenance as a distinct exception, never a sandbox workaround.

**Tests/expected:** S08/S12/S16 manual traces and static negative checks; current guard remains 58/58 on Bash 5+, Bash 3.2 required before release. No edit to `guard-main-checkout.sh`, `inject-worktree-rule.sh` or `hooks.json` is planned; existing guard behavior and fail-open policy remain stable. Missing jq means no enforced hook, never permission to violate procedural rules.

**Done:** permission failure cannot authorize primary edits; parent/read-only/sequential/parallel cases are coherent and cleanup cannot delete someone else's workspace.

**Rollback:** revert procedural changes and tests, leaving hook unchanged; do not delete live worktrees as rollback.

## T06 — Separate readiness, delivery and runtime mutation

- [ ] Complete T06.

**PR:** 2. **Dependencies:** T05.

**Exact files:**

- `plugins/development-lifecycle/skills/ship/SKILL.md`
- `plugins/development-lifecycle/skills/code-review/SKILL.md`
- `plugins/git-workflows/skills/commit/SKILL.md`
- `plugins/git-workflows/skills/pr/SKILL.md`
- `plugins/git-workflows/skills/finishing-a-development-branch/SKILL.md`
- `plugins/git-workflows/rules/git-workflow.md`
- `plugins/agent-toolkit/skills/safety-guard/SKILL.md`
- `tests/test_workflow_contract.py`

**Change:** replace Ship's default three-worker dispatch and bundle commit→push→PR with readiness first and the exact already-authorized action set. Reuse accepted Test/Review evidence; new changes invalidate affected checks. SOLO reviews sequentially; independent review needs authority. No auto inclusion of untracked files, no menu overriding an already chosen action, no broad NO-GO override for mandatory safety gates. Recognize `python3 -m unittest discover -s tests` for this repo. Distinguish commit, push, PR, external review publish, local/remote merge and runtime changes. A request for PR can authorize the necessary branch push, but readiness/commit does not authorize PR or merge. Protect main, stage only task scope, preserve unrelated work, and make force-push/rebase choices obey existing authorization. Replace stale `/prp-pr` and `/prp-commit` examples with existing names without introducing aliases. External PR review report publication must be separately within the user request. GitOps/HCP-triggering merge is a runtime mutation; record impact/rollback and require fresh permission. Safety-guard remains guidance, not a claimed interceptor.

**Tests/expected:** S09/S15 static/manual decision table includes readiness-only, commit-only, create-PR, review-without-publish, explicit publication, refused merge, unauthorized destructive action and preauthorized delivery. Capture zero forbidden actions; do not actually push or mutate runtime in fixture scenarios. Current diff, docs-only gate and NOT RUN test behavior are represented.

**Done:** identical authorization boundaries from every delivery entrypoint, with no surprise commits or repeated permission request for the same authorized action.

**Rollback:** revert complete delivery boundary change with tests; preserve existing artifacts and worktrees.

## T07 — Make toolkit and service procedures obey topology

- [ ] Complete T07.

**PR:** 2. **Dependencies:** T06.

**Exact files:**

- `plugins/agent-toolkit/skills/blueprint/SKILL.md`
- `plugins/agent-toolkit/skills/subagent-driven-development/SKILL.md`
- `plugins/agent-toolkit/skills/team-builder/SKILL.md`
- `plugins/agent-toolkit/skills/autonomous-agent-harness/SKILL.md`
- `plugins/agent-toolkit/skills/continuous-agent-loop/SKILL.md`
- `plugins/agent-toolkit/skills/iterative-retrieval/SKILL.md`
- `plugins/agent-toolkit/skills/rules-distill/SKILL.md`
- `plugins/agent-toolkit/skills/writing-skills/SKILL.md`
- `plugins/development-lifecycle/skills/claude-devfleet/SKILL.md`
- `plugins/agent-toolkit/README.md`
- `tests/test_workflow_contract.py`

**Change:** at each entrypoint check authority before capability; planning/role selection is not team launch. Keep all names. `blueprint` respects existing plan directories/profile depth, no direct-mode bypass of worktree-first, no unconditional memory update or generic multi-agent trigger. `subagent-driven-development` retains authorized sequential worker technique, replaces contradictory diagrams/final-dispatch/TDD wording, offers SOLO role passes honestly, and removes absent `executing-plans` prerequisite. Continuous/autonomous loops preserve explicit limits and no background success claims, but must carry task profile/topology/permissions across iterations. `iterative-retrieval` documents context technique for authorized delegation or local retrieval, not permission to spawn. `rules-distill` gates example worker analysis as well as main text. `writing-skills` adds profile/topology/auth review to authoring guidance. DevFleet's DAG is an optional execution mechanism, not another engineering lifecycle; do not call `plan_project` if it creates auto-dispatch state without safe controls. Inspect actual tool schema; require separate bounded launch and merge authority, no `auto_dispatch=true`/auto-merge default. If service cannot satisfy limits, report incompatibility and use no service. No service implementation, scheduler, worker or connection is created.

**Tests/expected:** S05–S08/S10/S14: available-but-unauthorized tool is never called, missing service produces prerequisite/manual path, bounded failed worker stops dependent integration, default remains SOLO. Review diagrams/examples along with prose. Standalone toolkit works without mandatory lifecycle installation or Superpowers.

**Done:** no procedure or example silently changes actors; service plan approval cannot authorize runtime or a chain of uncontrolled auto-merges. Optional orchestrator pilot prerequisites recorded.

**Rollback:** revert toolkit/service instructions and tests together; do not cancel external jobs unless separately authorized (none are launched by these tasks).

## T08 — Remove hard optional-provider dependency and verify adapters

- [ ] Complete T08.

**PR:** 2; version procedure also applies at each implementation PR boundary. **Dependencies:** T07.

**Exact files:**

- `plugins/development-lifecycle/.claude-plugin/plugin.json`
- `plugins/development-lifecycle/.codex-plugin/plugin.json`
- `plugins/git-workflows/.claude-plugin/plugin.json`
- `plugins/git-workflows/.codex-plugin/plugin.json`
- `plugins/agent-toolkit/.claude-plugin/plugin.json`
- `plugins/agent-toolkit/.codex-plugin/plugin.json`
- `plugins/backend/.claude-plugin/plugin.json`
- `plugins/backend/.codex-plugin/plugin.json`
- `plugins/dotnet/.claude-plugin/plugin.json`
- `plugins/dotnet/.codex-plugin/plugin.json`
- `plugins/renovate/.claude-plugin/plugin.json`
- `plugins/renovate/.codex-plugin/plugin.json`
- `plugins/devcontainer/.claude-plugin/plugin.json`
- `plugins/devcontainer/.codex-plugin/plugin.json`
- `plugins/development-lifecycle/README.md`
- `plugins/git-workflows/README.md`
- `docs/codex.md`
- `tests/test_codex_manifests.py`
- `tests/test_host_discovery.py`
- `tests/test_workflow_contract.py`

**Change:** remove lifecycle's declared Superpowers dependency without uninstalling a user's plugin. Bump each changed plugin's version in both host manifests per existing semver/release policy (including the four domain plugins changed only for T04 triggers); keep identity, skills path, explicit Codex `hooks: []` and Claude hooks unchanged. Do not add dependency/version fields to marketplace entries just for symmetry. Existing command wrappers are inspected, not edited unless descriptions changed in T03–T06 require synchronization; their exact paths are in the audit. Document default, on-demand rules, native versus shared roles, optional providers, true capability matrix and sequential/manual fallbacks. Add regression test that Superpowers is not a hard dependency and no renamed/duplicate host catalog appears. Use the T01 identity inventory to compare entrypoint set and wrapper links, not an empty new snapshot. Prepare native discovery test changes without executing them under current restrictions.

**Tests/expected:** existing static tests pass; changed manifest pairs have equal names/versions and correct discovery. In a future permitted clean CLI environment, install each owning plugin alone and then together using disposable host config, validate all catalog plugins and discover exact old skills. With no Superpowers, all stages have an internal/manual path. No user host settings are modified by tests.

**Done:** no hard external workflow provider, unchanged callable identities, actual optional/native discovery evidence recorded or explicitly NOT RUN and blocking final release. No manifest edit occurs on the current plan-only branch.

**Rollback:** restore prior revision's paired manifests and instructions atomically, reinstall prior version and start new sessions; do not delete optional provider user data.

## T09 — Introduce portable artifact resources through existing skills

- [ ] Complete T09.

**PR:** 3. **Dependencies:** T08.

**Exact files:**

- Create `plugins/development-lifecycle/resources/workflow/plan.md`.
- Create `plugins/development-lifecycle/resources/workflow/tasks.md`.
- Create `plugins/development-lifecycle/resources/workflow/handoff.md`.
- Create `plugins/development-lifecycle/resources/workflow/decision.md`.
- Modify `plugins/development-lifecycle/skills/spec/SKILL.md`.
- Modify `plugins/development-lifecycle/skills/architect/SKILL.md`.
- Modify `plugins/development-lifecycle/skills/architecture-decision-records/SKILL.md`.
- Modify `plugins/development-lifecycle/rules/common/workflow.md`.
- Modify `plugins/agent-toolkit/skills/blueprint/SKILL.md`.
- Modify `tests/test_codex_manifests.py`.
- Modify `tests/test_host_discovery.py`.
- Modify `tests/test_workflow_contract.py`.

**Change:** add fields specified in plan.md and spec §11; task template has exact files/change/dependencies/checks/expected result/done/rollback. Reuse ADR process with small neutral decision resource, not a duplicate architecture skill. Preserve project artifact paths and old formats; only default to `.plans/<slug>/` if there is no existing convention. Store topology authorization scope and missing permissions without implying that a handoff grants authority. Extend link scanning to resource Markdown including links within resources, fragments when present, missing references and install containment. Verify resources survive native install; no links from installed plugin to repository `docs/` or another plugin. Toolkit discovers optional provider instead of cloning templates.

**Tests/expected:** resource links resolve, fixtures cover missing field/broken path/escaping plugin root, old artifact paths remain unchanged. S06/S13 cold resume checks plan/handoff without chat, stale base, unassigned receiver and NOT RUN evidence. QUICK may keep state in session with no artifact; DEEP multi-session plan is durable. Native installed-resource check requires later permitted CLI run.

**Done:** all resources reachable from existing entrypoints and sufficient for an unbriefed session; no duplicate SKILL.md or migration of history. Version bump lifecycle/toolkit pairs under T08 procedure at PR3 boundary.

**Rollback:** revert templates and referring links/tests together; retain created user plans as ordinary Markdown.

## T10 — Publish capability and deferred-consumer strategy

- [ ] Complete T10.

**PR:** 3. **Dependencies:** T09.

**Exact files:**

- Create `docs/workflow/compatibility.md`.
- Modify `docs/codex.md`.
- Modify `README.md`.
- Modify `plugins/development-lifecycle/README.md`.
- Modify `plugins/agent-toolkit/README.md`.
- Modify `plugins/git-workflows/README.md`.

**Change:** consolidate human-readable host matrix and link to the packaged contract, explain loading/enforcement limits and manual artifacts, optional Superpowers and no hidden Codex hooks. Add future OpenCode spike checklist: pinned version, instruction loading, skill discovery, permission mapping/hooks, subagents, worktrees, install consumption, QUICK+SOLO/STANDARD+HANDOFF/REVIEW checks, verified native integration versus manual choice. Do not implement or launch OpenCode. Consumer follow-up checklist explicitly defers home-ops shared AGENTS/CLAUDE/.ai policy and project-skill migration, archive-link validation, domain gates, Cloudflare/HCP impact, secrets and runtime policy; defer dotfiles core/extended profiles, Codex install and chezmoi fresh/reapply matrix. Explain release/tag before consumers depend on changes. Preserve README command names and no-build installation. Record orchestrator pilot prerequisites without providing credentials or turning it into a dependency.

**Tests/expected:** all doc links resolve; AC1 OpenCode is scoped as documented manual contract, not verified native parity; AC12/14/18 clearly marked consumer-only. No changed paths outside this repository and no accidental edits in sibling repositories. Source specification remains unchanged.

**Done:** maintainer can tell what is implemented, tested, missing or deferred; no cross-repository task is marked complete here.

**Rollback:** revert compatibility docs/links as a unit; no consumer migration to reverse.

## T11 — Integrate scenario checks and final acceptance evidence

- [ ] Complete T11.

**PR:** 3. **Dependencies:** T10 and all prior tasks.

**Exact files:**

- Create `tests/fixtures/workflow/scenarios.json`.
- Create `docs/workflow/verification.md`.
- Modify `tests/test_workflow_contract.py`.
- Modify `tests/test_codex_manifests.py`.
- Modify `tests/test_host_discovery.py`.
- Modify `docs/plans/hybrid-ai-workflow/plan.md`.
- Modify `docs/plans/hybrid-ai-workflow/tasks.md`.

**Change:** encode S01–S16 inputs/authority/capabilities, required/forbidden actions and artifact expectations, including missing tools, policy conflict and partial failure. Static tests validate fixture completeness, instruction reachability and negative samples; manual evidence protocol ties real outputs to base/plugin SHA and host/version. No executing shell from JSON, model SDK runner, paid test system, scheduler or orchestrator. Run suitable static tests and local scenario walk-throughs in SOLO, record their limits. In a separately authorized host-enabled session, run all discovery and behavior trials for Claude and Codex on disposable repositories and record transcripts with secret redaction; HANDOFF/PARALLEL/REVIEW trials require explicit actor authorization. If unavailable, leave NOT RUN and do not claim release acceptance. Add direct instruction checks for missing jq and worktree denial; actual Bash 3.2/5+ guard runs are release gates. Validate installed resource links and identities.

**Tests/expected:** full static suite green; unchanged old identity set present; plugin installation/discovery green where executed; S01–S16 evidence accounts for both hosts and distinguishes manual simulation/live trial. Fresh install and reinstall smoke are real, isolated, no user config mutation. Historical Superpowers plan untouched. External source links verified only if changed; no unnecessary network gate on static suite.

**Done:** acceptance matrix in plan.md maps all in-scope requirements to actual evidence, any missing checks explicitly block their release claim; consumer/OpenCode follow-ups remain deferred. Review final diff for duplicated contract, policy loopholes and unrelated paths in a separate local pass. Prepare a reviewable result; commit/push/PR/release only under a later delivery instruction.

**Rollback:** reverse PR3 then PR2 then PR1; run corresponding static/discovery gates after each revert and verify prior names/resources work. A maintainer can reinstall the previously recorded revision without data migration. Do not claim a runtime rollback from reverting documentation.

## Completion record for this Plan stage

The audit, architecture decisions, traceability, tasks and test strategy have been prepared in SOLO. This is not evidence that any implementation task above is complete. Current artifacts are limited to `plan.md`, `tasks.md`, `audit.md`; primary checkout remains clean on `main`. T01 is now complete; the next task is T02, which requires a subsequent instruction. No functional policy edit has been made.
