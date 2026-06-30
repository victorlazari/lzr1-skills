---
name: customer-support
description: Comprehensive customer support skill covering support operations, technical support, knowledge management, support metrics, and customer experience for technology companies. Use when building support processes, creating help documentation, designing escalation workflows, measuring support quality, or implementing support tools.
---

# Customer Support

Expert-level customer support covering support operations, technical support, knowledge management, metrics, and customer experience for technology companies.

## When to Use

- Building support processes and workflows
- Creating help documentation and knowledge bases
- Designing escalation and triage systems
- Measuring support quality and efficiency
- Implementing support tools and automation
- Training support teams
- Handling customer escalations
- Building self-service experiences

## Workflow

1. **Understand the context** — What product, customer base, and support challenge?
2. **Select reference** — Choose the appropriate domain:
   - Support operations and processes → `references/support-operations.md`
   - Technical support and troubleshooting → `references/technical-support.md`
   - Knowledge management and self-service → `references/knowledge-management.md`
3. **Assess** — Current state, pain points, metrics
4. **Design** — Process, documentation, or solution
5. **Implement** — Roll out with training
6. **Measure** — Track effectiveness, iterate

## Core Principles (All Support Work)

- Customer-first: Empathy and resolution above all
- Speed matters: Fast first response, fast resolution
- Quality over quantity: Right answer first time
- Self-service: Enable customers to help themselves
- Proactive: Anticipate issues before customers report them
- Scalable: Processes that work at 10x volume
- Data-driven: Use metrics to identify and fix issues
- Continuous learning: Every ticket is a learning opportunity

## Role Capabilities

| Role | Expertise | Reference |
|---|---|---|
| Support Manager | Operations, team, metrics | `references/support-operations.md` |
| Technical Support | Troubleshooting, escalation | `references/technical-support.md` |
| Knowledge Manager | Documentation, self-service | `references/knowledge-management.md` |

## Key References

- **Support operations**: See `references/support-operations.md` for processes and metrics.
- **Technical support**: See `references/technical-support.md` for troubleshooting and escalation.
- **Knowledge management**: See `references/knowledge-management.md` for documentation and self-service.
- **Recommended reading**: See `references/reading-list.md` for curated books and articles.

---

## Multi-Specialist Protocol

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
