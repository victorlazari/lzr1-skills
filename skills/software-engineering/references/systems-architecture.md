# Systems Architecture

## Table of Contents
1. Architecture Decision Framework
2. Scalability Patterns
3. Data Architecture
4. Integration Patterns
5. Reliability Engineering
6. Architecture Documentation

---

## 1. Architecture Decision Framework

### Decision Process

1. Identify the architectural drivers (requirements, constraints, quality attributes)
2. Generate candidate architectures (at least 2-3 options)
3. Evaluate trade-offs using quality attributes
4. Document the decision (ADR - Architecture Decision Record)
5. Validate with prototypes for high-risk decisions

### Quality Attributes

| Attribute | Description | Tactics |
|---|---|---|
| Scalability | Handle growing load | Horizontal scaling, caching, sharding |
| Availability | Uptime percentage | Redundancy, failover, health checks |
| Performance | Response time, throughput | Caching, CDN, async processing |
| Security | Protection from threats | Encryption, auth, input validation |
| Maintainability | Ease of change | Modularity, clean interfaces, tests |
| Observability | Understanding system state | Logging, metrics, tracing |
| Cost | Infrastructure spend | Right-sizing, spot instances, serverless |

### Architecture Decision Record (ADR) Template

```markdown
# ADR-001: [Decision Title]

## Status: [Proposed | Accepted | Deprecated | Superseded]

## Context
What is the issue that we're seeing that is motivating this decision?

## Decision
What is the change that we're proposing and/or doing?

## Consequences
What becomes easier or more difficult to do because of this change?

## Alternatives Considered
What other options were evaluated and why were they rejected?
```

---

## 2. Scalability Patterns

### Horizontal Scaling

- **Stateless services**: No local state; use external stores
- **Load balancing**: Round-robin, least connections, consistent hashing
- **Auto-scaling**: Scale based on CPU, memory, queue depth, or custom metrics
- **Database scaling**: Read replicas, sharding, connection pooling

### Vertical Scaling Limits

- Simpler but has hard ceilings
- Use for databases before sharding
- Consider for compute-intensive single-threaded workloads
- Monitor for diminishing returns

### Caching Architecture

```
Client → CDN Cache → API Gateway Cache → Application Cache → Database Cache → Database
```

| Layer | What to Cache | TTL |
|---|---|---|
| CDN | Static assets, public API responses | Hours-days |
| API Gateway | Authenticated responses | Minutes |
| Application (Redis) | Computed results, sessions | Minutes-hours |
| Database | Query results, buffer pool | Automatic |

### Database Scaling Strategies

| Strategy | Complexity | Use Case |
|---|---|---|
| Read replicas | Low | Read-heavy workloads |
| Connection pooling | Low | Many short-lived connections |
| Vertical scaling | Low | Quick fix, single-node limit |
| Functional partitioning | Medium | Separate databases per service |
| Horizontal sharding | High | Very large datasets |
| CQRS | High | Read/write asymmetry |

---

## 3. Data Architecture

### Data Storage Selection

| Storage Type | Best For | Examples |
|---|---|---|
| Relational (SQL) | Structured data, transactions, joins | PostgreSQL, MySQL |
| Document | Semi-structured, flexible schema | MongoDB, DynamoDB |
| Key-Value | Caching, sessions, simple lookups | Redis, Memcached |
| Wide-Column | Time series, IoT, high write throughput | Cassandra, ScyllaDB |
| Graph | Relationships, social networks | Neo4j, Neptune |
| Search | Full-text search, analytics | Elasticsearch, Meilisearch |
| Object Storage | Files, media, backups | S3, GCS, MinIO |
| Vector | Embeddings, similarity search | Pinecone, pgvector |

### Data Flow Patterns

- **ETL (Extract, Transform, Load)**: Batch processing to data warehouse
- **ELT (Extract, Load, Transform)**: Load raw, transform in warehouse
- **CDC (Change Data Capture)**: Stream database changes as events
- **Event Sourcing**: Store events as source of truth, derive state
- **Data Mesh**: Domain-owned data products with federated governance

### Consistency Patterns

| Pattern | Consistency | Performance | Use Case |
|---|---|---|---|
| Two-Phase Commit | Strong | Low | Critical transactions |
| Saga (Orchestration) | Eventual | Medium | Multi-service workflows |
| Saga (Choreography) | Eventual | High | Decoupled services |
| Outbox Pattern | Eventual (reliable) | Medium | Event publishing |
| CRDT | Eventual (conflict-free) | High | Collaborative editing |

---

## 4. Integration Patterns

### API Gateway

Responsibilities: routing, authentication, rate limiting, request transformation, response caching, circuit breaking.

| Tool | Type | Best For |
|---|---|---|
| Kong | Open-source/Enterprise | Flexible, plugin ecosystem |
| AWS API Gateway | Managed | AWS-native, serverless |
| Envoy | Proxy/Service mesh | High-performance, K8s |
| Traefik | Cloud-native | Docker/K8s, auto-discovery |

### Service Mesh

For service-to-service communication in microservices:
- **mTLS**: Automatic encryption between services
- **Traffic management**: Canary deployments, traffic splitting
- **Observability**: Automatic metrics, traces, access logs
- **Resilience**: Retries, timeouts, circuit breakers

Tools: Istio, Linkerd, Consul Connect

### Event-Driven Integration

| Component | Purpose | Tools |
|---|---|---|
| Message Broker | Async communication | Kafka, RabbitMQ, NATS |
| Event Store | Event sourcing persistence | EventStoreDB, Kafka |
| Schema Registry | Event schema evolution | Confluent Schema Registry |
| Stream Processor | Real-time event processing | Kafka Streams, Flink |

---

## 5. Reliability Engineering

### SLO/SLI/SLA Framework

- **SLI (Service Level Indicator)**: Quantitative measure (e.g., latency p99)
- **SLO (Service Level Objective)**: Target value for SLI (e.g., p99 < 200ms)
- **SLA (Service Level Agreement)**: Contract with consequences (e.g., 99.9% uptime)
- **Error Budget**: Allowed unreliability (e.g., 0.1% = 43.8 min/month downtime)

### Availability Targets

| Target | Downtime/Year | Downtime/Month |
|---|---|---|
| 99% (two nines) | 3.65 days | 7.3 hours |
| 99.9% (three nines) | 8.76 hours | 43.8 minutes |
| 99.99% (four nines) | 52.6 minutes | 4.38 minutes |
| 99.999% (five nines) | 5.26 minutes | 26.3 seconds |

### Failure Handling

- **Graceful degradation**: Serve reduced functionality during partial failures
- **Circuit breaker**: Stop calling failing dependencies
- **Bulkhead**: Isolate failures to prevent cascade
- **Retry with backoff**: Handle transient failures
- **Timeout**: Never wait indefinitely for a response
- **Fallback**: Serve cached/default data when primary fails
- **Chaos engineering**: Proactively inject failures to find weaknesses

---

## 6. Architecture Documentation

### C4 Model

| Level | Shows | Audience |
|---|---|---|
| Context | System + external actors | Everyone |
| Container | Applications, databases, queues | Technical team |
| Component | Internal structure of a container | Developers |
| Code | Class/module level | Developers (rarely needed) |

### Documentation Artifacts

- **Architecture overview**: C4 context and container diagrams
- **ADRs**: All significant architecture decisions
- **API documentation**: OpenAPI/Swagger specs
- **Runbooks**: Operational procedures for common scenarios
- **Data flow diagrams**: How data moves through the system
- **Deployment diagrams**: Infrastructure topology
- **Security architecture**: Trust boundaries, data classification
