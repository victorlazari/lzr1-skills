---
name: supply-chain
description: Comprehensive supply chain skill covering procurement, vendor management, supply chain analytics, logistics, inventory management, and strategic sourcing for technology companies. Use when managing vendor relationships, optimizing procurement processes, analyzing supply chain data, managing inventory, or developing sourcing strategies.
---

# Supply Chain & Procurement

Expert-level supply chain management covering procurement, vendor management, supply chain analytics, logistics, inventory management, and strategic sourcing.

## Scope and Triggers

- **Triggers:** Managing vendor relationships and contracts, optimizing procurement processes, analyzing supply chain data and costs, managing inventory and demand planning, developing sourcing strategies, evaluating and selecting suppliers, risk management in supply chain, cost optimization and negotiation.
- **Non-goals:** Deep financial modeling, valuation, or investment research (route to `finance-pro-playbooks`). Formal legal review or compliance assessment for contract negotiation (route to `legal-review`).

## Preconditions

- Identify the specific supply chain or procurement need.
- Determine the target environment, permissions, inputs, and constraints.
- Detect user intent and required domains (procurement, analytics, or both).

## Source Freshness

- Volatile facts and compliance rules must be verified against current official documentation before taking action.
- Authoritative sources are documented in the respective reference files with a `Verified against upstream: 2026-08-07` marker.

## Workflow

1. **Understand the context** — What procurement need, supply chain challenge, or optimization?
2. **Select reference** — Choose the appropriate domain:
   - Procurement and sourcing → `references/procurement.md`
   - Supply chain analytics and optimization → `references/supply-chain-analytics.md`
3. **Gather Data** — Collect necessary data and perform analysis (spend, risk, demand).
4. **Plan** — Develop a strategy or plan based on the analysis, timeline, and stakeholder alignment.
5. **Execute** — Negotiate, contract, and implement the plan after obtaining necessary confirmations.
6. **Stop** — Stop when the objective is met or if a critical dependency or risk is identified that requires escalation.

## Safety

- **Read-only discovery:** Perform data gathering and analysis before any mutations.
- **Confirmation required:** Require explicit user confirmation before executing any binding contracts, financial commitments, or production-impacting actions.
- **Validation:** Validate vendor data against known authoritative sources.

## Validation

- Ensure all scripts have dry-run capabilities and fail safely on error.
- Run `scripts/validate-vendor.sh` to perform basic vendor validation checks.
- Use `templates/vendor-scorecard.md` for evaluating and scoring vendors.

## Failure Handling

- If a script fails, diagnose the error using the output, choose an alternative approach, and avoid repeating the failed action unchanged.
- Roll back any partial changes if a critical step fails.

## Output Contract

- Provide a clear, structured output detailing the analysis, strategy, and executed actions.
- Include evidence of vendor validation and risk assessment.
- Specify actionable next steps and any unresolved uncertainties.

## Resources

- `references/procurement.md`: Procurement and sourcing processes, vendor selection, contract management, negotiation, and risk management.
- `references/supply-chain-analytics.md`: Spend analysis, demand planning, inventory management, supply chain optimization, and performance metrics.
- `scripts/validate-vendor.sh`: Script to perform basic vendor validation checks.
- `templates/vendor-scorecard.md`: Template for evaluating and scoring vendors.

## Multi-Specialist Protocol

When multiple domains are detected, spawn all relevant specialists simultaneously — do not serialize them.

### Domain Detection Table

| Task Signal (examples) | Domain | Specialist Agent | Reference |
|---|---|---|---|
| `procurement`, ... | **Procurement** | Procurement Specialist | `references/procurement.md` |
| `analytics`, ... | **Supply Chain Analytics** | Analytics Specialist | `references/supply-chain-analytics.md` |

### Spawning Logic

**Single domain detected** → Fall back to original single-reference behavior.

**Multiple domains detected** → Launch all relevant specialists simultaneously:
- Each specialist receives: **full task context** + its dedicated reference file only
- No specialist waits for another — all start at the same time
- Maximum concurrent specialists: 2

### Cross-Domain Synthesizer

After all specialists complete, run one **Supply Chain Synthesizer** with all specialist outputs that:
1. **Identifies contradictions** between specialist recommendations for the same component
2. **Identifies gaps** — requirements addressed by no specialist
3. **Identifies dependencies** — where Domain A's output is a prerequisite for Domain B's recommendation
4. **Produces** a unified recommendation with explicit trade-off annotations for any resolved contradictions
