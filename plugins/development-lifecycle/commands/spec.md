---
description: Define the problem before writing code — interactive spec with verification gate
argument-hint: [feature idea, or blank to start with questions]
---

# Spec Command

**Input**: $ARGUMENTS

---

Invoke the `development-lifecycle:brainstorming` skill to run the full spec process.

**Output format override:** When the brainstorming skill reaches the "Write design doc" step, use the spec template below instead of a freeform design doc.

**Save path:** `docs/superpowers/specs/YYYY-MM-DD-<kebab-case-topic>.md` — create the directory if it doesn't exist.

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

```
/spec → /plan → loop(/build → /test → /review → /simplify) → /ship
```
