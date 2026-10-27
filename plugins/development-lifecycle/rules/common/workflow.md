# Hybrid AI Engineering Workflow

## Lifecycle

```text
Spec → Plan → Build → Test → Review → Simplify → Ship
```

This is the collection's single engineering lifecycle. Stages describe what
happens; the execution profile sets depth; the execution topology assigns actors.
A skill is a procedure, and a harness supplies tools. Neither creates another
lifecycle. All seven stages remain conceptually present and in this order.
A profile may combine activities or omit a separate document, not remove a stage.
Tests may guide Build through TDD; that technique does not reorder the lifecycle.
If Review or Simplify changes the result, rerun affected checks before readiness.

Plan uses existing specification, architecture and planning procedures; Build is
scoped implementation. Stage names do not imply new `/plan` or `/build` commands.
Keep existing skill, command and agent names and historical artifact paths.

## Selection and defaults

Resolve profile and topology independently, using this precedence:

1. Explicit current user instruction, within safety and permission constraints.
2. Recorded accepted state for the same task, checked against current authority.
3. The default for each missing field:

```yaml
defaults:
  profile: standard
  topology: solo
```

The logical default is STANDARD + SOLO in every harness. Display names uppercase;
accept explicit names case-insensitively and persist enum values lowercase.
No configuration file or workflow engine is required. A bare developer request
uses both defaults; `quick` or `deep` changes only profile. A request for a
separate reviewer, transfer or parallel team changes topology only within its
explicit scope. Selecting an expert role can mean a local role pass, not spawning
an agent. Task complexity, available agents, a plan or DEEP never grants authority.
Clarify unknown values or conflicting instructions before dependent actions;
continue only independent work that stays within the established scope.

Record the chosen profile/topology in an existing plan or handoff when present;
a brief session record is enough for a small QUICK task. A saved selection is
state, not new permission, and cannot override a restriction or revoked consent.

## Execution profiles

Choose QUICK for small reversible low-risk work, STANDARD for normal engineering,
and recommend DEEP for architecture, migrations, broad impact or multi-step work.
A recommendation does not silently change the user's selection.

| Stage | QUICK | STANDARD | DEEP |
| --- | --- | --- | --- |
| Spec | Session goal, scope and success | Concise requirements, non-goals and acceptance | Repository-grounded specification, constraints and measurable risks |
| Plan | Mental plan or short checklist | Affected areas, dependencies and gates; durable file for multi-session work | Durable staged tasks, decisions, ownership, rollout/rollback and permission gates |
| Build | Smallest scoped edit | Complete scoped implementation | Phased implementation with integration contracts and impact control |
| Test | Smallest meaningful regression or documented check | Appropriate automated checks and project gates | Layered positive, negative and scenario evidence |
| Review | Focused self-review of scope and regressions | Full self-review or separate local pass | Separate deliberate review pass; another agent only under authorized topology |
| Simplify | Remove obvious noise within scope | Evaluate a simpler, readable solution | Record alternatives, maintenance and operational tradeoffs |
| Ship | Readiness and only authorized delivery | Verify gates and perform only authorized actions | Readiness with rollout/rollback and separate runtime permission |

Research is proportional to uncertainty; start from relevant repository evidence.
Full planning dossiers, external research, TDD, every test type and a universal
coverage percentage are not prerequisites for every edit. TDD remains useful when
selected or required by project policy. A no-op Simplify assessment is valid.
DEEP + SOLO uses local role passes, including a distinct review pass; disclose
that self-review is not independent review by another actor.

## Execution topologies

| Topology | Actor contract |
| --- | --- |
| SOLO | One current owner performs the lifecycle; no subagent, other harness or orchestrator launch. Local sequential role passes are not independent agents. |
| HANDOFF | Explicitly authorized transfer through a portable handoff. The receiver verifies base, branch, worktree, scope, evidence and outstanding permissions. |
| PARALLEL | Explicitly authorized independent scopes with one named owner/integrator. Each concurrent writer has a separate branch/worktree; the integrator owns integration and final gates. |
| REVIEW | Explicitly authorized separate reviewer, read-only by default, reporting findings with file/line evidence. Write scope needs separate authorization. |

A read-only reviewer can share the owner's worktree when authorized. A sequential
writer can use that isolated worktree within its authorized scope. These are
isolation permissions, not authority to add actors. A failed work unit or review
must be reported; do not claim successful integration or independent review from
partial results.

## Authorization and capabilities

HANDOFF, PARALLEL and REVIEW require explicit user authorization before changing
actors. Do not infer it from recommending a topology, choosing a skill or being
able to call a tool. Reuse authorization already provided for the same action and
scope; do not repeatedly request it. Record the owner, scopes, integrator where
needed, allowed side effects and restrictions without storing secrets.

Check authority before capability. Then inspect actual exposed tools and schemas
for delegation, hooks, isolation, scheduling, memory or external services. A CLI,
Markdown agent file or installed plugin is not proof of an exposed capability.
Never launch another CLI, worker or service to bypass a delegation restriction.
If a requested capability is missing, report the limitation and use a manual or
SOLO path only when consistent with the user's intent. Do not silently relabel
self-review as REVIEW or local execution as HANDOFF. Missing tools never justify
fabricated calls, successful scans or background continuation claims.

