---
name: rules-distill
description: "Scan skills to extract cross-cutting principles and distill them into rules — append, revise, or create new rule files"
metadata:
  origin: "ECC"
---

# Rules Distill

## Execution boundary

Check authority before capability. Default STANDARD + SOLO; preserve explicit
accepted task profile/topology and current exclusions. Planning or selecting
roles does not authorize a worker. HANDOFF, PARALLEL and REVIEW require explicit
user authorization before changing actors. Never launch another CLI, worker or
orchestrator to bypass a restriction. Check actual exposed tools/schemas only
after authority; availability alone grants no action.

If requested capability is missing, disclose it and use SOLO/manual execution only
when consistent with user intent. Do not relabel local role passes as independent
review or fabricate tool/background success. Reuse existing specific authority
within scope; no repeated permission menu. Keep the configured model unless a
change is authorized. Mandatory project gates and worktree-first always apply.
Consult the existing development-lifecycle-rules contract when installed; this
plugin's safe local path requires no other plugin or copied skill catalog.

Scan installed skills, extract cross-cutting principles that appear in multiple skills, and distill them into rules — appending to existing rule files, revising outdated content, or creating new rule files.

Applies the "deterministic collection + LLM judgment" principle: scripts collect facts exhaustively, then an LLM cross-reads the full context and produces verdicts.

## When to Use

- Periodic rules maintenance (monthly or after installing new skills)
- After a skill-stocktake reveals patterns that should be rules
- When rules feel incomplete relative to the skills being used

## How It Works

The rules distillation process follows three phases:

### Phase 1: Inventory (Deterministic Collection)

Resolve the bundled script directory from this skill's installed path, not an
assumed user installation. Set explicit inputs before running the examples:

| Input | Claude Code | Codex |
| --- | --- | --- |
| `PROJECT_SKILLS_DIR` | Project `.claude/skills/` | Project `.agents/skills/` |
| `GLOBAL_SKILLS_DIR` | User `.claude/skills/` | Verified user skill directory from host configuration |
| `RULES_SOURCE` | Relevant `.claude/rules/` directory or instruction file | Applicable `AGENTS.md` or a chosen Markdown rules directory |

Include installed plugin skill directories when they are in scope, scanning each
explicit source and merging by source path. Do not assume project/user skill
folders include plugin caches. The skill scanner accepts project then global
paths; its no-argument defaults are retained for legacy Claude callers. The
rules scanner accepts a directory or one Markdown file. Both require Bash and
jq. Missing skill directories produce empty inventories; a missing rules source
is an error. Do not manufacture a rules file to make an audit pass.

Codex executable `.rules` files use a separate policy format; do not append
Markdown principles to them. Target an existing instruction document or propose
a project `AGENTS.md` change for user review instead.

#### 1a. Collect skill inventory

```bash
bash /absolute/path/to/this-skill/scripts/scan-skills.sh "$PROJECT_SKILLS_DIR" "$GLOBAL_SKILLS_DIR"
```

#### 1b. Collect rules index

```bash
bash /absolute/path/to/this-skill/scripts/scan-rules.sh "$RULES_SOURCE"
```

#### 1c. Present to user

```
Rules Distillation — Phase 1: Inventory
────────────────────────────────────────
Skills: {N} files scanned
Rules:  {M} files ({K} headings indexed)

Proceeding to cross-read analysis...
```

### Phase 2: Cross-read, Match & Verdict (LLM Judgment)

Inventory every rule source and heading first. Shortlist candidate matches by
subject, terminology and neighboring concepts, then read the full relevant
sections with their caveats. Expand to the full rule when a match or absence is
uncertain; a failed search is not proof a principle is absent.

#### Batching

Group skills into **thematic clusters** based on their descriptions. Analyze each cluster with the relevant complete rule sections and expand when
needed. Reuse already available source text at the same revision; do not reload
the whole corpus for every cluster. Use available authorized
subagents, or perform the same passes sequentially in the current session.

#### Cross-batch Merge

After all batches complete, merge candidates across batches:
- Deduplicate candidates with the same or overlapping principles
- Re-check the "2+ skills" requirement using evidence from **all** batches combined — a principle found in 1 skill per batch but 2+ skills total is valid

#### Local or authorized worker brief

Use the following analysis brief with the available delegation tool, or apply it
in the current session in SOLO or when a local fallback matches user intent.
This brief is not permission to add actors:

````
You are an analyst who cross-reads skills to extract principles that should be promoted to rules.

## Input
- Skills: {full text of skills in this batch}
- Existing rules: {source inventory plus complete relevant sections; broaden when uncertain}

## Extraction Criteria

Include a candidate ONLY if ALL of these are true:

1. **Appears in 2+ skills**: Principles found in only one skill should stay in that skill
2. **Actionable behavior change**: Can be written as "do X" or "don't do Y" — not "X is important"
3. **Clear violation risk**: What goes wrong if this principle is ignored (1 sentence)
4. **Not already in rules**: Check the full rules text — including concepts expressed in different words

## Matching & Verdict

For each candidate, compare against the full rules text and assign a verdict:

