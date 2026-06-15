# SaaS Metrics

## Table of Contents
1. Core SaaS Metrics
2. Unit Economics
3. Growth Metrics
4. Efficiency Metrics
5. Benchmarks by Stage

---

## 1. Core SaaS Metrics

### Revenue Metrics

| Metric | Formula | What It Tells You |
|---|---|---|
| MRR | Sum of all monthly recurring revenue | Current run rate |
| ARR | MRR × 12 | Annualized revenue |
| Net New MRR | New + Expansion - Contraction - Churn | Monthly momentum |
| CMRR | MRR + Committed (signed, not yet live) | Forward-looking revenue |
| ACV | Total contract value / Contract years | Average annual deal size |
| TCV | Total value of contract over full term | Total commitment |

### MRR Components

```
Beginning MRR
+ New MRR (new customers)
+ Expansion MRR (upgrades, seats, usage)
- Contraction MRR (downgrades)
- Churn MRR (lost customers)
= Ending MRR

Net Revenue Retention = (Beginning MRR + Expansion - Contraction - Churn) / Beginning MRR
```

---

## 2. Unit Economics

### Customer Acquisition Cost (CAC)

```
CAC = (Sales + Marketing spend) / New customers acquired

Fully-loaded CAC includes:
- Sales team compensation (base + commission)
- Marketing spend (paid + content + events)
- Sales tools and technology
- Allocated overhead

Blended CAC: All customers (organic + paid)
Paid CAC: Only paid-acquired customers
```

### Lifetime Value (LTV)

```
LTV = ARPA × Gross Margin / Revenue Churn Rate

Or: LTV = ARPA × Gross Margin × Average Customer Lifetime

Where:
  ARPA = Average Revenue Per Account (monthly or annual)
  Gross Margin = (Revenue - COGS) / Revenue
  Average Lifetime = 1 / Churn Rate
```

### LTV:CAC Ratio

| Ratio | Interpretation | Action |
|---|---|---|
| <1:1 | Losing money on each customer | Fix unit economics urgently |
| 1-2:1 | Barely profitable | Improve retention or reduce CAC |
| 3:1 | Healthy and sustainable | Maintain, consider investing more |
| 5:1+ | Very efficient (or under-investing) | Invest more in growth |

---

## 3. Growth Metrics

### Growth Rate Calculations

| Metric | Formula | Context |
|---|---|---|
| MoM growth | (This month - Last month) / Last month | Monthly momentum |
| YoY growth | (This year - Last year) / Last year | Annual trajectory |
| CAGR | (End value / Start value)^(1/years) - 1 | Multi-year growth |
| T2D3 | Triple, triple, double, double, double | VC growth expectation |

### Net Revenue Retention (NRR)

| NRR Range | Interpretation | Typical Company |
|---|---|---|
| <90% | Significant churn problem | High-churn SMB |
| 90-100% | Stable but not growing from base | Average SaaS |
| 100-110% | Healthy expansion | Good mid-market SaaS |
| 110-130% | Strong expansion motion | Best-in-class |
| 130%+ | Exceptional (usage-based often) | Snowflake, Datadog |

### Cohort Analysis

```
Month 0: 100% (all customers in cohort)
Month 1: 95% (5% churned)
Month 3: 88% (12% cumulative churn)
Month 6: 82% (18% cumulative churn)
Month 12: 75% (25% cumulative churn)

With expansion:
Month 0: 100% of revenue
Month 12: 115% of revenue (expansion > churn)
```

---

## 4. Efficiency Metrics

### Key Efficiency Ratios

| Metric | Formula | Good Benchmark |
|---|---|---|
| Magic Number | Net New ARR / Prior quarter S&M spend | >0.75 |
| CAC Payback | CAC / (Monthly ARPA × Gross Margin) | <12 months |
| Burn Multiple | Net Burn / Net New ARR | <2x |
| Rule of 40 | Growth Rate + FCF Margin | >40% |
| Gross Margin | (Revenue - COGS) / Revenue | >70% (SaaS) |
| Operating Margin | Operating Income / Revenue | Improving toward positive |
| FCF Margin | Free Cash Flow / Revenue | Improving toward positive |

### Burn Rate and Runway

```
Gross Burn = Total monthly expenses
Net Burn = Total expenses - Total revenue
Cash Runway = Cash balance / Net Burn (months)

Example:
  Cash: $10M
  Monthly revenue: $500K
  Monthly expenses: $1.2M
  Net burn: $700K/month
  Runway: 14.3 months

Target: Always maintain 12+ months runway
```

---

## 5. Benchmarks by Stage

### SaaS Benchmarks by ARR

| Metric | $1-5M ARR | $5-20M ARR | $20-50M ARR | $50M+ ARR |
|---|---|---|---|---|
| YoY Growth | 100-200% | 80-120% | 50-80% | 30-50% |
| Gross Margin | 60-70% | 70-80% | 75-85% | 80-85% |
| Net Retention | 100-110% | 110-120% | 115-130% | 120-140% |
| CAC Payback | 12-18 months | 12-15 months | 10-14 months | 8-12 months |
| Burn Multiple | 2-4x | 1.5-2.5x | 1-2x | <1.5x |
| Rule of 40 | 40-80% | 40-60% | 35-50% | 30-45% |

### Median SaaS Metrics (2024-2025)

| Metric | Median | Top Quartile |
|---|---|---|
| Gross margin | 75% | 82%+ |
| Net revenue retention | 110% | 125%+ |
| CAC payback | 15 months | 10 months |
| LTV:CAC | 3.5:1 | 5:1+ |
| Logo churn (annual) | 10-15% | <5% |
| Revenue churn (annual) | 8-12% | <5% |
| Magic number | 0.6 | 1.0+ |
