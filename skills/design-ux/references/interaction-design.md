# Interaction Design

## Table of Contents
1. Interaction Patterns
2. Motion Design
3. Information Architecture
4. Navigation Patterns
5. Form Design

---

## 1. Interaction Patterns

### Common UI Patterns

| Pattern | Use Case | Key Considerations |
|---|---|---|
| Progressive disclosure | Complex interfaces | Show only what's needed now |
| Infinite scroll | Content feeds | Provide "back to top", preserve position |
| Pagination | Structured content, tables | Show total, current position |
| Skeleton loading | Content loading | Match layout shape |
| Optimistic UI | Fast-feeling actions | Handle failure gracefully |
| Undo vs Confirm | Destructive actions | Undo for reversible, confirm for irreversible |
| Drag and drop | Reordering, organizing | Keyboard alternative required |
| Command palette | Power users | Cmd+K, searchable actions |
| Contextual menus | Object actions | Right-click or more button |
| Inline editing | Quick edits | Click to edit, clear save/cancel |

### Feedback Patterns

| Action | Feedback Type | Timing |
|---|---|---|
| Button click | Visual state change | Immediate (<100ms) |
| Form submit | Loading indicator | Immediate, then result |
| Background process | Progress bar or status | Continuous updates |
| Error | Inline message + highlight | Immediate on submit or on blur |
| Success | Toast/snackbar notification | After completion |
| Destructive action | Confirmation or undo | Before or immediately after |

### State Management

| State | Visual Treatment | User Action |
|---|---|---|
| Empty | Illustration + guidance | First-time use, no data |
| Loading | Skeleton or spinner | Waiting for data |
| Partial | Some content + loading | Progressive loading |
| Complete | Full content | Normal state |
| Error | Error message + retry | Something went wrong |
| Offline | Offline indicator + cached | No connection |

---

## 2. Motion Design

### Motion Principles

| Principle | Description | Example |
|---|---|---|
| Purpose | Every animation must have a reason | Guide attention, show relationship |
| Speed | Fast enough to not delay, slow enough to perceive | 150-300ms for most transitions |
| Easing | Natural acceleration/deceleration | ease-out for enter, ease-in for exit |
| Consistency | Same type of motion for same type of action | All modals animate the same way |
| Accessibility | Respect prefers-reduced-motion | Disable or reduce animations |

### Duration Guidelines

| Animation Type | Duration | Easing |
|---|---|---|
| Micro-interaction (button, toggle) | 100-200ms | ease-out |
| Small transition (tooltip, dropdown) | 150-250ms | ease-out |
| Medium transition (modal, panel) | 200-350ms | ease-in-out |
| Large transition (page, full-screen) | 300-500ms | ease-in-out |
| Complex sequence | 400-700ms total | Orchestrated |

### Common Animation Patterns

| Pattern | Use | Implementation |
|---|---|---|
| Fade | Appear/disappear | opacity: 0 → 1 |
| Scale | Emphasis, appear | transform: scale(0.95) → scale(1) |
| Slide | Panels, drawers | transform: translateX(-100%) → 0 |
| Expand/Collapse | Accordions, details | height: 0 → auto (or max-height) |
| Stagger | Lists, grids | Delay each item by 50-100ms |
| Morph | State change | Shared element transition |

---

## 3. Information Architecture

### IA Methods

| Method | Purpose | Output |
|---|---|---|
| Card sorting (open) | Discover user mental models | Category structure |
| Card sorting (closed) | Validate proposed structure | Category fit |
| Tree testing | Validate navigation findability | Success rates per task |
| Content audit | Inventory existing content | Content matrix |
| Site mapping | Visualize structure | Hierarchical diagram |

### Navigation Structures

| Structure | Description | Best For |
|---|---|---|
| Hierarchical | Tree structure (parent → child) | Large sites, documentation |
| Flat | All pages at same level | Small sites, apps |
| Hub and spoke | Central hub with spokes | Mobile apps, dashboards |
| Network | Interconnected (links between any) | Wikis, knowledge bases |
| Sequential | Linear progression | Onboarding, wizards |

### Content Organization Schemes

| Scheme | Organization By | Example |
|---|---|---|
| Alphabetical | A-Z | Glossary, directory |
| Chronological | Time | Blog, news, timeline |
| Geographical | Location | Store locator, maps |
| Topical | Subject matter | Documentation sections |
| Task-based | User goals | "I want to..." |
| Audience | User type | Admin vs user vs developer |

---

## 4. Navigation Patterns

### Navigation Types

| Pattern | Use Case | Placement |
|---|---|---|
| Top navigation | Primary nav, few items (5-7) | Header |
| Side navigation | Many items, deep hierarchy | Left sidebar |
| Bottom navigation | Mobile, 3-5 primary actions | Footer (mobile) |
| Breadcrumbs | Deep hierarchy, wayfinding | Below header |
| Tabs | Related content sections | Within content area |
| Mega menu | Large sites, many categories | Dropdown from top nav |
| Command palette | Power users, quick access | Overlay (Cmd+K) |

### Mobile Navigation

| Pattern | Items | Depth | Example |
|---|---|---|---|
| Tab bar | 3-5 | Flat | iOS tab bar |
| Hamburger menu | Many | Deep | Slide-out drawer |
| Bottom sheet | Variable | Contextual | Action sheets |
| Segmented control | 2-4 | Flat | View switcher |

---

## 5. Form Design

### Form Best Practices

| Practice | Description | Reason |
|---|---|---|
| Single column | One field per row | Faster completion |
| Top-aligned labels | Label above input | Fastest scanning |
| Logical grouping | Related fields together | Reduce cognitive load |
| Smart defaults | Pre-fill when possible | Reduce effort |
| Inline validation | Validate on blur | Immediate feedback |
| Clear error messages | Specific, actionable | Help users fix issues |
| Progress indication | Show steps in multi-step | Set expectations |
| Optional marking | Mark optional (not required) | Most fields should be required |

### Input Types

| Data | Input Type | Validation |
|---|---|---|
| Short text | Text input | Length, format |
| Long text | Textarea | Length |
| Email | Email input | Email format |
| Number | Number input | Range, precision |
| Date | Date picker | Range, format |
| Selection (few) | Radio buttons / Segmented | Required |
| Selection (many) | Dropdown / Combobox | Required |
| Multiple selection | Checkboxes / Multi-select | Min/max selections |
| Boolean | Toggle / Checkbox | N/A |
| File | File upload | Type, size |

### Error Handling

| Timing | Method | Best For |
|---|---|---|
| On submit | Validate all, show summary + inline | Simple forms |
| On blur | Validate field when leaving | Complex forms |
| On change | Real-time validation | Password strength, username |
| Hybrid | On blur + on submit | Most forms |

### Error Message Format

```
[Field label]: [What went wrong] + [How to fix it]

Good: "Email address: Please enter a valid email (e.g., name@company.com)"
Bad:  "Invalid input"
Bad:  "Error in field 3"
```
