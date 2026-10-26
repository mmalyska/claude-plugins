# security plugin

Security skills for code review, cloud infrastructure, and Claude Code and Codex configuration auditing.

## Skills

| Skill | Description |
|-------|-------------|
| `security-review` | Comprehensive security checklist for auth, user input, secrets, API endpoints, and payment flows |
| `security-scan` | Scan Claude Code or Codex configuration for misconfigurations, injection risks, and hook vulnerabilities |

## Install

```sh
claude plugin marketplace add mmalyska/claude-plugins
claude plugin install security@mmalyska-claude-plugins
```

## Codex

After registering this repository marketplace:

```sh
codex plugin add security@mmalyska-claude-plugins
```

Codex loads the same `skills/` files. Invoke them with `$<plugin>:<skill-name>`. Native
Claude agent entrypoints remain Claude-specific; their role skills work in either
host. Rules are on demand, and bundled Claude hooks are disabled in Codex.
