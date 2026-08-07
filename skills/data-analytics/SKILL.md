---
name: data-analytics
description: Comprehensive data and analytics skill covering data engineering, data analysis, business intelligence, data visualization, data science, and analytics engineering. Use when building data pipelines, performing data analysis, creating dashboards, designing data warehouses, writing SQL queries, or implementing analytics solutions.
---

# Data & Analytics

Expert-level data engineering, analytics, and business intelligence covering the full data lifecycle: ingestion, transformation, storage, analysis, visualization, and governance.

## When to Use

- Building or optimizing data pipelines (ETL/ELT)
- Data analysis and statistical exploration
- Business intelligence and dashboard creation
- Data warehouse and lakehouse design
- SQL query writing and optimization
- Data modeling and schema design
- Analytics engineering (dbt, metrics layers)
- Data governance and quality

## Workflow

1. **Understand the question** — What business question needs answering?
2. **Detect the target domain(s)** — Based on task signals (e.g., pipeline, analysis, visualization, dbt, governance).
3. **Select reference / Spawn specialists** —
   - If a single domain is detected, fall back to the single-reference behavior.
   - If multiple domains are detected, launch all relevant specialists simultaneously, providing each with the full task context and its dedicated reference file.
4. **Explore the data** — Understand structure, quality, and relationships
5. **Transform and model** — Clean, transform, and model for the use case
6. **Analyze and visualize** — Extract insights and present clearly
7. **Synthesize** — Run the Analytics Synthesizer with all specialist outputs to identify contradictions, gaps, and dependencies.
8. **Document and validate** — Ensure reproducibility and accuracy. Produce a unified recommendation with explicit trade-off annotations for any resolved contradictions.
9. **Stop** — Stop when the unified recommendation is complete and actionable.

## Core Principles (All Data Work)

- Data quality is non-negotiable: validate inputs, test transformations, monitor outputs
- Reproducibility: every analysis must be reproducible from source data
- Version control: SQL, dbt models, pipeline code, and documentation in git
- Idempotency: pipelines must produce the same result when re-run
- Lineage: track data from source to consumption for trust and debugging
- Minimize data movement: process data where it lives when possible
- Right tool for the job: SQL for set operations, Python for complex logic
- Document assumptions: every metric definition, filter, and business rule

## Role Capabilities

| Role | Expertise | Reference |
|---|---|---|
| Data Engineer | Pipelines, infrastructure, orchestration | `references/data-engineering.md` |
| Data Analyst | Analysis, SQL, business insights | `references/data-analysis.md` |
| Analytics Engineer | dbt, metrics, semantic layer | `references/data-modeling.md` |
| BI Engineer | Dashboards, reporting, self-service | `references/visualization.md` |
| Data Scientist | Statistics, modeling, experimentation | `references/data-analysis.md` |

## Key References

- **Data engineering**: See `references/data-engineering.md` for pipelines, orchestration, and infrastructure.
- **Data analysis**: See `references/data-analysis.md` for SQL, statistics, and exploration.
- **Visualization**: See `references/visualization.md` for dashboards and visual communication.
- **Data modeling**: See `references/data-modeling.md` for warehouse design and dbt.
- **Data governance**: See `references/data-governance.md` for quality, lineage, and cataloging.
- **Recommended reading**: See `references/reading-list.md` for curated books and articles.

---

## Multi-Specialist Protocol

> **Replaces the single "Select reference" step.** When multiple domains are detected, spawn all relevant specialists simultaneously — do not serialize them. This explicitly accounts for AI-ready data systems and streaming architectures.

### Domain Detection Table

Scan the task for signals that indicate which domains apply:

| Task Signal (examples) | Domain | Specialist Agent | Reference |
|---|---|---|---|
| `pipeline`, `streaming`, `lakehouse` | **Data Engineering** | Pipeline Specialist | `references/data-engineering.md` |
| `analysis`, `statistics` | **Data Analysis** | Analysis Specialist | `references/data-analysis.md` |
| `visualization`, `dashboard` | **Visualization** | Viz Specialist | `references/visualization.md` |
| `dbt`, `metricflow`, `semantic layer` | **Data Modeling** | Modeling Specialist | `references/data-modeling.md` |
| `governance`, `ai compliance` | **Data Governance** | Governance Specialist | `references/data-governance.md` |

### Spawning Logic

**Single domain detected** → Fall back to original single-reference behavior (no change).

**Multiple domains detected** → Launch all relevant specialists simultaneously:
- Each specialist receives: **full task context** + its dedicated reference file only
- No specialist waits for another — all start at the same time
- Maximum concurrent specialists: 5

### Cross-Domain Synthesizer

After all specialists complete, run one **Analytics Synthesizer** with all specialist outputs that:

1. **Identifies contradictions** between specialist recommendations for the same component
2. **Identifies gaps** — requirements addressed by no specialist
3. **Identifies dependencies** — where Domain A's output is a prerequisite for Domain B's recommendation
4. **Produces** a unified recommendation with explicit trade-off annotations for any resolved contradictions

> Synthesis focus for this skill: Ensures modeling assumptions are consistent with governance policies. Maps pipeline design decisions to their downstream impact on analysis accuracy.

## Safety and Validation

- **Safety**: Separate read-only discovery from mutations. Require confirmation for destructive, external, privileged, financial, legal, or production-impacting actions.
- **Validation**: Verify that the Multi-Specialist Protocol correctly spawns specialists for AI compliance when governance is detected; ensure dbt Semantic Layer examples use valid 2026 MetricFlow syntax; validate that Medallion architecture concepts are clearly defined in data engineering references.
- **Failure Handling**: If an action fails, diagnose the error, choose alternatives, and do not repeat the failed action unchanged.

## Output Contract

The final output must include a unified recommendation with explicit trade-off annotations for any resolved contradictions, actionable next steps, and evidence of validation.
