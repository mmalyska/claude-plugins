---
name: tdd-guide
description: "Guide selected test-first feature work and bug reproducers with project-specific coverage and relevant verification. Apply locally by default; separate-agent execution requires explicit user authorization."
---

# TDD Guide

Read [the workflow contract](../../rules/common/workflow.md) first. Select profile
and topology independently; default STANDARD + SOLO. Apply mandatory project
policy in every profile. This procedure does not authorize another actor or
work beyond the requested stage.

Use this role locally by default (STANDARD + SOLO), preserving explicit task
profile/topology. Naming a role does not authorize another actor. HANDOFF,
PARALLEL and REVIEW require explicit user authorization before delegation.
Check authority before exposed capability; reuse existing authorization only
within its scope. Keep the configured model and task/tool/permission limits.
Never launch another CLI to bypass a restriction. Read applicable shared
`AGENTS.md` first, then host adapters and project policy; report conflicts and
pause dependent actions until reconciled.

## Applicability and profile

Use this role when TDD is explicitly selected, useful for a behavior change or
required by project policy. It does not require all code changes to be test-first.
QUICK can use a documented check for a documentation-only edit; STANDARD uses
focused behavioral regressions; DEEP adds relevant layered/negative evidence.
Mandatory project gates remain binding in every profile. Apply this role locally
in SOLO; selecting this role does not authorize delegation or another harness.

## Selected TDD procedure

1. Describe the expected behavior and choose the smallest meaningful test.
2. Run it and confirm failure for the expected missing behavior (RED).
3. Implement the smallest passing change only when Build is authorized (GREEN).
4. Refactor within scope, keep checks green and run affected regressions.
5. Evaluate relevant coverage against the project's established policy.

Discover installed commands from repository evidence, including an existing
unittest suite; use [test](../test/SKILL.md) for command selection and reporting.
Do not install tools implicitly or weaken correct tests to hide a defect.

## Select applicable test types and edge cases

Choose unit tests for isolated behavior, integration checks for boundaries and
E2E for relevant critical flows. Project-required types stay mandatory; other
types depend on impact rather than being required for every edit.

Consider relevant null/empty inputs, invalid types, boundaries, error paths,
races, scale and special characters. Explain omitted high-risk cases; do not
force unrelated test classes or costly scenarios into a small scoped change.

## Quality checklist

- Behavior and acceptance criteria drive assertions, not internal implementation.
- Changed risk paths have meaningful coverage and failures are investigated.
- Tests are isolated; external systems are mocked or explicitly authorized fixtures.
- Existing project coverage targets and security gates are satisfied.
- Commands/results and unavailable checks are recorded honestly.

A failed required security or coverage gate blocks readiness. QUICK cannot waive
project policy. If a required check cannot run, record NOT RUN and the limitation.
No universal coverage percentage is imposed by this role.

## Optional deeper evaluation

For release-critical or stochastic behavior, use the available eval guidance or
write concrete capability/regression checks directly. Multiple model trials and
model graders require explicit scope and actual capability; report observed trial
counts, not invented pass@k/pass^k stability. No `tdd-workflow` or external
Superpowers provider is required; the procedure above is self-contained.
