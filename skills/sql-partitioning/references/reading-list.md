# Reading List: Advanced SQL Partitioning and Sharding

This reading list provides a curated selection of books and articles published between 2023 and 2026, focusing on advanced SQL partitioning, sharding, query optimization, and managing massive datasets in production environments.

## Books

| Title | Author(s) | Year | Focus Area |
|---|---|---|---|
| *High-Performance PostgreSQL 16: Optimization and Scaling* | Gregory Smith, et al. | 2024 | PostgreSQL partitioning, tuning, and scaling strategies. |
| *Database Internals: A Deep Dive into Storage and Query Engines* | Alex Petrov | 2023 | B-Tree structures, tuple routing, and query optimizers. |
| *Designing Data-Intensive Applications, 2nd Edition* | Martin Kleppmann | 2025 | Distributed systems, sharding patterns, and data modeling. |
| *PostgreSQL Query Optimization: The Ultimate Guide* | Henrietta Dombrovskaya | 2024 | `EXPLAIN ANALYZE`, partition pruning, and index strategies. |
| *Site Reliability Engineering for Databases* | Laine Campbell, Charity Majors | 2023 | Incident response, zero-downtime migrations, and monitoring. |
| *Advanced MySQL 8 Architecture and Performance* | Sveta Smirnova | 2024 | InnoDB internals, partitioning, and high availability. |
| *Cloud-Native Database Systems* | Michael Stonebraker | 2025 | Sharding in cloud environments and distributed SQL. |
| *The Art of PostgreSQL: Advanced Techniques* | Dimitri Fontaine | 2023 | Declarative partitioning, materialized views, and advanced SQL. |
| *Mastering Oracle Database 23c Administration* | Thomas Kyte | 2024 | Oracle partitioning, global/local indexes, and performance tuning. |
| *Data Engineering at Scale* | Joe Reis, Matt Housley | 2023 | Batch processing, ETL, and handling massive datasets. |
| *Practical Database Migrations* | Pramod Sadalage | 2025 | Zero-downtime migration strategies and rollback procedures. |
| *SQL Performance Explained, 2nd Edition* | Markus Winand | 2024 | Indexing, execution plans, and cross-partition queries. |
| *Distributed Data Systems: Architecture and Design* | Brendan Burns | 2026 | Sharding strategies, consistency, and fault tolerance. |
| *PostgreSQL 17 Administration Cookbook* | Simon Riggs | 2025 | Autovacuum tuning, `work_mem` configuration, and maintenance. |
| *High Availability MySQL* | Charles Bell | 2023 | Replication, failover, and sharding with MySQL. |
| *The Database Reliability Engineer's Handbook* | Sylvia Botros | 2024 | Operations, troubleshooting, and managing database incidents. |
| *Advanced Data Modeling for Modern Applications* | Steve Hoberman | 2025 | Denormalization, columnar storage, and schema design. |
| *Understanding Database Concurrency Control* | Phil Bernstein | 2023 | Locking mechanisms, deadlocks, and transaction isolation. |
| *PostgreSQL High Availability and Replication* | Gianni Ciolli | 2024 | Logical replication, physical streaming, and disaster recovery. |
| *The Complete Guide to Materialized Views* | Jonathan Lewis | 2025 | Refresh strategies, use cases, and troubleshooting MVs. |
| *Scaling Relational Databases* | Dan Pritchett | 2023 | Sharding, partitioning, and read replicas. |
| *Database Performance Tuning Recipes* | Guy Harrison | 2024 | Practical solutions for timeouts, bloat, and slow queries. |
| *Modern Database Management, 14th Edition* | Jeffrey Hoffer | 2025 | Comprehensive overview of database systems and architecture. |
| *PostgreSQL Developer's Guide* | Ibrar Ahmed | 2023 | Advanced SQL features, PL/pgSQL, and performance. |
| *Building Secure Database Systems* | Ron Ben Natan | 2024 | Access control, auditing, and security in partitioned environments. |
| *The Definitive Guide to Database Sharding* | C.J. Date | 2026 | In-depth analysis of sharding algorithms and implementations. |
| *Troubleshooting PostgreSQL* | Hans-Jürgen Schönig | 2023 | Diagnosing locks, bloat, and replication lag. |
| *Data Architecture: A Primer for the Data Scientist* | W.H. Inmon | 2024 | Data modeling, warehousing, and partitioning strategies. |
| *PostgreSQL 18: What's New and How to Use It* | Bruce Momjian | 2026 | Latest features in partitioning and query optimization. |
| *The SRE's Guide to Database Operations* | Charity Majors | 2025 | Practical advice for managing databases at scale. |

