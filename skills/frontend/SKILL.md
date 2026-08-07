---
name: frontend
description: Advanced Frontend Specialist Guide covering React, Next.js App Router, Server Components, TypeScript, Tailwind CSS, State Management, Testing & Performance.
---

# Frontend Specialist Skill

## Scope and Triggers
Use this skill when tasked with building, auditing, or optimizing modern frontend applications. It is particularly suited for projects utilizing React, Next.js (especially the App Router and Server Components), TypeScript, and Tailwind CSS. This skill should be invoked when dealing with complex state management, intricate testing strategies, or performance bottlenecks in web applications.

## Preconditions
- Verify the target environment, installed versions of React, Next.js, TypeScript, and Tailwind CSS.
- Ensure necessary permissions are granted for any file modifications or package installations.
- Understand the user's intent and specific goals for the frontend task.

## Source Freshness
Consult `references/source-map.md` for canonical URLs and verification dates of official documentation. Always verify volatile facts, such as supported versions or configuration schemas, against these sources rather than relying on static examples.

## Workflow
1. **Assess current state:** Identify technologies, versions, and goals.
2. **Verify dependencies:** Run `scripts/audit-deps.sh` to ensure compatibility.
3. **Select architecture:** Choose patterns and state management strategies based on assessment.
4. **Implement changes:** Apply modifications iteratively, separating read-only discovery from mutations.
5. **Validate:** Run syntax checks, tests, and performance profiling.
6. **Stop condition:** Stop when all tests pass, performance metrics are met, and no actionable findings remain.

## Safety
- Separate read-only discovery from mutations.
- Require confirmation before modifying production resources or executing destructive actions.
- Do not execute downloaded code without verification.

## Validation
- Run syntax checks (e.g., `tsc --noEmit`) and smoke tests after modifications.
- Validate installed dependency versions using `scripts/audit-deps.sh` before applying changes.
- Provide rollback guidance for failed migrations or updates.

## Failure Handling
- Diagnose errors using logs and error messages.
- Choose alternative approaches if a specific method fails.
- Roll back changes if a migration or update fails.
- Do not repeat a failed action unchanged.

## Output Contract
- Provide a structured summary of changes made.
- Include evidence of successful validation (e.g., test results, performance metrics).
- State any known limitations or unresolved issues.
- Suggest actionable next steps if applicable.

## Resources
- `references/react-patterns.md`: Focused reference for React fundamentals and advanced patterns.
- `references/nextjs-app-router.md`: Focused reference for Next.js App Router and Server Components.
- `references/state-management.md`: Focused reference for state management strategies.
- `references/testing-strategies.md`: Focused reference for testing methodologies.
- `references/performance-optimization.md`: Focused reference for performance optimization techniques.
- `references/source-map.md`: Source map linking to canonical documentation with verification dates.
- `scripts/audit-deps.sh`: Deterministic script to verify installed versions of React, Next.js, TypeScript, and Tailwind CSS.

## Orchestration
- Use parallel work only for independent dimensions.
- Define inputs, schemas, conflict handling, synthesis, and termination conditions for parallel tasks.

## Cross-Skill Routing
- Route to `security-review` when performing deep security audits or vulnerability assessments.
- Route to `webdev-readme-fullstack` when initializing or configuring a fullstack webdev project.
- Route to `webdev-readme-mobile` when initializing or configuring a mobile app project.
- Route to `webdev-readme-static` when initializing or configuring a static webdev project.
