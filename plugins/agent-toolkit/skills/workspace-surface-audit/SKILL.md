---
name: workspace-surface-audit
description: "Audit the active repo, MCP servers, plugins, connectors, env surfaces, and harness setup, then recommend the highest-value collection-provided skills, hooks, agents, and operator workflows. Use when the user wants help setting up Claude Code or Codex or understanding what capabilities are actually available in their environment."
metadata:
  origin: "ECC"
---

# Workspace Surface Audit

Read-only audit skill for answering the question "what can this workspace and machine actually do right now, and what should we add or enable next?"

This is the collection-provided answer to setup-audit plugins. It does not modify files unless the user explicitly asks for follow-up implementation.

## When to Use

- User says "set up Claude Code or Codex", "recommend automations", "what plugins or MCPs should I use?", or "what am I missing?"
- Auditing a machine or repo before installing more skills, hooks, or connectors
- Comparing official marketplace plugins against collection-provided coverage
- Reviewing `.env`, `.mcp.json`, plugin settings, or connected-app surfaces to find missing workflow layers
- Deciding whether a capability should be a skill, hook, agent, MCP, or external connector

## Non-Negotiable Rules

- Never print secret values. Surface only provider names, capability names, file paths, and whether a key or config exists.
- Prefer collection-provided workflows over generic "install another plugin" advice when the collection can reasonably own the surface.
- Treat external plugins as benchmarks and inspiration, not authoritative product boundaries.
- Separate three things clearly:
  - already available now
  - available but not wrapped well in this collection
  - not available and would require a new integration

## Host-specific discovery

For Claude inspect applicable `CLAUDE.md`, project `.claude/` settings and skills,
and exposed agents/tools. For Codex inspect applicable `AGENTS.md`, project
`.codex/config.toml`, `.agents/skills/`, configured user Codex location, and the
exposed skill/delegation catalog. Mark configured-but-unavailable tools separately.
Do not scan unrelated home directories or enable integrations as part of this audit.
Hook recommendations must name verified host support; these Codex manifests
explicitly disable bundled Claude hooks.

## Audit Inputs

Inspect only the files and settings needed to answer the question well:

1. Repo surface
   - `package.json`, lockfiles, language markers, framework config, `README.md`
   - `.mcp.json`, `.lsp.json`, `.claude/settings*.json`, `.codex/*`
   - `AGENTS.md`, `CLAUDE.md`, install manifests, hook configs
2. Environment surface
   - `.env*` files in the active repo and obvious explicitly in-scope workspaces
   - Surface only key names such as `STRIPE_API_KEY`, `TWILIO_AUTH_TOKEN`, `FAL_KEY`
3. Connected tool surface
   - Installed plugins, enabled connectors, MCP servers, LSPs, and app integrations
4. Collection surface
   - Existing skills, commands, hooks, agents, and manifests that already cover the need

## Audit Process

### Phase 1: Inventory What Exists

Produce a compact inventory:

- active harness targets
- installed plugins and connected apps
- configured MCP servers
- configured LSP servers
- env-backed services implied by key names
- existing ECC skills already relevant to the workspace

If a surface exists only as a primitive, call that out. Example:

- "Stripe is available via connected app, but the collection lacks a billing-operator skill"
- "Google Drive is connected, but there is no collection-provided Google Workspace operator workflow"

### Phase 2: Benchmark Against Official and Installed Surfaces

Compare the workspace against:

- official host-supported plugins that overlap with setup, review, docs, design, or workflow quality
- locally installed plugins in Claude or Codex
- the user's currently connected app surfaces

Do not just list names. For each comparison, answer:

1. what they actually do
2. whether the collection already has parity
3. whether ECC only has primitives
4. whether ECC is missing the workflow entirely

### Phase 3: Turn Gaps Into Collection Decisions

For every real gap, recommend the correct collection-provided shape:

| Gap Type | Preferred Workflow Shape |
|----------|---------------------|
| Repeatable operator workflow | Skill |
| Automatic enforcement or side-effect | Hook |
| Specialized delegated role | Agent |
| External tool bridge | MCP server or connector |
| Install/bootstrap guidance | Setup or audit skill |

Default to user-facing skills that orchestrate existing tools when the need is operational rather than infrastructural.

## Output Format

Return five sections in this order:

1. **Current surface**
   - what is already usable right now
2. **Parity**
   - where the collection already matches or exceeds the benchmark
3. **Primitive-only gaps**
   - tools exist, but the collection lacks a clean operator skill
4. **Missing integrations**
   - capability not available yet
5. **Top 3-5 next moves**
   - concrete collection-provided additions, ordered by impact

## Recommendation Rules

- Recommend at most 1-2 highest-value ideas per category.
- Favor skills with obvious user intent and business value:
  - setup audit
  - billing/customer ops
  - issue/program ops
  - Google Workspace ops
  - deployment/ops control
- If a connector is company-specific, recommend it only when it is genuinely available or clearly useful to the user's workflow.
- If the collection already has a strong primitive, propose a wrapper skill instead of inventing a brand-new subsystem.

## Good Outcomes

- The user can immediately see what is connected, what is missing, and what the collection should own next.
- Recommendations are specific enough to implement in the repo without another discovery pass.
- The final answer is organized around workflows, not API brands.
