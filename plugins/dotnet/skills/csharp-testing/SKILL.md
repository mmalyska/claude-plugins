---
name: csharp-testing
description: "C# and .NET testing patterns with xUnit, FluentAssertions, mocking, integration tests, and test organization best practices."
metadata:
  origin: "ECC"
---

# C# Testing Patterns

Comprehensive testing patterns for .NET applications using xUnit, FluentAssertions, and modern testing practices.

## When to Activate

- Writing new tests for C# code
- Reviewing test quality and coverage
- Setting up test infrastructure for .NET projects
- Debugging flaky or slow tests

## Test Framework Stack

| Tool | Purpose |
|---|---|
| **xUnit** | Test framework (preferred for .NET) |
| **FluentAssertions** | Readable assertion syntax |
| **NSubstitute** or **Moq** | Mocking dependencies |
| **Testcontainers** | Real infrastructure in integration tests |
| **WebApplicationFactory** | ASP.NET Core integration tests |
| **Bogus** | Realistic test data generation |

## Test Organization

```
tests/
  MyApp.UnitTests/
    Services/
      OrderServiceTests.cs
      PaymentServiceTests.cs
    Validators/
      EmailValidatorTests.cs
  MyApp.IntegrationTests/
    Api/
      OrderApiTests.cs
    Repositories/
      OrderRepositoryTests.cs
  MyApp.TestHelpers/
    Builders/
      OrderBuilder.cs
    Fixtures/
      DatabaseFixture.cs
```

## Common Anti-Patterns

| Anti-Pattern | Fix |
|---|---|
| Testing implementation details | Test behavior and outcomes |
| Shared mutable test state | Fresh instance per test (xUnit does this via constructors) |
| `Thread.Sleep` in async tests | Use `Task.Delay` with timeout, or polling helpers |
| Asserting on `ToString()` output | Assert on typed properties |
| One giant assertion per test | One logical assertion per test |
| Test names describing implementation | Name by behavior: `Method_ExpectedResult_WhenCondition` |
| Ignoring `CancellationToken` | Always pass and verify cancellation |

## Running Tests

```bash
# Run all tests
dotnet test

# Run with coverage
dotnet test --collect:"XPlat Code Coverage"

# Run specific project
dotnet test tests/MyApp.UnitTests/

# Filter by test name
dotnet test --filter "FullyQualifiedName~OrderService"

# Watch mode during development
dotnet watch test --project tests/MyApp.UnitTests/
```

## Select relevant detail

Choose the configured framework, isolate external dependencies and preserve
real runner outcomes. Completion requires the applicable cases and project gates,
not merely generating tests; dependencies and services need actual authorization.

| Task branch | Reference |
| --- | --- |
| Unit structure, parameterization or mocking | [Unit structure, parameterization or mocking](references/unit-and-mocking.md) |
| ASP.NET integration or container fixtures | [ASP.NET integration or container fixtures](references/integration-and-fixtures.md) |

Read only the branch that applies; expand when the task crosses topics.
