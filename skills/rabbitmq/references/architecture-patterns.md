# RabbitMQ 4.x Architecture Patterns

This reference provides focused guidance on modern High Availability paradigms in RabbitMQ 4.x, specifically Quorum Queues, Streams, and Dead Letter Exchanges (DLX).

## 1. Quorum Queues

Quorum Queues are the default and recommended queue type for High Availability in RabbitMQ 4.x. They use the Raft consensus algorithm to replicate data across nodes.

### 1.1. Key Characteristics

- **Replication:** Data is replicated to a quorum of nodes (e.g., 3 nodes).
- **Durability:** Messages are always written to disk (WAL).
- **Use Case:** General-purpose messaging where data safety is critical.

### 1.2. Configuration

Quorum Queues are declared with the `x-queue-type` argument set to `quorum`.

```json
{
  "name": "my-quorum-queue",
  "vhost": "/",
  "durable": true,
  "auto_delete": false,
  "arguments": {
    "x-queue-type": "quorum"
  }
}
```

## 2. Streams

Streams are an append-only log abstraction, ideal for high-throughput, replayable messaging.

### 2.1. Key Characteristics

- **Replayability:** Consumers can read from any point in the stream.
- **Throughput:** Highly optimized for large volumes of data.
- **Use Case:** Event sourcing, telemetry, and scenarios requiring message replay.

### 2.2. Configuration

Streams are declared with the `x-queue-type` argument set to `stream`.

```json
{
  "name": "my-stream",
  "vhost": "/",
  "durable": true,
  "auto_delete": false,
  "arguments": {
    "x-queue-type": "stream"
  }
}
```

## 3. Dead Letter Exchanges (DLX)

DLX is used to handle messages that cannot be processed successfully.

### 3.1. Key Characteristics

- **Triggers:** Messages are dead-lettered if they are rejected (`basic.reject` or `basic.nack` with `requeue=false`), expire (TTL), or exceed the queue length limit.
- **Routing:** Dead-lettered messages are routed to the specified DLX.

### 3.2. Configuration

Configure DLX using queue arguments:

```json
{
  "arguments": {
    "x-dead-letter-exchange": "my-dlx",
    "x-dead-letter-routing-key": "my-dlx-routing-key"
  }
}
```

## 4. Cross-Cluster Communication

For communication between different RabbitMQ clusters, use Federation or Shovel.

- **Federation:** Replicates messages across exchanges or queues in different clusters. Ideal for geographically distributed systems.
- **Shovel:** Moves messages from a source to a destination. Ideal for simple, unidirectional data transfer.

---
*Verified against upstream: 2026-08-07*
*Primary Source: https://www.rabbitmq.com/docs/quorum-queues*
*Primary Source: https://www.rabbitmq.com/docs/streams*
