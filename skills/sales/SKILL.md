---
name: sales
description: Comprehensive sales skill covering B2B sales, sales engineering, account management, revenue operations, and go-to-market strategy. Use when building sales processes, creating proposals, managing pipelines, designing compensation plans, enabling sales teams, or developing go-to-market strategies.
---

# Sales

Expert-level sales covering B2B selling, sales engineering, account management, revenue operations, and go-to-market strategy for technology and enterprise organizations.

## Scope and Triggers

- **Scope**: Building or optimizing sales processes, creating proposals, managing pipelines, designing compensation, sales enablement, go-to-market strategy, account planning, and revenue operations.
- **Triggers**: Activates when tasks involve B2B sales, sales engineering, account management, or revenue operations.
- **Non-goals**: Does not cover top-of-funnel marketing campaigns, technical support resolution, or complex corporate finance analysis.
- **Escalation Boundaries**:
  - `marketing` — Route when the task involves lead generation, brand awareness, or top-of-funnel marketing campaigns.
  - `customer-support` — Route when the task involves resolving technical issues, handling support tickets, or post-sale troubleshooting.
  - `finance-pro-playbooks` — Route when the task involves complex financial modeling, valuation, or corporate finance analysis beyond standard sales compensation or pricing.

## Preconditions

- Detect the specific sales domain (Sales Process, Account Management, RevOps, Sales Engineering) based on task signals.
- Identify the target audience, environment, and user intent before acting.

## Source Freshness

- Consult the bundled verified references for current methodologies and frameworks.
- For volatile facts (e.g., AI tool capabilities, specific platform features), verify against current official documentation.

## Workflow

1. **Detect Domain**: Scan the task for signals that indicate which domains apply:
   - `sales process`, `methodology`, `pipeline` → **Sales Process** (`references/sales-process.md`)
   - `account management`, `retention`, `expansion` → **Account Management** (`references/account-management.md`)
   - `RevOps`, `operations`, `analytics` → **Revenue Operations** (`references/revenue-operations.md`)
   - `SE`, `demo`, `POC` → **Sales Engineering** (`references/sales-engineering.md`)
2. **Spawn Specialists**:
   - **Single domain detected**: Route directly to the relevant reference file and execute the domain-specific workflow.
   - **Multiple domains detected**: Launch all relevant specialists simultaneously. Each specialist receives the full task context and its dedicated reference file. Maximum concurrent specialists: 4.
3. **Synthesize (if multiple specialists)**: Run a Deal Synthesizer to identify contradictions, gaps, and dependencies among specialist outputs. Produce a unified recommendation with explicit trade-off annotations.
4. **Execute**: Develop the deliverable (e.g., proposal, account plan, pipeline analysis).
5. **Stop Condition**: Stop when the final deliverable is complete and meets the defined acceptance criteria.

## Safety

- **Read-only Discovery**: Always separate read-only discovery from mutations.
- **Confirmation Required**: Require confirmation before modifying CRM data or sending outbound communications.
- **Validation**: Validate AI tool recommendations against current industry standards. Ensure all proposed methodologies align with the updated RevOps framework.
- **Dry-run**: Provide dry-run capabilities for any automated prospecting or pipeline updates.

## Validation

- Define syntax checks, dry runs, tests, evidence capture, and postcondition verification for any automated actions.

## Failure Handling

- If an action fails, diagnose the error, choose an alternative approach, and do not repeat the failed action unchanged.
- Provide rollback guidance for any destructive actions.

## Output Contract

- The final deliverable must be structured, evidence-based, and include actionable next steps.
- Explicitly note any trade-offs or resolved conflicts if multiple domains were involved.

## Resources

- `references/sales-process.md`: Sales methodology, pipeline, and closing.
- `references/sales-engineering.md`: Demos, POCs, and technical selling.
- `references/account-management.md`: Retention and expansion.
- `references/revenue-operations.md`: Ops, analytics, and tools.

## Orchestration

- Use parallel work only for independent dimensions (e.g., different sales domains).
- Define inputs, schemas, conflict handling, synthesis, and termination conditions for parallel tasks.

## Authoritative sources

- [Authoritative source map](references/source-map.md) — consult this before relying on volatile upstream behavior.

## Package resource index

| Resource | Purpose |
|---|---|
| [references/source-map.md](references/source-map.md) | Supporting package resource; inspect before use and apply the workflow’s safety and validation gates. |
