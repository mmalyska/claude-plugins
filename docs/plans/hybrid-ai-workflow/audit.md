# Repository-grounded audit — Hybrid AI Engineering Workflow

## Scope, method and limits

Audited `mmalyska/claude-plugins` at `b43bedd9347fe8b9806895a5e35416beb3250dae` on 2026-10-27, against [the specification](../../workflow/specification.md). Execution: DEEP + SOLO, Plan stage only. No subagent, second harness, orchestrator, production edit or manifest edit was used. Read source files, searched tracked Markdown/manifests/scripts across the repository, and inspected all implementation owners below. This is a repository audit, not external product-documentation research or a factual revalidation of historical sibling-repository SHAs.

Searches covered lifecycle/stage names, planning/research/TDD requirements, `mandatory`, `PROACTIVELY`, `MUST BE USED`, `parallel`, `subagent`, agent teams, authorization, worktree, hook differences, Superpowers, and external provider names. Source paths in tables are exact; line evidence is pinned to the audited SHA. Inventory includes unchanged related files to distinguish procedure, thin adapter, hook, test, history and domain example. Application concepts such as React component lifecycle, ADR record statuses, asynchronous parallel database calls, Renovate automerge policy and devcontainer lifecycle hooks are not competing engineering lifecycles.

No tracked root `AGENTS.md` or `CLAUDE.md` exists at the audited base. There is no tracked active `.plans` index. Historical plans use `docs/superpowers/`; current runtime instructions disagree on new artifact locations. See the planning-convention decision in [plan.md](plan.md). No history is rewritten.

## Findings and minimum remediation

Finding IDs are stable for task/evidence references. “Conflict” describes current text; qualified fallback clauses that already comply are retained, not treated as nonexistent.

| ID | Evidence at audited base | Conflict / implication | Minimal remediation / task |
| --- | --- | --- | --- |
| F01 | Lifecycle README says `spec → implementation and test → review → simplify → ship`; spec/test/review/ship skills have shorter diagrams; simplify mentions `/plan` | Multiple incomplete definitions and an apparent command with no native entrypoint; Plan/Build obscured | One packaged contract, stage links and accurate existing entrypoints; T02–T03, T06 |
| F02 | Git development workflow: mandatory external Research & Reuse, PRD/architecture/system_design/tech_doc/task_list, TDD and Commit & Push sequence | Full research/planning/TDD irrespective of profile, competing process | Proportional local-first guidance and authorized delivery; T03 |
| F03 | Common testing rule: all test types, minimum 80%, mandatory TDD; TDD role repeats 80%/Always; verification-loop example still says 80% | Conflicts with profile/risk/project-policy approach; corrected prose elsewhere does not remove examples | Keep explicit TDD technique, project gates and appropriate checks; T03 |
| F04 | Common patterns says “Use parallel agents”; common agents ends with unqualified “Parallelize independent read-only work”; security/code-review require `security-reviewer` | Actor authorization not reliably reached; phantom specialist requirement | Named topology authorization then capability, local role/checklist fallback; T03–T04 |
| F05 | Native/shared `code-reviewer` and C# reviewer descriptions say MUST BE USED; TDD, backend, renovate and devcontainer roles say PROACTIVELY | Metadata can trigger delegation before guarded body loads | Preserve identity and native metadata fields; correct triggers and role-vs-actor semantics; T04 |
| F06 | Ship opening/Phase 2 say dispatch three reviews; Proceed is commit+push+PR; final diagram skips stages | Local fallback and later authorization gate exist but conflict with headline/default behavior | Readiness only by default, explicit action set, SOLO local passes, no blanket override; T06 |
| F07 | using-git-worktrees Step 1b and quick-reference allow working in place after permission error | Direct conflict with worktree-first and explicit session constraint | Stop writes/report permission prerequisite; never downgrade isolation silently; T05 |
| F08 | Subagent-driven skill starts “fresh subagent per task”; diagram defaults to workers or absent `executing-plans`; prompt requires TDD | Authorized fallback exists, but dominant path changes topology and technique implicitly | Guard all paths/diagrams; keep optional technique and sequential role passes; T07 |
| F09 | Blueprint writes `plans/`, describes multi-agent trigger, direct mode edit-in-place, automatic register/memory | Artifact/path and isolation conflicts; local authorization fallback already exists | Established path first, profile-sensitive planning, no worktree bypass or automatic memory; T07, T09 |
| F10 | DevFleet example turns ordinary “Build a REST API” into mission DAG, auto-dispatch and auto-merge; `plan_project` may pre-enable dispatch | Approval of a plan can create uncontrolled side effects even before root mission launch | Authority before service calls; verify actual safe controls, fail explicitly if unavailable; T07 |
| F11 | Lifecycle Claude manifest declares `superpowers@claude-plugins-official`; README calls external plugins optional; Codex manifest lacks dependency | Declared hard dependency contradicts documentation and host parity | Remove dependency during future implementation, keep optional usage and stable names; T08 |
| F12 | Historical worktree plan header requires `superpowers:subagent-driven-development` or `superpowers:executing-plans` | Historical dependency cannot be copied into new plan requirements | Preserve historical text; neutral new plan and optional provider policy; T09–T10 |
| F13 | review/simplify select last commit before staged diff and omit unstaged scope; ship repeats last-commit security diff | Can review unrelated commit while missing current work, especially an uncommitted Plan session | Explicit scope/current diff/base-aware selection; preserve evidence; T03, T06 |
| F14 | review, code-review, code-reviewer and ship repeat severity, coverage and quality policy with differing block/warn rules | Overlapping policy; not four independent mandatory reviewers | One normative gate contract, retain transport/role/checklists and scope distinctions; T03, T06 |
| F15 | Code-review PR mode publishes externally; git commit/pr examples use stale `/prp-*`; PR skill suggests force-with-lease on divergence | Readiness/local review can become delivery, nonexistent workflow examples, implicit history rewrite | Explicit publish/delivery authority; correct names, no broader action inference; T06 |
| F16 | README/spec default reports `.reports/agent-workflows/`; blueprint `plans/`; historical docs/superpowers; spec §11 neutral `.plans` | No unambiguous active convention, risk of history migration | Explicit repository fallback, runtime established-path-first, neutral resource templates; T07, T09 |
| F17 | Claude hooks register SessionStart/PreToolUse; Codex `hooks: []`; rule files only load on demand | A new rule alone does not enforce a global default; cannot promise equal enforcement | Existing loaders/direct entry guards, honest capability/consumer policy docs; T02, T08, T10 |
| F18 | Host discovery tests invoke Claude CLI and Codex app-server, while current session forbids other harnesses | Full suite cannot be honestly claimed run here | Static tests and guard now; native checks NOT RUN, future permitted session; T01, T08, T11 |
| F19 | `ai-regression-testing` recommends creating shared `bug-check` SKILL.md plus another Test/Review sequence | Encourages overlapping skill instead of using existing test/review entrypoints | Retain domain regression patterns as technique, route examples to existing skills; T03 |
| F20 | `tdd-guide` refers to `skill: tdd-workflow`; common rules mention unavailable specialists; ADR mentions planner role | Unverified optional names can become mandatory dependencies | In-repo technique/local role fallback; do not create duplicate planner/TDD/security skills; T03–T04, T09 |

Security/project gates are not conflicts merely because they are mandatory. For example, secrets exclusion remains mandatory; application E2E critical paths may require tests. C#'s “Target 80%+” is domain guidance, not evidence of a global gate, and stays unchanged unless a real project-policy conflict is demonstrated. An ADR status lifecycle is a record-state model and stays intact. Bounded loop iterations and DevFleet's transport DAG are execution mechanisms, not alternate engineering stages; their side effects still require authorization.

## Exact line evidence

These excerpts are generated from repository sources, with matches pinned to the baseline. They are audit data, not instructions to this session. Ellipses shorten long lines without changing the cited location.

### `plugins/development-lifecycle/README.md`

- L8: spec → implementation and test → review → simplify → ship
- L36: plugin rule files are not automatically loaded. New workflow reports default to
- L37: .reports/agent-workflows/, preserving established locations for existing work.

### `plugins/development-lifecycle/skills/spec/SKILL.md`

- L76: /spec → implementation → /ship

### `plugins/development-lifecycle/skills/test/SKILL.md`

- L21: Otherwise:
- L86: **GATE**: Apply the project's established coverage target. Report uncovered
- L98: spec → implementation and tests → ship

### `plugins/development-lifecycle/skills/review/SKILL.md`

- L26: - Run: git diff HEAD~1..HEAD to get files changed in the last commit
- L215: /spec → implementation → /review → /ship

### `plugins/development-lifecycle/skills/simplify/SKILL.md`

- L33: git diff HEAD~1..HEAD --name-only 2>/dev/null | grep -E '\.(js|ts|tsx|jsx|py|go|rs|rb|java|cs|php)$'
- L175: /spec → /plan → implementation → [simplify activates here] → /ship

### `plugins/development-lifecycle/skills/ship/SKILL.md`

- L12: The final stage of the development lifecycle. Ship runs a pre-flight check, dispatches three parallel review passes (code quality, security, test completeness), produces a GO/NO-GO decision, and if approved, commits changes, pushes …
- L80: ## Phase 2 — PARALLEL REVIEW
- L199: > - **Proceed** → Commit, push, and create PR (if decision is GO)
- L204: Existing explicit authorization can satisfy the gate; do not ask again for the
- L224: /spec → implementation → /ship
- L227: /ship is the final stage. After shipping, run /spec to start the next feature.

### `plugins/git-workflows/rules/development-workflow.md`

- L14: 0. **Research & Reuse** _(mandatory before any new implementation)_
- L29: - Generate planning docs before coding: PRD, architecture, system_design, tech_doc, task_list
- L33: 3. **TDD Approach**
- L45: 5. **Commit & Push**

### `plugins/development-lifecycle/rules/common/testing.md`

- L3: ## Minimum Test Coverage: 80%
- L5: Test Types (ALL required):
- L12: MANDATORY workflow:
- L18: 6. Verify coverage (80%+)
- L29: - **tdd-guide** - Use PROACTIVELY for new features, enforces write-tests-first

