# Database Engineering

## Table of Contents
1. Schema Design
2. Query Optimization
3. Migrations
4. PostgreSQL
5. NoSQL Databases
6. Caching

---

## 1. Schema Design

### Normalization vs Denormalization

| Normal Form | Rule | Trade-off |
|---|---|---|
| 1NF | Atomic values, no repeating groups | Basic structure |
| 2NF | No partial dependencies | Reduces redundancy |
| 3NF | No transitive dependencies | Minimal redundancy |
| BCNF | Every determinant is a candidate key | Strictest normalization |

**When to denormalize**:
- Read-heavy workloads (>90% reads)
- Expensive joins on frequently accessed data
- Reporting/analytics queries
- Caching computed aggregations

### Data Modeling Patterns

| Pattern | Use Case | Implementation |
|---|---|---|
| Soft deletes | Audit trail, undo | `deleted_at TIMESTAMP NULL` |
| Temporal tables | Historical data, versioning | `valid_from`, `valid_to` columns |
| Polymorphic associations | Multiple parent types | Type column + ID, or separate tables |
| EAV (Entity-Attribute-Value) | Dynamic attributes | Avoid if possible; use JSONB instead |
| Adjacency list | Tree structures | `parent_id` self-reference |
| Materialized path | Tree queries | `/root/parent/child/` path column |
| Closure table | Complex tree operations | Separate ancestor-descendant table |

### Constraints and Integrity

```sql
-- Always use constraints to enforce data integrity at the database level
CREATE TABLE orders (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id),
    status VARCHAR(20) NOT NULL DEFAULT 'pending'
        CHECK (status IN ('pending', 'processing', 'completed', 'cancelled')),
    total_amount DECIMAL(10,2) NOT NULL CHECK (total_amount >= 0),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Partial unique index for business rules
CREATE UNIQUE INDEX idx_one_active_subscription_per_user
    ON subscriptions (user_id)
    WHERE status = 'active';
```

---

## 2. Query Optimization

### EXPLAIN ANALYZE Workflow

1. Run `EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT)` on the slow query
2. Look for: Sequential scans on large tables, nested loops with high row counts, sort operations on large sets
3. Identify the most expensive node (highest actual time)
4. Apply appropriate fix (index, rewrite, materialized view)
5. Re-run EXPLAIN to verify improvement

### Index Strategy

| Index Type | Use Case | PostgreSQL Syntax |
|---|---|---|
| B-tree (default) | Equality, range, sorting | `CREATE INDEX idx ON t(col)` |
| Hash | Equality only | `CREATE INDEX idx ON t USING hash(col)` |
| GIN | Full-text, JSONB, arrays | `CREATE INDEX idx ON t USING gin(col)` |
| GiST | Geometric, range types | `CREATE INDEX idx ON t USING gist(col)` |
| BRIN | Large sorted tables | `CREATE INDEX idx ON t USING brin(col)` |
| Partial | Subset of rows | `CREATE INDEX idx ON t(col) WHERE condition` |
| Covering | Include non-key columns | `CREATE INDEX idx ON t(col) INCLUDE (other)` |

### Common Anti-Patterns

| Anti-Pattern | Problem | Solution |
|---|---|---|
| SELECT * | Fetches unnecessary data | Select only needed columns |
| N+1 queries | Multiple round trips | JOIN or batch query |
| Missing indexes | Full table scans | Add targeted indexes |
| Over-indexing | Slow writes, wasted space | Remove unused indexes |
| Implicit type casts | Index not used | Match types exactly |
| Functions on indexed columns | Index not used | Create functional index |
| OFFSET pagination | Scans skipped rows | Use keyset pagination |

### Query Rewriting Techniques

```sql
-- Instead of correlated subquery:
SELECT * FROM orders WHERE user_id IN (SELECT id FROM users WHERE active = true);

-- Use JOIN:
SELECT o.* FROM orders o JOIN users u ON o.user_id = u.id WHERE u.active = true;

-- Instead of OFFSET pagination:
SELECT * FROM orders WHERE id > :last_seen_id ORDER BY id LIMIT 20;

-- Instead of counting for existence:
SELECT EXISTS (SELECT 1 FROM orders WHERE user_id = :id AND status = 'pending');
```

---

## 3. Migrations

### Migration Best Practices

- Every migration must be reversible (write both up and down)
- Test migrations on a copy of production data before deploying
- Never drop columns in the same deployment as code changes
- Break large data migrations into batches
- Add indexes concurrently (`CREATE INDEX CONCURRENTLY`)
- Use advisory locks to prevent concurrent migrations

### Safe Migration Patterns

