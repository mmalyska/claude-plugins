# backend plugin

Backend engineering skills for API design, Node.js/NestJS, PostgreSQL, database migrations, hexagonal architecture, and MCP server development.

## Skills

| Skill | Description |
|-------|-------------|
| `api-design` | REST API design patterns — resource naming, status codes, pagination, filtering, versioning |
| `backend-patterns` | Node.js, Express, and Next.js API route patterns and best practices |
| `database-migrations` | Schema migrations, rollbacks, and zero-downtime deployments across PostgreSQL and common ORMs |
| `hexagonal-architecture` | Ports & Adapters implementation with clear domain boundaries and dependency inversion |
| `mcp-server-patterns` | Build MCP servers with Node/TypeScript SDK — tools, resources, prompts, Zod validation |
| `nestjs-patterns` | NestJS modules, controllers, DTOs, guards, interceptors, and production-grade TypeScript backends |
| `postgres-patterns` | PostgreSQL query optimization, schema design, indexing, and security (Supabase-informed) |

## Install

```sh
claude plugin marketplace add mmalyska/claude-plugins
claude plugin install backend@mmalyska-claude-plugins
```

## Codex

After registering this repository marketplace:

```sh
codex plugin add backend@mmalyska-claude-plugins
```

Codex loads the same `skills/` files. Invoke them with `$<plugin>:<skill-name>`. Native
Claude agent entrypoints remain Claude-specific; their role skills work in either
host. Rules are on demand, and bundled Claude hooks are disabled in Codex.
