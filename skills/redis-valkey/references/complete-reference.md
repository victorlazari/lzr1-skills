# Advanced Redis and Valkey: Complete Production Reference

## 1. Introduction

In modern distributed systems, Redis and its open-source successor Valkey serve as critical infrastructure components, providing high-performance caching, message brokering, and real-time data processing capabilities. As organizations scale, the operational complexity of managing these in-memory data stores increases exponentially. This comprehensive reference is designed for technical support engineers, site reliability engineers (SREs), and database administrators who are responsible for maintaining, troubleshooting, and optimizing Redis and Valkey deployments in production environments.

This document consolidates advanced topics, including sophisticated caching patterns, Lua scripting for atomic operations, messaging paradigms like Pub/Sub and Streams, the RedisJSON module, strategies for mitigating hot keys, the critical process of migrating from Redis to Valkey, and a comprehensive CLI reference for `redis-cli` and `valkey-cli`. The focus remains steadfastly on production operations, worst-case scenarios, and actionable tech support methodologies.

## 2. Advanced Caching Patterns and Strategies

Caching is the most common use case for Redis and Valkey, but implementing it effectively at scale requires a nuanced understanding of access patterns and data lifecycles.

### 2.1 Cache Aside (Lazy Loading)

In the Cache Aside pattern, the application code is responsible for managing the cache. When data is requested, the application first checks the cache. If the data is present (a cache hit), it is returned immediately. If the data is missing (a cache miss), the application retrieves it from the primary database, stores it in the cache, and then returns it to the user.

**Production Considerations:**
- **Stale Data:** Because the cache is updated only on a miss, data can become stale if the primary database is updated independently. Implementing appropriate Time-To-Live (TTL) values is crucial.
- **Thundering Herd Problem:** If a highly requested key expires, multiple clients might simultaneously experience a cache miss and query the primary database, potentially overwhelming it.

**Tech Support Scenario:**
*Symptom:* A sudden spike in database load accompanied by increased latency.
*Diagnosis:* Check for the expiration of a popular cache key. Use the `MONITOR` command (with caution in production) or analyze slow logs to identify the queries hitting the database.
*Resolution:* Implement cache warming for critical keys or use a probabilistic early expiration strategy (e.g., XFetch) to refresh the cache before it fully expires.

### 2.2 Write-Through and Write-Behind Caching

In a Write-Through cache, data is written to the cache and the primary database simultaneously. This ensures data consistency but adds latency to write operations. In a Write-Behind (or Write-Back) cache, data is written only to the cache initially, and an asynchronous process later synchronizes it with the primary database.

**Production Considerations:**
- **Write-Through:** Excellent for read-heavy workloads where data consistency is paramount. However, it can bottleneck write-heavy applications.
- **Write-Behind:** Offers superior write performance but introduces the risk of data loss if the cache node fails before synchronization occurs.

**Tech Support Scenario:**
*Symptom:* Data inconsistencies between the cache and the primary database in a Write-Behind setup.
*Diagnosis:* Investigate the asynchronous synchronization worker. Check for failed jobs, network partitions, or resource exhaustion on the worker nodes.
*Resolution:* Implement robust error handling and retry mechanisms in the synchronization process. Monitor the queue length of pending writes.

### 2.3 Cache Eviction Policies

When the memory limit (`maxmemory`) is reached, Redis and Valkey must evict existing keys to make room for new ones. Choosing the right eviction policy is critical for maintaining cache hit rates.

| Policy | Description | Use Case |
| :--- | :--- | :--- |
| `volatile-lru` | Evicts the least recently used keys with an expiration set. | Standard caching where some keys are persistent. |
| `allkeys-lru` | Evicts the least recently used keys regardless of expiration. | Pure caching where all keys are expendable. |
| `volatile-lfu` | Evicts the least frequently used keys with an expiration set. | Workloads with consistent long-term popular keys. |
| `allkeys-lfu` | Evicts the least frequently used keys regardless of expiration. | Pure caching with consistent long-term popular keys. |

