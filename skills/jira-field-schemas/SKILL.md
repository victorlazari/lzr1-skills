---
name: jira-field-schemas
description: Manage, audit, and optimize Jira unified Field Schemes, Field Contexts, and Screen Schemes, ensuring compliance with 2026 limits (700 fields/space, 150 work types/scheme).
---

# Jira Field Schemas

## Scope and Triggers

**Use this skill when tasked with:**
- Designing or optimizing enterprise-grade Jira field architectures under the 2026 unified Field Schemes model.
- Managing Field Contexts to control default values and options (note: contexts no longer control visibility).
- Configuring the interplay between Fields, Screens, Screen Schemes, and Issue Type Screen Schemes.
- Auditing Jira instances for compliance with the 700 fields per space and 150 work types per scheme limits.
- Automating field schema management via the Jira REST API (Field Scheme Model APIs).

**Do NOT use this skill for:**
- Querying issues based on field values (use `jira-jql-search`).
- Automating issue transitions or updates based on field changes (use `jira-automation`).

## Preconditions

Before modifying any field schemas, the agent must:
1. Verify the Jira instance's migration status to the unified Field Schemes model.
2. Confirm the user has Jira Administrator permissions.
3. Identify the target spaces (projects) and work types (issue types).
4. Run the `audit-fields.py` script in read-only mode to assess current limits and fragmentation.

## Source Freshness

The Jira field architecture underwent a fundamental change in 2026, retiring Field Configurations and Field Configuration Schemes in favor of unified Field Schemes. Field Contexts no longer control visibility.
- **Verified against upstream:** 2026-08-07
- **Canonical Sources:**
  - [Say goodbye to field configuration schemes and hello to the future of Jira](https://community.atlassian.com/forums/Jira-Cloud-Admins-articles/Say-goodbye-to-field-configuration-schemes-and-hello-to-the/ba-p/3160315)
  - [Announcing General Availability of Field Schemes](https://community.atlassian.com/forums/Jira-Cloud-Admins-articles/Announcing-General-Availability-of-Field-Schemes/ba-p/3246894)

## Workflow

1. **Assess Current State (Read-Only)**:
   - Run `scripts/audit-fields.py` to map existing fields, contexts, and schemes.
   - Flag any violations of the new limits (700 fields/space, 150 work types/scheme).
2. **Rationalize Fields**:
   - Identify redundant fields and consolidate them.
   - Ensure Field Contexts are only used for default values and options, not visibility.
3. **Plan Migration/Updates**:
   - Use `references/migration-guide.md` to map legacy configurations to the new unified Field Schemes.
4. **Execute Updates (Requires Confirmation)**:
   - Use the new Field Scheme Model APIs to create or update Field Schemes.
   - **STOP:** Explicit user confirmation is required before any destructive changes (e.g., deleting fields or schemes).
5. **Validate**:
   - Re-run `scripts/audit-fields.py` to confirm the new schemas are within limits and correctly applied.
   - Stop when all spaces and schemes are compliant.

## Safety

- **Read-only discovery must precede any schema mutations.**
- **Destructive actions** (deleting fields, schemes, or contexts) require explicit user confirmation.
- The `audit-fields.py` script must run in a read-only mode by default.
- API automation must validate against the 700 fields/space and 150 work types/scheme limits before attempting creation.

## Validation

- Run `scripts/audit-fields.py` to verify that no space exceeds 700 fields and no scheme exceeds 150 work types.
- Verify that API responses indicate successful application of the new Field Scheme Model APIs.

## Failure Handling

- If the audit script fails to connect, verify API credentials and network access.
- If a space exceeds the 700-field limit, halt creation and prompt the user to consolidate or delete unused fields.
- If the Jira instance is still on the legacy model, warn the user and refer to the migration guide. Do not attempt to use the new APIs on a legacy instance.

## Output Contract

The final output must include:
- A summary of the actions taken (e.g., "Audited 5 spaces, consolidated 12 fields").
- The output of the `audit-fields.py` script, highlighting any remaining limit violations.
- A list of any destructive actions performed (with confirmation noted).
- Actionable next steps for any unresolved issues.

## Resources

- **[Complete Reference](references/complete-reference.md)**: Detailed architecture of the 2026 unified Field Schemes and REST API details.
- **[Migration Guide](references/migration-guide.md)**: Guide on the automated migration process, limits, and pre-migration auditing.
- **[Audit Script](scripts/audit-fields.py)**: Deterministic script to identify unused fields, scheme fragmentation, and limit violations.

## Orchestration

This skill supports parallel execution for auditing multiple spaces or rationalizing multiple fields.
- **Inputs**: List of space IDs or field IDs.
- **Concurrency**: Maximum 10 concurrent sub-agents.
- **Synthesis**: Aggregate audit results and cross-reference for conflicts (e.g., naming collisions). Stop when all targets are processed.
