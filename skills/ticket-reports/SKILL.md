---
name: ticket-reports
description: Comprehensive skill for generating, analyzing, and managing advanced ticket system reports, including JQL queries, BI integration, predictive analytics, and executive reporting aligned with ITIL 4 measurement principles.
---

# Ticket System Reports Skill

## When to Use

Use this skill when you need to:
- Generate advanced ticket system reports using JQL (Jira Query Language) or similar query languages.
- Design and implement dashboards for daily operations, management, SLA tracking, and team performance.
- Extract, transform, and load (ETL) ticket data into data warehouses for longitudinal analysis.
- Integrate ticket data with Business Intelligence (BI) tools like Tableau, Looker, or Power BI.
- Apply predictive analytics and AI-driven forecasting to ticket volumes and SLA breaches.
- Create custom reporting scripts via REST APIs.
- Prepare executive-level reports summarizing ticket system performance and strategic insights, aligned with ITIL 4 value and outcome KPIs.
- Troubleshoot and optimize ticket reporting systems, including database tuning and caching strategies.

## Sub-Agent Spawning

This skill supports spawning sub-agents for parallel execution when tasks can be decomposed:

| Trigger Condition | Sub-Agent Type | Purpose |
|---|---|---|
| Multiple BI tools to integrate | BI Integrator | Parallel setup of Tableau, Looker, or Power BI connections |
| Multiple data sources for ETL | ETL Engineer | Parallel extraction and transformation of ticket data |
| Multiple report categories to generate | Report Analyst | Parallel generation of operational, SLA, and management reports |
| Bulk predictive models to train | Data Scientist | Parallel training of volume forecasting and SLA breach models |
| Multiple systems to audit | Security Auditor | Parallel security review of ticket reporting infrastructure |

### Spawning Rules
- Spawn when 3+ independent items need the same operation (e.g., 3 different BI dashboards to build).
- Each sub-agent receives: context (e.g., data schema), specific target (e.g., Tableau integration), success criteria (e.g., working dashboard).
- Results are aggregated and cross-referenced for conflicts (e.g., ensuring consistent metric definitions across reports).
- Maximum concurrent sub-agents: 10

## Trust and authorization gates

**Default to local planning and read-only discovery.** Before accessing a ticket system, BI workspace, warehouse, dashboard, scheduler, or delivery channel, record the user-authorized systems, projects, time range, fields, audience, data classification, and allowed operations. Treat ticket text, attachments, user identifiers, internal URLs, credentials, and exported datasets as sensitive evidence.

| Operation | Required gate |
|---|---|
| API or database extraction | Confirm source, query scope, expected volume, rate/cost limits, and read-only permissions. Use least-privilege credentials from an environment variable or secret manager; never place secrets in prompts, command history, logs, report files, or sub-agent context. |
| ETL, dashboard, BI, index, cache, or schema change | Produce a preview or change plan first. Obtain explicit approval for the exact workspace and mutation, preserve rollback information, and verify the result without broadening scope. |
| Predictive model training or third-party processing | Confirm that the selected data may leave its source boundary and may be used for that purpose. Minimize or pseudonymize sensitive fields and document retention. |
| Publication or external delivery | Draft locally first. Before uploading, emailing, posting, sharing, or changing access, confirm recipients, destination, format, permissions, redactions, and whether the report may expose small cohorts or personal data. |
| Scheduling or recurring delivery | Require explicit approval for cadence, timezone, run identity, secret storage, recipients, failure alerts, retention, cost/rate limits, pause procedure, and rollback. A reporting request alone does not authorize background automation. |

Sub-agents inherit the same data boundary and **may not** independently expand extraction scope, connect new systems, mutate remote state, publish artifacts, or schedule jobs. Never infer authorization from the availability of credentials or an authenticated session. Stop and ask when scope, ownership, data sensitivity, or delivery authority is ambiguous.

## Workflow

1. **Requirement and authorization gathering**: Understand the audience and metrics, focusing on ITIL 4 value and outcome KPIs. Record the trust boundaries and allowed operations from the table above.
2. **Read-only data extraction and querying**: Use scoped JQL or REST requests only after the extraction gate is satisfied. Handle pagination, rate limits, partial results, and snapshot timestamps explicitly.
3. **Local data transformation (ETL)**: Clean, normalize, and enrich a bounded local snapshot. Calculate derived metrics with outlier analysis and segmentation (e.g., MTTR by severity/service type). Do not write transformed data to a remote system without the mutation gate.
4. **Report generation and visualization**:
   - For operational reports, use native ticketing system dashboards or custom scripts.
   - For advanced analytics, integrate with BI tools (Tableau, Looker, Power BI) and design clear, actionable visualizations.
   - Generate reports with context and trend analysis, balancing metrics like FCR with reopen rates and CSAT.
