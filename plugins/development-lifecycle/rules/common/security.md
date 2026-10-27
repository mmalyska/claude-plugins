# Security Guidelines

Read [the workflow contract](workflow.md) for profile/topology and authorization.
Mandatory security and project gates apply in QUICK, STANDARD and DEEP alike.

## Mandatory security checks

Before readiness or an authorized commit, verify applicable checks. For unrelated
concerns record NOT APPLICABLE with a reason; never waive an applicable required
gate because the profile is QUICK or a specialist is unavailable.

- No hardcoded secrets or credentials, including in logs and artifacts.
- Validate user input and protect relevant database queries against injection.
- Sanitize HTML and apply CSRF protection where the application needs it.
- Verify authentication/authorization, rate limits and safe error handling.
- Honor established project coverage/security targets and evidence requirements.

## Secret management

Use environment variables or an appropriate secret manager; never hardcode secret
values or print them in a report. Validate required configuration without exposing
values. Identify suspected exposures by references and scope; do not fetch secrets
when metadata or a schema is sufficient to assess the issue.

Credential rotation requires separate fresh explicit authorization with impact and
rollback. A recommendation to rotate is not permission to read or replace secrets.
Runtime/destructive remediation is likewise a separate authorized operation.

## Security response protocol

1. Stop the unsafe path and assess severity/evidence without exposing secrets.
2. Perform the security assessment locally by default. A missing security-reviewer
   agent does not waive assessment or mandatory gates. Use the relevant checklist
   here and in [code-review](code-review.md); an independent specialist requires
   explicit topology authorization plus actual exposed capability.
3. A failed required security or coverage gate blocks readiness. Address CRITICAL
   issues within existing authorized fix scope; otherwise report the blocker and
   required scope. Review-only is not remediation or delivery permission.
4. Record suspected exposure, affected components and proposed mitigation/rollback
   using references. Do not rotate credentials, deploy, or mutate runtime under
   general review or plan approval. Obtain separate fresh explicit authorization.
5. Inspect related patterns within scope, flag broader investigation if needed,
   and rerun affected required checks after any authorized change. Unavailable
   checks are NOT RUN and limit readiness, never a passing security assessment.

Read shared `AGENTS.md` first, then host adapters and project policy; report
conflicts and pause dependent actions until reconciled. An absent reviewer,
configuration difference or hook failure cannot select a weaker safety policy.
