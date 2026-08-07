# PostgreSQL Reference

Verified against upstream: 2026-08-07

## Architecture
PostgreSQL is an advanced open-source relational database management system (RDBMS). Its architecture is designed around the principles of the client-server model, supporting complex SQL queries, ACID compliance, and extensibility.

- **Process Model**: Multi-process architecture. The postmaster process forks a dedicated backend process for each client connection.
- **Storage Layer**: Organizes data into tablespaces, relations, pages (8KB), and tuples. Uses Write-Ahead Logging (WAL) for durability.
- **Buffer Manager**: Shared buffer pool caches data pages to minimize disk I/O.
- **Query Executor and Planner**: Generates execution plans based on table statistics and available indexes.
- **Concurrency and MVCC**: Uses Multi-Version Concurrency Control (MVCC) to provide concurrent access without locking readers.

## Indexing
PostgreSQL supports a rich variety of index types:
- **B-tree**: Default index type. Efficient for equality and range queries.
- **Hash**: Optimized for equality comparisons.
- **GiST**: Supports extensible data types such as geometric data and full-text search.
- **GIN**: Efficiently indexes composite values such as arrays and JSONB.
- **BRIN**: Lightweight index for very large tables with naturally ordered data.
- **pgvector**: Extension for vector search capabilities, critical for AI integration.

## Query Optimization
- **Statistics and ANALYZE**: The planner relies on table and column statistics collected by the `ANALYZE` command.
- **EXPLAIN and EXPLAIN ANALYZE**: Shows the planned query execution steps and runtime statistics.
- **Join Strategies**: Nested Loop Join, Hash Join, Merge Join.
- **Index Scan Types**: Index Scan, Bitmap Index Scan, Index Only Scan.

## Replication
- **Streaming Replication**: Continuously ships WAL segments from a primary to one or more standby servers.
- **Logical Replication**: Replicates data changes at the SQL level and supports replicating selective tables or data subsets.

## Security
- **Authentication**: Password-based (scram-sha-256), GSSAPI/Kerberos, Peer Authentication, Certificate Authentication.
- **SSL/TLS Encryption**: Supports SSL encryption for client-server communication.
- **Role-Based Access Control (RBAC)**: Granular privilege management.
- **Row-Level Security (RLS)**: Enforces fine-grained access control at the row level.

## Serverless and AI Integration
- **Serverless Deployments**: Best practices for deploying PostgreSQL in serverless and Kubernetes environments.
- **AI Integration**: Utilizing pgvector for vector search and integrating machine learning models directly within the database.
