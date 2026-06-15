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
