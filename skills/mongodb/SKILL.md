---
name: mongodb
description: Advanced MongoDB operations, performance tuning, and technical support guide for managing large-scale deployments.
---

# MongoDB Advanced Operations and Tech Support Skill

## When to Use

Use this skill when dealing with advanced MongoDB topics, particularly in production environments, worst-case scenarios, and practical troubleshooting. It is essential for:
- Optimizing complex aggregation pipelines to prevent performance degradation and memory exhaustion.
- Managing and troubleshooting change streams in event-driven architectures.
- Designing and debugging compound indexes following the ESR (Equality, Sort, Range) rule.
- Implementing and optimizing text search and time series collections.
- Handling massive datasets through sharding, archiving, and data lifecycle management.
- Utilizing MongoDB CLI tools (`mongosh`, `mongodump`, `mongorestore`, `mongoexport`, `mongoimport`) for advanced querying, backup, restoration, and data migration.
- Diagnosing and resolving performance bottlenecks, high resource usage, and common errors like "Connection Refused".

## Sub-Agent Spawning

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

## Workflow

1. **Identify the Problem Domain:** Determine if the issue relates to query performance, data modeling (indexes, time series), data management (sharding, archiving), or operational tasks (backup, restore, migration).
2. **Gather Diagnostics:** Use `mongosh` to collect data. Run `explain("executionStats")` for slow queries, check `rs.status()` for replica set health, or use `db.currentOp()` to identify long-running operations.
3. **Analyze and Plan:** Based on the diagnostics, formulate a plan. For example, if a query uses a `COLLSCAN`, plan to create a compound index following the ESR rule. If CPU usage is high, plan to kill long-running queries and optimize them.
4. **Execute Operations:** Apply the planned solution. Use background index creation (`{ background: true }`) in production. Use `mongodump` and `mongorestore` for data recovery or migration.
5. **Verify and Monitor:** After execution, verify the fix. Check query plans again, monitor resource usage, and ensure the system is stable. Set up profiling (`db.setProfilingLevel()`) if necessary to catch future slow queries.

## Core Principles

- **Early Filtering:** In aggregation pipelines, always use `$match` and `$limit` as early as possible to reduce the dataset size and utilize indexes.
- **The ESR Rule:** Design compound indexes by placing Equality fields first, followed by Sort fields, and finally Range fields.
- **Background Operations:** Always perform index creation and other heavy operations in the background to avoid locking the database in production.
- **Oplog Awareness:** When working with change streams or point-in-time recovery, always monitor the oplog window size to prevent data loss.
- **Security First:** Never hardcode passwords in CLI scripts, restrict access to backup files, and always use TLS/SSL for connections.

## Key References

- **Aggregation Pipeline Optimization:** Focus on early filtering, index utilization, and managing memory limits (`allowDiskUse: true`).
- **Change Streams:** Require replica sets or sharded clusters. Monitor oplog size and manage resume tokens carefully.
- **Compound Indexes:** Rely on the ESR rule and avoid relying on index intersection for critical queries.
- **Time Series Collections:** Optimize by choosing the correct granularity and filtering by `timeField` and `metaField`.
- **Sharding:** Choose a shard key with high cardinality and even distribution to avoid jumbo chunks.
- **CLI Tools:** Master `mongosh` for querying and management, `mongodump`/`mongorestore` for backups and point-in-time recovery, and `mongoexport`/`mongoimport` for data integration.
