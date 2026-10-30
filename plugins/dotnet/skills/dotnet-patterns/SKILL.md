---
name: dotnet-patterns
description: "Idiomatic C# and .NET patterns, conventions, dependency injection, async/await, and best practices for building robust, maintainable .NET applications."
metadata:
  origin: "ECC"
---

# .NET Development Patterns

Idiomatic C# and .NET patterns for building robust, performant, and maintainable applications.

## When to Activate

- Writing new C# code
- Reviewing C# code
- Refactoring existing .NET applications
- Designing service architectures with ASP.NET Core

## Core Principles

### 1. Prefer Immutability

Use records and init-only properties for data models. Mutability should be an explicit, justified choice.

```csharp
// Good: Immutable value object
public sealed record Money(decimal Amount, string Currency);

// Good: Immutable DTO with init setters
public sealed class CreateOrderRequest
{
    public required string CustomerId { get; init; }
    public required IReadOnlyList<OrderItem> Items { get; init; }
}

// Bad: Mutable model with public setters
public class Order
{
    public string CustomerId { get; set; }
    public List<OrderItem> Items { get; set; }
}
```

### 2. Explicit Over Implicit

Be clear about nullability, access modifiers, and intent.

```csharp
// Good: Explicit access modifiers and nullability
public sealed class UserService
{
    private readonly IUserRepository _repository;
    private readonly ILogger<UserService> _logger;

    public UserService(IUserRepository repository, ILogger<UserService> logger)
    {
        _repository = repository ?? throw new ArgumentNullException(nameof(repository));
        _logger = logger ?? throw new ArgumentNullException(nameof(logger));
    }

    public async Task<User?> FindByIdAsync(Guid id, CancellationToken cancellationToken)
    {
        return await _repository.FindByIdAsync(id, cancellationToken);
    }
}
```

### 3. Depend on Abstractions

Use interfaces for service boundaries. Register via DI container.

```csharp
// Good: Interface-based dependency
public interface IOrderRepository
{
    Task<Order?> FindByIdAsync(Guid id, CancellationToken cancellationToken);
    Task<IReadOnlyList<Order>> FindByCustomerAsync(string customerId, CancellationToken cancellationToken);
    Task AddAsync(Order order, CancellationToken cancellationToken);
}

// Registration
builder.Services.AddScoped<IOrderRepository, SqlOrderRepository>();
```

## Anti-Patterns to Avoid

| Anti-Pattern | Fix |
|---|---|
| `async void` methods | Return `Task` (except event handlers) |
| `.Result` or `.Wait()` | Use `await` |
| `catch (Exception) { }` | Handle or rethrow with context |
| `new Service()` in constructors | Use constructor injection |
| `public` fields | Use properties with appropriate accessors |
| `dynamic` in business logic | Use generics or explicit types |
| Mutable `static` state | Use DI scoping or `ConcurrentDictionary` |
| `string.Format` in loops | Use `StringBuilder` or interpolated string handlers |

## Select relevant detail

Keep async calls awaited, cancellation propagated and owned resources disposed.
Use the existing abstractions and Core Principles above; preserve project policy.

| Task branch | Reference |
| --- | --- |
| Async, guard clauses or result handling | [Async, guard clauses or result handling](references/language-and-async.md) |
| Options, EF repositories, middleware or minimal APIs | [Options, EF repositories, middleware or minimal APIs](references/application-and-data.md) |

Read only the branch that applies; expand when the task crosses topics.
