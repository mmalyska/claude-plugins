# Implementation tasks

All 11 tasks are **complete**, including documented no-change dispositions.
The user authorized execution and PR preparation. Dependencies remained serial
within SOLO; no other actor was launched. Original task instructions below are
the execution scope; actual results are in [results.md](results.md). [Plan](plan.md) and [decisions](decisions.md) define authority and design.

## Shared task contract

Owner/integrator: current operator, branch/worktree from plan.md; reverify current
Git/primary/base/isolation before any implementation write. Each task may update
its named output and its own task evidence/status after implementation is granted.
Existing user changes and previous campaign archives are excluded from every task.

For each task record actual files changed, old/new hashes, content/reference map,
commands/results, read-set costs and caveats in its evidence output. No field may
claim PASS from a proposed command. Preserve failed/unrun gates. Rollback means a
reviewed restoration patch for that task's source/references/checks and paired
versions, preserving other tasks; no reset, stash, destructive cleanup or delivery.

For each plugin actually changed by a task, paired metadata scope is exactly
`plugins/<that-owner>/.claude-plugin/plugin.json` and
`plugins/<that-owner>/.codex-plugin/plugin.json`: synchronized patch version only,
except no other manifest behavior may change. Apply once per completed unpublished
slice. Owner sets are listed below; do not bump unrelated plugins.

Common check support, only where needed: `tests/test_context_layout.py` and
`tests/fixtures/context-layout/manifest.json` from T01. Existing exact identities,
native metadata and Codex opt-outs remain frozen. `tests/test_workflow_contract.py`
may change only for T06/T08's explicitly described invariant-preserving refactor;
no wholesale snapshot refresh to make edits pass.

## Shared authoring gate — every touched skill and plan artifact

Apply the writing guidance in [plan.md](plan.md). Classify ordered steps and
reference, identify branches, and justify every external pointer with its trigger.
Keep common prerequisites inline and co-locate caveats. Completion means the
stated evidence covers every applicable item; a named output file alone is not
proof of completion. Preserve legitimate flat checklists. Record any environment
cache or possible no-op removed and why; uncertain model defaults are not proof.
Draft positive target actions while preserving explicit consent/safety exclusions.
Reference paths proposed below are permitted destinations, not mandatory splits.

## T01 — Baseline, invariant map and offline proof tools

Status: complete; see the named evidence output and [outcome](results.md).

- Finding: all C01–C07; prerequisite for any plugin changes.
- Dependencies: none. Owners changed: none.
- Exact files: `docs/audits/plugin-context/measure.py` (add output selection);
  new `tests/test_context_layout.py`,
  `tests/fixtures/context-layout/manifest.json`;
  new plan outputs `baseline.json`, `invariants.md`, `evidence/T01.md`;
  update the existing `writing-assessment.json` with baseline branch/invocation
  classification for each of the 70 identities before plugin edits.
- Change: preserve audit inventory as immutable input. Support `--output <path>`
  for after-inventory. Define source sections/example hashes, destination ownership,
  required inline constraints and per-topic read sets. Capture baseline paired
  versions and catalog/adapter identities. Do not embed a second runtime catalog.
- Invariant map: standalone use; complete first contract read; current Git/policy
  before writes; no actor/model/tool bypass; explicit scope/reuse; profile/topology;
  stage/delivery/runtime limits; required-gate truth; DEEP draft review; provenance.
- Checks: deterministic repeat inventory without changing baseline; JSON/schema
  validation; layout checker rejects missing/escaping links, unaccounted content,
  accidental new skills and a declared single-topic read set that unnecessarily
  reads everything. Explicit full-detail requests remain valid.
  Use real copied plugin directories with spaces; no host process or service.
- Expected/done: baseline covers 171 files/12 plugins/70 skills/23 adapters, with
  traceable hashes and meaningful negative checks. Only after this passes may T02
  change plugin source. Rollback: restore measure.py; retain evidence and do not
  remove fixtures/artifacts without ownership and applicable scope.
- Next: implement proof tools when implementation is granted.

## T02 — Correct task-specific rule and reference routing

Status: complete; see the named evidence output and [outcome](results.md).

- Finding: C06. Dependency: T01. Owners: frontend, security, devcontainer.
- Exact files: `plugins/frontend/skills/frontend-rules/SKILL.md`;
  `plugins/security/skills/security-review/SKILL.md`;
  `plugins/security/skills/security-review/cloud-infrastructure-security.md`;
  `plugins/devcontainer/README.md`;
  `plugins/devcontainer/skills/devcontainer-renovate-digest-pinning/SKILL.md`;
  plan output `evidence/T02.md`.
