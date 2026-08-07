# Partitioning Strategies

## 1. Table Partitioning Strategies

Table partitioning involves dividing a large logical table into smaller, more manageable physical pieces called partitions. This is a survival mechanism for databases handling terabytes of data, solving issues like index bloat, vacuuming nightmares, query timeouts, and archival impossibility.

### 1.1 Range Partitioning

The most common strategy, typically based on a timestamp or date column. Ideal for time-series data, logs, audit trails, and historical records.

```sql
-- Creating the parent table
CREATE TABLE production_logs (
    log_id BIGSERIAL,
    service_name VARCHAR(255) NOT NULL,
    log_level VARCHAR(50) NOT NULL,
    message TEXT,
    created_at TIMESTAMPTZ NOT NULL
) PARTITION BY RANGE (created_at);

-- Creating partitions (e.g., monthly)
CREATE TABLE production_logs_2023_10 PARTITION OF production_logs
    FOR VALUES FROM ('2023-10-01 00:00:00Z') TO ('2023-11-01 00:00:00Z');
```

### 1.2 List Partitioning

Used when data can be naturally grouped by a specific, finite set of values, such as region, tenant ID, or status.

```sql
CREATE TABLE customer_transactions (
    transaction_id BIGSERIAL,
    customer_id BIGINT NOT NULL,
    region_code VARCHAR(10) NOT NULL,
    amount DECIMAL(15, 2) NOT NULL,
    transaction_date DATE NOT NULL
) PARTITION BY LIST (region_code);

CREATE TABLE transactions_na PARTITION OF customer_transactions
    FOR VALUES IN ('US', 'CA', 'MX');
```

### 1.3 Hash Partitioning

Useful for distributing data evenly across partitions when there is no natural range or list, often used for load balancing massive write-heavy tables to prevent hot spots.

```sql
CREATE TABLE user_sessions (
    session_id UUID NOT NULL,
    user_id BIGINT NOT NULL,
    session_data JSONB,
    last_active TIMESTAMPTZ NOT NULL
) PARTITION BY HASH (user_id);

-- Creating 4 partitions
CREATE TABLE user_sessions_p0 PARTITION OF user_sessions FOR VALUES WITH (MODULUS 4, REMAINDER 0);
```

## 2. Sharding Strategies

| Strategy | Description | Pros | Cons |
|---|---|---|---|
| **Range-based** | Data split by ranges of shard key values (e.g., customer ID 1-1000). | Simple to understand and implement. | Hotspots if data distribution is uneven. |
| **Hash-based** | Data distributed by hashing the shard key. | Uniform distribution. | Harder to query across shards. |
| **Directory-based** | Central directory maps keys to shards. | Flexible and dynamic. | Directory is a single point of failure. |
| **Composite** | Combination of above (e.g., range + hash). | Balanced approach. | Increased complexity. |

## 3. Partition Pruning

Partition pruning is a query optimization technique where the database engine executes a query only on the relevant partitions instead of scanning all data. It significantly reduces I/O and improves query response time.

### 3.1 Limitations and Pitfalls

- **Functions on partition keys:** `WHERE YEAR(date) = 2023` disables pruning. Use direct column filters: `WHERE date BETWEEN '2023-01-01' AND '2023-12-31'`.
- **Non-immutable functions:** Partition pruning fails when using non-immutable functions or complex OR conditions in the WHERE clause.
- **Bind variables hiding values:** Pruning may not occur if partition key is a bind variable. Use literals or database-specific bind variable options.
- **Complex predicates:** Multiple OR conditions spanning partitions. Rewrite queries to use UNION ALL with individual partition filters.
- **Partition key mismatch:** Filtering on non-partition columns. Add partition key filters or consider repartitioning.
- **Performance cliff:** Planning time scales with partition count. Querying across a massive number of partitions can cause severe performance degradation during query planning.

## 4. Configuration Schemas and Tuning Recommendations

### 4.1 Constraint Exclusion and Partition Pruning

Ensure `enable_partition_pruning = on` for declarative partitioning. For legacy inheritance-based partitioning, use `constraint_exclusion = partition`. A "plan time explosion" often occurs when pruning is disabled or when dealing with thousands of partitions.

### 4.2 Memory Management: work_mem for Massive Sorts

The default `work_mem` setting is insufficient for operations on huge datasets. Tune `work_mem` dynamically at the session level for specific, resource-intensive queries to prevent the "temp file avalanche."

```sql
SET work_mem = '4GB';
-- Execute massive sort query
RESET work_mem;
```

### 4.3 Autovacuum Tuning for Partitioned Architectures

Default autovacuum settings are frequently inadequate for partitioned environments. Tune parameters like `autovacuum_max_workers`, `autovacuum_naptime`, `autovacuum_vacuum_scale_factor`, and `autovacuum_analyze_scale_factor`. Apply specific autovacuum settings at the table level for highly active partitions to prevent "statistics stagnation."

```sql
ALTER TABLE sales_partition_2023_10 SET (
    autovacuum_vacuum_scale_factor = 0.02,
    autovacuum_analyze_scale_factor = 0.01
);
```

## 5. Advanced Topics in Partitioning

- **Partition-wise joins:** Join individual partitions of two tables directly, requiring strict schema alignment.
- **Default partitions:** Act as a catch-all but are a massive operational risk, as they can grow massive and cause locks when creating correct partitions. Avoid default partitions in high-scale environments.
- **PostgreSQL 16+ enhancements:** Improved execution-time partition pruning for prepared statements and parallel append optimizations.
- **Operational complexity:** Requires robust partition management automation (e.g., pg_partman) to prevent silent data gaps.
- **Fast path locking:** Lock manager contention issues can occur when dealing with many partitions. Monitor lock manager waits.
