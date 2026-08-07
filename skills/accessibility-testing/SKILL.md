---
name: accessibility-testing
description: Execute automated accessibility testing with Axe-core/Playwright, manage known issues via snapshots, and validate dynamic trees, focus, and contrast.
---

# Accessibility Testing

## Scope and Triggers
Use this skill to perform automated accessibility testing using `@axe-core/playwright`, manage known accessibility issues via snapshot tracking, and validate complex UI patterns (focus management, dynamic trees, color contrast).
**Do not use** for general end-to-end testing (use `playwright-testing`) or deep manual WCAG audits (use `wcag-auditor`).

## Preconditions
- Target application must be accessible via URL or local server.
- Playwright and `@axe-core/playwright` must be installed in the target project.
- Verify installed versions of Axe-core and Playwright against expected capabilities before running scans.

## Source Freshness
- Volatile facts (e.g., WCAG criteria versions) are verified against upstream documentation.
- Consult `references/source-map.md` for authoritative links to Axe-core API, Playwright A11y guide, and WAI-ARIA APG.

## Workflow
1. **Assess Scope**: Determine the target pages or components for accessibility testing.
2. **Run Automated Scans**: Execute automated Axe scans using `@axe-core/playwright` with appropriate WCAG tags (e.g., `wcag2a`, `wcag2aa`, `wcag21a`, `wcag21aa`).
3. **Compare Snapshots**: Compare scan results against known issue snapshots using violation fingerprints to identify new issues.
4. **Targeted Validation**: Perform targeted validation for color contrast, focus management, and dynamic trees using provided references.
5. **Report**: Report new violations and provide actionable remediation recommendations.
6. **Stop Condition**: Stop when all target areas have been validated and new violations are reported or resolved.

## Safety
- **Read-only Discovery**: Automated scans do not modify production data.
- **Confirmation**: Require confirmation before updating known issue snapshots or performing destructive actions.
- **Dry-run**: Validate snapshot updates with a dry-run option where feasible.

## Validation
- Run syntax checks on all scripts before execution.
- Ensure automated scans fail with useful diagnostics when Axe scans fail or snapshot comparisons detect new violations.

## Failure Handling
- If an Axe scan fails, review the error diagnostics and ensure the target page is accessible.
- If snapshot comparison fails, verify if the changes are expected (e.g., new known issues) and update snapshots only after confirmation.
- Do not repeat a failed scan without addressing the underlying issue.

## Output Contract
- **Structure**: A detailed report of accessibility violations, categorized by severity and WCAG criteria.
- **Evidence**: Violation fingerprints, screenshots (if applicable), and specific DOM nodes affected.
- **Actionable Steps**: Clear remediation recommendations for each new violation.

## Resources
- [Axe-Playwright Integration](references/axe-playwright-integration.md): Guide on using `@axe-core/playwright` and snapshot tracking.
- [Focus Management](references/focus-management.md): Guidelines for testing focus traps and keyboard navigation.
- [Dynamic Trees](references/dynamic-trees.md): Guidelines for testing dynamic hierarchical trees.
- [Source Map](references/source-map.md): Authoritative documentation links.
- [Validate A11y Script](scripts/validate-a11y.sh): Deterministic script to run automated Axe scans.

## Orchestration
- Parallel execution is supported for independent pages or components. Ensure results are synthesized into a single report.
