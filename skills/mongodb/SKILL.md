---
name: mongodb
description: Advanced MongoDB operations, performance tuning, and technical support guide for managing large-scale deployments. Triggers on query optimization, sharding, backup/restore, and log analysis tasks.
---

# MongoDB Advanced Operations and Tech Support Skill

## Scope and Triggers

Use this skill when dealing with advanced MongoDB topics, particularly in production environments, worst-case scenarios, and practical troubleshooting. It activates for:
- Optimizing complex aggregation pipelines to prevent performance degradation and memory exhaustion.
- Managing and troubleshooting change streams in event-driven architectures.
- Designing and debugging compound indexes following the ESR (Equality, Sort, Range) rule.
- Implementing and optimizing text search and time series collections.
- Handling massive datasets through sharding, archiving, and data lifecycle management.
- Utilizing MongoDB CLI tools (`mongosh`, `mongodump`, `mongorestore`, `mongoexport`, `mongoimport`) for advanced querying, backup, restoration, and data migration.
- Diagnosing and resolving performance bottlenecks, high resource usage, and common errors like "Connection Refused".

**Non-goals:** This skill does not cover basic CRUD operations, application-level driver usage, or general database design principles outside of performance tuning.

## Preconditions

Before executing any operations, the agent must:
1. Detect the target environment (e.g., standalone, replica set, sharded cluster).
2. Verify the MongoDB version using `scripts/verify-mongodb-version.sh`.
3. Check permissions to ensure the agent has the necessary roles (e.g., `clusterMonitor`, `backup`, `restore`, `dbAdmin`).
4. Understand the user intent and constraints (e.g., acceptable downtime, performance requirements).

## Source Freshness

Volatile facts, such as supported operators or default configurations, are verified against MongoDB 8.0 documentation as of 2026-08-07. If the target MongoDB version differs, the agent must verify the behavior against the official documentation for that specific version.

## Workflow

1. **Identify the Problem Domain:** Determine if the issue relates to query performance, data modeling (indexes, time series), data management (sharding, archiving), or operational tasks (backup, restore, migration).
2. **Gather Diagnostics (Read-Only):** Use `mongosh` to collect data. Run `explain("executionStats")` for slow queries, check `rs.status()` for replica set health, or use `db.currentOp()` to identify long-running operations.
3. **Analyze and Plan:** Based on the diagnostics, formulate a plan using the focused references.
4. **Sub-Agent Spawning (Optional):** If applicable, spawn parallel sub-agents (Query Optimizer, Shard Manager, etc.) and run the Adversarial Verification Panel and Cross-System Consistency Validator.
5. **Synthesize Findings:** Resolve contradictions and finalize the operation plan.
6. **Request Confirmation:** Require explicit user confirmation for any destructive or production-impacting actions (e.g., dropping collections, killing operations, index creation).
7. **Execute Operations:** Apply the planned solution. Use background operations where possible.
8. **Verify and Monitor:** After execution, verify the fix. Check query plans again, monitor resource usage, and ensure the system is stable. Stop when the issue is resolved or escalate if progress stalls.

## Safety

- **Read-Only Discovery:** Always start with read-only commands (`explain()`, `rs.status()`, `db.currentOp()`) to gather diagnostics.
- **Confirmation Required:** Explicit user confirmation is mandatory before executing destructive commands (e.g., dropping collections, killing operations) or production-impacting actions (e.g., index creation, chunk migration).
- **Dry Runs:** Ensure all mutating CLI commands support a dry-run or are preceded by a read-only discovery phase.

## Validation

- Validate aggregation pipelines with `explain()` before execution.
- Use `scripts/verify-mongodb-version.sh` to confirm the target environment version before applying version-specific optimizations.
- Capture evidence of the issue (e.g., slow query logs, `explain()` output) before and after applying the fix.

## Failure Handling

- If an operation fails, diagnose the error using the output and logs.
- Do not repeat a failed action unchanged.
- If a destructive action fails, provide guidance on how to roll back or recover (e.g., restoring from backup).
- Escalate to the user if the issue cannot be resolved after multiple attempts.

## Output Contract

The final output must include:
- A summary of the issue and the diagnostics gathered.
- The operations performed, including any scripts or commands executed.
- Evidence of the fix (e.g., improved `explain()` output, resolved error logs).
- Confidence level (HIGH/MEDIUM/LOW) based on the refuter panel outcomes (if applicable).
- Actionable next steps or recommendations for future prevention.

## Resources

- [Aggregation Pipeline Optimization](references/aggregation.md)
- [Change Streams](references/change-streams.md)
- [Compound Indexes](references/indexing.md)
- [Sharding](references/sharding.md)
- [CLI Tools](references/cli-tools.md)
- [Verify MongoDB Version Script](scripts/verify-mongodb-version.sh)

## Orchestration

This skill supports spawning sub-agents for parallel execution when tasks can be decomposed:

| Trigger Condition | Sub-Agent Type | Purpose |
|---|---|---|
| Multiple slow queries to analyze | Query Optimizer | Parallel analysis of `explain()` plans and index recommendations |
| Multiple shards to balance | Shard Manager | Parallel monitoring and chunk migration management |
| Multiple collections to backup/restore | Backup Specialist | Parallel execution of `mongodump`/`mongorestore` operations |
| Bulk log analysis for errors | Log Analyzer | Parallel parsing of MongoDB logs to identify anomalies |

### Spawning Rules
- Spawn when 3+ independent items (queries, shards, collections, logs) need the same operation.
- Each sub-agent receives: context (e.g., database connection string), specific target (e.g., collection name or query), and success criteria (e.g., optimized query plan or successful backup).
- Results are aggregated and cross-referenced for conflicts (e.g., ensuring index recommendations don't conflict).
- Maximum concurrent sub-agents: 10.

### Adversarial Verification Panel
For each significant performance bottleneck produced by the parallel sub-agents:
1. Spawn **3 independent Refuter Agents** per finding, each with the finding and instruction: *"Assume this finding is wrong. Find the strongest argument against it."*
2. A finding is **confirmed** only if ≥2 refuters fail to refute it.
3. A finding is **discarded** if ≥2 refuters succeed.
4. When a confirmed finding had 1 successful refuter, include the dissenting argument in the output with a `CONTESTED` label.

### Cross-System Consistency Validator
After all parallel agents complete, but **before** synthesis, run one **Consistency Validator Agent** with all parallel outputs that:
- Flags any pair of recommendations that logically contradict each other.
- Notes where one agent's output is a prerequisite for another agent's recommendation.
- Passes contradictions to the Synthesis Agent as `MUST_RESOLVE` items.
- Passes missing prerequisites as `SEQUENCING_REQUIRED` items.

### Synthesis Agent
The synthesis step actively resolves rather than aggregates:
1. **`MUST_RESOLVE` contradictions**: Pick the better recommendation, annotate the reasoning, preserve the dissenting view as a footnote.
2. **`SEQUENCING_REQUIRED` items**: Re-order the unified operations plan so prerequisites appear before the steps that depend on them.
3. **Confidence calibration**: Label each finding `HIGH` / `MEDIUM` / `LOW` confidence based on refuter panel outcomes.
4. **Gap analysis**: Note any analysis dimension not covered by any of the parallel agents.
