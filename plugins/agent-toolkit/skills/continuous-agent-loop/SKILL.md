---
name: continuous-agent-loop
description: "Execute bounded agent iterations with verification, persistent progress, and recovery in Claude Code or Codex."
metadata:
  origin: "ECC"
---

# Continuous Agent Loop

Use for a task that needs repeated implement/check iterations. Establish the
objective, acceptance checks, allowed actions, and attempt/runtime limit first.
Use the project's current tracking location, or
`.reports/agent-workflows/loop.md` for a new progress record.

## Iteration

1. Read progress and current repository state. Choose the smallest ready task.
2. Implement within scope. Delegate only through available authorized tools;
   otherwise execute sequentially in the current session.
3. Run the relevant checks and compare their result with acceptance criteria.
4. Record changes, evidence, attempts consumed, blocker, and next action.
5. Continue only while there is measurable progress and budget remains.

Stop on completion, cancellation, a permission block, an unmet external
prerequisite, or the configured limit. On a repeated failure without new evidence,
reduce the problem to a reproducer and report the blocker. Do not increase
privileges, install a loop framework, or invent an unavailable audit command.

For parallel tasks use a dependency graph and isolated worktrees for writers.
For CI/PR workflows inspect actual checks; keep merge, push, and deployment
within explicit task authorization. Use the available `eval-harness` skill or
write concrete pass/fail checks directly.

This loop runs in the current session. For recurring/background execution use
`autonomous-agent-harness` to establish and verify a supported external runner;
do not claim that Markdown instructions keep running after the session ends.
