---
name: systematic-debugging
description: Use when encountering any bug, test failure, or unexpected behavior, before proposing fixes
---

# Systematic Debugging

## Overview

Random fixes waste time and create new bugs. Quick patches mask underlying issues.

**Core principle:** ALWAYS find root cause before attempting fixes. Symptom fixes are failure.

**Violating the letter of this process is violating the spirit of debugging.**

## The Iron Law

```
NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST
```

If you haven't completed Phase 1, you cannot propose fixes.

## When to Use

Use for ANY technical issue:
- Test failures
- Bugs in production
- Unexpected behavior
- Performance problems
- Build failures
- Integration issues

**Use this ESPECIALLY when:**
- Under time pressure (emergencies make guessing tempting)
- "Just one quick fix" seems obvious
- You've already tried multiple fixes
- You don't fully understand the issue

## The Four Phases

You MUST complete each phase before proceeding to the next.

### Phase 1: Root Cause Investigation

**BEFORE attempting ANY fix:**

1. **Read Error Messages Carefully**
   - Don't skip past errors or warnings — they often contain the exact solution
   - Read stack traces completely; note line numbers, file paths, error codes

2. **Reproduce Consistently**
   - Can you trigger it reliably?
   - If not reproducible → gather more data, don't guess

3. **Check Recent Changes**
   - What changed that could cause this?
   - Git diff, recent commits, new dependencies, config changes

4. **Gather Evidence in Multi-Component Systems**

   **For each component boundary: log what enters, log what exits, verify config propagation.**

   ```bash
   # Example pattern: verify at each layer before assuming which one fails
   echo "=== Layer 1 env: ${VAR:+SET}${VAR:-UNSET} ==="
   echo "=== Layer 2 state: $(command check) ==="
   ```

   Run once to gather evidence showing WHERE it breaks, THEN analyze, THEN investigate.

5. **Trace Data Flow**
   - Where does bad value originate?
   - What called this with bad value?
   - Keep tracing up until you find the source
   - Fix at source, not at symptom

### Phase 2: Pattern Analysis

**Find the pattern before fixing:**

1. **Find Working Examples** — locate similar working code in same codebase
2. **Compare Against References** — read reference implementation COMPLETELY
3. **Identify Differences** — what's different between working and broken?
4. **Understand Dependencies** — what settings, config, environment does it need?

### Phase 3: Hypothesis and Testing

**Scientific method:**

1. **Form Single Hypothesis** — "I think X is the root cause because Y"
2. **Test Minimally** — make the SMALLEST possible change to test hypothesis; one variable at a time
3. **Verify Before Continuing** — did it work? Yes → Phase 4. No → form NEW hypothesis. DON'T stack more fixes.
4. **When You Don't Know** — say so; don't pretend; research more

### Phase 4: Implementation

**Fix the root cause, not the symptom:**

1. **Create Failing Test Case** — simplest possible reproduction; automated test if possible; MUST have before fixing
2. **Implement Single Fix** — address the root cause; ONE change at a time; no "while I'm here" improvements
3. **Verify Fix** — test passes? No other tests broken? Issue actually resolved?

4. **If Fix Doesn't Work**
   - STOP
   - If < 3 attempts: Return to Phase 1, re-analyze with new information
   - **If ≥ 3 attempts: Question the architecture** (see below)

5. **If 3+ Fixes Failed: Question Architecture**

   Pattern indicating architectural problem:
   - Each fix reveals new shared state/coupling/problem in different place
   - Fixes require "massive refactoring" to implement
   - Each fix creates new symptoms elsewhere

   **STOP and discuss with your human partner before attempting more fixes.**

## Red Flags — STOP and Follow Process

If you catch yourself thinking:
- "Quick fix for now, investigate later"
- "Just try changing X and see if it works"
- "Add multiple changes, run tests"
- "It's probably X, let me fix that"
- "I don't fully understand but this might work"
- "One more fix attempt" (when already tried 2+)
- Each fix reveals new problem in different place

**ALL of these mean: STOP. Return to Phase 1.**

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "Issue is simple, don't need process" | Simple issues have root causes too. Process is fast for simple bugs. |
| "Emergency, no time for process" | Systematic debugging is FASTER than guess-and-check thrashing. |
| "Just try this first, then investigate" | First fix sets the pattern. Do it right from the start. |
| "I'll write test after confirming fix works" | Untested fixes don't stick. Test first proves it. |
| "Multiple fixes at once saves time" | Can't isolate what worked. Causes new bugs. |
| "I see the problem, let me fix it" | Seeing symptoms ≠ understanding root cause. |
| "One more fix attempt" (after 2+ failures) | 3+ failures = architectural problem. Question pattern. |

## Quick Reference

| Phase | Key Activities | Success Criteria |
|-------|---------------|------------------|
| **1. Root Cause** | Read errors, reproduce, check changes, gather evidence | Understand WHAT and WHY |
| **2. Pattern** | Find working examples, compare | Identify differences |
| **3. Hypothesis** | Form theory, test minimally | Confirmed or new hypothesis |
| **4. Implementation** | Create test, fix, verify | Bug resolved, tests pass |
