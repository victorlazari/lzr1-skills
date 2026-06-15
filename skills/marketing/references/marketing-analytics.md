# Marketing Analytics

## Table of Contents
1. Marketing Metrics Framework
2. Attribution Models
3. Marketing Technology Stack
4. Reporting and Dashboards
5. Marketing Operations

---

## 1. Marketing Metrics Framework

### Metrics by Funnel Stage

| Stage | Metrics | Tools |
|---|---|---|
| Awareness | Impressions, reach, brand searches, SOV | Google Ads, social platforms |
| Acquisition | Traffic, CTR, CPC, new visitors | GA4, ad platforms |
| Activation | Signups, trial starts, MQLs | CRM, marketing automation |
| Revenue | SQLs, pipeline, closed-won, ARPU | CRM, revenue tools |
| Retention | Churn, NRR, repeat purchase | Product analytics, CRM |
| Referral | NPS, referral rate, viral coefficient | Survey tools, referral platforms |

### Key Marketing KPIs

| Metric | Formula | Benchmark |
|---|---|---|
| CAC | Total marketing + sales cost / New customers | Varies by industry |
| LTV:CAC | Customer lifetime value / CAC | >3:1 |
| CAC payback | CAC / Monthly gross margin per customer | <12 months |
| Marketing ROI | (Revenue - Marketing cost) / Marketing cost | >5:1 |
| Pipeline velocity | Qualified leads × Win rate × Deal size / Sales cycle | Growing |
| Conversion rate | Conversions / Total visitors | 2-5% (website) |
| Cost per lead | Marketing spend / Leads generated | Varies by channel |

---

## 2. Attribution Models

### Attribution Model Comparison

| Model | Description | Best For |
|---|---|---|
| First touch | 100% credit to first interaction | Understanding awareness channels |
| Last touch | 100% credit to last interaction | Understanding conversion channels |
| Linear | Equal credit to all touchpoints | Simple multi-touch |
| Time decay | More credit to recent touchpoints | Short sales cycles |
| U-shaped | 40% first, 40% last, 20% middle | B2B with clear journey |
| W-shaped | 30% first, 30% lead creation, 30% opportunity, 10% rest | Complex B2B |
| Data-driven | ML-based credit assignment | Large data sets, sophisticated teams |

### Multi-Touch Attribution Challenges

| Challenge | Description | Mitigation |
|---|---|---|
| Cross-device | Users switch devices | Login-based tracking, probabilistic matching |
| Cookie deprecation | Third-party cookies going away | First-party data, server-side tracking |
| Walled gardens | Platforms don't share data | Platform-specific attribution + MMM |
| Offline touchpoints | Events, calls, word-of-mouth | UTM discipline, call tracking, surveys |
| Long sales cycles | Many touchpoints over months | CRM integration, full-journey tracking |

---

## 3. Marketing Technology Stack

### MarTech Categories

| Category | Purpose | Tools |
|---|---|---|
| CRM | Customer data, pipeline | Salesforce, HubSpot |
| Marketing automation | Email, nurture, scoring | HubSpot, Marketo, Pardot |
| Analytics | Web analytics, behavior | GA4, Mixpanel, Amplitude |
| Advertising | Paid media management | Google Ads, Meta Ads, LinkedIn |
| SEO | Search optimization | Ahrefs, Semrush, Moz |
| Content | CMS, creation, management | WordPress, Contentful, Webflow |
| Social | Management, listening | Hootsuite, Sprout Social |
| ABM | Account-based marketing | Demandbase, 6sense, Terminus |
| Data enrichment | Contact/company data | ZoomInfo, Clearbit, Apollo |
| CDP | Customer data platform | Segment, mParticle |

### MarTech Stack Architecture

```
Data Layer:
  CDP (Segment) → Data Warehouse (Snowflake/BigQuery)

Engagement Layer:
  Marketing Automation (HubSpot) → Email, Ads, Social

Intelligence Layer:
  Analytics (GA4 + Mixpanel) → Attribution → Reporting

Orchestration Layer:
  CRM (Salesforce) → Lead routing → Sales handoff
```

---

## 4. Reporting and Dashboards

### Marketing Dashboard Framework

| Dashboard | Audience | Metrics | Cadence |
|---|---|---|---|
| Executive | CMO, CEO | Revenue, pipeline, ROI | Monthly |
| Channel performance | Marketing team | By-channel metrics | Weekly |
| Campaign | Campaign managers | Campaign-specific KPIs | Real-time |
| Content | Content team | Traffic, engagement, conversions | Weekly |
| SEO | SEO team | Rankings, organic traffic, backlinks | Weekly |
| Paid media | Media buyers | ROAS, CPA, spend efficiency | Daily |

### Reporting Best Practices

| Practice | Description |
|---|---|
| Lead with outcomes | Start with business impact, then tactics |
| Compare to targets | Show actual vs goal, not just numbers |
| Show trends | Month-over-month, year-over-year |
| Segment data | By channel, campaign, audience |
| Include context | Explain anomalies, external factors |
| Actionable insights | "So what?" and "Now what?" for each finding |

---

## 5. Marketing Operations

### Marketing Ops Functions

| Function | Responsibility | Tools |
|---|---|---|
| Tech stack management | Evaluate, implement, maintain tools | All MarTech |
| Data management | Clean, enrich, govern marketing data | CDP, CRM |
| Process design | Campaign workflows, approvals | Project management |
| Reporting | Dashboards, attribution, ROI | BI tools, analytics |
| Lead management | Scoring, routing, lifecycle | Marketing automation, CRM |
| Compliance | GDPR, CAN-SPAM, consent | Consent management |
| Budget management | Allocation, tracking, forecasting | Financial tools |

### Lead Lifecycle

```
Anonymous → Known → Engaged → MQL → SAL → SQL → Opportunity → Customer

Definitions:
- Anonymous: Visited site, no identity
- Known: Provided email/info
- Engaged: Multiple interactions
- MQL: Meets scoring threshold
- SAL: Sales accepted
- SQL: Sales qualified (real opportunity)
- Opportunity: In pipeline
- Customer: Closed-won
```

### Campaign Operations Workflow

| Phase | Activities | Output |
|---|---|---|
| Brief | Goals, audience, budget, timeline | Campaign brief |
| Plan | Channels, content, targeting, schedule | Campaign plan |
| Build | Create assets, set up targeting, QA | Ready-to-launch campaign |
| Launch | Activate, monitor initial performance | Live campaign |
| Optimize | A/B test, adjust targeting/budget | Improved performance |
| Report | Analyze results, document learnings | Campaign report |
