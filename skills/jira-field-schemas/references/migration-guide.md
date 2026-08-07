# Jira Field Schemas: Migration Guide

**Verified against upstream:** 2026-08-07

## 1. Introduction

This guide outlines the process for migrating from legacy Field Configurations and Field Configuration Schemes to the 2026 unified Field Schemes model. The migration process is largely automated by Atlassian, but requires careful pre-migration auditing and post-migration validation to ensure compliance with new system limits.

## 2. The Automated Migration Process

Atlassian provides an automated migration path that converts existing Field Configurations and Field Configuration Schemes into the new unified Field Schemes.

### 2.1. What to Expect

- **Increased Scheme Count:** The automated migration may result in an increased number of Field Schemes as it attempts to map complex legacy configurations into the new unified model.
- **Context Changes:** Field Contexts that previously restricted visibility will be converted. The visibility rules will be absorbed into the new Field Schemes, and the contexts will revert to only managing default values and options.
- **Global Contexts:** Every field will be assigned a global context if it does not already have one.

## 3. Pre-Migration Auditing

Before the automated migration occurs, it is critical to audit the existing Jira instance to prevent issues and ensure a smooth transition.

### 3.1. Limit Verification

The new model enforces strict limits:
- **700 fields per space (project)**
- **150 work types (issue types) per scheme**

Use the `audit-fields.py` script to identify any spaces or schemes that currently exceed or are close to these limits.

### 3.2. Field Rationalization

- **Identify Unused Fields:** Find custom fields that are rarely or never used and delete them (requires user confirmation).
- **Consolidate Redundant Fields:** Merge similar fields to reduce the overall field count per space.
- **Review Contexts:** Ensure that Field Contexts are not being used as a primary method for hiding fields, as this behavior will change.

## 4. Post-Migration Validation

After the migration is complete, perform the following checks:

1. **Run the Audit Script:** Execute `audit-fields.py` again to confirm that all spaces and schemes are within the new limits.
2. **Verify Visibility:** Spot-check key work types to ensure that fields are visible (or hidden) as expected under the new Field Schemes.
3. **Check API Integrations:** Ensure that any custom scripts or integrations have been updated to use the new Field Scheme Model APIs (RFC 103, 104, 105, 121) instead of the deprecated legacy endpoints.
