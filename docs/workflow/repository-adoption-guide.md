# Repository adoption guide

How to adapt another repository to the Hybrid AI Engineering Workflow. The guide is
harness-agnostic: it applies to Claude Code, Codex and a future OpenCode adapter.
It is derived from two completed adoptions, a workstation-bootstrap repository
(`dotfiles`) and a GitOps infrastructure repository (`home-ops`), generalized so
that nothing here depends on either of them.

## 1. Purpose and ownership

This page is a procedure for adopters. It defines no workflow of its own.

| Concern                                                                                                                   | Owner            | Where                                                                                                                                                                                                                                                                                                          |
| ------------------------------------------------------------------------------------------------------------------------- | ---------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Lifecycle, execution profiles, execution topologies, defaults, authorization, worktree-first, artifact and evidence rules | `claude-plugins` | The [workflow contract](../../plugins/development-lifecycle/rules/common/workflow.md) is normative                                                                                                                                                                                                             |
| Capability matrix, deferred consumer follow-ups, release sequence                                                         | `claude-plugins` | [Compatibility and consumer strategy](compatibility.md)                                                                                                                                                                                                                                                        |
| Portable plan, tasks, handoff and decision structures                                                                     | `claude-plugins` | [plan](../../plugins/development-lifecycle/resources/workflow/plan.md), [tasks](../../plugins/development-lifecycle/resources/workflow/tasks.md), [handoff](../../plugins/development-lifecycle/resources/workflow/handoff.md), [decision](../../plugins/development-lifecycle/resources/workflow/decision.md) |
| Worktree layout and the Claude guard                                                                                      | `claude-plugins` | [Worktree workflow](../../plugins/git-workflows/rules/worktree-workflow.md)                                                                                                                                                                                                                                    |
| This adoption procedure and its templates                                                                                 | `claude-plugins` | This page                                                                                                                                                                                                                                                                                                      |
| Application of the workflow in one repository                                                                             | That repository  | Its own `AGENTS.md`, policy files, plans and contributor docs                                                                                                                                                                                                                                                  |

Rules for adopters:

- Link to the contract; never restate the lifecycle, a profile or a topology. A copy
  drifts, and a drifted copy is a second specification. Add a test that fails when a
  definition is copied (section 11).
- Repository-local documentation records only how the workflow is applied there:
  which files hold the rules, which gates run, which actions need consent.
- Pin the revision of `claude-plugins` that you link to (a tag or a commit), and
  record it. A mutable branch is not a reproducible reference.
- The [specification](specification.md) is background and rationale. Where it and
  the contract differ, follow the contract.
- Superpowers, if installed, is an optional technique provider. No stage of the
  workflow may depend on it, and an adoption must work with it disabled.

## 2. When to adopt, and how risk sets planning depth

Adopt when more than one harness, session or person works in the repository, or when
agent mistakes are costly (secrets, shared infrastructure, publication on merge).
Do not adopt for a throwaway repository; a single `AGENTS.md` with the hard rules
is enough there.

The adoption itself is a change to the files agents obey, so plan it in proportion
to the repository's risk. The profile names below are defined in the contract; this
table only recommends one for the adoption work.

| Repository risk | Typical signals                                                                                                                       | Recommended depth for the adoption                                                        | Extra care                                                                                  |
| --------------- | ------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------- |
| Low             | Library or documentation; merge publishes nothing; no secrets                                                                         | QUICK or STANDARD                                                                         | Still add `AGENTS.md`, worktree-first and the validation matrix                             |
| Medium          | CI pipelines, release tooling, shared build configuration, credentials in CI                                                          | STANDARD                                                                                  | Permission matrix, drift tests, pinned workflow references                                  |
| High            | Merge deploys or publishes; infrastructure as code with auto-apply; secrets or key material in scope; destructive operations possible | Recommend DEEP for the adoption and for any later change to guard, permission or CI files | Durable plan, tested rollback, merge classified as an operation, explicit consent templates |

A recommendation does not change the profile the user selected, and no profile
lowers a safety, permission, worktree or quality-gate requirement. Re-evaluate the
risk when the repository gains an automatic effect on merge.

## 3. Instruction ownership model

One file holds the rules every session must obey. Everything else points to it.