**Tech Support Scenario:**
*Symptom:* High cache miss rates and frequent evictions.
*Diagnosis:* Check the `evicted_keys` metric in the `INFO stats` output. Analyze the access patterns to determine if the current eviction policy aligns with the workload.
*Resolution:* If the workload has a strong temporal locality, LRU is appropriate. If certain keys are consistently popular over time, LFU might yield better results. Consider increasing the `maxmemory` limit if resources permit.

## 3. Lua Scripting for Atomic Operations

Lua scripting allows developers to execute complex logic directly on the Redis/Valkey server. Because scripts are executed atomically, they prevent race conditions and reduce network round trips.

### 3.1 The Power of Atomicity

When a Lua script is executing, no other commands or scripts can run. This guarantees that the operations within the script are performed as a single, indivisible unit. This is invaluable for operations like conditional updates, rate limiting, and complex inventory management.

### 3.2 Production Risks and Worst-Case Scenarios

While powerful, Lua scripting introduces significant operational risks.

- **Blocking the Server:** Because execution is atomic, a long-running Lua script will block the entire server, causing all other client requests to queue up and potentially time out.
- **Infinite Loops:** A poorly written script with an infinite loop can render the server completely unresponsive.

**Tech Support Scenario:**
*Symptom:* The Redis/Valkey server becomes unresponsive, and clients report widespread timeouts.
*Diagnosis:* Check the `INFO commandstats` for the `eval` and `evalsha` commands. Look for high `usec_per_call` values.
*Resolution:* If a script is stuck in an infinite loop, use the `SCRIPT KILL` command to terminate it. If the script has already performed write operations, `SCRIPT KILL` will fail to prevent data inconsistency. In this worst-case scenario, the only recourse is to use the `SHUTDOWN NOSAVE` command, which will result in data loss since the last snapshot.

### 3.3 Best Practices for Lua Scripting

- **Keep Scripts Short and Fast:** Scripts should execute in milliseconds. Avoid complex computations or large data iterations within the script.
- **Use EVALSHA:** Always load scripts using `SCRIPT LOAD` and execute them using `EVALSHA` to save bandwidth and parsing overhead.
- **Parameterize Scripts:** Pass keys and arguments explicitly rather than hardcoding them within the script. This ensures that the script can be properly routed in a clustered environment.

## 4. Messaging Paradigms: Pub/Sub vs. Streams

Redis and Valkey offer two distinct messaging paradigms: Publish/Subscribe (Pub/Sub) and Streams. Understanding their differences is crucial for architectural decisions and troubleshooting.

### 4.1 Publish/Subscribe (Pub/Sub)

Pub/Sub is a fire-and-forget messaging system. Publishers send messages to channels, and subscribers listening to those channels receive them.

**Production Characteristics:**
- **Ephemeral:** Messages are not stored. If a subscriber is disconnected when a message is published, that message is lost to that subscriber.
- **Low Latency:** Extremely fast for real-time broadcasting (e.g., chat applications, live updates).

**Tech Support Scenario:**
*Symptom:* Subscribers are missing messages.
*Diagnosis:* Verify network stability between the subscribers and the server. Check if the subscribers are experiencing high CPU load, causing them to process messages slower than they are published.
*Resolution:* Implement application-level acknowledgments if message delivery guarantees are required, or migrate to Redis Streams.

### 4.2 Redis Streams

Introduced in Redis 5.0, Streams provide a persistent, append-only log data structure. They offer robust messaging capabilities, including consumer groups, message acknowledgments, and historical message retrieval.

**Production Characteristics:**
- **Persistence:** Messages are stored in memory and can be persisted to disk (RDB/AOF).
- **Consumer Groups:** Allow multiple consumers to cooperate in processing a stream of messages, ensuring that each message is processed by only one consumer in the group.
- **Acknowledgments:** Consumers must explicitly acknowledge (`XACK`) messages after processing them.

