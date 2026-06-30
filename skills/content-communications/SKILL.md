---
name: content-communications
description: Comprehensive content and communications skill covering content strategy, technical writing, copywriting, corporate communications, and developer relations for technology companies. Use when creating content strategies, writing technical documentation, crafting marketing copy, managing corporate communications, or building developer advocacy programs.
---

# Content & Communications

Expert-level content and communications covering content strategy, technical writing, copywriting, corporate communications, and developer relations for technology companies.

## When to Use

- Creating content strategies and editorial calendars
- Writing technical documentation and guides
- Crafting marketing copy and messaging
- Managing corporate and internal communications
- Building developer relations programs
- Creating thought leadership content
- Writing press releases and announcements
- Developing brand voice and style guides

## Workflow

1. **Understand the context** — What audience, channel, and communication goal?
2. **Select reference** — Choose the appropriate domain:
   - Content strategy and planning → `references/content-strategy.md`
   - Technical writing → `references/technical-writing.md`
   - Copywriting and messaging → `references/copywriting.md`
   - Corporate communications → `references/corporate-comms.md`
3. **Research** — Audience, competitors, industry context
4. **Plan** — Outline, structure, key messages
5. **Create** — Write, edit, refine
6. **Distribute** — Publish, promote, measure

## Core Principles (All Content Work)

- Audience-first: Know who you're writing for
- Clear over clever: Clarity beats creativity
- Value-driven: Every piece should provide value
- Consistent: Brand voice, style, quality
- Measurable: Track performance, iterate
- Accessible: Inclusive language, readable formats
- Strategic: Content serves business objectives
- Authentic: Genuine voice, not corporate speak

## Role Capabilities

| Role | Expertise | Reference |
|---|---|---|
| Content Strategist | Strategy, planning, governance | `references/content-strategy.md` |
| Technical Writer | Documentation, guides, API docs | `references/technical-writing.md` |
| Copywriter | Marketing copy, messaging, ads | `references/copywriting.md` |
| Communications Manager | Corporate comms, PR, internal | `references/corporate-comms.md` |

## Key References

- **Content strategy**: See `references/content-strategy.md` for planning and governance.
- **Technical writing**: See `references/technical-writing.md` for documentation.
- **Copywriting**: See `references/copywriting.md` for marketing and messaging.
- **Corporate communications**: See `references/corporate-comms.md` for PR and internal comms.
- **Recommended reading**: See `references/reading-list.md` for curated books and articles.

---

## Multi-Specialist Protocol

> **Replaces the single "Select reference" step.** When multiple domains are detected, spawn all relevant specialists simultaneously — do not serialize them.

### Domain Detection Table

Scan the task for signals that indicate which domains apply:

| Task Signal (examples) | Domain | Specialist Agent | Reference |
|---|---|---|---|
| `content strategy`, ... | **Content Strategy** | Content Strategy Specialist | `references/content-strategy.md` |
| `copywriting`, ... | **Copywriting** | Copywriting Specialist | `references/copywriting.md` |
| `technical writing`, ... | **Technical Writing** | TechWrite Specialist | `references/technical-writing.md` |
| `PR`, ... | **Corporate Communications** | CorpComms Specialist | `references/corporate-comms.md` |

### Spawning Logic

**Single domain detected** → Fall back to original single-reference behavior (no change).

**Multiple domains detected** → Launch all relevant specialists simultaneously:
- Each specialist receives: **full task context** + its dedicated reference file only
- No specialist waits for another — all start at the same time
- Maximum concurrent specialists: 4

### Cross-Domain Synthesizer

After all specialists complete, run one **Voice & Tone Synthesizer** with all specialist outputs that:

1. **Identifies contradictions** between specialist recommendations for the same component
2. **Identifies gaps** — requirements addressed by no specialist
3. **Identifies dependencies** — where Domain A's output is a prerequisite for Domain B's recommendation
4. **Produces** a unified recommendation with explicit trade-off annotations for any resolved contradictions

> Synthesis focus for this skill: Ensures brand voice is consistent across technical docs and marketing copy. Catches where a PR message contradicts the product documentation.
