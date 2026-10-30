# Plugin context audit — 2026-10-30

The best first optimization is to make example-heavy skills load their relevant
examples on demand. Keep the campaign's repaired entrypoints and safety boundaries.
Do not start by replacing the complete workflow contract with a summary, deleting
roles or introducing another global instruction layer.

## Scope and evidence

Static inventory of **all 12 plugins: 171 tracked files, 70 canonical skills,
29 rules, four resources, 10 agent adapters, 13 command adapters and 24 manifests**.
Source is `d82efc568f29c3b6dbd7f1ded7726474820d0a3a`, the published PR #37
head. GitHub verified that PR merged as
`ae10c049c4e0d1667d7544199a980854d96794c3`. This audit uses the pinned PR
head without updating primary or previous worktrees.

[Inventory](inventory.json) contains every file's hash, bytes, characters, rough
body estimate, metadata and links. [Measurement script](measure.py) reproduces it:

```sh
python3 -B docs/audits/plugin-context/measure.py --output /tmp/plugin-context-current.json
```

All plugin files were scanned structurally. Manual review focused on loading
entrypoints, descriptions, rule selectors, repeated paragraphs, example-heavy
skills and cross-plugin workflow overlap. This is not a line-by-line correctness
review of every domain example. External framework APIs and sibling repository
conventions were not revalidated. No private/home configuration, live host/model,
new actor, installation, plugin edit or runtime change was used.

Procedure: the collection's existing `context-budget` skill. Exact counts are
UTF-8 bytes/characters. Token estimates use prose words × 1.3 plus fenced-example
characters / 4; a second characters / 4 proxy illustrates uncertainty where
helpful. **No matching tokenizer, host context counter, billing or measured
per-session token usage was available.** Estimates are neither limits nor a
remaining-context percentage. A skill filename is not proof that it is loaded.

## What contributes context

| Surface | Measured source size | Loading interpretation |
| --- | --- | --- |
| All 70 skill names/descriptions | 11,380 characters / 1,388 words; roughly 1,804 prose-estimate tokens before host formatting | Potential catalog metadata when all are exposed. Actual formatting, selection and native agent catalog overhead are unknown. |
| All SKILL.md files | 424,315 bytes including frontmatter | On-demand source, not a fresh-session charge. Do not claim 424 KB is always loaded. |
| Claude git-workflows startup rule + current preamble | 6,016 bytes / 6,006 characters / 913 words; roughly 1.2–1.5k tokens | Injected in a Git repository when the configured SessionStart hook succeeds. Missing jq/git/errors can yield no context. Disabled-hook note adds text. Codex has no equivalent bundled injection. |
| Required workflow contract | 18,924 bytes / 18,912 characters; roughly 3.5–4.7k tokens | Complete first-use load is explicit for lifecycle entrypoints. Already-loaded, still-available content is not a new file read by definition; actual rereads were not measured. |
| Spec + workflow contract | 22,992 source characters, including Spec frontmatter | One plausible first-use read set, not a startup measurement. Git/project policy may add context. |
| Reviewer + review + common-review rule + workflow contract | 42,093 source characters; roughly 8.0–10.5k tokens | Conditional linked read set if all four bodies are loaded. The role and procedure cross-link; not every invocation necessarily loads the whole set. |
| Native command/agent adapters | 23 thin files; Claude command wrappers attach canonical source, agent adapters link to it | Existing adapters are already thin. Do not count full role bodies twice as baseline merely because both native and skill entrypoints exist. |
| Tool schemas and other plugins/configuration | Unknown in actual user sessions | No supplied plugin manifest declares mcpServers. That does not prove external tools are absent or cost zero. Those schemas and private host settings are outside this source audit. |

The most useful distinction is **baseline catalog/startup overhead versus the
incremental cost of selecting a skill**. Most proposed savings below are the
second kind. They cannot be added up as a per-session saving or billing claim.

## Every plugin, with a disposition

