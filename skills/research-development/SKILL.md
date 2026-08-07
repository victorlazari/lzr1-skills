---
name: research-development
description: Comprehensive research and development skill covering innovation strategy, technical research methodology, R&D management, technology scouting, and emerging technology evaluation for technology companies. Use when conducting technical research, evaluating emerging technologies, developing innovation strategies, managing R&D programs, or building technology roadmaps.
---

# Research & Development

Expert-level R&D covering innovation strategy, technical research methodology, R&D management, technology scouting, and emerging technology evaluation.

## Scope and Triggers

- **Handles:** Technical research, literature reviews, emerging technology evaluation, innovation strategy development, R&D portfolio management, technology scouting, and research roadmaps.
- **Activates when:** Task involves technical research, evaluating emerging technologies, developing innovation strategies, managing R&D programs, or building technology roadmaps.
- **Non-goals:** Not for financial modeling, valuation, or investment research (use `finance-pro-playbooks`). Not for adopting a specialized professional role for execution (use `ai-teammates`).

## Preconditions

- Detect the target domain (innovation strategy, research methodology, or technology evaluation).
- Ensure the user intent is clear and the problem statement is defined before proceeding with technology evaluation.

## Source Freshness

- **ISO 56000:2025 Innovation management:** Verified against upstream 2026-08-07. See `references/innovation-strategy.md`.
- **Technology Readiness Assessment Guidebook (Feb 2025):** Verified against upstream 2026-08-07. See `references/technology-evaluation.md`.

## Workflow

1. **Understand the context and define the specific problem statement** before any evaluation.
2. **Select the appropriate domain reference** (innovation strategy, research methodology, or technology evaluation).
3. **Conduct AI-powered technology scouting** and literature review.
4. **Evaluate technologies** using the updated TRL definitions from the 2025 DoD TRA Guidebook.
5. **Synthesize findings** and identify patterns or gaps.
6. **Recommend actionable insights** and decisions based on the evaluation.
7. **Stop** when a unified recommendation with explicit trade-offs is produced.

## Safety

- Separate read-only discovery from mutations.
- Require confirmation for destructive, external, privileged, financial, legal, or production-impacting actions.

## Validation

- Verify that all technology evaluations start with a documented problem statement.
- Ensure TRL assessments follow the 2025 DoD guidelines.
- Validate that innovation strategies align with ISO 56000:2025 principles.
- Check that AI scouting is used before finalizing vendor shortlists.

## Failure Handling

- If evaluation fails, diagnose the issue, choose alternative technologies, and avoid repeating the same failed evaluation.

## Output Contract

- A unified recommendation with explicit trade-offs.
- Documented problem statement.
- TRL assessments following 2025 DoD guidelines.
- Innovation strategies aligned with ISO 56000:2025 principles.

## Resources

- `references/innovation-strategy.md`: Innovation strategy and programs.
- `references/research-methodology.md`: Technical research methodology.
- `references/technology-evaluation.md`: Technology evaluation and scouting.
- `references/reading-list.md`: Recommended reading and resources.

## Orchestration

### Multi-Specialist Protocol

When multiple domains are detected, spawn all relevant specialists simultaneously — do not serialize them.

#### Domain Detection Table

| Task Signal (examples) | Domain | Specialist Agent | Reference |
|---|---|---|---|
| `innovation`, `ideation`, `emerging technology`, `technology radar`, `strategic bet`, `R&D roadmap`, `future-proofing`, `disruptive` | **Innovation Strategy** | Innovation Specialist | `references/innovation-strategy.md` |
| `research methodology`, `experiment design`, `hypothesis`, `qualitative study`, `quantitative analysis`, `user study`, `literature review`, `research protocol` | **Research Methodology** | Methodology Specialist | `references/research-methodology.md` |
| `technology evaluation`, `build vs buy`, `proof of concept`, `POC`, `vendor selection`, `benchmark`, `evaluation criteria`, `due diligence`, `tech assessment` | **Technology Evaluation** | Tech Eval Specialist | `references/technology-evaluation.md` |

#### Spawning Logic

**Single domain detected** → Fall back to original single-reference behavior (no change).

**Multiple domains detected** → Launch all relevant specialists simultaneously:
- Each specialist receives: **full task context** + its dedicated reference file only
- No specialist waits for another — all start at the same time
- Maximum concurrent specialists: 3

#### Cross-Domain Synthesizer

After all specialists complete, run one **R&D Decision Synthesizer** with all specialist outputs that:

1. **Identifies contradictions** between specialist recommendations for the same component
2. **Identifies gaps** — requirements addressed by no specialist
3. **Identifies dependencies** — where Domain A's output is a prerequisite for Domain B's recommendation
4. **Produces** a unified recommendation with explicit trade-off annotations for any resolved contradictions

> Synthesis focus for this skill: Ensures the technology evaluation methodology is appropriate for the innovation strategy goals. Flags where evaluation criteria bias toward known solutions when the strategy calls for exploration.

## Authoritative sources

- [Authoritative source map](references/source-map.md) — consult this before relying on volatile upstream behavior.

## Package resource index

| Resource | Purpose |
|---|---|
| [references/source-map.md](references/source-map.md) | Supporting package resource; inspect before use and apply the workflow’s safety and validation gates. |
