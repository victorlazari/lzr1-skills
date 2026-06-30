---
name: research-development
description: Comprehensive research and development skill covering innovation strategy, technical research methodology, R&D management, technology scouting, and emerging technology evaluation for technology companies. Use when conducting technical research, evaluating emerging technologies, developing innovation strategies, managing R&D programs, or building technology roadmaps.
---

# Research & Development

Expert-level R&D covering innovation strategy, technical research methodology, R&D management, technology scouting, and emerging technology evaluation.

## When to Use

- Conducting technical research and literature reviews
- Evaluating emerging technologies for adoption
- Developing innovation strategies and programs
- Managing R&D portfolios and programs
- Technology scouting and competitive intelligence
- Patent analysis and IP strategy
- Building research roadmaps
- Academic-industry collaboration

## Workflow

1. **Understand the context** — What research question, technology, or innovation challenge?
2. **Select reference** — Choose the appropriate domain:
   - Innovation strategy and programs → `references/innovation-strategy.md`
   - Technical research methodology → `references/research-methodology.md`
   - Technology evaluation → `references/technology-evaluation.md`
3. **Research** — Literature review, technology scan, competitive analysis
4. **Analyze** — Synthesize findings, identify patterns
5. **Recommend** — Actionable insights, roadmap, decisions
6. **Communicate** — Reports, presentations, publications

## Core Principles (All R&D Work)

- Evidence-based: Ground decisions in data and research
- Systematic: Rigorous methodology, reproducible results
- Forward-looking: Anticipate trends, not just react
- Balanced: Short-term value and long-term bets
- Collaborative: Cross-functional, open to external input
- Measurable: Track innovation metrics and outcomes
- Ethical: Responsible innovation, consider societal impact
- Iterative: Rapid experimentation, fail fast, learn quickly

## Role Capabilities

| Role | Expertise | Reference |
|---|---|---|
| Innovation Strategist | Innovation programs, portfolio, culture | `references/innovation-strategy.md` |
| Technical Researcher | Research methodology, publications | `references/research-methodology.md` |
| Technology Scout | Emerging tech, evaluation, adoption | `references/technology-evaluation.md` |

## Key References

- **Innovation strategy**: See `references/innovation-strategy.md` for programs and portfolio.
- **Research methodology**: See `references/research-methodology.md` for technical research.
- **Technology evaluation**: See `references/technology-evaluation.md` for emerging tech.
- **Recommended reading**: See `references/reading-list.md` for curated books and articles.

---

## Multi-Specialist Protocol

> **Replaces the single "Select reference" step.** When multiple domains are detected, spawn all relevant specialists simultaneously — do not serialize them.

### Domain Detection Table

Scan the task for signals that indicate which domains apply:

| Task Signal (examples) | Domain | Specialist Agent | Reference |
|---|---|---|---|
| `innovation`, `ideation`, `emerging technology`, `technology radar`, `strategic bet`, `R&D roadmap`, `future-proofing`, `disruptive` | **Innovation Strategy** | Innovation Specialist | `references/innovation-strategy.md` |
| `research methodology`, `experiment design`, `hypothesis`, `qualitative study`, `quantitative analysis`, `user study`, `literature review`, `research protocol` | **Research Methodology** | Methodology Specialist | `references/research-methodology.md` |
| `technology evaluation`, `build vs buy`, `proof of concept`, `POC`, `vendor selection`, `benchmark`, `evaluation criteria`, `due diligence`, `tech assessment` | **Technology Evaluation** | Tech Eval Specialist | `references/technology-evaluation.md` |

### Spawning Logic

**Single domain detected** → Fall back to original single-reference behavior (no change).

**Multiple domains detected** → Launch all relevant specialists simultaneously:
- Each specialist receives: **full task context** + its dedicated reference file only
- No specialist waits for another — all start at the same time
- Maximum concurrent specialists: 3

### Cross-Domain Synthesizer

After all specialists complete, run one **R&D Decision Synthesizer** with all specialist outputs that:

1. **Identifies contradictions** between specialist recommendations for the same component
2. **Identifies gaps** — requirements addressed by no specialist
3. **Identifies dependencies** — where Domain A's output is a prerequisite for Domain B's recommendation
4. **Produces** a unified recommendation with explicit trade-off annotations for any resolved contradictions

> Synthesis focus for this skill: Ensures the technology evaluation methodology is appropriate for the innovation strategy goals. Flags where evaluation criteria bias toward known solutions when the strategy calls for exploration.