- Change: label TypeScript/Web selectors distinctly; state when one/both apply.
  Link cloud reference conditionally from security-review and replace its
  misleading skill-like table with reference metadata/prose. Correct shortened
  ghcr-image-pipeline references to the existing canonical identity/local link.
  Do not change any deployment/auth configuration or domain example behavior.
- Checks: selectors resolve exact files, local links work from standalone copies,
  no new skill ID, no unconditional all-rule load, unchanged examples/checklists.
- Expected/done: three unambiguous routes, unchanged capability and measured route
  sizes. Rollback: restore these five bodies/README and corresponding owner versions.
- Next: record routing checks before reference extraction uses these entrypoints.

## T03 — Pilot: frontend/backend pattern references

Status: complete; see the named evidence output and [outcome](results.md).

- Finding: C01. Dependencies: T01/T02. Owners: frontend, backend.
- Exact existing files: `plugins/frontend/skills/frontend-patterns/SKILL.md`,
  `plugins/backend/skills/backend-patterns/SKILL.md`.
- Exact new reference files under frontend-patterns:
  `references/components.md`, `references/state-and-data.md`,
  `references/forms-and-accessibility.md`, `references/performance.md`.
- Exact new reference files under backend-patterns:
  `references/layers-and-middleware.md`, `references/data-and-caching.md`,
  `references/auth-and-rate-limits.md`, `references/jobs-errors-and-logging.md`.
- Outputs: `evidence/T03.md`, `read-sets/T03.json` in this plan directory.
- Change: preserve names/descriptions, examples and relevant constraints. Identify
  branches before choosing splits; keep shared principles and required examples
  inline, with precise conditional pointers. No automatic reference sweep.
- Checks: all original sections/examples mapped, standalone links/fragments,
  catalog/manifest tests; compare old full skill versus new core-only and
  core+components or core+layers read sets. Also report full expansion cost.
- Expected/done for a split: both representative single-topic reads are smaller,
  identities unchanged, no content loss and each disclosure follows a real branch.
  If not justified, retain source and record no-change; that completes the pilot
  assessment but does not satisfy T04/T05's prerequisite of a proven split.
  Revise the strategy before extending it. Rollback: restore both skills and versions;
  new references are task-owned but removal still requires applicable scope.
- Next: review pilot evidence, then proceed to T04/T05.

## T04 — Domain example libraries beyond the pilot

Status: complete; see the named evidence output and [outcome](results.md).

- Finding: C01. Dependencies: T03 accepted read-set/content proof.
- Owners: backend, dotnet, devops, devcontainer, security.
- Exact existing SKILL.md files, relative to `plugins/`:
  `backend/skills/api-design/SKILL.md`,
  `backend/skills/database-migrations/SKILL.md`,
  `dotnet/skills/dotnet-patterns/SKILL.md`,
  `dotnet/skills/csharp-testing/SKILL.md`,
  `devops/skills/docker-patterns/SKILL.md`,
  `devops/skills/deployment-patterns/SKILL.md`,
  `devcontainer/skills/devcontainer-ghcr-image-pipeline/SKILL.md`,
  `devcontainer/skills/devcontainer-secrets-injection/SKILL.md`,
  `security/skills/security-review/SKILL.md` (retain T02 routing).
- New references beneath each respective skill directory:

  | Skill | Exact `references/` filenames |
  | --- | --- |
  | api-design | `http-contracts.md`, `pagination-and-query.md`, `implementation-examples.md` |
  | database-migrations | `postgresql.md`, `orms-typescript.md`, `orms-python-go.md`, `expand-contract.md` |
  | dotnet-patterns | `language-and-async.md`, `application-and-data.md` |
  | csharp-testing | `unit-and-mocking.md`, `integration-and-fixtures.md` |
  | docker-patterns | `images-and-compose.md`, `networking-and-operations.md` |
  | deployment-patterns | `ci-and-release.md`, `health-and-rollback.md` |
  | devcontainer-ghcr-image-pipeline | `publish-workflow.md` |
  | devcontainer-secrets-injection | `local-codespaces-examples.md` |
  | security-review | `application-security-examples.md` |

- Outputs: `evidence/T04.md`, `read-sets/T04.json`.
- Change: select by actual topic/stack. Keep migration constraints, rollback,
  secret handling, cancellation/disposal and authorization prerequisites inline.
  Keep cloud reference distinct. Do not silently update third-party examples or
  change project requirements during relocation.