### `plugins/development-lifecycle/rules/common/agents.md`

- L14: Delegate only when authorized by the current session. Otherwise perform focused
- L24: Parallelize independent read-only work when supported. Concurrent writers need

### `plugins/development-lifecycle/rules/common/patterns.md`

- L7: 2. Use parallel agents to evaluate options:

### `plugins/development-lifecycle/rules/common/security.md`

- L20: - Rotate any secrets that may have been exposed
- L26: 2. Use **security-reviewer** agent
- L28: 4. Rotate any exposed secrets

### `plugins/development-lifecycle/rules/common/code-review.md`

- L37: - [ ] Test coverage meets 80% minimum
- L41: **STOP and use security-reviewer agent when:**
- L67: | **security-reviewer** | Security vulnerabilities, OWASP Top 10 |
- L80: 5. Verify coverage >= 80%

### `plugins/development-lifecycle/agents/code-reviewer.md`

- L3: description: Expert code review specialist. Proactively reviews code for quality, security, and maintainability. Use immediately after writing or modifying code. MUST BE USED for all code changes.

### `plugins/development-lifecycle/agents/tdd-guide.md`

- L3: description: Test-Driven Development specialist enforcing write-tests-first methodology. Use PROACTIVELY when writing new features, fixing bugs, or refactoring code. Ensures 80%+ test coverage.

### `plugins/development-lifecycle/skills/tdd-guide/SKILL.md`

- L3: description: "Test-Driven Development specialist enforcing write-tests-first methodology. Use PROACTIVELY when writing new features, fixing bugs, or refactoring code. Ensures 80%+ test coverage."
- L14: - Ensure 80%+ test coverage
- L39: # Required: 80%+ branches, functions, lines, statements
- L46: | **Unit** | Individual functions in isolation | Always |
- L47: | **Integration** | API endpoints, database operations | Always |
- L78: - [ ] Coverage is 80%+
- L80: For detailed mocking patterns and framework-specific examples, see skill: tdd-workflow.

### `plugins/agent-toolkit/skills/verification-loop/SKILL.md`

- L66: # Target: 80% minimum

### `plugins/git-workflows/skills/using-git-worktrees/SKILL.md`

- L120: **Sandbox fallback:** If git worktree add fails with a permission error, tell the user the sandbox blocked worktree creation and you're working in the current directory instead. Then run setup and baseline tests in place.
- L170: | Permission error on create | Work in place |

### `plugins/agent-toolkit/skills/blueprint/SKILL.md`

- L27: 3. **Draft** — Writes a self-contained Markdown plan file to plans/. Every step includes a context brief, task list, verification commands, and exit criteria — so a fresh agent can execute any step without reading prior steps.
- L31: Blueprint detects git/gh availability automatically. With git + GitHub CLI, it generates full branch/PR/CI workflow plans. Without them, it switches to direct mode (edit-in-place, no branches).
- L60: - **Branch/PR/CI workflow** — Built into every step. Degrades gracefully to direct mode when git/gh is absent.
- L72: For adversarial review, use an available authorized subagent; otherwise perform

### `plugins/agent-toolkit/skills/subagent-driven-development/SKILL.md`

- L8: Execute plan by dispatching fresh subagent per task, with two-stage review after each: spec compliance review first, then code quality review.
- L18: Check whether delegation is exposed and authorized. In Claude use the available
- L34: "executing-plans" [shape=box];
- L42: "Stay in this session?" -> "executing-plans" [label="no - parallel session"];
- L122: - TDD requirement: write failing test first, then implement

### `plugins/development-lifecycle/skills/claude-devfleet/SKILL.md`

- L27: settings for auto-dispatch/auto-merge and ensure the requested scope authorizes
- L48: M1 completes → auto-merge → auto-dispatch M2 (depends_on M1)
- L50: M2 completes → auto-merge
- L63: | create_mission(project_id, title, prompt, depends_on?, auto_dispatch?) | Add a mission. depends_on is a list of mission ID strings (e.g., ["abc-123"]). Set auto_dispatch=true to auto-start when deps are met. |
- L77: 1. **Plan**: Call plan_project(prompt="...") → returns project_id + list of missions with depends_on chains and auto_dispatch=true.
- L79: 3. **Dispatch**: Call dispatch_mission(mission_id=<first_mission_id>) on the root mission (empty depends_on). Remaining missions auto-dispatch as their dependencies complete (because plan_project sets auto_dispatch=true on them).
- L85: DevFleet runs up to 3 concurrent agents by default (configurable via DEVFLEET_MAX_AGENTS). When all slots are full, missions with auto_dispatch=true queue in the mission watcher and dispatch automatically as slots free up. Check get…
- L93: 3. Remaining missions auto-dispatch as dependencies resolve (they have auto_dispatch=true).
- L101: 2. create_mission(project_id=project_id, title="...", prompt="...", auto_dispatch=true) for the first (root) mission → capture root_mission_id.
- L102: create_mission(project_id=project_id, title="...", prompt="...", auto_dispatch=true, depends_on=["<root_mission_id>"]) for each subsequent task.
- L112: 5. create_mission(project_id=project_id, title="Review", prompt="...", depends_on=[impl_mission_id], auto_dispatch=true) — auto-starts since the dependency is already met.
- L116: - Always confirm the plan with the user before dispatching, unless they said to go ahead.
- L121: - Each agent runs in an isolated git worktree and auto-merges on completion. If a merge conflict occurs, the changes remain on the agent's worktree branch for manual resolution.
- L122: - When manually creating missions, always set auto_dispatch=true if you want them to trigger automatically when dependencies complete. Without this flag, missions stay in draft status.

### `plugins/development-lifecycle/.claude-plugin/plugin.json`

- L13: "superpowers@claude-plugins-official"

### `docs/superpowers/plans/2026-09-17-worktree-first-git-workflow.md`

- L3: > **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (- [ ]) syntax for tracking.

### `plugins/development-lifecycle/skills/code-review/SKILL.md`

- L105: 1. **Project rules** — Read applicable AGENTS.md (Codex) or CLAUDE.md (Claude), project documentation, and contributing guidelines
- L236: ### Phase 7 — PUBLISH

### `plugins/git-workflows/skills/commit/SKILL.md`

- L99: - /prp-pr            → create a pull request
- L109: | /prp-commit | Stages all, auto-generates message |
- L110: | /prp-commit staged | Commits only what's already staged |
- L111: | /prp-commit *.ts | Stages all TypeScript files, commits |
- L112: | /prp-commit except tests | Stages everything except test files |
- L113: | /prp-commit the database migration | Finds DB migration files from status, stages them |
- L114: | /prp-commit only new files | Stages untracked files only |

### `plugins/git-workflows/skills/pr/SKILL.md`

- L34: | Clean working directory | No uncommitted changes | Warn: "You have uncommitted changes. Commit or stash first. Use /prp-commit to commit." |
- L185: - **Force push needed**: If remote has diverged and rebase was done, use git push --force-with-lease (never --force).

### `plugins/development-lifecycle/skills/ai-regression-testing/SKILL.md`

- L200: Store this as skills/bug-check/SKILL.md inside a shared plugin, or in the
- L212: ## Step 1: Automated Tests (mandatory, cannot skip)

### `docs/codex.md`

- L55: | Rules | On-demand rule skills; no automatic Codex injection |
- L56: | Hooks | Claude hooks remain host-specific; Codex manifests explicitly use hooks: [] |
- L63: New reports default to .reports/agent-workflows/; resuming work preserves its
- L77: Bash and jq. Native discovery tests run when the corresponding Claude/Codex CLI

## Implementation inventory and file-level disposition

Every current file of the three workflow-owning plugins is listed below (Markdown, JSON and shell), including supporting techniques that do not need changes. Hidden manifests are included. Future paths are listed only in tasks.md, not misrepresented as existing files. File-level task links identify minimum edits; an adapter listed for inspection preserves its link/metadata unless its description actually conflicts. The current manifest contents remain untouched by this planning task.

### `plugins/development-lifecycle`

