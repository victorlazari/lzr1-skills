# Advanced Redis and Valkey: Complete Production Reference

**Verified against upstream: 2026-08-07**

## 1. Introduction

In modern distributed systems, Redis and its open-source successor Valkey serve as critical infrastructure components. This comprehensive reference is designed for technical support engineers, SREs, and DBAs responsible for maintaining, troubleshooting, and optimizing Redis and Valkey deployments in production environments.

## 2. Valkey 8.0 and 8.1 Enhancements

Valkey 8.0 and 8.1 introduce significant performance and observability improvements:
- **New Hashtable Implementation:** Improves memory efficiency and performance.
- **I/O Thread Optimizations:** Better offloading of I/O operations for increased throughput.
- **Observability:** Enhanced `COMMANDLOG` feature for troubleshooting latency, and improved `LATENCY LATEST` command.

*Primary Sources:*
- Valkey 8.0.0 Release Notes: https://valkey.io/blog/valkey-8-ga/
- Valkey 8.1.0 Release Notes: https://valkey.io/blog/valkey-8-1-0-ga/

## 3. Migrating from Redis to Valkey

Following the licensing changes to Redis, many organizations are migrating to Valkey. Valkey maintains high compatibility with Redis OSS 7.2 and earlier.

**CRITICAL WARNING:** Valkey is a fork of Redis 7.2.4. It is **NOT** compatible with Redis Community Edition (CE) version 7.4 and later RDB files.

### 3.1 Pre-Migration Checklist

- **Version Audit:** Ensure the current Redis version is 7.2 or older.
- **Client Libraries:** Most existing Redis client libraries work seamlessly with Valkey.

### 3.2 Migration Strategies

**Strategy 1: Replica Promotion (Zero Downtime)**
1. Deploy a new Valkey instance.
2. Configure Valkey as a replica of the existing Redis primary node (`REPLICAOF`).
3. Wait for initial synchronization and zero replication lag.
4. Pause application traffic briefly.
5. Execute `REPLICAOF NO ONE` on Valkey to promote it.
6. Update application configuration and resume traffic.

**Strategy 2: Backup and Restore (Physical Migration)**
1. Stop application traffic to Redis.
2. Trigger a manual snapshot (`BGSAVE`).
3. Copy `dump.rdb` to the Valkey server.
4. Start Valkey, ensuring it loads `dump.rdb`. **Note:** Ensure AOF is disabled on the first start of Valkey when performing a physical migration using an RDB file.
5. Update application configuration and resume traffic.

*Primary Sources:*
- Valkey Migration Guide: https://valkey.io/topics/migration/
- Percona Redis to Valkey Migration Guide: https://docs.percona.com/valkey/migration.html

## 4. Advanced Caching Patterns

- **Cache Aside (Lazy Loading):** Application manages the cache. Risk of stale data and thundering herd.
- **Write-Through:** Data written to cache and DB simultaneously. Good for read-heavy workloads.
- **Write-Behind:** Data written to cache initially, synced asynchronously. High write performance, risk of data loss.

### Cache Eviction Policies
- `volatile-lru`: Evicts least recently used keys with expiration.
- `allkeys-lru`: Evicts least recently used keys regardless of expiration.
- `volatile-lfu`: Evicts least frequently used keys with expiration.
- `allkeys-lfu`: Evicts least frequently used keys regardless of expiration.

## 5. Lua Scripting

Lua scripts execute atomically, preventing race conditions.
- **Risks:** Long-running scripts block the server. Infinite loops require `SCRIPT KILL` or `SHUTDOWN NOSAVE`.
- **Best Practices:** Keep scripts short, use `EVALSHA`, and parameterize scripts.

## 6. Messaging: Pub/Sub vs. Streams

- **Pub/Sub:** Ephemeral, low latency. Messages lost if subscriber disconnected.
- **Streams:** Persistent, append-only log. Supports consumer groups and acknowledgments (`XACK`).

## 7. RedisJSON

Allows in-place updates of JSON documents, reducing network bandwidth.
- **Challenges:** Higher memory overhead compared to native hashes.

## 8. Handling Hot Keys

- **Identify:** `redis-cli --hotkeys`, `MONITOR` (caution), client metrics.
- **Mitigate (Read-Heavy):** Client-side caching, read replicas.
- **Mitigate (Write-Heavy):** Key sharding, batching.

## 9. CLI Reference

```bash
# Continuous statistics
redis-cli -h production-db --stat

# Measure latency
redis-cli -h production-db --latency

# Scan for large keys
redis-cli -h production-db --bigkeys

# Scan for hot keys (requires LFU)
redis-cli -h production-db --hotkeys

# Memory stats
redis-cli MEMORY STATS

# Analyze specific key memory
redis-cli MEMORY USAGE "user:profile:12345"
```
