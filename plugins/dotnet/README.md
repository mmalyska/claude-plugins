# dotnet

.NET/C# development agents and rules for Claude Code and Codex.

## Agents

- `csharp-reviewer` — C# code review: async patterns, nullable types, LINQ, security, performance
- `database-reviewer` — PostgreSQL query optimization, schema design, security

## Rules

C#-specific coding style, testing (xUnit + Moq), security, hooks (formatters/analyzers), and patterns targeting .NET 10.

## Install

```sh
claude plugin install dotnet@mmalyska-claude-plugins
```

## Codex

After registering this repository marketplace:

```sh
codex plugin add dotnet@mmalyska-claude-plugins
```

Codex loads the same `skills/` files. Invoke them with `$<plugin>:<skill-name>`. Native
Claude agent entrypoints remain Claude-specific; their role skills work in either
host. Rules are on demand, and bundled Claude hooks are disabled in Codex.
