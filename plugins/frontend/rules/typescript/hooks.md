---
paths:
  - "**/*.ts"
  - "**/*.tsx"
  - "**/*.js"
  - "**/*.jsx"
---

# TypeScript/JavaScript Verification

Use the project's installed formatter and lint scripts after relevant edits,
and its type-check command for TypeScript changes. Check changed code for
accidental debug logging before finishing.

Claude Code may run these through configured PostToolUse/Stop hooks when the
installed version supports them. Codex's bundled hooks are explicitly disabled
in this collection; execute the same checks directly. Do not copy Claude hook
matchers or settings into Codex. No hook is installed by reading this document.
