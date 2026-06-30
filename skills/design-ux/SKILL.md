---
name: design-ux
description: Comprehensive design and UX skill covering user experience design, UI design, design systems, user research, accessibility, interaction design, and information architecture. Use when designing interfaces, creating design systems, conducting UX research, improving usability, building prototypes, or establishing design standards.
---

# Design & UX

Expert-level design covering user experience, interface design, design systems, research methods, accessibility, and interaction patterns for digital products.

## When to Use

- Designing user interfaces and interactions
- Building or maintaining design systems
- Conducting user research and usability testing
- Improving product accessibility (WCAG compliance)
- Creating information architecture and navigation
- Establishing design principles and standards
- Prototyping and wireframing
- Design critique and review

## Workflow

1. **Understand the problem** — Who are the users? What are their goals?
2. **Select reference** — Choose the appropriate design domain:
   - UX process and research → `references/ux-research.md`
   - UI design and visual design → `references/ui-design.md`
   - Design systems → `references/design-systems.md`
   - Accessibility → `references/accessibility.md`
   - Interaction design → `references/interaction-design.md`
3. **Research** — Understand users, context, and constraints
4. **Design** — Create solutions informed by principles and patterns
5. **Validate** — Test with users, iterate based on feedback
6. **Document** — Specifications, guidelines, and handoff materials

## Core Principles (All Design Work)

- User-centered: Every design decision should serve user needs
- Accessibility first: Design for all abilities from the start (not retrofitted)
- Consistency: Use established patterns; deviate only with good reason
- Simplicity: Remove complexity; every element must earn its place
- Feedback: Users should always know what's happening and what to do next
- Error prevention: Design to prevent errors, not just handle them
- Progressive disclosure: Show only what's needed at each step
- Evidence-based: Validate assumptions with research and data

## Role Capabilities

| Role | Expertise | Reference |
|---|---|---|
| UX Designer | Research, flows, wireframes | `references/ux-research.md` |
| UI Designer | Visual design, typography, color | `references/ui-design.md` |
| Design System Lead | Components, tokens, documentation | `references/design-systems.md` |
| UX Researcher | Methods, testing, synthesis | `references/ux-research.md` |
| Accessibility Specialist | WCAG, assistive tech, audits | `references/accessibility.md` |
| Interaction Designer | Motion, micro-interactions, patterns | `references/interaction-design.md` |
| Information Architect | Navigation, taxonomy, structure | `references/interaction-design.md` |

## Key References

- **UX research**: See `references/ux-research.md` for methods, testing, and synthesis.
- **UI design**: See `references/ui-design.md` for visual design, typography, and layout.
- **Design systems**: See `references/design-systems.md` for components, tokens, and governance.
- **Accessibility**: See `references/accessibility.md` for WCAG, ARIA, and inclusive design.
- **Interaction design**: See `references/interaction-design.md` for patterns and motion.
- **Recommended reading**: See `references/reading-list.md` for curated books and articles.

---

## Multi-Specialist Protocol

> **Replaces the single "Select reference" step.** When multiple domains are detected, spawn all relevant specialists simultaneously — do not serialize them.

### Domain Detection Table

Scan the task for signals that indicate which domains apply:

| Task Signal (examples) | Domain | Specialist Agent | Reference |
|---|---|---|---|
| `user research`, ... | **UX Research** | UX Research Specialist | `references/ux-research.md` |
| `interaction`, ... | **Interaction Design** | Interaction Specialist | `references/interaction-design.md` |
| `visual`, ... | **UI Design** | UI Design Specialist | `references/ui-design.md` |
| `design system`, ... | **Design Systems** | Design Systems Specialist | `references/design-systems.md` |
| `accessibility`, ... | **Accessibility** | A11y Specialist | `references/accessibility.md` |

### Spawning Logic

**Single domain detected** → Fall back to original single-reference behavior (no change).

**Multiple domains detected** → Launch all relevant specialists simultaneously:
- Each specialist receives: **full task context** + its dedicated reference file only
- No specialist waits for another — all start at the same time
- Maximum concurrent specialists: 5

### Cross-Domain Synthesizer

After all specialists complete, run one **Design System Synthesizer** with all specialist outputs that:

1. **Identifies contradictions** between specialist recommendations for the same component
2. **Identifies gaps** — requirements addressed by no specialist
3. **Identifies dependencies** — where Domain A's output is a prerequisite for Domain B's recommendation
4. **Produces** a unified recommendation with explicit trade-off annotations for any resolved contradictions

> Synthesis focus for this skill: Ensures accessibility requirements are baked into design system components before handoff, not retrofitted. Maps UX research findings to interaction design decisions.
