# Financial Modeling

## Table of Contents
1. Model Architecture
2. Revenue Modeling
3. Expense Modeling
4. Three-Statement Model
5. Scenario Analysis

---

## 1. Model Architecture

### Model Structure Best Practices

| Principle | Description |
|---|---|
| Separation of concerns | Inputs, calculations, and outputs on separate sheets |
| One formula per row | Don't mix formulas across a row |
| No hardcoded numbers in formulas | All assumptions in dedicated inputs section |
| Color coding | Blue = input, black = formula, green = link to other sheet |
| Documentation | Assumption notes, version history, table of contents |
| Error checks | Built-in checks for balance sheet balance, circular refs |
| Flexibility | Easy to update assumptions without restructuring |

### Standard Model Tabs

| Tab | Content | Purpose |
|---|---|---|
| Cover/TOC | Model name, version, navigation | Overview |
| Assumptions | All inputs and drivers | Single source of truth |
| Revenue | Revenue build-up | Top-line forecast |
| COGS | Cost of goods sold | Gross margin |
| OpEx | Operating expenses by department | Operating costs |
| Headcount | Hiring plan, compensation | People costs |
| P&L | Income statement | Profitability |
| Balance Sheet | Assets, liabilities, equity | Financial position |
| Cash Flow | Operating, investing, financing | Cash management |
| KPIs | Key metrics dashboard | Performance tracking |
| Scenarios | Sensitivity analysis | Risk assessment |

---

## 2. Revenue Modeling

### SaaS Revenue Model

```
New MRR = New customers × Average contract value / 12
Expansion MRR = Existing customers × Expansion rate
Contraction MRR = Existing customers × Contraction rate
Churn MRR = Churned customers × Their MRR
Net New MRR = New + Expansion - Contraction - Churn

ARR = MRR × 12
```

### Revenue Drivers

| Driver | Formula | Typical Range |
|---|---|---|
| New logo growth | New customers per month | 5-20% MoM (early), 2-5% (mature) |
| Net dollar retention | (Start MRR + expansion - contraction - churn) / Start MRR | 100-130% (good SaaS) |
| Average contract value | Total new ACV / New customers | Growing over time |
| Sales cycle length | Days from first touch to close | 30-90 days (SMB), 90-180 (enterprise) |
| Win rate | Closed-won / Total opportunities | 20-30% |
| Seat expansion | Additional seats per account per year | 10-30% |

---

## 3. Expense Modeling

### Expense Categories

| Category | Components | As % of Revenue (Benchmark) |
|---|---|---|
| COGS | Hosting, support, implementation | 15-25% (SaaS) |
| R&D | Engineering, product, design | 20-30% |
| Sales & Marketing | Sales, marketing, partnerships | 30-50% (growth), 20-30% (mature) |
| G&A | Finance, HR, legal, admin | 10-15% |

### Headcount Planning

```
Fully loaded cost = Base salary + Benefits (20-30%) + Equity + Taxes (10-15%)

Example:
  Base salary: $150,000
  Benefits (25%): $37,500
  Equity (annual vest): $25,000
  Taxes (12%): $18,000
  Total loaded cost: $230,500

Hiring timeline:
  Month 1: Req approved
  Month 2-3: Recruiting
  Month 3-4: Start date
  Month 4-7: Ramp (partial productivity)
  Month 7+: Full productivity
```

---

## 4. Three-Statement Model

### Income Statement Structure

```
Revenue
- COGS
= Gross Profit (Gross Margin %)
- R&D
- Sales & Marketing
- G&A
= Operating Income (Operating Margin %)
+/- Other Income/Expense
= Pre-tax Income
- Taxes
= Net Income (Net Margin %)
```

### Balance Sheet Structure

```
Assets:
  Cash and equivalents
  Accounts receivable
  Prepaid expenses
  Property and equipment
  Intangible assets

Liabilities:
  Accounts payable
  Deferred revenue
  Accrued expenses
  Debt (short-term and long-term)

Equity:
  Common stock
  Retained earnings
  Additional paid-in capital
```

### Cash Flow Statement

```
Operating Activities:
  Net income
  + Depreciation/amortization
  + Stock-based compensation
  +/- Changes in working capital
  = Cash from operations

Investing Activities:
  - Capital expenditures
  - Acquisitions
  = Cash from investing

Financing Activities:
  + Debt raised
  - Debt repaid
  + Equity raised
  - Dividends/buybacks
  = Cash from financing

Net change in cash = Operating + Investing + Financing
```

---

## 5. Scenario Analysis

### Scenario Framework

| Scenario | Revenue Growth | Assumptions |
|---|---|---|
| Bull case | +20-30% above base | Strong market, high win rates, fast expansion |
| Base case | Plan/budget | Current trends continue |
| Bear case | -20-30% below base | Market downturn, higher churn, slower sales |
| Stress test | -50%+ below base | Severe recession, major customer loss |

### Sensitivity Analysis

```
Key variables to test:
1. Revenue growth rate (+/- 10-20%)
2. Gross margin (+/- 5%)
3. Sales efficiency (CAC payback +/- 3 months)
4. Churn rate (+/- 2%)
5. Hiring pace (+/- 20% headcount)

Output: Impact on cash runway, profitability, and key metrics
```

### Rule of 40

```
Rule of 40 = Revenue Growth Rate + Profit Margin

Examples:
  40% growth + 0% margin = 40 ✓
  20% growth + 20% margin = 40 ✓
  60% growth + (-20%) margin = 40 ✓
  10% growth + 10% margin = 20 ✗

Benchmark: >40 is excellent, >25 is good for SaaS
```