An external orchestrator is optional, not required for correctness. A future
pilot requires at least three completed manual HANDOFF/PARALLEL tasks and a
partial-execution failure test. Even authorized delegation does not authorize
an uncontrolled auto-dispatch or auto-merge chain. Inspect service side effects
before calling it; if it cannot respect scope and permissions, do not use it.

## Safety and worktree-first

Every profile preserves mandatory safety rules, user permissions, worktree-first
and project quality gates. QUICK cannot lower these requirements. Recommend
DEEP for destructive or high-impact changes while retaining the mandatory gates
regardless of the chosen profile.

Before a write, verify repository root, default branch, status and isolation;
distinguish a linked worktree from a submodule. The primary checkout remains
clean on its default branch. Use exposed native isolation if suitable, otherwise
manual git worktrees. Locally exclude `.worktrees/` via `.git/info/exclude`, not a
tracked `.gitignore` change. If isolation is blocked, stop writes and report the
permission prerequisite; never silently fall back to editing primary. Explicitly
authorized primary maintenance is a separate operation, not a sandbox workaround.
Do not reset, stash, clean or remove another owner's work to obtain a clean state.

Apply shared project policy from applicable `AGENTS.md`, host adapters and project
documentation; surface conflicts rather than choose different policies by host.
Do not copy a consumer's cluster-specific rules into global skills. Keep secrets
out of prompts, artifacts, logs, test fixtures and PRs; use references, not values.
Use existing project tools and required checks; report unavailable checks and
uncertainty, never silently pass them or fetch/install dependencies implicitly.

## Artifacts and evidence

Preserve the established project artifact directory and old formats. When no
convention exists, use `.plans/<slug>/plan.md` and `tasks.md` for a new durable
plan. Do not migrate `.plans`, `.archive/.plans`, Superpowers or PRP history.
No artifact file is mandatory for every QUICK task.

A durable plan records objective/non-goals, acceptance, profile/topology,
owner/integrator, base SHA, branch/worktree, decisions, exact scopes and ownership,
tasks/dependencies, gates, permission/runtime impact, rollout/rollback, status and
next action. Each task names files, intended change, dependencies, verification,
expected result and completion criterion. Decision records include alternatives,
choice, consequences and a revisit condition.

A handoff is a snapshot: task, from/to (or unassigned), base SHA, branch/worktree,
profile/topology/status, completed changes, decisions, affected files, test
results, risks, missing permissions and exact next step. It must be usable without
chat history. The receiver checks current repository state and authority first;
a stale base or permission mismatch needs reconciliation before dependent writes.

Record checks as PASS, FAIL, NOT RUN or NOT APPLICABLE with reasons and actual
commands/results. Distinguish static checks, local scenario walkthroughs and live
harness trials. Do not claim independent, native or runtime evidence from prose.

## Stage and delivery boundaries

An instruction for a stage or task authorizes that bounded work only. Stop after
the requested stage; planning does not authorize Build, and completing a task does
not authorize subsequent tasks. The seven-stage model describes the overall
workflow, not permission to run every stage in this session.

Ship means readiness assessment and only the delivery actions already authorized
by the user. Readiness alone does not authorize commit, push, PR creation, external
review publication, merge or deployment. Keep those actions distinct; for an
explicit PR request, necessary branch push may be within scope. Use existing
specific authorization rather than adding redundant confirmation prompts.
Never silently include unrelated/untracked work or bypass mandatory project gates
with a blanket GO/override. A failed or required but unrun gate limits readiness.

A merge that triggers GitOps or HCP auto-apply is a runtime mutation. Runtime and
destructive mutations need separate fresh explicit permission with impact and
rollback; plan approval or delegation permission is not runtime consent. A revert
of plugin guidance cannot reverse runtime changes. Keep rollback scoped, preserve
user artifacts and do not discard work or remove worktrees without authorization.

## Loading and host limitations

Read this contract through the existing `development-lifecycle-rules` skill when
following this collection's workflow. It is plugin-local guidance, not a new
skill, command, scheduler or execution engine. Existing commands and role
entrypoints keep their names and share the same procedure files across hosts.

Rules load on demand. Installing a Markdown plugin does not intercept arbitrary
prompts or automatically load this contract into every session. Claude retains
native entrypoints and its existing git-workflows worktree hooks as a best-effort
backstop; hook errors or missing jq do not waive procedural requirements. Codex
uses shared skills and explicit preflight; collection manifests keep `hooks: []`.
Markdown native-agent files do not automatically register Codex agents. Shared
contract does not mean equal enforcement. Projects can reference this contract
through their existing policy; no global host configuration is installed here.

Superpowers may supply an explicitly selected technique when available, but the
workflow must have a local/manual path when it is absent. Do not invoke an absent
provider or create another catalog of copied skills. OpenCode currently has a
manual path through shared project instructions and Markdown artifacts; native
integration and capability parity require a later pinned-version spike.