- Checks: content maps; selected stack/topic plus core costs; links/identities;
  original domain reviewer suffix hashes remain unchanged (these roles are not
  edited here). Run appropriate static suites.
- Expected/done: each proposed split improves its named normal read, or records
  no-change with measured rationale. Every original example accounted for.
  Rollback: per-owner source/reference/version patch, not whole-worktree reset.
- Next: report per-skill results, not a single inflated aggregate token saving.

## T05 — Lifecycle example/template references

Status: complete; see the named evidence output and [outcome](results.md).

- Findings: C01/C03. Dependency: T03. Owner: development-lifecycle.
- Exact existing files under `plugins/development-lifecycle/skills/`:
  `ai-regression-testing/SKILL.md`, `e2e-testing/SKILL.md`,
  `architecture-decision-records/SKILL.md`, `aside/SKILL.md`.
- New references under those same skill directories respectively:
  `references/regression-examples.md`, `references/playwright-examples.md`,
  `references/adr-template-and-examples.md`, `references/aside-examples.md`.
- Outputs: `evidence/T05.md`, `read-sets/T05.json`.
- Change: inline procedure/selection and essential permission boundaries; retain
  established artifact paths, ADR alternatives/status/revisit semantics, honest
  regression evidence and the no-write aside boundary. No new duplicate test,
  planning or reviewer skill. Do not edit workflow.md or its portable templates.
- Checks: template/section preservation, links, selector read sets, existing
  workflow/manifest static tests. Keep references conditional.
- Expected/done: measurable normal reads improve, no lost template field/behavior;
  otherwise a justified no-change disposition. Rollback per moved content/version.
- Next: provide stable lifecycle references before T06 touches review routing.

## T06 — Review policy/procedure/transport/domain ownership

Status: complete; see the named evidence output and [outcome](results.md).

- Finding: C02. Dependencies: T01/T05 and D02 mode-semantics map.
- Owner: development-lifecycle.
- Exact source files: `plugins/development-lifecycle/skills/review/SKILL.md`,
  `plugins/development-lifecycle/skills/code-review/SKILL.md`,
  `plugins/development-lifecycle/skills/code-reviewer/SKILL.md`,
  `plugins/development-lifecycle/rules/common/code-review.md`;
  new `plugins/development-lifecycle/skills/code-reviewer/references/domain-checks.md`;
  `tests/test_workflow_contract.py` only for maintaining equivalent review-scope,
  delivery and policy assertions after ownership moves.
- Conditional exact file: new
  `plugins/development-lifecycle/resources/workflow/review-scope.md` only if
  `decisions.md` records a smaller real read set than using bounded inline scope
  instructions. If not useful, do not create it. Both branches are scoped here.
- Outputs: `evidence/T06.md`, `read-sets/T06.json`, D02 rationale update.
- Change: remove mandatory review↔reviewer load cycle; use common policy once;
  route optional domain checks. Clarify reuse of a fully read, same-source contract
  that remains in context; keep complete first load and reload on relevant loss.
- Checks: explicit/staged/unstaged/untracked/clean-base target cases; local review
  versus PR transport; local fix versus external publication permissions; severity
  mode map unchanged. Existing assertion relocation must retain deletion/negative
  checks, not remove guarantees. Native adapter bodies/metadata unchanged.
- Expected/done: both local and PR review read sets are smaller without missing
  policy/domain detail. If severity consolidation is ambiguous, retain inline
  mode thresholds and consolidate only scope/format; request a separate policy
  decision before changing thresholds. Rollback entire scope/policy slice together.
- Next: record exact policy ownership/read sets for T08 boundary evaluation.

## T07 — Meta-workflow retrieval and worked examples

Status: complete; see the named evidence output and [outcome](results.md).

- Finding: C03. Dependencies: T01/T05. Owner: agent-toolkit.
- Exact source files under `plugins/agent-toolkit/skills/`:
  `rules-distill/SKILL.md`, `iterative-retrieval/SKILL.md`,
  `search-first/SKILL.md`, `eval-harness/SKILL.md`.
- Exact new references under those respective directories:
  `references/verdict-schema-and-examples.md`,
  `references/retrieval-examples.md`, `references/search-examples.md`,
  `references/eval-examples.md`.
- Outputs: `evidence/T07.md`, `read-sets/T07.json`.
- Change: keep bounded instructions and substantive criteria inline; move lengthy
  diagrams/transcripts. Distillation inventories all rules, shortlists likely
  matches, then reads full relevant sections/neighboring constraints and expands
  when needed. A failed search is not proof a principle is absent. Preserve
  cross-batch evidence, NOT RUN limits and local/standalone fallback.
