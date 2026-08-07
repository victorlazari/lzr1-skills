# Axe-Playwright Integration

**Verified against upstream: 2026-08-07**

## Overview
This guide details how to integrate `@axe-core/playwright` for automated accessibility testing, focusing on specific WCAG tags and snapshot-based known issue tracking.

## Basic Setup
Ensure `@axe-core/playwright` is installed:
```bash
npm install -D @axe-core/playwright
```

## Running Scans with Tags
Use `AxeBuilder.withTags()` to target specific WCAG criteria:
```javascript
import { test, expect } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';

test('accessibility scan', async ({ page }) => {
  await page.goto('https://example.com');
  const accessibilityScanResults = await new AxeBuilder({ page })
    .withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa'])
    .analyze();

  expect(accessibilityScanResults.violations).toEqual([]);
});
```

## Snapshot-Based Tracking
To manage known issues and reduce noise, use violation fingerprints instead of full objects for snapshot comparisons.

### Generating Fingerprints
Create a helper function to extract stable fingerprints from violations:
```javascript
function createViolationFingerprints(violations) {
  return violations.map(violation => ({
    id: violation.id,
    impact: violation.impact,
    nodes: violation.nodes.map(node => node.target.join(', '))
  }));
}
```

### Using Snapshots in Tests
```javascript
test('accessibility scan with snapshots', async ({ page }) => {
  await page.goto('https://example.com');
  const results = await new AxeBuilder({ page }).analyze();
  const fingerprints = createViolationFingerprints(results.violations);

  // Compare against known issues snapshot
  expect(fingerprints).toMatchSnapshot('known-a11y-issues.json');
});
```
