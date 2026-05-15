# dotnet

.NET/C# development agents and rules for Claude Code.

## Agents

- `csharp-reviewer` — C# code review: async patterns, nullable types, LINQ, security, performance
- `database-reviewer` — PostgreSQL query optimization, schema design, security

## Rules

C#-specific coding style, testing (xUnit + Moq), security, hooks (formatters/analyzers), and patterns targeting .NET 10.

## Install

```sh
claude plugin install dotnet@mmalyska/claude-plugins
```
