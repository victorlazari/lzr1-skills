---
name: jira-field-schemas
description: Expert-level skill for managing, auditing, and optimizing Jira Service Management Field Schemas, Field Contexts, and Screen Schemes.
---

# Jira Field Schemas

## When to Use

Use this skill when tasked with:
- Designing or optimizing enterprise-grade Jira field architectures.
- Managing advanced Field Contexts to control scope, defaults, and restrictions.
- Configuring the complex interplay between Fields, Screens, Screen Schemes, and Issue Type Screen Schemes.
- Preparing for the unified Field Schemes experience (slated for 2026).
- Automating field schema management via the Jira REST API or `jira-field-schemas` CLI.
- Performing security audits on Jira field configurations and permissions.
- Troubleshooting field visibility, indexing, or configuration conflicts.

## Sub-Agent Spawning

This skill supports spawning sub-agents for parallel execution when tasks can be decomposed:

| Trigger Condition | Sub-Agent Type | Purpose |
|---|---|---|
| Multiple projects to audit | Schema Auditor | Parallel review of field configurations across projects |
| Multiple custom fields to rationalize | Field Rationalizer | Parallel analysis of field usage and context overlap |
| Multiple screens to configure | Screen Configurator | Parallel setup of screens and screen schemes |
| Bulk API updates | API Automator | Parallel execution of field context updates via REST API |

### Spawning Rules
- Spawn when 3+ independent items (projects, fields, screens) need the same operation.
- Each sub-agent receives: context, specific target (e.g., project ID or field ID), success criteria.
- Results are aggregated and cross-referenced for conflicts (e.g., naming collisions, type mismatches).
- Maximum concurrent sub-agents: 10.

## Workflow

1. **Assessment & Discovery**:
   - Audit existing field configurations, contexts, and screen schemes.
   - Identify redundant fields, overlapping contexts, and performance bottlenecks.
   - Review current field limits (e.g., 700 fields per configuration, 150 issue types per scheme).

2. **Design & Rationalization**:
   - Consolidate similar fields using Field Contexts to vary options and defaults.
   - Standardize screens and screen schemes for common issue types.
   - Group issue types logically to reduce the number of field configuration schemes.

3. **Implementation & Automation**:
   - Use the `jira-field-schemas` CLI or REST API for bulk creation, updates, and assignments.
   - Configure field visibility, required status, and renderers.
   - Set up user picker restrictions and custom option sets per context.

4. **Validation & Security Audit**:
   - Verify field visibility across Create, Edit, and View screens.
   - Conduct a security audit to ensure proper access controls and compliance.
   - Perform reindexing to ensure changes are reflected in search results.

5. **Documentation & Maintenance**:
   - Maintain a field dictionary tracking field purposes, contexts, and associated projects.
   - Prepare migration paths for the 2026 unified Field Schemes update.

## Core Principles

- **Avoid Redundancy**: Reuse fields wherever possible rather than creating new similar fields.
- **Leverage Contexts**: Use Field Contexts to vary field options and defaults instead of creating separate fields per project.
- **Limit Visibility**: Do not add fields to screens unnecessarily; manage visibility strictly via screens.
- **Automate at Scale**: Utilize the CLI and REST API for managing schemas across hundreds of projects.
- **Future-Proofing**: Design schemas with the upcoming unified Field Schemes model in mind, minimizing fragmentation.

## Key References

- **Complete Reference**: `/home/ubuntu/specialist-skills/jira-field-schemas/references/complete-reference.md`
- **Reading List**: `/home/ubuntu/specialist-skills/jira-field-schemas/references/reading-list.md`

---

## Adversarial Verification Panel

For each significant field configuration issue (conflicts, redundancies, permission problems, schema anomalies) produced by the parallel sub-agents:

1. Spawn **3 independent Refuter Agents** per finding, each with:
   - The finding in full
   - Instruction: *"Assume this finding is wrong. Find the strongest argument against it."*
   - Default stance: `refuted=true` if evidence is insufficient or ambiguous
2. A finding is **confirmed** only if ≥2 refuters fail to refute it
3. A finding is **discarded** if ≥2 refuters succeed
4. When a confirmed finding had 1 successful refuter, include the dissenting argument in the output with a `CONTESTED` label

> This prevents plausible-but-wrong field configuration issues from reaching the final output. The 3-vote panel eliminates single-point hallucination without requiring unanimity.

## Cross-System Consistency Validator

After all parallel agents (Schema Auditor, Field Rationalizer, Screen Configurator, API Automator) complete, but **before** synthesis:

Run one **Consistency Validator Agent** with all parallel outputs that:
- Flags any pair of recommendations that logically contradict each other
  *(example: one agent recommending to consolidate two fields into one context while another agent recommends keeping them separate due to screen scheme dependencies)*
- Notes where one agent's output is a prerequisite for another agent's recommendation
- Passes contradictions to the Synthesis Agent as `MUST_RESOLVE` items
- Passes missing prerequisites as `SEQUENCING_REQUIRED` items

## Synthesis Agent (Upgraded)

The synthesis step actively resolves rather than aggregates:

1. **`MUST_RESOLVE` contradictions**: Pick the better recommendation, annotate the reasoning, preserve the dissenting view as a footnote
2. **`SEQUENCING_REQUIRED` items**: Re-order the unified field schema optimization report so prerequisites appear before the steps that depend on them
3. **Confidence calibration**: Label each finding `HIGH` / `MEDIUM` / `LOW` confidence based on refuter panel outcomes
4. **Gap analysis**: Note any analysis dimension not covered by any of the parallel agents — these are blind spots, not confirmed negatives
