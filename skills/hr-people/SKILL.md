---
name: hr-people
description: Comprehensive HR and people operations skill covering talent acquisition, people operations, organizational development, compensation and benefits, employee experience, and HR analytics. Use when designing hiring processes, building org structures, creating compensation frameworks, developing culture programs, or managing people operations.
---

# HR & People Operations

Expert-level HR covering talent acquisition, people operations, organizational development, compensation, employee experience, and HR analytics for technology companies.

## Scope and Triggers

- **Scope**: Designing hiring processes, building organizational structures, creating compensation and equity programs, developing culture programs, managing performance reviews, HR compliance, and people analytics.
- **Triggers**: Use when the task involves HR policies, job descriptions, compensation bands, org design, or people operations.
- **Non-goals**: Does not handle code review, IDE extensions, or AST analysis (route to `coderabbit-reviewer`). Does not handle financial modeling, equity valuation, or company financial analysis beyond basic compensation (route to `finance-pro-playbooks`).

## Preconditions

- Detect the specific HR domain (compensation, org design, talent acquisition, people ops) based on task signals.
- Identify the target audience, company stage, and geographic location.
- Verify if the task involves volatile legal or compliance facts.

## Source Freshness

- For volatile legal or compliance facts, consult the source map (`references/source-map.md`) to verify current requirements.
- Ensure all generated compensation bands comply with specified state transparency laws.

## Workflow

1. **Detect Domain**: Scan the task for signals that indicate which domains apply:
   - Hiring and recruiting → `references/talent-acquisition.md`
   - Org design and development → `references/org-development.md`
   - Compensation and equity → `references/compensation.md`
   - People ops and compliance → `references/people-ops.md`
2. **Route**: Route to the appropriate reference file for domain-specific guidelines and 2026 compliance rules.
3. **Verify**: If the task involves volatile legal or compliance facts, consult the source map (`references/source-map.md`) to verify current requirements.
4. **Generate**: Generate the requested HR artifact (policy, job description, compensation band, etc.) applying the relevant guidelines.
5. **Validate**: Validate the artifact against safety and compliance constraints (e.g., salary transparency laws).
6. **Present**: Present the artifact to the user, requesting confirmation for any legally binding or sensitive outputs.

## Safety

- **Read-only**: Separate read-only discovery from mutations.
- **Confirmation**: Require confirmation before generating legally binding HR policies or compliance documents.
- **Privacy**: Ensure no PII or sensitive employee data is processed without explicit user consent.
- **Dry-run**: Provide dry-run outputs for org design changes.

## Validation

- Validate that all generated compensation bands comply with specified state transparency laws.
- Ensure the artifact meets the requirements specified in the relevant reference file.

## Failure Handling

- If a compliance check fails, notify the user and request guidance or updated information.
- If a domain cannot be determined, ask the user for clarification.

## Output Contract

- The output must be a structured artifact (policy, job description, compensation band, etc.) that adheres to the guidelines in the relevant reference file.
- Include explicit trade-off annotations for any resolved contradictions.
- State any assumptions made during generation.

## Resources

- `references/talent-acquisition.md`: Hiring and recruiting guidelines.
- `references/org-development.md`: Org design and development guidelines.
- `references/compensation.md`: Compensation and equity guidelines, including 2026 compliance.
- `references/people-ops.md`: People ops and compliance guidelines, including 2026 updates.
- `references/source-map.md`: Source map for consulting external sources for volatile legal or compliance information.

## Orchestration

- Use parallel work only for independent dimensions.
- Define inputs, schemas, conflict handling, synthesis, and termination conditions for parallel tasks.
