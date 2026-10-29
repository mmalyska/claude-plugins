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

Defaults fill omitted values, not explicit unknown names. Restrictions on actors
do not resolve an unknown topology. For example, `topology AUTO` together with
`do not start another actor` still requires clarification before implementation:
ask whether SOLO was intended and keep the selection unresolved until answered.
Do not substitute SOLO merely because it is the only permitted topology;
announcing a substitution is not clarification. Independent read-only inspection
may continue within scope, but dependent edits must wait. A valid explicit or
accepted selection still applies without redundant confirmation.

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

For DEEP multi-session work, review the completed plan draft in a distinct local
pass before marking Plan complete. Inspect the actual drafted artifacts and tasks,
then record their scope/revision, findings and corrections or a reasoned no-change
result, with evidence and limits. A completion sentence, line count or future code
Review task alone does not establish this pass. This is plan validation inside
Plan, not authority for Build, the later product Review stage or another actor.
If the pass is incomplete, record NOT RUN and keep the plan draft/incomplete.

Reconcile task write/output paths, dependencies, decision-conditional branches,
check commands, expected results, done/rollback criteria, ownership/base/worktree,
authority and next action against that draft. A task that records a decision or
findings must name the durable output path; Files none means no file mutation.
Keep proposed decisions distinguishable from accepted ones and carry unverified
research as uncertainty. QUICK remains a brief session plan without a dossier.

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

When asked to consider specialists, assess the benefit and coordination cost.
A reasoned SOLO conclusion is valid; do not invent specialist work for a small task.
If recommending specialists, describe bounded candidate scopes, expected benefit
and any missing actor authorization as a proposal only. Keep execution within current
authority; a proposal does not authorize dispatch or require pausing unrelated
authorized SOLO work to request workers.

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

Before the first edit, including in an existing worktree, establish these facts
from actual Git output rather than a directory name or branch-name convention:

```sh
git rev-parse --show-toplevel
git rev-parse --absolute-git-dir
git rev-parse --git-common-dir
git rev-parse --show-superproject-working-tree
git branch --show-current
git status --porcelain
git worktree list --porcelain
```

Resolve Git/common directories to absolute physical paths. Use the worktree
metadata to locate primary; check its actual branch, HEAD and status with
`git -C <verified-primary> branch --show-current`, `rev-parse HEAD` and
`status --porcelain`. Check the writer HEAD and accepted task base too. A path
containing `.worktrees`, a feature branch, a hook's silence or controller setup
is not evidence that these checks ran. Do not treat a submodule as a linked
worktree; verify its superproject's isolation and ownership before mutation.

Resolve the default from origin/HEAD or verified project policy. In a no-remote
fixture without default policy, report that no remote default is available and
record the verified actual primary branch as the local task base when consistent
with the task. `init.defaultBranch` is only a creation preference, not proof of
an existing repository's default. Missing origin/HEAD alone need not block work
when that local base and isolation are verified. Ambiguous isolation/base, dirty
or non-default primary means stop dependent writes and report the discrepancy;
never repair it by switching, resetting, stashing or cleaning user state. Record
the verified primary, writer and base briefly in session or existing task state.
The existing git-workflows worktree skill supplies setup/creation details; these
checks apply even when no worktree needs creating.

A denied or unexecuted prerequisite check remains unresolved; successful partial
output does not complete the other checks in a rejected compound command. Retain
facts already established, identify what is still missing, and recover only with
permitted read-only checks or the host's normal permission path within scope.
Do not bypass a denial or repeat an action the host forbids retrying. Equivalent
Git output may establish a fact without repeating a particular command. If the
remaining isolation/default/base facts cannot be verified, stop dependent writes
and report the blocker; unrelated read-only work may continue. Permission to edit
is not evidence that pre-write prerequisites passed. Do not record a denied
origin/default query as an absent ref or a verified no-remote fallback.

