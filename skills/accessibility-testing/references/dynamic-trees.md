# Dynamic Trees

**Verified against upstream: 2026-08-07**

## Overview
Guidelines for testing dynamic hierarchical trees (e.g., file explorers, nested menus) following WAI-ARIA APG patterns.

## WAI-ARIA APG Tree Pattern
A tree view is a widget that presents a hierarchical list. Key requirements:
- `role="tree"` on the container.
- `role="treeitem"` on each node.
- `role="group"` for nested collections.
- `aria-expanded` on nodes with children.
- `aria-selected` for selection state.

## Keyboard Interaction Testing
Tree views require specific keyboard interactions:
- **Up/Down Arrow**: Move focus to previous/next visible node.
- **Right Arrow**: Expand a collapsed node or move to the first child of an expanded node.
- **Left Arrow**: Collapse an expanded node or move to the parent of a child node.
- **Enter/Space**: Select a node.

### Playwright Test Example
```javascript
test('tree view keyboard navigation', async ({ page }) => {
  await page.goto('/components/tree');

  // Focus the tree
  await page.keyboard.press('Tab');
  const firstItem = page.locator('[role="treeitem"]').first();
  await expect(firstItem).toBeFocused();

  // Expand node with Right Arrow
  await page.keyboard.press('ArrowRight');
  await expect(firstItem).toHaveAttribute('aria-expanded', 'true');

  // Move to child with Right Arrow
  await page.keyboard.press('ArrowRight');
  const childItem = page.locator('[role="group"] [role="treeitem"]').first();
  await expect(childItem).toBeFocused();

  // Collapse node with Left Arrow (from child)
  await page.keyboard.press('ArrowLeft');
  await expect(firstItem).toBeFocused();
  await page.keyboard.press('ArrowLeft');
  await expect(firstItem).toHaveAttribute('aria-expanded', 'false');
});
```
