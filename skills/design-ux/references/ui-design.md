# UI Design

## Table of Contents
1. Visual Design Principles
2. Typography
3. Color Theory
4. Layout and Grid
5. Responsive Design
6. Design Tools

---

## 1. Visual Design Principles

### Gestalt Principles

| Principle | Description | Application |
|---|---|---|
| Proximity | Related items are grouped together | Group form fields, card content |
| Similarity | Similar items are perceived as related | Consistent button styles, icons |
| Continuity | Eye follows smooth paths | Alignment, visual flow |
| Closure | Mind completes incomplete shapes | Icons, progress indicators |
| Figure/Ground | Distinguish foreground from background | Modals, overlays, elevation |
| Common region | Items in same area are grouped | Cards, sections, containers |

### Visual Hierarchy

| Level | Element | Treatment |
|---|---|---|
| 1 (Primary) | Page title, primary CTA | Largest, boldest, high contrast |
| 2 (Secondary) | Section headers, key content | Medium size, semi-bold |
| 3 (Tertiary) | Body text, supporting info | Normal size, regular weight |
| 4 (Quaternary) | Metadata, captions, hints | Smaller, lighter color |

### Spacing System

```
Base unit: 4px (or 8px)
Scale: 4, 8, 12, 16, 24, 32, 48, 64, 96, 128

Usage:
- Inline spacing (between text elements): 4-8px
- Component internal padding: 12-16px
- Between components: 16-24px
- Between sections: 32-64px
- Page margins: 16-64px (responsive)
```

---

## 2. Typography

### Type Scale

| Level | Size | Weight | Use |
|---|---|---|---|
| Display | 48-72px | Bold | Hero headlines |
| H1 | 32-40px | Bold | Page titles |
| H2 | 24-28px | Semi-bold | Section headers |
| H3 | 20-22px | Semi-bold | Subsection headers |
| H4 | 16-18px | Medium | Card titles |
| Body | 16px | Regular | Paragraph text |
| Small | 14px | Regular | Secondary text |
| Caption | 12px | Regular | Labels, metadata |

### Typography Best Practices

| Rule | Guideline | Reason |
|---|---|---|
| Line length | 45-75 characters | Readability |
| Line height | 1.4-1.6× font size | Comfortable reading |
| Paragraph spacing | 0.75-1× line height | Visual separation |
| Font pairing | Max 2-3 typefaces | Consistency |
| Contrast ratio | 4.5:1 minimum (body text) | Accessibility |
| Responsive | Scale down on mobile | Fit viewport |

### Font Selection

| Category | Characteristics | Use Case |
|---|---|---|
| Sans-serif | Clean, modern, screen-optimized | UI, digital products |
| Serif | Traditional, authoritative | Long-form reading, editorial |
| Monospace | Fixed-width, technical | Code, data, tables |
| Display | Decorative, expressive | Headlines, branding |

---

## 3. Color Theory

### Color System Structure

```
Primary:    Brand color (CTAs, key actions)
Secondary:  Supporting brand color
Neutral:    Grays (text, borders, backgrounds)
Success:    Green (confirmations, positive)
Warning:    Yellow/Orange (caution, attention)
Error:      Red (errors, destructive actions)
Info:       Blue (informational, links)
```

### Color Accessibility

| Ratio | WCAG Level | Use Case |
|---|---|---|
| 3:1 | AA (large text) | Headings ≥18px or ≥14px bold |
| 4.5:1 | AA (normal text) | Body text, labels |
| 7:1 | AAA (normal text) | Enhanced accessibility |
| 3:1 | AA (UI components) | Icons, borders, focus indicators |

### Dark Mode Considerations

| Aspect | Light Mode | Dark Mode |
|---|---|---|
| Background | White (#FFFFFF) | Dark gray (#121212, not pure black) |
| Surface | Light gray (#F5F5F5) | Elevated gray (#1E1E1E) |
| Primary text | Dark (#1A1A1A) | Light (#E0E0E0) |
| Secondary text | Medium (#666666) | Medium (#A0A0A0) |
| Elevation | Shadows | Lighter surface colors |
| Accent colors | Full saturation | Desaturated (easier on eyes) |

---

## 4. Layout and Grid

### Grid System

```
12-column grid (most common):
- Columns: 12
- Gutter: 16-24px
- Margin: 16px (mobile), 24px (tablet), 32-64px (desktop)

Common layouts:
- Full width: 12 columns
- Two-thirds + sidebar: 8 + 4 columns
- Equal halves: 6 + 6 columns
- Three equal: 4 + 4 + 4 columns
- Content centered: 2 + 8 + 2 columns
```

### Layout Patterns

| Pattern | Description | Use Case |
|---|---|---|
| F-pattern | Users scan in F shape | Text-heavy pages |
| Z-pattern | Users scan in Z shape | Landing pages, minimal content |
| Card grid | Equal-sized content blocks | Dashboards, galleries |
| Split screen | Two equal panels | Comparison, onboarding |
| Asymmetric | Content + sidebar | Documentation, settings |
| Single column | Focused, linear flow | Forms, articles, mobile |

---

## 5. Responsive Design

### Breakpoints

| Breakpoint | Width | Target |
|---|---|---|
| Mobile S | 320px | Small phones |
| Mobile M | 375px | Standard phones |
| Mobile L | 425px | Large phones |
| Tablet | 768px | Tablets (portrait) |
| Laptop | 1024px | Small laptops, tablets (landscape) |
| Desktop | 1440px | Standard desktops |
| Large | 1920px+ | Large monitors |

### Responsive Strategies

| Strategy | Description | When to Use |
|---|---|---|
| Fluid | Percentage-based widths | Content areas, images |
| Adaptive | Different layouts per breakpoint | Complex layouts |
| Mobile-first | Design mobile, enhance for larger | Most projects |
| Container queries | Respond to parent size | Component-level responsiveness |

---

## 6. Design Tools

### Tool Ecosystem

| Tool | Primary Use | Strengths |
|---|---|---|
| Figma | UI design, prototyping, design systems | Collaborative, web-based |
| Sketch | UI design (macOS) | Mature plugin ecosystem |
| Adobe XD | UI design, prototyping | Adobe ecosystem integration |
| Framer | Advanced prototyping | Code-based interactions |
| Principle | Animation prototyping | Complex animations |
| Miro/FigJam | Collaboration, workshops | Whiteboarding, brainstorming |
| Maze | Usability testing | Figma integration, analytics |
| Hotjar | Behavior analytics | Heatmaps, recordings |

### Design-to-Development Handoff

| Aspect | What to Specify | Format |
|---|---|---|
| Spacing | Margins, padding, gaps | Pixel values or tokens |
| Typography | Font, size, weight, line-height | Design tokens |
| Colors | Exact values, opacity | Hex/RGB/HSL tokens |
| States | Default, hover, active, disabled, focus | All interactive states |
| Responsive | Behavior at each breakpoint | Annotations or specs |
| Motion | Duration, easing, triggers | Animation specs |
| Assets | Icons, images, illustrations | SVG, optimized formats |