Apply shared project policy from applicable `AGENTS.md`, host adapters and project
documentation; surface conflicts rather than choose different policies by host.
An unresolved conflict over a required project gate blocks dependent edits.
Report the disagreement and the blocked implementation before changing files;
do not defer reconciliation until Test, verification or Ship. Choosing the
stronger gate or proposing to run both checks does not by itself reconcile
contradictory instructions. Independent read-only diagnosis may continue within
scope. Reuse a valid recorded reconciliation checked against current authority;
ask only when the genuine disagreement remains unresolved. Clearly compatible
additional checks and an already reconciled policy need no extra confirmation.

Do not copy a consumer's cluster-specific rules into global skills. Keep secrets
out of prompts, artifacts, logs, test fixtures and PRs; use references, not values.
Use existing project tools and required checks; report unavailable checks and
uncertainty, never silently pass them or fetch/install dependencies implicitly.

## Artifacts and evidence

Preserve the established project artifact directory and old formats. When no
convention exists, use `.plans/<slug>/plan.md` and `tasks.md` for a new durable
plan. Do not migrate `.plans`, `.archive/.plans`, Superpowers or PRP history.
No artifact file is mandatory for every QUICK task.

Packaged optional structures: [plan](../../resources/workflow/plan.md),
[tasks](../../resources/workflow/tasks.md),
[handoff](../../resources/workflow/handoff.md#receiver-preflight) and
[decision](../../resources/workflow/decision.md). Reuse the existing ADR process;
these are resources, not new skills. Template values grant no authority. Persist
profile/topology in lowercase; explicit current instructions still take precedence.
An unassigned receiver cannot claim a transfer or launch a worker.

A durable plan records objective/non-goals, acceptance, profile/topology,
owner/integrator, base SHA, branch/worktree, decisions, exact scopes and ownership,
tasks/dependencies, gates, permission/runtime impact, rollout/rollback, status and
next action. Each task names files, intended change, dependencies, verification,
expected result and completion criterion. Decision records include alternatives,
choice, consequences and a revisit condition.

Keep handoffs in the active plan folder; `.ai/handoffs/` is the fallback only
for tasks without an active plan, preserving established project locations.

A handoff is a snapshot: task, from/to (or unassigned), base SHA, branch/worktree,
profile/topology/status, completed changes, decisions, affected files, test
results, risks, missing permissions and exact next step. It must be usable without
chat history. The receiver checks current repository state and authority first;
a stale base or permission mismatch needs reconciliation before dependent writes.

Record checks as PASS, FAIL, NOT RUN or NOT APPLICABLE with reasons and actual
commands/results. Distinguish static checks, local scenario walkthroughs and live
harness trials. Do not claim independent, native or runtime evidence from prose.

### Check exit status

Capture the test runner's exit code before another command can overwrite it.
This evidence requirement applies in every profile, even when the on-demand
[testing rules](testing.md) have not been loaded. Run each short check in its own
tool call with complete output and its own exit status. Run Git diagnostics in a
separate call. Apply this to both expected RED failures and GREEN verification.

Do not infer test success from `tests | tail`, `tests | tee`, or
`tests; git status`: the shell may return the filter's or final command's status.
If a wrapper is needed, preserve and return the runner status explicitly. For
this repository's unittest-style checks, this shell pattern also works with
`set -e` enabled:

```sh
check_status=0
python3 -B -m unittest discover -s tests -v || check_status=$?
printf 'unittest exit: %s\n' "$check_status"
exit "$check_status"
```

Use the actual project's check command. For large output, keep a complete log in
an authorized location and capture the runner exit code before displaying an
excerpt. A successful filter or later diagnostic cannot turn a failed test into
a PASS. If the runner status was lost, rerun the check with proper capture before
claiming verified success; otherwise report the missing evidence explicitly.

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
following this collection's workflow. Load the complete contract on first use,
resolving links from the active installed skill. Continue truncated reads through
the final section; summaries and head-only excerpts do not satisfy initial
loading. If required guidance is unavailable, stop dependent work and report it;
do not replace it with an invented procedure. It is plugin-local guidance, not a new
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
