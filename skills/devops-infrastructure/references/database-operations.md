# Database Operations

## Table of Contents
1. High Availability
2. Backup and Recovery
3. Replication
4. Performance Tuning
5. Operational Procedures

---

## 1. High Availability

### HA Architectures

| Pattern | RPO | RTO | Complexity |
|---|---|---|---|
| Primary-Standby (sync) | 0 | Minutes | Low |
| Primary-Standby (async) | Seconds | Minutes | Low |
| Multi-AZ (managed) | 0 | <1 min | Low (managed) |
| Active-Active | 0 | 0 (no failover) | High |
| Patroni (PostgreSQL) | 0 | Seconds | Medium |

### PostgreSQL HA with Patroni

```yaml
# Patroni provides automatic failover for PostgreSQL
# Architecture: Patroni + etcd/Consul + HAProxy/PgBouncer
Primary (read-write) ←→ etcd (consensus)
    ↓ streaming replication
Standby 1 (read-only) ←→ etcd
Standby 2 (read-only) ←→ etcd
    ↑
HAProxy/PgBouncer (connection routing)
```

### Failover Procedures

1. Detect primary failure (health checks, consensus)
2. Promote standby to primary (automatic with Patroni)
3. Redirect connections (DNS update or proxy reconfiguration)
4. Verify data consistency on new primary
5. Rebuild old primary as new standby
6. Verify replication is healthy

---

## 2. Backup and Recovery

### Backup Strategy (3-2-1 Rule)

- **3** copies of data (production + 2 backups)
- **2** different storage media/locations
- **1** offsite copy (different region/cloud)

### PostgreSQL Backup Methods

| Method | Type | Speed | PITR | Use Case |
|---|---|---|---|---|
| pg_dump | Logical | Slow (large DBs) | No | Small DBs, schema-only |
| pg_basebackup | Physical | Fast | Yes (with WAL) | Production backups |
| pgBackRest | Physical + incremental | Fast | Yes | Enterprise production |
| Barman | Physical + incremental | Fast | Yes | Enterprise production |
| WAL archiving | Continuous | Minimal overhead | Yes | Point-in-time recovery |

### Recovery Procedures

```bash
# Point-in-time recovery with pgBackRest
pgbackrest --stanza=main --type=time \
  --target="2025-01-15 14:30:00" \
  --target-action=promote \
  restore

# Verify recovery
psql -c "SELECT pg_is_in_recovery();"  # Should be false after promote
psql -c "SELECT * FROM critical_table LIMIT 5;"  # Verify data
```

### Backup Testing

- Restore backups weekly in a test environment
- Verify data integrity after restore (checksums, row counts)
- Measure and document recovery time
- Test PITR to specific timestamps
- Automate backup verification in CI/CD

---

## 3. Replication

### Replication Types

| Type | Consistency | Latency | Use Case |
|---|---|---|---|
| Synchronous | Strong | Higher (write latency) | Financial, critical data |
| Asynchronous | Eventual | Low | Read scaling, analytics |
| Logical | Selective | Variable | Cross-version, selective tables |
| Streaming | Physical | Very low | HA standby |

### Read Replica Patterns

```
Application
├── Writes → Primary (single node)
└── Reads → Read Replicas (multiple nodes)
    ├── Replica 1 (general reads)
    ├── Replica 2 (reporting/analytics)
    └── Replica 3 (search indexing)
```

**Considerations**:
- Replication lag: reads may be stale (monitor `pg_stat_replication`)
- Connection routing: use PgBouncer or application-level routing
- Failover: promote replica if primary fails
- Load distribution: route heavy queries to dedicated replicas

### Monitoring Replication

```sql
-- PostgreSQL: Check replication lag
SELECT client_addr, state, 
       pg_wal_lsn_diff(pg_current_wal_lsn(), replay_lsn) AS lag_bytes,
       now() - pg_last_xact_replay_timestamp() AS lag_time
FROM pg_stat_replication;

-- Alert if lag > 30 seconds or > 100MB
```

---

## 4. Performance Tuning

### PostgreSQL Configuration

| Parameter | Purpose | Guideline |
|---|---|---|
| shared_buffers | Shared memory cache | 25% of RAM |
| effective_cache_size | Planner's cache estimate | 50-75% of RAM |
| work_mem | Per-operation sort/hash memory | RAM / (max_connections * 4) |
| maintenance_work_mem | VACUUM, CREATE INDEX | 512MB-2GB |
| max_connections | Connection limit | Use pooling, keep low (100-200) |
| wal_buffers | WAL write buffer | 64MB |
| random_page_cost | SSD vs HDD planner hint | 1.1 for SSD, 4.0 for HDD |
| effective_io_concurrency | Concurrent I/O operations | 200 for SSD |

### Vacuum and Maintenance

```sql
-- Check tables needing vacuum
SELECT schemaname, relname, n_dead_tup, last_autovacuum
FROM pg_stat_user_tables
WHERE n_dead_tup > 10000
ORDER BY n_dead_tup DESC;

-- Manual vacuum for critical tables
VACUUM (VERBOSE, ANALYZE) large_table;

-- Reindex bloated indexes
REINDEX INDEX CONCURRENTLY idx_name;
```

### Connection Pooling

| Tool | Mode | Best For |
|---|---|---|
| PgBouncer | Transaction/Session/Statement | Most deployments |
| pgpool-II | Session + load balancing | Read replica routing |
| Application pool (HikariCP) | Application-level | JVM applications |

**PgBouncer Configuration**:
```ini
[databases]
mydb = host=primary port=5432 dbname=mydb

[pgbouncer]
pool_mode = transaction        # Release connection after transaction
max_client_conn = 1000         # Max client connections
default_pool_size = 25         # Connections per database/user pair
reserve_pool_size = 5          # Emergency connections
server_idle_timeout = 600      # Close idle server connections
```

---

## 5. Operational Procedures

### Database Migrations in Production

1. **Pre-flight**: Test migration on production-size data copy
2. **Backup**: Take backup immediately before migration
3. **Maintenance window** (if needed): Communicate to stakeholders
4. **Execute**: Run migration with monitoring
5. **Verify**: Check data integrity, application health
6. **Rollback plan**: Have tested rollback ready

### Monitoring Checklist

| Metric | Warning | Critical | Action |
|---|---|---|---|
| Connection usage | 70% of max | 85% of max | Scale pool or investigate leaks |
| Replication lag | >10 seconds | >60 seconds | Check network, replica load |
| Disk usage | 75% | 85% | Expand storage, archive data |
| Long-running queries | >30 seconds | >5 minutes | Investigate, possibly kill |
| Lock waits | >5 seconds | >30 seconds | Identify blocking query |
| Cache hit ratio | <95% | <90% | Increase shared_buffers |
| Dead tuples | >1M per table | >10M per table | Run VACUUM |

### Emergency Procedures

```bash
# Kill long-running query
SELECT pg_terminate_backend(pid)
FROM pg_stat_activity
WHERE state = 'active' AND query_start < NOW() - INTERVAL '5 minutes'
AND query NOT LIKE '%pg_stat%';

# Check for blocking locks
SELECT blocked.pid AS blocked_pid,
       blocked.query AS blocked_query,
       blocking.pid AS blocking_pid,
       blocking.query AS blocking_query
FROM pg_stat_activity blocked
JOIN pg_locks bl ON bl.pid = blocked.pid
JOIN pg_locks l ON l.locktype = bl.locktype AND l.relation = bl.relation
JOIN pg_stat_activity blocking ON blocking.pid = l.pid
WHERE NOT bl.granted AND l.granted;
```
