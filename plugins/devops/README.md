# devops plugin

Infrastructure and deployment skills for CI/CD pipelines, Docker, containerization, and production readiness.

## Skills

| Skill | Description |
|-------|-------------|
| `deployment-patterns` | CI/CD pipelines, Docker containerization, health checks, rollback strategies, and production readiness checklists |
| `docker-patterns` | Docker and Docker Compose for local dev, container security, networking, volume strategies, and multi-service orchestration |

## Install

```sh
claude plugin marketplace add mmalyska/claude-plugins
claude plugin install devops@mmalyska-claude-plugins
```

## Codex

After registering this repository marketplace:

```sh
codex plugin add devops@mmalyska-claude-plugins
```

Codex loads the same `skills/` files. Invoke them with `$<plugin>:<skill-name>`. Native
Claude agent entrypoints remain Claude-specific; their role skills work in either
host. Rules are on demand, and bundled Claude hooks are disabled in Codex.
