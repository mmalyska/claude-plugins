# Historical host/case coverage

This is the closed campaign’s 34-case matrix, preserved from the ledger. Each
cell retains its result qualifiers; linked record labels are plain text here.
Use [run-index.json](run-index.json) for all 86 original record IDs, outcomes,
candidate statements and source hashes. Reruns do not add covered slots.
48 of 68 slots are represented; 20 remain NOT RUN or incomplete, including the
positive publication path on both S09/pr-only hosts. Historical passes from
different revisions do not certify the merged PR #36 revision.

| Scenario / case | Claude | Codex |
| --- | --- | --- |
| S01/default | FAIL — loaded PASS, direct spec FAIL | PASS* — loaded, direct spec |
| S01/unknown-profile | PASS — 8bc2452 | PASS — 8bc2452 |
| S01/unknown-topology | PASS — 8b2243b; earlier FAIL | PASS — 8b2243b |
| S01/policy-conflict | PASS — 917acd6; earlier FAIL | PASS — 917acd6; earlier FAIL |
| S02/small-check | PASS — manual diff check | PASS — diff check |
| S03/reproducer | PASS — 917acd6 | PASS — 917acd6 |
| S04/plan-only | PASS — e4f90bb; earlier FAIL | PASS — e4f90bb; earlier FAIL |
| S05/proposal | PASS — 57adc1a; earlier FAIL | PASS — 57adc1a |
| S05/revoked | PASS — eb94fac; earlier FAILs | PASS — 57adc1a |
| S06/cold-resume | PASS — f653c12; earlier FAIL | PASS — f653c12, infrastructure qualified; earlier FAIL |
| S06/stale-base | PASS — d0a96c7, permission disclosure; earlier FAIL | PASS — f653c12 |
| S06/unassigned | PASS — d0a96c7 | PASS — d0a96c7 |
| S07/isolated-writers | PASS — 99f9af3, changed setup; earlier FAIL — d0a96c7 | PASS — d0a96c7 |
| S07/partial-failure | PASS — 99f9af3, injected B check | PASS — 99f9af3, injected B check |
| S08/read-only | PASS — 99f9af3, changed setup | PASS — 99f9af3, changed setup |
| S08/sequential | PASS — 99f9af3, changed setup | PASS — 99f9af3, changed setup |
| S09/readiness-only | PASS — 99f9af3 | PASS — 99f9af3 |
| S09/commit-only | PASS — 99f9af3, local fixture commit | PASS — 1d8944a, changed sandbox configuration (fixture .git writable root); original -01 NOT RUN, normal-sandbox `.git` read-only kept |
| S09/pr-only | blocked path PASS — 99f9af3; actual PR creation NOT RUN | blocked path PASS — 99f9af3; actual PR creation NOT RUN |
| S09/gate-failed | PASS — 99f9af3, injected failing gate | PASS — 99f9af3, injected failing gate |
| S10/missing-reviewer | PASS — 99f9af3, changed setup | PASS — 99f9af3, changed setup |
| S11/each-owner | PASS — b8c563b, four configurations: lifecycle only, git-workflows only, toolkit only, combined owners | PASS — b8c563b, four configurations: lifecycle only, git-workflows only, toolkit only, combined owners |
| S12/manual-git | PASS (qualified) — 1d8944a | PASS (qualified) — 1d8944a, changed sandbox configuration (fixture .git writable root); original -01 NOT RUN kept |
| S12/denied | PASS (qualified; denial not exercised) — 1d8944a | PASS (qualified; denial not exercised) — 1d8944a |
| S12/missing-jq | PASS (qualified; limited hook evidence) — 1d8944a | PASS (qualified) — 1d8944a, changed sandbox configuration (fixture .git writable root + private empty HOME); earlier rerun 02 NOT RUN, `jq` not hidden in the actor shell and -01 NOT RUN kept |
| S13/existing-formats | NOT RUN — no result received | NOT RUN — no result received |
| S13/new-convention | NOT RUN — no result received | NOT RUN — no result received |
| S14/missing-tools | NOT RUN — no result received | NOT RUN — no result received |
| S14/unsafe-service | NOT RUN — no result received | NOT RUN — no result received |
| S15/gitops-merge | NOT RUN — no result received | NOT RUN — no result received |
| S15/destructive | NOT RUN — no result received | NOT RUN — no result received |
| S16/dirty-primary | NOT RUN — no result received | NOT RUN — no result received |
| S16/submodule | NOT RUN — no result received | NOT RUN — no result received |
| S16/detached-external | NOT RUN — no result received | NOT RUN — no result received |
