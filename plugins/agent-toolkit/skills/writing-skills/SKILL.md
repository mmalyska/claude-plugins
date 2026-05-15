---
name: writing-skills
description: Use when creating new skills, editing existing skills, or verifying skills work before deployment
---

# Writing Skills

## Overview

**Writing skills IS Test-Driven Development applied to process documentation.**

You write test cases (pressure scenarios with subagents), watch them fail (baseline behavior), write the skill (documentation), watch tests pass (agents comply), and refactor (close loopholes).

**Core principle:** If you didn't watch an agent fail without the skill, you don't know if the skill teaches the right thing.

## What is a Skill?

A **skill** is a reference guide for proven techniques, patterns, or tools. Skills help future Claude instances find and apply effective approaches.

**Skills are:** Reusable techniques, patterns, tools, reference guides

**Skills are NOT:** Narratives about how you solved a problem once

## When to Create a Skill

**Create when:**
- Technique wasn't intuitively obvious
- You'd reference this again across projects
- Pattern applies broadly (not project-specific)
- Others would benefit

**Don't create for:**
- One-off solutions
- Standard practices well-documented elsewhere
- Project-specific conventions (put in CLAUDE.md)
- Mechanical constraints that can be automated

## SKILL.md Structure

**Frontmatter (YAML):**
- `name`: Use letters, numbers, and hyphens only
- `description`: Third-person. Start with "Use when..." to focus on triggering conditions. NEVER summarize the skill's process or workflow — Claude may follow the description instead of reading the full skill.

```markdown
---
name: skill-name
description: Use when [specific triggering conditions and symptoms]
---

# Skill Name

## Overview
What is this? Core principle in 1-2 sentences.

## When to Use
Bullet list with symptoms and use cases; when NOT to use

## Core Pattern
Before/after code comparison or step-by-step guide

## Quick Reference
Table or bullets for scanning common operations

## Common Mistakes
What goes wrong + fixes
```

## Claude Search Optimization (CSO)

**Description field is critical for discovery:**

```yaml
# ❌ BAD: Summarizes workflow — Claude may follow this instead of reading skill
description: Use when executing plans - dispatches subagent per task with code review between tasks

# ✅ GOOD: Just triggering conditions, no workflow summary
description: Use when executing implementation plans with independent tasks in the current session
```

**Keyword coverage:** Include error messages, symptoms, synonyms, tool names.

**Token efficiency:** Skills load into every conversation. Keep them concise.
- Frequently-loaded skills: under 200 words
- Other skills: under 500 words

## TDD for Skills

| TDD Concept | Skill Creation |
|-------------|----------------|
| **Test fails (RED)** | Agent violates rule without skill (baseline) |
| **Test passes (GREEN)** | Agent complies with skill present |
| **Refactor** | Close loopholes while maintaining compliance |

### RED: Baseline First

Run pressure scenario with subagent WITHOUT the skill. Document exact behavior:
- What choices did they make?
- What rationalizations did they use (verbatim)?
- Which pressures triggered violations?

### GREEN: Write Minimal Skill

Write skill that addresses those specific rationalizations. Run same scenarios WITH skill. Agent should now comply.

### REFACTOR: Close Loopholes

Agent found new rationalization? Add explicit counter. Re-test until bulletproof.

## The Iron Law

```
NO SKILL WITHOUT A FAILING TEST FIRST
```

This applies to NEW skills AND EDITS to existing skills. No exceptions — not for "simple additions," not for "documentation updates."

## Skill Creation Checklist

**RED Phase:**
- [ ] Create pressure scenarios (3+ combined pressures for discipline skills)
- [ ] Run scenarios WITHOUT skill — document baseline behavior verbatim
- [ ] Identify patterns in rationalizations/failures

**GREEN Phase:**
- [ ] Name uses only letters, numbers, hyphens
- [ ] YAML frontmatter with `name` and `description`
- [ ] Description starts with "Use when..." — no workflow summary
- [ ] Keywords throughout for search
- [ ] Clear overview with core principle
- [ ] Addresses specific baseline failures
- [ ] Run scenarios WITH skill — verify compliance

**REFACTOR Phase:**
- [ ] Identify NEW rationalizations from testing
- [ ] Add explicit counters (for discipline skills)
- [ ] Build rationalization table
- [ ] Re-test until bulletproof

**Deployment:**
- [ ] Commit skill to git and push

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Describe workflow in description | Use triggering conditions only |
| Skip baseline testing | Must see failure before writing skill |
| Batch multiple skills without testing | Test each before moving to next |
| Write for hypothetical rationalizations | Write for observed ones |
| Heavy reference inline | Move to separate file |
