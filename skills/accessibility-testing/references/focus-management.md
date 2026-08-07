# Focus Management

**Verified against upstream: 2026-08-07**

## Overview
Guidelines and examples for testing focus traps and keyboard navigation in complex components like modals, drawers, and popovers, aligning with WAI-ARIA APG patterns.

## Testing Focus Traps
When a modal or dialog is open, focus must be trapped within it.

### Playwright Test Example
```javascript
test('modal traps focus', async ({ page }) => {
  await page.goto('/components/modal');
  await page.click('button[aria-haspopup="dialog"]');

  // Verify focus is moved into the modal
  const modal = page.locator('[role="dialog"]');
  await expect(modal).toBeVisible();

  // Press Tab and verify focus stays within the modal
  await page.keyboard.press('Tab');
  let focusedElement = await page.evaluate(() => document.activeElement.tagName);
  // Assert focusedElement is within the modal

  // Press Shift+Tab and verify focus stays within the modal
  await page.keyboard.press('Shift+Tab');
  focusedElement = await page.evaluate(() => document.activeElement.tagName);
  // Assert focusedElement is within the modal
});
```

## Keyboard Navigation
Ensure all interactive elements are reachable via keyboard (Tab/Shift+Tab) and can be activated using Enter or Space.

### Playwright Test Example
```javascript
test('keyboard navigation', async ({ page }) => {
  await page.goto('/components/menu');

  // Tab to the menu button
  await page.keyboard.press('Tab');
  await expect(page.locator('button[aria-haspopup="menu"]')).toBeFocused();

  // Open menu with Enter
  await page.keyboard.press('Enter');
  await expect(page.locator('[role="menu"]')).toBeVisible();

  // Navigate menu items with arrow keys (if applicable per APG)
  await page.keyboard.press('ArrowDown');
  await expect(page.locator('[role="menuitem"]').first()).toBeFocused();
});
```
