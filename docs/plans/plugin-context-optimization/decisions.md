# Context optimization decisions

The user authorized execution and PR preparation after reviewing the plan.
Decisions below were followed; retain branches and limitations are recorded in
[results.md](results.md). Original design alternatives remain for provenance. Authority remains in
[plan.md](plan.md), with exact conditional branches in [tasks.md](tasks.md).

## D01 — Preserve entrypoints, route optional detail

- Choice: existing SKILL.md core with common prerequisites and, where branches justify
  them, skill-local `references/*.md`; retain all
  names, descriptions except T09's exact metadata targets, and native adapters.
- Alternatives: delete examples (loses capability), add narrow new skills (grows
  catalog), always load a central reference (shifts rather than reduces context).
- Consequence: extra file selection must be useful. Core + selected topic must be
  cheaper than its former complete read, with essential constraints inline.
- Revisit: selectors grow so large or topic overlap so wide that no normal read
  improves. Retain the original skill when splitting would make it worse.

## D02 — Preserve review gates while separating responsibilities

- Choice: review owns scope/local procedure; common code-review rule owns shared
  policy; code-review owns local/PR transport and authorized publication;
  code-reviewer owns supplementary domain checks. Avoid cyclic mandatory reads.
- Current source differs on HIGH findings: some paths request changes while
  others warn. Inventory each mode's before/after behavior. Keep stronger or weaker
  existing behavior explicit for that mode; do not alter it through deduplication.
- Alternatives: standardize every HIGH to block or warn. These are policy changes,
  not context optimizations, and need a separately accepted decision.
- Consequence: if consolidation cannot preserve the modes clearly, consolidate
  only scope/format duplication and leave thresholds inline with an explanation.
- Revisit: user explicitly approves a uniform severity policy. Until then,
  ambiguous required-gate behavior blocks that part of T06, not independent work.

## D03 — Keep safety local and the repaired core intact

- Choice: keep workflow contract, worktree rule and hook/guard behavior unchanged;
  allow bounded same-revision reuse clarification in entrypoints only. Preserve
  complete first load and re-read when relevant context/revision/policy is lost.
- Standalone role/toolkit boundary compression is conditional on a complete
  semantic map and worthwhile reduction; no-change is a valid measured outcome.
- Alternatives: a new global safety file or mandatory cross-plugin loader adds
  dependencies and may cost more than repeated short paragraphs.
- Consequence: preserve existing exact safety declarations required by tests
  wherever possible; never weaken those tests just to accept smaller text.
- Revisit: objective host/read-set evidence supports a separately scoped core
  rewrite. This plan does not authorize it.

## D04 — Setup choices are additive, not automatic reconfiguration

- Choice: explicit core-plus-selected-domain installation guidance alongside the
  existing all-owner option. Preserve unspecified-request behavior; honor a
  current user's named subset. Describe choices in Markdown, not invented host
  flags. Installed/exposed count reductions are estimates until actually verified.
- Suggested core: development-lifecycle + git-workflows. Toolkit/security and
  domain owners are selected according to task; none becomes a new dependency.
- Alternatives: uninstall irrelevant plugins or change default user profiles.
  Those are not authorized and would remove previously available capability.
- Revisit: a later explicit profile/configuration task, with actual host evidence.

## D05 — Offline proof, honest context estimates

- Choice: fixed baseline hashes, content preservation, standalone link checks,
  per-topic read sets and exact catalog identities; rough estimator matches audit.
- No measured host/model tokens, cold-session loading or billing reduction is
  claimed. Static route scenarios are not model-behavior tests.
- Keep full-detail expansion cost visible: reference splitting can increase total
  bytes slightly while reducing normal reads. Report that tradeoff.
- Revisit: user authorizes actual usage measurements; do not launch models now.

## D06 — Cover all audit findings without rewriting every plugin

- C01: T03–T05. C02: T06. C03: T05/T07. C04: T08. C05: T09.
  C06: T02. C07: T11 and the shared authoring gate. T01/T10 provide cross-cutting
  evidence and final acceptance.
- Keep Android, narrow Renovate domain topics and existing small rules loaders
  intact except named corrections and T08's mapped auditor-boundary evaluation.
  Keep MCP/NestJS/Postgres examples unchanged; T11 may clarify their pointers or
  prose in place, but adds no new example destinations. Disk size alone is not
  a defect.
- Larger API/migration recipes are in T04; unchanged skills get a documented
  no-change disposition in T10 rather than disappearing from the scope.
- Revisit: measured tasks show an unchanged owner dominating context; propose
  that specific additional scope rather than silently extending this plan.

## D07 — Apply writing-for-agents across all skills without importing host mechanics

- Sources: [writing guide](https://github.com/mattpocock/skills/blob/main/skills/productivity/writing-for-agents/SKILL.md)
  and [mechanics](https://github.com/mattpocock/skills/blob/main/skills/productivity/writing-for-agents/SKILL-MECHANICS.md),
  with observed blob IDs in [writing-assessment.json](writing-assessment.json).
- Choice: evaluate all 70 skills for pointer branches, information order,
  co-location, completion bounds, duplication, environment caches and wording.
  Use the same rules for the plan and task outputs. Preserve material shared by
  every branch inline, including legitimate flat reference/checklists.
- Consequence: proposed reference filenames are allowable destinations, not a
  requirement to create every file. T11 may improve source within its explicit
  scopes or retain it with rationale. Necessary safety repetition is not removed
  mechanically in pursuit of a single shared file or assumed model default.
- Host mechanics: the repository currently allows only name, description and
  metadata in shared skill frontmatter (`tests/test_codex_manifests.py`). Keep
  that supported surface. A manual-only flag, changed invocation eligibility or
  router skill would need separate verified per-host design and identity scope.
- Revisit: actual measured retrieval failures or a later verified host capability
  justify a different pointer, inline placement or explicit invocation decision.
  No external skill is installed or added as a runtime dependency.
