# Agent Orchestration

Discover the active host's available agent types and shared role skills. Do not
assume an agent exists because another collection or a user-level directory
contains a similarly named file.

- **Claude Code:** use exposed native agents; `claude agents` can inventory the
  installation when CLI access is available. Native definitions remain under
  `agents/` and link to shared role instructions.
- **Codex:** use available configured agent types through the exposed delegation
  tool, or apply the shared role skill in the current session. Markdown agent
  files do not automatically register native Codex agents.

Delegate only when authorized by the current session. Otherwise perform focused
role passes sequentially and disclose the lack of independent review. Do not
start a second CLI to circumvent a delegation restriction.

Choose roles for the actual task: architecture for design tradeoffs, TDD guidance
for test design, code review for correctness/maintainability, or build resolution
for compiler failures. Give each role the objective, relevant context, constraints,
and expected evidence. Use the session's configured model unless a change is
authorized.

Parallelize independent read-only work when supported. Concurrent writers need
separate worktrees; sequential work can share the current isolated checkout.
Collect findings before changing dependent work and resolve conflicting advice
against requirements and verification evidence.
