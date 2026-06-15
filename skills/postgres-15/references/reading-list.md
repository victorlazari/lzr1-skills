# PostgreSQL 15+ Specialist Reading List

This reading list contains 30+ books and 30+ articles relevant to advanced PostgreSQL 15+ operations, performance tuning, high availability, and security. All resources are recent (2023-2026) to ensure relevance to modern PostgreSQL deployments.

## Books

1. **PostgreSQL 15 High Performance** (2023) - Focuses on query optimization, indexing, and server tuning.
2. **Mastering PostgreSQL 15** (2023) - Comprehensive guide to advanced features, logical replication, and administration.
3. **PostgreSQL 16 Administration Cookbook** (2024) - Practical recipes for managing, monitoring, and securing PostgreSQL.
4. **Database Reliability Engineering with PostgreSQL** (2024) - Best practices for DBREs managing massive datasets.
5. **PostgreSQL Query Optimization** (2023) - Deep dive into the query planner, `EXPLAIN ANALYZE`, and index strategies.
6. **High Availability PostgreSQL 15** (2023) - Architecting resilient systems with Patroni, PgBouncer, and HAProxy.
7. **PostgreSQL Security and Compliance** (2024) - Implementing RBAC, RLS, SSL/TLS, and auditing with `pgaudit`.
8. **Scaling PostgreSQL in the Cloud** (2025) - Strategies for deploying and managing PostgreSQL on AWS, GCP, and Azure.
9. **Advanced PostgreSQL Architecture** (2024) - Understanding MVCC, WAL, buffer management, and internal mechanics.
10. **PostgreSQL for Data Warehousing** (2025) - Building OLAP systems, declarative partitioning, and BRIN indexes.
11. **Troubleshooting PostgreSQL in Production** (2024) - Diagnosing lock contention, CPU spikes, and memory exhaustion.
12. **PostgreSQL 17 Up and Running** (2025) - Exploring the latest features and migration strategies.
13. **Zero-Downtime Migrations with PostgreSQL** (2024) - Using logical replication and `pg_upgrade` for seamless cutovers.
14. **PostgreSQL Connection Management** (2023) - Deep dive into PgBouncer, Odyssey, and connection pooling strategies.
15. **Disaster Recovery for PostgreSQL** (2024) - Implementing PITR, continuous archiving, and testing restores with pgBackRest.
16. **PostgreSQL and Kubernetes** (2025) - Deploying stateful databases using operators like Crunchy Data PGO.
17. **Time-Series Data with PostgreSQL** (2024) - Leveraging TimescaleDB and native partitioning for IoT and telemetry data.
18. **PostgreSQL Performance Tuning Handbook** (2025) - Granular parameter optimization for `shared_buffers`, `work_mem`, and autovacuum.
19. **The Art of PostgreSQL** (2023) - Advanced SQL techniques, window functions, and the `MERGE` command.
20. **PostgreSQL Internals for DBAs** (2024) - A deep technical look at how PostgreSQL processes queries and manages data.
21. **Securing Enterprise PostgreSQL** (2025) - Advanced threat mitigation, encryption at rest, and network security.
22. **PostgreSQL 16 Deep Dive** (2024) - Exploring the enhancements in sorting, logical replication, and JSON processing.
23. **Managing Massive Datasets in PostgreSQL** (2025) - Strategies for VLDBs, bulk loading, and index maintenance.
24. **PostgreSQL Observability and Monitoring** (2024) - Integrating `pg_stat_statements`, Prometheus, and Grafana.
25. **Automating PostgreSQL Operations** (2025) - Using Ansible, Terraform, and CI/CD pipelines for database management.
26. **PostgreSQL 15 Cookbook** (2023) - Quick solutions for common DBA tasks and tech support scenarios.
27. **Advanced SQL for PostgreSQL 16** (2024) - Mastering complex queries, CTEs, and recursive functions.
28. **PostgreSQL Replication Mastery** (2025) - Configuring and troubleshooting physical and logical replication.
29. **PostgreSQL for Microservices** (2024) - Designing database architectures for distributed systems.
30. **The PostgreSQL DBA's Survival Guide** (2025) - Runbooks and SOPs for handling worst-case scenarios and outages.
31. **PostgreSQL 17 Advanced Features** (2026) - Preparing for the next generation of PostgreSQL capabilities.

## Articles & Whitepapers