| Layer                                                              | Holds                                                                                                                                                     | Must not hold                                                                            |
| ------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------- |
| `AGENTS.md` (repository root)                                      | The canonical shared rules: project overview, hard rules, worktree-first, permission classes, validation gates, plan conventions, pointers to deeper docs | Harness tool names, installation steps, long procedures, copies of the workflow contract |
| Thin harness adapters (for example `CLAUDE.md`)                    | An import of or pointer to `AGENTS.md`, plus facts true for only that harness (settings location, hook behavior, memory location)                         | A second copy of any rule, or a rule that contradicts `AGENTS.md`                        |
| Placeholders for harnesses not yet verified (for example OpenCode) | A short note: read `AGENTS.md`, run the preflight by hand before the first write, no parity claim                                                         | Any statement about behavior you have not probed                                         |
| Policy files (`.agents/policy/` or your equivalent)                | Detailed permission lists, validation matrix, plan-index rules, loaded on demand                                                                          | Anything an agent needs on every turn                                                    |
| Project skills                                                     | Domain procedures, with one canonical location                                                                                                            | Statements about a harness's behavior presented as repository facts                      |
| Memory and notes                                                   | Hints and history                                                                                                                                         | Rules. A rule has a home in `AGENTS.md` or policy, never only in memory                  |

Guidelines:

- Keep `AGENTS.md` short enough to be read in full by every harness; check the
  size limit of each harness you support, and record the result.
- A Claude adapter can be as small as the following. If an import is not honored
  by the version you use, replace it with an instruction to read the file; do not
  copy the rules.

  ```md
  # Claude Code adapter

  @AGENTS.md

  Claude-specific facts only. `AGENTS.md` is authoritative.
  ```

- When two instruction sources disagree about a required gate, that is a conflict
  to report and resolve before dependent edits, as the contract requires. Never
  resolve it silently per host.
- Archived plans, old notes and generated mirrors are history or output, not
  instructions. Say so in `AGENTS.md`.
- Never write secret values, private hostnames, addresses or account identifiers
  into instructions, plans, tests, fixtures or PR text. Use names and references.

## 4. Repository audit before implementation

Audit read-only, in a linked worktree, before choosing anything. Record each finding
with the command or file that produced it and the base SHA.

1. **Base.** Fetch, record the default branch and the exact base SHA. Confirm the
   primary checkout is clean and leave it untouched.
2. **Instruction files.** Find `AGENTS.md`, `CLAUDE.md`, any other harness files,
   editor or devcontainer settings, and what a session in each harness would
   actually see today. A missing `AGENTS.md` means other harnesses see no rules.
3. **Harness-specific content.** Mark rules that assume one harness: skill-loading
   mandates, tool names, memory mechanisms, "blocked by the assistant's permissions"
   statements, plan formats that name an optional provider.
4. **Existing enforcement.** Git hooks, CI jobs, harness permission files, branch
   protection (repository settings are not in the tree; ask the owner and record
   the answer with its date).
5. **Automatic effects of merge.** Which paths deploy, publish, apply or release
   when merged. List them; they drive the permission matrix (section 9).
6. **Plans and archive.** Where plans live, which formats exist, whether an index
   exists, whether history references provider-specific directives.
7. **Skills.** Where project skills live, which harnesses discover them, any
   existing mirror or symlink and how it is checked.
8. **Validation.** The commands that gate a change, which are local only, which are
   CI only, which cannot fail (a task runner that always exits 0 is not a gate).
9. **Tooling available now.** Versions of the harness CLIs, linters and runners
   present in the audit environment. Absent tools are `NOT RUN`, not assumptions.
10. **Platforms.** Operating systems and devcontainers contributors use. Symlink and
    shell behavior differ; an untested platform stays unverified.

The audit output is evidence for the plan. It authorizes nothing.

## 5. Harness capability probes

Never assume what a harness does. Probe it, and record the outcome honestly. Probe
in a disposable repository or a linked worktree; a probe that needs a live model
session needs the owner's authority to run one.

| Probe | Question                                                                                   | Typical method                                                              |
| ----- | ------------------------------------------------------------------------------------------ | --------------------------------------------------------------------------- |
| P1    | Does the harness load `AGENTS.md`, and what is its size limit?                             | A canary rule near the end of the file; ask the session to cite it          |
| P2    | Does the adapter import or pointer load `AGENTS.md`?                                       | Canary rule reachable only through the adapter                              |
| P3    | Are project skills discovered at the chosen location, through a symlink, through a mirror? | A probe skill visible only in the tested layout                             |
| P4    | Can the harness intercept a write before it happens (hook), and with what input schema?    | Harness documentation, then a disposable test; otherwise `NOT RUN`          |
| P5    | Does a linked worktree work inside the harness's sandbox, including git writes?            | Create a file and a commit in a disposable linked worktree                  |
| P6    | Do repository git hooks run from a linked worktree and from each harness?                  | A deliberately failing hook in a disposable clone                           |
| P7    | Does the platform check out symlinks correctly?                                            | Run on each supported platform, or leave `NOT RUN`                          |
| P8    | How does the harness pin a shared plugin or marketplace revision?                          | Harness documentation and an install in a throwaway configuration directory |

