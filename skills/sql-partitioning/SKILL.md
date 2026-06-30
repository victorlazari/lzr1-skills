---
name: sql-partitioning
description: Advanced SQL partitioning, sharding, query optimization, and troubleshooting for high-scale production databases.
---

# SQL Partitioning and Sharding Specialist

## When to Use

This skill is designed for technical support operations, database administrators (DBAs), and site reliability engineers (SREs) managing massive SQL datasets (terabytes to petabytes). Use this skill when encountering:
- Severe performance degradation or query timeouts on large tables.
- Index bloat, vacuuming nightmares, or transaction ID wraparound risks.
- Challenges with cross-partition queries, partition pruning failures, or materialized views.
- Need for zero-downtime database migrations from unpartitioned to partitioned tables.
- Complex database incidents requiring advanced CLI diagnostics and emergency mitigation.
- Configuration tuning for partitioned architectures (e.g., `work_mem`, `autovacuum`, `enable_partition_pruning`).

## Sub-Agent Spawning

This skill supports spawning sub-agents for parallel execution when tasks can be decomposed:

| Trigger Condition | Sub-Agent Type | Purpose |
|---|---|---|
| Multiple massive tables to migrate | Migration Specialist | Parallel execution of zero-downtime table migrations |
| Multiple partitions requiring index rebuilds | Index Optimizer | Parallel concurrent index creation across partitions |
| Widespread query timeouts across services | Query Analyzer | Parallel `EXPLAIN ANALYZE` diagnostics for slow queries |
| Multi-shard health and replication checks | Shard Monitor | Parallel verification of shard health and replication lag |

### Spawning Rules
- Spawn when 3+ independent items (tables, partitions, queries, shards) need the same operation.
- Each sub-agent receives: context (database schema, current load), specific target (table/partition/query), and success criteria (e.g., index built, query optimized).
- Results are aggregated and cross-referenced for conflicts (e.g., locking issues, resource contention).
- Maximum concurrent sub-agents: 10.

## Workflow

1. **Incident Triage and Diagnostics:**
   - Identify the root cause of latency or timeouts using advanced CLI one-liners (e.g., finding long-running queries, blocking locks, or high bloat).
   - Execute `EXPLAIN (ANALYZE, BUFFERS)` to verify partition pruning and identify inefficient execution plans (e.g., sequential scans on massive tables).
2. **Configuration and Tuning:**
   - Verify critical parameters like `enable_partition_pruning` and `constraint_exclusion`.
   - Dynamically adjust `work_mem` at the session level for massive sorts to prevent temp file avalanches.
   - Tune autovacuum parameters at the table level for highly active partitions to prevent statistics stagnation.
3. **Execution and Mitigation:**
   - Implement safe index creation using `CREATE INDEX CONCURRENTLY` on individual partitions, followed by attaching them to the parent index.
   - Execute data archival or deletion in small batches to avoid WAL bloat and replication lag.
   - Perform zero-downtime migrations using techniques like partition exchange or `pg_repack`.
4. **Validation and Monitoring:**
   - Verify data integrity and query performance post-migration or optimization.
   - Monitor system resources (CPU, I/O, memory) and replication lag to ensure stability.

## Core Principles

- **Never Block Production:** Always use concurrent operations (e.g., `CREATE INDEX CONCURRENTLY`) and avoid DDL statements that hold exclusive locks on massive tables.
- **Batch Everything:** Massive updates or deletes must be executed in small batches with sleep intervals to allow vacuuming and replication to catch up.
- **Prune Relentlessly:** Ensure queries are designed to leverage partition pruning by filtering directly on partition keys without functions or implicit casts.
- **Pre-Validate Constraints:** When attaching partitions, always pre-validate constraints to avoid full table scans and catastrophic locking.
- **Avoid Default Partitions:** Prevent silent data spillage and massive default partition growth by explicitly handling unexpected partition keys.

## Key References

- [Complete Reference Guide](./references/complete-reference.md)
- [Reading List](./references/reading-list.md)

---

## Adversarial Verification Panel

For each significant partitioning and query optimization recommendations produced by the parallel sub-agents:

1. Spawn **3 independent Refuter Agents** per finding, each with:
   - The finding in full
   - Instruction: *"Assume this finding is wrong. Find the strongest argument against it."*
   - Default stance: `refuted=true` if evidence is insufficient or ambiguous
2. A finding is **confirmed** only if ≥2 refuters fail to refute it
3. A finding is **discarded** if ≥2 refuters succeed
4. When a confirmed finding had 1 successful refuter, include the dissenting argument in the output with a `CONTESTED` label

> This prevents plausible-but-wrong partitioning and query optimization recommendations from reaching the final output. The 3-vote panel eliminates single-point hallucination without requiring unanimity.

## Cross-System Consistency Validator

After all parallel agents (Migration Specialist, Index Optimizer, Query Analyzer, Shard Monitor) complete, but **before** synthesis:

Run one **Consistency Validator Agent** with all parallel outputs that:
- Flags any pair of recommendations that logically contradict each other
  *(example: Index Optimizer recommending a new concurrent index on a partition while Migration Specialist is mid-way through a partition exchange on the same table)*
- Notes where one agent's output is a prerequisite for another agent's recommendation
- Passes contradictions to the Synthesis Agent as `MUST_RESOLVE` items
- Passes missing prerequisites as `SEQUENCING_REQUIRED` items

## Synthesis Agent (Upgraded)

The synthesis step actively resolves rather than aggregates:

1. **`MUST_RESOLVE` contradictions**: Pick the better recommendation, annotate the reasoning, preserve the dissenting view as a footnote
2. **`SEQUENCING_REQUIRED` items**: Re-order the unified remediation plan so prerequisites appear before the steps that depend on them
3. **Confidence calibration**: Label each finding `HIGH` / `MEDIUM` / `LOW` confidence based on refuter panel outcomes
4. **Gap analysis**: Note any analysis dimension not covered by any of the parallel agents — these are blind spots, not confirmed negatives
