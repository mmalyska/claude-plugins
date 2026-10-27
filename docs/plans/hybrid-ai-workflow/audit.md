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