Skill bytes include frontmatter; rule bytes are separate. KB here means decimal
1,000 bytes, rounded. Android is a placeholder, not a missing audit entry.

| Plugin | Skills | Skill KB | Rule KB | Context disposition |
| --- | ---: | ---: | ---: | --- |
| development-lifecycle | 22 | 133.5 | 36.4 | Biggest owner. Simplify review routing; move examples/templates from selected leaf skills. Keep repaired contract and loading gates. |
| agent-toolkit | 14 | 79.0 | 0 | Trim meta-workflow diagrams/example transcripts; make rules-distill retrieval scoped. Keep standalone boundaries. |
| backend | 8 | 69.2 | 0 | Split broad pattern/API/migration examples by topic or stack; keep applicability and safe migration principles inline. |
| git-workflows | 5 | 23.7 | 12.4 | Startup text matters more than disk total. Preserve #36's preamble, guard behavior and current pre-write requirements. Defer rule compression. |
| dotnet | 4 | 23.5 | 6.7 | Extract optional C#/test examples; retain cancellation, disposal, security and project-policy checks inline. |
| frontend | 4 | 20.2 | 18.3 | First candidate for example extraction. Give TS/Web rule links distinct labels and task selectors. |
| devcontainer | 4 | 19.6 | 0 | Pipeline and secret-injection examples can be references; keep secret handling and runtime/configuration authority visible. Domain-specific patterns should not become global defaults. |
| devops | 2 | 19.3 | 0 | Move deployment/Docker recipes to topic references; keep impact, prerequisites and rollback inline. |
| renovate | 4 | 18.7 | 0 | Already narrow topics. Keep datasource/preset distinctions; improve exact-name links before splitting further. |
| security | 2 | 15.6 | 0 | Retain checklists; move implementation samples behind topic links. Existing cloud reference needs a real conditional link, not a new skill identity. |
| personal-essentials | 1 | 2.1 | 0 | Optional task/domain installation guidance can reduce irrelevant catalog exposure; no automatic uninstall/configuration change. |
| android | 0 | 0 | 0 | Leave placeholder alone; no current skill-body savings. |

## Prioritized findings

### C01 — Extract examples from broad leaf skills first (high value, lower risk)

The frontend-patterns body is 14,599 characters, with **13,023 fenced-example
characters (89%)**. backend-patterns is 13,638 body characters, with **12,039
fenced-example characters (88%)**. A small UI or API task currently opens a large
collection of examples spanning unrelated techniques.

Keep the same SKILL.md name/description and a concise applicability checklist,
selection table and essential constraints. Identify shared versus conditional
branches before splitting; code percentage alone is not sufficient. Move only
branch-specific complete examples to plugin-local
`references/` files, grouped by actual topic. Example frontend routing:
`components.md`, `state-and-data.md`, `forms-and-accessibility.md`,
`performance.md`. Load only the matching reference; do not read all references
because the skill was selected. Expand when imports/callers or uncertainty require it.
Do not create extra SKILL.md files: references should add zero catalog entries.

Good follow-on targets: dotnet-patterns, csharp-testing, docker-patterns and
deployment-patterns. Across these six skills, **53,285 fenced-example characters**
could be placed behind conditional links: a rough **13.3k-token upper bound**
across six separate complete activations if none of those examples were needed.
This is a source-content bound, not a promised saving; selected references and new
routing text subtract from it. No content should be discarded to achieve a quota.

### C02 — Break the review loading cycle (high value, moderate risk)

`development-lifecycle/skills/review/SKILL.md` links to the reviewer role;
`skills/code-reviewer/SKILL.md` links back to review scope selection. Both include
review checklists and link common review policy; `code-review` adds local/PR
transport and another checklist/report shape. Correctness, security, scope and
severity content overlaps across these entrypoints.

