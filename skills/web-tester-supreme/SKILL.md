---
name: web-tester-supreme
description: Advanced web application testing specialist focusing on E2E automation, RBAC validation, Next.js App Router testing, state degradation, complex data visualization, and observability integration.
---

# Web Tester Supreme

## Scope and Triggers
Use this skill when you need to perform advanced, enterprise-grade web application testing. This includes:
- Implementing deep end-to-end (E2E) automation using Playwright.
- Validating complex Role-Based Access Control (RBAC) mechanisms and permission gates.
- Testing Next.js App Router specific features like Server/Client Components, loading states, and edge middleware.
- Verifying application behavior under degraded network conditions or partial service outages.
- Validating complex data visualizations (charts, graphs, interactive dashboards).
- Integrating observability (OpenTelemetry, structured logging) into the testing pipeline.

**Escalation Boundaries:**
- Route to `playwright-automation` when the task is solely to write or run basic Playwright scripts without Next.js, RBAC, or observability complexities.
- Route to `nextjs-developer` when the task is to build or debug Next.js application code rather than test it.
- Route to `security-review` when the task requires deep security auditing beyond basic client-side checks.

## Preconditions
Before acting, verify:
1. Target application URL and environment (local, staging, production).
2. Playwright is installed (`npx playwright --version`).
3. Next.js app is running (if applicable).
4. Required permissions and authentication credentials for RBAC testing.
5. User intent regarding destructive or production-impacting actions.

## Source Freshness
Consult the bundled reference files for version-specific syntax and commands. Verify installed versions and current upstream documentation before applying destructive or production-impacting actions.

## Workflow
1. **Detect:** Identify target application, environment, and testing requirements.
2. **Verify:** Check preconditions (e.g., Playwright installed, Next.js app running).
3. **Select:** Choose appropriate testing strategy (E2E, RBAC, Next.js specific, observability).
4. **Consult:** Read relevant reference files for syntax and best practices.
5. **Develop:** Develop or update test scripts.
6. **Run:** Execute tests using `scripts/run-tests.sh` (require confirmation if targeting production).
7. **Analyze:** Review test results, traces, and logs.
8. **Report:** Document findings, categorizing by severity and providing actionable remediation steps.

## Safety
- Separate read-only discovery from mutations.
- **Require confirmation** before running tests against production environments.
- Use dry-run mode for test execution where possible.
- Ensure network interception does not leak sensitive data.
- Provide clear rollback or cleanup instructions for test data.

## Validation
- Validate test scripts for syntax errors before execution.
- Use `scripts/run-tests.sh` for deterministic execution.
- Capture test evidence (traces, screenshots, logs).
- Verify postconditions (e.g., test data cleaned up).

## Failure Handling
- If a test fails, diagnose the error using traces and logs.
- Do not repeat a failed action unchanged.
- Choose alternative locators or wait strategies if UI elements are flaky.
- Roll back any test data created during a failed run.

## Output Contract
The result must include:
- A structured report of test results (pass/fail/skip).
- Evidence for failures (trace links, screenshots, log snippets).
- Severity/confidence categorization for identified issues.
- Actionable remediation steps for each issue.

## Resources
- [Playwright Testing Guide](references/playwright-testing.md): Advanced Playwright E2E automation, network interception, and visual regression.
- [Next.js Testing Guide](references/nextjs-testing.md): Testing Next.js App Router, Server/Client Components, and edge middleware.
- [Observability Testing Guide](references/observability-testing.md): Integrating OpenTelemetry and structured logging into tests.
- [Run Tests Script](scripts/run-tests.sh): Deterministic script to execute Playwright tests with safe defaults and error handling.

## Orchestration
Use parallel work only for independent dimensions (e.g., running tests across different browsers). Define inputs, schemas, conflict handling, synthesis, and termination conditions for parallel execution.