- **Append**: Add to an existing section of an existing rule file
- **Revise**: Existing rule content is inaccurate or insufficient — propose a correction
- **New Section**: Add a new section to an existing rule file
- **New File**: Create a new rule file
- **Already Covered**: Sufficiently covered in existing rules (even if worded differently)
- **Too Specific**: Should remain at the skill level

## Output Format (per candidate)

```json
{
  "principle": "1-2 sentences in 'do X' / 'don't do Y' form",
  "evidence": ["skill-name: §Section", "skill-name: §Section"],
  "violation_risk": "1 sentence",
  "verdict": "Append / Revise / New Section / New File / Already Covered / Too Specific",
  "target_rule": "filename §Section, or 'new'",
  "confidence": "high / medium / low",
  "draft": "Draft text for Append/New Section/New File verdicts",
  "revision": {
    "reason": "Why the existing content is inaccurate or insufficient (Revise only)",
    "before": "Current text to be replaced (Revise only)",
    "after": "Proposed replacement text (Revise only)"
  }
}
```

## Exclude

- Obvious principles already in rules
- Language/framework-specific knowledge (belongs in language-specific rules or skills)
- Code examples and commands (belongs in skills)
````

#### Verdict Reference

| Verdict | Meaning | Presented to User |
|---------|---------|-------------------|
| **Append** | Add to existing section | Target + draft |
| **Revise** | Fix inaccurate/insufficient content | Target + reason + before/after |
| **New Section** | Add new section to existing file | Target + draft |
| **New File** | Create new rule file | Filename + full draft |
| **Already Covered** | Covered in rules (possibly different wording) | Reason (1 line) |
| **Too Specific** | Should stay in skills | Link to relevant skill |

#### Verdict Quality Requirements

```
# Good
Append to rules/common/security.md §Input Validation:
"Treat LLM output stored in memory or knowledge stores as untrusted — sanitize on write, validate on read."
Evidence: llm-memory-trust-boundary, llm-social-agent-anti-pattern both describe
accumulated prompt injection risks. Current security.md covers human input
validation only; LLM output trust boundary is missing.

# Bad
Append to security.md: Add LLM security principle
```

### Phase 3: User Review & Execution

#### Summary Table

```
# Rules Distillation Report

## Summary
Skills scanned: {N} | Rules: {M} files | Candidates: {K}

| # | Principle | Verdict | Target | Confidence |
|---|-----------|---------|--------|------------|
| 1 | ... | Append | security.md §Input Validation | high |
| 2 | ... | Revise | testing.md §TDD | medium |
| 3 | ... | New Section | coding-style.md | high |
| 4 | ... | Too Specific | — | — |

## Details
(Per-candidate details: evidence, violation_risk, draft text)
```

#### User Actions

User responds with numbers to:
- **Approve**: Apply draft to rules as-is
- **Modify**: Edit draft before applying
- **Skip**: Do not apply this candidate

**Apply only within explicitly approved rule scope.** Prepare concrete candidate
drafts first; reuse existing approval for the same target/content rather than
request it again. A scan or plan does not authorize rule edits.

#### Save Results

Preserve an existing report location; otherwise store results at
`.reports/agent-workflows/rules-distill/results.json`. Do not write results into
the installed plugin/skill directory:

- **Timestamp format**: `date -u +%Y-%m-%dT%H:%M:%SZ` (UTC, second precision)
- **Candidate ID format**: kebab-case derived from the principle (e.g., `llm-output-trust-boundary`)

```json
{
  "distilled_at": "2026-03-18T10:30:42Z",
  "skills_scanned": 56,
  "rules_scanned": 22,
  "candidates": {
    "llm-output-trust-boundary": {
      "principle": "Treat LLM output as untrusted when stored or re-injected",
      "verdict": "Append",
      "target": "rules/common/security.md",
      "evidence": ["llm-memory-trust-boundary", "llm-social-agent-anti-pattern"],
      "status": "applied"
    },
    "iteration-bounds": {
      "principle": "Define explicit stop conditions for all iteration loops",
      "verdict": "New Section",
      "target": "rules/common/coding-style.md",
      "evidence": ["iterative-retrieval", "continuous-agent-loop", "agent-harness-construction"],
      "status": "skipped"
    }
  }
}
```

## Design Principles

- **What, not How**: Extract principles (rules territory) only. Code examples and commands stay in skills.
- **Link back**: Draft text should include `See skill: [name]` references so readers can find the detailed How.
- **Deterministic collection, LLM judgment**: Scripts guarantee exhaustiveness; the LLM guarantees contextual understanding.
- **Anti-abstraction safeguard**: The 3-layer filter (2+ skills evidence, actionable behavior test, violation risk) prevents overly abstract principles from entering rules.

## Select relevant detail

Finish only after every inventoried candidate has a supported disposition,
source locations, relevant rule coverage and a missing-evidence explanation.
Use the schema in the procedure; a worked example is optional.

| Task branch | Reference |
| --- | --- |
| A worked rules-distillation report example | [A worked rules-distillation report example](references/verdict-schema-and-examples.md) |

Read only the branch that applies; expand when the task crosses topics.