Assign responsibilities without deleting existing names: `review` owns scope and
local procedure; common review policy owns severity/gates; `code-review` owns PR
fetch/publication transport; `code-reviewer` owns optional domain checks. Replace
whole-file cross-loading for scope selection with a small plugin-local scope
resource only if that avoids a real repeated read. Do not add a new resource
merely to move the same cost. Clarify when an already fully loaded contract at
the same installed revision can be reused while still in context; re-read after
loss/compaction or a relevant revision/policy change. Never replace the required
first complete load with a head excerpt.

Preserve review-only/fix/publication distinctions and current staged/unstaged/
untracked scope. Reconcile existing gate semantics explicitly before deduplicating;
shortening must not silently change a HIGH finding from a blocker to a warning.

### C03 — Reduce meta-workflow overhead (medium value, lower risk)

`agent-toolkit/skills/rules-distill/SKILL.md` is 12,575 bytes. It says to send full
relevant rules for each thematic batch and rules are small enough to avoid grep
prefiltering. Repeating a whole rule corpus across batches can exceed the cost
of the skill itself. Its example transcript/schema also takes substantial space.
`iterative-retrieval`, `search-first`, `eval-harness` and lifecycle `aside` contain
large diagrams, examples or repeated report formats.

Keep bounded executable instructions inline; put lengthy worked examples/schemas
in references. For distillation, inventory the complete corpus, shortlist possible
matches by headings/terms, then read full relevant sections and neighboring
constraints before deciding. Expand to the full file when necessary; never treat
an unmatched search as proof a principle is absent. Preserve cross-batch evidence
and standalone/local fallback. Do not add rules merely because two skills repeat
something; assess whether on-demand skill guidance is the right location first.

### C04 — Compress boundary repetition carefully (medium value, higher risk)

One 574-character normalized standalone-role paragraph appears in 10 skills;
source duplication beyond the first copy is 5,166 characters. Two toolkit boundary
paragraphs (446 and 554 normalized characters) each appear eight times, adding
7,000 redundant source characters beyond their first copies. The inventory gives
exact paths. These figures describe duplication on disk, not tokens every session.

Some repetition is intentional: each owner must work alone, and direct entry
must retain authority, project-policy, model/tool limits and no-bypass boundaries.
Prefer a shorter self-contained inline boundary where semantics can be mapped
one-for-one. A mandatory shared-file read can cost more than the paragraph it
replaces; a cross-plugin dependency would break standalone behavior. Keep this
behind leaf/example work and require an invariant map before any edits.

### C05 — Improve catalog precision and optional installation scope (modest baseline value)

Descriptions like `verification-loop`'s “A comprehensive verification system” and
`update-docs`/`update-codemaps`' “Use the ... workflow” provide poor task selection.
`workspace-surface-audit` has the longest description and a wide remit. Improve
trigger/non-trigger precision instead of shortening all descriptions uniformly.
The whole 70-skill name/description source is only about 1.8k estimated tokens
before host formatting, so descriptor edits are unlikely to be the largest win.

`personal-setup` installs ten plugin owners for the selected host. Offer optional
core-plus-selected-domain guidance while preserving the existing explicit
all-plugin option. Installed/exposed status must be verified before claiming
catalog savings. Do not disable/uninstall anything or change user/global profiles
as an audit side effect. Retain stable IDs, native metadata and Codex alias opt-outs.

### C06 — Use precise rule/reference routing (small cost, useful clarity)

`frontend-rules` lists both TypeScript and Web files with duplicate labels such
as coding-style/testing/security. Label them by domain and state when to read
one versus both. The existing “read only relevant rules” approach is already good;
do not flatten all 12 into an unconditional load.

`security-review/cloud-infrastructure-security.md` is an existing 10,171-byte
reference, not one of the 70 discovered skills. Its table advertises a skill-like
name, but the parent security-review body does not link to it. Add a conditional
cloud/CI/IAM reference route rather than introducing another skill/catalog entry.
Use the canonical `devcontainer-ghcr-image-pipeline` name in devcontainer README
and pinning guidance instead of a shortened nonmatching skill name.

## C07 — Apply agent-writing guidance across all skills and the plan

