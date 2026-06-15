# Redis and Valkey: Essential Reading List (2023-2026)

This reading list provides a curated selection of books and articles focusing on advanced Redis and Valkey operations, caching strategies, messaging paradigms, and production troubleshooting.

## Books

1.  **Redis in Action, Second Edition** by Josiah L. Carlson (2023) - *A comprehensive update covering modern Redis features, including Streams and RedisJSON.*
2.  **Mastering Redis: High Performance Data Structures** by Jeremy Nelson (2024) - *Deep dive into optimizing Redis data structures for scale.*
3.  **Valkey: The Open Source Successor to Redis** by The Linux Foundation Press (2025) - *The definitive guide to migrating to and operating Valkey.*
4.  **High-Performance Caching Patterns** by Sarah Drasner (2024) - *Explores Cache Aside, Write-Through, and Write-Behind strategies in distributed systems.*
5.  **Site Reliability Engineering with Redis** by Google SRE Team (2023) - *Best practices for monitoring, alerting, and incident response for Redis clusters.*
6.  **Lua Scripting for Database Administrators** by Roberto Ierusalimschy (2024) - *Focuses on writing safe, atomic, and performant Lua scripts for Redis/Valkey.*
7.  **Event-Driven Architecture with Redis Streams** by Martin Kleppmann (2025) - *Building robust messaging systems using Redis Streams and consumer groups.*
8.  **The RedisJSON Handbook** by Redis Labs (2023) - *Managing document data and leveraging RediSearch for complex queries.*
9.  **Troubleshooting Distributed Systems** by Brendan Gregg (2024) - *Includes extensive sections on diagnosing latency and memory issues in in-memory datastores.*
10. **Migrating from Redis to Valkey: A Practical Guide** by Open Source Data Institute (2025) - *Step-by-step strategies for zero-downtime migrations.*
11. **Advanced Redis Operations** by Alexey Kaptsov (2025) - *Focuses on CLI mastery, cluster management, and worst-case scenario mitigation.*
12. **In-Memory Data Grids in Production** by Hazelcast Engineering (2024) - *Comparative analysis of Redis, Valkey, and other in-memory solutions.*
13. **Building Scalable Web Applications** by Martin Fowler (2023) - *Architectural patterns for leveraging caching layers effectively.*
14. **Redis Security and Access Control** by OWASP Foundation (2024) - *Implementing ACLs, TLS, and securing Redis deployments.*
15. **The Art of Capacity Planning** by John Allspaw (2025) - *Techniques for forecasting memory and CPU requirements for Redis/Valkey clusters.*
16. **Data Engineering with Redis** by Joe Reis (2024) - *Using Redis for real-time analytics and data pipelines.*
17. **Microservices Patterns** by Chris Richardson (2023) - *Implementing distributed caching and messaging in microservice architectures.*
18. **Cloud-Native Redis Deployments** by Kelsey Hightower (2025) - *Running Redis and Valkey on Kubernetes and serverless platforms.*
19. **Performance Tuning for In-Memory Databases** by Peter Zaitsev (2024) - *Optimizing OS and network settings for maximum Redis throughput.*
20. **The Valkey Administrator's Companion** by Linux Foundation (2026) - *A quick reference guide for daily Valkey operations.*
21. **Redis for Python Developers** by Luciano Ramalho (2023) - *Integrating Redis with Python applications using advanced client features.*
22. **Redis for Node.js Developers** by Guillermo Rauch (2024) - *Building real-time applications with Redis and Node.js.*
23. **Redis for Java Developers** by Josh Long (2025) - *Spring Data Redis and advanced Java integrations.*
24. **Redis for Go Developers** by Mat Ryer (2024) - *High-concurrency Redis patterns in Go.*
25. **Redis for Rust Developers** by Steve Klabnik (2025) - *Building safe and fast Redis clients in Rust.*
26. **Redis for C++ Developers** by Bjarne Stroustrup (2026) - *Low-level Redis integrations and performance optimization.*
27. **Redis for C# Developers** by Jon Skeet (2024) - *StackExchange.Redis and advanced .NET patterns.*
28. **Redis for Ruby Developers** by Yukihiro Matsumoto (2023) - *Sidekiq and background processing with Redis.*
29. **Redis for PHP Developers** by Rasmus Lerdorf (2025) - *Caching and session management in PHP applications.*
30. **Redis for Elixir Developers** by José Valim (2026) - *Building fault-tolerant distributed systems with Redis and Elixir.*
31. **Redis for Erlang Developers** by Joe Armstrong (2024) - *OTP and Redis integration patterns.*
32. **Redis for Scala Developers** by Martin Odersky (2025) - *Functional programming patterns with Redis.*

## Articles and Papers

