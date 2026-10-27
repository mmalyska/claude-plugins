# Code Review Standards

Read [the workflow contract](workflow.md) first. QUICK uses focused self-review,
STANDARD full self-review or a separate local pass, and DEEP a distinct deliberate
review pass with evidence. In SOLO apply roles locally; an independent actor
requires explicit topology authorization. Mandatory project gates remain binding
in every profile. Use the existing review/code-review/code-reviewer entrypoints
for stage, transport and role respectively; they do not add lifecycle stages.

## Purpose

Code review ensures quality, security, and maintainability before code is merged. This rule defines when and how to conduct code reviews.

## When to Review

**MANDATORY review triggers:**

- After writing or modifying code
- Before any commit to shared branches
- When security-sensitive code is changed (auth, payments, user data)
- When architectural changes are made
- Before merging pull requests

**Pre-Review Requirements:**

Before requesting review, ensure:

- Required project checks are passing; record unavailable ones as NOT RUN,
  never as a pass. Review may inspect incomplete work, but readiness is blocked
  by failed required checks.
- Merge conflicts are resolved
- Branch is up to date with target branch

## Review Checklist

Before marking code complete:

- [ ] Code is readable and well-named
- [ ] Functions are focused (<50 lines)
- [ ] Files are cohesive (<800 lines)
- [ ] No deep nesting (>4 levels)
- [ ] Errors are handled explicitly
- [ ] No hardcoded secrets or credentials
- [ ] No console.log or debug statements
- [ ] Tests exist for new functionality
- [ ] Applicable project coverage and security gates are satisfied

## Security Review Triggers

**Perform a focused security assessment when relevant, especially for:**

- Authentication or authorization code
- User input handling
- Database queries
- File system operations
- External API calls
- Cryptographic operations
- Payment or financial code

## Review Severity Levels

| Level | Meaning | Action |
| ------- | --------- | -------- |
| CRITICAL | Security vulnerability or data loss risk | **BLOCK** - Must fix before merge |
| HIGH | Bug or significant quality issue | **WARN** - Should fix before merge |
| MEDIUM | Maintainability concern | **INFO** - Consider fixing |
| LOW | Style or minor suggestion | **NOTE** - Optional |

## Role use and review procedure

1. Honor the requested scope; inspect unstaged/staged and task-relevant untracked
   work before the actual base comparison. Select a recent commit only if intended.
2. Read surrounding context and project policy: shared AGENTS.md first, then
   applicable host adapters; surface conflicts.
3. Apply security and relevant quality/domain checklists and report findings first.
4. Run appropriate checks and mandatory project gates with actual results.
5. Use an available authorized specialist only when needed; otherwise apply the
   relevant security/domain checklist in this session. Do not require nonexistent
   security-reviewer, language-reviewer or other agent registrations.

A failed required security or coverage gate blocks readiness. Review-only does not
authorize edits, publication, commit or merge. Keep existing explicit fix scope;
request a missing decision before dependent changes, not approval already given.

## Common Issues to Catch

### Security

- Hardcoded credentials (API keys, passwords, tokens)
- SQL injection (string concatenation in queries)
- XSS vulnerabilities (unescaped user input)
- Path traversal (unsanitized file paths)
- CSRF protection missing
- Authentication bypasses

### Code Quality

- Large functions (>50 lines) - split into smaller
- Large files (>800 lines) - extract modules
- Deep nesting (>4 levels) - use early returns
- Missing error handling - handle explicitly
- Mutation patterns - prefer immutable operations
- Missing tests - add test coverage

### Performance

- N+1 queries - use JOINs or batching
- Missing pagination - add LIMIT to queries
- Unbounded queries - add constraints
- Missing caching - cache expensive operations

## Approval Criteria

- **Approve**: No CRITICAL or HIGH issues
- **Warning**: Only HIGH issues (merge with caution)
- **Block**: CRITICAL issues found

## Integration with Other Rules

This rule works with:

- [testing.md](testing.md) - Test coverage requirements
- [security.md](security.md) - Security checklist
- the project's git workflow conventions - Commit standards
- [agents.md](agents.md) - Agent delegation
