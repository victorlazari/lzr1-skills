---
name: operations
description: Comprehensive operations skill covering business operations, project management, process optimization, vendor management, and operational excellence for technology companies. Use when designing processes, managing projects, optimizing workflows, selecting vendors, or building operational frameworks.
---

# Operations

Expert-level operations covering business operations, project management, process optimization, vendor management, and operational excellence for technology companies.

## Scope and Triggers

**Use this skill when:**
- Designing and optimizing business processes
- Managing projects and programs
- Vendor evaluation and management
- Building operational playbooks and SOPs
- Capacity planning and resource allocation
- Operational metrics and reporting
- Change management and transformation
- Scaling operations for growth

**Do not use this skill for:**
- Financial modeling, valuation, or detailed financial analysis (route to `finance-pro-playbooks`)
- Building automated workflows, integrations, or scheduled tasks (route to `automation-and-scheduling`)

## Preconditions

Before acting, detect the target, environment, constraints, and user intent. Determine the operational domain (Project Management, Process Optimization, Vendor Management, or Operational Excellence) based on the task context.

## Source Freshness

This skill incorporates current authoritative sources (PMBOK 8th Edition, ITIL 4, Shingo Model, CIPS).
- **Verified against upstream:** 2026-08-07
- Do not invent versions, flags, APIs, policies, or claims. Convert volatile details into runtime checks against installed versions and official docs.

## Workflow

1. **Detect Domain:** Detect the operational domain based on the task context.
2. **Load Reference:** Load the corresponding reference file to access domain-specific frameworks and standards:
   - Project and program management → `references/project-management.md`
   - Process design and optimization → `references/process-optimization.md`
   - Vendor and procurement → `references/vendor-management.md`
   - Operational excellence → `references/operational-excellence.md`
3. **Assess:** Assess the current state, constraints, and requirements using the loaded framework.
4. **Design:** Design the process, plan, or evaluation matrix, utilizing templates where applicable (e.g., `templates/vendor-scorecard.csv`).
5. **Validate:** Validate the proposed solution against safety and compliance rules (e.g., run `scripts/validate-vendor-scorecard.py`).
6. **Stop:** Stop when a complete, actionable operational plan or evaluation is produced and validated.

## Safety

- Separate read-only discovery from mutations.
- Require confirmation before finalizing vendor selections or approving budgets.
- Ensure process changes include a rollback plan.
- Verify that capacity planning models account for buffer and constraints.
- Do not download or execute untrusted artifacts.

## Validation

- Validate vendor scorecards using `scripts/validate-vendor-scorecard.py`.
- Ensure all project management recommendations align with PMBOK 8th Edition principles.
- Ensure process optimization outputs are compatible with ITIL 4 service value systems.
- Validate vendor management strategies against modern risk and compliance frameworks.
- Check that operational excellence metrics include behavioral indicators alongside performance KPIs.

## Failure Handling

- If validation fails, diagnose errors, choose alternatives, and roll back if necessary.
- Do not repeat a failed action unchanged.

## Output Contract

Produce a complete, actionable operational plan or evaluation. The output must include:
- The structure of the plan or evaluation.
- Evidence supporting the recommendations.
- Severity/confidence levels for risks or constraints.
- Actionable next steps.

## Resources

- `references/project-management.md`: Project and program management (PMBOK 8th Edition).
- `references/process-optimization.md`: Process design and optimization (ITIL 4).
- `references/vendor-management.md`: Vendor and procurement (Strategic sourcing, digital procurement).
- `references/operational-excellence.md`: Operational excellence (Shingo Model).
- `templates/vendor-scorecard.csv`: Standardized template for vendor evaluation scoring.
- `scripts/validate-vendor-scorecard.py`: Validates vendor scorecard data against required criteria and weights.

## Orchestration

Use parallel work only for independent dimensions. Define inputs, schemas, conflict handling, synthesis, and termination conditions.
