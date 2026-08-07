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

## Preconditions

Before taking action, the agent must:
1. Validate the target environment, permissions, and constraints using deterministic scripts.
2. Ensure read-only discovery precedes any mutation.
3. Verify that partition keys and functions used in queries are immutable.
4. Check for outdated table statistics using `ANALYZE`.
5. Monitor lock manager waits and fast path locking contention.
6. Validate that partition management automation (e.g., pg_partman) is running successfully to prevent silent data gaps.
7. Test query planning time for long-range queries across many partitions.

## Source Freshness

Volatile facts (e.g., supported versions, configuration defaults) must be verified against current upstream documentation or bundled verified references. See `references/source-map.md` for authoritative sources.

## Workflow

1. **Pre-flight check:** Validate target environment, permissions, and constraints using deterministic scripts (`scripts/validate-partition-config.sh`).
2. **Discovery:** Perform read-only analysis of current partition configuration and performance metrics.
3. **Planning:** Generate a migration or optimization plan using the provided template (`templates/migration-plan.md`).
4. **Confirmation:** Require explicit user confirmation for the proposed plan.
5. **Execution:** Execute the plan in small, verifiable batches with dry runs where possible (`scripts/dry-run-migration.sh`).
6. **Validation:** Verify data integrity and performance post-execution.
7. **Stop condition:** Stop when all planned actions are completed successfully or if a critical error occurs requiring rollback.

## Safety

- **Never Block Production:** Always use concurrent operations (e.g., `CREATE INDEX CONCURRENTLY`) and avoid DDL statements that hold exclusive locks on massive tables.
- **Batch Everything:** Massive updates or deletes must be executed in small batches with sleep intervals to allow vacuuming and replication to catch up.
- **Prune Relentlessly:** Ensure queries are designed to leverage partition pruning by filtering directly on partition keys without functions or implicit casts.
- **Pre-Validate Constraints:** When attaching partitions, always pre-validate constraints to avoid full table scans and catastrophic locking.
- **Avoid Default Partitions:** Prevent silent data spillage and massive default partition growth by explicitly handling unexpected partition keys.
- **Explicit Confirmation:** Require explicit user confirmation for all destructive or production-impacting actions (e.g., dropping partitions, executing migrations).

## Validation

- Define syntax checks, dry runs, tests, evidence capture, and postcondition verification.
- Provide deterministic validation scripts for syntax checks and dry runs.
- Include rollback guidance for all mutating operations.

## Failure Handling

- Explain how to diagnose errors, choose alternatives, roll back, and avoid repeating a failed action unchanged.
- If a critical error occurs, stop execution and require rollback.

## Output Contract

The result must specify the structure, evidence, severity/confidence, and actionable next steps expected.

## Resources

- [Partitioning Strategies](./references/partitioning-strategies.md)
- [Troubleshooting Commands](./references/troubleshooting-commands.md)
- [Migration Guide](./references/migration-guide.md)
- [Source Map](./references/source-map.md)
- [Validate Partition Config Script](./scripts/validate-partition-config.sh)
- [Dry Run Migration Script](./scripts/dry-run-migration.sh)
- [Migration Plan Template](./templates/migration-plan.md)

## Orchestration

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

### Adversarial Verification Panel

For each significant partitioning and query optimization recommendations produced by the parallel sub-agents:

1. Spawn **3 independent Refuter Agents** per finding, each with:
   - The finding in full
   - Instruction: *"Assume this finding is wrong. Find the strongest argument against it."*
   - Default stance: `refuted=true` if evidence is insufficient or ambiguous
2. A finding is **confirmed** only if ≥2 refuters fail to refute it
3. A finding is **discarded** if ≥2 refuters succeed
4. When a confirmed finding had 1 successful refuter, include the dissenting argument in the output with a `CONTESTED` label

### Cross-System Consistency Validator

After all parallel agents (Migration Specialist, Index Optimizer, Query Analyzer, Shard Monitor) complete, but **before** synthesis:

Run one **Consistency Validator Agent** with all parallel outputs that:
- Flags any pair of recommendations that logically contradict each other
- Notes where one agent's output is a prerequisite for another agent's recommendation
- Passes contradictions to the Synthesis Agent as `MUST_RESOLVE` items
- Passes missing prerequisites as `SEQUENCING_REQUIRED` items

### Synthesis Agent (Upgraded)

The synthesis step actively resolves rather than aggregates:

1. **`MUST_RESOLVE` contradictions**: Pick the better recommendation, annotate the reasoning, preserve the dissenting view as a footnote
2. **`SEQUENCING_REQUIRED` items**: Re-order the unified remediation plan so prerequisites appear before the steps that depend on them
3. **Confidence calibration**: Label each finding `HIGH` / `MEDIUM` / `LOW` confidence based on refuter panel outcomes
4. **Gap analysis**: Note any analysis dimension not covered by any of the parallel agents — these are blind spots, not confirmed negatives

## Cross-Skill Routing

- `finance-pro-playbooks` — route when task involves financial data modeling or reporting
- `security-review` — route when task involves database security, access control, or auditing
- `automation-and-scheduling` — route when task involves automated partition management or scheduled maintenance
