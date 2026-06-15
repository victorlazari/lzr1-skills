---
name: ticket-supreme
description: Advanced architecture and implementation guide for enterprise-grade ticketing and issue-tracking systems, focusing on high availability, real-time communication, SLA management, security, omnichannel integration, and AI/ML capabilities.
---

# Ticket System Supreme Specialist

## When to Use

This skill should be invoked when designing, architecting, or implementing enterprise-grade customer support centers and ticket systems that require handling extremely large scale (e.g., 100k+ concurrent agents). It is essential for tasks involving complex operational requirements, high availability, real-time communication protocols, nuanced SLA management, stringent security and compliance measures, omnichannel integration techniques, AI/ML-driven automation, and data migration strategies.

## Sub-Agent Spawning

This skill supports spawning sub-agents for parallel execution when tasks can be decomposed:

| Trigger Condition | Sub-Agent Type | Purpose |
|---|---|---|
| Multiple microservices to design | Architecture Designer | Parallel design of stateless microservices |
| Multiple databases to scale | Database Optimizer | Parallel sharding and replication planning |
| Multiple omnichannel integrations | Integration Specialist | Parallel implementation of email, social, and webhook ingestion |
| Multiple AI/ML models to train | AI/ML Engineer | Parallel development of ticket deflection, categorization, and sentiment analysis models |
| Bulk data migration tasks | Migration Engineer | Parallel execution of ETL pipelines for data migration |

### Spawning Rules
- Spawn when 3+ independent items need the same operation
- Each sub-agent receives: context, specific target, success criteria
- Results are aggregated and cross-referenced for conflicts
- Maximum concurrent sub-agents: 10

## Workflow

1. **Architecture Design**: Establish fundamental design principles, including stateless application layers, distributed data stores, microservices architecture, event-driven communication, and health monitoring.
2. **Infrastructure Scaling**: Implement scalable infrastructure patterns using load balancers, API gateways, application layers, real-time layers, data layers, message brokers, cache layers, and storage layers.
3. **Real-time Communication**: Develop WebSocket architectures for real-time updates, presence tracking, typing indicators, and fault tolerance with reconnection strategies.
4. **SLA Management**: Handle advanced SLA edge cases, including pause conditions, multi-timezone SLA handling, and dynamic SLA recalculation.
5. **Security & Compliance**: Enforce Role-Based Access Control (RBAC), Row-Level Security (RLS), Personally Identifiable Information (PII) redaction, and regulatory compliance (GDPR & SOC2).
6. **Omnichannel Integration**: Implement email parsing strategies, social media ingestion, and API webhooks for event handling.
7. **AI/ML Integration**: Integrate AI/ML for ticket deflection, automated ticket categorization, sentiment analysis, and agent copilot functionalities.
8. **Data Migration**: Plan and execute data migration strategies, including pre-migration planning, migration approaches (Big Bang, Phased, Parallel Run), data transformation, validation, and post-migration monitoring.

## Core Principles

- **High Availability & Scaling**: Ensure zero downtime, linear scalability, and fault tolerance through stateless application layers, distributed data stores, and microservices architecture.
- **Real-time Responsiveness**: Utilize dedicated WebSocket servers and fast in-memory stores for real-time updates, presence tracking, and typing indicators.
- **Nuanced SLA Management**: Support stateful SLA timers, timezone-aware formats, and dynamic SLA recalculation based on priority changes.
- **Stringent Security**: Implement granular permissions, data visibility restrictions, PII protection, and compliance with data privacy regulations.
- **Omnichannel Capabilities**: Normalize messages from various channels into a unified model and process them through scalable webhook mechanisms.
- **Intelligent Automation**: Leverage AI/ML to reduce agent load, classify tickets, prioritize based on sentiment, and enhance agent productivity.
- **Robust Data Migration**: Carefully plan and execute data migration with thorough data inventory, quality assessment, transformation, and validation.

## Key References

- [High Availability & Scaling Architecture](./references/complete-reference.md#high-availability--scaling-architecture)
- [Real-time Communication](./references/complete-reference.md#real-time-communication)
- [Advanced SLA Edge Cases](./references/complete-reference.md#advanced-sla-edge-cases)
- [Security & Compliance](./references/complete-reference.md#security--compliance)
- [Omnichannel Integration Patterns](./references/complete-reference.md#omnichannel-integration-patterns)
- [AI/ML Integration](./references/complete-reference.md#aiml-integration)
- [Data Migration Strategies](./references/complete-reference.md#data-migration-strategies)
- [Ticket-Supreme CLI Command Reference](./references/complete-reference.md#ticket-supreme-cli-command-reference)
