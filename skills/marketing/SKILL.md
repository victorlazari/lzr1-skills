---
name: marketing
description: Comprehensive marketing skill covering digital marketing, content marketing, SEO, growth marketing, brand strategy, marketing analytics, and demand generation. Use when creating marketing strategies, writing copy, planning campaigns, optimizing SEO, analyzing marketing performance, or building brand positioning.
---

# Marketing

Expert-level marketing covering digital strategy, content, SEO, growth, brand, analytics, demand generation, and marketing operations for B2B and B2C organizations.

## When to Use

- Creating marketing strategies and campaign plans
- Writing marketing copy and content
- SEO strategy and optimization
- Growth marketing and demand generation
- Brand strategy and positioning
- Marketing analytics and attribution
- Email marketing and automation
- Social media strategy and execution

## Workflow

1. **Understand the context** — What product, audience, stage, and goals?
2. **Select reference** — Choose the appropriate domain:
   - Digital and content strategy → `references/digital-marketing.md`
   - SEO and organic growth → `references/seo.md`
   - Brand and positioning → `references/brand-strategy.md`
   - Analytics and measurement → `references/marketing-analytics.md`
3. **Research** — Audience, competitors, channels, and benchmarks
4. **Strategize** — Define objectives, channels, messaging, and budget
5. **Execute** — Create content, launch campaigns, optimize
6. **Measure** — Track KPIs, attribute results, iterate

## Core Principles (All Marketing Work)

- Customer-first: Understand the audience before creating anything
- Data-driven: Measure everything, optimize based on evidence
- Consistency: Unified brand voice and messaging across channels
- Value-first: Provide value before asking for anything
- Test and iterate: Small experiments before big bets
- Full-funnel thinking: Awareness through retention, not just acquisition
- Channel-market fit: Right message, right channel, right time
- ROI-focused: Every activity should tie to business outcomes

## Role Capabilities

| Role | Expertise | Reference |
|---|---|---|
| Digital Marketer | Campaigns, channels, paid media | `references/digital-marketing.md` |
| Content Marketer | Strategy, creation, distribution | `references/digital-marketing.md` |
| SEO Specialist | Technical SEO, content SEO, link building | `references/seo.md` |
| Growth Marketer | Acquisition, activation, experimentation | `references/digital-marketing.md` |
| Brand Strategist | Positioning, messaging, identity | `references/brand-strategy.md` |
| Marketing Analyst | Attribution, reporting, optimization | `references/marketing-analytics.md` |
| Marketing Ops | Automation, tech stack, processes | `references/marketing-analytics.md` |

## Key References

- **Digital marketing**: See `references/digital-marketing.md` for channels, content, and campaigns.
- **SEO**: See `references/seo.md` for search optimization strategy and tactics.
- **Brand strategy**: See `references/brand-strategy.md` for positioning and messaging.
- **Marketing analytics**: See `references/marketing-analytics.md` for measurement and attribution.
- **Recommended reading**: See `references/reading-list.md` for curated books and articles.

---

## Multi-Specialist Protocol

> **Replaces the single "Select reference" step.** When multiple domains are detected, spawn all relevant specialists simultaneously — do not serialize them.

### Domain Detection Table

Scan the task for signals that indicate which domains apply:

| Task Signal (examples) | Domain | Specialist Agent | Reference |
|---|---|---|---|
| `brand`, `positioning`, `identity`, `brand voice`, `messaging`, `narrative`, `value proposition`, `brand strategy` | **Brand & Positioning** | Brand Specialist | `references/brand-strategy.md` |
| `demand gen`, `lead generation`, `MQL`, `paid ads`, `campaign`, `ABM`, `outbound`, `inbound`, `acquisition`, `digital marketing` | **Demand Generation** | Demand Gen Specialist | `references/digital-marketing.md` |
| `SEO`, `organic`, `keyword`, `search ranking`, `backlink`, `content SEO`, `technical SEO`, `search intent`, `SERP` | **SEO** | SEO Specialist | `references/seo.md` |
| `analytics`, `attribution`, `CAC`, `ROAS`, `funnel`, `conversion rate`, `marketing metrics`, `dashboard`, `reporting` | **Marketing Analytics** | Analytics Specialist | `references/marketing-analytics.md` |

### Spawning Logic

**Single domain detected** → Fall back to original single-reference behavior (no change).

**Multiple domains detected** → Launch all relevant specialists simultaneously:
- Each specialist receives: **full task context** + its dedicated reference file only
- No specialist waits for another — all start at the same time
- Maximum concurrent specialists: 4

### Cross-Domain Synthesizer

After all specialists complete, run one **Campaign Synthesizer** with all specialist outputs that:

1. **Identifies contradictions** between specialist recommendations for the same component
2. **Identifies gaps** — requirements addressed by no specialist
3. **Identifies dependencies** — where Domain A's output is a prerequisite for Domain B's recommendation
4. **Produces** a unified recommendation with explicit trade-off annotations for any resolved contradictions

> Synthesis focus for this skill: Ensures messaging aligns with funnel metrics targets. Catches where a brand positioning change requires a demand gen strategy adjustment.