| Existing file | Responsibility / disposition | Task |
| --- | --- | --- |
| `plugins/development-lifecycle/.claude-plugin/plugin.json` | Claude identity/version; lifecycle dependency removal only in implementation | T08 |
| `plugins/development-lifecycle/.codex-plugin/plugin.json` | Codex discovery; same skill tree; hooks explicitly disabled; future paired version only | T08 |
| `plugins/development-lifecycle/README.md` | Discovery and behavior summary; align only relevant lifecycle/topology/capability claims | T02,T08,T10 |
| `plugins/development-lifecycle/agents/architect.md` | Thin native Claude role adapter; preserve tools/model/name, gate triggering descriptions | T04 |
| `plugins/development-lifecycle/agents/build-error-resolver.md` | Thin native Claude role adapter; preserve tools/model/name, gate triggering descriptions | T04 |
| `plugins/development-lifecycle/agents/code-reviewer.md` | Thin native Claude role adapter; preserve tools/model/name, gate triggering descriptions | T04 |
| `plugins/development-lifecycle/agents/doc-updater.md` | Thin native Claude role adapter; preserve tools/model/name, gate triggering descriptions | T04 |
| `plugins/development-lifecycle/agents/docs-lookup.md` | Thin native Claude role adapter; preserve tools/model/name, gate triggering descriptions | T04 |
| `plugins/development-lifecycle/agents/tdd-guide.md` | Thin native Claude role adapter; preserve tools/model/name, gate triggering descriptions | T04 |
| `plugins/development-lifecycle/commands/aside.md` | Thin Claude command; preserve basename/input and shared-skill link; inspect description parity | Inspect / retain |
| `plugins/development-lifecycle/commands/code-review.md` | Thin Claude command; preserve basename/input and shared-skill link; inspect description parity | Inspect / retain |
| `plugins/development-lifecycle/commands/learn-eval.md` | Thin Claude command; preserve basename/input and shared-skill link; inspect description parity | Inspect / retain |
| `plugins/development-lifecycle/commands/review.md` | Thin Claude command; preserve basename/input and shared-skill link; inspect description parity | Inspect / retain |
| `plugins/development-lifecycle/commands/ship.md` | Thin Claude command; preserve basename/input and shared-skill link; inspect description parity | Inspect / retain |
| `plugins/development-lifecycle/commands/skill-create.md` | Thin Claude command; preserve basename/input and shared-skill link; inspect description parity | Inspect / retain |
| `plugins/development-lifecycle/commands/spec.md` | Thin Claude command; preserve basename/input and shared-skill link; inspect description parity | Inspect / retain |
| `plugins/development-lifecycle/commands/test.md` | Thin Claude command; preserve basename/input and shared-skill link; inspect description parity | Inspect / retain |
| `plugins/development-lifecycle/commands/update-codemaps.md` | Thin Claude command; preserve basename/input and shared-skill link; inspect description parity | Inspect / retain |
| `plugins/development-lifecycle/commands/update-docs.md` | Thin Claude command; preserve basename/input and shared-skill link; inspect description parity | Inspect / retain |
| `plugins/development-lifecycle/rules/common/agents.md` | On-demand rule/policy; apply listed targeted edits, otherwise retain domain guidance | T04 |
| `plugins/development-lifecycle/rules/common/code-review.md` | On-demand rule/policy; apply listed targeted edits, otherwise retain domain guidance | T03 |
| `plugins/development-lifecycle/rules/common/coding-style.md` | On-demand rule/policy; apply listed targeted edits, otherwise retain domain guidance | Inspect / retain |
| `plugins/development-lifecycle/rules/common/hooks.md` | On-demand rule/policy; apply listed targeted edits, otherwise retain domain guidance | Inspect / retain |
| `plugins/development-lifecycle/rules/common/patterns.md` | On-demand rule/policy; apply listed targeted edits, otherwise retain domain guidance | T03 |
| `plugins/development-lifecycle/rules/common/performance.md` | On-demand rule/policy; apply listed targeted edits, otherwise retain domain guidance | T03 |
| `plugins/development-lifecycle/rules/common/security.md` | On-demand rule/policy; apply listed targeted edits, otherwise retain domain guidance | T04 |
| `plugins/development-lifecycle/rules/common/testing.md` | On-demand rule/policy; apply listed targeted edits, otherwise retain domain guidance | T03 |
| `plugins/development-lifecycle/skills/ai-regression-testing/SKILL.md` | Shared procedure/technique; change only as assigned, otherwise retain existing scoped functionality | T03 |
| `plugins/development-lifecycle/skills/architect/SKILL.md` | Shared procedure/technique; change only as assigned, otherwise retain existing scoped functionality | T03,T04,T09 |
| `plugins/development-lifecycle/skills/architecture-decision-records/SKILL.md` | Shared procedure/technique; change only as assigned, otherwise retain existing scoped functionality | T09 |
| `plugins/development-lifecycle/skills/aside/SKILL.md` | Shared procedure/technique; change only as assigned, otherwise retain existing scoped functionality | Inspect / retain |
| `plugins/development-lifecycle/skills/build-error-resolver/SKILL.md` | Shared procedure/technique; change only as assigned, otherwise retain existing scoped functionality | T04 |
| `plugins/development-lifecycle/skills/claude-devfleet/SKILL.md` | Shared procedure/technique; change only as assigned, otherwise retain existing scoped functionality | T07 |
| `plugins/development-lifecycle/skills/code-review/SKILL.md` | Shared procedure/technique; change only as assigned, otherwise retain existing scoped functionality | T03,T06 |
| `plugins/development-lifecycle/skills/code-reviewer/SKILL.md` | Shared procedure/technique; change only as assigned, otherwise retain existing scoped functionality | T03,T04 |
| `plugins/development-lifecycle/skills/development-lifecycle-rules/SKILL.md` | Shared procedure/technique; change only as assigned, otherwise retain existing scoped functionality | T02 |
| `plugins/development-lifecycle/skills/doc-updater/SKILL.md` | Shared procedure/technique; change only as assigned, otherwise retain existing scoped functionality | T04 |
| `plugins/development-lifecycle/skills/docs-lookup/SKILL.md` | Shared procedure/technique; change only as assigned, otherwise retain existing scoped functionality | T04 |
| `plugins/development-lifecycle/skills/e2e-testing/SKILL.md` | Shared procedure/technique; change only as assigned, otherwise retain existing scoped functionality | Inspect / retain |
| `plugins/development-lifecycle/skills/learn-eval/SKILL.md` | Shared procedure/technique; change only as assigned, otherwise retain existing scoped functionality | Inspect / retain |
| `plugins/development-lifecycle/skills/review/SKILL.md` | Shared procedure/technique; change only as assigned, otherwise retain existing scoped functionality | T03 |
| `plugins/development-lifecycle/skills/ship/SKILL.md` | Shared procedure/technique; change only as assigned, otherwise retain existing scoped functionality | T06 |
| `plugins/development-lifecycle/skills/simplify/SKILL.md` | Shared procedure/technique; change only as assigned, otherwise retain existing scoped functionality | T03 |
| `plugins/development-lifecycle/skills/skill-create/SKILL.md` | Shared procedure/technique; change only as assigned, otherwise retain existing scoped functionality | Inspect / retain |
| `plugins/development-lifecycle/skills/spec/SKILL.md` | Shared procedure/technique; change only as assigned, otherwise retain existing scoped functionality | T03,T09 |
| `plugins/development-lifecycle/skills/tdd-guide/SKILL.md` | Shared procedure/technique; change only as assigned, otherwise retain existing scoped functionality | T03,T04 |
| `plugins/development-lifecycle/skills/test/SKILL.md` | Shared procedure/technique; change only as assigned, otherwise retain existing scoped functionality | T03 |
| `plugins/development-lifecycle/skills/update-codemaps/SKILL.md` | Shared procedure/technique; change only as assigned, otherwise retain existing scoped functionality | Inspect / retain |
| `plugins/development-lifecycle/skills/update-docs/SKILL.md` | Shared procedure/technique; change only as assigned, otherwise retain existing scoped functionality | Inspect / retain |

### `plugins/git-workflows`

| Existing file | Responsibility / disposition | Task |
| --- | --- | --- |
| `plugins/git-workflows/.claude-plugin/plugin.json` | Claude identity/version; lifecycle dependency removal only in implementation | T08 |
| `plugins/git-workflows/.codex-plugin/plugin.json` | Codex discovery; same skill tree; hooks explicitly disabled; future paired version only | T08 |
| `plugins/git-workflows/README.md` | Discovery and behavior summary; align only relevant lifecycle/topology/capability claims | T05,T08,T10 |
| `plugins/git-workflows/commands/commit.md` | Thin Claude command; preserve basename/input and shared-skill link; inspect description parity | Inspect / retain |
| `plugins/git-workflows/commands/pr.md` | Thin Claude command; preserve basename/input and shared-skill link; inspect description parity | Inspect / retain |
| `plugins/git-workflows/hooks/guard-main-checkout.sh` | Existing Claude worktree enforcement/injection or disposable-fixture tests; no hook rewrite planned | Inspect / retain |
| `plugins/git-workflows/hooks/hooks.json` | Existing Claude worktree enforcement/injection or disposable-fixture tests; no hook rewrite planned | Inspect / retain |
| `plugins/git-workflows/hooks/inject-worktree-rule.sh` | Existing Claude worktree enforcement/injection or disposable-fixture tests; no hook rewrite planned | Inspect / retain |
| `plugins/git-workflows/hooks/test-guard.sh` | Existing Claude worktree enforcement/injection or disposable-fixture tests; no hook rewrite planned | T01 |
| `plugins/git-workflows/hooks/test-linux-container.sh` | Existing Claude worktree enforcement/injection or disposable-fixture tests; no hook rewrite planned | Inspect / retain |
| `plugins/git-workflows/rules/development-workflow.md` | On-demand rule/policy; apply listed targeted edits, otherwise retain domain guidance | T03 |
| `plugins/git-workflows/rules/git-workflow.md` | On-demand rule/policy; apply listed targeted edits, otherwise retain domain guidance | T06 |
| `plugins/git-workflows/rules/worktree-workflow.md` | On-demand rule/policy; apply listed targeted edits, otherwise retain domain guidance | T05 |
| `plugins/git-workflows/skills/commit/SKILL.md` | Shared procedure/technique; change only as assigned, otherwise retain existing scoped functionality | T06 |
| `plugins/git-workflows/skills/finishing-a-development-branch/SKILL.md` | Shared procedure/technique; change only as assigned, otherwise retain existing scoped functionality | T05,T06 |
| `plugins/git-workflows/skills/git-workflows-rules/SKILL.md` | Shared procedure/technique; change only as assigned, otherwise retain existing scoped functionality | Inspect / retain |
| `plugins/git-workflows/skills/pr/SKILL.md` | Shared procedure/technique; change only as assigned, otherwise retain existing scoped functionality | T06 |
| `plugins/git-workflows/skills/using-git-worktrees/SKILL.md` | Shared procedure/technique; change only as assigned, otherwise retain existing scoped functionality | T05 |

### `plugins/agent-toolkit`