- Checks: static read-set case with a match plus one requiring broader expansion;
  preserve schemas/grader/stop criteria; no spawned retrieval agent or invented
  tool. Do not change repeated boundary paragraphs until T08.
- Expected/done: lower ordinary read cost, exhaustive inventory still accounted
  for, examples available. Rollback procedure and worked references as one slice.
- Next: establish compact core before assessing boundary savings.

## T08 — Evaluate and selectively compress repeated boundaries

Status: complete; see the named evidence output and [outcome](results.md).

- Finding: C04. Dependencies: T06/T07. Owners: agent-toolkit, backend,
  devcontainer, development-lifecycle, dotnet, renovate, only if actually changed.
- Exact 10 role SKILL.md targets under `plugins/`:
  `backend/skills/database-reviewer/SKILL.md`,
  `devcontainer/skills/devcontainer-auditor/SKILL.md`,
  `development-lifecycle/skills/architect/SKILL.md`,
  `development-lifecycle/skills/build-error-resolver/SKILL.md`,
  `development-lifecycle/skills/code-reviewer/SKILL.md`,
  `development-lifecycle/skills/doc-updater/SKILL.md`,
  `development-lifecycle/skills/docs-lookup/SKILL.md`,
  `development-lifecycle/skills/tdd-guide/SKILL.md`,
  `dotnet/skills/csharp-reviewer/SKILL.md`,
  `renovate/skills/renovate-auditor/SKILL.md`.
- Exact eight toolkit SKILL.md targets under `plugins/agent-toolkit/skills/`:
  `autonomous-agent-harness/SKILL.md`, `blueprint/SKILL.md`,
  `continuous-agent-loop/SKILL.md`, `iterative-retrieval/SKILL.md`,
  `rules-distill/SKILL.md`, `subagent-driven-development/SKILL.md`,
  `team-builder/SKILL.md`, `writing-skills/SKILL.md`.
- Test scope: `tests/test_workflow_contract.py` only if an equivalent shorter
  declaration needs matched invariant/deletion checks. Preserve native metadata,
  hook hashes, four frozen domain-checklist suffix hashes and all safety tests.
  Keep the existing suffix delimiter sentence intact where tests use it.
- Outputs: `evidence/T08.md`, `boundary-map.md`, `read-sets/T08.json`.
- Change: edit only mapped boundary paragraphs. Keep scope, actual actor authority,
  no bypass, configured model/tool limits, project-policy precedence/conflicts,
  mandatory gates, missing-capability disclosure and standalone use self-contained.
  No cross-plugin loader or new shared always-read file.
- Checks: every old invariant mapped to inline text and negative check; source
  review of ambiguities; source/read-set savings after any added links. No broad
  golden-hash refresh. Do not move unrelated domain checklists/examples here.
- Expected/done: compress only if all invariants remain and cost decreases with
  no extra mandatory read. Otherwise retain original wording and record why;
  no-change is completion of this evaluation, not a silently omitted fix.
  Rollback individual paragraphs/tests/versions together without affecting T06/T07.
- Next: report changed/retained owners before metadata/version finalization.

## T09 — Precise descriptions and additive setup choices

Status: complete; see the named evidence output and [outcome](results.md).

- Finding: C05. Dependencies: T02/T08. Owners: agent-toolkit,
  development-lifecycle, personal-essentials.
- Exact metadata targets: `plugins/agent-toolkit/skills/verification-loop/SKILL.md`,
  `plugins/agent-toolkit/skills/workspace-surface-audit/SKILL.md`,
  `plugins/development-lifecycle/skills/update-docs/SKILL.md`,
  `plugins/development-lifecycle/skills/update-codemaps/SKILL.md`;
  paired description fields only in
  `plugins/development-lifecycle/commands/update-docs.md` and
  `plugins/development-lifecycle/commands/update-codemaps.md`.
- Exact setup documentation: `plugins/personal-essentials/skills/personal-setup/SKILL.md`,
  `plugins/personal-essentials/README.md`, root `README.md`, `docs/codex.md`.
- Outputs: `evidence/T09.md`, `description-map.md`, `read-sets/T09.json`.
- Change: task-specific triggers instead of vague comprehensive/use-workflow
  wording. Keep canonical names and required safety description clauses. Offer
  core + explicitly chosen domain owners alongside existing all-owner commands;
  maintain unspecified-request behavior and host selection. Explain installed
  versus exposed uncertainty. Do not invent CLI flags or install/remove plugins.
