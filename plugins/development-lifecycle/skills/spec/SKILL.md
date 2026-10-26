---
name: spec
description: "Define the problem before writing code — interactive spec with verification gate"
---

Use the current user request as input. In a Claude command invocation, `$ARGUMENTS` carries that input; in Codex, use the text accompanying the skill.
Command-style examples below name workflows: in Codex select the corresponding
installed skill (`$plugin:skill`); do not execute slash commands in a shell.

# Spec Command

**Input**: $ARGUMENTS

---

Clarify the problem, inspect the relevant repository context, identify users
and constraints, compare viable approaches, and agree on measurable success
criteria. Ask only questions that materially affect the design. Use the template
below to record decisions and unresolved issues. If a brainstorming skill is
available it may assist, but it is not required.

**Output:** Use the spec template below and review it with the user before implementation when the task requires a design decision.

**Save path:** Preserve an existing project spec location. Otherwise use
`.reports/agent-workflows/specs/YYYY-MM-DD-<kebab-case-topic>.md`.

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

```text
/spec → implementation → /ship
```
