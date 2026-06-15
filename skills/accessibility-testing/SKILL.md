---
name: accessibility-testing
description: Advanced accessibility testing strategies including snapshot-based known issue tracking, color contrast validation, complex focus management, and dynamic hierarchical trees.
---

# Accessibility Testing Advanced

## When to Use

Use this skill when you need to:
- Implement automated accessibility testing in CI/CD pipelines using Playwright and Axe.
- Manage and track known accessibility issues using snapshot-based tracking to reduce noise.
- Validate color contrast dynamically across dark and light modes, especially with Tailwind CSS and shadcn/ui.
- Ensure proper focus management in complex interactive components like modals, drawers, and popovers.
- Implement and test accessibility in dynamic hierarchical trees (e.g., file explorers, nested menus) following WAI-ARIA Authoring Practices.
- Balance automated testing with manual accessibility audits for comprehensive coverage.

## Sub-Agent Spawning

This skill supports spawning sub-agents for parallel execution when tasks can be decomposed:

| Trigger Condition | Sub-Agent Type | Purpose |
|---|---|---|
| Multiple pages/routes to scan | A11y Scanner | Parallel automated Axe scans across different routes |
| Multiple themes to validate | Contrast Checker | Parallel color contrast validation for light/dark modes |
| Multiple complex components | Interaction Tester | Parallel focus management and keyboard navigation testing |
| Bulk snapshot updates | Snapshot Manager | Parallel updating of known issue snapshots |

### Spawning Rules
- Spawn when 3+ independent pages, components, or themes need accessibility validation.
- Each sub-agent receives: context (e.g., URL, component name), specific target (e.g., dark mode, modal component), success criteria (e.g., zero new violations, correct focus trap).
- Results are aggregated to provide a comprehensive accessibility report.
- Maximum concurrent sub-agents: 10

## Workflow

1.  **Initial Assessment:** Determine the scope of accessibility testing (e.g., full site scan, specific component validation, theme contrast check).
2.  **Automated Scanning:** Use `@axe-core/playwright` to run automated accessibility scans on target pages or components.
3.  **Snapshot Comparison:** Compare scan results against known issue snapshots (`a11y-known-issues.json`) to filter out existing non-critical issues.
4.  **Targeted Validation:**
    *   **Color Contrast:** Emulate media color schemes (`light`/`dark`) and programmatically calculate contrast ratios for text and interactive elements.
    *   **Focus Management:** Simulate keyboard interactions (`Tab`, `Shift+Tab`) to verify focus traps in modals/drawers and logical tab order.
    *   **Dynamic Trees:** Verify ARIA roles (`tree`, `treeitem`, `aria-expanded`) and keyboard navigation (Arrow keys, Space/Enter) in hierarchical components.
5.  **Reporting & Remediation:** Report new violations, update snapshots if necessary, and provide actionable recommendations for fixing identified issues.

## Core Principles

-   **Shift-Left Accessibility:** Integrate automated accessibility checks early in the development lifecycle (CI/CD) to catch regressions quickly.
-   **Signal over Noise:** Utilize snapshot-based tracking to manage known issues, ensuring that test failures indicate genuine new accessibility regressions.
-   **Dynamic Validation:** Static checks are insufficient for modern web apps; validate accessibility dynamically across different states (themes, expanded/collapsed, modal open/closed).
-   **Keyboard First:** Ensure all interactive elements are fully operable via keyboard, as this is foundational for screen reader users and power users alike.
-   **Semantic HTML & ARIA:** Rely on native semantic HTML elements whenever possible, using ARIA attributes only to bridge gaps in complex custom widgets.

## Key References

-   [W3C Web Content Accessibility Guidelines (WCAG) 2.1](https://www.w3.org/TR/WCAG21/)
-   [WAI-ARIA Authoring Practices Guide (APG)](https://www.w3.org/WAI/ARIA/apg/)
-   [Playwright Accessibility Testing Documentation](https://playwright.dev/docs/accessibility-testing)
-   [Axe Core Documentation](https://github.com/dequelabs/axe-core)
