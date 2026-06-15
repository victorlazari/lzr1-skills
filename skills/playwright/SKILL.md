---
name: playwright
description: Advanced Playwright End-to-End (E2E) testing techniques, configuration, and troubleshooting for modern web applications.
---

# Playwright E2E Specialist

## When to Use

Use this skill when you need to:
- Set up, configure, or optimize Playwright for End-to-End (E2E) testing.
- Implement advanced testing strategies like network interception, API mocking, and visual regression testing.
- Configure multi-browser matrix testing and mobile emulation.
- Integrate Playwright tests into CI/CD pipelines (e.g., GitHub Actions).
- Diagnose and resolve flaky tests, timeouts, and other Playwright execution errors.
- Write robust, accessible, and maintainable tests using Playwright's web-first assertions and semantic locators.

## Sub-Agent Spawning

This skill supports spawning sub-agents for parallel execution when tasks can be decomposed:

| Trigger Condition | Sub-Agent Type | Purpose |
|---|---|---|
| Multiple test suites to run | Test Executor | Parallel execution of independent test suites |
| Multiple browsers/devices to test | Matrix Tester | Parallel testing across different browsers and devices |
| Bulk test flakiness investigation | Diagnostics Agent | Parallel investigation of multiple flaky tests |
| Large-scale visual regression | Visual Reviewer | Parallel comparison of visual snapshots |

### Spawning Rules
- Spawn when 3+ independent items need the same operation
- Each sub-agent receives: context, specific target, success criteria
- Results are aggregated and cross-referenced for conflicts
- Maximum concurrent sub-agents: 10

## Workflow

1.  **Environment & Configuration Setup:**
    -   Ensure Node.js is installed and configure `playwright.config.ts`.
    -   Define global settings, projects (browsers/devices), and web server configurations.
    -   Set up session persistence (e.g., `storageState`) for authenticated flows.
2.  **Test Development:**
    -   Use semantic locators (`getByRole`, `getByLabel`, `getByText`) to interact with elements.
    -   Implement web-first assertions (`expect(locator).toBeVisible()`) to leverage auto-waiting.
    -   Utilize network interception (`page.route()`) to mock APIs and isolate tests from backend volatility.
3.  **Advanced Testing Scenarios:**
    -   Implement visual regression testing using `toHaveScreenshot()`.
    -   Configure mobile emulation and test responsive layouts.
    -   Integrate accessibility testing using `@axe-core/playwright`.
4.  **Execution & CI/CD Integration:**
    -   Run tests locally using the Playwright CLI (`npx playwright test`).
    -   Configure GitHub Actions or other CI/CD tools to run tests automatically on push/PR.
    -   Utilize parallel workers and retries to optimize execution time and handle transient failures.
5.  **Troubleshooting & Diagnostics:**
    -   Use Playwright Trace Viewer (`--trace on`) and Inspector (`PWDEBUG=1`) to debug failures.
    -   Analyze common errors (TimeoutError, TargetClosedError) and apply recovery strategies.
    -   Address flaky tests by ensuring strict locators, waiting for specific states, and isolating test data.

## Core Principles

-   **Web-First Assertions:** Always use Playwright's built-in assertions that automatically wait and retry, rather than manual DOM checks.
-   **Semantic Locators:** Prioritize user-facing attributes (roles, labels, text) over brittle CSS or XPath selectors to ensure tests are resilient to UI changes and accessible.
-   **Test Isolation:** Ensure each test runs independently without sharing state (unless explicitly managed via `storageState`) to prevent cross-test pollution.
-   **Deterministic Execution:** Use network mocking and HAR replay to eliminate external dependencies and ensure consistent test results.
-   **Comprehensive Diagnostics:** Always leverage Trace Viewer and verbose logging when debugging complex issues or flaky tests.

## Key References

-   **Playwright CLI:** `npx playwright test`, `npx playwright codegen`, `npx playwright show-trace`.
-   **Configuration:** `playwright.config.ts` for global, project, and test-level settings.
-   **Locators:** `page.getByRole()`, `page.getByLabel()`, `page.getByText()`, `page.getByTestId()`.
-   **Assertions:** `expect(locator).toBeVisible()`, `expect(locator).toHaveText()`, `expect(page).toHaveScreenshot()`.
-   **Network:** `page.route()`, `route.fulfill()`, `route.abort()`.
