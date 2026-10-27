# Common Patterns

## Skeleton Projects

Follow [the workflow contract](workflow.md): research depth depends on profile,
uncertainty and risk. Start with repository patterns/tests. A QUICK local edit
need not search external skeletons; STANDARD checks relevant reuse opportunities;
DEEP compares alternatives when architecture or dependencies warrant it.

Evaluate security, extensibility and relevance locally by default. Parallel agents
require explicit topology authorization and actual capability, not merely a useful
comparison. Recommend adopting/extending a proven implementation only if suitable;
cloning a project, adding dependencies or connecting services is a separate scoped
action. Do not install tools or replace the project's foundation implicitly.

## Design Patterns

### Repository Pattern

Encapsulate data access behind a consistent interface:

- Define standard operations: findAll, findById, create, update, delete
- Concrete implementations handle storage details (database, API, file, etc.)
- Business logic depends on the abstract interface, not the storage mechanism
- Enables easy swapping of data sources and simplifies testing with mocks

### API Response Format

Use a consistent envelope for all API responses:

- Include a success/status indicator
- Include the data payload (nullable on error)
- Include an error message field (nullable on success)
- Include metadata for paginated responses (total, page, limit)
