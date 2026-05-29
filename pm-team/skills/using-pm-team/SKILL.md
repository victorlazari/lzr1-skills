---
name: lzr1:using-pm-team
description: |
  12 pre-dev workflow skills + 2 standalone discovery skills + 1 standalone dashboard skill + 4 research agents organized into
  Small Track (5 gates, <2 days) and Large Track (10 gates, 2+ days) for systematic feature
  planning with research-first approach.
---

# Using lzr1 Team-Product: Pre-Dev Workflow & Delivery Tracking

## When to use

- Starting any feature implementation
- Need systematic planning before coding
- User requests "plan a feature"

## Skip when

- Quick exploratory work → skip formal planning
- Bug fix with known solution → direct implementation
- Trivial change (<1 hour) → skip formal planning


The lzr1-pm-team plugin provides 12 pre-development planning skills and 4 research agents. Use them via `Skill tool: "lzr1:gate-name"`.

Follow the **ORCHESTRATOR principle** from `lzr1:using-lzr1`. Dispatch pre-dev workflow to handle planning; plan thoroughly before coding.

## Two Tracks: Choose Your Path

### Small Track (5 Gates) — <2 Day Features

Use when ALL criteria met: implementation <2 days, no new external dependencies, no new data models, no multi-service integration, uses existing architecture, single developer.

| Gate | Skill | Output |
|------|-------|--------|
| 0 | lzr1:pre-dev-research | research.md |
| 1 | lzr1:pre-dev-prd-creation | prd.md |
| 2 | lzr1:pre-dev-trd-creation | trd.md |
| 3 | lzr1:pre-dev-task-breakdown | tasks.md |
| 4 | lzr1:pre-dev-delivery-planning | delivery-roadmap.md + .json |

**Planning time:** 60-90 minutes

### Large Track (10 Gates) — ≥2 Day Features

Use when ANY criteria met: implementation ≥2 days, new external dependencies, new data models/entities, multi-service integration, new architecture patterns, team collaboration needed.

| Gate | Skill | Output |
|------|-------|--------|
| 0 | lzr1:pre-dev-research | research.md |
| 1 | lzr1:pre-dev-prd-creation | prd.md |
| 1.5 | lzr1:pre-dev-design-validation | design-validation.md (if UI) |
| 2 | lzr1:pre-dev-feature-map | feature-map.md |
| 2.5 | lzr1:pre-dev-design-validation | design-validation.md (if UI, Large) |
| 3 | lzr1:pre-dev-trd-creation | trd.md |
| 4 | lzr1:pre-dev-api-design | api-design.md |
| 5 | lzr1:pre-dev-data-model | data-model.md |
| 6 | lzr1:pre-dev-dependency-map | dependencies.md |
| 7 | lzr1:pre-dev-task-breakdown | tasks.md |
| 8 | lzr1:pre-dev-subtask-creation | subtasks/ |
| 9 | lzr1:pre-dev-delivery-planning | delivery-roadmap.md + .json |

**Planning time:** 2.5-5 hours

## Gate Summaries

| Gate | Skill | What It Does |
|------|-------|-------------|
| 0 | lzr1:pre-dev-research | Parallel research: codebase patterns, best practices, framework docs |
| 1 | lzr1:pre-dev-prd-creation | Business requirements (WHAT/WHY), user stories, success metrics |
| 1.5/2.5 | lzr1:pre-dev-design-validation | UX completeness check: screens, states, responsive, a11y |
| 2 | lzr1:pre-dev-feature-map | Feature relationships, dependencies, deployment order (Large only) |
| 3 | lzr1:pre-dev-trd-creation | Technical architecture, technology-agnostic patterns |
| 4 | lzr1:pre-dev-api-design | API contracts, operations, error handling (Large only) |
| 5 | lzr1:pre-dev-data-model | Entities, relationships, ownership (Large only) |
| 6 | lzr1:pre-dev-dependency-map | Explicit tech choices, versions, licenses (Large only) |
| 7 | lzr1:pre-dev-task-breakdown | Value-driven tasks with success criteria |
| 8 | lzr1:pre-dev-subtask-creation | Zero-context 2-5 min implementation steps (Large only) |
| 9/4 | lzr1:pre-dev-delivery-planning | Realistic schedule with critical path + JSON output |

## Standalone Skills

| Skill | When to Use |
|-------|-------------|
| lzr1:deep-doc-review | Before dev-cycle to catch doc contradictions |
| lzr1:delivery-status | Progress tracking against approved roadmap |
| lzr1:streaming-event-mapping | Map eventable points in Go service for lib-streaming |
| lzr1:creating-grafana-dashboards | Sweep telemetry → telemetry-dictionary.md → PM iterates themes → Grafonnet dashboards + blocking drift CI |

## Research Agents (dispatched by Gate 0)

| Agent | Specialization |
|-------|---------------|
| lzr1:repo-research-analyst | Codebase patterns, existing solutions |
| lzr1:best-practices-researcher | External best practices, industry standards |
| lzr1:framework-docs-researcher | Tech stack docs, version constraints |
| lzr1:product-designer | UX research, personas, competitive analysis |

## Entry Points

- **Small Track:** Invoke `lzr1:pre-dev-feature`
- **Large Track:** Invoke `lzr1:pre-dev-full`
- **Specific gate:** Invoke the gate's skill directly if prior gates are done