**Tech Support Scenario:**
*Symptom:* Memory usage is growing rapidly, and the stream length is unbounded.
*Diagnosis:* Check the stream length using `XLEN`. Inspect the Pending Entries List (PEL) using `XPENDING` to see if consumers are failing to acknowledge messages.
*Resolution:* Ensure consumers are correctly calling `XACK`. Implement a capping strategy using the `MAXLEN` argument with `XADD` to limit the stream size. Handle "dead letters" (messages that repeatedly fail processing) by moving them to a separate stream or logging them.

## 5. RedisJSON: Managing Document Data

The RedisJSON module extends Redis and Valkey to natively support JSON data types. It allows for storing, updating, and querying JSON documents efficiently.

### 5.1 Operational Advantages

- **In-Place Updates:** Unlike storing JSON as serialized strings, RedisJSON allows updating specific fields within a document without retrieving and rewriting the entire object. This significantly reduces network bandwidth and CPU overhead.
- **Integration with RediSearch:** When combined with the RediSearch module, RedisJSON enables powerful full-text search and secondary indexing capabilities on JSON documents.

### 5.2 Production Challenges

- **Memory Overhead:** Storing data as JSON objects incurs a higher memory overhead compared to native Redis hashes or strings due to the internal tree structure used to represent the JSON.
- **Complexity in Clustering:** Querying across multiple shards in a clustered environment can be complex and may require application-level aggregation.

**Tech Support Scenario:**
*Symptom:* High memory consumption after migrating from serialized strings to RedisJSON.
*Diagnosis:* Compare the memory usage of the keys using the `MEMORY USAGE` command.
*Resolution:* Evaluate if the benefits of in-place updates and querying outweigh the memory cost. Consider flattening deeply nested JSON structures or using native Redis hashes for simpler data models.

## 6. Handling Hot Keys

A "hot key" is a single key that receives an overwhelming volume of read or write requests, creating a bottleneck on the specific shard or node where it resides. This is a common and severe issue in large-scale deployments.

### 6.1 Identifying Hot Keys

- **Redis CLI:** Use the `redis-cli --hotkeys` command (requires the `maxmemory-policy` to be set to an LFU variant).
- **MONITOR Command:** Use `MONITOR` for a brief period and analyze the output, but be extremely cautious as this can degrade server performance.
- **Client-Side Metrics:** Instrument the application code to track key access frequencies.

### 6.2 Mitigation Strategies

**For Read-Heavy Hot Keys:**
1.  **Client-Side Caching:** Cache the hot key's value directly within the application's memory for a short duration (e.g., a few seconds). This drastically reduces the load on the Redis/Valkey server.
2.  **Read Replicas:** Distribute the read load across multiple replica nodes. Ensure the application is configured to route read queries to replicas.

**For Write-Heavy Hot Keys:**
1.  **Key Sharding (Splitting):** Append a random integer or a hash of the user ID to the key name (e.g., `inventory:item123:1`, `inventory:item123:2`). Distribute the writes across these sub-keys and aggregate them on read.
2.  **Batching:** Accumulate writes on the client side and send them in batches using pipelining or Lua scripts.

**Tech Support Scenario:**
*Symptom:* One node in a cluster has 100% CPU utilization, while others are idle. Latency spikes are observed for specific operations.
*Diagnosis:* This is the classic signature of a hot key. Identify the key using the methods described above.
*Resolution:* Immediately implement client-side caching as a stopgap measure. Work with the development team to implement key sharding or architectural changes for a long-term solution.

## 7. Migrating from Redis to Valkey

Following the licensing changes to Redis, many organizations are migrating to Valkey, the open-source, Linux Foundation-backed fork. Valkey maintains high compatibility with Redis, making the migration process relatively straightforward, but careful planning is essential.

### 7.1 Compatibility and Assessment

Valkey is a fork of Redis 7.2.4. Therefore, it is fully compatible with the Redis protocol, commands, and data structures up to that version.

