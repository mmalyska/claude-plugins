---
name: frontend-patterns
description: "Frontend development patterns for React, Next.js, state management, performance optimization, and UI best practices."
metadata:
  origin: "ECC"
---

# Frontend Development Patterns

Modern frontend patterns for React, Next.js, and performant user interfaces.

## When to Activate

- Building React components (composition, props, rendering)
- Managing state (useState, useReducer, Zustand, Context)
- Implementing data fetching (SWR, React Query, server components)
- Optimizing performance (memoization, virtualization, code splitting)
- Working with forms (validation, controlled inputs, Zod schemas)
- Handling client-side routing and navigation
- Building accessible, responsive UI patterns

## Select relevant detail

Use composition for reusable UI; keep state ownership explicit, async states visible,
and keyboard/focus behavior testable. Select detail by the behavior being changed.

| Task branch | Reference |
| --- | --- |
| Component composition or error boundaries | [Component composition or error boundaries](references/components.md) |
| State, async data or custom hooks | [State, async data or custom hooks](references/state-and-data.md) |
| Forms, keyboard or focus behavior | [Forms, keyboard or focus behavior](references/forms-and-accessibility.md) |
| Rendering performance or animation | [Rendering performance or animation](references/performance.md) |

Read only the branch that applies; expand when the task crosses topics.
