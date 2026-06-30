---
name: ticket-reports
description: Comprehensive skill for generating, analyzing, and managing advanced ticket system reports, including JQL queries, BI integration, predictive analytics, and executive reporting.
---

# Ticket System Reports Skill

## When to Use

Use this skill when you need to:
- Generate advanced ticket system reports using JQL (Jira Query Language) or similar query languages.
- Design and implement dashboards for daily operations, management, SLA tracking, and team performance.
- Extract, transform, and load (ETL) ticket data into data warehouses for longitudinal analysis.
- Integrate ticket data with Business Intelligence (BI) tools like Tableau, Looker, or Power BI.
- Apply predictive analytics and AI-driven forecasting to ticket volumes and SLA breaches.
- Create custom reporting scripts via REST APIs for automated and tailored reporting.
- Prepare executive-level reports summarizing ticket system performance and strategic insights.
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

## Workflow

1. **Requirement Gathering**: Understand the audience (e.g., operational team, executives) and the specific metrics needed (e.g., SLA compliance, MTTR, ticket volume trends).
2. **Data Extraction & Querying**: Use advanced JQL or REST APIs to extract the necessary ticket data. Handle pagination and rate limits appropriately.
3. **Data Transformation (ETL)**: Clean, normalize, and enrich the data. Calculate derived metrics like resolution time or SLA breach status.
4. **Report Generation & Visualization**: 
   - For operational reports, use native ticketing system dashboards or custom scripts.
   - For advanced analytics, integrate with BI tools (Tableau, Looker, Power BI) and design clear, actionable visualizations.
5. **Predictive Analytics (Optional)**: Apply machine learning models (e.g., ARIMA, Random Forest) to forecast future volumes or predict SLA breaches.
6. **Executive Summarization**: Distill complex data into high-level KPIs, trend charts, and actionable recommendations for leadership.
7. **Optimization & Troubleshooting**: Ensure the reporting system is performant by optimizing database queries, implementing caching, and handling edge cases like concurrency and data consistency.

## Core Principles

- **Relevance & Actionability**: Reports must be tailored to the audience and provide insights that drive action (e.g., highlighting SLA breaches for immediate attention).
- **Accuracy & Consistency**: Ensure precise data extraction and consistent metric definitions across all reports to maintain trust in the data.
- **Performance & Scalability**: Design reporting systems that can handle large data volumes efficiently using caching, indexing, and optimized queries.
- **Security & Compliance**: Protect sensitive ticket data through encryption, role-based access control (RBAC), and regular security audits.
- **Automation**: Leverage scripts and scheduled tasks to automate report generation and delivery, reducing manual effort.

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
