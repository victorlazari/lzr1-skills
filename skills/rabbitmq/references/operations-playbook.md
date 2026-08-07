# RabbitMQ 4.x Operations Playbook

This reference provides focused guidance on CLI commands, diagnostics, and Sev-1 incident response for RabbitMQ 4.x.

## 1. Diagnostics and Discovery

Always start with read-only discovery to understand the cluster state.

- **Cluster Status:** `rabbitmq-diagnostics cluster_status`
- **Node Status:** `rabbitmq-diagnostics status`
- **Alarms:** `rabbitmq-diagnostics alarms`
- **Environment:** `rabbitmq-diagnostics environment`
- **Memory Breakdown:** `rabbitmq-diagnostics memory_breakdown`

## 2. Incident Response (Sev-1)

### 2.1. Memory or Disk Alarms

When a node hits the memory or disk watermark, it blocks publishers.

1. **Identify the Alarm:** `rabbitmq-diagnostics alarms`
2. **Analyze Memory:** `rabbitmq-diagnostics memory_breakdown`
3. **Check Queues:** `rabbitmqctl list_queues name messages memory`
4. **Mitigation:**
   - Add resources (memory/disk).
   - Purge non-critical queues (requires user confirmation).
   - Adjust watermarks (temporary measure, requires user confirmation).

### 2.2. Network Partitions and Raft Consensus

RabbitMQ 4.x relies on Raft for Quorum Queues and Streams. Network partitions can lead to a loss of quorum.

1. **Check Cluster Status:** `rabbitmq-diagnostics cluster_status`
2. **Check Quorum Status:** `rabbitmq-diagnostics quorum_status <queue_name>`
3. **Mitigation:**
   - Resolve the underlying network issue.
   - If a node is permanently lost, remove it: `rabbitmqctl forget_cluster_node <node_name>` (requires user confirmation).
   - If quorum is lost, manual intervention may be required to force a new leader (highly destructive, requires user confirmation).

### 2.3. WAL Exhaustion (Quorum Queues)

Quorum Queues use a Write-Ahead Log (WAL). If consumers are slow, the WAL can grow and exhaust disk space.

1. **Check Disk Usage:** `df -h`
2. **Check Queue Lengths:** `rabbitmqctl list_queues name messages_ready messages_unacknowledged`
3. **Mitigation:**
   - Increase consumer capacity.
   - Adjust `x-max-length` or `x-max-length-bytes` (requires user confirmation).

## 3. Destructive Commands (Require Confirmation)

The following commands MUST NOT be executed without explicit user confirmation:

- `rabbitmqctl reset`: Resets a node to a pristine state.
- `rabbitmqctl force_reset`: Forces a reset even if the node cannot contact the cluster.
- `rabbitmqctl forget_cluster_node <node_name>`: Removes a node from the cluster.
- `rabbitmqadmin purge queue name=<queue_name>`: Deletes all messages in a queue.

## 4. Verification

After any operation, verify the cluster health:

- `rabbitmq-diagnostics status`
- `rabbitmq-diagnostics cluster_status`
- `rabbitmq-diagnostics check_running`
- `rabbitmq-diagnostics check_local_alarms`

---
*Verified against upstream: 2026-08-07*
*Primary Source: https://www.rabbitmq.com/docs/cli*
