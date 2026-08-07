# Migration Plan Template

## 1. Overview

- **Target Table:** [Table Name]
- **Current Size:** [Size in GB/TB]
- **Partitioning Strategy:** [Range / List / Hash]
- **Partition Key:** [Column Name]
- **Estimated Downtime:** [Zero / X minutes]

## 2. Pre-conditions

- [ ] Target environment validated.
- [ ] Permissions verified.
- [ ] Constraints checked.
- [ ] Partition keys and functions are immutable.
- [ ] Table statistics are up-to-date.
- [ ] Lock manager waits are within acceptable limits.
- [ ] Partition management automation is running.

## 3. Execution Steps

1. **Create New Partitioned Table:**
   ```sql
   -- SQL to create the new partitioned table
   ```

2. **Create Partitions:**
   ```sql
   -- SQL to create initial partitions
   ```

3. **Migrate Data (Batching):**
   ```sql
   -- SQL or script to migrate data in batches
   ```

4. **Create Indexes Concurrently:**
   ```sql
   -- SQL to create indexes concurrently on partitions
   ```

5. **Attach Partitions:**
   ```sql
   -- SQL to attach partitions to the parent table
   ```

6. **Swap Tables (if applicable):**
   ```sql
   -- SQL to swap the old and new tables
   ```

## 4. Post-conditions

- [ ] Data integrity verified (row counts, checksums).
- [ ] Query performance validated (`EXPLAIN ANALYZE`).
- [ ] System resources monitored (CPU, I/O, memory).
- [ ] Replication lag is within acceptable limits.

## 5. Rollback Plan

- **Trigger Condition:** [Condition that triggers rollback]
- **Rollback Steps:**
  1. [Step 1]
  2. [Step 2]
  3. [Step 3]
