# Backend Engineering

## Table of Contents
1. Service Architecture
2. API Design
3. Distributed Systems
4. Data Processing
5. Security
6. Observability

---

## 1. Service Architecture

### Architectural Patterns

| Pattern | Best For | Trade-offs |
|---|---|---|
| Monolith | Small teams, early stage, simple domains | Simple but hard to scale independently |
| Modular Monolith | Growing teams, clear domain boundaries | Best of both worlds, migration path |
| Microservices | Large teams, independent scaling needs | Complex operations, network overhead |
| Event-Driven | Async workflows, decoupled systems | Eventual consistency, debugging complexity |
| Serverless | Variable traffic, event processing | Cold starts, vendor lock-in |
| CQRS | Read/write asymmetry, complex queries | Complexity, eventual consistency |

### Service Design Principles

- **Single Responsibility**: Each service owns one bounded context
- **API-first**: Design the contract before implementation
- **Stateless**: Store state externally (database, cache, queue)
- **Idempotent**: Operations safe to retry without side effects
- **Resilient**: Handle failures gracefully (circuit breakers, retries, fallbacks)
- **Observable**: Emit structured logs, metrics, and traces

### Microservice Communication

| Pattern | Use Case | Properties |
|---|---|---|
| REST/HTTP | Synchronous request-response | Simple, widely supported |
| gRPC | High-performance, typed contracts | Fast, streaming, code generation |
| Message Queue | Async, decoupled processing | Reliable, buffered, ordered |
| Event Bus | Pub/sub, event sourcing | Decoupled, scalable |
| GraphQL | Client-driven data fetching | Flexible, single endpoint |

---

## 2. API Design

### REST API Best Practices

```
GET    /api/v1/users          → List users (with pagination)
GET    /api/v1/users/:id      → Get single user
POST   /api/v1/users          → Create user
PUT    /api/v1/users/:id      → Full update
PATCH  /api/v1/users/:id      → Partial update
DELETE /api/v1/users/:id      → Delete user
```

**Design Rules**:
- Use nouns for resources, HTTP verbs for actions
- Use plural nouns consistently (`/users` not `/user`)
- Nest resources for relationships (`/users/:id/orders`)
- Use query parameters for filtering, sorting, pagination
- Return appropriate HTTP status codes (201 for create, 204 for delete)
- Include `Location` header for created resources
- Implement HATEOAS for discoverability (when appropriate)

### API Versioning

| Strategy | Pros | Cons |
|---|---|---|
| URL path (`/v1/`) | Clear, easy routing | URL pollution |
| Header (`Accept: v1`) | Clean URLs | Hidden, harder to test |
| Query param (`?version=1`) | Simple | Easy to forget |

### Pagination Patterns

| Pattern | Best For | Implementation |
|---|---|---|
| Offset/Limit | Simple lists, small datasets | `?offset=20&limit=10` |
| Cursor-based | Large datasets, real-time data | `?cursor=abc123&limit=10` |
| Keyset | Sorted large datasets | `?after_id=100&limit=10` |

