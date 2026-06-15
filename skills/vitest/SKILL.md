---
name: vitest
description: Comprehensive Vitest unit testing specialist for modern full-stack environments (Next.js 16, React 19, Tailwind v4, shadcn/ui). Covers advanced mocking, snapshot testing, code coverage, and complex state management.
---

# Vitest Unit Testing Specialist

## When to Use

Use this skill when you need to design, implement, or troubleshoot unit tests using Vitest in a modern JavaScript/TypeScript ecosystem. It is particularly tailored for full-stack applications leveraging Next.js 16, React 19, Tailwind CSS v4, and shadcn/ui. This skill is essential when:
- Setting up or optimizing Vitest configurations for speed and reliability.
- Implementing advanced mocking strategies for external dependencies like Prisma ORM, Valkey (Redis) cache, and RabbitMQ queues.
- Writing tests for React Server Components and Client Components.
- Mocking Next.js App Router hooks (`useRouter`, `usePathname`).
- Performing snapshot testing for UI components, custom hooks, and serialized data.
- Validating Zod schemas and complex state management patterns (State Machines, Context Providers, Compound Components).
- Diagnosing and troubleshooting Vitest execution errors, timeouts, and coverage issues.

## Sub-Agent Spawning

This skill supports spawning sub-agents for parallel execution when tasks can be decomposed:

| Trigger Condition | Sub-Agent Type | Purpose |
|---|---|---|
| Multiple React components to test | Component Tester | Parallel snapshot and interaction testing of UI components |
| Multiple external services to mock | Mocking Specialist | Parallel implementation of repository adapters and mocks (Prisma, Redis, RabbitMQ) |
| Multiple Zod schemas to validate | Schema Validator | Parallel testing of validation rules and edge cases |
| Bulk test failure troubleshooting | Diagnostics Agent | Parallel investigation of failing test suites and error codes |

### Spawning Rules
- Spawn when 3+ independent items (components, services, schemas, or failing suites) need the same operation.
- Each sub-agent receives: context (tech stack details), specific target (e.g., a specific component or service), and success criteria (e.g., 90% coverage, passing tests).
- Results are aggregated and cross-referenced for conflicts (e.g., ensuring mock implementations do not conflict).
- Maximum concurrent sub-agents: 10.

## Workflow

1.  **Environment Assessment**: Analyze the project's tech stack (Next.js version, React version, ORM, caching, message queues) to determine the appropriate testing strategy.
2.  **Configuration Setup**: Configure `vitest.config.ts` for optimal performance, including environment selection (`node` vs `jsdom`), coverage thresholds, and parallel execution settings.
3.  **Mocking Strategy Implementation**: Abstract external dependencies (Prisma, Valkey, RabbitMQ) behind interfaces or adapters and implement robust mocks to ensure test isolation and speed.
4.  **Test Implementation**:
    -   Write tests for React Server Components (focusing on static markup generation).
    -   Write tests for React Client Components (focusing on DOM interactions and state changes using `@testing-library/react`).
    -   Implement snapshot tests for UI consistency and serialized data validation.
    -   Test custom hooks and complex state management logic.
    -   Validate Zod schemas against valid, invalid, and edge-case inputs.
5.  **Coverage and Optimization**: Run tests with coverage reporting enabled. Identify gaps in critical business logic and optimize test execution speed using parallelization and caching.
6.  **Troubleshooting**: Diagnose any failing tests using Vitest's error codes, logging, and tracing mechanisms.

## Core Principles

-   **Isolation**: Unit tests must be completely isolated from external systems (databases, caches, networks). Use sophisticated mocking strategies to achieve this.
-   **Speed**: Leverage Vitest's native ESM support, in-process execution, and parallel worker pools to maintain blazing-fast test execution times.
-   **Deterministic Outcomes**: Tests should produce the same results every time they run. Avoid relying on real timers or external state; use fake timers and controlled mocks.
-   **Meaningful Coverage**: Focus coverage metrics on critical business logic, boundary conditions, and error paths rather than purely declarative UI code.
-   **Architecture Alignment**: Align testing strategies with the application's architecture (e.g., testing Server Components as pure functions, mocking App Router hooks appropriately).

## Key References

-   **Complete Reference**: `/home/ubuntu/specialist-skills/vitest/references/complete-reference.md` - An exhaustive guide covering advanced mocking, snapshot testing, configuration schemas, CLI commands, and troubleshooting.
-   **Reading List**: `/home/ubuntu/specialist-skills/vitest/references/reading-list.md` - A curated list of recent books and articles on Vitest, React testing, and modern JavaScript testing practices.
