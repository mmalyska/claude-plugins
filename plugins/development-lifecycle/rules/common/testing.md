# Testing Requirements

Read [the workflow contract](workflow.md) for profile selection and stage scope.
The Test stage verifies changed behavior; TDD is a technique selected when useful,
explicitly requested or required by project policy.

## Profile-sized verification

- QUICK: smallest meaningful regression or documented check; Markdown/link checks
  can be sufficient for a low-risk documentation change.
- STANDARD: appropriate automated behavior tests plus applicable project gates.
- DEEP: relevant layered, negative and integration scenarios with durable evidence.

Choose unit, integration and E2E coverage according to actual behavior, risk and
project policy, not as three universal requirements. Discover existing commands
from repository instructions/configuration, including unittest suites; inspect
side effects and available tools before running them. Do not implicitly fetch
runners or start another harness outside session authority.

## Required project gates

Mandatory project gates remain binding in every profile.
A failed required security or coverage gate blocks readiness.
QUICK cannot waive established project targets or safety requirements. There is
no collection-wide coverage percentage. Apply the project's configured target,
when present, and report uncovered changed risks. A required but unavailable
check is NOT RUN and limits readiness; an unrelated check is NOT APPLICABLE with
a reason. Never claim a green result that was not observed.

## Selected TDD and failure investigation

When TDD fits the task, write a focused test, confirm the expected RED failure,
implement only within authorized Build scope, then GREEN and scoped refactoring.
Use the existing tdd-guide role locally or follow this procedure directly; no
external provider or delegated actor is required. A verification-only request
does not authorize implementation fixes.

Inspect test isolation, mocks, actual behavior and requirement expectations.
Fix implementation defects rather than weaken valid tests. Correct a wrong test
only with evidence of its requirement mismatch. Record commands, real exit status,
PASS/FAIL/NOT RUN/NOT APPLICABLE and remaining uncertainty.
