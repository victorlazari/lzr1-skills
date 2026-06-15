---
name: rabbitmq-documentdb
description: Specialist skill for integrating, managing, and troubleshooting RabbitMQ message brokers with Amazon DocumentDB.
---

# RabbitMQ & DocumentDB Specialist

## When to Use

Use this skill when the task involves designing, implementing, securing, or troubleshooting systems that integrate RabbitMQ with Amazon DocumentDB. This includes scenarios such as:
- Architecting event-driven microservices using RabbitMQ as the communication backbone and DocumentDB as the state store.
- Configuring RabbitMQ exchanges, queues, bindings, and clustering for high availability and reliable message delivery.
- Designing DocumentDB schemas, partitioning strategies, and indexing policies for optimal query performance.
- Implementing data synchronization patterns like Change Data Capture (CDC) or dual writes between RabbitMQ and DocumentDB.
- Performing security audits, configuring TLS/SSL, and setting up IAM or RBAC for both systems.
- Troubleshooting message loss, duplication, high CPU utilization, or connection issues in integrated environments.

## Sub-Agent Spawning

This skill supports spawning sub-agents for parallel execution when tasks can be decomposed:

| Trigger Condition | Sub-Agent Type | Purpose |
|---|---|---|
| Multiple clusters to configure | Infrastructure Provisioner | Parallel setup of RabbitMQ and DocumentDB clusters |
| Multiple collections to index | Database Optimizer | Parallel creation and tuning of DocumentDB indexes |
| Multiple microservices to integrate | Integration Developer | Parallel implementation of RabbitMQ consumers/producers |
| Bulk troubleshooting across nodes | Diagnostics Agent | Parallel log analysis and health checks |
| Comprehensive security audit | Security Auditor | Parallel review of network, IAM, and TLS configurations |

### Spawning Rules
- Spawn when 3+ independent items (clusters, collections, services, nodes) need the same operation.
- Each sub-agent receives: context, specific target (e.g., specific collection or node), and success criteria.
- Results are aggregated and cross-referenced for conflicts or inconsistencies.
- Maximum concurrent sub-agents: 10.

## Workflow

1. **Requirement Analysis**: Understand the specific use case, whether it's a new architecture design, performance tuning, security audit, or troubleshooting an existing issue.
2. **Architecture Design**: Determine the appropriate RabbitMQ exchange types (Direct, Topic, Fanout, Headers) and DocumentDB consistency models based on the application's needs.
3. **Configuration & Implementation**:
   - Set up RabbitMQ queues with appropriate durability, TTL, and Dead Letter Exchanges (DLX).
   - Configure DocumentDB collections, partition keys, and indexes.
   - Implement consumers with idempotent logic and manual acknowledgments to ensure data consistency.
4. **Security Hardening**: Apply network isolation (VPC), enable TLS for data in transit, configure encryption at rest, and enforce strict access controls (RBAC/IAM).
5. **Performance Tuning**: Optimize RabbitMQ prefetch counts and connection pooling. Tune DocumentDB queries using the profiler and appropriate indexing.
6. **Monitoring & Diagnostics**: Set up metrics collection and alerting. Use distributed tracing and log analysis to troubleshoot issues like message loss or high latency.

## Core Principles

- **Idempotency**: Consumers must be designed to handle duplicate messages gracefully, typically using DocumentDB's `upsert` operations with unique identifiers.
- **Reliability**: Utilize RabbitMQ publisher confirms, durable queues, persistent messages, and manual consumer acknowledgments to prevent message loss.
- **Security First**: Always encrypt data in transit (TLS) and at rest (KMS). Apply the principle of least privilege using RBAC in RabbitMQ and IAM in DocumentDB.
- **Scalability**: Leverage RabbitMQ clustering and DocumentDB replica sets to handle high throughput and ensure high availability.
- **Observability**: Implement comprehensive logging, monitoring, and distributed tracing to quickly identify and resolve bottlenecks or failures.

## Key References

- [Complete Reference Guide](./references/complete-reference.md)
- [Reading List](./references/reading-list.md)
