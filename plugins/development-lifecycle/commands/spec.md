---
description: Define the problem before writing code — interactive spec with verification gate
argument-hint: [feature idea, or blank to start with questions]
---

# Spec Command

**Input**: $ARGUMENTS

---

Kick off spec-driven development. Understand what to build and why before touching code.

## Phase 1 — UNDERSTAND

If `$ARGUMENTS` is provided, restate it:

> I understand you want to build: {restatement}
> Is this correct?

If blank, ask:

> What do you want to build? Describe in a few sentences.

**GATE**: Wait for confirmation before proceeding.

---

## Phase 2 — CLARIFY

Present these questions together (user can answer in one reply):

> **Problem & Users**
> 1. Who has this problem? (specific role, not just "users")
> 2. What pain are they experiencing today?
> 3. Why does the current solution fail them?
> 4. How will you know the problem is solved?
>
> **Scope**
> 5. What are the 2–3 must-have capabilities for v1?
> 6. What is explicitly out of scope?
> 7. Any technical constraints? (stack, performance, security, deadlines)

**GATE**: Wait for answers.

---

## Phase 3 — GENERATE SPEC

Determine the kebab-case name from the feature idea. Save to:
`docs/superpowers/specs/YYYY-MM-DD-<kebab-name>.md`

Use today's date (check with `date +%Y-%m-%d` if needed). Create the directory if it doesn't exist.

Write the spec file with this template:

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

[Any constraints, stack choices, or integration points]

## Open Questions

- [ ] [Unresolved question that could change the approach]
```

---

## Phase 4 — CONFIRM AND HAND OFF

Show the spec to the user. Ask:

> Spec saved to `docs/superpowers/specs/{filename}.md`
>
> Does this capture the problem correctly?
> - **Yes** → continue to planning with: `/plan docs/superpowers/specs/{filename}.md`
> - **Revise** → describe what to change

**GATE**: Do not proceed to planning until the user confirms the spec.

---

## Lifecycle Position

```
/spec → /plan → loop(/build → /test → /review → /simplify) → /ship
```

This command produces a spec doc. The next step is `/plan` to decompose the spec into tasks.