| Existing file | Responsibility / disposition | Task |
| --- | --- | --- |
| `plugins/agent-toolkit/.claude-plugin/plugin.json` | Claude identity/version; lifecycle dependency removal only in implementation | T08 |
| `plugins/agent-toolkit/.codex-plugin/plugin.json` | Codex discovery; same skill tree; hooks explicitly disabled; future paired version only | T08 |
| `plugins/agent-toolkit/README.md` | Discovery and behavior summary; align only relevant lifecycle/topology/capability claims | T07,T10 |
| `plugins/agent-toolkit/skills/autonomous-agent-harness/SKILL.md` | Shared procedure/technique; change only as assigned, otherwise retain existing scoped functionality | T07 |
| `plugins/agent-toolkit/skills/blueprint/SKILL.md` | Shared procedure/technique; change only as assigned, otherwise retain existing scoped functionality | T07,T09 |
| `plugins/agent-toolkit/skills/context-budget/SKILL.md` | Shared procedure/technique; change only as assigned, otherwise retain existing scoped functionality | Inspect / retain |
| `plugins/agent-toolkit/skills/continuous-agent-loop/SKILL.md` | Shared procedure/technique; change only as assigned, otherwise retain existing scoped functionality | T07 |
| `plugins/agent-toolkit/skills/eval-harness/SKILL.md` | Shared procedure/technique; change only as assigned, otherwise retain existing scoped functionality | Inspect / retain |
| `plugins/agent-toolkit/skills/iterative-retrieval/SKILL.md` | Shared procedure/technique; change only as assigned, otherwise retain existing scoped functionality | T07 |
| `plugins/agent-toolkit/skills/rules-distill/SKILL.md` | Shared procedure/technique; change only as assigned, otherwise retain existing scoped functionality | T07 |
| `plugins/agent-toolkit/skills/rules-distill/scripts/scan-rules.sh` | Existing optional scanner script; unchanged, keep scanner regression tests | Inspect / retain |
| `plugins/agent-toolkit/skills/rules-distill/scripts/scan-skills.sh` | Existing optional scanner script; unchanged, keep scanner regression tests | Inspect / retain |
| `plugins/agent-toolkit/skills/safety-guard/SKILL.md` | Shared procedure/technique; change only as assigned, otherwise retain existing scoped functionality | T06 |
| `plugins/agent-toolkit/skills/search-first/SKILL.md` | Shared procedure/technique; change only as assigned, otherwise retain existing scoped functionality | T03 |
| `plugins/agent-toolkit/skills/subagent-driven-development/SKILL.md` | Shared procedure/technique; change only as assigned, otherwise retain existing scoped functionality | T07 |
| `plugins/agent-toolkit/skills/team-builder/SKILL.md` | Shared procedure/technique; change only as assigned, otherwise retain existing scoped functionality | T07 |
| `plugins/agent-toolkit/skills/verification-loop/SKILL.md` | Shared procedure/technique; change only as assigned, otherwise retain existing scoped functionality | T03 |
| `plugins/agent-toolkit/skills/workspace-surface-audit/SKILL.md` | Shared procedure/technique; change only as assigned, otherwise retain existing scoped functionality | Inspect / retain |
| `plugins/agent-toolkit/skills/writing-skills/SKILL.md` | Shared procedure/technique; change only as assigned, otherwise retain existing scoped functionality | T07 |

### Repository packaging, tests, specification and history

| Existing file | Role / disposition |
| --- | --- |
| `README.md` | Complete lifecycle display and collection install/discovery summary; link canonical guidance |
| `.claude-plugin/marketplace.json` | Twelve plugin identities/sources; preserve; no new adapter catalog or version field needed |
| `docs/codex.md` | Shared behavior, namespaced discovery, capability limits, optional CLI checks; update guidance |
| `docs/workflow/specification.md` | Source of requirements, read-only for implementation planning |
| `docs/superpowers/plans/2026-09-17-worktree-first-git-workflow.md` | Historical dated plan with mandatory provider header; preserve as history |
| `docs/superpowers/specs/2026-09-17-worktree-first-git-workflow-design.md` | Historical guard design and behavioral probes; preserve |
| `tests/test_codex_manifests.py` | Identity/version, no codex-skills copies, skill metadata, plugin-local links and wrapper reachability |
| `tests/test_host_discovery.py` | Claude validation and Codex native discovery using temporary config; launches CLIs; not run now |
| `tests/test_rule_scanners.py` | Both host skill directories, overrides, rules source files, empty/missing/error fixtures |

### Other plugin surfaces inspected and retained

These files implement domain review, host installation or rule discovery, not a separate workflow. T04 makes a narrow triggering/actor-authorization correction in four domain role pairs, including C# MUST BE USED metadata; preserve all domain checklists and native identity/tool/model fields. Other listed files are inspected and retained. Their identities belong to T01/T08 compatibility checks; no domain rewrite is planned.

- `plugins/backend/README.md` — domain role/rule/host installation context; inspect compatibility, no planned policy copy.
- `plugins/backend/skills/database-reviewer/SKILL.md` — T04: narrow trigger/authorization correction, preserve domain body; T08: paired manifest version update.
- `plugins/dotnet/README.md` — domain role/rule/host installation context; inspect compatibility, no planned policy copy.
- `plugins/dotnet/rules/csharp/testing.md` — domain role/rule/host installation context; inspect compatibility, no planned policy copy.
- `plugins/dotnet/skills/csharp-reviewer/SKILL.md` — T04: narrow trigger/authorization correction, preserve domain body; T08: paired manifest version update.
- `plugins/dotnet/skills/csharp-testing/SKILL.md` — domain role/rule/host installation context; inspect compatibility, no planned policy copy.
- `plugins/frontend/README.md` — domain role/rule/host installation context; inspect compatibility, no planned policy copy.
- `plugins/frontend/rules/typescript/security.md` — domain role/rule/host installation context; inspect compatibility, no planned policy copy.
- `plugins/frontend/rules/typescript/testing.md` — domain role/rule/host installation context; inspect compatibility, no planned policy copy.
- `plugins/security/README.md` — domain role/rule/host installation context; inspect compatibility, no planned policy copy.
- `plugins/renovate/README.md` — domain role/rule/host installation context; inspect compatibility, no planned policy copy.
- `plugins/renovate/skills/renovate-auditor/SKILL.md` — T04: narrow trigger/authorization correction, preserve domain body; T08: paired manifest version update.
- `plugins/devcontainer/README.md` — domain role/rule/host installation context; inspect compatibility, no planned policy copy.
- `plugins/devcontainer/skills/devcontainer-auditor/SKILL.md` — T04: narrow trigger/authorization correction, preserve domain body; T08: paired manifest version update.
- `plugins/personal-essentials/README.md` — domain role/rule/host installation context; inspect compatibility, no planned policy copy.
- `plugins/personal-essentials/skills/personal-setup/SKILL.md` — domain role/rule/host installation context; inspect compatibility, no planned policy copy.
- `plugins/backend/agents/database-reviewer.md` — T04: correct proactive/mandatory actor trigger; preserve native metadata and shared-role link.
- `plugins/devcontainer/agents/devcontainer-auditor.md` — T04: correct proactive/mandatory actor trigger; preserve native metadata and shared-role link.
- `plugins/dotnet/agents/csharp-reviewer.md` — T04: correct proactive/mandatory actor trigger; preserve native metadata and shared-role link.
- `plugins/renovate/agents/renovate-auditor.md` — T04: correct proactive/mandatory actor trigger; preserve native metadata and shared-role link.

Untracked build outputs and local caches are not implementation sources. No tracked scripts/build pipeline defines an additional workflow engine. Do not manufacture one to satisfy the Plan stage.

## Overlap decisions

- Lifecycle is owned by development-lifecycle; git owns isolation/delivery mechanics; toolkit owns planning/context/optional execution techniques. They consume one conceptual contract without copying whole skills or violating install boundaries.
- `review`, `code-review`, `code-reviewer`, and Ship review overlap but serve stage/transport/role/readiness purposes. Reuse policy and keep callable names; no forced rename or extra reviewer agent.
- `test`, `tdd-guide`, E2E patterns, API regression patterns, eval-harness and verification-loop are techniques/evidence, not five mandatory lifecycle stages. Keep useful domain examples; remove hard global technique requirements and phantom providers.
- `architect`, blueprint and ADR handle design/Plan/decisions. No new planner skill or duplicate plan lifecycle is needed.
- Team-builder, subagent-driven-development, iterative-retrieval, loops and DevFleet are optional execution aids. Authorization changes topology, not their availability or an ordinary planning request.
- Codex/Claude share body files. Native tool/model fields stay in native adapters; Codex has no automatic plugin-rule injection or Markdown agent registration. Equal contract does not mean equal hook enforcement.

## Baseline and next action

Static manifest/reference tests 3/3 and scanner tests 2/2 passed. Guard fixture suite passed 58/58 with process-only commit signing disabled; initial default signing failed one fixture due to missing signing-agent socket. No real repository commit was created. Native discovery, live behavior, macOS/Bash 3.2, external services and consumer environments were not executed. See plan.md for exact commands and limits.

Audit completed without production changes. Recommended implementation starts with T01 and then T02; all other tasks remain unchecked. Any future implementation must revalidate evidence against its new base rather than assume these line numbers still identify the same clauses.

Domain metadata evidence: `plugins/dotnet/agents/csharp-reviewer.md:3` and `plugins/dotnet/skills/csharp-reviewer/SKILL.md:3` require MUST BE USED for C# projects. Backend database reviewer and renovate/devcontainer auditor native/shared descriptions use PROACTIVELY at line 3 (renovate/devcontainer native adapters at line 2). These are the same metadata-level issue as F05, not an exemption from global SOLO.

## T01 baseline refresh and frozen compatibility inventory

T01 completed on 2026-10-27 in DEEP + SOLO. Product implementation has not started; T02 is not authorized by the T01 request. This section records the current baseline rather than replacing historical evidence above.

