# Development Workflow

This file adds git responsibilities to the collection's shared engineering
lifecycle. When development-lifecycle is installed, read its existing
`development-lifecycle-rules` skill for the normative contract; no copied skill
catalog or hard cross-plugin dependency is required.

## Shared stages and local responsibilities

The shared stages are Spec, Plan, Build, Test, Review, Simplify and Ship, with
STANDARD + SOLO defaults. Profiles QUICK/STANDARD/DEEP change depth, not stage
order. Use task instructions and accepted state first, then missing-field defaults.
Other actor topologies require explicit user authorization; selecting a planning
or review role alone does not authorize dispatch.

- **Spec / Plan:** inspect relevant repository evidence, scope, acceptance and
  project gates. QUICK can use a session checklist; STANDARD records affected
  files, dependencies and checks; DEEP needs durable tasks, decisions, ownership,
  impact and rollout/rollback. Preserve existing artifact paths. No mandatory
  web/registry sweep or PRD/architecture/system_design/tech_doc/task_list dossier.
- **Build:** before writes use the existing using-git-worktrees procedure and
  [worktree policy](./worktree-workflow.md). Primary remains clean on the default
  branch; branch/worktree names follow `<type>/<slug>`. If isolation is blocked,
  stop writes rather than silently edit primary. Implement only authorized scope.
- **Test:** choose meaningful verification by risk/profile and required project
  policy; TDD is selected where useful or required, not universal. QUICK does not
  waive mandatory project gates. Use installed tools and report unavailable
  checks as NOT RUN; no implicit tool installation or forbidden harness launch.
- **Review / Simplify:** inspect current work before base/recent-commit targets,
  assess locally in SOLO, and simplify only within scope. Rerun affected checks
  after edits. Independent review requires explicit authorization.
- **Ship:** assess readiness and execute only explicitly authorized delivery.
  Readiness is not commit/push/PR/merge/deployment permission. Apply
  [git conventions](./git-workflow.md) only for an authorized git action.

## Research, safety and readiness

Start from repository reuse patterns. Expand to available primary documentation
when uncertainty warrants it; external research is not mandatory for every edit.
Installing dependencies, cloning foundations or connecting services needs scope.
Mandatory project security/coverage gates remain binding in every profile; failed
required gates block readiness. Do not claim success for unrun checks. Merge that
triggers GitOps/HCP auto-apply is runtime mutation with separate fresh permission,
impact and rollback; a plan or parallel-work approval is not runtime consent.

This plugin supplies git procedures, not a competing lifecycle or automatic
session policy injection. Its standalone guidance remains safe without another
plugin. Existing hook enforcement is Claude-specific; Codex follows procedural
preflight with bundled hooks disabled. Existing technique conflicts are resolved
in favor of shared safety, user scope and mandatory project policy.