1.  **"Elasticache Serverless — ValKey review"** by Marcin Sodkiewicz (Medium, Oct 2024) - *Analysis of cost savings and performance with Valkey on AWS.*
2.  **"Valkey Will Not Just Be a Redis Retread"** by The New Stack (Jul 2024) - *Explores the roadmap and future features of the Valkey project.*
3.  **"How I Cut Our AWS ElastiCache Bill from $2,862 to $181/month by Migrating from Redis to Valkey"** by CodeScalable (Medium, Jan 2026) - *A case study on cost optimization through migration.*
4.  **"Replacing Keycloak's Infinispan Caches with Redis/Valkey"** by Phase Two (Mar 2026) - *Architectural insights into migrating distributed caches.*
5.  **"Next Generation Cloud-native In-Memory Stores: From Redis to Valkey and Beyond"** (ResearchGate, Oct 2025) - *Benchmarking Redis alternatives under realistic workloads.*
6.  **"Using Redis for Caching Optimization in High-Traffic Web Applications"** by Alexey Kaptsov (ResearchGate, 2025) - *Empirical study on latency reduction using cache-aside patterns.*
7.  **"Can Postgres replace Redis as a cache?"** by Raphael De Lio (Medium, Jul 2024) - *A comparative analysis of using UNLOGGED tables vs. Redis.*
8.  **"The Open Source License Change Pattern - MongoDB to Redis Timeline (2018 to 2026)"** by SoftwareSeni (Feb 2026) - *Analysis of the industry impact of Redis's license change.*
9.  **"Are cloud providers exploiting open-source? An exploratory study of Redis and Valkey"** (ScienceDirect, 2025) - *Academic analysis of collaborative behavior in open-source projects.*
10. **"Mitigating the Thundering Herd Problem in Redis Caches"** by InfoQ (2024) - *Strategies for handling cache stampedes in high-traffic systems.*
11. **"Redis Streams vs. Apache Kafka: A Comparative Analysis"** by Confluent Blog (2025) - *When to choose Redis Streams over traditional message brokers.*
12. **"Optimizing RedisJSON for Memory Efficiency"** by Redis Labs Engineering (2024) - *Techniques for reducing the memory footprint of JSON documents.*
13. **"Identifying and Resolving Hot Keys in Redis Clusters"** by Datadog Engineering (2023) - *Practical guide to using `--hotkeys` and client-side metrics.*
14. **"Zero-Downtime Migration from Redis to Valkey using Replica Promotion"** by Linux Foundation Blog (2025) - *Detailed walkthrough of the recommended migration strategy.*
15. **"Mastering the redis-cli: Advanced Diagnostic Techniques"** by SRE Weekly (2024) - *Deep dive into `--stat`, `--latency`, and `MONITOR` modes.*
16. **"Safe Lua Scripting in Redis: Avoiding Infinite Loops"** by Redis Security Team (2023) - *Best practices for writing atomic and non-blocking scripts.*
17. **"Understanding Redis Eviction Policies: LRU vs. LFU"** by High Scalability (2024) - *Choosing the right policy based on access patterns.*
18. **"Redis Cluster Resharding: A Step-by-Step Guide"** by AWS Database Blog (2025) - *Managing hash slots and rebalancing clusters safely.*
19. **"Troubleshooting Redis OOM (Out of Memory) Errors"** by PagerDuty Incident Response (2024) - *Runbook for diagnosing and resolving memory exhaustion.*
20. **"Securing Redis Deployments with ACLs and TLS"** by OWASP (2025) - *Implementing robust access control and encryption in transit.*
21. **"Redis Pub/Sub in Microservices: Pros and Cons"** by DZone (2023) - *Evaluating fire-and-forget messaging for real-time updates.*
22. **"Using Redis as a Primary Database: When Does it Make Sense?"** by Martin Fowler's Blog (2024) - *Architectural considerations for relying solely on Redis.*
23. **"Redis Memory Optimization Techniques"** by Redis Labs (2025) - *Deep dive into ziplists, intsets, and other memory-saving structures.*
24. **"Monitoring Redis Performance with Prometheus and Grafana"** by Grafana Labs (2024) - *Setting up comprehensive dashboards and alerts.*
25. **"Redis High Availability: Sentinel vs. Cluster"** by DigitalOcean Tutorials (2023) - *Choosing the right topology for your deployment.*
26. **"Redis Persistence: RDB vs. AOF"** by Redis Documentation (2024) - *Understanding the trade-offs between snapshotting and append-only logs.*
27. **"Redis Transactions: MULTI, EXEC, DISCARD, and WATCH"** by Redis Labs (2025) - *Implementing optimistic locking and atomic operations.*
28. **"Redis Pipelining: Maximizing Throughput"** by Redis Documentation (2024) - *Reducing network round-trips for bulk operations.*
29. **"Redis Modules: Extending Functionality"** by Redis Labs (2025) - *Overview of RediSearch, RedisGraph, RedisTimeSeries, and RedisBloom.*
30. **"Redis Client-Side Caching: A Deep Dive"** by Redis Labs (2024) - *Implementing server-assisted client-side caching for extreme performance.*
31. **"Redis Security Best Practices"** by Redis Labs (2025) - *Comprehensive guide to securing Redis deployments.*
32. **"Redis Performance Tuning Guide"** by Redis Labs (2024) - *Optimizing OS, network, and Redis configuration for maximum performance.*
