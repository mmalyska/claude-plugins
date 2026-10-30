---
name: backend-patterns
description: "Backend architecture patterns, API design, database optimization, and server-side best practices for Node.js, Express, and Next.js API routes."
metadata:
  origin: "ECC"
---

# Backend Development Patterns

Backend architecture patterns and best practices for scalable server-side applications.

## When to Activate

- Designing REST or GraphQL API endpoints
- Implementing repository, service, or controller layers
- Optimizing database queries (N+1, indexing, connection pooling)
- Adding caching (Redis, in-memory, HTTP cache headers)
- Setting up background jobs or async processing
- Structuring error handling and validation for APIs
- Building middleware (auth, logging, rate limiting)

## Select relevant detail

Keep transport, business logic and persistence boundaries explicit. Validate input,
bound queries/retries and preserve authorization checks. Select the affected layer.

| Task branch | Reference |
| --- | --- |
| API layers, repositories or middleware | [API layers, repositories or middleware](references/layers-and-middleware.md) |
| Queries, transactions or caching | [Queries, transactions or caching](references/data-and-caching.md) |
| Authentication, authorization or request limits | [Authentication, authorization or request limits](references/auth-and-rate-limits.md) |
| Jobs, failures or observability | [Jobs, failures or observability](references/jobs-errors-and-logging.md) |

Read only the branch that applies; expand when the task crosses topics.
