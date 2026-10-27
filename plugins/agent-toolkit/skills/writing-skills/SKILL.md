---
name: writing-skills
description: "Create, revise, or validate reusable skills that work directly in Claude Code and Codex."
---

# Writing Shared Skills

## Execution boundary

Check authority before capability. Default STANDARD + SOLO; preserve explicit
accepted task profile/topology and current exclusions. Planning or selecting
roles does not authorize a worker. HANDOFF, PARALLEL and REVIEW require explicit
user authorization before changing actors. Never launch another CLI, worker or
orchestrator to bypass a restriction. Check actual exposed tools/schemas only
after authority; availability alone grants no action.

If requested capability is missing, disclose it and use SOLO/manual execution only
when consistent with user intent. Do not relabel local role passes as independent
review or fabricate tool/background success. Reuse existing specific authority
within scope; no repeated permission menu. Keep the configured model unless a
change is authorized. Mandatory project gates and worktree-first always apply.
Consult the existing development-lifecycle-rules contract when installed; this
plugin's safe local path requires no other plugin or copied skill catalog.

Write one portable workflow, with explicit host-specific steps only where they
change execution. Keep instructions focused on behavior the agent would not
already infer from the task.

## Format and discovery

Use `skills/<name>/SKILL.md` with YAML `name` and `description`. Names use
lowercase letters, digits, and hyphens and match the directory. Describe both
purpose and triggering conditions concisely. Put provenance under `metadata`.
Keep Claude-only agent model/tool settings in native agent entrypoints, not in
shared skill frontmatter. Scripts, references, and assets belong with the skill
or elsewhere inside the same packaged plugin with valid relative links.

Claude invokes skills through its skill/command interface; Codex exposes installed plugin skills as `$plugin:name`.
Do not embed host-specific command syntax as the only way to follow a workflow.
Skill catalog metadata loads before bodies; keep conditional details in linked
references rather than duplicating them in descriptions.

## Portable behavior

- Describe file/search/plan operations by purpose. Use the tools actually exposed
  by the active host, not a required `TodoWrite` or `Task(...)` spelling.
- Check authority before capabilities for delegation, memory, scheduling,
  browsing or MCP calls. Resolve profile/topology independently, with STANDARD +
  SOLO defaults. Supply a local/manual path only when compatible with user intent.
- Distinguish the running host from the configuration being edited. For Codex
  project skills use `.agents/skills/`; for Claude use `.claude/skills/`.
  Verify user-level locations against current host configuration.
- Do not claim that an instruction file installs hooks, enforcement, logging,
  recurring tasks, or external tools. Verify any required integration.
- Keep user authorization and stop conditions intact. A skill does not authorize
  unrelated changes, external actions, or privilege escalation.

## Profile/topology authoring review

Audit descriptions, diagrams, examples, prompts and final steps, not just an opening
warning. None may turn planning, a role name, DEEP or tool availability into actor
or delivery permission. Persist profile/topology/permissions across iterations and
handoffs without treating saved state as new authority. Keep mandatory project
gates in QUICK, local sequential roles in SOLO, bounded authorized actors elsewhere
and no false background/scheduler/enforcement claims. One shared lifecycle remains;
technique phases do not create a competing engineering process.

## Validate

Check frontmatter, naming, local links, dependency availability, and install
containment. Test changed scripts on disposable fixtures. For meaningful behavior
changes, use realistic scenarios covering both hosts and missing capabilities.
Use independent agent trials only when available and authorized; otherwise
record a manual scenario review and its limits. Do not invent successful trial
results or require paid/delegated runs for every wording edit.

For example: a review should still work without subagents; an automation request
should report that scheduling is unavailable rather than pretending a task was
created. Iterate based on demonstrated failures and preserve existing useful
behavior. Committing or publishing a skill follows the user's requested scope.