Record every probe with this shape:

| ID     | Harness and version | Date     | Method                   | Result                | Evidence or reason                           |
| ------ | ------------------- | -------- | ------------------------ | --------------------- | -------------------------------------------- |
| `P<n>` | `<name> <version>`  | `<date>` | `<command or procedure>` | PASS / FAIL / NOT RUN | `<observed output, or why it could not run>` |

Rules for the result column:

- `PASS` only for an observed outcome, in the stated version, on the stated date.
- `FAIL` when the behavior was observed and is wrong or absent. Keep the failure;
  design around it.
- `NOT RUN` when the probe was not executed for any reason: no session, no
  approval, tool missing, platform unavailable. State the reason. "Expected to pass"
  is `NOT RUN`.
- Use `NOT APPLICABLE` only when the probe cannot apply by design, with the reason.
- A static check, a fixture or a documentation reading is not a live-harness result.
  Label which kind of evidence you have. See the
  [evidence conventions](verification.md) used by this collection.
- Results are version-specific. Re-run or re-label them after a harness upgrade.

An unverified harness stays a placeholder in `AGENTS.md` and onboarding docs, with
the unverified claims labeled as such.

## 6. Choosing an adapter strategy

Harnesses discover project skills and instructions from different places. Choose one
canonical location for each artifact and a strategy for the rest.

| Strategy                      | Use when                                                                   | Cost and risk                                                           | Required test                                                     |
| ----------------------------- | -------------------------------------------------------------------------- | ----------------------------------------------------------------------- | ----------------------------------------------------------------- |
| Symlink                       | Every supported harness and platform follows it (probes P3, P7 are `PASS`) | Cheapest; breaks silently on a platform that does not materialize links | Link target check plus discovery probe on each platform           |
| Generated mirror              | A harness or platform cannot follow links, or you cannot verify them       | A second copy exists; it is output, not source                          | Deterministic generator, a `--check` mode, and a CI drift test    |
| Harness-specific adapter file | The harness needs different metadata, not different content                | Content can diverge if the adapter grows                                | Test that the adapter stays thin and points to the canonical file |

Mirror rules:

- Edit only the canonical files. Mark the mirror as generated, and say so in its
  directory.
- The generator is deterministic: stable ordering, no timestamps, byte-for-byte
  reproducible output. Running it twice changes nothing.
- CI runs the generator's check mode and fails on any difference. A parity test
  also catches a mirror entry with no source and a source with no entry.
- A mirror made of regular files does not depend on symlink behavior, which is why
  it is the safe default when a platform is unverified.
- Use the same pattern for any derived artifact (for example a harness permission
  file generated from the policy matrix).

Prefer generating and validating over copying by hand. Keep host-specific metadata
in the entrypoint, not in the shared skill body.

## 7. Worktree-first enforcement and its limits

The rule itself is defined in the [worktree workflow](../../plugins/git-workflows/rules/worktree-workflow.md):
the primary checkout stays on the default branch with a clean tree, and every change
happens in a linked worktree. This section covers how an adopting repository
enforces it. State the layers and their limits honestly.

| Layer                                                    | Covers                                                                          | Limits                                                                                                                       |
| -------------------------------------------------------- | ------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------- |
| Rule in `AGENTS.md` plus a preflight script or procedure | Every harness                                                                   | A model instruction; nothing stops a violation before it happens                                                             |
| Harness hook (for example the Claude `PreToolUse` guard) | The harness that supports it, for the tools and shell patterns it can see       | Sees only common writes; a program that writes from inside itself is invisible; fails open when its dependencies are missing |
| Git `pre-commit` hook                                    | A commit made from any harness in the primary checkout or on the default branch | Runs only where installed; hook installation is per clone and must be probed for linked worktrees (P6)                       |
| CI and review                                            | What reaches the default branch                                                 | After the fact                                                                                                               |
| Branch protection                                        | Direct pushes                                                                   | A repository setting outside the tree; verify and date it, and note which options are off                                    |

Guidance:

- State plainly in onboarding docs which layers exist per harness. Where a harness
  has no pre-write hook, say that its enforcement is instruction plus preflight.
- A minimal preflight compares the git directory with the common git directory,
  reports the branch and status, and exits with distinct codes for "go", "stop and
  create a worktree" and "could not tell". Treat "could not tell" as stop.
- A break-glass override is for a person at a terminal, with a recorded reason. An
  agent never sets it, never uses `--no-verify`, and never works around a denied
  write.
