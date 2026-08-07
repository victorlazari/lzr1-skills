---
name: customer-support
description: Comprehensive customer support skill covering support operations, technical support, knowledge management, support metrics, and customer experience for technology companies. Use when building support processes, creating help documentation, designing escalation workflows, measuring support quality, or implementing support tools.
---

# Customer Support

Expert-level customer support covering support operations, technical support, knowledge management, metrics, and customer experience for technology companies.

## Scope and Triggers

- **Triggers**: Use when building support processes, creating help documentation, designing escalation workflows, measuring support quality, or implementing support tools.
- **Scope**: Support operations, technical support, knowledge management, metrics, and customer experience.
- **Non-goals**: Not for direct customer interaction, not for building software features, not for marketing campaigns.

## Preconditions

- Identify the target product, customer base, and support challenge.
- Determine the current state, pain points, and metrics using the 2026 four-pillar framework.
- Verify the environment, versions, permissions, inputs, constraints, and user intent before acting.

## Source Freshness

- Volatile facts, such as specific tool recommendations or metric benchmarks, must be verified against current upstream documentation.
- See `references/reading-list.md` for a curated list of authoritative sources.

## Workflow

1. **Understand the context** — What product, customer base, and support challenge?
2. **Assess** — Current state, pain points, and metrics using the 2026 four-pillar framework (speed, quality, cost, loyalty).
3. **Select reference** — Choose the appropriate domain:
   - Support operations and processes → `references/support-operations.md`
   - Technical support and troubleshooting → `references/technical-support.md`
   - Knowledge management and self-service → `references/knowledge-management.md`
4. **Design** — Process, documentation, or solution incorporating AI automation and proactive support where applicable.
5. **Implement** — Roll out with training and explicit fallback mechanisms to human agents.
6. **Measure** — Track effectiveness using updated KPIs (e.g., automation resolution rate) and iterate.

**Stop condition**: Solution is implemented, metrics are established, and fallback mechanisms are verified.

## Safety

- Separate read-only discovery from mutations.
- Require confirmation for destructive, external, privileged, financial, legal, or production-impacting actions.

## Validation

- Verify that all metric definitions align with the 2026 four-pillar framework.
- Ensure ITIL 4 terminology is used consistently across all reference files.
- Validate that AI automation workflows include fallback mechanisms to human agents.
- Check that proactive support triggers are clearly defined in the escalation matrix.

## Failure Handling

- Diagnose errors using logs and metrics.
- Choose alternatives based on the 2026 four-pillar framework.
- Roll back changes if they negatively impact speed, quality, cost, or loyalty.
- Avoid repeating a failed action unchanged.

## Output Contract

- Structure: Clear, actionable recommendations based on the selected reference domain.
- Evidence: Metrics and data supporting the recommendations.
- Severity/Confidence: High confidence based on authoritative sources.
- Actionable next steps: Specific actions to implement the recommendations.

## Resources

- **Support operations**: See `references/support-operations.md` for processes and metrics.
- **Technical support**: See `references/technical-support.md` for troubleshooting and escalation.
- **Knowledge management**: See `references/knowledge-management.md` for documentation and self-service.
- **Recommended reading**: See `references/reading-list.md` for curated books and articles.

## Orchestration

> **Replaces the single "Select reference" step.** When multiple domains are detected, spawn all relevant specialists simultaneously — do not serialize them.

### Domain Detection Table

Scan the task for signals that indicate which domains apply:

| Task Signal (examples) | Domain | Specialist Agent | Reference |
|---|---|---|---|
| `technical support`, ... | **Technical Support** | Tech Support Specialist | `references/technical-support.md` |
| `support operations`, ... | **Support Operations** | Operations Specialist | `references/support-operations.md` |
| `knowledge base`, ... | **Knowledge Management** | Knowledge Specialist | `references/knowledge-management.md` |

### Spawning Logic

**Single domain detected** → Fall back to original single-reference behavior (no change).

**Multiple domains detected** → Launch all relevant specialists simultaneously:
- Each specialist receives: **full task context** + its dedicated reference file only
- No specialist waits for another — all start at the same time
- Maximum concurrent specialists: 3

### Cross-Domain Synthesizer

After all specialists complete, run one **Support Process Synthesizer** with all specialist outputs that:

1. **Identifies contradictions** between specialist recommendations for the same component
2. **Identifies gaps** — requirements addressed by no specialist
3. **Identifies dependencies** — where Domain A's output is a prerequisite for Domain B's recommendation
4. **Produces** a unified recommendation with explicit trade-off annotations for any resolved contradictions

> Synthesis focus for this skill: Ensures KB changes are reflected in ticketing workflows and escalation paths. Flags where a support operation change requires a knowledge base update to prevent re-escalation.

## Source freshness

Package guidance was **verified against upstream on 2026-08-07**. Re-check linked official sources at runtime before relying on volatile versions, flags, limits, prices, lifecycle dates, or hosted-service behavior.