| Operation | Unsafe | Safe |
|---|---|---|
| Add column | With NOT NULL + no default | Add nullable, backfill, add constraint |
| Remove column | Drop in same deploy | Stop reading → deploy → drop |
| Rename column | Direct rename | Add new → copy data → drop old |
| Add index | `CREATE INDEX` (locks) | `CREATE INDEX CONCURRENTLY` |
| Change type | `ALTER COLUMN TYPE` | Add new column → migrate → swap |

### Large Table Migrations

```sql
-- Batch update pattern for large tables
DO $$
DECLARE
    batch_size INT := 10000;
    affected INT;
BEGIN
    LOOP
        UPDATE large_table
        SET new_column = compute_value(old_column)
        WHERE id IN (
            SELECT id FROM large_table
            WHERE new_column IS NULL
            LIMIT batch_size
            FOR UPDATE SKIP LOCKED
        );
        GET DIAGNOSTICS affected = ROW_COUNT;
        EXIT WHEN affected = 0;
        COMMIT;
        PERFORM pg_sleep(0.1); -- Reduce load
    END LOOP;
END $$;
```

---

## 4. PostgreSQL

### PostgreSQL-Specific Features

| Feature | Use Case | Example |
|---|---|---|
| JSONB | Semi-structured data | `data JSONB`, GIN index |
| Arrays | Multi-value columns | `tags TEXT[]` |
| CTEs | Readable complex queries | `WITH cte AS (...)` |
| Window functions | Analytics, ranking | `ROW_NUMBER() OVER (...)` |
| Partitioning | Very large tables | Range, list, hash partitioning |
| Logical replication | Selective replication | Pub/sub between databases |
| pg_stat_statements | Query performance | Track slow queries |
| LISTEN/NOTIFY | Real-time events | Lightweight pub/sub |

### Connection Pooling

| Tool | Type | Best For |
|---|---|---|
| PgBouncer | External pooler | Most deployments |
| pgpool-II | Pooler + load balancer | Read replicas |
| Built-in (application) | Application-level | Simple setups |

**Configuration**:
- Transaction mode: Best for most applications (releases connection after transaction)
- Session mode: Required for prepared statements, temp tables
- Pool size: Start with `(2 * CPU cores) + effective_spindle_count` per database

### Backup and Recovery

- **pg_dump**: Logical backup (portable, slow for large DBs)
- **pg_basebackup**: Physical backup (fast, point-in-time recovery)
- **WAL archiving**: Continuous archiving for PITR
- **Barman/pgBackRest**: Production backup management tools

---

## 5. NoSQL Databases

### MongoDB

- Document model: Embed related data for read performance
- Schema validation: Use JSON Schema for data integrity
- Indexing: Compound indexes follow ESR rule (Equality, Sort, Range)
- Aggregation pipeline: Powerful data transformation framework
- Sharding: Hash-based or range-based distribution

### Redis

| Data Structure | Use Case | Commands |
|---|---|---|
| Strings | Cache, counters, flags | GET, SET, INCR |
| Hashes | Objects, user profiles | HGET, HSET, HMGET |
| Lists | Queues, activity feeds | LPUSH, RPOP, LRANGE |
| Sets | Tags, unique items | SADD, SMEMBERS, SINTER |
| Sorted Sets | Leaderboards, scheduling | ZADD, ZRANGE, ZRANGEBYSCORE |
| Streams | Event logs, messaging | XADD, XREAD, XREADGROUP |

### DynamoDB

- Design for access patterns first (single-table design)
- Use composite keys (PK + SK) for flexible queries
- GSI for alternative access patterns
- Use DynamoDB Streams for CDC
- Implement TTL for automatic data expiration

---

## 6. Caching

### Redis Caching Patterns

```python
# Cache-aside pattern
def get_user(user_id):
    # Try cache first
    cached = redis.get(f"user:{user_id}")
    if cached:
        return json.loads(cached)
    
    # Cache miss: query database
    user = db.query("SELECT * FROM users WHERE id = %s", user_id)
    
    # Store in cache with TTL
    redis.setex(f"user:{user_id}", 3600, json.dumps(user))
    return user

# Cache invalidation on write
def update_user(user_id, data):
    db.execute("UPDATE users SET ... WHERE id = %s", user_id)
    redis.delete(f"user:{user_id}")  # Invalidate cache
```

### Cache Stampede Prevention

- **Mutex/lock**: Only one request refreshes cache, others wait
- **Early expiration**: Refresh before actual expiry (background refresh)
- **Probabilistic early expiration**: Random early refresh to distribute load
- **Stale-while-revalidate**: Serve stale data while refreshing in background