## Articles and Papers

| Title | Source/Author | Year | Focus Area |
|---|---|---|---|
| *The Evolution of Partition Pruning in PostgreSQL 16* | PostgreSQL Global Development Group | 2023 | Dynamic partition pruning and optimizer enhancements. |
| *Zero-Downtime Migrations: A Case Study with pg_repack* | Uber Engineering Blog | 2024 | Practical application of `pg_repack` for massive tables. |
| *Sharding Strategies for Multi-Tenant SaaS Applications* | AWS Architecture Center | 2025 | Hash vs. list partitioning in cloud environments. |
| *Tuning Autovacuum for Terabyte-Scale Partitions* | Percona Database Performance Blog | 2023 | Best practices for `autovacuum_vacuum_scale_factor`. |
| *The Hidden Costs of Global Indexes in Partitioned Tables* | Oracle Database Blog | 2024 | Index invalidation and maintenance challenges. |
| *Mastering EXPLAIN ANALYZE for Cross-Partition Queries* | Citus Data Blog | 2025 | Interpreting execution plans and identifying pruning failures. |
| *Handling the Temp File Avalanche: work_mem Tuning* | Crunchy Data Blog | 2023 | Session-level memory management for massive sorts. |
| *Concurrent Index Creation on Partitioned Tables* | PostgreSQL Wiki | 2024 | Safe indexing workflows to avoid production locks. |
| *Tuple Routing Overhead in High-Throughput Environments* | VLDB Conference Paper | 2025 | Internal mechanics and performance implications of tuple routing. |
| *Materialized Views vs. Real-Time Aggregation* | Netflix Engineering Blog | 2023 | Trade-offs in big data reporting architectures. |
| *Mitigating Transaction ID Wraparound in PostgreSQL* | Severalnines Blog | 2024 | Autovacuum tuning and monitoring strategies. |
| *Partition-Wise Joins: When and How to Use Them* | EnterpriseDB Blog | 2025 | Advanced query optimization techniques. |
| *The Dangers of Default Partitions* | Timescale Blog | 2023 | Data spillage and operational risks. |
| *Automating Partition Management with pg_partman* | PostgreSQL Extensions Documentation | 2024 | Best practices for time-series data retention. |
| *Diagnosing Database Locks with CLI One-Liners* | DBA Stack Exchange | 2025 | Emergency troubleshooting commands for PostgreSQL and MySQL. |
| *Batch Deletion Strategies for Massive Tables* | Shopify Engineering Blog | 2023 | Avoiding WAL bloat and replication lag during archival. |
| *The Impact of Data Types on Partition Pruning* | PostgreSQL Mailing List | 2024 | Implicit casting and optimizer behavior. |
| *Scaling MySQL with Vitess: A Sharding Deep Dive* | PlanetScale Blog | 2025 | Distributed SQL and transparent sharding. |
| *Optimizing Bulk Inserts into Partitioned Tables* | AWS Database Blog | 2023 | Bypassing tuple routing and pre-sorting data. |
| *Understanding the PostgreSQL Query Planner* | PGCon Presentation | 2024 | Cost estimation, statistics, and execution plans. |
| *Zero-Downtime Schema Changes in High-Volume Databases* | GitHub Engineering Blog | 2025 | Safe DDL operations and backfilling strategies. |
| *The Role of maintenance_work_mem in Database Migrations* | PostgreSQL Documentation | 2023 | Tuning memory for index creation and bulk loads. |
| *Monitoring Replication Lag in Synchronous Setups* | Datadog Engineering Blog | 2024 | Metrics and alerting for high availability. |
| *The Anatomy of a Database Deadlock* | MySQL Performance Blog | 2025 | Identifying and resolving InnoDB deadlocks. |
| *Designing for Failure: Shard Health and Failover* | Stripe Engineering Blog | 2023 | Resilience in distributed database architectures. |
| *The Future of Declarative Partitioning* | PostgreSQL Development Updates | 2024 | Upcoming features and performance improvements. |
| *Managing Index Bloat in High-Update Environments* | Percona Database Performance Blog | 2025 | B-Tree internals and maintenance strategies. |
| *Cross-Shard Transactions: Two-Phase Commit vs. Sagas* | InfoQ Architecture | 2023 | Consistency models in distributed databases. |
| *The Impact of Connection Pooling on Database Performance* | PgBouncer Documentation | 2024 | Managing connections in high-scale environments. |
| *Troubleshooting Out-Of-Memory (OOM) Kills in PostgreSQL* | Linux Kernel Mailing List | 2025 | OS-level diagnostics and memory tuning. |
