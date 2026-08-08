# Operational Excellence

**Verified against upstream:** 2026-08-07
**Primary Sources:**
- Shingo Model (https://shingo.org/shingo-model/)
- Shingo Institute (https://shingo.org/about-the-shingo-institute/)

## Table of Contents
1. Operational Metrics
2. Capacity Planning
3. Business Continuity
4. Scaling Operations
5. OKRs and Goal Setting

---

## 1. Operational Metrics (Shingo Model Integration)

Focus on Cultural Enablers, Continuous Improvement, and Enterprise Alignment.

### Key Operational KPIs

| Category | Metric | Description |
|---|---|---|
| Efficiency | Process cycle time | Time from start to completion |
| Efficiency | Throughput | Units processed per time period |
| Efficiency | Utilization | % of capacity being used |
| Quality | Error rate | Defects per unit of work |
| Quality | First-time-right | % completed correctly first time |
| Cost | Cost per transaction | Total cost / Volume |
| Cost | Operating expense ratio | OpEx / Revenue |
| Customer | Response time | Time to first response |
| Customer | Resolution time | Time to full resolution |
| People | Productivity | Output per person |
| Culture | Employee Engagement | eNPS, turnover rate |
| Culture | Safety Incidents | Number of safety incidents |

### Dashboard Design

| Audience | Metrics Focus | Update Frequency |
|---|---|---|
| Executive | Revenue, efficiency, strategic KPIs | Weekly/Monthly |
| Operations Manager | Process metrics, SLAs, capacity | Daily |
| Team Lead | Task completion, quality, blockers | Real-time |
| Individual | Personal productivity, queue | Real-time |

---

## 2. Capacity Planning

### Capacity Planning Process

| Step | Activity | Output |
|---|---|---|
| 1. Demand forecast | Predict future workload | Volume projections |
| 2. Current capacity | Assess existing resources | Capacity baseline |
| 3. Gap analysis | Compare demand vs capacity | Shortfall/surplus |
| 4. Options | Identify ways to close gap | Hiring, automation, outsourcing |
| 5. Decision | Choose approach | Capacity plan |
| 6. Execute | Implement changes | Updated capacity |
| 7. Monitor | Track actual vs planned | Adjustments |

### Resource Planning

```
Required headcount = Demand volume × Time per unit / Available hours per person

Example:
  Monthly tickets: 5,000
  Average handle time: 30 minutes
  Available hours per agent: 140 hours/month (accounting for meetings, breaks)
  Required agents: 5,000 × 0.5 / 140 = 17.9 → 18 agents

  Add buffer (20%): 18 × 1.2 = 22 agents
```

---

## 3. Business Continuity

### Business Continuity Plan (BCP)

| Component | Description |
|---|---|
| Risk assessment | Identify threats and vulnerabilities |
| Business impact analysis | Determine critical functions and RTOs |
| Recovery strategies | How to restore operations |
| Plan documentation | Written procedures for each scenario |
| Testing | Regular drills and exercises |
| Maintenance | Annual review and updates |

### Recovery Objectives

| Metric | Definition | Example |
|---|---|---|
| RTO (Recovery Time Objective) | Max acceptable downtime | 4 hours |
| RPO (Recovery Point Objective) | Max acceptable data loss | 1 hour |
| MTPD (Maximum Tolerable Period of Disruption) | Absolute max before irreversible damage | 24 hours |

### Critical Function Priority

| Priority | Functions | RTO |
|---|---|---|
| P1 - Critical | Customer-facing services, payment processing | <1 hour |
| P2 - Essential | Internal tools, communication, support | <4 hours |
| P3 - Important | Reporting, analytics, non-urgent processes | <24 hours |
| P4 - Deferrable | Training, non-critical projects | <72 hours |

---

## 4. Scaling Operations

### Scaling Strategies

| Strategy | Description | When to Use |
|---|---|---|
| Standardize | Create SOPs, templates, playbooks | Before scaling |
| Automate | Remove manual steps | Repetitive, high-volume |
| Outsource | External partners for non-core | Cost-effective, scalable |
| Self-service | Enable customers/employees to help themselves | High-volume, simple requests |
| Specialize | Dedicated teams for specific functions | Complexity requires expertise |
| Platform | Build internal tools | Unique processes at scale |

### Operational Maturity Model

| Level | Characteristics | Focus |
|---|---|---|
| 1 - Reactive | Ad hoc, heroic efforts | Survival |
| 2 - Defined | Documented processes, some consistency | Documentation |
| 3 - Managed | Metrics, SLAs, regular reviews | Measurement |
| 4 - Optimized | Continuous improvement, automation | Efficiency |
| 5 - Innovative | Predictive, AI-driven, industry-leading | Innovation |

---

## 5. OKRs and Goal Setting

### OKR Framework

```
Objective: Qualitative, inspiring, time-bound
  Key Result 1: Quantitative, measurable outcome
  Key Result 2: Quantitative, measurable outcome
  Key Result 3: Quantitative, measurable outcome

Scoring:
  0.0 - 0.3: Failed to make progress
  0.4 - 0.6: Made progress but fell short
  0.7 - 1.0: Delivered (0.7 is often the target for stretch goals)
```

### OKR Alignment

| Level | Objective Focus | Cadence |
|---|---|---|
| Company | Strategic direction, big bets | Annual + Quarterly |
| Department | Functional contribution to company goals | Quarterly |
| Team | Specific deliverables and outcomes | Quarterly |
| Individual | Personal contribution to team goals | Quarterly |

### Goal-Setting Best Practices

| Practice | Description |
|---|---|
| Outcome-focused | Measure results, not activities |
| Ambitious | Stretch goals (70% achievement = success) |
| Measurable | Clear, quantifiable key results |
| Time-bound | Quarterly cadence with check-ins |
| Aligned | Connected to company strategy |
| Transparent | Visible across the organization |
| Limited | 3-5 objectives, 3-5 KRs each |

## Recommended Reading (Source Map)
- **The Goal** — Eliyahu Goldratt (1984), North River Press. Theory of constraints.
- **The Phoenix Project** — Gene Kim et al. (2013), IT Revolution. IT operations novel.
- **The Unicorn Project** — Gene Kim (2019), IT Revolution. Developer productivity.
- **Operations Management** — Nigel Slack et al. (9th ed, 2022), Pearson.
- **Good Strategy Bad Strategy** — Richard Rumelt (2011), Crown. Strategy fundamentals.
- **The Hard Thing About Hard Things** — Ben Horowitz (2014), Harper Business. Operational challenges.
- **Scaling Up** — Verne Harnish (2014), Gazelles. Growth operations.
- **Blitzscaling** — Reid Hoffman & Chris Yeh (2018), Currency. Rapid scaling.
- **High Output Management** — Andy Grove (1983), Vintage. Management operations.
- **The Great CEO Within** — Matt Mochary (2019). Operational excellence for leaders.
- **Measure What Matters** — John Doerr (2018), Portfolio. OKRs.
- **Radical Focus** — Christina Wodtke (2nd ed, 2021). OKR implementation.
- **Business Continuity Management** — Michael Blyth (2009), Wiley.
- **The Resilient Enterprise** — Yossi Sheffi (2005), MIT Press. Supply chain resilience.
- **First Round Review** — review.firstround.com. Startup operations insights.
- **a16z Operations** — a16z.com. Scaling operations.
- **Stripe Atlas Guides** — stripe.com/atlas/guides. Startup operations.
- **The Mochary Method** — mocharymethod.com. CEO operations.
- **What Matters** — whatmatters.com. OKR resources (John Doerr).
- **Lattice OKR Guide** — lattice.com/library. OKR implementation.
- **GitLab OKR Handbook** — handbook.gitlab.com. OKR in practice.
- **SaaStr Operations** — saastr.com. SaaS scaling.
- **Y Combinator Library** — ycombinator.com/library. Startup scaling.
- **Sequoia Arc** — sequoiacap.com. Company building.
- **BCI (Business Continuity Institute)** — thebci.org. BC resources.
- **FEMA Continuity** — fema.gov. Business continuity planning.
- **AWS Well-Architected** — aws.amazon.com/architecture. Operational excellence pillar.
