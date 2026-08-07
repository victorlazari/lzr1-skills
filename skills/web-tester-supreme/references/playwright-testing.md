# Playwright Testing Guide

**Verified against upstream:** 2026-08-07

## Overview
This guide covers advanced Playwright E2E automation, network interception, and visual regression testing.

## Authoritative Sources
- [Playwright Documentation](https://playwright.dev/docs/intro)

## Advanced Automation
- Use `page.route()` for network interception and mocking.
- Implement custom fixtures for reusable test setup and teardown.
- Utilize `page.waitForResponse()` and `page.waitForRequest()` for precise synchronization.

## Visual Regression
- Use `expect(page).toHaveScreenshot()` for visual comparisons.
- Configure screenshot thresholds and masks to handle dynamic content.

## Best Practices
- Prefer user-facing locators (e.g., `getByRole`, `getByText`) over CSS/XPath.
- Avoid hardcoded waits (`page.waitForTimeout()`); use auto-waiting and assertions.
- Run tests in parallel to reduce execution time.
