# MongoDB Reference

Verified against upstream: 2026-08-07

## Architecture
MongoDB is a leading open-source NoSQL document database, optimized for flexible schemas and horizontal scalability.

- **Server Components**: mongod (primary database daemon), mongos (routing service), mongocryptd (client-side encryption).
- **Data Model and Storage**: Stores data as BSON (Binary JSON) documents. Default storage engine is WiredTiger.
- **Concurrency Control**: WiredTiger supports document-level locking, enabling high concurrency.
- **Sharding and Scaling**: Supports horizontal scaling through sharding.

## Indexing
MongoDB indexing is tailored to its document model:
- **Single Field Indexes**: Index on a single document field.
- **Compound Indexes**: Involve multiple fields.
- **Multikey Indexes**: Automatically created when the indexed field is an array.
- **Text Indexes**: Support full-text search over string content.
- **Geospatial Indexes**: Support 2d and 2dsphere indexes for geospatial queries.
- **Vector Search**: Atlas Vector Search for AI integration.

## Query Optimization
- **Explain Plans**: The `explain()` method shows query plan details.
- **Index Intersection**: Can combine multiple single-field indexes to satisfy complex queries.
- **Covered Queries**: Queries that can be answered solely from the index without fetching documents.
- **Aggregation Pipeline Optimization**: Placing `$match` early, using `$project` to limit fields.

## Replication
MongoDB achieves high availability through replica sets.
- **Replica Set Architecture**: Primary (handles writes), Secondaries (replicate data), Arbiters (vote in elections).
- **Automatic Failover**: If the primary fails, an election is triggered to select a new primary.
- **Write Concerns**: Define the level of acknowledgment required for write operations.
- **Read Preferences**: Control how read operations are distributed among replica set members.

## Security
- **Authentication Mechanisms**: SCRAM-SHA-1 / SCRAM-SHA-256, X.509 Certificate Authentication, LDAP Integration, Kerberos Authentication.
- **Role-Based Access Control (RBAC)**: Defines roles granting granular privileges on resources.
- **Network Encryption (TLS/SSL)**: Secures client-server and inter-node communications.
- **Encryption at Rest**: Encrypted Storage Engine with native data encryption on disk.
- **Client-Side Field Level Encryption (CSFLE) / Queryable Encryption**: Enables encryption of sensitive fields on the client side.

## Serverless and AI Integration
- **Serverless Deployments**: Best practices for deploying MongoDB in serverless environments (e.g., MongoDB Atlas Serverless).
- **AI Integration**: Utilizing Atlas Vector Search for building AI-powered applications.
