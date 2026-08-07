# Troubleshooting Commands

## 1. Advanced CLI One-Liners for Operations

**Find the longest-running active queries:**
```bash
psql -U postgres -d mydb -c "
SELECT pid, age(clock_timestamp(), query_start) AS duration, usename, state, query
FROM pg_stat_activity
WHERE state != 'idle' AND query NOT ILIKE '%pg_stat_activity%'
ORDER BY duration DESC LIMIT 10;"
```

**Kill a specific runaway query:**
```bash
psql -U postgres -d mydb -c "SELECT pg_cancel_backend(<PID>);"
```

**Identify tables with the most bloat:**
```bash
psql -U postgres -d mydb -c "
SELECT relname AS table_name, n_dead_tup AS dead_tuples, n_live_tup AS live_tuples,
       ROUND((n_dead_tup::numeric / NULLIF(n_live_tup + n_dead_tup, 0)) * 100, 2) AS bloat_ratio
FROM pg_stat_user_tables
ORDER BY n_dead_tup DESC LIMIT 10;"
```

## 2. Mastering EXPLAIN ANALYZE

`EXPLAIN ANALYZE` is the primary diagnostic tool for query performance. Look for execution time, node types (e.g., Seq Scan vs. Index Scan), actual rows vs. estimated rows, and buffers. Ensure partition pruning is occurring by checking that only relevant partitions are scanned.

## 3. Troubleshooting Common Issues

| Issue | Description | Troubleshooting Steps |
|---|---|---|
| **Stale data in MV** | MV not refreshed or refresh failed. | Check refresh schedules and logs; force manual refresh. |
| **Refresh performance degradation** | Refresh taking longer than usual. | Investigate underlying base table changes; optimize logs. |
| **Query not using MV** | Optimizer not selecting MV for query. | Verify MV definitions and query compatibility; consider optimizer hints. |
| **MV invalidation due to base table changes** | Schema changes or partition modifications invalidate MV. | Review and recompile MV; re-create if necessary. |
| **Shard Hotspotting** | One shard receives disproportionate traffic. | Re-sharding or key rebalancing; caching. |
| **Cross-shard Joins** | Queries span multiple shards, leading to latency. | Denormalize data; use async aggregation. |
| **Shard Failure / Node Crash** | One or more shards become unavailable. | Replica sets, failover mechanisms, alerting. |
| **Re-sharding / Data Migration** | Moving data to new shards due to growth or imbalance. | Use online migration tools; minimize locks; phased rollout. |
| **Timeouts on Large Queries** | Queries take longer than allowed, causing failures. | Query optimization, pagination, and timeouts set appropriately. |

## 4. Additional Checks

- **Outdated statistics:** Check for outdated table statistics using `ANALYZE`.
- **Lock manager contention:** Monitor lock manager waits and fast path locking contention.
- **Partition management automation:** Validate that partition management automation (e.g., pg_partman) is running successfully to prevent silent data gaps.
- **Query planning time:** Test query planning time for long-range queries across many partitions.
