# Workflow live-trial campaign — closed with qualifications

Campaign: 2026-10-28–30, Claude Code and Codex. **82 scored LIVE records:
66 PASS and 16 historical FAIL.** Four additional NOT RUN observations are
excluded from that tally. **48/68 host/case slots have representative evidence;
20 remain incomplete.** The user ended exhaustive testing to conserve subscription
limits and accepted a risk-based closeout. No more campaign runs are queued.

This is a curated publication from an intentionally uncommitted local archive,
not the full transcript collection. It adds no tests, model calls or behavioral
PASS. [All run outcomes](run-index.json), [coverage](coverage.md),
[findings and repairs](findings.md), [selected observations](selected-observations.md)
and [selected checks](selected-checks.json) retain failures and qualifications.
[Publication validation](publication.md) records integrity and secret-scan checks.

## What the evidence supports

Recorded configurations exercise bounded local tasks, stage/actor restrictions,
real isolated concurrent writers, actual cold transfer, readiness/delivery
boundaries and disclosure of unavailable reviewers. Recurring failures concerned
guidance loading, source discovery, pre-write Git facts and test-exit evidence.
Many focused repairs already passed later tests; those passes do not erase earlier
failures or establish universal obedience.

Two PASS records cover only S09/pr-only’s blocked path: successful PR publication
is NOT RUN. Three Codex PASS reruns used a separately granted writable fixture
`.git`; the corrected missing-jq rerun also used a private empty HOME. Normal
sandbox runs and changed configurations remain distinguishable in the index.
CLI exit 0 was never a sufficient behavioral verdict. Independent operator checks
are separate from actor evidence. AGENTS.md may be loaded natively without a Read
event; absence of that event alone does not prove missing policy.

## Revisions and hosts

Each record retains its own candidate statement in the index. The earliest
operator-supplied remote observations have weaker provenance and missing candidate
or fixture metadata. Local captured trials span multiple candidates, including
`f302539`, `8bc2452`, `8b2243b`, `917acd6`, `e4f90bb`, `57adc1a`, `eb94fac`,
`f653c12`, `d0a96c7`, `99f9af3`, `b8c563b` and `1d8944a`.
The last live candidate was `1d8944a3f53f785496c6c6d5c06a2dc0ef63c6cc`.

Local Claude configurations used opusplan (observed claude-sonnet-5-5), with
240 seconds and USD 2 per prompt; these bounds are not a billing guarantee.
Claude versions included 2.1.312 and 2.1.314. Codex 0.164.0 used gpt-6.1-sol,
low reasoning, with a 240-second prompt bound; its observed model ID was not
exposed. Early remote records have their own displayed model/provenance limits.
The selected excerpts preserve exact per-run host details where available.

## Final repair and closure

[PR #36](https://github.com/mmalyska/claude-plugins/pull/36) merged as
`ab7604b2cb7af099d4a3b264ff43bda7a97f37b5` at 2026-10-30 11:13:42 UTC.
It replaces a startup instruction to proceed without further file reads, adds
an offline injector check, aligns future S12 gate setup and bumps git-workflows
to 1.3.10. Before merge, 61 workflow-contract tests, nine manifest tests and
injector/syntax/preservation checks passed. There is **no live retest on that
merged revision**. Offline payload correctness is not model-compliance evidence.

Campaign closure does not waive gates: **full-conformance release acceptance
remains BLOCKED**, with native/platform/rollback and abnormal-checkout gaps
retained. Deferred live coverage includes S13–S16 and actual S09 PR creation.
Use the workflow within actual task permissions; reopen targeted testing only
for a concrete failure or relevant submodule/runtime use, under a fresh grant.
The broad all-plugin context audit is optional and separately scoped.

## Publication scope and provenance

The original 1,877-file archive (about 24 MB) remains local and unchanged. This
publication includes outcome metadata for all 86 run records, 11 selected record
excerpts and selected offline/operator checks. Source SHA-256 values identify
the original local records; hashes do not make omitted files publicly available
or independently prove their contents.

Raw streams, thinking/signatures, private profiles, auth, temporary fixture state,
launch scripts and operator handoffs are excluded. Local paths in excerpts are
normalized. No claim is made that every original artifact is published or that
the excerpts are an independently reproducible model evaluation.