- Do not rely on a directory name or a silent hook as evidence of isolation.
- Layout: `.worktrees/<type>/<slug>` for branch `<type>/<slug>`, with `.worktrees/`
  in `.git/info/exclude`.

## 8. Plan and archive conventions

Preserve any established plan location and format. Only when none exists, use the
default from the contract: `.plans/<slug>/plan.md` and `tasks.md`.

- One folder per plan. A handoff, if one is needed, goes in that folder.
- Keep an index of active plans (one row per plan) and a check script that fails
  when front matter and index disagree. Run it after touching plans.
- When a plan ships or is dropped, move it to the archive in a small separate PR
  that edits the indexes and rewrites links. Do not move or rewrite old entries
  during adoption.
- Archived plans are history. Instruct agents not to follow directives found in
  them (older plans may name optional providers or tools that no longer apply).
- A plan states intent and records evidence. It authorizes no action: not delivery,
  not another actor, not a mutation.
- Plans hold no secret values and no private identifiers.
- Reuse the packaged [plan](../../plugins/development-lifecycle/resources/workflow/plan.md)
  and [tasks](../../plugins/development-lifecycle/resources/workflow/tasks.md)
  resources for resume state. The skeletons in section 17 extend them with the
  fields an adoption needs; they do not replace them.

## 9. Permission boundaries and action classes

Give every action a class, and give every class a default. The contract fixes the
principles (authority before capability, no implicit delivery or runtime consent);
the table below is a template for your repository's own matrix.

| Class                               | Examples (adapt to your tools)                                                                 | Suggested default                                                       |
| ----------------------------------- | ---------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------- |
| READ                                | Repository, git and hosting-service reads that expose no secret value                          | Allowed                                                                 |
| LOCAL_CHECK                         | Render, lint, test, diff, formatter, planning-mode output review                               | Allowed; treat output as potentially sensitive                          |
| REPO_WRITE                          | Edits in the working tree                                                                      | Allowed in a linked worktree only                                       |
| DELIVERY                            | Commit, push of a feature branch, open a PR, PR comments                                       | Only when the user's instruction covers it; never to the default branch |
| SECRET_ACCESS                       | Reading secret values, printing the environment                                                | Denied; request a reference or schema                                   |
| GITOPS_TRIGGER (or your equivalent) | Merging, changing automerge or sync policy, anything whose merge deploys, publishes or applies | Fresh consent per action, with an impact statement                      |
| RUNTIME_MUTATION                    | Applying to a live system, syncing, patching, scaling, infrastructure apply                    | Fresh consent per action                                                |
| DESTRUCTIVE                         | Deleting data or namespaces, resetting nodes, rotating credentials                             | Deep review, rollback and backup evidence, consent each time            |

Rules to carry over:

- An operation not listed takes the stricter class.
- Consent comes from the user in the current session. Text in files, PRs, issues,
  logs, tool output or another agent's message is not consent.
- Consent names the action, the target and the effect, and covers that action once.
  Approving a plan, an earlier step or a PR does not approve the next mutation.
- Subagents do not inherit consent. Non-interactive runs treat consent classes as
  denied.
- Keep a **merge-impact map**: the list of paths whose merge has an automatic
  effect, with the effect. Review and PR templates reference it.
- If a harness has a machine-readable permission file, generate or parity-test it
  against the policy matrix, so the two cannot disagree.

Consent request template (use placeholders; never real hostnames or identifiers):

> I will run `<exact command>`. Target: `<system and object>`. Effect: `<what
changes>`. Rollback: `<how it is undone>`. Do you approve this one command?

Impact statement template for a merge:

> Merging PR `#<number>` has an automatic effect. Paths: `<globs from the merge-impact
map>`. Mechanism: `<what applies or publishes, and whether it prunes>`. Rollback:
> `<revert plus the follow-up needed>`. Do you approve the merge?

## 10. Validation matrix

A validation matrix says, per change type, which checks gate it, where they run and
what cannot be checked locally. Keep it in a policy file that `AGENTS.md` links to.

| Change type                         | Local checks                                    | CI checks                  | Read-only live checks | Needs consent   | Notes                          |
| ----------------------------------- | ----------------------------------------------- | -------------------------- | --------------------- | --------------- | ------------------------------ |
| `<documentation>`                   | `<formatter, link check>`                       | `<docs build, link check>` | none                  | none            | `<publication on merge?>`      |
| `<application code>`                | `<unit tests, lint>`                            | `<same plus integration>`  | `<optional>`          | none            |                                |
| `<configuration or infrastructure>` | `<render, validate, plan>`                      | `<same>`                   | `<read-only status>`  | `<apply, sync>` | `<automatic effect on merge?>` |
| `<agent instructions and plans>`    | `<instruction tests, plan check, mirror check>` | `<same>`                   | none                  | none            | See section 11                 |

