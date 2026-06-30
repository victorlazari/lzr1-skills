---
name: operations
description: Comprehensive operations skill covering business operations, project management, process optimization, vendor management, and operational excellence for technology companies. Use when designing processes, managing projects, optimizing workflows, selecting vendors, or building operational frameworks.
---

# Operations

Expert-level operations covering business operations, project management, process optimization, vendor management, and operational excellence for technology companies.

## When to Use

- Designing and optimizing business processes
- Managing projects and programs
- Vendor evaluation and management
- Building operational playbooks and SOPs
- Capacity planning and resource allocation
- Operational metrics and reporting
- Change management and transformation
- Scaling operations for growth

## Workflow

1. **Understand the context** — What process, team, and operational challenge?
2. **Select reference** — Choose the appropriate domain:
   - Project and program management → `references/project-management.md`
   - Process design and optimization → `references/process-optimization.md`
   - Vendor and procurement → `references/vendor-management.md`
   - Operational excellence → `references/operational-excellence.md`
3. **Assess** — Current state, pain points, constraints
4. **Design** — Process, framework, or solution
5. **Implement** — Roll out with change management
6. **Measure** — Track effectiveness, iterate

## Core Principles (All Operations Work)

- Process-driven: Document, standardize, then optimize
- Measurable: If you can't measure it, you can't improve it
- Scalable: Design for 10x, not just today
- Lean: Eliminate waste, maximize value delivery
- Automated: Automate repetitive tasks wherever possible
- Cross-functional: Operations connects all departments
- Continuous improvement: Never stop optimizing
- Customer-focused: Internal or external, serve the customer

## Role Capabilities

| Role | Expertise | Reference |
|---|---|---|
| Project Manager | Delivery, timelines, risk | `references/project-management.md` |
| Business Operations | Process, strategy, scaling | `references/process-optimization.md` |
| Procurement/Vendor Mgmt | Sourcing, contracts, relationships | `references/vendor-management.md` |
| Operations Manager | Efficiency, metrics, excellence | `references/operational-excellence.md` |
| Program Manager | Multi-project coordination | `references/project-management.md` |

## Key References

- **Project management**: See `references/project-management.md` for delivery and execution.
- **Process optimization**: See `references/process-optimization.md` for workflow design.
- **Vendor management**: See `references/vendor-management.md` for procurement and vendors.
- **Operational excellence**: See `references/operational-excellence.md` for metrics and scaling.
- **Recommended reading**: See `references/reading-list.md` for curated books and articles.

---

## Multi-Specialist Protocol

> **Replaces the single "Select reference" step.** When multiple domains are detected, spawn all relevant specialists simultaneously — do not serialize them.

### Domain Detection Table

Scan the task for signals that indicate which domains apply:

| Task Signal (examples) | Domain | Specialist Agent | Reference |
|---|---|---|---|
| `process`, ... | **Process Optimization** | Process Specialist | `references/process-optimization.md` |
| `project`, ... | **Project Management** | PM Specialist | `references/project-management.md` |
| `operational excellence`, ... | **Operational Excellence** | OpEx Specialist | `references/operational-excellence.md` |
| `vendor`, ... | **Vendor Management** | Vendor Specialist | `references/vendor-management.md` |

### Spawning Logic

**Single domain detected** → Fall back to original single-reference behavior (no change).

**Multiple domains detected** → Launch all relevant specialists simultaneously:
- Each specialist receives: **full task context** + its dedicated reference file only
- No specialist waits for another — all start at the same time
- Maximum concurrent specialists: 4

### Cross-Domain Synthesizer

After all specialists complete, run one **Operational Conflict Resolver** with all specialist outputs that:

1. **Identifies contradictions** between specialist recommendations for the same component
2. **Identifies gaps** — requirements addressed by no specialist
3. **Identifies dependencies** — where Domain A's output is a prerequisite for Domain B's recommendation
4. **Produces** a unified recommendation with explicit trade-off annotations for any resolved contradictions

> Synthesis focus for this skill: Catches where a process optimization creates a vendor contract conflict. Ensures operational KPIs are reflected in vendor SLA requirements.