**Pre-Migration Checklist:**
- **Version Audit:** Ensure the current Redis version is 7.2 or older. If using Redis modules (e.g., RediSearch, RedisJSON), verify their availability and compatibility in the Valkey ecosystem.
- **Client Libraries:** Most existing Redis client libraries will work seamlessly with Valkey without any code changes. However, it is recommended to test the specific client library versions used by the application.

### 7.2 Migration Strategies

**Strategy 1: Replica Promotion (Zero Downtime)**
This is the recommended approach for production environments requiring high availability.
1.  Deploy a new Valkey instance.
2.  Configure the Valkey instance as a replica of the existing Redis primary node using the `REPLICAOF` command.
3.  Wait for the initial synchronization (RDB transfer) to complete and for the replication lag to reach zero.
4.  During a maintenance window, pause application traffic or configure the application to handle a brief interruption.
5.  Execute the `REPLICAOF NO ONE` command on the Valkey instance to promote it to a primary node.
6.  Update the application configuration to point to the new Valkey primary node.
7.  Resume application traffic.

**Strategy 2: Backup and Restore (Downtime Required)**
Suitable for non-critical environments or when network connectivity between the old and new infrastructure is restricted.
1.  Stop application traffic to the Redis instance.
2.  Trigger a manual snapshot using the `BGSAVE` command.
3.  Wait for the snapshot to complete and copy the `dump.rdb` file to the Valkey server.
4.  Start the Valkey server, ensuring it is configured to load the `dump.rdb` file.
5.  Update the application configuration and resume traffic.

### 7.3 Post-Migration Validation

- **Data Integrity:** Verify that key counts and memory usage align between the old Redis instance and the new Valkey instance.
- **Performance Monitoring:** Closely monitor CPU, memory, latency, and throughput metrics. Compare them against historical baselines to ensure performance parity or improvement.
- **Log Analysis:** Review the Valkey server logs for any warnings or errors related to configuration or command compatibility.

## 8. Comprehensive CLI Reference for redis-cli and valkey-cli

The `redis-cli` and `valkey-cli` tools are indispensable utilities for database administrators, site reliability engineers, and technical support specialists.

### 8.1 Core Connectivity and Authentication

```bash
# Connect to a local instance on the default port (6379)
redis-cli

# Connect to a remote instance with a specific port and password
redis-cli -h redis.production.internal -p 6380 -a 'SuperSecretPassword123!'

# Connect using a URI (Redis 6.0+)
redis-cli -u redis://username:password@redis.production.internal:6380/0

# Connect using TLS with a specific certificate and key
redis-cli -h secure-redis.internal -p 6379 --tls \
  --cert /etc/ssl/certs/redis-client.crt \
  --key /etc/ssl/private/redis-client.key \
  --cacert /etc/ssl/certs/ca.crt

# Connect via Unix socket
redis-cli -s /var/run/redis/redis-server.sock
```

### 8.2 Advanced Operational Modes

```bash
# Display continuous statistics every second
redis-cli -h production-db --stat

# Measure continuous latency
redis-cli -h production-db --latency

# Measure latency and record history over time
redis-cli -h production-db --latency-history

# Display a latency distribution spectrum (requires Redis 2.8.13+)
redis-cli -h production-db --latency-dist

# Scan the entire keyspace for large keys (memory intensive)
redis-cli -h production-db --bigkeys

# Scan the keyspace for frequently accessed keys (requires LFU policy)
redis-cli -h production-db --hotkeys

# Stream all commands (use with extreme caution in production)
redis-cli -h production-db MONITOR
```

### 8.3 Advanced One-Liners for Data Manipulation

```bash
# Non-blocking bulk deletion using SCAN and UNLINK (Redis 4.0+)
redis-cli --scan --pattern "session:*" | xargs -L 1000 redis-cli UNLINK

# Export keys matching a pattern to a local file
redis-cli --scan --pattern "config:*" | while read key; do
  echo "SET $key \"$(redis-cli GET $key)\"" >> export.txt
done

# Import data from a file using pipe mode (highly efficient)
cat data.txt | redis-cli --pipe

# Find keys without a TTL (returns -1)
redis-cli --scan | while read key; do
  ttl=$(redis-cli TTL $key)
  if [ $ttl -eq -1 ]; then
    echo "No TTL: $key"
  fi
done > keys_without_ttl.txt
```

