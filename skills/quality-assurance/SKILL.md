---
name: quality-assurance
description: Comprehensive quality assurance skill covering test strategy, test automation, performance testing, API testing, and QA processes for software products. Use when designing test strategies, writing test plans, building automation frameworks, conducting performance testing, or establishing QA processes.
---

# Quality Assurance

Expert-level QA covering test strategy, automation, performance testing, API testing, and quality processes for software products.

## When to Use

- Designing test strategies and test plans
- Building test automation frameworks
- Performance and load testing
- API and integration testing
- QA process design and metrics
- Bug triage and defect management
- Test environment management
- Release quality gates

## Workflow

1. **Understand the context** — What product, stack, and quality goals?
2. **Select reference** — Choose the appropriate domain:
   - Test strategy and planning → `references/test-strategy.md`
   - Test automation → `references/test-automation.md`
   - Performance testing → `references/performance-testing.md`
3. **Plan** — Define scope, approach, and coverage
4. **Design** — Create test cases, data, and environments
5. **Execute** — Run tests, report results
6. **Improve** — Analyze trends, optimize coverage

## Core Principles (All QA Work)

- Shift left: Find bugs early, test early, involve QA in design
- Risk-based: Focus testing on highest-risk areas
- Automation-first: Automate repetitive tests, manual for exploratory
- Data-driven: Use metrics to guide testing decisions
- Continuous: Testing is ongoing, not a phase
- User-focused: Test from the user's perspective
- Reproducible: Tests should be deterministic and repeatable
- Collaborative: QA works with dev, product, and ops

## Role Capabilities

| Role | Expertise | Reference |
|---|---|---|
| QA Engineer | Test design, execution, processes | `references/test-strategy.md` |
| SDET/Automation Engineer | Frameworks, CI/CD integration | `references/test-automation.md` |
| Performance Engineer | Load testing, benchmarking | `references/performance-testing.md` |

## Key References

- **Test strategy**: See `references/test-strategy.md` for planning and methodology.
- **Test automation**: See `references/test-automation.md` for frameworks and CI/CD.
- **Performance testing**: See `references/performance-testing.md` for load and stress testing.
- **Recommended reading**: See `references/reading-list.md` for curated books and articles.

---

## Multi-Specialist Protocol

> **Replaces the single "Select reference" step.** When multiple domains are detected, spawn all relevant specialists simultaneously — do not serialize them.

### Domain Detection Table

Scan the task for signals that indicate which domains apply:

| Task Signal (examples) | Domain | Specialist Agent | Reference |
|---|---|---|---|
| `test plan`, ... | **Test Strategy** | Strategy Specialist | `references/test-strategy.md` |
| `automation`, ... | **Test Automation** | Automation Specialist | `references/test-automation.md` |
| `performance`, ... | **Performance Testing** | Performance Specialist | `references/performance-testing.md` |

### Spawning Logic

**Single domain detected** → Fall back to original single-reference behavior (no change).

**Multiple domains detected** → Launch all relevant specialists simultaneously:
- Each specialist receives: **full task context** + its dedicated reference file only
- No specialist waits for another — all start at the same time
- Maximum concurrent specialists: 3

### Cross-Domain Synthesizer

After all specialists complete, run one **QA Synthesizer** with all specialist outputs that:

1. **Identifies contradictions** between specialist recommendations for the same component
2. **Identifies gaps** — requirements addressed by no specialist
3. **Identifies dependencies** — where Domain A's output is a prerequisite for Domain B's recommendation
4. **Produces** a unified recommendation with explicit trade-off annotations for any resolved contradictions

> Synthesis focus for this skill: Aligns automation coverage with strategy gaps. Ensures performance SLAs are reflected in the test plan. Flags where automation effort would be wasted without a strategy foundation.