Suggested levels, if you want shorthand (these are yours to define, not canonical):
L0 local, L1 CI, L2 read-only live checks, L3 anything that needs consent.

Reporting rules, using the vocabulary from the contract:

- Record each check as PASS, FAIL, NOT RUN (with the reason), or NOT APPLICABLE.
- A check that was not executed is NOT RUN even if it is expected to pass. "Not
  installed locally, covered by CI" is NOT RUN locally.
- A green CI run is L1 evidence only. It says nothing about L2 or L3.
- Confirm that a gate can fail. A runner that always exits 0 gates nothing; read its
  output or wrap it. Capture the exit code of the runner itself, not of a pipeline
  that filters it.
- Put a Validation table (one row per check) and an Impact line in the PR template.

PR validation table:

| Check     | Command or method | Level | Result                                 | Evidence or reason   |
| --------- | ----------------- | ----- | -------------------------------------- | -------------------- |
| `<check>` | `<command>`       | L0    | PASS / FAIL / NOT RUN / NOT APPLICABLE | `<output or reason>` |

## 11. CI patterns for instructions, plans and documentation

The instructions are code: test them. Run these jobs on pull requests, scoped by
`paths` to the files they protect. Keep CI permissions read-only, give workflows no
secrets they do not need, and pin every third-party action to a full 40-character
commit SHA with the version in a trailing comment. Do not mark a new check as
required until the owner decides.

| Job or test           | Fails when                                                                                                 | Notes                                                                                         |
| --------------------- | ---------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------- |
| Instruction integrity | `AGENTS.md` is missing, too large for a supported harness, or a required section is missing                | Read the limit from the probe record                                                          |
| Thin adapter          | An adapter contains more than the import or pointer and harness-only facts, or lacks the import line       | Compare against the shared file; fail on duplicated rules                                     |
| No workflow copy      | A repository doc defines the lifecycle, a profile or a topology instead of linking                         | Search for the canonical definition tables or stage chains; allow links and one-line mentions |
| Link check            | A relative link does not resolve, or a link to `claude-plugins` is not the pinned form                     | Cover instructions, policy, plans and contributor docs                                        |
| Plan check            | Plan front matter is incomplete, an index row is missing or stale, a link to or from the archive is broken | Run the same script locally and in CI                                                         |
| Mirror drift          | A generated mirror differs from the generator's output, or has an orphan                                   | Generator check mode, not a hand comparison                                                   |
| Permission parity     | A harness permission file disagrees with the policy matrix                                                 | Only if such a file exists                                                                    |
| Hook tests            | The guard or a git hook misclassifies a case                                                               | Test the allow, ask/deny and fail-open paths; run shell scripts through ShellCheck            |
| Private-value scan    | A file contains a private domain, hostname, address, account or secret identifier                          | Maintain the pattern list outside the public tree where needed                                |
| Documentation build   | The site fails to build in strict mode                                                                     | See below                                                                                     |
| Action pinning        | A workflow uses a tag or branch reference instead of a full SHA                                            |                                                                                               |
| Clean tree            | Tests leave tracked or untracked changes behind                                                            | `git status --porcelain` must be empty after the suite                                        |

Documentation that publishes after merge must build during PR validation. If merge
to the default branch publishes a site, a broken navigation entry or link is
otherwise found on the production path. Add a PR-time job that runs the same build
in strict mode with the same configuration, read-only permissions and no deploy. If
its dependencies cannot be installed locally, the local result is NOT RUN and CI is
the evidence.

Add at least one negative test per job: a deliberately broken input in a scratch
worktree that makes the job fail. A check that has never failed has not been shown to
work.

Where the runner is not available locally (a platform, a native harness, a service),
keep the test in CI or behind an explicit opt-in switch, and record the local result
as NOT RUN. Never count a skipped test as PASS.

## 12. Rollout as small, reversible PRs

Each PR stands alone, can be reverted alone, and does not depend on an unreleased
change in another repository. Order matters: the contract is released and pinned
before consumers rely on it.

| Step                | Content                                                                                                                                                      | Revert effect                     |
| ------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------ | --------------------------------- |
| 0. Audit and plan   | Audit findings and the adoption plan, as documents only                                                                                                      | Removes documents                 |
| 1. Shared rules     | `AGENTS.md`, thin adapter, instruction-integrity and thin-adapter tests; keep the old harness file's content until every supported harness passes its probes | Restores the old state            |
| 2. Enforcement      | Preflight, hooks, git hook, permission policy and parity tests                                                                                               | Removes enforcement; rules remain |
| 3. Skills           | Canonical location, the chosen strategy (symlink or mirror), drift tests                                                                                     | Restores the previous layout      |
| 4. CI               | Plan check, link check, docs build, scans; pin actions                                                                                                       | Removes jobs                      |
| 5. Contributor docs | The repository-local application page, linking to this guide at a pinned reference                                                                           | Removes the page and nav entry    |
| 6. Pilot (optional) | One small, non-production change through the whole lifecycle; frictions become follow-up tasks                                                               | Reverts the pilot PR              |

