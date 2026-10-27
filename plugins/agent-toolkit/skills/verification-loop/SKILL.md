---
name: verification-loop
description: "A comprehensive verification system for Claude Code or Codex sessions."
metadata:
  origin: "ECC"
---

# Verification Loop Skill

A comprehensive verification system for Claude Code or Codex sessions.

## When to Use

Invoke this skill:

- After completing a feature or significant code change
- Before creating a PR
- When you want to ensure quality gates pass
- After refactoring

## Execution

Discover commands from the project's own configuration; examples below apply
only when those tools are already installed. Do not use package runners that
fetch missing tools implicitly. Capture actual exit status (use `pipefail` if
piping output), redact credentials, and mark unavailable checks as NOT RUN.
Use the project's coverage target rather than imposing a new global threshold.

Choose relevant phases by profile and project policy: QUICK runs a meaningful
focused check, STANDARD runs appropriate affected checks and project gates, and
DEEP adds relevant layered/negative evidence. All use the same existing lifecycle;
these phases organize checks, not new mandatory stages. Apply STANDARD + SOLO
when no accepted selection exists. If available, consult the existing
`development-lifecycle-rules` contract; no hard provider dependency is needed.
Mandatory project gates remain binding in every profile. A failed required
security or coverage gate blocks readiness. QUICK cannot waive it. Mark irrelevant
phases NOT APPLICABLE with a reason; unavailable required checks NOT RUN.

When using the piped Bash examples below, enable `set -o pipefail` first so the
producer's failure is retained; otherwise run the check without truncation and
capture its actual exit code. Inspect runner side effects before invocation.

## Verification Phases

### Phase 1: Build Verification

```bash
# Check if project builds
npm run build 2>&1 | tail -20
# OR
pnpm build 2>&1 | tail -20
```

If build fails, STOP and fix before continuing.

### Phase 2: Type Check

```bash
# TypeScript projects
npm run typecheck  # Only if this script is configured; no implicit fetch

# Python projects
pyright . 2>&1 | head -30
```

Report all type errors. Fix critical ones before continuing.

### Phase 3: Lint Check

```bash
# JavaScript/TypeScript
npm run lint 2>&1 | head -30

# Python
ruff check . 2>&1 | head -30
```

### Phase 4: Test Suite

```bash
# Run tests with coverage
npm run test -- --coverage 2>&1 | tail -50

# Check coverage threshold
# Target: the established project policy, if any; no global threshold
```

Report:

- Total tests: X
- Passed: X
- Failed: X
- Coverage: X%

### Phase 5: Security Scan

```bash
# Check for secrets
grep -rn "sk-" --include="*.ts" --include="*.js" . 2>/dev/null | head -10
grep -rn "api_key" --include="*.ts" --include="*.js" . 2>/dev/null | head -10

# Check for console.log
grep -rn "console.log" --include="*.ts" --include="*.tsx" src/ 2>/dev/null | head -10
```

### Phase 6: Diff Review

```bash
# Show what changed
git diff --stat
git diff --name-only
git diff --cached --name-only
git ls-files --others --exclude-standard
# When clean, compare the actual task base: git diff <base>...HEAD --name-only
```

Review task-relevant untracked files without staging them; a recent commit is
a target only when intended, not an automatic fallback. Review each scoped file for:

- Unintended changes
- Missing error handling
- Potential edge cases

## Output Format

After running relevant phases, produce a verification report. Use PASS/FAIL,
NOT RUN or NOT APPLICABLE with reasons; readiness alone authorizes no delivery:

```text
VERIFICATION REPORT
==================

Build:     [PASS/FAIL]
Types:     [PASS/FAIL] (X errors)
Lint:      [PASS/FAIL] (X warnings)
Tests:     [PASS/FAIL] (X/Y passed, Z% coverage)
Security:  [PASS/FAIL] (X issues)
Diff:      [X files changed]

Overall:   [READY/NOT READY] for PR

Issues to Fix:
1. ...
2. ...
```

## Continuous Mode

For long sessions, choose meaningful checkpoints after relevant changes or risk
transitions; do not rerun the full suite on a timer without new evidence. For example:

```markdown
Set a mental checkpoint:
- After completing each function
- After finishing a component
- Before moving to next task

Invoke the verification-loop skill
```

## Integration with Hooks

In Claude this can complement installed PostToolUse hooks. In Codex the
collection's bundled hooks are disabled; run verification explicitly. Never
report a hook, background checkpoint, or test run that did not actually execute.
