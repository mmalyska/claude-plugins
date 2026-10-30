---
name: ai-regression-testing
description: "Regression testing strategies for AI-assisted development. Sandbox-mode API testing without database dependencies, automated bug-check workflows, and patterns to catch AI blind spots where the same model writes and reviews code."
metadata:
  origin: "ECC"
---

# AI Regression Testing

Read [the workflow contract](../../rules/common/workflow.md) first. Select profile
and topology independently; default STANDARD + SOLO. Apply mandatory project
policy in every profile. This procedure does not authorize another actor or
work beyond the requested stage.

Testing patterns specifically designed for AI-assisted development, where the same model writes code and reviews it — creating systematic blind spots that only automated tests can catch.

## When to Activate

- AI agent (Claude Code, Cursor, Codex) has modified API routes or backend logic
- A bug was found and fixed — need to prevent re-introduction
- Project has a sandbox/mock mode that can be leveraged for DB-free testing
- Running the existing test or review procedures for changed API behavior
- Multiple code paths exist (sandbox vs production, feature flags, etc.)

## The Core Problem

When an AI writes code and then reviews its own work, it carries the same assumptions into both steps. This creates a predictable failure pattern:

```text
AI writes fix → AI reviews fix → AI says "looks correct" → Bug still exists
```

**Real-world example** (observed in production):

```text
Fix 1: Added notification_settings to API response
  → Forgot to add it to the SELECT query
  → AI reviewed and missed it (same blind spot)

Fix 2: Added it to SELECT query
  → TypeScript build error (column not in generated types)
  → AI reviewed Fix 1 but didn't catch the SELECT issue

Fix 3: Changed to SELECT *
  → Fixed production path, forgot sandbox path
  → AI reviewed and missed it AGAIN (4th occurrence)

Fix 4: Test caught it instantly on first run PASS:
```

The pattern: **sandbox/production path inconsistency** is the #1 AI-introduced regression.

## Integrating with existing Test and Review procedures

Use [test](../test/SKILL.md) for meaningful API regressions and
[review](../review/SKILL.md) for code/contract review. Do not create a separate
`bug-check` skill or require another workflow provider. The examples above are
API-testing techniques, not required tests or commands for every change.

Choose checks by profile, changed behavior and project policy:

- QUICK: smallest meaningful API check when API behavior changes; documentation
  edits can use documented Markdown checks rather than an API suite.
- STANDARD: reproduce the relevant API failure and run affected project gates.
- DEEP: cover failure paths, sandbox/production parity and integration scenarios
  where applicable, with durable evidence and a separate local review pass.

Discover installed project test/build commands; do not assume npm or install a
runner. Review response shapes, selected database columns, error rollback and
optimistic-update races when relevant. A failing required check blocks readiness;
record unavailable checks as NOT RUN. Propose targeted regression coverage for
actual fixes and rerun affected checks if review changes implementation. No test
result authorizes delivery or production mutations.

## Strategy: Test Where Bugs Were Found

Don't aim for 100% coverage. Instead:

```text
Bug found in /api/user/profile     → Write test for profile API
Bug found in /api/user/messages    → Write test for messages API
Bug found in /api/user/favorites   → Write test for favorites API
No bug in /api/user/notifications  → Don't write test (yet)
```

**Why this works with AI development:**

1. AI tends to make the **same category of mistake** repeatedly
2. Bugs cluster in complex areas (auth, multi-path logic, state management)
3. Once tested, that exact regression **cannot happen again**
4. Test count grows organically with bug fixes — no wasted effort

## Quick Reference

| AI Regression Pattern | Test Strategy | Priority |
| --- | --- | --- |
| Sandbox/production mismatch | Assert same response shape in sandbox mode | High |
| SELECT clause omission | Assert all required fields in response | High |
| Error state leakage | Assert state cleanup on error | Medium |
| Missing rollback | Assert state restored on API failure | Medium |
| Type cast masking null | Assert field is not undefined | Medium |

## DO / DON'T

**DO:**

- Write tests immediately after finding a bug (before fixing it if possible)
- Test the API response shape, not the implementation
- Run relevant automated checks and record failures before readiness
- Keep focused sandbox checks fast and use integration checks for real boundaries
- Name tests after the bug they prevent (e.g., "BUG-R1 regression")

**DON'T:**

- Restrict regression coverage to historical bugs when new behavior needs tests
- Trust AI self-review as a substitute for automated tests
- Skip sandbox path testing because "it's just mock data"
- Write integration tests when unit tests suffice
- Aim for coverage percentage — aim for regression prevention

## Select relevant detail

Use existing Test/Review procedures and project gates. Record real reproducer
and post-change outcomes; examples do not certify a scanner or independent review.

| Task branch | Reference |
| --- | --- |
| Sandbox API setup or a known regression pattern | [Sandbox API setup or a known regression pattern](references/regression-examples.md) |

Read only the branch that applies; expand when the task crosses topics.
