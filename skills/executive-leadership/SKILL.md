---
name: executive-leadership
description: Comprehensive executive leadership skill covering CEO strategy, CTO technology leadership, CFO financial strategy, COO operations, VP Engineering management, and Chief of Staff coordination for technology companies. Use when making strategic decisions, building executive presentations, planning company direction, managing boards, fundraising, or leading organizational transformation.
---

# Executive Leadership

Expert-level executive leadership covering CEO strategy, CTO technology leadership, CFO financial strategy, COO operations, VP Engineering management, and Chief of Staff coordination.

## When to Use

- Strategic planning and company direction
- Board presentations and investor communications
- Fundraising strategy and pitch decks
- Organizational design and scaling
- Technology strategy and roadmap
- Financial planning and modeling
- Executive decision-making frameworks
- Leadership team coordination

## Workflow

1. **Understand the context** — What decision, audience, and strategic challenge?
2. **Select reference** — Choose the appropriate domain:
   - CEO strategy and vision → `references/ceo-strategy.md`
   - CTO technology leadership → `references/cto-technology.md`
   - CFO financial strategy → `references/cfo-finance.md`
   - Organizational leadership → `references/org-leadership.md`
3. **Analyze** — Data, market, competitive landscape
4. **Decide** — Framework-driven decision-making
5. **Communicate** — Stakeholder-appropriate messaging
6. **Execute** — Alignment, accountability, follow-through

## Core Principles (All Executive Work)

- Strategic: Think long-term, act short-term
- Data-informed: Use data to guide, not dictate
- Decisive: Make decisions with incomplete information
- Transparent: Communicate openly with stakeholders
- Accountable: Own outcomes, not just activities
- Scalable: Build for the next stage of growth
- People-first: Great companies are built by great teams
- Customer-obsessed: Revenue follows customer value

## Role Capabilities

| Role | Expertise | Reference |
|---|---|---|
| CEO | Vision, strategy, fundraising, board | `references/ceo-strategy.md` |
| CTO | Technology strategy, architecture, R&D | `references/cto-technology.md` |
| CFO | Financial strategy, fundraising, metrics | `references/cfo-finance.md` |
| COO / VP Eng / CoS | Operations, org design, execution | `references/org-leadership.md` |

## Key References

- **CEO strategy**: See `references/ceo-strategy.md` for vision and strategic planning.
- **CTO technology**: See `references/cto-technology.md` for technology leadership.
- **CFO finance**: See `references/cfo-finance.md` for financial strategy.
- **Organizational leadership**: See `references/org-leadership.md` for org design and execution.
- **Recommended reading**: See `references/reading-list.md` for curated books and articles.

---

## Multi-Specialist Protocol

> **Replaces the single "Select reference" step.** When multiple domains are detected, spawn all relevant specialists simultaneously — do not serialize them.

### Domain Detection Table

Scan the task for signals that indicate which domains apply:

| Task Signal (examples) | Domain | Specialist Agent | Reference |
|---|---|---|---|
| `strategy`, ... | **CEO / Strategy** | CEO Lens | `references/ceo-strategy.md` |
| `finance`, ... | **CFO / Finance** | CFO Lens | `references/cfo-finance.md` |
| `technology`, ... | **CTO / Technology** | CTO Lens | `references/cto-technology.md` |
| `org`, ... | **Org & Leadership** | Org Lens | `references/org-leadership.md` |

### Spawning Logic

**Single domain detected** → Fall back to original single-reference behavior (no change).

**Multiple domains detected** → Launch all relevant specialists simultaneously:
- Each specialist receives: **full task context** + its dedicated reference file only
- No specialist waits for another — all start at the same time
- Maximum concurrent specialists: 4

### Cross-Domain Synthesizer

After all specialists complete, run one **Executive Decision Synthesizer** with all specialist outputs that:

1. **Identifies contradictions** between specialist recommendations for the same component
2. **Identifies gaps** — requirements addressed by no specialist
3. **Identifies dependencies** — where Domain A's output is a prerequisite for Domain B's recommendation
4. **Produces** a unified recommendation with explicit trade-off annotations for any resolved contradictions

> Synthesis focus for this skill: Surfaces where a CTO's technical recommendation conflicts with the CFO's financial model. Ensures strategic decisions account for org capacity to execute.
