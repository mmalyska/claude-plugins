---
name: search-first
description: "Research-before-coding workflow. Search for existing tools, libraries, and patterns before writing custom code. Uses available research tools or an authorized researcher."
metadata:
  origin: "ECC"
---

# /search-first — Research Before You Code

Research is a technique within the existing workflow, not another lifecycle.
Use explicit task profile/topology and accepted state, defaulting to STANDARD +
SOLO. If available, consult development-lifecycle-rules for the shared contract;
this plugin has no hard provider dependency. Mandatory project policy applies.
Research depth follows uncertainty and impact, not a mandatory external sweep.

## Trigger

Use this skill when:

- Starting a new feature that likely has existing solutions
- Adding a dependency or integration
- The user asks "add X functionality" and you're about to write code
- Before creating a new utility, helper, or abstraction

## Workflow

```text
┌─────────────────────────────────────────────┐
│  1. NEED ANALYSIS                           │
│     Define what functionality is needed      │
│     Identify language/framework constraints  │
├─────────────────────────────────────────────┤
│  2. SCOPED SEARCH (local by default)      │
│     ┌──────────┐ ┌──────────┐ ┌──────────┐  │
│     │  npm /   │ │  MCP /   │ │  GitHub / │  │
│     │  PyPI    │ │  Skills  │ │  Web      │  │
│     └──────────┘ └──────────┘ └──────────┘  │
├─────────────────────────────────────────────┤
│  3. EVALUATE                                │
│     Score candidates (functionality, maint, │
│     community, docs, license, deps)         │
├─────────────────────────────────────────────┤
│  4. DECIDE                                  │
│     ┌─────────┐  ┌──────────┐  ┌─────────┐  │
│     │  Adopt  │  │  Extend  │  │  Build   │  │
│     │ as-is   │  │  /Wrap   │  │  Custom  │  │
│     └─────────┘  └──────────┘  └─────────┘  │
├─────────────────────────────────────────────┤
│  5. PROPOSE SCOPED ACTION                    │
│     Install/configure/build only when       │
│     authorized; planning can stop here      │
└─────────────────────────────────────────────┘
```

## Decision Matrix

| Signal | Action |
| -------- | -------- |
| Exact match, well-maintained, MIT/Apache | **Adopt** — install and use directly |
| Partial match, good foundation | **Extend** — install + write thin wrapper |
| Multiple weak matches | **Compose** — combine 2-3 small packages |
| Nothing suitable found | **Build** — write custom, but informed by research |

## How to Use

### Quick Mode (inline)

For QUICK, inspect relevant repository patterns first and stop when uncertainty
is resolved. No registry, MCP, installed-skill or GitHub sweep is required for a
small known local edit. For STANDARD, investigate relevant reuse/dependency
questions. For DEEP, compare alternatives and risks in durable planning evidence.

Use `rg` over relevant modules/tests, then available primary documentation or
registries only when needed. Discover tools before use. A recommendation to adopt
or extend is not permission to install a package, clone a project or connect MCP.
Those are separate authorized actions; existing scope can supply that authority.

### Full Mode (agent)

For non-trivial functionality, delegate to an available researcher only when
authorized. Otherwise perform the same research in the current session. The
following is a prompt template, not a literal host tool call:

```text
Research brief:
  Research existing tools for: [DESCRIPTION]
  Language/framework: [LANG]
  Constraints: [ANY]

  Search: npm/PyPI, MCP servers, installed skills, GitHub
  Return: Structured comparison with recommendation
```

## Integration Points

### With planner agent

During Plan, do relevant research locally; delegate only with explicit authority:

- Researcher identifies available tools
- Planner incorporates them into the implementation plan
- Avoids "reinventing the wheel" in the plan

### With architect agent

The architect can investigate locally or consult an explicitly authorized researcher for:

- Technology stack decisions
- Integration pattern discovery
- Existing reference architectures

### With iterative-retrieval skill

Combine for progressive discovery:

- Cycle 1: Broad search (npm, PyPI, MCP)
- Cycle 2: Evaluate top candidates in detail
- Cycle 3: Test compatibility with project constraints

## Anti-Patterns

- **Jumping to code**: Writing a utility without checking if one exists
- **Ignoring MCP**: Not checking if an MCP server already provides the capability
- **Over-customizing**: Wrapping a library so heavily it loses its benefits
- **Dependency bloat**: Installing a massive package for one small feature

## Select relevant detail

Use repository evidence first and research unresolved dependency questions at
the selected depth. Complete the search with sources, adopt/extend/build rationale
and the exact remaining permission or knowledge gap.

| Task branch | Reference |
| --- | --- |
| A worked adoption decision or category-specific search | [A worked adoption decision or category-specific search](references/search-examples.md) |

Read only the branch that applies; expand when the task crosses topics.
