---
name: postgres-15
description: Advanced PostgreSQL 15+ Operations and Tech Support Guide for managing massive datasets, high concurrency, and complex operational requirements.
---

# PostgreSQL 15+ Specialist

## When to Use

Use this skill when dealing with PostgreSQL 15+ in production environments, specifically for:
- Managing and optimizing massive datasets (terabytes/petabytes) using declarative partitioning and BRIN indexes.
- Diagnosing and resolving complex performance degradation, high CPU/Memory usage, and lock contention.
- Tuning autovacuum, `shared_buffers`, `work_mem`, and connection pooling (PgBouncer) for high-concurrency workloads.
- Executing zero-downtime database migrations and major version upgrades.
- Implementing robust disaster recovery strategies, including Point-in-Time Recovery (PITR) and handling worst-case scenarios like Transaction ID (TXID) wraparound or data corruption.
- Conducting comprehensive security audits, managing Role-Based Access Control (RBAC), Row-Level Security (RLS), and configuring `pgaudit`.

## Sub-Agent Spawning

This skill supports spawning sub-agents for parallel execution when tasks can be decomposed:

| Trigger Condition | Sub-Agent Type | Purpose |
|---|---|---|
| Multiple massive tables to partition | Partitioning Specialist | Parallel implementation of declarative partitioning |
| Multiple databases to audit | Security Auditor | Parallel security review of RBAC, RLS, and `pg_hba.conf` |
| Multiple slow queries to optimize | Query Optimizer | Parallel analysis of `EXPLAIN ANALYZE` and index tuning |
| Multiple replicas to monitor | Replication Monitor | Parallel health checks of streaming and logical replication |
| Bulk data loading across tables | Data Migration Agent | Parallel execution of `COPY` and index recreation |

### Spawning Rules
- Spawn when 3+ independent items (tables, databases, queries) need the same operation.
- Each sub-agent receives: context, specific target (e.g., table name, query), success criteria.
- Results are aggregated and cross-referenced for conflicts (e.g., overlapping index creation).
- Maximum concurrent sub-agents: 10.

## Workflow

1. **Initial Assessment & Monitoring:**
   - Review PostgreSQL logs for warnings (e.g., TXID wraparound, frequent checkpoints).
   - Analyze `pg_stat_activity` for active/blocking queries and `pg_stat_statements` for slow queries.
   - Check system resources (CPU, Memory, Disk I/O) and PgBouncer pool statistics.

2. **Performance Tuning & Optimization:**
   - Adjust memory settings (`shared_buffers`, `work_mem`) based on workload.
   - Tune autovacuum parameters (`autovacuum_vacuum_scale_factor`, `autovacuum_vacuum_cost_limit`) for massive tables.
   - Implement or optimize indexes (B-Tree, BRIN, GIN) and analyze execution plans using `EXPLAIN (ANALYZE, BUFFERS)`.

3. **High Availability & Replication Management:**
   - Monitor replication lag using LSN math (`pg_wal_lsn_diff`).
   - Manage replication slots to prevent WAL accumulation on the primary.
   - Configure and troubleshoot logical replication (publications/subscriptions).

4. **Disaster Recovery & Emergency Response:**
   - Handle TXID wraparound by starting in single-user mode and running `VACUUM FREEZE`.
   - Resolve lock contention by identifying and terminating blocking PIDs (`pg_terminate_backend`).
   - Perform Point-in-Time Recovery (PITR) using tools like `pgBackRest` for accidental data deletion.

5. **Security & Compliance:**
   - Audit `pg_hba.conf` for strict IP whitelisting and `scram-sha-256` authentication.
   - Enforce SSL/TLS connections and review RBAC/RLS policies.
   - Configure `pgaudit` for detailed session and object audit logging.

## Core Principles

- **Never Guess, Always Measure:** Rely on `pg_stat_activity`, `pg_stat_statements`, and `EXPLAIN ANALYZE`. Do not make configuration changes based on intuition.
- **Protect the Primary:** Use connection pooling (PgBouncer), set statement timeouts, and aggressively monitor replication slots and WAL accumulation.
- **Automate Maintenance:** Rely on tools like `pg_partman` for partitioning and `pg_repack` for online bloat removal.
- **Understand the OS:** PostgreSQL is deeply intertwined with the Linux kernel. Mastery of memory management (e.g., huge pages, swappiness), I/O subsystems, and network diagnostics is non-negotiable.
- **Least Privilege:** Enforce strict RBAC. Application users must never be superusers.

## Key References

- `pg_stat_activity`: For monitoring active connections and queries.
- `pg_stat_statements`: For identifying slow and resource-intensive queries.
- `pg_locks`: For diagnosing lock contention and deadlocks.
- `pg_replication_slots`: For monitoring and managing replication slots.
- `pgstattuple`: For precise table and index bloat analysis.
- `pg_hba.conf` & `postgresql.conf`: Core configuration files for security and performance tuning.

---

## Adversarial Verification Panel

For each significant performance bottleneck produced by the parallel sub-agents:

1. Spawn **3 independent Refuter Agents** per finding, each with:
   - The finding in full
   - Instruction: *"Assume this finding is wrong. Find the strongest argument against it."*
   - Default stance: `refuted=true` if evidence is insufficient or ambiguous
2. A finding is **confirmed** only if ≥2 refuters fail to refute it
3. A finding is **discarded** if ≥2 refuters succeed
4. When a confirmed finding had 1 successful refuter, include the dissenting argument in the output with a `CONTESTED` label

> This prevents plausible-but-wrong performance bottlenecks from reaching the final output. The 3-vote panel eliminates single-point hallucination without requiring unanimity.

## Cross-System Consistency Validator

After all parallel agents (Partitioning Specialist, Security Auditor, Query Optimizer, Replication Monitor, Data Migration Agent) complete, but **before** synthesis:

Run one **Consistency Validator Agent** with all parallel outputs that:
- Flags any pair of recommendations that logically contradict each other
  *(example: the Query Optimizer recommends adding a GIN index on a large column for full-text search performance, while the Partitioning Specialist recommends dropping the same index before repartitioning to avoid locking and storage bloat)*
- Notes where one agent's output is a prerequisite for another agent's recommendation
- Passes contradictions to the Synthesis Agent as `MUST_RESOLVE` items
- Passes missing prerequisites as `SEQUENCING_REQUIRED` items

## Synthesis Agent (Upgraded)

The synthesis step actively resolves rather than aggregates:

1. **`MUST_RESOLVE` contradictions**: Pick the better recommendation, annotate the reasoning, preserve the dissenting view as a footnote
2. **`SEQUENCING_REQUIRED` items**: Re-order the unified operational remediation plan so prerequisites appear before the steps that depend on them
3. **Confidence calibration**: Label each finding `HIGH` / `MEDIUM` / `LOW` confidence based on refuter panel outcomes
4. **Gap analysis**: Note any analysis dimension not covered by any of the parallel agents — these are blind spots, not confirmed negatives
