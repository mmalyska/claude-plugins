---
paths:
  - "**/*.cs"
  - "**/*.csx"
  - "**/*.csproj"
  - "**/*.sln"
  - "**/Directory.Build.props"
  - "**/Directory.Build.targets"
---

# C# Verification

Use the project's installed .NET SDK and established solution/test entrypoints.
Run formatting checks as appropriate, `dotnet build` after structural changes,
and relevant `dotnet test` checks after behavior changes. Use `--no-build` only
when testing an up-to-date build. Inspect changed `appsettings*.json` for secrets
without printing credential values.

Claude Code may attach these checks to configured PostToolUse/Stop hooks after
verifying the installed schema. In Codex, bundled hooks are disabled in this
collection; run checks directly. Reading this rule does not configure hooks or
automatic enforcement in either host.
