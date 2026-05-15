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
> 3. How are they solving this today, and where does that break down?
> 4. How will you know the problem is solved?
>
> **Scope**
> 5. What are the 2–3 must-have capabilities for v1?
> 6. What is explicitly out of scope?
> 7. Any technical constraints? (stack, performance, security, deadlines)

**GATE**: Wait for answers. If the user skips a question or says "not sure", leave the corresponding spec section as a clearly-marked open question (`- [ ] Still unclear: …`) rather than inventing an answer.

---

## Phase 3 — GENERATE SPEC

Determine the kebab-case name from the feature idea. Resolve the save path:

1. If `docs/superpowers/specs/` exists in the repo root, use it.
2. If `docs/specs/` exists, use that instead.
3. Otherwise ask: "Where should I save the spec? (e.g. `docs/specs/` or just `./`)"

Use today's date (check with `date +%Y-%m-%d` if needed). Create the directory if it doesn't exist.

**Store the fully-resolved path** (e.g. `docs/superpowers/specs/2026-05-15-my-feature.md`) as `spec_path` to use in Phase 4.

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

- **Stack:** [Languages, frameworks, runtimes]
- **Constraints:** [Performance, security, compliance, deadlines]
- **Integrations:** [External systems, APIs, data sources]

## Open Questions

- [ ] [Unresolved question that could change the approach]
```

---

## Phase 4 — CONFIRM AND HAND OFF

Show the spec to the user. Ask (substituting the actual `spec_path` resolved in Phase 3):

> Spec saved to `<spec_path>`
>
> Does this capture the problem correctly?
> - **Yes** → continue to planning with: `/plan <spec_path>`
> - **Revise** → describe what to change

If the user says **Revise**: apply the requested changes to the spec file in-place, show the revised section(s), then repeat the confirmation question above.

**GATE**: Do not proceed to planning until the user confirms the spec.

---

## Lifecycle Position

```
/spec → /plan → loop(/build → /test → /review → /simplify) → /ship
```

This command produces a spec doc. The next step is `/plan` to decompose the spec into tasks.
