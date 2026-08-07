# Accounting & Treasury

Verified against upstream: 2026-08-07

## Table of Contents
1. Revenue Recognition (ASC 606)
2. Financial Reporting
3. Treasury Management
4. Tax Considerations
5. Audit and Compliance

---

## 1. Revenue Recognition (ASC 606)

### Five-Step Model

| Step | Description | SaaS Application |
|---|---|---|
| 1. Identify contract | Agreement with commercial substance | Signed subscription agreement |
| 2. Identify performance obligations | Distinct goods/services promised | Software access, support, implementation |
| 3. Determine transaction price | Amount expected to receive | Contract value, variable consideration |
| 4. Allocate price | Distribute to each obligation | Standalone selling price allocation |
| 5. Recognize revenue | When/as obligations are satisfied | Over time (subscription) or point-in-time |

### SaaS Revenue Recognition Patterns

| Revenue Type | Recognition | Timing |
|---|---|---|
| Subscription (SaaS) | Ratably over contract term | Monthly over 12/24/36 months |
| Implementation/Setup | Over implementation period or at completion | Depends on distinct obligation |
| Professional services | As services are delivered | Time-based or milestone |
| Usage/consumption | As usage occurs | Monthly based on consumption |
| Perpetual license | At delivery | Point-in-time |

### Contract Modifications (Upgrades, Downgrades, Usage)

Under ASC 606, contract modifications must be evaluated to determine if they should be accounted for as a separate contract or as a modification to the existing contract.

- **Upgrades (Additional Services):** If the upgrade adds distinct services at their standalone selling price, account for it as a separate contract. If not at standalone selling price, account for it prospectively as a termination of the old contract and creation of a new one.
- **Downgrades (Reduced Services):** Typically accounted for prospectively. The remaining unrecognized revenue is recognized over the remaining modified term.
- **Usage-Based Pricing:** Revenue is recognized as the usage occurs. If there is a minimum commitment, that portion is recognized ratably, and overages are recognized as incurred.

### Deferred Revenue

```
Deferred Revenue = Cash collected - Revenue recognized

Example (annual prepaid subscription):
  Contract: $120,000/year, paid upfront
  Month 1: Cash +$120K, Revenue +$10K, Deferred Revenue +$110K
  Month 2: Revenue +$10K, Deferred Revenue -$10K
  ...
  Month 12: Revenue +$10K, Deferred Revenue = $0
```

---

## 2. Financial Reporting

### Monthly Close Process

| Day | Activity | Owner |
|---|---|---|
| Day 1-2 | Bank reconciliation, AP/AR close | Accounting |
| Day 3-4 | Revenue recognition, deferred revenue | Revenue accountant |
| Day 5-6 | Expense accruals, prepaid amortization | Accounting |
| Day 7-8 | Payroll reconciliation, equity comp | Accounting |
| Day 9-10 | Financial statement preparation | Controller |
| Day 11-12 | Variance analysis, commentary | FP&A |
| Day 13-15 | Management review, board reporting | CFO |

### Key Financial Reports

| Report | Audience | Frequency | Content |
|---|---|---|---|
| Income statement | Management, board | Monthly | Revenue, expenses, profit |
| Balance sheet | Management, board | Monthly | Assets, liabilities, equity |
| Cash flow statement | Management, board | Monthly | Cash movements |
| Budget vs actual | Department heads | Monthly | Variance analysis |
| Board deck | Board of directors | Quarterly | KPIs, financials, strategy |
| Investor update | Investors | Monthly/Quarterly | Metrics, milestones, asks |

---

## 3. Treasury Management

### Cash Management

| Activity | Description | Frequency |
|---|---|---|
| Cash forecasting | Project cash inflows and outflows | Weekly (13-week) |
| Working capital | Manage AR, AP, inventory timing | Ongoing |
| Investment policy | Where to park excess cash | Quarterly review |
| Banking relationships | Manage bank accounts, credit facilities | Ongoing |
| FX management | Hedge currency exposure | As needed |
| Debt management | Service debt, manage covenants | Ongoing |

### 13-Week Cash Flow Forecast

```
Week 1-13 rolling forecast:

Inflows:
  + Customer payments (AR collections)
  + Investment income
  + Other income

Outflows:
  - Payroll (bi-weekly)
  - Vendor payments (AP)
  - Rent and facilities
  - Software and subscriptions
  - Taxes
  - Debt service
  - Capital expenditures

Net cash flow = Inflows - Outflows
Ending cash = Beginning cash + Net cash flow
```

---

## 4. Tax Considerations

### Key Tax Areas for Tech Companies

| Area | Consideration | Impact |
|---|---|---|
| R&D tax credits | Section 174 capitalization (US) | Significant cash benefit |
| Transfer pricing | Intercompany pricing for global ops | Compliance risk |
| Sales tax/VAT | SaaS taxability varies by jurisdiction | Collection obligation |
| Stock compensation | 409A valuation, ISO vs NSO | Employee tax impact |
| International | Permanent establishment, withholding | Global structure |
| State taxes | Nexus, apportionment | Multi-state compliance |

### R&D Capitalization (Section 174) - 2026 OB3 Update

```
Under the 2026 One Big Beautiful Bill Act (OB3):
- Domestic R&D: Immediate expensing is restored. Companies can fully deduct domestic R&D expenses in the year incurred.
- Foreign R&D: Continues to require 15-year amortization.
- Section 280C: Companies must carefully plan the interaction between the R&D tax credit and the immediate deduction under Section 280C to optimize cash tax benefits.
- This significantly improves cash flow for R&D-heavy companies compared to the 2022-2025 rules.
```

---

## 5. Audit and Compliance

### SOX Compliance (Public Companies)

| Section | Requirement | Activities |
|---|---|---|
| Section 302 | CEO/CFO certify financial statements | Quarterly certification |
| Section 404 | Internal controls over financial reporting | Annual assessment |
| Section 906 | Criminal penalties for false certification | Compliance |

### Internal Controls

| Control Type | Description | Example |
|---|---|---|
| Preventive | Stop errors before they occur | Approval workflows, segregation of duties |
| Detective | Identify errors after they occur | Reconciliations, variance analysis |
| Corrective | Fix errors once identified | Adjustment entries, process changes |

### Audit Readiness

| Area | Preparation | Documentation |
|---|---|---|
| Revenue | Contract review, recognition policy | Revenue waterfall, policy memo |
| Expenses | Accrual completeness, cutoff | Expense support, approvals |
| Equity | Cap table, option grants, 409A | Board minutes, valuations |
| Cash | Bank reconciliations | Statements, reconciliations |
| Estimates | Judgments and assumptions | Methodology documentation |
