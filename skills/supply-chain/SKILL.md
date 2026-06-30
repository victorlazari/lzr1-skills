---
name: supply-chain
description: Comprehensive supply chain skill covering procurement, vendor management, supply chain analytics, logistics, inventory management, and strategic sourcing for technology companies. Use when managing vendor relationships, optimizing procurement processes, analyzing supply chain data, managing inventory, or developing sourcing strategies.
---

# Supply Chain & Procurement

Expert-level supply chain management covering procurement, vendor management, supply chain analytics, logistics, inventory management, and strategic sourcing.

## When to Use

- Managing vendor relationships and contracts
- Optimizing procurement processes
- Analyzing supply chain data and costs
- Managing inventory and demand planning
- Developing sourcing strategies
- Evaluating and selecting suppliers
- Risk management in supply chain
- Cost optimization and negotiation

## Workflow

1. **Understand the context** — What procurement need, supply chain challenge, or optimization?
2. **Select reference** — Choose the appropriate domain:
   - Procurement and sourcing → `references/procurement.md`
   - Supply chain analytics and optimization → `references/supply-chain-analytics.md`
3. **Analyze** — Spend analysis, supplier assessment, risk evaluation
4. **Plan** — Strategy, timeline, stakeholder alignment
5. **Execute** — Negotiate, contract, implement
6. **Optimize** — Monitor, measure, improve

## Core Principles (All Supply Chain Work)

- Total cost of ownership: Look beyond purchase price
- Risk diversification: Avoid single points of failure
- Data-driven: Decisions backed by analytics
- Relationship-based: Long-term partnerships over transactions
- Sustainable: Environmental and social responsibility
- Compliant: Regulatory and policy adherence
- Agile: Adapt to disruptions quickly
- Transparent: Clear communication with stakeholders

## Role Capabilities

| Role | Expertise | Reference |
|---|---|---|
| Procurement Manager | Sourcing, negotiation, contracts | `references/procurement.md` |
| Supply Chain Analyst | Analytics, optimization, forecasting | `references/supply-chain-analytics.md` |

## Key References

- **Procurement**: See `references/procurement.md` for sourcing and vendor management.
- **Supply chain analytics**: See `references/supply-chain-analytics.md` for optimization.
- **Recommended reading**: See `references/reading-list.md` for curated books and articles.

---

## Multi-Specialist Protocol

> **Replaces the single "Select reference" step.** When multiple domains are detected, spawn all relevant specialists simultaneously — do not serialize them.

### Domain Detection Table

Scan the task for signals that indicate which domains apply:

| Task Signal (examples) | Domain | Specialist Agent | Reference |
|---|---|---|---|
| `procurement`, ... | **Procurement** | Procurement Specialist | `references/procurement.md` |
| `analytics`, ... | **Supply Chain Analytics** | Analytics Specialist | `references/supply-chain-analytics.md` |

### Spawning Logic

**Single domain detected** → Fall back to original single-reference behavior (no change).

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

> Synthesis focus for this skill: Catches where an analytics-driven demand insight requires an immediate procurement contract amendment. Maps inventory optimization recommendations to supplier lead time constraints.
