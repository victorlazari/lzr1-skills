---
name: product-management
description: Comprehensive product management skill covering product strategy, roadmapping, discovery, prioritization, growth, and technical product management. Use when defining product vision, writing PRDs, prioritizing features, conducting discovery, analyzing metrics, planning roadmaps, or making product decisions.
---

# Product Management

Expert-level product management covering strategy, discovery, delivery, growth, and technical product management for digital products.

## When to Use

- Defining product vision and strategy
- Writing PRDs, specs, and user stories
- Prioritizing features and managing backlogs
- Conducting product discovery
- Analyzing product metrics and KPIs
- Planning roadmaps and releases
- Growth strategy and experimentation
- Stakeholder communication and alignment

## Workflow

1. **Understand the context** — What product, stage, market, and constraints?
2. **Select reference** — Choose the appropriate domain:
   - Strategy and vision → `references/product-strategy.md`
   - Discovery and validation → `references/product-discovery.md`
   - Execution and delivery → `references/product-delivery.md`
   - Growth and metrics → `references/product-growth.md`
3. **Frame the problem** — Define the opportunity clearly before solutions
4. **Gather evidence** — Data, research, customer feedback
5. **Decide and communicate** — Make decisions, align stakeholders
6. **Measure and iterate** — Track outcomes, learn, adjust

## Core Principles (All Product Work)

- Outcomes over outputs: Measure impact, not features shipped
- Customer-centric: Every decision should trace back to user value
- Evidence-based: Validate assumptions before building
- Prioritize ruthlessly: Say no to most things to focus on what matters
- Think in bets: Acknowledge uncertainty, size bets accordingly
- Cross-functional: Product is a team sport (eng, design, data, business)
- Iterate: Ship small, learn fast, compound improvements
- Communicate clearly: Alignment is the PM's primary job

## Role Capabilities

| Role | Expertise | Reference |
|---|---|---|
| Product Manager | Strategy, discovery, delivery | All references |
| Technical PM | APIs, platforms, developer experience | `references/product-delivery.md` |
| Growth PM | Acquisition, activation, retention | `references/product-growth.md` |
| Product Strategist | Vision, market, positioning | `references/product-strategy.md` |

## Key References

- **Product strategy**: See `references/product-strategy.md` for vision, positioning, and roadmaps.
- **Product discovery**: See `references/product-discovery.md` for validation and research.
- **Product delivery**: See `references/product-delivery.md` for execution, specs, and agile.
- **Product growth**: See `references/product-growth.md` for metrics, experimentation, and growth.
- **Recommended reading**: See `references/reading-list.md` for curated books and articles.

---

## Multi-Specialist Protocol

> **Replaces the single "Select reference" step.** When multiple domains are detected, spawn all relevant specialists simultaneously — do not serialize them.

### Domain Detection Table

Scan the task for signals that indicate which domains apply:

| Task Signal (examples) | Domain | Specialist Agent | Reference |
|---|---|---|---|
| `discovery`, ... | **Product Discovery** | Discovery Specialist | `references/product-discovery.md` |
| `delivery`, ... | **Product Delivery** | Delivery Specialist | `references/product-delivery.md` |
| `strategy`, ... | **Product Strategy** | Strategy Specialist | `references/product-strategy.md` |
| `growth`, ... | **Product Growth** | Growth Specialist | `references/product-growth.md` |

### Spawning Logic

**Single domain detected** → Fall back to original single-reference behavior (no change).

**Multiple domains detected** → Launch all relevant specialists simultaneously:
- Each specialist receives: **full task context** + its dedicated reference file only
- No specialist waits for another — all start at the same time
- Maximum concurrent specialists: 4

### Cross-Domain Synthesizer

After all specialists complete, run one **Product Decision Synthesizer** with all specialist outputs that:

1. **Identifies contradictions** between specialist recommendations for the same component
2. **Identifies gaps** — requirements addressed by no specialist
3. **Identifies dependencies** — where Domain A's output is a prerequisite for Domain B's recommendation
4. **Produces** a unified recommendation with explicit trade-off annotations for any resolved contradictions

> Synthesis focus for this skill: Ensures growth instrumentation is included in delivery planning. Flags where a strategy decision requires discovery validation before execution begins.
