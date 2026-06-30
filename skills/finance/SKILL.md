---
name: finance
description: Comprehensive finance skill covering financial planning and analysis (FP&A), accounting, treasury, financial modeling, SaaS metrics, fundraising, and corporate finance. Use when building financial models, analyzing metrics, planning budgets, preparing investor materials, managing cash flow, or making financial decisions.
---

# Finance

Expert-level finance covering FP&A, accounting, financial modeling, SaaS metrics, fundraising, treasury, and corporate finance for technology companies.

## When to Use

- Building financial models and forecasts
- Analyzing SaaS/business metrics
- Planning budgets and resource allocation
- Preparing investor materials and board decks
- Managing cash flow and treasury
- Revenue recognition and accounting
- Fundraising strategy and valuation
- Financial reporting and compliance

## Workflow

1. **Understand the context** — What stage, business model, and financial question?
2. **Select reference** — Choose the appropriate domain:
   - Financial modeling and FP&A → `references/financial-modeling.md`
   - SaaS and business metrics → `references/saas-metrics.md`
   - Accounting and reporting → `references/accounting.md`
   - Fundraising and valuation → `references/fundraising.md`
3. **Gather data** — Financial statements, metrics, benchmarks
4. **Analyze** — Build models, identify trends, compare to benchmarks
5. **Recommend** — Data-driven recommendations with scenarios
6. **Present** — Clear communication of financial insights

## Core Principles (All Finance Work)

- Accuracy: Double-check every number; errors compound
- Conservatism: Better to under-promise than over-promise
- Transparency: Show assumptions clearly; make models auditable
- Scenario planning: Always model best, base, and worst cases
- Cash is king: Revenue is vanity, profit is sanity, cash is reality
- Unit economics: Understand the economics of each customer/transaction
- Benchmarking: Compare to industry standards and peers
- Forward-looking: Historical data informs, but forecasts drive decisions

## Role Capabilities

| Role | Expertise | Reference |
|---|---|---|
| FP&A Analyst | Budgets, forecasts, variance analysis | `references/financial-modeling.md` |
| Financial Controller | Accounting, reporting, compliance | `references/accounting.md` |
| Treasury Manager | Cash management, banking, risk | `references/accounting.md` |
| SaaS Finance | Unit economics, metrics, benchmarks | `references/saas-metrics.md` |
| CFO/Finance Leader | Strategy, fundraising, board | `references/fundraising.md` |

## Key References

- **Financial modeling**: See `references/financial-modeling.md` for models, forecasts, and FP&A.
- **SaaS metrics**: See `references/saas-metrics.md` for unit economics and benchmarks.
- **Accounting**: See `references/accounting.md` for reporting, compliance, and treasury.
- **Fundraising**: See `references/fundraising.md` for valuation, investors, and capital.
- **Recommended reading**: See `references/reading-list.md` for curated books and articles.

---

## Multi-Specialist Protocol

> **Replaces the single "Select reference" step.** When multiple domains are detected, spawn all relevant specialists simultaneously — do not serialize them.

### Domain Detection Table

Scan the task for signals that indicate which domains apply:

| Task Signal (examples) | Domain | Specialist Agent | Reference |
|---|---|---|---|
| `accounting`, ... | **Accounting** | Accounting Specialist | `references/accounting.md` |
| `model`, ... | **Financial Modeling** | Modeling Specialist | `references/financial-modeling.md` |
| `fundraising`, ... | **Fundraising** | Fundraising Specialist | `references/fundraising.md` |
| `SaaS`, ... | **SaaS Metrics** | Metrics Specialist | `references/saas-metrics.md` |

### Spawning Logic

**Single domain detected** → Fall back to original single-reference behavior (no change).

**Multiple domains detected** → Launch all relevant specialists simultaneously:
- Each specialist receives: **full task context** + its dedicated reference file only
- No specialist waits for another — all start at the same time
- Maximum concurrent specialists: 4

### Cross-Domain Synthesizer

After all specialists complete, run one **Financial Consistency Checker** with all specialist outputs that:

1. **Identifies contradictions** between specialist recommendations for the same component
2. **Identifies gaps** — requirements addressed by no specialist
3. **Identifies dependencies** — where Domain A's output is a prerequisite for Domain B's recommendation
4. **Produces** a unified recommendation with explicit trade-off annotations for any resolved contradictions

> Synthesis focus for this skill: Ensures SaaS metric definitions are consistent across the financial model. Flags where fundraising narrative assumptions conflict with accounting classifications.
