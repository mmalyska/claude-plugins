---
name: spec
description: "Define the problem before writing code — interactive spec with verification gate"
---

# Spec Command

Read [the workflow contract](../../rules/common/workflow.md) in full before
defining requirements. Resolve it relative to this installed skill file, not the
project cwd or a global search. Read every section, including loading and delivery
boundaries; if the tool truncates output, continue until the entire file is read.
Do not use a head-only excerpt or substitute a fallback spec when required
guidance is unavailable; report the blocker and stop dependent work. Select profile
and topology independently; default STANDARD + SOLO. Apply mandatory project
policy in every profile. This procedure does not authorize another actor or
work beyond the requested stage.

Use the current user request as input. In a Claude command invocation, `$ARGUMENTS` carries that input; in Codex, use the text accompanying the skill.
Command-style examples below name workflows: in Codex select the corresponding
installed skill (`$plugin:skill`); do not execute slash commands in a shell.

**Input**: $ARGUMENTS

---

Clarify the problem, inspect the relevant repository context, identify users
and constraints, compare viable approaches, and agree on measurable success
criteria. Ask only questions that materially affect the design. Use the template
below to record decisions and unresolved issues. If a brainstorming skill is
available it may assist, but it is not required.

## Profile-sized output

- QUICK: record goal, scope and success briefly in session; no mandatory file.
- STANDARD: concise requirements, non-goals and acceptance; use the template's
  relevant sections when the design is non-obvious.
- DEEP: durable repository-grounded specification, alternatives, risks and
  measurable acceptance. Record unresolved decisions instead of inventing them.

The template is optional structure, not a required dossier for every task.
Review material design decisions with the user before dependent implementation;
reuse accepted decisions without asking again. When Plan is authorized, identify
exact files, dependencies, checks and completion criteria using existing planning
procedures. A Spec-only instruction stops here; it does not authorize Build.

**Save path:** Preserve an existing project spec location. Otherwise use
`.reports/agent-workflows/specs/YYYY-MM-DD-<kebab-case-topic>.md`.

## Portable planning resources

When a durable Plan is authorized, reuse the [plan](../../resources/workflow/plan.md),
[task records](../../resources/workflow/tasks.md) and, for an authorized transfer,
[handoff](../../resources/workflow/handoff.md#receiver-preflight). Keep the existing
spec/plan locations and formats; `.plans/<slug>/` is only a fallback without a
project convention. QUICK does not require a file; DEEP multi-session state must
be durable. These resources do not authorize Build, another actor or delivery.

## Spec Template

```md
# [Feature Name] Spec

**Date:** YYYY-MM-DD
**Status:** Draft

## Problem

[2–3 sentences: who has what problem, what is the cost of not solving it]

## Users

**Primary:** [specific description of the target user]
**Not for:** [who this is NOT for, and why]

## Success Criteria

- [ ] [Measurable outcome 1]
- [ ] [Measurable outcome 2]
- [ ] [Measurable outcome 3]

## Scope

### Must Have (v1)
- [Capability 1]
- [Capability 2]

### Out of Scope
- [Deferred item 1] — [why]
- [Deferred item 2] — [why]

## Technical Notes

- **Stack:** [Languages, frameworks, runtimes]
- **Constraints:** [Performance, security, compliance, deadlines]
- **Integrations:** [External systems, APIs, data sources]

## Open Questions

- [ ] [Unresolved question that could change the approach]
```

If a brainstorming question has no answer, record it as `- [ ] Still unclear: …` in Open Questions rather than inventing an answer.

## Lifecycle Position

Follow the seven stages in [the workflow contract](../../rules/common/workflow.md).
This skill supplies Spec and informs Plan; it does not define another lifecycle.
