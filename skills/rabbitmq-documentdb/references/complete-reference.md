# RabbitMQ & DocumentDB Specialist: Complete Reference Guide

*Verified against upstream: 2026-08-07*

## 1. Introduction

This reference guide provides actionable, normative requirements for integrating and managing RabbitMQ and DocumentDB. It focuses on current capabilities, including RabbitMQ 4.3 and DocumentDB 8.0.

## 2. RabbitMQ Advanced Concepts (Version 4.3+)

### 2.1 Quorum Queues and Priorities
- **Requirement:** Use Quorum Queues for high availability and data safety.
- **Capability:** RabbitMQ 4.3 introduces 32 strict message priority levels for Quorum Queues.
- **Action:** Configure queues with appropriate priority levels based on application needs.

### 2.2 Delayed Retries
- **Requirement:** Replace complex dead-letter cycle workarounds with native delayed retries.
- **Capability:** RabbitMQ 4.3 supports native delayed retries.
- **Action:** Configure delayed retry policies for entity-specific rate limits and transient failures.

### 2.3 Metadata Store
- **Requirement:** Ensure compatibility with Khepri.
- **Capability:** Khepri is the only metadata store in RabbitMQ 4.3.
- **Action:** Verify that all plugins and integrations are compatible with Khepri.

### 2.4 Consumer Timeouts
- **Requirement:** Configure consumer timeouts appropriately for quorum queues.
- **Action:** Set consumer timeouts to handle unresponsive consumers and prevent message blocking.

## 3. DocumentDB Advanced Concepts (Version 8.0+)

### 3.1 Engine Version and Upgrades
- **Requirement:** Target engine version 8.0 for new deployments.
- **Capability:** DocumentDB supports in-place upgrades from version 5.0 to 8.0.
- **Action:** Plan and execute in-place upgrades for existing 5.0 clusters.

### 3.2 Query Optimization and Aggregation
- **Requirement:** Leverage new aggregation operators for complex queries.
- **Capability:** DocumentDB 8.0 adds 46 new MongoDB aggregation operators and cursor methods.
- **Action:** Refactor existing queries to use the new operators for improved performance.

### 3.3 Performance Improvements
- **Capability:** DocumentDB 8.0 improves query latency by up to 7x and compression ratio by up to 5x.
- **Action:** Monitor performance metrics after upgrading to 8.0 to verify improvements.

## 4. Integrating RabbitMQ with DocumentDB

### 4.1 Architectural Considerations
- **Requirement:** Use idempotent consumers to avoid duplicate writes (e.g., using `upsert`).
- **Requirement:** Implement message acknowledgements to ensure at-least-once delivery.
- **Requirement:** Utilize RabbitMQ native delayed retries for transient DocumentDB connection issues.

## 5. Security and Compliance

### 5.1 Network Security
- **Requirement:** Isolate RabbitMQ and DocumentDB within a VPC.
- **Requirement:** Define strict ingress and egress rules using Security Groups & NACLs.

### 5.2 Authentication and Authorization
- **Requirement:** Use strong passwords, TLS/SSL, and Role-Based Access Control (RBAC) in RabbitMQ.
- **Requirement:** Enable IAM Authentication and use TLS connections in DocumentDB.

### 5.3 Data Encryption
- **Requirement:** Enable TLS for both RabbitMQ and DocumentDB in transit.
- **Requirement:** Use AWS KMS for DocumentDB encryption at rest.

## 6. Configuration Schemas

### 6.1 RabbitMQ Configuration
- `rabbitmq.conf`: Main configuration file (node name, ports, logging, auth).
- `advanced.config`: Complex configurations (Erlang term format, SSL options).

### 6.2 DocumentDB Configuration
- `connection-settings.json`: Host, port, credentials, SSL flag. Use the provided template.
- `security-settings.json`: Encryption, backup retention, KMS key, VPC security groups.
