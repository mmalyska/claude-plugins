# Spec depth repair (2026-11-08)

## Observed

A real planning session in a consumer repository selected DEEP + SOLO and was asked
for a complete specification. The agent:

- never loaded the spec skill or the workflow contract before writing;
- wrote `plan.md`, `tasks.md` and `evidence.md`, with the specification folded into
  `plan.md`, and recorded `profile: DEEP` anyway;
- omitted rejected alternatives and a risk section, and skipped the distinct review
  pass of the draft;
- later told the user the skill had a verification gate, from its description. The
  skill body defined none.

The owner found the PR hard to review because requirements and design were mixed.

## Causes in the packaged guidance

| Cause | Repair |
| --- | --- |
| "May omit a separate document" had no exception for DEEP | DEEP keeps a separate specification |
| Nothing defined when work is big enough for DEEP | Five named triggers; line counts excluded |
| No rule for changing profile during work | Stop, recommend, raise freely, lower only on the user's word |
| Recording a profile did not bind the procedure | The contract and spec skill load before the first DEEP artifact |
| Description claimed a gate the body lacked | A real gate, and a test that keeps them aligned |
| Description did not say when to use the skill | It now names the requested-spec and DEEP cases |
| Template lacked what DEEP requires | Decisions, alternatives and risks sections |
| Default save path ignored plan folders | `spec.md` beside the plan in such projects |
| Planning guidance did not require a spec | Blueprint and the plan resource start from the accepted one |

## Checks

| Check | Result |
| --- | --- |
| New `SpecDepthTest` before the repair | FAIL, as intended (20 failures, 1 error) |
| `python3 -B -m unittest discover -s tests` after the repair | PASS (100 tests, 3 skipped) |
| Fresh model rerun of a DEEP planning task | NOT RUN |

The contract hash in `tests/fixtures/context-layout/manifest.json` was updated because
this repair changes the contract on purpose. The original spec template block is
unchanged; the DEEP sections are a separate block, so the example guard still holds.

These are static checks of packaged text. They do not show that a model will follow
the guidance: skills load on demand, and nothing forces an agent to open one.
