---
name: iterative-retrieval
description: "Pattern for progressively refining context retrieval to solve the subagent context problem"
metadata:
  origin: "ECC"
---

# Iterative Retrieval Pattern

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

A bounded context-search technique for local SOLO analysis or explicitly
authorized workers. Search/evaluate/refine steps are not another lifecycle or
authority to spawn a retrieval agent. Code below is pseudocode, not exposed tools.

## When to Activate

- Retrieving context locally or briefing an already authorized worker
- Building multi-agent workflows where context is progressively refined
- Encountering "context too large" or "missing context" failures in agent tasks
- Designing RAG-like retrieval pipelines for code exploration
- Optimizing token usage in agent orchestration

## The Problem

Subagents are spawned with limited context. They don't know:
- Which files contain relevant code
- What patterns exist in the codebase
- What terminology the project uses

Standard approaches fail:
- **Send everything**: Exceeds context limits
- **Send nothing**: Agent lacks critical information
- **Guess what's needed**: Often wrong

## The Solution: Iterative Retrieval

A bounded search loop that progressively refines context. At the limit, report
unresolved gaps; critical missing context blocks dependent implementation rather
than granting permission to guess. Local search does not need another actor:

```
┌─────────────────────────────────────────────┐
│                                             │
│   ┌──────────┐      ┌──────────┐            │
│   │ SEARCH │─────│ EVALUATE │            │
│   └──────────┘      └──────────┘            │
│        ▲                  │                 │
│        │                  ▼                 │
│   ┌──────────┐      ┌──────────┐            │
│   │   LOOP   │─────│  REFINE  │            │
│   └──────────┘      └──────────┘            │
│                                             │
│        Max 3 cycles, then proceed           │
└─────────────────────────────────────────────┘
```

### Phase 1: SEARCH

Initial broad query to gather candidate files:

```javascript
// Start with high-level intent
const initialQuery = {
  patterns: ['src/**/*.ts', 'lib/**/*.ts'],
  keywords: ['authentication', 'user', 'session'],
  excludes: ['*.test.ts', '*.spec.ts']
};

// Local search or an explicitly authorized retrieval operation
const candidates = await retrieveFiles(initialQuery);
```

### Phase 2: EVALUATE

Assess retrieved content for relevance:

```javascript
function evaluateRelevance(files, task) {
  return files.map(file => ({
    path: file.path,
    relevance: scoreRelevance(file.content, task),
    reason: explainRelevance(file.content, task),
    missingContext: identifyGaps(file.content, task)
  }));
}
```

Scoring criteria:
- **High (0.8-1.0)**: Directly implements target functionality
- **Medium (0.5-0.7)**: Contains related patterns or types
- **Low (0.2-0.4)**: Tangentially related
- **None (0-0.2)**: Not relevant, exclude

### Phase 3: REFINE

Update search criteria based on evaluation:

```javascript
function refineQuery(evaluation, previousQuery) {
  return {
    // Add new patterns discovered in high-relevance files
    patterns: [...previousQuery.patterns, ...extractPatterns(evaluation)],

    // Add terminology found in codebase
    keywords: [...previousQuery.keywords, ...extractKeywords(evaluation)],

    // Exclude confirmed irrelevant paths
    excludes: [...previousQuery.excludes, ...evaluation
      .filter(e => e.relevance < 0.2)
      .map(e => e.path)
    ],

    // Target specific gaps
    focusAreas: evaluation
      .flatMap(e => e.missingContext)
      .filter(unique)
  };
}
```

### Phase 4: LOOP

Repeat with refined criteria (max 3 cycles):

```javascript
async function iterativeRetrieve(task, maxCycles = 3) {
  let query = createInitialQuery(task);
  let bestContext = [];

  for (let cycle = 0; cycle < maxCycles; cycle++) {
    const candidates = await retrieveFiles(query);
    const evaluation = evaluateRelevance(candidates, task);

    // Check if we have sufficient context
    const highRelevance = evaluation.filter(e => e.relevance >= 0.7);
    if (highRelevance.length >= 3 && !hasCriticalGaps(evaluation)) {
      return {files: highRelevance, complete: true};
    }

    // Refine and continue
    query = refineQuery(evaluation, query);
    bestContext = mergeContext(bestContext, highRelevance);
  }

  return {files: bestContext, complete: false};
}
```

## Practical Examples

### Example 1: Bug Fix Context

```
Task: "Fix the authentication token expiry bug"

Cycle 1:
  SEARCH: Search for "token", "auth", "expiry" in src/**
  EVALUATE: Found auth.ts (0.9), tokens.ts (0.8), user.ts (0.3)
  REFINE: Add "refresh", "jwt" keywords; exclude user.ts

Cycle 2:
  SEARCH: Search refined terms
  EVALUATE: Found session-manager.ts (0.95), jwt-utils.ts (0.85)
  REFINE: Sufficient context (2 high-relevance files)

Result: auth.ts, tokens.ts, session-manager.ts, jwt-utils.ts
```

### Example 2: Feature Implementation

```
Task: "Add rate limiting to API endpoints"

Cycle 1:
  SEARCH: Search "rate", "limit", "api" in routes/**
  EVALUATE: No matches - codebase uses "throttle" terminology
  REFINE: Add "throttle", "middleware" keywords

Cycle 2:
  SEARCH: Search refined terms
  EVALUATE: Found throttle.ts (0.9), middleware/index.ts (0.7)
  REFINE: Need router patterns

Cycle 3:
  SEARCH: Search "router", "express" patterns
  EVALUATE: Found router-setup.ts (0.8)
  REFINE: Sufficient context

Result: throttle.ts, middleware/index.ts, router-setup.ts
```

## Integration with Agents

Apply this brief locally by default or give it to an already authorized worker:

```markdown
When retrieving context for this task:
1. Start with broad keyword search
2. Evaluate each file's relevance (0-1 scale)
3. Identify what context is still missing
4. Refine search criteria and repeat (max 3 cycles)
5. Return files with relevance >= 0.7
```

## Best Practices

1. **Start broad, narrow progressively** - Don't over-specify initial queries
2. **Learn codebase terminology** - First cycle often reveals naming conventions
3. **Track what's missing** - Explicit gap identification drives refinement
4. **Stop at "good enough"** - 3 high-relevance files beats 10 mediocre ones
5. **Exclude confidently** - Low-relevance files won't become relevant

## Related

- [The Longform Guide](https://x.com/affaanmustafa/status/2014040193557471352) - Subagent orchestration section
- An installed learning skill, if available, for retaining reusable patterns
- Bundled role skills, or native agent definitions when supported by the host
