# Frontend Verification and Optional Hooks

Use existing project scripts for formatting, linting, type checking, CSS checks,
and the production build. Select checks relevant to the changed files and run
commands directly when automatic hooks are unavailable. Do not fetch remote
packages or assume a file-path environment variable exists.

In Claude Code, these checks can be attached to supported PostToolUse or Stop
hooks after verifying the installed schema and passing file arguments safely.
Hook configuration is a separate requested change; this document installs none.
In Codex, bundled hooks are disabled by this collection's manifests, so run the
same checks explicitly or through the project's existing CI.

Check file size and module boundaries during review. A warning in Markdown is
not enforced interception. Report which commands actually ran and their exit
status. Prefer format, then lint, then type checks, then relevant build checks.
