---
name: frontend
description: Advanced Frontend Specialist Guide covering React, Next.js App Router, Server Components, TypeScript, Tailwind CSS, State Management, Testing & Performance.
---

# Frontend Specialist Skill

## When to Use

Use this skill when tasked with building, auditing, or optimizing modern frontend applications. It is particularly suited for projects utilizing React, Next.js (especially the App Router and Server Components), TypeScript, and Tailwind CSS. This skill should be invoked when dealing with complex state management, intricate component patterns, performance bottlenecks, or when establishing robust testing strategies for large-scale frontend codebases.

## Sub-Agent Spawning

This skill supports spawning sub-agents for parallel execution when tasks can be decomposed:

| Trigger Condition | Sub-Agent Type | Purpose |
|---|---|---|
| Multiple components to refactor | Component Refactorer | Parallel refactoring of React components to modern patterns |
| Multiple routes to migrate | Route Migrator | Parallel migration of pages to Next.js App Router |
| Multiple files to type-check | TypeScript Auditor | Parallel auditing and fixing of TypeScript types |
| Bulk performance auditing | Performance Profiler | Parallel Lighthouse/performance checks across routes |
| Multiple test suites to write | Test Engineer | Parallel creation of unit and integration tests |

### Spawning Rules
- Spawn when 3+ independent items (components, routes, files) need the same operation
- Each sub-agent receives: context, specific target, success criteria
- Results are aggregated and cross-referenced for conflicts
- Maximum concurrent sub-agents: 10

## Workflow

1.  **Assessment and Planning**: Evaluate the current state of the frontend application. Identify the core technologies in use (React version, Next.js routing paradigm, styling framework). Determine the primary goals (e.g., migration to App Router, performance optimization, type safety improvements).
2.  **Architecture and Pattern Selection**: Choose appropriate React patterns (e.g., custom hooks, Suspense boundaries) and Next.js features (Server vs. Client Components). Establish a clear state management strategy (local vs. global vs. server state).
3.  **Implementation**:
    *   Develop components using strict TypeScript typing, leveraging generics and discriminated unions where applicable.
    *   Implement styling using Tailwind CSS, optimizing for performance with PurgeCSS and JIT mode.
    *   Integrate data fetching, preferring Server Components in Next.js for server-side data.
4.  **Testing and Validation**: Write comprehensive unit and integration tests using React Testing Library. Implement E2E tests for critical user flows using Playwright or Cypress.
5.  **Performance Optimization**: Profile the application using React DevTools and Lighthouse. Implement code splitting, dynamic imports, and image optimization. Ensure optimal caching strategies are in place.
6.  **Review and Refinement**: Conduct a final review against official best practices and security guidelines.

## Core Principles

*   **Server-First Rendering**: Default to React Server Components in Next.js to minimize client-side JavaScript and improve initial load times.
*   **Strict Type Safety**: Utilize advanced TypeScript features to catch errors at compile time and ensure robust component interfaces.
*   **Utility-First Styling**: Leverage Tailwind CSS for rapid, consistent, and performant UI development, avoiding premature abstraction.
*   **Appropriate State Management**: Choose the simplest state management solution that fits the requirement; avoid global state when local or server state suffices.
*   **Test-Driven Reliability**: Prioritize testing user interactions and accessibility over implementation details.
*   **Continuous Optimization**: Treat performance as a feature, continuously monitoring and optimizing bundle sizes and rendering times.

## Key References

*   React Official Documentation
*   Next.js Documentation - App Router
*   TypeScript Handbook
*   Tailwind CSS Official Site
*   Redux Toolkit Documentation
*   React Testing Library Documentation
*   Playwright Documentation