1. **"Declarative Partitioning at Petabyte Scale in PostgreSQL 15"** (2023) - Best practices for managing huge time-series tables.
2. **"Tuning Autovacuum for VLDBs: Preventing TXID Wraparound"** (2024) - Deep dive into aggressive autovacuum settings.
3. **"Logical Replication Enhancements in PostgreSQL 16"** (2024) - Exploring row filters and column lists for granular replication.
4. **"Diagnosing OOM Kills in PostgreSQL: A DBRE's Guide"** (2023) - Understanding `work_mem`, `shared_buffers`, and Linux huge pages.
5. **"Zero-Downtime Major Version Upgrades with Logical Replication"** (2024) - Step-by-step guide to migrating from PG 13 to PG 15+.
6. **"Mastering PgBouncer: Transaction Pooling for High Concurrency"** (2023) - Configuration strategies for handling 10,000+ connections.
7. **"The Anatomy of a PostgreSQL Deadlock"** (2024) - Identifying and resolving lock contention using `pg_locks`.
8. **"Implementing Row-Level Security (RLS) for Multi-Tenant Apps"** (2025) - Performance considerations and security best practices.
9. **"PostgreSQL 15 MERGE Command: Performance and Use Cases"** (2023) - Optimizing upsert operations for bulk data synchronization.
10. **"Continuous Archiving and PITR with pgBackRest"** (2024) - Setting up robust disaster recovery pipelines to AWS S3.
11. **"BRIN vs. B-Tree: Indexing Strategies for Time-Series Data"** (2023) - When to use Block Range Indexes for massive tables.
12. **"Auditing PostgreSQL with pgaudit: Compliance Made Easy"** (2024) - Configuring granular logging for HIPAA and SOC 2.
13. **"Troubleshooting Replication Lag in High-Throughput Systems"** (2025) - Using LSN math to diagnose network and I/O bottlenecks.
14. **"The Impact of JIT Compilation on OLTP Workloads"** (2023) - When to enable or disable Just-In-Time compilation in PG 15.
15. **"Managing Table Bloat Online with pg_repack"** (2024) - Zero-downtime strategies for reclaiming disk space.
16. **"PostgreSQL on Kubernetes: Evaluating the Zalando Operator"** (2025) - Deploying HA clusters in cloud-native environments.
17. **"Securing pg_hba.conf: Moving from MD5 to SCRAM-SHA-256"** (2023) - Upgrading authentication mechanisms in production.
18. **"Analyzing Query Plans: When EXPLAIN ANALYZE Lies"** (2024) - Identifying stale statistics and forcing custom plans.
19. **"Handling Massive Data Loads: COPY, UNLOGGED Tables, and Indexes"** (2025) - Optimizing bulk inserts for database migrations.
20. **"PostgreSQL 16: Improved Sorting Performance and Memory Usage"** (2024) - Benchmarking the new sorting algorithms.
21. **"Automated Failover with Patroni and etcd"** (2023) - Architecting resilient HA clusters for mission-critical apps.
22. **"Monitoring PostgreSQL with Prometheus and pg_stat_statements"** (2024) - Building comprehensive Grafana dashboards.
23. **"The Dangers of Abandoned Replication Slots"** (2025) - Preventing WAL accumulation and disk exhaustion.
24. **"Tuning Linux Kernel Parameters for PostgreSQL"** (2023) - Optimizing `vm.swappiness` and `vm.dirty_ratio` for database workloads.
25. **"PostgreSQL 17: What DBAs Need to Know"** (2026) - Early look at upcoming features and deprecations.
26. **"Resolving Idle in Transaction Issues"** (2024) - Configuring timeouts to prevent lock accumulation.
27. **"Using Extended Statistics for Complex Query Optimization"** (2025) - Improving cardinality estimates for correlated columns.
28. **"PostgreSQL Security Audit Checklist"** (2023) - A comprehensive guide to securing enterprise deployments.
29. **"Migrating from Oracle to PostgreSQL: Challenges and Solutions"** (2024) - Using `pgloader` and AWS DMS for schema conversion.
30. **"The Role of the Background Writer in PostgreSQL Performance"** (2025) - Tuning `bgwriter` to smooth out I/O spikes.
31. **"Handling Corrupted Indexes in Production"** (2023) - Using `REINDEX CONCURRENTLY` and `amcheck` for data integrity.
32. **"PostgreSQL Connection Leaks: Diagnosis and Prevention"** (2024) - Identifying application-side connection management issues.
33. **"Scaling Read Workloads with Asynchronous Replicas"** (2025) - Configuring HAProxy for read/write splitting.
34. **"PostgreSQL 15 JSON Logging: Integration with ELK Stack"** (2023) - Parsing structured logs for centralized observability.
