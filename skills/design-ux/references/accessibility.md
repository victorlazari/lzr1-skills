# Accessibility

## Table of Contents
1. WCAG Guidelines
2. ARIA
3. Keyboard Navigation
4. Screen Readers
5. Testing and Auditing

---

## 1. WCAG Guidelines

### WCAG 2.2 Principles (POUR)

| Principle | Description | Key Success Criteria |
|---|---|---|
| Perceivable | Information must be presentable to all senses | Text alternatives, captions, contrast |
| Operable | Interface must be operable by all users | Keyboard, timing, seizures, navigation |
| Understandable | Information and UI must be understandable | Readable, predictable, input assistance |
| Robust | Content must work with assistive technologies | Parsing, name/role/value |

### Key Success Criteria

| Criterion | Level | Requirement |
|---|---|---|
| 1.1.1 Non-text Content | A | Alt text for images |
| 1.3.1 Info and Relationships | A | Semantic HTML structure |
| 1.4.3 Contrast (Minimum) | AA | 4.5:1 text, 3:1 large text |
| 1.4.11 Non-text Contrast | AA | 3:1 for UI components |
| 2.1.1 Keyboard | A | All functionality via keyboard |
| 2.4.3 Focus Order | A | Logical focus sequence |
| 2.4.7 Focus Visible | AA | Visible focus indicator |
| 2.5.8 Target Size | AA | 24×24px minimum (WCAG 2.2) |
| 3.3.2 Labels or Instructions | A | Labels for form inputs |
| 4.1.2 Name, Role, Value | A | Programmatic name for controls |

### Conformance Levels

| Level | Description | Typical Target |
|---|---|---|
| A | Minimum accessibility | Legal minimum |
| AA | Standard accessibility | Most organizations target this |
| AAA | Enhanced accessibility | Specific content/audiences |

---

## 2. ARIA

### ARIA Roles

| Category | Roles | Use Case |
|---|---|---|
| Landmark | banner, navigation, main, complementary | Page structure |
| Widget | button, checkbox, dialog, tab, menu | Interactive components |
| Document | article, heading, list, table | Content structure |
| Live region | alert, status, log, timer | Dynamic updates |

### Common ARIA Patterns

```html
<!-- Accessible button (when not using <button>) -->
<div role="button" tabindex="0" aria-pressed="false"
     onkeydown="handleKeyDown(event)">
  Toggle Feature
</div>

<!-- Accessible dialog -->
<div role="dialog" aria-modal="true" aria-labelledby="dialog-title">
  <h2 id="dialog-title">Confirm Action</h2>
  <p>Are you sure you want to proceed?</p>
  <button>Cancel</button>
  <button>Confirm</button>
</div>

<!-- Accessible tabs -->
<div role="tablist" aria-label="Settings">
  <button role="tab" aria-selected="true" aria-controls="panel-1">General</button>
  <button role="tab" aria-selected="false" aria-controls="panel-2">Security</button>
</div>
<div role="tabpanel" id="panel-1" aria-labelledby="tab-1">...</div>

<!-- Live region for dynamic content -->
<div aria-live="polite" aria-atomic="true">
  3 items added to cart
</div>
```

### ARIA Best Practices

| Rule | Description |
|---|---|
| First rule of ARIA | Don't use ARIA if native HTML works |
| No ARIA is better than bad ARIA | Incorrect ARIA is worse than none |
| All interactive ARIA elements need keyboard support | role="button" needs Enter/Space |
| Don't change native semantics | Don't add role="button" to a link |
| All interactive elements must have accessible names | aria-label or aria-labelledby |

---

## 3. Keyboard Navigation

### Focus Management

| Pattern | Implementation | Use Case |
|---|---|---|
| Tab order | tabindex="0" (in DOM order) | Standard navigation |
| Skip links | Hidden link to main content | Skip repetitive navigation |
| Focus trap | Contain focus within component | Modals, dialogs |
| Focus restore | Return focus after closing | Modal close, delete action |
| Roving tabindex | One tab stop, arrows to navigate | Toolbars, tab lists |

### Keyboard Shortcuts

| Key | Standard Action |
|---|---|
| Tab | Move to next focusable element |
| Shift+Tab | Move to previous focusable element |
| Enter | Activate button/link |
| Space | Activate button, toggle checkbox |
| Escape | Close modal/dropdown/tooltip |
| Arrow keys | Navigate within component (tabs, menus) |
| Home/End | First/last item in list |

---

## 4. Screen Readers

### Screen Reader Behavior

| Element | Announced As | Requirement |
|---|---|---|
| `<button>` | "Button, [label]" | Visible text or aria-label |
| `<a href>` | "Link, [text]" | Descriptive link text |
| `<img alt="...">` | "Image, [alt text]" | Meaningful alt text |
| `<input>` | "[Label], edit text" | Associated `<label>` |
| Heading | "Heading level N, [text]" | Proper hierarchy |
| Landmark | "Navigation/Main/..." | Semantic HTML or role |

### Writing Accessible Content

| Element | Good | Bad |
|---|---|---|
| Link text | "View order details" | "Click here" |
| Alt text | "Bar chart showing 23% revenue growth" | "chart.png" |
| Button text | "Delete message" | "X" (without aria-label) |
| Error message | "Email is required" | "Error" |
| Form label | "Email address" | Placeholder only |

---

## 5. Testing and Auditing

### Testing Tools

| Tool | Type | Tests |
|---|---|---|
| axe DevTools | Automated | WCAG violations in DOM |
| Lighthouse | Automated | Accessibility score + issues |
| WAVE | Automated | Visual overlay of issues |
| VoiceOver (macOS) | Manual | Screen reader testing |
| NVDA (Windows) | Manual | Screen reader testing |
| Keyboard only | Manual | All functionality without mouse |
| Color contrast analyzers | Automated | Contrast ratio checking |

### Audit Checklist

| Category | Check | Method |
|---|---|---|
| Structure | Proper heading hierarchy | Inspect headings |
| Images | Meaningful alt text | Review all images |
| Forms | Labels associated with inputs | Inspect form elements |
| Color | Sufficient contrast ratios | Contrast checker |
| Keyboard | All interactive elements reachable | Tab through page |
| Focus | Visible focus indicators | Tab through page |
| Dynamic | Live regions for updates | Screen reader test |
| Motion | Respects prefers-reduced-motion | Media query check |
| Responsive | Accessible at all breakpoints | Test at each size |
| Language | lang attribute set | Inspect HTML |