- Current base and primary `main`: `2194b9ad587963dd75a8d6b4fa320b963ee88f9a` (merged plan PR #8).
- Original audit base: `b43bedd9347fe8b9806895a5e35416beb3250dae`, verified ancestor of current base.
- Drift: exactly the three added plan documents; `plugins/`, `tests/`, marketplace, root README, `docs/codex.md` and source specification are byte-identical across bases. Original conflict evidence and T02–T11 file scopes remain valid.
- Execution branch: `feat/hybrid-ai-workflow`.
- Execution worktree: `/workspaces/claude-plugins/.worktrees/feat/hybrid-ai-workflow`.
- Git dir: `/workspaces/claude-plugins/.git/worktrees/hybrid-ai-workflow`; common dir: `/workspaces/claude-plugins/.git`. They differ; superproject path is empty.
- Primary was clean on `main` before/after setup; implementation worktree had no staged, unstaged or untracked changes before tests. `.worktrees/` is locally excluded. Planning worktree remains preserved.
- No tracked `AGENTS.md` or `CLAUDE.md` was introduced. Existing repo instructions were inspected; no new instruction drift.
- Environment: Git 2.56.0; Python 3.15.0; Bash 5.3.20 (Linux x86_64); jq 1.8.2. These version checks invoked no AI harness.

### Commands, results and limitations

| Command / inspection | Exit | Observed result |
| --- | --- | --- |
| `git fetch origin main` then `git merge --ff-only origin/main` in clean primary | 0 | Fast-forward from original base to merged-plan base; no local edits |
| `git worktree add -b feat/hybrid-ai-workflow .worktrees/feat/hybrid-ai-workflow main` | 0 | New isolated worktree at current base |
| `git rev-parse --absolute-git-dir`, `git rev-parse --path-format=absolute --git-common-dir`, `git rev-parse --show-superproject-working-tree` | 0 | Linked worktree, no submodule confusion |
| `git merge-base --is-ancestor b43bedd9347fe8b9806895a5e35416beb3250dae HEAD` | 0 | Audit baseline is ancestor |
| `git diff b43bedd9347fe8b9806895a5e35416beb3250dae..HEAD --name-status` | 0 | Only plan.md, tasks.md, audit.md added |
| `python3 -B -m unittest discover -s tests -p test_codex_manifests.py -v` | 0 | 3 tests PASS: identity/version/frontmatter, contained references/wrappers, both-host install instructions |
| `python3 -B -m unittest discover -s tests -p test_rule_scanners.py -v` | 0 | 2 tests PASS: both host dirs/overrides; rules file/directory and empty/missing paths |
| `bash plugins/git-workflows/hooks/test-guard.sh` | 1 | 57 pass / 1 fail; fixture seed commits could not sign (missing agent socket), so submodule fixture was invalid |
| Same guard command with child-process-only `commit.gpgsign=false` | 0 | 58 pass / 0 fail; fixture/environment failure, no product regression |
| `git diff --check`, pre-test `git status --porcelain` | 0 | No whitespace errors, clean before evidence edits |

The successful guard rerun used this exact wrapper. It preserves any existing process Git config entries and changes no repository/global Git configuration:

```python
import os, subprocess
settings = dict(os.environ)
count = int(settings.get('GIT_CONFIG_COUNT', '0'))
settings.update({
    'GIT_CONFIG_COUNT': str(count + 1),
    f'GIT_CONFIG_KEY_{count}': 'commit.gpgsign',
    f'GIT_CONFIG_VALUE_{count}': 'false',
})
result = subprocess.run(
    ['bash', 'plugins/git-workflows/hooks/test-guard.sh'],
    env=settings, text=True, capture_output=True,
)
print(result.stdout)
raise SystemExit(result.returncode)
```

Native CLI discovery/validation and harness version calls remain NOT RUN because other harness launches are prohibited. The full unittest suite was not invoked: `test_host_discovery.py` starts Claude/Codex processes. Live scenarios, optional services, Bash 3.2/macOS and consumer environments are also NOT RUN. No native installation, enabled user configuration, live hooks, scheduling, delegation or runtime capability is inferred from repository declarations. No model calls or real repository commits were performed; test commits exist only in disposable fixtures.

### Catalog identities and paired versions

Snapshot is repository-declared discovery at the base above, not a claim of a live user installation. Marketplace identity: `mmalyska-claude-plugins`. Native metadata and full file bytes are reproducible with `git show <base>:<path>`.

| Catalog identity | Catalog source | Claude version | Codex version | Codex skill discovery | Codex hooks | Declared Claude dependency |
| --- | --- | --- | --- | --- | --- | --- |
| `personal-essentials` | `./plugins/personal-essentials` | `1.0.1` | `1.0.1` | `./skills/` | `[]` | `none` |
| `git-workflows` | `./plugins/git-workflows` | `1.2.1` | `1.2.1` | `./skills/` | `[]` | `none` |
| `development-lifecycle` | `./plugins/development-lifecycle` | `1.1.1` | `1.1.1` | `./skills/` | `[]` | `superpowers@claude-plugins-official` |
| `dotnet` | `./plugins/dotnet` | `1.0.1` | `1.0.1` | `./skills/` | `[]` | `none` |
| `frontend` | `./plugins/frontend` | `1.0.1` | `1.0.1` | `./skills/` | `[]` | `none` |
| `backend` | `./plugins/backend` | `1.0.1` | `1.0.1` | `./skills/` | `[]` | `none` |
| `devops` | `./plugins/devops` | `1.0.1` | `1.0.1` | `./skills/` | `[]` | `none` |
| `security` | `./plugins/security` | `1.0.1` | `1.0.1` | `./skills/` | `[]` | `none` |
| `agent-toolkit` | `./plugins/agent-toolkit` | `1.0.1` | `1.0.1` | `./skills/` | `[]` | `none` |
| `renovate` | `./plugins/renovate` | `0.1.1` | `0.1.1` | `./skills/` | `[]` | `none` |
| `devcontainer` | `./plugins/devcontainer` | `0.1.1` | `0.1.1` | `./skills/` | `[]` | `none` |
| `android` | `./plugins/android` | `0.1.0` | `0.1.0` | `absent` | `[]` | `none` |

For every row, exact manifest paths are `<catalog source>/.claude-plugin/plugin.json` and `<catalog source>/.codex-plugin/plugin.json`. Identity and version equality was verified, with Codex hooks empty throughout. Android intentionally has no skills. Superpowers is still a declared lifecycle Claude dependency: F11 remains open, removal belongs to T08. All seven plugins potentially changed by later policy work have their current versions captured, including backend/dotnet/renovate/devcontainer.

### All existing shared skill identities

| Installed identity | Shared source and frontmatter name |
| --- | --- |
| `$personal-essentials:personal-setup` | `plugins/personal-essentials/skills/personal-setup/SKILL.md`; `name: personal-setup` |
| `$git-workflows:commit` | `plugins/git-workflows/skills/commit/SKILL.md`; `name: commit` |
| `$git-workflows:finishing-a-development-branch` | `plugins/git-workflows/skills/finishing-a-development-branch/SKILL.md`; `name: finishing-a-development-branch` |
| `$git-workflows:git-workflows-rules` | `plugins/git-workflows/skills/git-workflows-rules/SKILL.md`; `name: git-workflows-rules` |
| `$git-workflows:pr` | `plugins/git-workflows/skills/pr/SKILL.md`; `name: pr` |
| `$git-workflows:using-git-worktrees` | `plugins/git-workflows/skills/using-git-worktrees/SKILL.md`; `name: using-git-worktrees` |
| `$development-lifecycle:ai-regression-testing` | `plugins/development-lifecycle/skills/ai-regression-testing/SKILL.md`; `name: ai-regression-testing` |
| `$development-lifecycle:architect` | `plugins/development-lifecycle/skills/architect/SKILL.md`; `name: architect` |
| `$development-lifecycle:architecture-decision-records` | `plugins/development-lifecycle/skills/architecture-decision-records/SKILL.md`; `name: architecture-decision-records` |
| `$development-lifecycle:aside` | `plugins/development-lifecycle/skills/aside/SKILL.md`; `name: aside` |
| `$development-lifecycle:build-error-resolver` | `plugins/development-lifecycle/skills/build-error-resolver/SKILL.md`; `name: build-error-resolver` |
| `$development-lifecycle:claude-devfleet` | `plugins/development-lifecycle/skills/claude-devfleet/SKILL.md`; `name: claude-devfleet` |
| `$development-lifecycle:code-review` | `plugins/development-lifecycle/skills/code-review/SKILL.md`; `name: code-review` |
| `$development-lifecycle:code-reviewer` | `plugins/development-lifecycle/skills/code-reviewer/SKILL.md`; `name: code-reviewer` |
| `$development-lifecycle:development-lifecycle-rules` | `plugins/development-lifecycle/skills/development-lifecycle-rules/SKILL.md`; `name: development-lifecycle-rules` |
| `$development-lifecycle:doc-updater` | `plugins/development-lifecycle/skills/doc-updater/SKILL.md`; `name: doc-updater` |
| `$development-lifecycle:docs-lookup` | `plugins/development-lifecycle/skills/docs-lookup/SKILL.md`; `name: docs-lookup` |
| `$development-lifecycle:e2e-testing` | `plugins/development-lifecycle/skills/e2e-testing/SKILL.md`; `name: e2e-testing` |
| `$development-lifecycle:learn-eval` | `plugins/development-lifecycle/skills/learn-eval/SKILL.md`; `name: learn-eval` |
| `$development-lifecycle:review` | `plugins/development-lifecycle/skills/review/SKILL.md`; `name: review` |
| `$development-lifecycle:ship` | `plugins/development-lifecycle/skills/ship/SKILL.md`; `name: ship` |
| `$development-lifecycle:simplify` | `plugins/development-lifecycle/skills/simplify/SKILL.md`; `name: simplify` |
| `$development-lifecycle:skill-create` | `plugins/development-lifecycle/skills/skill-create/SKILL.md`; `name: skill-create` |
| `$development-lifecycle:spec` | `plugins/development-lifecycle/skills/spec/SKILL.md`; `name: spec` |
| `$development-lifecycle:tdd-guide` | `plugins/development-lifecycle/skills/tdd-guide/SKILL.md`; `name: tdd-guide` |
| `$development-lifecycle:test` | `plugins/development-lifecycle/skills/test/SKILL.md`; `name: test` |
| `$development-lifecycle:update-codemaps` | `plugins/development-lifecycle/skills/update-codemaps/SKILL.md`; `name: update-codemaps` |
| `$development-lifecycle:update-docs` | `plugins/development-lifecycle/skills/update-docs/SKILL.md`; `name: update-docs` |
| `$dotnet:csharp-reviewer` | `plugins/dotnet/skills/csharp-reviewer/SKILL.md`; `name: csharp-reviewer` |
| `$dotnet:csharp-testing` | `plugins/dotnet/skills/csharp-testing/SKILL.md`; `name: csharp-testing` |
| `$dotnet:dotnet-patterns` | `plugins/dotnet/skills/dotnet-patterns/SKILL.md`; `name: dotnet-patterns` |
| `$dotnet:dotnet-rules` | `plugins/dotnet/skills/dotnet-rules/SKILL.md`; `name: dotnet-rules` |
| `$frontend:design-system` | `plugins/frontend/skills/design-system/SKILL.md`; `name: design-system` |
| `$frontend:frontend-patterns` | `plugins/frontend/skills/frontend-patterns/SKILL.md`; `name: frontend-patterns` |
| `$frontend:frontend-rules` | `plugins/frontend/skills/frontend-rules/SKILL.md`; `name: frontend-rules` |
| `$frontend:nextjs-turbopack` | `plugins/frontend/skills/nextjs-turbopack/SKILL.md`; `name: nextjs-turbopack` |
| `$backend:api-design` | `plugins/backend/skills/api-design/SKILL.md`; `name: api-design` |
| `$backend:backend-patterns` | `plugins/backend/skills/backend-patterns/SKILL.md`; `name: backend-patterns` |
| `$backend:database-migrations` | `plugins/backend/skills/database-migrations/SKILL.md`; `name: database-migrations` |
| `$backend:database-reviewer` | `plugins/backend/skills/database-reviewer/SKILL.md`; `name: database-reviewer` |
| `$backend:hexagonal-architecture` | `plugins/backend/skills/hexagonal-architecture/SKILL.md`; `name: hexagonal-architecture` |
| `$backend:mcp-server-patterns` | `plugins/backend/skills/mcp-server-patterns/SKILL.md`; `name: mcp-server-patterns` |
| `$backend:nestjs-patterns` | `plugins/backend/skills/nestjs-patterns/SKILL.md`; `name: nestjs-patterns` |
| `$backend:postgres-patterns` | `plugins/backend/skills/postgres-patterns/SKILL.md`; `name: postgres-patterns` |
| `$devops:deployment-patterns` | `plugins/devops/skills/deployment-patterns/SKILL.md`; `name: deployment-patterns` |
| `$devops:docker-patterns` | `plugins/devops/skills/docker-patterns/SKILL.md`; `name: docker-patterns` |
| `$security:security-review` | `plugins/security/skills/security-review/SKILL.md`; `name: security-review` |
| `$security:security-scan` | `plugins/security/skills/security-scan/SKILL.md`; `name: security-scan` |
| `$agent-toolkit:autonomous-agent-harness` | `plugins/agent-toolkit/skills/autonomous-agent-harness/SKILL.md`; `name: autonomous-agent-harness` |
| `$agent-toolkit:blueprint` | `plugins/agent-toolkit/skills/blueprint/SKILL.md`; `name: blueprint` |
| `$agent-toolkit:context-budget` | `plugins/agent-toolkit/skills/context-budget/SKILL.md`; `name: context-budget` |
| `$agent-toolkit:continuous-agent-loop` | `plugins/agent-toolkit/skills/continuous-agent-loop/SKILL.md`; `name: continuous-agent-loop` |
| `$agent-toolkit:eval-harness` | `plugins/agent-toolkit/skills/eval-harness/SKILL.md`; `name: eval-harness` |
| `$agent-toolkit:iterative-retrieval` | `plugins/agent-toolkit/skills/iterative-retrieval/SKILL.md`; `name: iterative-retrieval` |
| `$agent-toolkit:rules-distill` | `plugins/agent-toolkit/skills/rules-distill/SKILL.md`; `name: rules-distill` |
| `$agent-toolkit:safety-guard` | `plugins/agent-toolkit/skills/safety-guard/SKILL.md`; `name: safety-guard` |
| `$agent-toolkit:search-first` | `plugins/agent-toolkit/skills/search-first/SKILL.md`; `name: search-first` |
| `$agent-toolkit:subagent-driven-development` | `plugins/agent-toolkit/skills/subagent-driven-development/SKILL.md`; `name: subagent-driven-development` |
| `$agent-toolkit:team-builder` | `plugins/agent-toolkit/skills/team-builder/SKILL.md`; `name: team-builder` |
| `$agent-toolkit:verification-loop` | `plugins/agent-toolkit/skills/verification-loop/SKILL.md`; `name: verification-loop` |
| `$agent-toolkit:workspace-surface-audit` | `plugins/agent-toolkit/skills/workspace-surface-audit/SKILL.md`; `name: workspace-surface-audit` |
| `$agent-toolkit:writing-skills` | `plugins/agent-toolkit/skills/writing-skills/SKILL.md`; `name: writing-skills` |
| `$renovate:renovate-auditor` | `plugins/renovate/skills/renovate-auditor/SKILL.md`; `name: renovate-auditor` |
| `$renovate:renovate-automerge-rules` | `plugins/renovate/skills/renovate-automerge-rules/SKILL.md`; `name: renovate-automerge-rules` |
| `$renovate:renovate-custom-regex-managers` | `plugins/renovate/skills/renovate-custom-regex-managers/SKILL.md`; `name: renovate-custom-regex-managers` |
| `$renovate:renovate-extending-presets` | `plugins/renovate/skills/renovate-extending-presets/SKILL.md`; `name: renovate-extending-presets` |
| `$devcontainer:devcontainer-auditor` | `plugins/devcontainer/skills/devcontainer-auditor/SKILL.md`; `name: devcontainer-auditor` |
| `$devcontainer:devcontainer-ghcr-image-pipeline` | `plugins/devcontainer/skills/devcontainer-ghcr-image-pipeline/SKILL.md`; `name: devcontainer-ghcr-image-pipeline` |
| `$devcontainer:devcontainer-renovate-digest-pinning` | `plugins/devcontainer/skills/devcontainer-renovate-digest-pinning/SKILL.md`; `name: devcontainer-renovate-digest-pinning` |
| `$devcontainer:devcontainer-secrets-injection` | `plugins/devcontainer/skills/devcontainer-secrets-injection/SKILL.md`; `name: devcontainer-secrets-injection` |

Frozen count: 70 shared skills with 70 unique frontmatter names; every name matches its directory. No new names or duplicate host skill catalogs were introduced.

### Native command and agent to shared-skill pairs

Native identity is the adapter basename; an explicit `name` is shown when present. Tools/model stay host-specific. The listed mappings plus the pinned base freeze the exact compatibility surface, including descriptive metadata not duplicated here.

| Native adapter | Shared target | Native name / tools / model |
| --- | --- | --- |
| `plugins/personal-essentials/commands/personal-setup.md` | `plugins/personal-essentials/skills/personal-setup/SKILL.md` | `implicit basename; no tools/model override` |
| `plugins/git-workflows/commands/commit.md` | `plugins/git-workflows/skills/commit/SKILL.md` | `implicit basename; no tools/model override` |
| `plugins/git-workflows/commands/pr.md` | `plugins/git-workflows/skills/pr/SKILL.md` | `implicit basename; no tools/model override` |
| `plugins/development-lifecycle/commands/aside.md` | `plugins/development-lifecycle/skills/aside/SKILL.md` | `implicit basename; no tools/model override` |
| `plugins/development-lifecycle/commands/code-review.md` | `plugins/development-lifecycle/skills/code-review/SKILL.md` | `implicit basename; no tools/model override` |
| `plugins/development-lifecycle/commands/learn-eval.md` | `plugins/development-lifecycle/skills/learn-eval/SKILL.md` | `implicit basename; no tools/model override` |
| `plugins/development-lifecycle/commands/review.md` | `plugins/development-lifecycle/skills/review/SKILL.md` | `implicit basename; no tools/model override` |
| `plugins/development-lifecycle/commands/ship.md` | `plugins/development-lifecycle/skills/ship/SKILL.md` | `implicit basename; no tools/model override` |
| `plugins/development-lifecycle/commands/skill-create.md` | `plugins/development-lifecycle/skills/skill-create/SKILL.md` | `name=skill-create` |
| `plugins/development-lifecycle/commands/spec.md` | `plugins/development-lifecycle/skills/spec/SKILL.md` | `implicit basename; no tools/model override` |
| `plugins/development-lifecycle/commands/test.md` | `plugins/development-lifecycle/skills/test/SKILL.md` | `implicit basename; no tools/model override` |
| `plugins/development-lifecycle/commands/update-codemaps.md` | `plugins/development-lifecycle/skills/update-codemaps/SKILL.md` | `implicit basename; no tools/model override` |
| `plugins/development-lifecycle/commands/update-docs.md` | `plugins/development-lifecycle/skills/update-docs/SKILL.md` | `implicit basename; no tools/model override` |
| `plugins/development-lifecycle/agents/architect.md` | `plugins/development-lifecycle/skills/architect/SKILL.md` | `name=architect; tools=["Read", "Grep", "Glob"]; model=opus` |
| `plugins/development-lifecycle/agents/build-error-resolver.md` | `plugins/development-lifecycle/skills/build-error-resolver/SKILL.md` | `name=build-error-resolver; tools=["Read", "Write", "Edit", "Bash", "Grep", "Glob"]; model=sonnet` |
| `plugins/development-lifecycle/agents/code-reviewer.md` | `plugins/development-lifecycle/skills/code-reviewer/SKILL.md` | `name=code-reviewer; tools=["Read", "Grep", "Glob", "Bash"]; model=sonnet` |
| `plugins/development-lifecycle/agents/doc-updater.md` | `plugins/development-lifecycle/skills/doc-updater/SKILL.md` | `name=doc-updater; tools=["Read", "Write", "Edit", "Bash", "Grep", "Glob"]; model=haiku` |
| `plugins/development-lifecycle/agents/docs-lookup.md` | `plugins/development-lifecycle/skills/docs-lookup/SKILL.md` | `name=docs-lookup; tools=["Read", "Grep", "Glob", "WebSearch", "WebFetch", "mcp__context7__resolve-library-id", "mcp__context7__query-docs"]; model=sonnet` |
| `plugins/development-lifecycle/agents/tdd-guide.md` | `plugins/development-lifecycle/skills/tdd-guide/SKILL.md` | `name=tdd-guide; tools=["Read", "Write", "Edit", "Bash", "Grep"]; model=sonnet` |
| `plugins/dotnet/agents/csharp-reviewer.md` | `plugins/dotnet/skills/csharp-reviewer/SKILL.md` | `name=csharp-reviewer; tools=["Read", "Grep", "Glob", "Bash"]; model=sonnet` |
| `plugins/backend/agents/database-reviewer.md` | `plugins/backend/skills/database-reviewer/SKILL.md` | `name=database-reviewer; tools=["Read", "Write", "Edit", "Bash", "Grep", "Glob"]; model=sonnet` |
| `plugins/renovate/agents/renovate-auditor.md` | `plugins/renovate/skills/renovate-auditor/SKILL.md` | `implicit basename; no tools/model override` |
| `plugins/devcontainer/agents/devcontainer-auditor.md` | `plugins/devcontainer/skills/devcontainer-auditor/SKILL.md` | `implicit basename; no tools/model override` |

Frozen count: 13 commands and 10 native agents; every shared target exists and each thin adapter links to it.

### Declaration and content fingerprint

To make later compatibility comparisons unambiguous, the digest below covers sorted repository-relative paths and SHA-256 content digests of every tracked file under `plugins/`, `tests/`, plus `.claude-plugin/marketplace.json`. It is evidence only, not a new runtime format or test implementation.

- Files: 169. Combined SHA-256: `1b7303fe02a0986a84c3b97c8a9748fd58e2e89633cb21f16558072985563a35`.
- Digest recipe: for each sorted tracked path, concatenate `path + NUL + sha256(file bytes).hexdigest() + newline`; SHA-256 the UTF-8 concatenation.
- Read-only inspection included the source specification, plan, current README/Codex guidance, existing test modules, and the audited manifest/adapter/rule/skill/hook paths. Source drift comparison is empty; historical line evidence stays valid.
- Remaining findings F01–F20 are unchanged and deliberately unresolved by T01. No task scope or dependency adjustment is needed.
- Changed paths for T01 are only this plan's `plan.md`, `tasks.md`, `audit.md`; no plugin, manifest or test was edited.
- Next action: stop after T01. T02 (normative contract plus initial regression checks) needs a subsequent instruction; the subsequent user instruction authorizes commit/push/PR of these T01 documents only; merge and release remain unauthorized.

## T02 contract implementation evidence

T02 completed locally on `feat/hybrid-ai-workflow-contract`, in worktree `/workspaces/claude-plugins/.worktrees/feat/hybrid-ai-workflow-contract`, based on `ad2ec8c` (T01). The fetched `origin/main` remains `2194b9ad587963dd75a8d6b4fa320b963ee88f9a`; T01 PR #9 is not yet included there. A separate worktree preserves its branch and PR unchanged. Execution remains DEEP + SOLO with no subagent, second harness or orchestrator.

### Changed paths and intent

- `plugins/development-lifecycle/rules/common/workflow.md`: single packaged contract for stages, profiles, selection/defaults, actor topology/authority, worktree and safety, state/evidence, stage/delivery boundaries and loading/capability limits.
- `plugins/development-lifecycle/skills/development-lifecycle-rules/SKILL.md`: read the contract first, then task-relevant rules; generic technique conflicts cannot override it or mandatory project policy.
- `plugins/development-lifecycle/README.md`: linked full lifecycle, default and authorization summary; explicit incomplete-rollout notice for T03–T08.
- `README.md`: linked existing lifecycle summary and default; normalized the touched table separator for Markdown lint.
- `tests/test_workflow_contract.py`: document-structure and critical declaration checks, invalid sample coverage, existing rule index containment/reachability and README links. This is test-only Markdown inspection, not a resolver/workflow runtime.
- `docs/plans/hybrid-ai-workflow/{plan,tasks,audit}.md`: current status, actual evidence and next action; historical T01 identity snapshot is preserved.

No manifest, native command/agent adapter, hook, existing stage skill body or sibling repository changed. Version changes belong to the later authorized implementation PR boundary. T02 creates no new Plan/Build skill or command. F01 is addressed in the README/contract only; existing stage diagrams and other F01–F20 consumers remain pending T03–T08, so no complete conformity claim is made.

### Commands and results

| Command / check | Exit | Evidence |
| --- | --- | --- |
| `python3 -B -m unittest discover -s tests -p test_workflow_contract.py -v` | 0 | 5 tests PASS; 12 malformed/missing-value samples and each of 9 missing sections are rejected |
| `python3 -B -m unittest discover -s tests -p test_codex_manifests.py -v` | 0 | 3 tests PASS; identities, contained rule/skill references, native wrapper links and install instructions preserved |
| Markdown lint on changed Markdown, with MD013 disabled for wide tables | 0 | Structural formatting PASS |
| Local link/fragment inspection and `git diff --check` | 0 | No broken local targets or whitespace errors |
| Separate local scope review | 0 | Five T02 implementation paths plus three evidence documents only; no manifest or hook edits; primary clean on main |

Negative samples remove/reorder lifecycle stages, remove profile/topology defaults, replace SOLO with PARALLEL, remove a profile column/stage/topology row, empty a profile cell, weaken explicit actor authorization, remove the stage stop boundary or empty the document. Section-deletion samples check every required contract section. Tests validate shape and critical declarations, not natural-language policy obedience or an invented runtime implementation.

### Separate local scenario walkthrough

- Unqualified request: the default block supplies STANDARD and SOLO independently; current explicit user instructions and accepted same-task state take precedence. Unknown/conflicting input requires clarification before dependent action.
- QUICK documentation typo: session goal/checklist, smallest edit, meaningful Markdown check, focused self-review, no-op Simplify, readiness only; the seven stages remain conceptually present without requiring TDD/full planning dossiers.
- STANDARD bug fix: focused requirements and plan, implementation with relevant reproducer/project gates, full self-review, scoped simplification and readiness; no default dispatch.
- DEEP + SOLO architecture work: durable tasks/decisions/rollback, layered checks and a separate deliberate local review pass. The contract explicitly prohibits using DEEP or tool availability as permission to add an actor.
- Missing requested reviewer capability: disclose the limitation, no second CLI or fake REVIEW; SOLO fallback only when consistent with user intent.
- Plan/task-only instruction: stop at that boundary; neither seven-stage wording nor readiness authorizes later tasks, commit/push/PR or runtime mutation.

These are source-based walkthroughs by the same agent, not live model trials or independent review. Native discovery/validation and full unittest discovery remain NOT RUN under the no-other-harness constraint; scanners and guard retain the unchanged passing T01 baseline and were not rerun because no related files changed. Remaining uncertainty is model compliance and integration with the still-unmodified consumers. T03 is the next task and requires a new instruction; T02 commit/push/PR is now authorized by a subsequent instruction; merge remains unauthorized. T01 PR #9 is now merged at `d0c51a0`; the T02 branch incorporates main and PR #10 targets `main` with only the T02 increment. Earlier baseline/branch observations above describe the initial T02 implementation.

## T03 profile-sized procedure evidence

T03 completed locally in DEEP + SOLO on `feat/hybrid-ai-workflow-profiles`, worktree
`/workspaces/claude-plugins/.worktrees/feat/hybrid-ai-workflow-profiles`, based on
`775372df4c65a397bc74687a20052ebb6c9c0852` (merged T02 PR #10). Clean primary `main` was updated by fast-forward
before creating the worktree. No subagent, other harness, orchestrator, commit,
push or PR was used for T03. Historical inventory and findings above are preserved;
this section records targeted remediation rather than silently replacing baseline.

### Exact scope and minimum changes

The sixteen guidance paths are enumerated in the T03 task and in the explicit
`PROFILE_DOCUMENTS` tuple in `tests/test_workflow_contract.py`:

- `spec` and `architect`: concise QUICK/session output, relevant STANDARD design,
  durable DEEP files/dependencies/gates/decisions; template/checklist is selective,
  not a full dossier for every edit; explicit stage boundary.
- `test` and `tdd-guide`: selected feature/fix RED-GREEN-REFACTOR and meaningful
  reproducers remain; documentation can use a documented check; project-command
  discovery includes unittest and checks runner side effects. Removed universal
  test-first/all-types/80% requirements and phantom provider prerequisite.
- `ai-regression-testing`: retain domain regression examples, replace extra
  bug-check skill/command proposal with existing test/review links; no automatic
  API tests for a wording-only change and no instruction to ignore new behavior.
- `review`, `code-review`, `code-reviewer`, `simplify`: current unstaged/staged and
  relevant untracked work first, then actual task base when clean or intended
  explicit revision; documentation/configuration included. Existing role/checklist
  and local/PR transport preserved. Shared AGENTS policy first; no package fetch;
  report publication needs authority; rollback only owned simplification edits.
- Common testing/code-review/patterns/performance rules: profile/risk-sized checks
  and research, local role fallback, no universal coverage/dossier/parallel agents;
  failed mandatory project security/coverage gates still block readiness.
- Git development-workflow rule: shared stage responsibilities instead of another
  research/TDD/commit pipeline; safe standalone defaults and plugin-local links.
- Toolkit search-first and verification-loop: proportional local-first research,
  scoped adoption actions, relevant checkpoints, real exit status, NOT RUN versus
  NOT APPLICABLE, no global 80% example or automatic last-commit target.
- `tests/test_workflow_contract.py`: seven additional tests, explicit 16-file audit
  scope, eight historical-directive negative samples, eight project-gate mutation
  samples across four documents, scope/provider/publish/link regressions. The
  test-only prose checker ignores fenced examples and frontmatter, keeping actor
  metadata migration scoped to T04; confidence percentages are not coverage gates.
- `docs/plans/hybrid-ai-workflow/{plan,tasks,audit}.md`: task status and this evidence.

Names and native command/agent wrappers are preserved. Shared tdd-guide's coverage
claim was corrected with its T03 technique scope; the native tdd-guide trigger and
remaining proactive/MUST-BE-USED metadata are explicitly pending T04. The shared
workflow contract itself is unchanged, with no duplicate skill or new lifecycle.
Readability-only Markdown fixes (headings, fences, lists and table separators) are
limited to the touched documents. No manifest/version, hook, native adapter,
historical plan or sibling-repository file changed. T08's paired version procedure
remains a future delivery/release boundary, not authority to modify manifests now.

### Commands, observed results and limits

| Command / check | Exit | Observed result |
| --- | --- | --- |
| `python3 -B -m unittest discover -s tests -p test_workflow_contract.py -v` | 0 | 12 tests PASS, including 7 new T03 checks |
| `python3 -B -m unittest discover -s tests -p test_codex_manifests.py -v` | 0 | 3 tests PASS; identities, contained references and native wrappers intact |
| `python3 -B -m unittest discover -s tests -p test_rule_scanners.py -v` | 0 | 2 tests PASS; scanner and both-host directory behavior unchanged |
| Markdown lint on changed Markdown, MD013 disabled | 0 | Structure/formatting PASS; no additional lint rule disabled |
| Plugin/document links, task-status and scope inspection; `git diff --check` | 0 | No broken local link/fragment or whitespace error; exact task scope only |

An intermediate test run caught a missing exact project-failure declaration in
verification-loop (semicolon instead of a sentence boundary); the document and
negative-test precondition were corrected and the final suite passes. This is
static declaration coverage, not a claim of model obedience. Initial Markdown
lint found existing formatting issues in the touched files and moved heading
positions; they were corrected locally without disabling structural checks.
Native discovery/full unittest discovery, model scenarios, optional providers,
Bash 3.2/macOS and consumers remain NOT RUN under current restrictions. Guard
was not repeated because no isolation/hook implementation changed; its passing
T01 fixture evidence is historical, not a new T03 run.

### Separate local scenario walkthroughs and negative policy samples

- S02 QUICK documentation typo: spec can stay in session, Plan is a short checklist,
  Build is scoped wording, Test is meaningful Markdown/link validation, Review
  sees the actual unstaged/staged/untracked change, Simplify can be a no-op, Ship
  is readiness only. No synthetic RED, registry sweep or mandatory design dossier.
- S03 STANDARD observable bug: accepted behavior, affected files/checks, meaningful
  reproducer, expected RED, authorized fix, GREEN and appropriate regressions;
  code review/Simplify invalidate and rerun affected checks. A verification-only
  request reports defects without silently authorizing implementation.
- S04 DEEP architecture change: repository-grounded alternatives, durable phases,
  exact files/dependencies/ownership/gates, impact/rollback and a separate local
  role review pass. Current host/model remains; no worker launched by complexity.
- Required-policy sample: a project can require 95% coverage, TDD for a component,
  security checks and no exposed secrets. The static checker accepts those scoped
  requirements and rejects deleting the binding/failure declarations in each of
  four active policies. Failed security/coverage gates block readiness even in
  QUICK; unavailable required gates stay NOT RUN, never PASS. No synthetic policy
  runtime was created to mirror and “prove” English instructions.
- Scope sample: opposing staged and unstaged changes are both inspected, relevant
  untracked docs are not dropped, and a clean task branch uses its actual base.
  A recent unrelated commit is never the default review target.
- S09 boundary check: PR-number input produces a local artifact, not automatic
  external publication; commands run only with publication authority. Full Ship
  and all other delivery paths remain pending T06, so S09 integration is not
  claimed complete here.

These are same-agent source walkthroughs, not independent or live-harness trials.
F01/F02/F03/F13/F19/F20 are addressed only in the T03 owners above. Native actor
triggers, other worktree/Ship/toolkit paths and the hard optional-provider manifest
still await T04–T08. Remaining uncertainty is their integration and actual model
behavior; full conformance is not claimed. T03 is marked complete locally with no
commit/push/PR. Stop before T04; further delivery or implementation needs a new
instruction.

### T03 PR preparation update

The subsequent user instruction authorizes committing/pushing T03 and opening its
PR to main. Following the T03/T08 version procedure, increment only version fields
in each paired Claude/Codex manifest: development-lifecycle 1.1.1 → 1.2.0,
agent-toolkit 1.0.1 → 1.1.0, git-workflows 1.2.1 → 1.3.0. These six metadata edits
are the sole scope extension at the authorized PR boundary; names, discovery,
hooks and dependencies remain unchanged. Earlier no-manifest/no-delivery statements
above describe the initial implementation stage. T04+, merge and release remain
unauthorized. Revalidate tests, Markdown and scope before publishing.

## T04 role authorization evidence

T04 completed locally in DEEP + SOLO on `feat/hybrid-ai-workflow-role-authorization`,
worktree `/workspaces/claude-plugins/.worktrees/feat/hybrid-ai-workflow-role-authorization`,
based on `a6b54c40f7e1189fcfb4b36378edcfccaddf580d` (merged T03 PR #11). Primary `main` was clean and updated
fast-forward before worktree creation. No subagent, other harness, orchestrator,
commit, push or PR was invoked for this task. Earlier inventory remains historical.

### File-level changes and compatibility

Exact owners are the 23 implementation/test paths listed in T04, plus the three
plan evidence documents. No additional product path is changed.

- Native/shared role pairs: lifecycle architect, build-error-resolver,
  code-reviewer, doc-updater, docs-lookup and tdd-guide; backend database-reviewer;
  dotnet csharp-reviewer; renovate renovate-auditor; devcontainer
  devcontainer-auditor. Purpose-specific descriptions now say local by default
  and require explicit user authorization for separate-agent execution. Removed
  proactive/MUST-BE-USED actor triggers and the native unconditional TDD/80% claim.
- Native adapters change only description text. Exact presence/absence and values
  of all other frontmatter fields (name, tools, model) and their one-link bodies
  are frozen in regression tests. Missing native names remain implicit basenames.
- Shared role entry guards default to STANDARD + SOLO while preserving explicit
  task selection. A role name grants no new actor; HANDOFF/PARALLEL/REVIEW require
  authority before exposed capability. Guard preserves configured model/task/tool
  scope, prohibits another CLI bypass and requires shared AGENTS policy/conflict
  reconciliation before dependent actions.
- All six lifecycle roles reference the same plugin-local workflow contract.
  Domain guards add no dependency or cross-plugin resource link. Four domain
  checklist suffixes have the same SHA-256 as the merged T03 baseline.
- Common agents rule names actor topology and authority, including read-only
  parallel work; missing capability is disclosed without silent topology change.
  Writer isolation/integrator duties and honest partial-result reporting remain.
- Security rule retains mandatory applicable checks and local assessment. Missing
  security-reviewer does not waive a security/coverage failure. Fixes require
  actual scope; rotation/runtime remediation needs separate fresh permission
  with impact/rollback. Conflicting host policy cannot select weaker safety.
- `tests/test_workflow_contract.py` adds seven tests and baseline compatibility
  constants. `plan.md`, `tasks.md`, `audit.md` record status, evidence and next task.

The original domain checklist text is not reformatted or rewritten. Existing
lifecycle role procedures beyond guard/description remain intact. No tools/model
was selected or a native agent instantiated in this session. No manifests,
versions, hooks, duplicate skills, new lifecycle or sibling repositories changed;
paired versions belong to a later authorized PR boundary under T08's procedure.

### T04 commands and results

| Command / check | Exit | Observed result |
| --- | --- | --- |
| `python3 -B -m unittest discover -s tests -p test_workflow_contract.py -v` | 0 | 19 tests PASS, including 7 new T04 tests |
| `python3 -B -m unittest discover -s tests -p test_codex_manifests.py -v` | 0 | 3 tests PASS; identity/discovery metadata, wrapper links and contained resources |
| `python3 -B -m unittest discover -s tests -p test_rule_scanners.py -v` | 0 | 2 tests PASS; both-host scanner behavior |
| Markdown lint comparison, MD013 disabled | 0 | Baseline 69 diagnostics, current 67 across 22 touched role/rule Markdown files; no added count for any file/rule pair |
| Plan-evidence Markdown lint, local links/fragments, scope/metadata inspection and `git diff --check` | 0 | PASS; primary clean on main, exact authorized paths only |

Markdown comparison reads baseline file contents with `git show HEAD:<path>` into
a temporary directory, runs installed markdownlint-cli with `--json --disable
MD013`, and compares diagnostic counts for each relative file/rule pair. This
is a no-added-diagnostics check, not a claim that all historical formatting is
clean. Existing headings/list/table issues remain in preserved checklists.
Native wrappers and domain bodies stay unchanged rather than normalize those
unrelated sections. Newly written rules and plan evidence are checked separately.

### Separate local walkthroughs and negative samples

- S01 direct role request: description and shared entry guard both select local
  role application by default. A tool registry or a named role cannot create
  authority. STANDARD + SOLO applies when fields are absent.
- S04 DEEP + SOLO: same expertise applied as a local pass, preserving configured
  model and tool/permission limits, with lack of independent review disclosed.
  No second agent/harness launch is suggested by complexity.
- Authorized external reviewer missing: common agents rule discloses the limit
  and offers local sequential analysis only if compatible with user intent;
  available-but-unauthorized native agents remain unused.
- Security issue with no reviewer: perform the local checklist/assessment and
  report a failed required security gate as blocking readiness. Absence of a
  specialist cannot convert failure into PASS or trigger a secret rotation.
- Conflicting AGENTS versus host-adapter policy: shared-role and security guards
  require reporting the conflict and pausing dependent actions; neither host
  silently chooses a weaker rule.
- Static negative samples delete the role-not-actor, explicit authority,
  authority-before-capability and conflict boundaries; four more weaken the
  missing-reviewer, required-gate, rotation-permission and policy-conflict
  declarations. Tests reject each sample. Metadata tests cover all ten adapters,
  paired descriptions, immutable non-description fields and original wrapper
  bodies; domain hashes verify exact checklist preservation.

These are source-based same-agent walkthroughs and document checks, not an
execution policy engine or proof of native/model behavior. Native discovery/full
suite and live actor scenarios remain NOT RUN under the no-other-harness
constraint. Hook/guard tests were not repeated because no hook/isolation code
changed. Remaining F04/F05/F20 behavior outside these owners is queued for
T05–T08; full workflow conformance is not claimed. T04 is complete locally and
uncommitted; stop before T05 and delivery pending another instruction.

### T04 PR preparation update

The subsequent user instruction authorizes T04 commit/push/PR. Apply the planned
paired patch version increments for corrected role authorization guidance:
development-lifecycle 1.2.0 → 1.2.1; backend and dotnet 1.0.1 → 1.0.2; renovate
and devcontainer 0.1.1 → 0.1.2. Only version fields change in the ten manifests;
identities, tool/model metadata, discovery paths, hooks and dependencies remain
unchanged. Earlier no-manifest/no-delivery statements describe the initial T04
implementation. T05+, merge and release remain unauthorized. Revalidate static
tests, local links, diff whitespace and Markdown diagnostics before publication.
