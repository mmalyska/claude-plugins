---
name: security-scan
description: "Audit Claude Code or Codex configuration for exposed secrets, risky permissions, unsafe tools, and instruction injection."
metadata:
  origin: "ECC"
---

# Agent Configuration Security Scan

Audit the configuration the user named. The host running this skill and the
configuration being inspected may differ. If unspecified, inspect project
configuration for the active host; include user-level files only when relevant
and permitted. This is an audit, not automatic remediation.

## Inventory by target

| Target | Relevant surfaces |
| --- | --- |
| Claude Code | `CLAUDE.md`, `.claude/settings*.json`, `.mcp.json`, `.claude/agents/`, `.claude/skills/`, installed plugin manifests and hooks |
| Codex | `AGENTS.md`, project `.codex/config.toml`, configured user Codex directory (`CODEX_HOME` when set), `.agents/skills/`, agent configuration, installed plugin manifests, configured MCP servers |

Read only existing applicable files. Distinguish local defaults from active
configuration and managed settings; do not assume one file shows effective policy.
Redact secret values in every finding, excerpt, command output, and report.

## Manual review (available in either host)

1. **Credentials:** identify literal secrets and environment handling. Report key
   names and file locations, never values. Check whether sensitive files are tracked.
2. **Permissions:** review wildcard command grants, privileged execution, disabled
   sandboxing, approval bypasses, and excessive writable roots against the task.
   The absence of a deny list or hook alone is not a vulnerability.
3. **Tools and MCP:** inspect transport, endpoint trust, executable/package pinning,
   credential forwarding, and least privilege. Flag unreviewed package execution
   and unexpected network destinations with concrete evidence.
4. **Hooks and scripts:** inspect quoting, untrusted interpolation, path handling,
   exfiltration, and failure behavior. Separate scripts present on disk from hooks
   actually enabled and trusted by the host.
5. **Instructions and agents:** examine auto-run instructions, untrusted content
   treated as authority, broad tool access, and unnecessary privileges. A missing
   model selection is not itself a security issue.
6. **Report:** severity, redacted evidence/location, impact, suggested fix, and
   whether effective configuration was verified. Mark unreadable surfaces as
   unassessed rather than safe. Default a saved report to
   `.reports/agent-workflows/security-scan.md`, preserving existing locations.

## Optional external scanner

[AgentShield](https://github.com/affaan-m/agentshield) is an optional dependency.
If an installed scanner is available, inspect its local help and documentation
for the installed version and confirm it supports the target format before
using it. Do not assume a Claude configuration scanner understands Codex TOML,
AGENTS.md semantics, or effective Codex policy. If support is absent or unclear,
perform the manual review above and report that automated coverage is unavailable.

Do not run `npx` to fetch a scanner, install global packages, enable paid model
analysis, scaffold configuration, or apply fixes as an implicit part of a scan.
Prepare requested remediation separately and preserve the user's existing scope.
