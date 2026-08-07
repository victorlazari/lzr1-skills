---
name: vitest
description: Comprehensive Vitest 4.1 unit testing specialist for modern full-stack environments (Next.js 16, React 19). Covers advanced mocking, snapshot testing, test tags, and complex state management.
---

# Vitest Unit Testing Specialist

## When to Use

Use this skill when you need to design, implement, or troubleshoot unit tests using Vitest in a modern JavaScript/TypeScript ecosystem. It is particularly tailored for full-stack applications leveraging Next.js 16, React 19, Tailwind CSS v4, and shadcn/ui. This skill is essential when:

- Setting up or optimizing Vitest 4.1 configurations for speed and reliability, including test tags and `viteModuleRunner: false`.
- Implementing advanced mocking strategies for external dependencies like Prisma ORM, Valkey (Redis) cache, and RabbitMQ queues.
- Writing tests for React Client Components and sync Server Components.
- Mocking Next.js App Router hooks (`useRouter`, `usePathname`).
- Performing snapshot testing for UI components, custom hooks, and serialized data.
- Validating Zod schemas using `expect.schemaMatching` and complex state management patterns.
- Diagnosing and troubleshooting Vitest execution errors, timeouts, and coverage issues.

**Note:** Async Server Components are not supported by Vitest and require E2E testing (e.g., Playwright).

## Sub-Agent Spawning

This skill supports spawning sub-agents for parallel execution when tasks can be decomposed:

| Trigger Condition                  | Sub-Agent Type     | Purpose                                                                            |
| ---------------------------------- | ------------------ | ---------------------------------------------------------------------------------- |
| Multiple React components to test  | Component Tester   | Parallel snapshot and interaction testing of UI components                         |
| Multiple external services to mock | Mocking Specialist | Parallel implementation of repository adapters and mocks (Prisma, Redis, RabbitMQ) |
| Multiple Zod schemas to validate   | Schema Validator   | Parallel implementation of schema validation tests using `expect.schemaMatching`   |
| Bulk test failure troubleshooting  | Diagnostics Agent  | Parallel investigation of failing test suites and error codes                      |

### Spawning Rules

- Spawn when 3+ independent items (components, services, schemas, or failing suites) need the same operation.
- Each sub-agent receives: context (tech stack details), specific target (e.g., a specific component or service), and success criteria (e.g., 90% coverage, passing tests).
- Results are aggregated and cross-referenced for conflicts (e.g., ensuring mock implementations do not conflict).
- Maximum concurrent sub-agents: 10.

## Workflow

1.  **Environment Assessment**: Analyze the project's tech stack (Next.js version, React version, ORM, caching, message queues) to determine the appropriate testing strategy. Verify the installed Vitest version and consult the official documentation for the latest configuration options and API changes.
2.  **Configuration Setup**: Configure `vitest.config.ts`, utilizing test tags and the experimental `viteModuleRunner: false` option if appropriate.
3.  **Mocking Strategy Implementation**: Abstract external dependencies (Prisma, Valkey, RabbitMQ) behind interfaces or adapters and implement robust mocks to ensure test isolation and speed. Use `aroundEach`/`aroundAll` hooks for context management.
4.  **Test Implementation**:
    - Write tests for React Client Components (focusing on DOM interactions and state changes using `@testing-library/react`).
    - Test sync Server Components with Vitest, but route async Server Components to E2E testing.
    - Implement snapshot tests for UI consistency and serialized data validation.
    - Test custom hooks and complex state management logic.
    - Validate Zod schemas against valid, invalid, and edge-case inputs using `expect.schemaMatching`.
    - Utilize the new `test.extend` builder pattern with type inference and `onCleanup` callbacks.
5.  **Coverage and Optimization**: Run tests with coverage reporting enabled. Identify gaps in critical business logic and optimize test execution speed using parallelization and caching.
6.  **Execution and Diagnostics**: Run tests, utilizing Browser Mode visual regression testing and Playwright Traces if configured. Diagnose any failing tests using Vitest's error codes, logging, and tracing mechanisms.

## Core Principles

- **Isolation**: Unit tests must be completely isolated from external systems (databases, caches, networks). Use sophisticated mocking strategies to achieve this.
- **Speed**: Leverage Vitest's native ESM support, in-process execution, and parallel worker pools to maintain blazing-fast test execution times.
- **Deterministic Outcomes**: Tests should produce the same results every time they run. Avoid relying on real timers or external state; use fake timers and controlled mocks.
- **Meaningful Coverage**: Focus coverage metrics on critical business logic, boundary conditions, and error paths rather than purely declarative UI code.
- **Architecture Alignment**: Align testing strategies with the application's architecture (e.g., testing Server Components as pure functions, mocking App Router hooks appropriately).

## Key References

- **Complete Reference**: `references/complete-reference.md` - An exhaustive guide covering advanced mocking, snapshot testing, configuration schemas, CLI commands, and troubleshooting.
- **Reading List**: `references/reading-list.md` - A curated list of recent books and articles on Vitest, React testing, and modern JavaScript testing practices.

---

## Adversarial Verification Panel

For each significant test finding (failing tests, coverage gaps, mocking issues) produced by the parallel sub-agents:

1. Spawn **3 independent Refuter Agents** per finding, each with:
   - The finding in full
   - Instruction: _"Assume this finding is wrong. Find the strongest argument against it."_
   - Default stance: `refuted=true` if evidence is insufficient or ambiguous
2. A finding is **confirmed** only if ≥2 refuters fail to refute it
3. A finding is **discarded** if ≥2 refuters succeed
4. When a confirmed finding had 1 successful refuter, include the dissenting argument in the output with a `CONTESTED` label

> This prevents plausible-but-wrong test findings (failing tests, coverage gaps, mocking issues) from reaching the final output. The 3-vote panel eliminates single-point hallucination without requiring unanimity.

## Cross-System Consistency Validator

After all parallel agents (Component Tester, Mocking Specialist, Schema Validator, Diagnostics Agent) complete, but **before** synthesis:

Run one **Consistency Validator Agent** with all parallel outputs that:

- Flags any pair of recommendations that logically contradict each other
  _(example: Component Tester recommends accepting a snapshot update while Diagnostics Agent flags the same snapshot as a symptom of a broken mock)_
- Notes where one agent's output is a prerequisite for another agent's recommendation
- Passes contradictions to the Synthesis Agent as `MUST_RESOLVE` items
- Passes missing prerequisites as `SEQUENCING_REQUIRED` items

## Synthesis Agent (Upgraded)

The synthesis step actively resolves rather than aggregates:

1. **`MUST_RESOLVE` contradictions**: Pick the better recommendation, annotate the reasoning, preserve the dissenting view as a footnote
2. **`SEQUENCING_REQUIRED` items**: Re-order the unified test report so prerequisites appear before the steps that depend on them
3. **Confidence calibration**: Label each finding `HIGH` / `MEDIUM` / `LOW` confidence based on refuter panel outcomes
4. **Gap analysis**: Note any analysis dimension not covered by any of the parallel agents — these are blind spots, not confirmed negatives
