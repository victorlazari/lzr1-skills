---
name: playwright
description: Advanced Playwright End-to-End (E2E) testing techniques, configuration, and troubleshooting for modern web applications.
---

# Playwright E2E Specialist

## Scope and triggers

Use this skill when you need to:
- Set up, configure, or optimize Playwright for End-to-End (E2E) testing.
- Implement advanced testing strategies like network interception, API mocking, and visual regression testing.
- Configure multi-browser matrix testing and mobile emulation.
- Integrate Playwright tests into CI/CD pipelines (e.g., GitHub Actions).
- Diagnose and resolve flaky tests, timeouts, and other Playwright execution errors.
- Write robust, accessible, and maintainable tests using Playwright's web-first assertions and semantic locators.
- Utilize new features like component testing (stories and galleries), WebAuthn passkeys, and `AbortSignal`.

**Non-goals:**
- General web scraping without testing intent.
- Testing frameworks other than Playwright (e.g., Cypress, Selenium).

## Preconditions

Before executing Playwright actions, ensure:
- The target application is accessible.
- Node.js is installed (verify with `node -v`).
- Playwright CLI is installed (verify with `npx playwright --version`).
- The environment is verified using `scripts/verify-playwright-env.sh`.

## Source freshness

Volatile facts, such as supported browser versions and CLI flags, are verified against upstream documentation.
- **Verified against upstream:** 2026-08-07
- **Primary Sources:**
  - Playwright Installation: https://playwright.dev/docs/intro
  - Playwright Release Notes: https://playwright.dev/docs/release-notes

## Workflow

1. **Discover:** Identify the target application and testing requirements.
2. **Verify:** Run `scripts/verify-playwright-env.sh` to ensure Node.js, Playwright CLI, and browsers are correctly installed.
3. **Configure:** Use `templates/playwright.config.ts` to set up or update the Playwright configuration, including safe defaults and `retryStrategy: 'isolated'`.
4. **Develop:** Write tests using semantic locators, web-first assertions, and new features like WebAuthn passkeys or component testing.
5. **Execute:** Run tests locally or in CI/CD. Use dry runs (`--list` or `--debug`) to validate test discovery before full execution.
6. **Diagnose:** If tests fail, use Trace Viewer (`--trace on`) and Inspector (`PWDEBUG=1`) to investigate.
7. **Stop:** Terminate the workflow when all tests pass or actionable findings are reported.

## Safety

- **Read-only discovery:** Always use dry runs (`--list`) to verify test configuration before executing tests.
- **Confirmation:** Require user confirmation before running tests against production environments or performing destructive actions.
- **No untrusted code:** Do not download or execute untrusted artifacts.

## Validation

- Run syntax checks on created files (e.g., `bash -n` for scripts, `npx tsc` for TypeScript files if applicable).
- Verify test execution using dry runs.
- Capture evidence of test failures using Trace Viewer and screenshots.

## Failure handling

- **Diagnosis:** Analyze common errors (TimeoutError, TargetClosedError) using Trace Viewer.
- **Alternatives:** If a locator fails, try a more semantic alternative (e.g., `getByRole` instead of `getByTestId`).
- **Rollback:** Provide clear guidance for reverting failed test runs or configuration changes.
- **Avoid repetition:** Do not repeat the same failed action without modifying the approach.

## Output contract

The final output must include:
- A summary of the actions performed (e.g., tests created, configuration updated).
- Evidence of test execution (e.g., pass/fail status, trace links).
- Actionable next steps for resolving any remaining issues.
- Confidence level of the findings (HIGH/MEDIUM/LOW).

## Resources

- `references/complete-reference.md`: Comprehensive technical guide with verification dates.
- `scripts/verify-playwright-env.sh`: Deterministic script to verify the environment.
- `templates/playwright.config.ts`: Reusable configuration template with safe defaults.

## Orchestration

This skill supports spawning sub-agents for parallel execution when tasks can be decomposed:

| Trigger Condition | Sub-Agent Type | Purpose |
|---|---|---|
| Multiple test suites to run | Test Executor | Parallel execution of independent test suites |
| Multiple browsers/devices to test | Matrix Tester | Parallel testing across different browsers and devices |
| Bulk test flakiness investigation | Diagnostics Agent | Parallel investigation of multiple flaky tests |
| Large-scale visual regression | Visual Reviewer | Parallel comparison of visual snapshots |

### Spawning Rules
- Spawn when 3+ independent items need the same operation.
- Each sub-agent receives: context, specific target, success criteria.
- Results are aggregated and cross-referenced for conflicts.
- Maximum concurrent sub-agents: 10.

### Adversarial Verification Panel
For significant test failures and flakiness findings:
1. Spawn 3 independent Refuter Agents per finding.
2. A finding is confirmed only if ≥2 refuters fail to refute it.
3. A finding is discarded if ≥2 refuters succeed.

### Cross-System Consistency Validator
Run one Consistency Validator Agent with all parallel outputs to flag contradictions and missing prerequisites before synthesis.

### Synthesis Agent
Actively resolve contradictions, re-order prerequisites, calibrate confidence, and note gap analysis.
