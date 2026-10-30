# Publication validation — 2026-10-30

This branch publishes a curated report from the closed local campaign archive.
It is based on the verified PR #36 merge,
`ab7604b2cb7af099d4a3b264ff43bda7a97f37b5`. It changes documentation only.
No model, actor, native-host trial or fixture rerun occurred during publication.

## Checks performed

- Compared all 86 indexed record hashes and outcomes against the source records:
  66 PASS, 16 FAIL, four excluded NOT RUN observations; 82 scored LIVE records.
- Checked the 34-row host/case matrix: 48/68 slots represented, 20 incomplete.
- Parsed all published JSON; checked local Markdown links and whitespace.
- Checked published files for JWT/private-key patterns and internal thinking,
  signature and credential field names.
- Ran installed Gitleaks against the curated evidence (186,550 bytes at scan time)
  and verification document (24,602 bytes): both exit 0, no leaks found.
- Compared content hashes for all 1,881 original evidence/handoff/verification
  files: unchanged. No cleanup, original-archive commit or original branch update.

These are publication-integrity checks, not new behavioral evidence or a complete
security certification. Raw streams, launch scripts, profiles/auth and `.ai/`
operator continuity are intentionally excluded from this PR. Source checksums do
not publish the omitted originals. Selected observations are operator-authored
record excerpts, and selected checks are independently labeled operator/offline
checks. Read the [scope and limitations](README.md) before interpreting counts.

The [publication manifest](publication-manifest.json) lists checksums of the
published evidence files other than itself, and hashes of the original ledger,
findings and closeout used for curation. The original archive remains local and
intentionally uncommitted. It has not been replaced by this smaller publication.
