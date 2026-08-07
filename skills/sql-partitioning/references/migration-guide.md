# Migration Guide

## 1. Migrating Unpartitioned Tables to Partitioned Tables

### 1.1 Why Migrate to Partitioned Tables?

Migrating to partitioned tables offers improved query performance via partition pruning, easier data management (e.g., archiving, purging), better maintenance (index rebuilds on partitions), and reduced locking and improved concurrency.

### 1.2 Planning the Migration

Analyze current workload and query patterns. Choose partition keys based on access patterns. Estimate data volume per partition. Plan for downtime or online migration methods. Backup data and schemas before migration.

### 1.3 Migration Strategies

| Strategy | Description | Pros | Cons |
|---|---|---|---|
| **Export/Import** | Export data, create partitioned table, import. | Simple and clean. | Downtime required; large data slow. |
| **CTAS (Create Table As Select)** | Create new partitioned table with SELECT from old. | Minimal downtime if done correctly. | Needs storage for duplicate data. |
| **Online Table Redefinition** | Use database tools (e.g., Oracle DBMS_REDEFINITION). | No downtime. | Complex; requires expertise. |
| **Partition Exchange** | Create partitioned table with empty partitions, then exchange data. | Fast data movement. | Requires table structure compatibility. |

### 1.4 Operational Impact and Rollback Procedures

Some migration methods require table locks, necessitating planned maintenance windows. Migration jobs may consume resources impacting production. Keep original tables intact until migration is verified, and have scripts ready to restore. Inform stakeholders of expected downtime and risks.

### 1.5 Post-Migration Validation and Monitoring

Verify data counts, checksums, and constraints. Run representative queries and compare execution plans. Monitor query performance and resource usage. Enable detailed logging for the initial period. Prepare to rollback or patch migration if issues arise.

## 2. Managing Partitions in Production

### 2.1 Attaching and Detaching Partitions

During migrations or archival processes, you need to move data without locking the parent table for extended periods.

**Detaching a partition (Archival):**
```sql
ALTER TABLE production_logs DETACH PARTITION production_logs_2022_01;
```

**Attaching a partition concurrently (Migration):**
```sql
-- 1. Create the new table with constraints matching the partition bounds
CREATE TABLE new_partition_2023_12 (LIKE production_logs INCLUDING ALL);
ALTER TABLE new_partition_2023_12 ADD CONSTRAINT check_date
    CHECK (created_at >= '2023-12-01 00:00:00Z' AND created_at < '2024-01-01 00:00:00Z');

-- 2. Load data into the new table
INSERT INTO new_partition_2023_12 SELECT * FROM old_massive_table WHERE created_at >= '2023-12-01 00:00:00Z' AND created_at < '2024-01-01 00:00:00Z';

-- 3. Attach the partition
ALTER TABLE production_logs ATTACH PARTITION new_partition_2023_12
    FOR VALUES FROM ('2023-12-01 00:00:00Z') TO ('2024-01-01 00:00:00Z');

-- 4. Drop the constraint
ALTER TABLE new_partition_2023_12 DROP CONSTRAINT check_date;
```

### 2.2 Index Creation on Partitions

Creating indexes on massive tables is dangerous. Always use `CONCURRENTLY` when creating indexes on live production tables. For partitioned tables, build the indexes on the individual partitions and then attach them to the parent index.

```sql
-- 1. Create the index on the parent table as INVALID
CREATE INDEX idx_logs_level ON ONLY production_logs (log_level);

-- 2. Build the index concurrently on each partition
CREATE INDEX CONCURRENTLY idx_logs_level_2023_10 ON production_logs_2023_10 (log_level);

-- 3. Attach the partition indexes to the parent index
ALTER INDEX idx_logs_level ATTACH PARTITION idx_logs_level_2023_10;
```

### 2.3 Database Migrations and Partitioning

During large migrations, temporarily increase `maintenance_work_mem` significantly to allow index creation to occur entirely in memory. Increase `max_wal_size` and `checkpoint_timeout` to handle the enormous volume of WAL data generated during migrations.
