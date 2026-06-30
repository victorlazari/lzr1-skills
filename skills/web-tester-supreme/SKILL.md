---
name: web-tester-supreme
description: Advanced web application testing specialist focusing on E2E automation, RBAC validation, Next.js App Router testing, state degradation, complex data visualization, and observability integration.
---

# Web Tester Supreme

## When to Use

Use this skill when you need to perform advanced, enterprise-grade web application testing. This includes:
- Implementing deep end-to-end (E2E) automation using Playwright.
- Validating complex Role-Based Access Control (RBAC) mechanisms and permission gates.
- Testing Next.js App Router specific features like Server/Client Components, loading boundaries, and error boundaries.
- Simulating state and cache degradation (e.g., Valkey cache failures, PostgreSQL replica lag) to ensure application resilience.
- Verifying complex data displays, such as hierarchical tree views, Recharts canvas resizing, and grid-layout constraints.
- Integrating observability into test flows by asserting OpenTelemetry traces and validating structured Pino logs.
- Executing performance, load, security, and accessibility audits using the Web-Tester-Supreme CLI.

## Sub-Agent Spawning

This skill supports spawning sub-agents for parallel execution when tasks can be decomposed:

| Trigger Condition | Sub-Agent Type | Purpose |
|---|---|---|
| Multiple browsers/devices to test | Cross-Browser Tester | Parallel E2E test execution across different environments |
| Multiple user roles to validate | RBAC Validator | Parallel permission and access control testing |
| Multiple API endpoints to mock/test | API Mocking Agent | Parallel API test execution and schema validation |
| Multiple UI components to verify | Visual Regression Tester | Parallel pixel-diffing and visual consistency checks |
| Massive test suites to execute | Sharded Test Runner | Parallel execution of sharded test suites |

### Spawning Rules
- Spawn when 3+ independent items (browsers, roles, endpoints, components) need the same operation
- Each sub-agent receives: context, specific target, success criteria
- Results are aggregated and cross-referenced for conflicts
- Maximum concurrent sub-agents: 10

## Workflow

1.  **Initialization and Configuration**:
    - Initialize the testing environment using `web-tester-supreme init`.
    - Configure the `.webtesterrc` file with project-specific settings, including timeouts, retries, and browser configurations.
    - Set up environment variables for base URLs, authentication tokens, and CI/CD contexts.

2.  **Test Development and Automation**:
    - Develop E2E tests using Playwright, leveraging network interception for API mocking and visual regression testing for UI consistency.
    - Implement RBAC tests by alternating SSO roles and validating permission gates.
    - Write Next.js specific tests to verify Server vs. Client Components and route interception.

3.  **Resilience and Complex UI Testing**:
    - Simulate infrastructure faults (cache failures, database lag) to test graceful degradation.
    - Validate complex UI components like tree views, charts, and grid layouts under various viewport sizes and interactions.

4.  **Execution and Debugging**:
    - Run test suites using `web-tester-supreme run`, utilizing parallelization and sharding for speed.
    - Debug failing tests interactively using `web-tester-supreme debug` or by analyzing generated trace files (`show-trace`).

5.  **Observability and Reporting**:
    - Integrate OpenTelemetry and Pino log assertions into critical test flows.
    - Generate and review comprehensive test reports using `web-tester-supreme report`.

## Core Principles

-   **Deterministic Execution**: Ensure tests are reliable by heavily utilizing network interception, API mocking, and HAR recording to eliminate external dependencies.
-   **Comprehensive Coverage**: Go beyond functional testing to include visual regression, performance benchmarking, security auditing, and accessibility checks.
-   **Resilience First**: Actively test how the application behaves under failure conditions (e.g., cache misses, network latency) to guarantee graceful degradation.
-   **Observability Driven**: Treat telemetry (traces, logs) as first-class citizens in the testing strategy to ensure the application is not only working but also observable.
-   **Scalability and Speed**: Leverage parallel execution, sharding, and state reuse (e.g., caching authentication state) to maintain fast feedback loops in CI/CD pipelines.

## Key References

-   **Playwright Documentation**: For advanced browser automation, network interception, and visual regression testing.
-   **Next.js App Router Testing Guide**: For understanding Server/Client components and edge middleware testing.
-   **OpenTelemetry and Pino**: For integrating observability assertions into E2E test flows.
-   **Web-Tester-Supreme CLI Reference**: For mastering the extensive command set, flags, and configuration options available in the framework.

---

## Parallel Execution Protocol

> **All 5 agents launch simultaneously.** Do not wait for one to finish before starting the next. Each agent receives the full task context and its dedicated reference file only.

### Agent Roster

| Agent | Dimension | Scope | Reference |
|---|---|---|---|
| **Functional Agent** | Functional Testing | Business logic correctness, user flows, edge cases, regression against spec | `references/complete-reference.md` |
| **Visual Agent** | Visual Regression | Layout shifts, rendering differences across browsers/devices, snapshot deltas | `references/complete-reference.md` |
| **A11y Agent** | Accessibility Audit | WCAG 2.1 AA compliance, ARIA, keyboard nav, screen reader compatibility | `references/complete-reference.md` |
| **Performance Agent** | Performance Testing | Core Web Vitals, load time, bundle size, memory leaks, render blocking | `references/complete-reference.md` |
| **Security Agent** | Client-Side Security | XSS, CSRF, CSP headers, sensitive data in localStorage, mixed content | `references/complete-reference.md` |

### Spawning Rules

- **Trigger**: Every invocation of this skill — no exceptions
- **Concurrency**: All 5 agents launch in a single `parallel()` call
- **Context per agent**: Full task input + its dedicated reference file only (no cross-agent sharing during analysis)
- **Maximum concurrent agents**: 5

### Synthesis Agent

After all 5 agents report, run one **Synthesis Agent** with all reports that:

1. **Cross-references** findings across dimensions for interaction effects that no single agent could see
2. **Deduplicates** overlapping findings (same issue detected by multiple agents → one canonical entry)
3. **Prioritizes** the merged set by severity/impact
4. **Produces** a single unified output document

> Synthesis note for this skill: Cross-reference visual regressions with performance findings to surface component-level root causes (e.g., a new animation causing both layout shift and CPU spike). Map security findings to functional test gaps. Produce a prioritized defect matrix.

### Quality Gate

A finding from one agent that **contradicts** a finding from another agent must be flagged as `CONFLICT` and passed to the Synthesis Agent as a `MUST_RESOLVE` item — never silently dropped.
