# frontend

React/Next.js and TypeScript rules for Claude Code and Codex.

## Rules

**Web:** coding style (CSS custom properties, semantic HTML, animation), design quality (anti-template policy, hierarchy), testing (visual regression, a11y, cross-browser), performance (Core Web Vitals, bundle budgets), patterns (state management, data fetching), hooks, security (CSP, XSS prevention).

**TypeScript:** coding style, patterns, testing, hooks (ESLint/Prettier/tsc), security.

## Install

```sh
claude plugin install frontend@mmalyska-claude-plugins
```

## Codex

After registering this repository marketplace:

```sh
codex plugin add frontend@mmalyska-claude-plugins
```

Codex loads the same `skills/` files. Invoke them with `$<plugin>:<skill-name>`. Native
Claude agent entrypoints remain Claude-specific; their role skills work in either
host. Rules are on demand, and bundled Claude hooks are disabled in Codex.
