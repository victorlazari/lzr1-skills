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

## Preconditions

- Detect the target product, stage, market, and constraints before acting.
- Identify the specific product management domain (Strategy, Discovery, Delivery, Growth).
- Ensure required inputs (e.g., user research, metrics, business goals) are available.

## Source Freshness

- Authoritative sources (SVPG, Reforge, Pragmatic Institute) are integrated into references.
- Volatile facts (e.g., specific tool integrations, current industry benchmarks) must be verified against upstream documentation if older than 6 months.
- Verified against upstream: 2026-08-07

## Workflow

1. **Analyze the user request** to determine the required product management domains (Strategy, Discovery, Delivery, Growth).
2. **If multiple domains are detected**, spawn parallel specialists using the Multi-Specialist Protocol defined below.
3. **For each domain**, consult the corresponding reference file to execute the specific framework or procedure:
   - Strategy and vision → `references/product-strategy.md`
   - Discovery and validation → `references/product-discovery.md`
   - Execution and delivery → `references/product-delivery.md`
   - Growth and metrics → `references/product-growth.md`
4. **If the task involves creating a PRD**, use `templates/prd-template.md` and validate the output using `scripts/validate-prd.py`.
5. **Synthesize the outputs** from all domains, resolving any contradictions and ensuring all dependencies are addressed.
6. **Present the final product decision**, roadmap, or document to the user, requesting confirmation for any high-impact actions.
7. **Stop** when the user approves the final output or when all actionable findings have been addressed.

## Safety and Validation

- **Safety:** Require explicit user confirmation before finalizing strategic decisions, pricing changes, or feature launches. Separate read-only discovery from mutations.
- **Validation:** Validate PRD structure using `scripts/validate-prd.py` before considering delivery planning complete. Ensure all metric definitions are cross-referenced with actual data sources before finalizing growth experiments.

## Failure Handling

- If PRD validation fails, review the missing sections and update the document using the template.
- If a strategic decision lacks sufficient evidence, pause and request further discovery or data analysis.
- Do not repeat failed actions unchanged; adjust the approach based on the error or missing information.

## Output Contract

- A structured product document (e.g., PRD, roadmap, strategy memo) following the provided templates.
- Explicit evidence supporting decisions (e.g., user research, metrics).
- Actionable next steps for the team (e.g., engineering, design, marketing).

## Resources

- **Product strategy**: `references/product-strategy.md`
- **Product discovery**: `references/product-discovery.md`
- **Product delivery**: `references/product-delivery.md`
- **Product growth**: `references/product-growth.md`
- **PRD Template**: `templates/prd-template.md`
- **PRD Validator**: `scripts/validate-prd.py`

## Cross-Skill Routing

- `software-engineering` — route when the task requires writing code, designing system architecture, or implementing technical solutions.
- `ui-ux-design` — route when the task requires creating visual designs, wireframes, or detailed user interface specifications.
- `data-analysis` — route when the task requires complex statistical analysis, writing SQL queries, or building data pipelines beyond basic product metrics.

---

## Multi-Specialist Protocol

When multiple domains are detected, spawn all relevant specialists simultaneously — do not serialize them.

### Domain Detection Table

Scan the task for signals that indicate which domains apply:

| Task Signal (examples) | Domain | Specialist Agent | Reference |
|---|---|---|---|
| `discovery`, `research`, `interviews` | **Product Discovery** | Discovery Specialist | `references/product-discovery.md` |
| `delivery`, `agile`, `sprint`, `prd` | **Product Delivery** | Delivery Specialist | `references/product-delivery.md` |
| `strategy`, `vision`, `roadmap` | **Product Strategy** | Strategy Specialist | `references/product-strategy.md` |
| `growth`, `metrics`, `retention` | **Product Growth** | Growth Specialist | `references/product-growth.md` |

### Spawning Logic

**Single domain detected** → Fall back to original single-reference behavior.

**Multiple domains detected** → Launch all relevant specialists simultaneously:
- Each specialist receives: **full task context** + its dedicated reference file only
- No specialist waits for another — all start at the same time
- Maximum concurrent specialists: 4

### Cross-Domain Synthesizer

After all specialists complete, run one **Product Decision Synthesizer** with all specialist outputs that:

1. **Identifies contradictions** between specialist recommendations for the same component.
2. **Identifies gaps** — requirements addressed by no specialist.
3. **Identifies dependencies** — where Domain A's output is a prerequisite for Domain B's recommendation.
4. **Produces** a unified recommendation with explicit trade-off annotations for any resolved contradictions.

> Synthesis focus for this skill: Ensures growth instrumentation is included in delivery planning. Flags where a strategy decision requires discovery validation before execution begins.

## Authoritative sources

- [Authoritative source map](references/source-map.md) — consult this before relying on volatile upstream behavior.

## Package resource index

| Resource | Purpose |
|---|---|
| [references/source-map.md](references/source-map.md) | Supporting package resource; inspect before use and apply the workflow’s safety and validation gates. |
