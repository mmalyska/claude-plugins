# Performance and Context Management

Use the active host's configured model and reasoning settings. Change them only
when the user or session instructions authorize it; model names, context limits,
prices, and reasoning controls vary by host and version. Do not assume Claude
model tiers or thinking flags apply to Codex.

For complex changes, create a concrete plan and review task dependencies. Use
available authorized role delegation where helpful, otherwise run focused review
passes in the current session.

Keep context focused: read relevant files, move conditional detail into references,
record accepted decisions and verification evidence, and create a resume brief
before a session boundary. Use host-reported context limits when available; do
not infer a fixed percentage remaining from file sizes or a model family name.

If a build fails, capture the real exit status and error, isolate the smallest
failing change, fix it, and rerun the relevant check. Use a build-error-resolver
role if available; it is not a required dependency.