- Checks: native/shared description equality, catalog unchanged; example setup
  subsets contain only requested owners, all-owner option still matches current
  supported list, Android remains placeholder, no provider dependency. Only
  static setup examples are checked; actual installs are NOT RUN.
- Expected/done: clearer selection with measured metadata size, no false baseline
  savings claim, no global/home configuration mutation. Rollback metadata and
  paired native descriptions together; preserve unrelated README content.
- Next: T10 integrates actual task dispositions.

## T11 — All-skill writing review and bounded editorial corrections

Status: complete; see the named evidence output and [outcome](results.md).

- Finding: C07; applies C01–C06 consistently. Dependencies: T01–T09.
- Exact skill scope: the 70 `source_path` entries in
  [writing-assessment.json](writing-assessment.json), each tied to its baseline
  hash. Review every entry, including narrow skills retained by earlier tasks.
  Completed earlier fixes are assessed against their new content, not overwritten.
- Metadata support: matching existing native command/agent description fields
  only when a skill description changes; derive the exact existing pair from the
  frozen 23-adapter mapping in `tests/test_codex_manifests.py`. Adapter bodies,
  names, tools/models and invocation/import behavior stay unchanged.
- Outputs: update `writing-assessment.json` with each keep/clarify/disclose result,
  rationale and resulting hashes; new `evidence/T11.md`, `read-sets/T11.json`.
- Permitted edits: description/pointer subjects and triggers, information order,
  step completion wording, co-location and redundant non-normative prose within those 70
  bodies. Further reference moves use only T03–T07's already named destinations;
  a new skill, destination, host flag or normative policy needs separate scope.
- Guardrails: preserve all C01–C06 invariants and T08's protected boundary/domain
  sections. Leave uncertain no-ops intact. Unify duplicate meaning within an
  owner where safe; standalone/direct-entry safety remains explicit. Preserve
  undisclosed reference when every branch needs it or a flat checklist is clearer.
- Checks: 70/70 completed dispositions; every revised pointer maps distinct
  branches to existing targets; every revised step has checkable, exhaustive done
  criteria; metadata/native equality and preserved identities. Reuse relevant
  T01–T09 evidence, rerunning only affected static/read-set checks after edits.
- Expected/done: no unaudited skill identity, no unsupported invocation mechanics,
  no unsubstantiated no-op deletion and no split justified solely by size. All
  changed/retained outcomes are explained. Rollback only this editorial delta,
  preserving earlier task fixes and evidence.
- Next: T10 final integration/review; no automatic publication.

## T10 — Integrate, measure, review and hand off

Status: complete; see the named evidence output and [outcome](results.md).

- Findings: C01–C07 final acceptance. Dependencies: T01–T09 and T11 complete or
  recorded criterion-based no-change; unresolved required gates block readiness.
- Exact outputs in this plan directory: `after.json`, `results.md`,
  `content-map.json`, `read-sets/final.json`, `implementation-review.md`,
  `handoff.md`; update task/decision status and
  `docs/audits/plugin-context/README.md` with results link, not altered baseline facts.
- Metadata reconciliation: paired plugin manifests only for actually changed
  owners, per shared task contract. No Android change. No new runtime procedure.
- Checks: run the three focused offline suites named in plan.md; include relevant
  additional static tests only after inspecting side effects. Check all relocated
  plugin-local links/fragments from standalone copies, versions, identity set,
  guard/workflow preservation, source/content maps and original archive hashes.
  Run installed Gitleaks on changed artifacts and whitespace checks.
- Read-set report: baseline → core-only → representative topic → full expansion,
  per skill/route. Distinguish source duplication from known startup payload and
  possible exposed metadata. Report unknown actual host/model tokens explicitly.
- All-skill authoring gate: T11's 70/70 dispositions account for pointer branches,
  common/conditional content, completion evidence and preserved safety. A claimed
  no-op without evidence is retained or explicitly marked uncertain.
- Separate local review: read the final actual changed artifacts and all task
  outputs; inspect content maps and missing branches. Record findings/corrections
  against the exact resulting hashes; it is not an independent reviewer claim.
- Expected/done: every audit finding accounted for, checks actually pass or
  honest blockers remain, no misleading context/compliance claim. No repeated live
  trials. Rollback: reviewed per-slice patch, preserving baseline/history/evidence.
- Next: present reviewable implementation and ask only for any separately missing
  commit/push/PR scope. Do not publish or clean up automatically.
