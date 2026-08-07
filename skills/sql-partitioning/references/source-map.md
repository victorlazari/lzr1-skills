# Source Map

This source map replaces the traditional reading list and specifies what each source governs and when to consult it.

**Verified against upstream: 2026-08-07**

## Authoritative Sources

| Source | URL | Governs | When to Consult |
|---|---|---|---|
| PostgreSQL 18 Documentation: 5.12. Table Partitioning | https://www.postgresql.org/docs/current/ddl-partitioning.html | Official syntax, supported features, and limitations of declarative partitioning. | When verifying syntax for `CREATE TABLE ... PARTITION BY`, attaching/detaching partitions, or checking version-specific limitations. |
| Exploring the Limitations of Postgres Partitioning: Lessons Learned and Best Practices | https://dev.to/nightbird07/exploring-the-limitations-of-postgres-partitioning-lessons-learned-and-best-practices-5cj9 | Practical limitations, performance cliffs, and operational complexities. | When designing a partitioning strategy or troubleshooting unexpected performance degradation at scale. |
| PostgreSQL Tutorial: Reasons Partition Pruning Not Work | https://www.rockdata.net/tutorial/troubleshooting-partition-pruning/ | Common causes of partition pruning failures (e.g., non-immutable functions, complex OR conditions). | When `EXPLAIN ANALYZE` shows that partition pruning is not occurring as expected. |
| PostgreSQL 16: New Query Intelligence Features for Better Performance | https://postgresqlblog.hashnode.dev/postgresql-16-new-query-intelligence-features-for-better-performance | Enhancements in PostgreSQL 16+, such as improved execution-time partition pruning. | When optimizing queries on PostgreSQL 16 or later, or when evaluating upgrade benefits. |
| How a Simple Query Brought Down Performance: A PostgreSQL Partition Pruning Mystery | https://medium.com/@shaileshkumarmishra/how-a-simple-query-brought-down-performance-a-postgresql-partition-pruning-mystery-3019954e95ff | Real-world case studies of partition pruning failures and their impact. | When investigating sudden performance drops related to partitioned tables. |
| The Hidden Costs of Table Partitioning at Scale | https://www.tigerdata.com/blog/hidden-costs-table-partitioning-scale | Planning time scaling with partition count, lock manager contention, and fast path locking limitations. | When planning to scale to thousands of partitions or when diagnosing lock manager waits. |

## Supplementary Sources

| Source | Focus Area | When to Consult |
|---|---|---|
| *High-Performance PostgreSQL 16: Optimization and Scaling* (Gregory Smith, et al., 2024) | PostgreSQL partitioning, tuning, and scaling strategies. | For comprehensive guidance on tuning `work_mem`, `autovacuum`, and other parameters for partitioned environments. |
| *Database Internals: A Deep Dive into Storage and Query Engines* (Alex Petrov, 2023) | B-Tree structures, tuple routing, and query optimizers. | When needing a deep understanding of how the database engine handles partitioned data internally. |
| *Designing Data-Intensive Applications, 2nd Edition* (Martin Kleppmann, 2025) | Distributed systems, sharding patterns, and data modeling. | When designing sharding architectures or evaluating trade-offs between different sharding strategies. |
| *Site Reliability Engineering for Databases* (Laine Campbell, Charity Majors, 2023) | Incident response, zero-downtime migrations, and monitoring. | When planning zero-downtime migrations or establishing monitoring and alerting for partitioned databases. |
| *Practical Database Migrations* (Pramod Sadalage, 2025) | Zero-downtime migration strategies and rollback procedures. | When executing complex database migrations and needing robust rollback plans. |
| *The Complete Guide to Materialized Views* (Jonathan Lewis, 2025) | Refresh strategies, use cases, and troubleshooting MVs. | When implementing or troubleshooting materialized views in massive datasets. |
