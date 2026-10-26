---
name: safety-guard
description: "Apply a requested cautious-operation or directory-scoped workflow in Claude Code or Codex, distinguishing guidance from enforcement."
metadata:
  origin: "ECC"
---

# Safety Guard

Use when the user asks for a cautious workflow or a restricted editing scope.
This Markdown skill provides procedural checks. It does not install a hook,
change the sandbox, intercept commands, or produce an automatic audit log.

## Modes

- **Careful:** before a destructive operation, identify the target, inspect the
  current state, and choose a reversible alternative when practical. Confirm
  destructive operations that the current request has not authorized.
- **Freeze:** record the allowed directory and check every proposed write target
  against it, including shell redirection, rename destinations, and symlinks.
  Read access follows the host's existing permissions. If a required write is
  outside scope, explain it and ask for an expanded scope.
- **Guard:** combine careful operation and freeze scope.
- **Off:** stop applying this skill's extra workflow constraints. This cannot
  disable host permissions, sandbox policy, or installed hooks.

Treat `freeze src/api/` or `guard --dir src/api/` as user intent accompanying the
skill, not a claim that these are installed CLI subcommands.

## Host controls

- **Claude Code:** inspect applicable permissions and installed hooks if the task
  includes enforcement setup. This repository's git-workflows hook protects
  worktree discipline; it is not a general safety-guard implementation.
- **Codex:** follow active sandbox and approval settings. A setting that suppresses
  approval prompts does not by itself restrict writes or destructive operations.
  Codex hook support depends on the installed host and is disabled in this
  collection's Codex manifests.

If the user needs enforced restrictions, identify a verified host mechanism and
prepare the concrete configuration separately. Do not claim enforcement or
logging until that mechanism has been configured and checked. Report any
remaining gaps, including writes performed inside arbitrary programs.
