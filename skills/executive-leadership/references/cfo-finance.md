# CFO Financial Strategy

## Table of Contents
1. Financial Planning
2. SaaS Metrics
3. Fundraising Finance
4. Unit Economics
5. Financial Operations

---

## 1. Financial Planning

### Annual Planning Process

| Phase | Activities | Timeline |
|---|---|---|
| Strategic context | Board input, market analysis | Month 1 |
| Top-down targets | Revenue, headcount, margin goals | Month 1 |
| Bottom-up plans | Department budgets, hiring plans | Month 2 |
| Reconciliation | Align top-down and bottom-up | Month 2-3 |
| Approval | Board review and approval | Month 3 |
| Communication | Cascade to organization | Month 3 |

### Budget Structure

| Category | Components | Typical % of Revenue |
|---|---|---|
| COGS | Hosting, support, onboarding | 15-25% |
| R&D | Engineering, product, design | 25-40% |
| Sales & Marketing | Sales team, marketing spend | 30-50% |
| G&A | Finance, HR, legal, facilities | 10-20% |

### Financial Model Components

```
Revenue Model:
  New ARR = New customers × ACV
  Expansion ARR = Existing customers × Net expansion rate
  Churned ARR = Existing customers × Churn rate
  Net New ARR = New + Expansion - Churn

Expense Model:
  Headcount plan × Fully loaded cost
  + Non-headcount (tools, marketing, hosting)
  = Total expenses

Cash Flow:
  Revenue (cash collected)
  - Expenses (cash spent)
  - CapEx
  = Net cash flow
  
  Beginning cash + Net cash flow = Ending cash
```

---

## 2. SaaS Metrics

### Key SaaS Metrics

| Metric | Formula | Benchmark (Growth Stage) |
|---|---|---|
| ARR | Monthly recurring revenue × 12 | Growing >100% YoY (early) |
| MRR Growth | (MRR end - MRR start) / MRR start | >10% monthly (early) |
| Net Revenue Retention | (Start ARR + Expansion - Churn) / Start ARR | >120% |
| Gross Revenue Retention | (Start ARR - Churn) / Start ARR | >90% |
| CAC | Total S&M spend / New customers | Varies by ACV |
| LTV | ARPA × Gross margin / Churn rate | LTV:CAC > 3:1 |
| CAC Payback | CAC / (ARPA × Gross margin) | <18 months |
| Burn Multiple | Net burn / Net new ARR | <2x (efficient) |
| Rule of 40 | Revenue growth % + FCF margin % | >40% |
| Magic Number | Net new ARR / Prior quarter S&M | >1.0 |

### Cohort Analysis

```
Month 0: 100% (starting ARR of cohort)
Month 3: 95% (5% churned)
Month 6: 93% (2% more churned)
Month 12: 90% (3% more churned)
Month 12 with expansion: 110% (20% expanded)
Net retention at 12 months: 110%
```

---

## 3. Fundraising Finance

### Investor Metrics Focus by Stage

| Stage | Key Metrics | Benchmarks |
|---|---|---|
| Seed | Team, TAM, early traction | Some revenue, strong team |
| Series A | ARR, growth rate, retention | $1-3M ARR, >100% growth |
| Series B | Unit economics, efficiency | $5-15M ARR, improving margins |
| Series C | Path to profitability, market share | $20-50M ARR, Rule of 40 |

### Use of Funds Allocation

| Category | Typical Allocation |
|---|---|
| Engineering/Product | 40-50% |
| Sales & Marketing | 30-40% |
| G&A | 10-15% |
| Buffer | 5-10% |

### Runway Planning

```
Monthly burn rate = Total monthly expenses - Monthly revenue
Runway (months) = Cash balance / Monthly burn rate

Target: 18-24 months runway post-raise
Start fundraising: When 6-9 months runway remaining
```

---

## 4. Unit Economics

### Unit Economics Framework

| Metric | Calculation | Healthy |
|---|---|---|
| Gross margin | (Revenue - COGS) / Revenue | >70% (SaaS) |
| Contribution margin | (Revenue - COGS - Variable costs) / Revenue | >50% |
| LTV:CAC ratio | Customer lifetime value / Customer acquisition cost | >3:1 |
| Payback period | Months to recover CAC | <18 months |
| Fully loaded CAC | All S&M costs / New customers | Declining over time |

### Pricing Strategy

| Model | Description | Best For |
|---|---|---|
| Per seat | Charge per user | Collaboration tools |
| Usage-based | Charge per unit consumed | Infrastructure, API |
| Tiered | Feature-based tiers | Most SaaS |
| Flat rate | Single price for all | Simple products |
| Hybrid | Base + usage | Enterprise SaaS |
| Value-based | Priced on value delivered | High-value enterprise |

---

## 5. Financial Operations

### Month-End Close Process

| Day | Activity |
|---|---|
| Day 1-2 | Revenue recognition, billing reconciliation |
| Day 3-4 | Expense accruals, payroll |
| Day 5-6 | Bank reconciliation, intercompany |
| Day 7-8 | Financial statements draft |
| Day 9-10 | Review, adjustments, final close |

### Financial Controls

| Control | Purpose | Implementation |
|---|---|---|
| Approval workflows | Prevent unauthorized spend | Expense limits by level |
| Segregation of duties | Prevent fraud | Separate approval and payment |
| Bank reconciliation | Catch errors/fraud | Monthly reconciliation |
| Budget vs actual | Track spending | Monthly variance analysis |
| Audit trail | Accountability | All changes logged |
| Access controls | Protect financial data | Role-based access |
