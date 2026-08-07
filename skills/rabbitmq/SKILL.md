---
name: rabbitmq
description: Advanced RabbitMQ 4.x operations, troubleshooting, and architecture design focusing on Quorum Queues and Streams.
---

# RabbitMQ Operations Specialist

This skill provides comprehensive expertise in managing, troubleshooting, and optimizing RabbitMQ 4.x in production environments. It focuses exclusively on modern High Availability paradigms, specifically Quorum Queues and Streams, and provides deterministic workflows for cluster management and incident response.

## Scope and Triggers

**Use this skill when you need to:**
- Diagnose and resolve RabbitMQ production incidents (memory/disk alarms, network partitions, Raft consensus issues).
- Troubleshoot message backlogs, consumer starvation, or WAL exhaustion.
- Design or audit RabbitMQ topologies using Quorum Queues, Streams, and Dead Letter Exchanges (DLX).
- Configure and tune RabbitMQ 4.x for high throughput or low latency.
- Perform security audits on RabbitMQ clusters (TLS, RBAC).

**Do NOT use this skill for:**
- Building new event-driven applications or background workers (route to `automation-and-scheduling`).
- Deploying a new RabbitMQ instance via Docker or systemd (route to `persistent-computing`).
- Managing legacy Classic Mirrored Queues or Classic Queue version 1 (CQv1).

## Preconditions and Source Freshness

Before executing any commands, you MUST:
1. Verify the cluster state and version using `rabbitmq-diagnostics status` and `rabbitmq-diagnostics cluster_status`.
2. Ensure the cluster is running RabbitMQ 4.x.
3. Consult the official RabbitMQ 4.x documentation for any volatile facts, commands, or configurations.

## Workflow

1. **Discovery:** Run `rabbitmq-diagnostics status` and `rabbitmq-diagnostics cluster_status` to understand the current state.
2. **Validation:** Run `scripts/validate-topology.sh` against the cluster's `definitions.json` to identify legacy configurations (e.g., `ha-mode`, transient non-exclusive queues).
3. **Migration Planning:** If legacy configurations are found, halt and require user confirmation to plan a migration to Quorum Queues or Streams.
4. **Execution:** Execute operational or troubleshooting tasks using `references/operations-playbook.md` and `references/architecture-patterns.md`.
5. **Verification:** Run `rabbitmq-diagnostics` to ensure cluster health, Raft consensus stability, and expected post-conditions.

## Safety and Validation

- **Read-Only Discovery:** Always use `rabbitmq-diagnostics` for read-only discovery before any mutation.
- **Confirmation Required:** Explicit user confirmation is REQUIRED before executing destructive commands like `rabbitmqctl reset`, `rabbitmqctl force_reset`, or `rabbitmqadmin purge queue`.
- **Validation:** Validate `definitions.json` changes with `scripts/validate-topology.sh` before applying them.
- **Focus:** Ensure Quorum Queue WAL exhaustion and Raft consensus issues are the primary focus of HA troubleshooting.

## Failure Handling

- If a command fails, do not repeat it unchanged.
- Diagnose the error using `rabbitmq-diagnostics` and log files.
- Consult `references/operations-playbook.md` for alternative approaches or rollback procedures.
- If Raft consensus is lost, prioritize restoring quorum before attempting other operations.

## Output Contract

The result must include:
- A summary of the actions taken and their outcomes.
- Evidence of cluster health (e.g., `rabbitmq-diagnostics status` output).
- Any identified legacy configurations or architectural risks.
- Actionable next steps for remediation or optimization.

## Resources

- `references/operations-playbook.md`: Focused guide on CLI commands, diagnostics, and Sev-1 incident response for RabbitMQ 4.x.
- `references/architecture-patterns.md`: Focused guide on Quorum Queues, Streams, DLX, and cross-cluster communication.
- `scripts/validate-topology.sh`: Deterministic script to check `definitions.json` for legacy `ha-mode` policies, transient non-exclusive queues, and other 4.0-incompatible configurations.
