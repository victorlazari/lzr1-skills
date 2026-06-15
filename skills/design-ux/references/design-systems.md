# Design Systems

## Table of Contents
1. Design System Architecture
2. Design Tokens
3. Component Library
4. Documentation
5. Governance

---

## 1. Design System Architecture

### Design System Layers

| Layer | Contents | Consumers |
|---|---|---|
| Foundation | Tokens (color, spacing, typography) | All layers above |
| Core components | Buttons, inputs, cards, modals | Product teams |
| Patterns | Forms, navigation, data display | Product teams |
| Templates | Page layouts, common screens | Product teams |
| Documentation | Guidelines, usage, principles | Everyone |

### Maturity Model

| Level | Characteristics | Team Size |
|---|---|---|
| 1 - Ad hoc | Inconsistent, no shared library | No dedicated team |
| 2 - Managed | Shared Figma library, some components | Part-time contributor |
| 3 - Defined | Coded components, documentation | 1-2 dedicated |
| 4 - Measured | Adoption metrics, versioning | 3-5 dedicated |
| 5 - Optimized | Automated, self-service, community | 5+ dedicated |

---

## 2. Design Tokens

### Token Structure

```
Global tokens → Alias tokens → Component tokens

Example:
  Global:    color.blue.500 = #2563EB
  Alias:     color.primary = color.blue.500
  Component: button.primary.background = color.primary
```

### Token Categories

| Category | Examples | Format |
|---|---|---|
| Color | Primary, secondary, neutral, semantic | Hex, HSL |
| Typography | Font family, size, weight, line-height | px, rem |
| Spacing | Padding, margin, gap | px, rem |
| Border | Width, radius, style | px |
| Shadow | Elevation levels | Box-shadow values |
| Motion | Duration, easing | ms, cubic-bezier |
| Breakpoints | Screen sizes | px |
| Z-index | Stacking order | Integer scale |

### Token Implementation

```json
{
  "color": {
    "primary": {
      "50": { "value": "#EFF6FF", "type": "color" },
      "100": { "value": "#DBEAFE", "type": "color" },
      "500": { "value": "#3B82F6", "type": "color" },
      "700": { "value": "#1D4ED8", "type": "color" },
      "900": { "value": "#1E3A8A", "type": "color" }
    },
    "semantic": {
      "background": { "value": "{color.neutral.50}", "type": "color" },
      "surface": { "value": "{color.neutral.0}", "type": "color" },
      "text-primary": { "value": "{color.neutral.900}", "type": "color" },
      "text-secondary": { "value": "{color.neutral.600}", "type": "color" }
    }
  },
  "spacing": {
    "xs": { "value": "4px", "type": "spacing" },
    "sm": { "value": "8px", "type": "spacing" },
    "md": { "value": "16px", "type": "spacing" },
    "lg": { "value": "24px", "type": "spacing" },
    "xl": { "value": "32px", "type": "spacing" }
  }
}
```

---

## 3. Component Library

### Component Anatomy

| Aspect | Description | Example |
|---|---|---|
| Props/Variants | Configuration options | Size: sm/md/lg, variant: primary/secondary |
| States | Interactive states | Default, hover, active, focus, disabled |
| Slots/Children | Content areas | Icon, label, description |
| Behavior | Interaction logic | Click handler, keyboard navigation |
| Accessibility | ARIA, keyboard, screen reader | Role, label, focus management |

### Component Categories

| Category | Components | Priority |
|---|---|---|
| Actions | Button, IconButton, Link, Menu | Critical |
| Inputs | TextField, Select, Checkbox, Radio, Toggle | Critical |
| Layout | Container, Grid, Stack, Divider | Critical |
| Feedback | Alert, Toast, Dialog, Progress | High |
| Navigation | Tabs, Breadcrumb, Sidebar, Pagination | High |
| Data display | Table, Card, Badge, Avatar, Tooltip | High |
| Overlay | Modal, Drawer, Popover, Dropdown | Medium |
| Media | Image, Video, Carousel, Gallery | Medium |

### Component API Design Principles

- Consistent prop naming across components (size, variant, disabled)
- Composition over configuration (slots/children over complex props)
- Sensible defaults (work out of the box)
- Accessible by default (ARIA, keyboard, focus management)
- Controlled and uncontrolled modes
- Forward refs and spread props for flexibility
- Theme-aware (respond to design tokens)

---

## 4. Documentation

### Documentation Structure

| Section | Content | Audience |
|---|---|---|
| Getting started | Installation, setup, quick start | Developers |
| Design principles | Philosophy, decision framework | Designers + developers |
| Foundations | Tokens, color, typography, spacing | Designers + developers |
| Components | Usage, props, examples, do/don't | Developers |
| Patterns | Common UI patterns, best practices | Designers + developers |
| Resources | Assets, templates, tools | Everyone |
| Changelog | Version history, migration guides | Developers |

### Component Documentation Template

```markdown
# Button

## Overview
Brief description of the component and when to use it.

## Variants
- Primary: Main actions (one per section)
- Secondary: Supporting actions
- Tertiary: Low-emphasis actions
- Destructive: Irreversible actions

## Props
| Prop | Type | Default | Description |
|---|---|---|---|
| variant | string | "primary" | Visual style |
| size | string | "md" | sm, md, lg |
| disabled | boolean | false | Disable interaction |
| loading | boolean | false | Show loading state |

## Usage Guidelines
### Do
- Use primary for the main action
- Use consistent sizing within a group

### Don't
- Don't use multiple primary buttons in one section
- Don't use disabled buttons without explanation

## Accessibility
- Keyboard: Enter/Space to activate
- ARIA: role="button" (automatic for <button>)
- Focus: Visible focus indicator
```

---

## 5. Governance

### Contribution Model

| Model | Description | Best For |
|---|---|---|
| Centralized | Core team owns everything | Small orgs, early stage |
| Federated | Teams contribute, core team reviews | Medium orgs |
| Community | Open contribution with guidelines | Large orgs, mature systems |

### Versioning Strategy

| Change Type | Version Bump | Example |
|---|---|---|
| Bug fix | Patch (0.0.x) | Fix button focus ring |
| New component/feature | Minor (0.x.0) | Add Tooltip component |
| Breaking change | Major (x.0.0) | Rename prop, remove component |

### Adoption Metrics

| Metric | Description | Target |
|---|---|---|
| Coverage | % of UI using system components | >80% |
| Adoption rate | New features using system | >90% |
| Contribution rate | External contributions per quarter | Growing |
| Satisfaction | Developer/designer satisfaction | >4.0/5.0 |
| Consistency | Visual consistency score | >90% |