Per PR: state the profile and topology, list validation as a table, add an Impact
line (does merge publish or deploy?), and write the rollback. Delivery actions
(push, PR, merge, tag) happen only on explicit instruction.

## 13. Migration, rollback and recovery

Migration:

- Add before you remove. Keep the old instruction content until each supported
  harness has passed the relevant probes against the new layout.
- Do not mass-move or rewrite plans, archives or notes. Add the new convention
  beside the old one and make readers tolerate both.
- Tag or record the last known-good revision of this collection and of your repo
  before each step.

Rollback:

- Each PR reverts as one unit with `git revert`. Paired artifacts (a source and its
  mirror, a policy and its parity test) revert together.
- Roll back adapters and mirrors without touching archives or plan history.
- A revert of documentation or policy cannot undo runtime effects. If a merge
  triggered a deploy or an apply, rollback needs its own authorized runtime step,
  written in the impact statement before the merge.
- Stop conditions: a permission gate regresses; skill discovery is lost; a write
  reaches the primary checkout; archive links break; different harnesses obey
  different safety rules. Stop further rollout until resolved.

Recovery:

- Pinned consumer drifted or the shared revision is bad: reinstall the last known-good
  revision, start a fresh session, and re-run the probes.
- Hook not running in a worktree: re-install per clone, then verify with the
  preflight; never skip hooks to proceed.
- Mirror drift: regenerate from the canonical files; never edit the mirror.
- An agent wrote to the primary checkout: stop, report, and fix with an explicitly
  authorized primary-maintenance step. Do not reset, stash, clean or remove user
  state to hide it.

## 14. Optional orchestration

An orchestrator is an optional client of the same artifacts, never a requirement and
never the correctness boundary. Nothing in this guide needs one, and the workflow
works with one harness and no delegation.