The user supplied [writing-for-agents](https://github.com/mattpocock/skills/blob/main/skills/productivity/writing-for-agents/SKILL.md)
and its [skill mechanics](https://github.com/mattpocock/skills/blob/main/skills/productivity/writing-for-agents/SKILL-MECHANICS.md).
The [plan](../../plans/plugin-context-optimization/plan.md) now applies their
writing criteria to every audited skill, not just the largest files. The
[70-skill matrix](../../plans/plugin-context-optimization/writing-assessment.json)
records source identities/hashes and proposed review assignments; it is not a
claim that every existing step has already been rewritten or behaviorally tested.

This refines C01–C06: decide splits by actual branches and information order,
make pointer triggers precise, co-locate constraints/caveats, and make completion
criteria observable and exhaustive. Keep common material inline and retain useful
flat checklists. Review duplication and environment-derived facts before trimming.
Prefer direct positive actions while keeping necessary safety/consent exclusions.
A suspected default/no-op is not safe to delete solely on author intuition.

The external guide's invocation flag and visibility claims are not treated as
verified cross-host behavior. Current shared frontmatter tests allow name,
description and metadata only; keep that surface and existing discovery. No
manual-only conversion, new router skill, external runtime dependency or host
configuration change is included. A separate supported-host design would be
needed before using host-specific flags to reduce catalog exposure.

The implementation plan now has 11 tasks: T11 reviews all 70 skill identities
before T10's final integration. Its shared authoring gate applies to the plan and
all future task outputs too. Existing fixed campaign semantics remain protected.

## Campaign repairs to retain

PR #20's Codex command-import opt-outs already prevent duplicate command aliases.
PR #22's rooted native attachments and complete first-load behavior already fix
headless discovery. #23 keeps runner status meaningful. #28–31 address unresolved
preflight/current actor state and accept unambiguous facts without extra narration.
#32/#33 provide actual installed locators and command forms. #34's CLAUDE.md pointer
was deliberately removed by #35 after native AGENTS.md loading was demonstrated.
#36 corrects startup wording. These are completed fixes, not new audit tasks.

Preserve standalone owners and optional providers, named actor authority,
worktree-first/current state, policy conflicts, NOT RUN honesty, stage/delivery/
runtime gates and separate DEEP draft review. Do not infer actual loaded policy
from explicit Read events alone. Do not alter guard fail-open behavior or model
choice while optimizing text. Do not solve context cost by fetching/installing
another service or introducing a global always-loaded copy of the contract.

## Proposed first implementation slice

Start with **frontend-patterns and backend-patterns only**: two existing skill
entrypoints plus plugin-local reference files and relevant packaging/link checks.
Preserve examples and task semantics, keep IDs/descriptions stable, and update
paired versions only for changed plugins. Target useful topic selection rather
than a file-length limit. This isolates the expected large savings from lifecycle
safety changes and avoids refactoring every owner at once.

Offline acceptance: all prior content accounted for in core/reference mapping;
local links/fragments resolve from a standalone plugin install path; exact skill
identities stay at 70 with no generated aliases/new provider dependency; manifests
and relevant static tests pass. Compare the before/after initial core read and
representative single-topic read (core plus that reference), reporting exact
characters and the same rough estimator. A split that immediately reads every
reference has no demonstrated benefit. Do not repeat live campaign tests or launch
new actors for this change; runtime compliance remains unmeasured without a later
explicit grant. No implementation is performed by this audit.

## Status

Validation: all 171 plugin-source hashes match the pinned revision; inventory
totals, local report links and whitespace pass. The measurement script runs
offline and records whether plugin source is dirty. No production tests or native
metadata/model trials were needed for this report-only audit.

Audit baseline is retained unchanged in inventory.json. The user subsequently
authorized execution and PR preparation; see the [implementation outcome](../../plans/plugin-context-optimization/results.md)
for measured read sets, all-skill dispositions, preserved constraints and offline
verification. The earlier audit sections describe the baseline, not final source.
