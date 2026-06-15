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
2. **Select reference** — Choose the appropriate domain:
   - Data pipelines and infrastructure → `references/data-engineering.md`
   - Analysis and statistics → `references/data-analysis.md`
   - Visualization and dashboards → `references/visualization.md`
   - Data modeling and warehousing → `references/data-modeling.md`
   - Data governance and quality → `references/data-governance.md`
3. **Explore the data** — Understand structure, quality, and relationships
4. **Transform and model** — Clean, transform, and model for the use case
5. **Analyze and visualize** — Extract insights and present clearly
6. **Document and validate** — Ensure reproducibility and accuracy

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
