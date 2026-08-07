---
name: postgres-15
description: Advanced PostgreSQL 15+ Operations and Tech Support Guide for managing massive datasets, high concurrency, and complex operational requirements.
---

# PostgreSQL 15+ Specialist

## Scope and Triggers

Use this skill when dealing with PostgreSQL 15+ in production environments, specifically for:
- Managing and optimizing massive datasets (terabytes/petabytes) using declarative partitioning and BRIN indexes.
- Diagnosing and resolving complex performance degradation, high CPU/Memory usage, and lock contention.
- Tuning autovacuum, `shared_buffers`, `work_mem`, and connection pooling (PgBouncer) for high-concurrency workloads.
- Executing zero-downtime database migrations and major version upgrades.
- Implementing robust disaster recovery strategies, including Point-in-Time Recovery (PITR) and handling worst-case scenarios like Transaction ID (TXID) wraparound or data corruption.
- Conducting comprehensive security audits, managing Role-Based Access Control (RBAC), Row-Level Security (RLS), and configuring `pgaudit`.

**Escalation Boundaries:**
- Route to `automation-and-scheduling` when the user needs to set up recurring maintenance tasks like `pg_partman` partition creation or `pg_repack` runs.
- Route to `security-review` when the user needs a comprehensive security audit of the application code interacting with the database, beyond just the database configuration.

## Preconditions

Before executing any operations, the following preconditions must be met:
1. **Version Validation:** PostgreSQL version must be 15 or higher.
2. **Extension Availability:** Required extensions (e.g., `pg_stat_statements`, `pgaudit`) must be installed.
3. **Permissions:** The executing user must have sufficient privileges for the intended operation (e.g., superuser for configuration changes, specific roles for data manipulation).

Run `scripts/check-pg-version.sh` to verify version and extension availability.

## Source Freshness

PostgreSQL configurations, default values, and command syntax can change between minor versions. Always consult the official documentation for the most current information.
- For volatile facts, refer to the mapped sources in `references/complete-reference.md`.
- Verify the installed version and current upstream documentation before applying destructive or production-impacting actions.

## Workflow

1. **Assess the Environment:** Run `scripts/check-pg-version.sh` to confirm PostgreSQL 15+ and required extensions.
2. **Identify the Requirement:** Determine the specific operational requirement (e.g., performance tuning, high availability, disaster recovery, security audit).
3. **Consult References:** Review `references/complete-reference.md` for relevant configuration parameters, commands, and PostgreSQL 15 specific features (e.g., `MERGE`, `jsonlog`, WAL compression).
4. **Diagnostic Analysis:** For performance issues, run `scripts/analyze-bloat.sql` and analyze `pg_stat_statements` to identify bottlenecks.
5. **Formulate Remediation Plan:** Develop a plan, ensuring read-only discovery precedes any mutation.
6. **Request Confirmation:** Require user confirmation for any destructive (e.g., `DROP TABLE`, `TRUNCATE`) or production-impacting actions (e.g., `REINDEX`, `VACUUM FULL`).
7. **Execute Plan:** Execute the remediation plan, monitoring system resources and replication lag during execution.
8. **Validate Outcome:** Use postcondition checks (e.g., verifying index usage, checking replication status) to confirm success.
9. **Output Report:** Generate a structured report detailing findings, actions taken, and actionable next steps.

## Safety

- **Read-Only First:** Always perform read-only discovery (e.g., `EXPLAIN`, `SELECT`) before executing mutations.
- **Confirmation Required:** Explicit user confirmation is mandatory for destructive commands (`DROP`, `TRUNCATE`) and production-impacting operations (`REINDEX`, `VACUUM FULL`).
- **Version Specifics:** Verify PostgreSQL version is 15+ before applying version-specific features.
- **Dry-Run:** Use dry-run mode for data migration scripts where possible.
- **Backups:** Ensure PITR backups are available before major schema changes.
- **Configuration Validation:** Validate `pg_hba.conf` syntax before reloading the server configuration.

## Validation

- **Syntax Checks:** Run `bash -n` on shell scripts and ensure SQL scripts parse correctly.
- **Dry Runs:** Execute scripts in dry-run mode when available to preview changes.
- **Postconditions:** Verify the expected outcome (e.g., reduced bloat, improved query execution time, successful replication).

## Failure Handling

- **Diagnosis:** If an operation fails, review PostgreSQL logs and system metrics to identify the root cause.
- **Alternatives:** If a specific approach fails (e.g., `REINDEX CONCURRENTLY` times out), consider alternatives (e.g., creating a new index and dropping the old one).
- **Rollback:** Have a rollback plan ready for any mutation. Do not repeat a failed action unchanged.

## Output Contract

The final output must be a structured report containing:
- **Findings:** Clear description of the identified issues or current state.
- **Actions Taken:** Detailed list of executed commands and configuration changes.
- **Evidence:** Output from diagnostic queries (e.g., `EXPLAIN ANALYZE`, `pg_stat_statements`) supporting the findings and actions.
- **Severity/Confidence:** Assessment of the issue's severity and confidence in the applied solution.
- **Actionable Next Steps:** Recommendations for ongoing maintenance or further optimization.

## Resources

- `references/complete-reference.md`: Comprehensive guide to PostgreSQL 15+ architecture, tuning, and features.
- `scripts/check-pg-version.sh`: Script to verify PostgreSQL version and required extensions.
- `scripts/analyze-bloat.sql`: Deterministic SQL script to identify bloated tables and indexes.

## Orchestration

This skill supports parallel execution for independent dimensions:
- **Inputs:** List of independent targets (e.g., multiple databases, distinct query sets).
- **Schemas:** Standardized output format for each parallel task.
- **Conflict Handling:** Synthesize results to identify and resolve conflicting recommendations (e.g., overlapping index creation).
- **Synthesis:** Aggregate findings into a unified report, prioritizing critical issues.
- **Termination:** Stop parallel execution when all targets have been processed or a critical failure occurs.
