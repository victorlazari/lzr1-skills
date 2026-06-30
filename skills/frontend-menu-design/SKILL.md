---
name: frontend-menu-design
description: Advanced frontend menu architecture, focusing on usability, accessibility, security, performance, and modern React/Next.js ecosystems.
---

# Frontend Menu Design

## When to Use

Use this skill when designing, implementing, or auditing frontend menu systems in modern web applications. It is particularly relevant for:
- Building complex mega menus or deeply nested navigation structures.
- Implementing Role-Based Access Control (RBAC) within UI navigation.
- Integrating menus with Next.js App Router (layouts, intercepting routes, prefetching).
- Orchestrating advanced menu animations using Framer Motion.
- Ensuring WCAG accessibility compliance and keyboard navigation.
- Optimizing menu performance (lazy loading, CSS containment).
- Developing mobile-first responsive navigation (drawers, swipe gestures).
- Securing menus against XSS and enforcing Content Security Policies (CSP).

## Sub-Agent Spawning

This skill supports spawning sub-agents for parallel execution when tasks can be decomposed:

| Trigger Condition | Sub-Agent Type | Purpose |
|---|---|---|
| Multiple menu components to audit | Accessibility Auditor | Parallel WCAG compliance review of each menu component |
| Multiple user roles to validate | RBAC Validator | Parallel verification of menu visibility per role |
| Multiple framework integrations | Integration Specialist | Parallel setup of menu components across different frameworks |
| Bulk animation orchestration | Animation Engineer | Parallel implementation of Framer Motion variants |

### Spawning Rules
- Spawn when 3+ independent items need the same operation
- Each sub-agent receives: context, specific target, success criteria
- Results are aggregated and cross-referenced for conflicts
- Maximum concurrent sub-agents: 10

## Workflow

1.  **Requirements Gathering & Architecture:**
    *   Determine the complexity of the menu (basic, mega-menu, sidebar, radial).
    *   Identify the target framework (React, Next.js, Vue, etc.).
    *   Define user roles and required RBAC filtering.
2.  **Component Scaffolding:**
    *   Utilize the `frontend-menu-design` CLI to initialize the project or generate specific components (`item`, `dropdown`, `group`).
    *   Establish the state management strategy (controlled vs. uncontrolled, Context API).
3.  **Implementation & Integration:**
    *   Implement server-side and client-side RBAC validation (e.g., `PermissionGate`).
    *   Integrate with routing mechanisms (e.g., Next.js `usePathname`, intercepting routes).
    *   Apply UI primitives like Radix UI for accessible foundations.
4.  **Animation & Styling:**
    *   Orchestrate animations using Framer Motion (staggered children, spring physics).
    *   Apply responsive design strategies (hamburger menus, touch targets).
5.  **Security & Performance Optimization:**
    *   Sanitize dynamic labels using DOMPurify.
    *   Implement strict Content Security Policies (CSP).
    *   Apply performance optimizations (lazy loading submenus, CSS containment).
6.  **Testing & Validation:**
    *   Conduct accessibility audits (keyboard navigation, ARIA attributes).
    *   Verify RBAC enforcement across all roles.

## Core Principles

-   **Security First:** RBAC must be enforced on the server side; client-side hiding is only for usability. Sanitize all dynamic content.
-   **Accessibility is Mandatory:** Menus must be fully navigable via keyboard and screen readers, adhering to WAI-ARIA patterns.
-   **Performance Matters:** Complex menus should not degrade application performance. Utilize lazy loading and CSS containment.
-   **Progressive Enhancement:** Core navigation should function without JavaScript where possible, with advanced features layered on top.
-   **Declarative Animation:** Use tools like Framer Motion for predictable, performant, and maintainable animation orchestration.

## Key References

-   Radix UI Navigation Menu Documentation
-   Framer Motion React Animation
-   Next.js App Router Documentation
-   WAI-ARIA Menubar Pattern
-   DOMPurify GitHub Repository
-   OWASP XSS Prevention Cheat Sheet

---

## Adversarial Verification Panel

For each significant menu design recommendation produced by the parallel sub-agents:

1. Spawn **3 independent Refuter Agents** per finding, each with:
   - The finding in full
   - Instruction: *"Assume this finding is wrong. Find the strongest argument against it."*
   - Default stance: `refuted=true` if evidence is insufficient or ambiguous
2. A finding is **confirmed** only if ≥2 refuters fail to refute it
3. A finding is **discarded** if ≥2 refuters succeed
4. When a confirmed finding had 1 successful refuter, include the dissenting argument in the output with a `CONTESTED` label

> This prevents plausible-but-wrong menu design recommendations from reaching the final output. The 3-vote panel eliminates single-point hallucination without requiring unanimity.

## Cross-System Consistency Validator

After all parallel agents (Accessibility Auditor, RBAC Validator, Integration Specialist, Animation Engineer) complete, but **before** synthesis:

Run one **Consistency Validator Agent** with all parallel outputs that:
- Flags any pair of recommendations that logically contradict each other
  *(example: Animation Engineer recommends heavy Framer Motion stagger animations while the Accessibility Auditor flags that same animation as violating prefers-reduced-motion requirements)*
- Notes where one agent's output is a prerequisite for another agent's recommendation
- Passes contradictions to the Synthesis Agent as `MUST_RESOLVE` items
- Passes missing prerequisites as `SEQUENCING_REQUIRED` items

## Synthesis Agent (Upgraded)

The synthesis step actively resolves rather than aggregates:

1. **`MUST_RESOLVE` contradictions**: Pick the better recommendation, annotate the reasoning, preserve the dissenting view as a footnote
2. **`SEQUENCING_REQUIRED` items**: Re-order the unified menu design report so prerequisites appear before the steps that depend on them
3. **Confidence calibration**: Label each finding `HIGH` / `MEDIUM` / `LOW` confidence based on refuter panel outcomes
4. **Gap analysis**: Note any analysis dimension not covered by any of the parallel agents — these are blind spots, not confirmed negatives
