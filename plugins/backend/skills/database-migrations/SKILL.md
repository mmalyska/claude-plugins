---
name: database-migrations
description: "Database migration best practices for schema changes, data migrations, rollbacks, and zero-downtime deployments across PostgreSQL, MySQL, and common ORMs (Prisma, Drizzle, Kysely, Django, TypeORM, golang-migrate)."
metadata:
  origin: "ECC"
---

# Database Migration Patterns

Safe, reversible database schema changes for production systems.

## When to Activate

- Creating or altering database tables
- Adding/removing columns or indexes
- Running data migrations (backfill, transform)
- Planning zero-downtime schema changes
- Setting up migration tooling for a new project

## Core Principles

1. **Every change is a migration** — never alter production databases manually
2. **Migrations are forward-only in production** — rollbacks use new forward migrations
3. **Schema and data migrations are separate** — never mix DDL and DML in one migration
4. **Test migrations against production-sized data** — a migration that works on 100 rows may lock on 10M
5. **Migrations are immutable once deployed** — never edit a migration that has run in production

## Migration Safety Checklist

Before applying any migration:

- [ ] Migration has both UP and DOWN (or is explicitly marked irreversible)
- [ ] No full table locks on large tables (use concurrent operations)
- [ ] New columns have defaults or are nullable (never add NOT NULL without default)
- [ ] Indexes created concurrently (not inline with CREATE TABLE for existing tables)
- [ ] Data backfill is a separate migration from schema change
- [ ] Tested against a copy of production data
- [ ] Rollback plan documented

## Anti-Patterns

| Anti-Pattern | Why It Fails | Better Approach |
|-------------|-------------|-----------------|
| Manual SQL in production | No audit trail, unrepeatable | Always use migration files |
| Editing deployed migrations | Causes drift between environments | Create new migration instead |
| NOT NULL without default | Locks table, rewrites all rows | Add nullable, backfill, then add constraint |
| Inline index on large table | Blocks writes during build | CREATE INDEX CONCURRENTLY |
| Schema + data in one migration | Hard to rollback, long transactions | Separate migrations |
| Dropping column before removing code | Application errors on missing column | Remove code first, drop column next deploy |

## Select relevant detail

Keep expand/contract changes reversible: deploy compatible code, backfill in
bounded batches, verify old/new readers, then remove obsolete schema only under
accepted runtime scope. Apply every safety checklist item above; record blockers.

| Task branch | Reference |
| --- | --- |
| PostgreSQL DDL, indexes or backfills | [PostgreSQL DDL, indexes or backfills](references/postgresql.md) |
| Prisma, Drizzle or Kysely migrations | [Prisma, Drizzle or Kysely migrations](references/orms-typescript.md) |
| Django or golang-migrate workflows | [Django or golang-migrate workflows](references/orms-python-go.md) |
| A phased zero-downtime migration | [A phased zero-downtime migration](references/expand-contract.md) |

Read only the branch that applies; expand when the task crosses topics.
