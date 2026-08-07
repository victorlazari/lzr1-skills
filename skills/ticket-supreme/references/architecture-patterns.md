# Architecture Patterns for Enterprise Ticketing Systems

Verified against upstream: 2026-08-07

## High Availability and Scaling

- **Stateless Microservices:** Design services to be stateless, allowing horizontal scaling.
- **Database Sharding:** Distribute data across multiple databases to handle high read/write loads.
- **Read Replicas:** Use read replicas to offload read queries from the primary database.
- **Caching:** Implement caching layers (e.g., Redis, Memcached) to reduce database load and improve response times.

## Real-Time Communication

- **WebSockets:** Use WebSockets for real-time updates (e.g., new tickets, status changes, chat messages).
- **Server-Sent Events (SSE):** Use SSE for unidirectional real-time updates from the server to the client.
- **Message Queues:** Use message queues (e.g., RabbitMQ, Kafka) for asynchronous processing and decoupling services.

## SLA Management

- **Deterministic Recalculation:** Ensure SLA recalculations are deterministic and timezone-aware.
- **Event-Driven Updates:** Trigger SLA updates based on specific events (e.g., ticket creation, status change, priority change).
- **Background Processing:** Use background jobs to process SLA breaches and send notifications.

## Primary Sources

- [AWS Architecture Center](https://aws.amazon.com/architecture/)
- [Zendesk Developer Documentation](https://developer.zendesk.com/)
- [Jira Service Management](https://www.atlassian.com/software/jira/service-management)
