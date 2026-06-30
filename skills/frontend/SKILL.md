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

---

## Adversarial Verification Panel

For each significant component and performance finding produced by the parallel sub-agents:

1. Spawn **3 independent Refuter Agents** per finding, each with:
   - The finding in full
   - Instruction: *"Assume this finding is wrong. Find the strongest argument against it."*
   - Default stance: `refuted=true` if evidence is insufficient or ambiguous
2. A finding is **confirmed** only if ≥2 refuters fail to refute it
3. A finding is **discarded** if ≥2 refuters succeed
4. When a confirmed finding had 1 successful refuter, include the dissenting argument in the output with a `CONTESTED` label

> This prevents plausible-but-wrong component and performance findings from reaching the final output. The 3-vote panel eliminates single-point hallucination without requiring unanimity.

## Cross-System Consistency Validator

After all parallel agents (Component Refactorer, Route Migrator, TypeScript Auditor, Performance Profiler, Test Engineer) complete, but **before** synthesis:

Run one **Consistency Validator Agent** with all parallel outputs that:
- Flags any pair of recommendations that logically contradict each other
  *(example: Performance Profiler recommends lazy-loading a component while Component Refactorer marks it as a Server Component (which cannot be dynamically imported as a Client Component))*
- Notes where one agent's output is a prerequisite for another agent's recommendation
- Passes contradictions to the Synthesis Agent as `MUST_RESOLVE` items
- Passes missing prerequisites as `SEQUENCING_REQUIRED` items

## Synthesis Agent (Upgraded)

The synthesis step actively resolves rather than aggregates:

1. **`MUST_RESOLVE` contradictions**: Pick the better recommendation, annotate the reasoning, preserve the dissenting view as a footnote
2. **`SEQUENCING_REQUIRED` items**: Re-order the unified frontend improvement plan so prerequisites appear before the steps that depend on them
3. **Confidence calibration**: Label each finding `HIGH` / `MEDIUM` / `LOW` confidence based on refuter panel outcomes
4. **Gap analysis**: Note any analysis dimension not covered by any of the parallel agents — these are blind spots, not confirmed negatives