### 8.4 Cluster Management and Troubleshooting

```bash
# Check the overall health of the cluster
redis-cli -c -h cluster-node-1 cluster info

# List all nodes, their roles, and slot assignments
redis-cli -c -h cluster-node-1 cluster nodes

# Use the built-in cluster check utility
redis-cli --cluster check cluster-node-1:6379

# Interactively reshard the cluster
redis-cli --cluster reshard cluster-node-1:6379

# Automatically rebalance slots across all nodes
redis-cli --cluster rebalance cluster-node-1:6379 --cluster-use-empty-masters

# Attempt to fix a broken cluster (use with caution)
redis-cli --cluster fix cluster-node-1:6379
```

### 8.5 Memory Management and Optimization

```bash
# Get a high-level overview of memory usage
redis-cli MEMORY STATS

# Analyze the memory usage of a specific key
redis-cli MEMORY USAGE "user:profile:12345"

# Force the allocator to release memory back to the OS (jemalloc only)
redis-cli MEMORY PURGE

# Check the current maxmemory configuration and policy
redis-cli CONFIG GET maxmemory
redis-cli CONFIG GET maxmemory-policy

# Monitor the eviction rate in real-time
redis-cli INFO STATS | grep evicted_keys
```

### 8.6 Worst-Case Scenarios and Incident Response

**The "OOM (Out of Memory)" Scenario:**
1.  Identify Big Keys: `redis-cli --bigkeys`
2.  Check Client Buffers: `redis-cli CLIENT LIST | awk '{print $1, $2, $12}' | sort -k3 -nr | head -n 10`
3.  Kill Problematic Clients: `redis-cli CLIENT KILL id <client_id>`
4.  Emergency Flush (Extreme Caution): `redis-cli FLUSHALL ASYNC`

**The "High CPU Usage" Scenario:**
1.  Check the Slow Log: `redis-cli SLOWLOG GET 10`
2.  Identify Expensive Commands: Look for `KEYS`, `SMEMBERS` on large sets, or complex Lua scripts.
3.  Kill Long-Running Scripts: `redis-cli SCRIPT KILL`

**The "Network Partition / Split Brain" Scenario:**
1.  Verify Replication Status: `redis-cli INFO REPLICATION`
2.  Check Sentinel Logs: Connect to the Sentinel instances and review their logs.
3.  Force a Failover (if necessary): `redis-cli -p 26379 SENTINEL FAILOVER mymaster`

### 8.7 Security and Auditing

```bash
# List all ACL users
redis-cli ACL LIST

# Check the effective permissions of a specific user
redis-cli ACL GETUSER default

# Generate a new secure password
redis-cli ACL GENPASS

# Check if dangerous commands are renamed or disabled
redis-cli CONFIG GET rename-command

# Verify that requirepass is set
redis-cli CONFIG GET requirepass

# Ensure that the server is bound to the correct interfaces
redis-cli CONFIG GET bind
```

## 9. Conclusion

Managing Redis and Valkey in production requires a deep understanding of their internal mechanics, data structures, and operational paradigms. By mastering advanced caching strategies, leveraging Lua scripting safely, understanding the nuances of Pub/Sub and Streams, and proactively mitigating hot keys, technical support and operations teams can ensure the stability, performance, and scalability of these critical infrastructure components. The migration to Valkey represents a strategic shift towards open-source sustainability, and with careful execution, it can be achieved seamlessly, preserving the robust capabilities that organizations rely upon. The `redis-cli` and `valkey-cli` tools are far more than simple query interfaces; they are comprehensive diagnostic and operational suites essential for managing large-scale deployments and rapidly mitigating incidents.
