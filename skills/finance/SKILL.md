---
name: finance
description: Comprehensive finance skill covering financial planning and analysis (FP&A), accounting, treasury, financial modeling, SaaS metrics, fundraising, and corporate finance. Use when building financial models, analyzing metrics, planning budgets, preparing investor materials, managing cash flow, or making financial decisions.
---

# Finance

Expert-level finance covering FP&A, accounting, financial modeling, SaaS metrics, fundraising, treasury, and corporate finance for technology companies.

## Scope and Triggers

**Scope:** This skill handles financial planning and analysis (FP&A), accounting (including ASC 606 and Section 174), financial modeling, SaaS metrics, fundraising, treasury, and corporate finance.
**Triggers:** Use this skill when the user requests building financial models, analyzing SaaS/business metrics, planning budgets, preparing investor materials, managing cash flow, revenue recognition, fundraising strategy, or financial reporting.
**Non-goals/Escalation:** Do not use this skill for executing trades, transferring funds, filing taxes, or providing legal/tax advice. Route to `excel-generator` for downloadable Excel files. Route to `business-strategy` for pure market positioning without financial modeling.

## Preconditions

1. **Detect Domain:** Scan the task for signals indicating Accounting, Financial Modeling, Fundraising, or SaaS Metrics.
2. **Identify Context:** Determine the stage, business model, and specific financial question.
3. **Verify Inputs:** Ensure necessary financial statements, metrics, or benchmarks are provided or can be reasonably assumed.

## Source Freshness

- **Tax Law:** Verify the current status of tax laws (e.g., Section 174/OB3) if the task requires real-time accuracy beyond the 2026 baseline.
- **Benchmarks:** Verify current SaaS growth benchmarks if the task requires real-time accuracy beyond the 2024/2025 data (e.g., ~30% median growth).
- **Accounting Standards:** Verify current ASC 606 guidance for revenue recognition.

## Workflow

1. **Understand the context:** Determine the stage, business model, and specific financial question.
2. **Domain Detection:** Scan the task for signals indicating Accounting, Financial Modeling, Fundraising, or SaaS Metrics.
3. **Spawning Logic:**
   - If a single domain is detected, use the corresponding reference.
   - If multiple domains are detected, launch all relevant specialists simultaneously (max 4).
4. **Gather Data:** Collect financial statements, metrics, and benchmarks.
5. **Analyze:** Build models, identify trends, and compare to benchmarks using the updated 2026 tax rules and current SaaS metrics.
6. **Cross-Domain Synthesis:** If multiple specialists were used, run a Financial Consistency Checker to identify contradictions, gaps, and dependencies, producing a unified recommendation.
7. **Recommend & Present:** Deliver data-driven recommendations with scenarios and clear communication of financial insights. Stop when the final analysis or model is presented to the user.

## Safety

- **Read-only Discovery:** Separate read-only discovery (e.g., analyzing financial statements) from mutations (e.g., generating final board materials).
- **Confirmation Required:** Require explicit confirmation before generating final board or investor materials, or providing any financial/tax analysis that could be construed as advice.
- **Disclaimer:** Provide a one-time disclaimer that the analysis is for informational purposes and does not constitute professional financial or tax advice.

## Validation

- **Model Checks:** Verify that any financial models generated correctly apply the new 2026 Section 174 rules for domestic vs. foreign R&D.
- **Revenue Recognition:** Ensure SaaS revenue recognition models correctly handle contract modifications (upgrades/downgrades) under ASC 606.
- **Benchmarks:** Validate that SaaS growth benchmarks used in analyses reflect the current ~30% median rather than outdated higher figures.

## Failure Handling

- **Missing Data:** If required financial data is missing, state assumptions clearly and ask the user for confirmation.
- **Contradictions:** If cross-domain synthesis identifies contradictions, explicitly annotate trade-offs and ask the user for clarification.
- **Errors:** If a model fails to balance (e.g., balance sheet), diagnose the error, adjust assumptions, and recalculate. Do not present an unbalanced model.

## Output Contract

- **Structure:** Provide a clear, structured analysis with assumptions, methodology, and results.
- **Evidence:** Cite specific benchmarks, tax rules, or accounting standards used.
- **Confidence:** State the confidence level of the analysis based on the quality of the inputs.
- **Next Steps:** Provide actionable recommendations based on the analysis.

## Resources

- [Accounting & Treasury](references/accounting.md): Use for revenue recognition (ASC 606), financial reporting, treasury management, tax considerations (Section 174), and audit/compliance.
- [Financial Modeling](references/financial-modeling.md): Use for model architecture, revenue modeling, expense modeling, three-statement models, and scenario analysis.
- [Fundraising & Valuation](references/fundraising.md): Use for fundraising process, valuation methods, investor materials, term sheets, and cap table management.
- [SaaS Metrics](references/saas-metrics.md): Use for core SaaS metrics, unit economics, growth metrics, efficiency metrics, and benchmarks by stage.
- [Reading List](references/reading-list.md): Use for curated books and articles on finance topics.

## Orchestration (Multi-Specialist Protocol)

When multiple domains are detected, spawn all relevant specialists simultaneously — do not serialize them.

### Domain Detection Table

| Task Signal (examples) | Domain | Specialist Agent | Reference |
|---|---|---|---|
| `accounting`, ... | **Accounting** | Accounting Specialist | `references/accounting.md` |
| `model`, ... | **Financial Modeling** | Modeling Specialist | `references/financial-modeling.md` |
| `fundraising`, ... | **Fundraising** | Fundraising Specialist | `references/fundraising.md` |
| `SaaS`, ... | **SaaS Metrics** | Metrics Specialist | `references/saas-metrics.md` |

### Spawning Logic

- **Single domain detected:** Fall back to original single-reference behavior.
- **Multiple domains detected:** Launch all relevant specialists simultaneously. Each specialist receives full task context + its dedicated reference file only. No specialist waits for another. Maximum concurrent specialists: 4.

### Cross-Domain Synthesizer

After all specialists complete, run one **Financial Consistency Checker** with all specialist outputs that:
1. **Identifies contradictions** between specialist recommendations for the same component.
2. **Identifies gaps** — requirements addressed by no specialist.
3. **Identifies dependencies** — where Domain A's output is a prerequisite for Domain B's recommendation.
4. **Produces** a unified recommendation with explicit trade-off annotations for any resolved contradictions.

## Authoritative sources

- [Authoritative source map](references/source-map.md) — consult this before relying on volatile upstream behavior.

## Package resource index

| Resource | Purpose |
|---|---|
| [references/source-map.md](references/source-map.md) | Supporting package resource; inspect before use and apply the workflow’s safety and validation gates. |
