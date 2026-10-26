---
name: context-budget
description: "Audit instruction and tool context overhead in Claude Code or Codex, distinguishing measured usage from estimates."
metadata:
  origin: "ECC"
---

# Context Budget

Inventory the current session's instructions, skills, agent roles, and tools.
Identify duplicate or oversized context without assuming that every installed
file is loaded.

## Inventory

- **Claude Code:** applicable `CLAUDE.md` chain, loaded rules, installed skill
  names/descriptions, available agents, and configured/exposed MCP tools.
- **Codex:** applicable `AGENTS.md` chain, exposed skill catalog, configured agent
  roles, and exposed tools. Inspect relevant `.codex/config.toml` and user
  configuration only within the audit's scope.
- In either host, distinguish active, installed-but-inactive, on-demand body,
  and unknown loading status. Deduplicate identical content by resolved source
  and content, not by filename alone. Do not print configuration secrets.

## Measure and estimate

Prefer host-reported usage or the matching model tokenizer when available.
Otherwise label prose `words × 1.3` and code `characters / 4` as rough estimates.
Measure exposed tool schemas when accessible; if not, report schema cost as
unknown, not a fixed 500-token cost per tool. Installed configuration does not
prove a server's tools are in context.

Report the model/context limit only when the session or verified configuration
provides it. If unknown, do not calculate remaining tokens or a usage percentage.
Keep catalog metadata separate from skill bodies, which load on demand. Agent
prompts may load only when delegated; do not count their full text as baseline.

## Findings and report

Show source, loading status, measured/estimated tokens, method, and confidence.
Flag duplicate instructions, overly broad descriptions, irrelevant loaded rules,
and large bodies that could become references. Rank a few concrete reductions
by likely savings and loss of capability. Use ranges where loading is uncertain.

Offer a compact report by default and per-file detail on request. Recommend
changes; do not disable plugins, remove tools, or rewrite configuration as part
of an audit unless the user requested those changes.
