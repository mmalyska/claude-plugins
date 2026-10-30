---
name: api-design
description: "REST API design patterns including resource naming, status codes, pagination, filtering, error responses, versioning, and rate limiting for production APIs."
metadata:
  origin: "ECC"
---

# API Design Patterns

Conventions and best practices for designing consistent, developer-friendly REST APIs.

## When to Activate

- Designing new API endpoints
- Reviewing existing API contracts
- Adding pagination, filtering, or sorting
- Implementing error handling for APIs
- Planning API versioning strategy
- Building public or partner-facing APIs

## API Design Checklist

Before shipping a new endpoint:

- [ ] Resource URL follows naming conventions (plural, kebab-case, no verbs)
- [ ] Correct HTTP method used (GET for reads, POST for creates, etc.)
- [ ] Appropriate status codes returned (not 200 for everything)
- [ ] Input validated with schema (Zod, Pydantic, Bean Validation)
- [ ] Error responses follow standard format with codes and messages
- [ ] Pagination implemented for list endpoints (cursor or offset)
- [ ] Authentication required (or explicitly marked as public)
- [ ] Authorization checked (user can only access their own resources)
- [ ] Rate limiting configured
- [ ] Response does not leak internal details (stack traces, SQL errors)
- [ ] Consistent naming with existing endpoints (camelCase vs snake_case)
- [ ] Documented (OpenAPI/Swagger spec updated)

## Select relevant detail

Apply the API Design Checklist above to each changed endpoint. Match existing
contracts, validate input and preserve authentication and authorization boundaries.

| Task branch | Reference |
| --- | --- |
| Resource, HTTP, response or auth contracts | [Resource, HTTP, response or auth contracts](references/http-contracts.md) |
| Pagination, filtering, sorting or sparse fields | [Pagination, filtering, sorting or sparse fields](references/pagination-and-query.md) |
| A concrete framework endpoint implementation | [A concrete framework endpoint implementation](references/implementation-examples.md) |

Read only the branch that applies; expand when the task crosses topics.