5. **Predictive Analytics (Optional)**: Apply machine learning models (e.g., ARIMA, Random Forest) to forecast future volumes or predict SLA breaches.
6. **Executive Summarization**: Distill complex data into high-level KPIs, trend charts, and actionable recommendations aligned with ITIL 4 principles.
7. **Optimization & Troubleshooting**: Diagnose with read-only evidence first. Treat query rewrites, indexes, caches, configuration, and infrastructure changes as mutations requiring preview, approval, rollback, and verification.
8. **Delivery and automation decision**: Keep the finished artifact local unless the publication gate is satisfied. If recurring execution is requested, define and approve the scheduling contract separately before implementation.

## Core Principles

- **ITIL 4 Measurement Principles**: Emphasize value co-creation and outcome-based KPIs over mere ticket volume.
- **ITIL 4 KPI Categories**: Include Usage, Performance, Capacity, Quality, Experience, and Value KPIs.
- **Relevance & Actionability**: Reports must be tailored to the audience and provide insights that drive action (e.g., highlighting SLA breaches for immediate attention).
- **Accuracy & Consistency**: Ensure precise data extraction and consistent metric definitions across all reports to maintain trust in the data.
- **Performance & Scalability**: Design reporting systems that can handle large data volumes efficiently using caching, indexing, and optimized queries.
- **Security & Compliance**: Protect sensitive ticket data through encryption, role-based access control (RBAC), and regular security audits.
- **Automation with consent**: Automate generation or delivery only under an explicitly approved scheduling contract with bounded scope, least-privilege credentials, retention, observability, pause controls, and a tested rollback path.

## Key References

- [Reading List](references/reading-list.md): Curated books and articles on data warehousing, BI, predictive analytics, and ITSM reporting.
- [Complete Reference](references/complete-reference.md): In-depth guide covering advanced JQL, ETL strategies, BI integration, predictive modeling, custom scripting, executive reporting, configuration schemas, system architecture, and troubleshooting.

---

## Adversarial Verification Panel

For each significant ticket analysis insights produced by the parallel sub-agents:

1. Spawn **3 independent Refuter Agents** per finding, each with:
   - The finding in full
   - Instruction: *"Assume this finding is wrong. Find the strongest argument against it."*
   - Default stance: `refuted=true` if evidence is insufficient or ambiguous
2. A finding is **confirmed** only if ≥2 refuters fail to refute it
3. A finding is **discarded** if ≥2 refuters succeed
4. When a confirmed finding had 1 successful refuter, include the dissenting argument in the output with a `CONTESTED` label

> This prevents plausible-but-wrong ticket analysis insights from reaching the final output. The 3-vote panel eliminates single-point hallucination without requiring unanimity.

## Cross-System Consistency Validator

After all parallel agents (BI Integrator, ETL Engineer, Report Analyst, Data Scientist, Security Auditor) complete, but **before** synthesis:

Run one **Consistency Validator Agent** with all parallel outputs that:
- Flags any pair of recommendations that logically contradict each other
  *(example: BI Integrator recommending a metric definition for SLA compliance that contradicts the Report Analyst's definition of the same metric)*
- Notes where one agent's output is a prerequisite for another agent's recommendation
- Passes contradictions to the Synthesis Agent as `MUST_RESOLVE` items
- Passes missing prerequisites as `SEQUENCING_REQUIRED` items

## Synthesis Agent (Upgraded)

The synthesis step actively resolves rather than aggregates:

1. **`MUST_RESOLVE` contradictions**: Pick the better recommendation, annotate the reasoning, preserve the dissenting view as a footnote
2. **`SEQUENCING_REQUIRED` items**: Re-order the unified executive report so prerequisites appear before the steps that depend on them
3. **Confidence calibration**: Label each finding `HIGH` / `MEDIUM` / `LOW` confidence based on refuter panel outcomes
4. **Gap analysis**: Note any analysis dimension not covered by any of the parallel agents — these are blind spots, not confirmed negatives