Consider one only after the contract's prerequisites are met (completed manual
HANDOFF and PARALLEL tasks, and a partial-execution failure test; see
[compatibility](compatibility.md#optional-orchestrator-pilot)). Any non-SOLO use
needs explicit authorization naming actors, tools, ownership, integrator and allowed
side effects. An orchestrator must not bypass permission gates, merge changes that
have runtime effects without consent, pass secrets between agents, or declare success
without the project's quality gates. A task graph or an available agent grants no
authority.

## 15. Lessons from the first adoptions

Generalized patterns, not rules of any one repository.

1. **Merge can be a production operation.** In a GitOps repository, merge to the
   default branch is what the controller applies, and an infrastructure-as-code path
   may auto-apply. Classify merge as a mutation, keep a merge-impact map, and require
   an impact statement and rollback before merging. Plan approval is not merge
   consent.
2. **Build publishing documentation in the PR.** If merge publishes a site, run the
   strict build during PR validation. Finding a dead navigation entry after merge
   means finding it on the production path.
3. **Generated harness mirrors need deterministic sync and drift tests.** A mirror is
   safe only if the generator is reproducible and CI fails on any difference.
4. **Unavailable platform or native tests stay NOT RUN.** A missing runner, a
   platform you cannot reach, an install you were not approved to perform, or a
   skipped native test is NOT RUN with a reason. CI may supply the evidence; local
   expectation does not.
5. **No standing authorization.** Approval to implement is not approval to push, open
   a PR, merge, tag, publish or mutate an external system. Each is its own
   instruction, and approval for one does not carry to the next.
6. **Pin what you consume, and verify how.** Link to a tag or commit of the shared
   workflow. Pinning mechanisms differ by harness and version (one harness accepted a
   commit pin while another did not at the time of the adoption); probe, record, and
   fall back to a lock plus a drift check when a harness cannot pin.
7. **Hooks are per clone.** Git hooks installed in one clone do not exist in a fresh
   one; verify they run from linked worktrees, and document the one-time install.
8. **Harness facts do not belong in repository rules.** Statements such as "blocked
   by the assistant's permissions" describe a harness, not the repository. Move them
   to the adapter or delete them.
9. **Memory is not policy.** Anything an agent must obey lives in a committed file.
10. **Instructions deserve tests, and tests deserve a failing case.** Include a
    negative test for each instruction check.
11. **Disclose enforcement honestly.** Where a harness lacks a hook, say the
    protection is a procedure, not a guard.
12. **Do not copy the workflow.** Every restatement of lifecycle, profiles or
    topologies becomes a conflict later. Link to the pinned contract.

## 16. Adoption checklist

Copy this list into the adoption plan and tick items only with evidence. An item
that was not executed stays unticked and is recorded as NOT RUN in section E.

### A. Audit

- [ ] Fetched; recorded the default branch and base SHA.
- [ ] Primary checkout is clean and untouched; work is in a linked worktree.
- [ ] Inventoried instruction files and what each harness sees today.
- [ ] Marked harness-specific rules and optional-provider dependencies.
- [ ] Listed existing enforcement: hooks, CI, harness permission files, branch
      protection (with date and source).
- [ ] Built the merge-impact map (paths with automatic effects).
- [ ] Listed plan locations, formats, indexes and archive.
- [ ] Listed skills locations and current discovery.
- [ ] Listed validation commands and which can fail.
- [ ] Recorded tool versions available; marked absent tools.
- [ ] Recorded supported platforms.

### B. Decisions

- [ ] Repository risk class and recommended depth for the adoption (section 2).
- [ ] Harnesses in scope, verified or placeholder.
- [ ] Pinned reference of `claude-plugins`, and the bump procedure.
- [ ] Adapter strategy per artifact: symlink, mirror or adapter file (section 6).
- [ ] Plan location and format; archive procedure.
- [ ] Action classes, defaults and the consent templates.
- [ ] Validation matrix rows.
- [ ] Rollout PR sequence and who decides each delivery step.
- [ ] Whether any optional orchestration is out of scope (default: out of scope).

### C. Implementation

- [ ] `AGENTS.md` written; no copy of the workflow definitions.
- [ ] Thin adapters added; placeholders for unverified harnesses.
- [ ] Preflight and enforcement layers added as decided.
- [ ] Permission policy and, if applicable, generated harness permission files.
- [ ] Skills canonical location and strategy implemented, with generator if a mirror.
- [ ] Plan convention, index, check script and archive notes.
- [ ] Validation matrix and PR template Validation and Impact sections.
- [ ] CI jobs from section 11 added, with actions pinned to full SHAs.
- [ ] Contributor page written and linked to the pinned guide.

### D. Verification

- [ ] Probes P1 to P8 recorded as PASS, FAIL or NOT RUN with evidence.
- [ ] Instruction, adapter, no-copy, link, plan, mirror and scan checks pass locally
      or are recorded NOT RUN with reasons.
- [ ] Each CI job has a negative test.
- [ ] Docs build (if merge publishes) runs on the PR.
- [ ] Same behavior across harnesses for: worktree, secrets, mutation consent,
      default-branch push.
- [ ] Rollback of each PR rehearsed or reasoned and written down.
- [ ] Working tree is clean after the test suite.

### E. Unresolved items and NOT RUN

- [ ] Every NOT RUN has a reason and an owner for resolving it.
- [ ] Open decisions listed with a recommendation.
- [ ] Follow-ups listed (platform coverage, native probes, branch-protection options).
- [ ] No claim of full conformance beyond the recorded evidence.

## 17. Templates

These extend the packaged [plan](../../plugins/development-lifecycle/resources/workflow/plan.md)
and [tasks](../../plugins/development-lifecycle/resources/workflow/tasks.md)
resources, which remain the source for resume-state semantics, evidence rules and
authority handling. They add front matter and the task fields an adoption plan
needs. Persist profile and topology in lowercase; for allowed values and meaning
see the [contract](../../plugins/development-lifecycle/rules/common/workflow.md).
Replace every placeholder with an observed fact, or write `unknown`. Template values
grant no authority.

### 17.1 `plan.md` skeleton

```markdown
---
title: <plan title>
slug: <slug>
status: planned
profile: standard
topology: solo
owner: <current actor>
integrator: <actor, or not applicable with reason>
base_sha: <verified full SHA>
branch: <type>/<slug>
worktree: <absolute verified path>
workflow_ref: <pinned tag or SHA of the shared workflow>
created: <YYYY-MM-DD>
updated: <YYYY-MM-DD>
next_action: <exact bounded action or blocking prerequisite>
---

# <Plan title>

## Scope

- Objective: <problem and intended behavior>
- In scope: <exact files and boundaries>
- Out of scope: <excluded work and repositories>

## Dependencies

- Upstream: <pinned workflow reference, other PRs, tools, approvals, or none>
- Blocked by: <missing prerequisite, or none>

## Audit summary

<Findings with the command or file that produced each. Link evidence.md if long.>

## Decisions

| ID  | Decision | Alternatives | Status (proposed or accepted) | Revisit when |
| --- | -------- | ------------ | ----------------------------- | ------------ |
| D1  | <choice> | <options>    | proposed                      | <condition>  |

## Tests

| Check   | Command or method | Level | Expected result     |
| ------- | ----------------- | ----- | ------------------- |
| <check> | <command>         | L0    | <observable result> |

## Expected result

<What is true after the plan is complete, observable without chat history.>

## Acceptance criteria

- [ ] <observable criterion>
- [ ] <mandatory project gate>

## Rollout

<Ordered small PRs, each independently revertible; gates between them.>

## Rollback

<Exact reversible change and its checks. Runtime rollback needs separate authority.>

## Mutation consent

- Authority source: <current explicit instruction, or none>
- Delivery actions accepted: <commit, push, PR, merge, tag, separately, or none>
- Runtime or destructive impact: <description, or none>
- Fresh consent on record: <exact scope, or NOT AUTHORIZED>

## Evidence and status

| Check   | Revision, host, date      | Result  | Evidence or reason                |
| ------- | ------------------------- | ------- | --------------------------------- |
| <check> | <SHA, tool version, date> | NOT RUN | <why unavailable; what it blocks> |

Completed: <task IDs and results>. Blocked: <IDs and reasons>.
Risks: <uncertainty and mitigation>.
```

Required front matter: `title`, `slug`, `status`, `profile`, `topology`, `owner`,
`base_sha`, `branch`, `worktree`, `workflow_ref`, `updated`, `next_action`.
Suggested `status` values: `planned`, `in_progress`, `review`, `blocked`, `shipped`,
`dropped`. A repository plan check should enforce the required fields and match each
plan to its index row.

### 17.2 `tasks.md` skeleton

```markdown
---
plan: <slug>
updated: <YYYY-MM-DD>
---

# Tasks for <plan title>

## T01: <bounded outcome>

- Status: planned
- Scope: <repository-relative files to create or change; explicit exclusions>
- Depends on: <task IDs and external prerequisites, or none>
- Owner and integrator: <actor, branch and worktree; others unassigned unless authorized>
- Tests: <commands or methods; mandatory project gates>
- Expected result: <observable output or assertion for each test>
- Acceptance: <specific observable done condition and blocking gates>
- Rollback: <scoped reversal and validation; runtime authority is separate>
- Mutation consent: <none, or the exact action, target and effect that needs fresh consent>
- Actual evidence: <PASS, FAIL, NOT RUN or NOT APPLICABLE, with exit status, revision, host and date, or the reason>
- Risks: <remaining uncertainty and mitigation>
- Next action: <exact bounded step or missing prerequisite>

## T02: <bounded outcome>

- Status: planned
- Scope: <files>
- Depends on: T01
- Owner and integrator: <actor>
- Tests: <commands>
- Expected result: <assertion>
- Acceptance: <done condition>
- Rollback: <reversal>
- Mutation consent: none
- Actual evidence: NOT RUN (<reason>)
- Risks: <risk>
- Next action: <step>
```

Keep failed and unrun checks visible. Do not mark a task `complete` from a proposed
command or a checkbox. A task that records a decision or findings names the durable
file it writes; "Scope: none" means no file is changed. Do not widen scope silently;
record the reason for a change.

### 17.3 Probe record skeleton

```markdown
## Capability probes

| ID  | Harness and version | Date   | Method      | Result  | Evidence or reason |
| --- | ------------------- | ------ | ----------- | ------- | ------------------ |
| P1  | <harness> <version> | <date> | <procedure> | NOT RUN | <reason>           |
```

## 18. References

- [Workflow contract](../../plugins/development-lifecycle/rules/common/workflow.md):
  lifecycle, profiles, topologies, defaults, authorization, safety, artifacts.
- [Compatibility and consumer strategy](compatibility.md): capability matrix,
  consumer follow-ups, release sequence, OpenCode manual path.
- [Specification](specification.md): background and rationale.
- [Verification record](verification.md) and [live-trial guide](live-trials.md):
  evidence conventions and trial templates.
- [Installation and maintenance](../codex.md): Claude and Codex installation.
- [Worktree workflow](../../plugins/git-workflows/rules/worktree-workflow.md): the
  invariant, layout and the Claude guard.
- Packaged resources: [plan](../../plugins/development-lifecycle/resources/workflow/plan.md),
  [tasks](../../plugins/development-lifecycle/resources/workflow/tasks.md),
  [handoff](../../plugins/development-lifecycle/resources/workflow/handoff.md),
  [decision](../../plugins/development-lifecycle/resources/workflow/decision.md).