### Error Handling

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Request validation failed",
    "details": [
      {"field": "email", "message": "Invalid email format"},
      {"field": "age", "message": "Must be between 0 and 150"}
    ],
    "request_id": "req_abc123",
    "documentation_url": "https://api.example.com/docs/errors#VALIDATION_ERROR"
  }
}
```

### Rate Limiting

- Implement token bucket or sliding window algorithms
- Return `429 Too Many Requests` with `Retry-After` header
- Include rate limit headers: `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset`
- Different limits per endpoint, user tier, and authentication method

---

## 3. Distributed Systems

### CAP Theorem Trade-offs

| Choice | Sacrifice | Use Case |
|---|---|---|
| CP (Consistency + Partition Tolerance) | Availability | Financial transactions, inventory |
| AP (Availability + Partition Tolerance) | Consistency | Social media, caching, analytics |

### Consistency Patterns

- **Strong consistency**: All reads see the latest write (expensive, slow)
- **Eventual consistency**: Reads may be stale but will converge (fast, scalable)
- **Causal consistency**: Preserves cause-effect ordering (good middle ground)
- **Read-your-writes**: User always sees their own updates (common requirement)

### Distributed System Patterns

| Pattern | Purpose | Implementation |
|---|---|---|
| Circuit Breaker | Prevent cascade failures | Hystrix, resilience4j, Polly |
| Saga | Distributed transactions | Orchestration or Choreography |
| Outbox | Reliable event publishing | DB transaction + event table |
| CQRS | Separate read/write models | Different stores for reads/writes |
| Event Sourcing | Audit trail, temporal queries | Append-only event log |
| Bulkhead | Isolate failures | Separate thread pools/resources |

### Message Queue Patterns

- **Work Queue**: Distribute tasks among workers (competing consumers)
- **Pub/Sub**: Broadcast events to multiple subscribers
- **Dead Letter Queue**: Handle failed messages for investigation
- **Exactly-once processing**: Idempotent consumers + deduplication
- **Ordering guarantees**: Partition by key for ordered processing

---

## 4. Data Processing

### Batch Processing

- Use for periodic aggregations, reports, ETL
- Frameworks: Apache Spark, Apache Beam, dbt
- Design for idempotency (safe to re-run)
- Implement checkpointing for long-running jobs
- Monitor job duration, data volume, error rates

### Stream Processing

- Use for real-time analytics, event processing, CDC
- Frameworks: Apache Kafka Streams, Apache Flink, Spark Streaming
- Handle late-arriving data with watermarks
- Implement windowing (tumbling, sliding, session)
- Design for exactly-once semantics where needed

### Caching Strategies

| Strategy | Description | Use Case |
|---|---|---|
| Cache-aside | App manages cache explicitly | General purpose |
| Read-through | Cache loads on miss | Transparent caching |
| Write-through | Write to cache and DB | Strong consistency |
| Write-behind | Write to cache, async to DB | High write throughput |
| Refresh-ahead | Proactively refresh before expiry | Predictable access patterns |

**Cache Invalidation** (the hard problem):
- TTL-based: Simple but may serve stale data
- Event-based: Invalidate on write events
- Version-based: Include version in cache key
- Tag-based: Invalidate by tag/category

---

## 5. Security

### Authentication & Authorization

| Method | Use Case | Considerations |
|---|---|---|
| JWT | Stateless auth, microservices | Token size, revocation complexity |
| OAuth 2.0 | Third-party access, SSO | Complex flows, token management |
| API Keys | Service-to-service, simple auth | Rotation, scoping |
| mTLS | Service mesh, zero-trust | Certificate management |
| Session-based | Traditional web apps | Sticky sessions, scaling |

### Security Best Practices

- **Input validation**: Validate all inputs at the boundary (type, length, format, range)
- **Parameterized queries**: Never concatenate user input into queries
- **Output encoding**: Encode output based on context (HTML, URL, JS, SQL)
- **Secrets management**: Use vault systems (HashiCorp Vault, AWS Secrets Manager)
- **Least privilege**: Minimum permissions for each service/user
- **Defense in depth**: Multiple security layers, don't trust any single control
- **Audit logging**: Log all security-relevant events with context
- **Dependency scanning**: Automated CVE detection in dependencies

---

## 6. Observability

### Three Pillars

| Pillar | Purpose | Tools |
|---|---|---|
| Logs | Event records, debugging | ELK, Loki, CloudWatch |
| Metrics | Numerical measurements, alerting | Prometheus, Datadog, CloudWatch |
| Traces | Request flow across services | Jaeger, Zipkin, OpenTelemetry |

### Structured Logging

```json
{
  "timestamp": "2025-01-15T10:30:00Z",
  "level": "error",
  "service": "payment-service",
  "trace_id": "abc123",
  "user_id": "usr_456",
  "message": "Payment processing failed",
  "error": "insufficient_funds",
  "amount": 99.99,
  "currency": "USD"
}
```

### Key Metrics (RED Method)

- **Rate**: Requests per second
- **Errors**: Error rate (percentage of failed requests)
- **Duration**: Latency distribution (p50, p95, p99)

### Alerting Strategy

- Alert on symptoms (user impact), not causes
- Use multi-window, multi-burn-rate alerts for SLOs
- Implement runbooks for every alert
- Avoid alert fatigue: every alert must be actionable
