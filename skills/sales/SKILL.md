---
name: sales
description: Comprehensive sales skill covering B2B sales, sales engineering, account management, revenue operations, and go-to-market strategy. Use when building sales processes, creating proposals, managing pipelines, designing compensation plans, enabling sales teams, or developing go-to-market strategies.
---

# Sales

Expert-level sales covering B2B selling, sales engineering, account management, revenue operations, and go-to-market strategy for technology and enterprise organizations.

## When to Use

- Building or optimizing sales processes
- Creating proposals, decks, and business cases
- Managing sales pipelines and forecasting
- Designing compensation and territory plans
- Sales enablement and training materials
- Go-to-market strategy and execution
- Account planning and expansion
- Revenue operations and analytics

## Workflow

1. **Understand the context** — What product, market, deal size, and sales motion?
2. **Select reference** — Choose the appropriate domain:
   - Sales process and methodology → `references/sales-process.md`
   - Sales engineering and demos → `references/sales-engineering.md`
   - Account management and expansion → `references/account-management.md`
   - Revenue operations → `references/revenue-operations.md`
3. **Research** — Buyer, competition, and deal context
4. **Strategize** — Plan approach, messaging, and tactics
5. **Execute** — Engage, present, negotiate, close
6. **Optimize** — Measure, learn, improve process

## Core Principles (All Sales Work)

- Buyer-centric: Focus on the buyer's problem, not your product
- Consultative: Be a trusted advisor, not a pushy seller
- Value-based: Sell outcomes and ROI, not features
- Process-driven: Repeatable methodology beats individual heroics
- Data-informed: Use metrics to identify and fix bottlenecks
- Multi-threaded: Build relationships across the buying committee
- Urgency without pressure: Create genuine reasons to act now
- Long-term thinking: Protect relationships for expansion and referrals

## Role Capabilities

| Role | Expertise | Reference |
|---|---|---|
| Account Executive | Full-cycle B2B sales | `references/sales-process.md` |
| Sales Engineer | Technical demos, POCs, solutions | `references/sales-engineering.md` |
| Account Manager | Retention, expansion, renewals | `references/account-management.md` |
| Revenue Ops | Process, data, tools, forecasting | `references/revenue-operations.md` |

## Key References

- **Sales process**: See `references/sales-process.md` for methodology, pipeline, and closing.
- **Sales engineering**: See `references/sales-engineering.md` for demos, POCs, and technical selling.
- **Account management**: See `references/account-management.md` for retention and expansion.
- **Revenue operations**: See `references/revenue-operations.md` for ops, analytics, and tools.
- **Recommended reading**: See `references/reading-list.md` for curated books and articles.

---

## Multi-Specialist Protocol

> **Replaces the single "Select reference" step.** When multiple domains are detected, spawn all relevant specialists simultaneously — do not serialize them.

### Domain Detection Table

Scan the task for signals that indicate which domains apply:

| Task Signal (examples) | Domain | Specialist Agent | Reference |
|---|---|---|---|
| `sales process`, ... | **Sales Process** | Sales Process Specialist | `references/sales-process.md` |
| `account management`, ... | **Account Management** | Account Mgmt Specialist | `references/account-management.md` |
| `RevOps`, ... | **Revenue Operations** | RevOps Specialist | `references/revenue-operations.md` |
| `SE`, ... | **Sales Engineering** | SE Specialist | `references/sales-engineering.md` |

### Spawning Logic

**Single domain detected** → Fall back to original single-reference behavior (no change).

**Multiple domains detected** → Launch all relevant specialists simultaneously:
- Each specialist receives: **full task context** + its dedicated reference file only
- No specialist waits for another — all start at the same time
- Maximum concurrent specialists: 4

### Cross-Domain Synthesizer

After all specialists complete, run one **Deal Synthesizer** with all specialist outputs that:

1. **Identifies contradictions** between specialist recommendations for the same component
2. **Identifies gaps** — requirements addressed by no specialist
3. **Identifies dependencies** — where Domain A's output is a prerequisite for Domain B's recommendation
4. **Produces** a unified recommendation with explicit trade-off annotations for any resolved contradictions

> Synthesis focus for this skill: Ensures CRM process aligns with technical qualification criteria. Flags where account management expansion motions conflict with the sales process stage gates.
