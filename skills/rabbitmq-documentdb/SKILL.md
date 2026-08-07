---
name: rabbitmq-documentdb
description: Specialist skill for integrating, managing, and troubleshooting RabbitMQ message brokers with Amazon DocumentDB.
---

# RabbitMQ & DocumentDB Specialist

## Scope and Triggers

Use this skill when the task involves designing, implementing, securing, or troubleshooting systems that integrate RabbitMQ with Amazon DocumentDB.
- **In Scope:** Architecting event-driven microservices, configuring RabbitMQ exchanges/queues/bindings, designing DocumentDB schemas/indexes, implementing data synchronization (CDC), security audits, and troubleshooting integration issues.
- **Out of Scope:** General application development not related to RabbitMQ/DocumentDB integration, or managing other message brokers (e.g., Kafka) or databases (e.g., DynamoDB).
- **Escalation Boundaries:** Route to `trivy-scanner` when scanning RabbitMQ or DocumentDB container images for vulnerabilities. Route to `security-review` when performing a comprehensive security audit of the application code interacting with these services.

## Preconditions

Before executing any operations, the agent must:
1. Detect the target environment (e.g., AWS VPC, Kubernetes cluster).
2. Verify RabbitMQ version (target 4.3+ for Khepri metadata store, 32 priority levels, and delayed retries).
3. Verify DocumentDB engine version (target 8.0+ for improved latency, compression, and new aggregation operators).
4. Ensure necessary permissions (IAM roles, RabbitMQ RBAC) are available.
5. Confirm user intent for any destructive or production-impacting actions.

## Source Freshness

Volatile facts, such as supported versions or specific command flags, require runtime verification against official sources.
- See `references/source-map.md` for authoritative sources.
- Verify installed versions and current upstream documentation before applying destructive or production-impacting actions.

## Workflow

1. **Discover current environment state (read-only):** Identify RabbitMQ and DocumentDB clusters, versions, and configurations.
2. **Validate prerequisites and configuration syntax:** Use `scripts/validate-config.sh` to perform syntax and smoke tests on configurations.
3. **Present proposed changes:** Require explicit user confirmation for any mutating actions (e.g., dropping databases/collections, deleting users, modifying queues).
4. **Execute configuration or integration steps:** Apply changes using safe, deterministic methods.
5. **Run post-execution validation and health checks:** Ensure the system is stable and performing as expected.
6. **Stop and provide rollback instructions:** If any step fails, halt execution and guide the user through rollback procedures.

## Safety

- **Read-only discovery:** Always separate read-only discovery from mutation steps.
- **Explicit confirmation:** Require explicit user confirmation for destructive actions (e.g., dropping databases/collections, deleting users).
- **Dry-run support:** Implement dry-run support in validation scripts where feasible.
- **Rollback guidance:** Provide rollback guidance for failed migrations or configuration changes.

## Validation

- **Syntax checks:** Use `scripts/validate-config.sh` to validate RabbitMQ and DocumentDB configuration files.
- **Postcondition verification:** Verify that queues are created, indexes are built, and connections are established successfully.

## Failure Handling

- If a configuration fails validation, diagnose the error using the output of `validate-config.sh` and suggest corrections.
- If a mutation fails, provide rollback instructions and avoid repeating the failed action unchanged.

## Output Contract

The result must include:
- A structured summary of actions taken.
- Evidence of successful validation (e.g., output of `validate-config.sh`).
- Severity/confidence levels for any identified issues.
- Actionable next steps for the user.

## Resources

- [Complete Reference Guide](references/complete-reference.md): Actionable, normative requirements with primary source links.
- [Source Map](references/source-map.md): Maps specific tasks to authoritative sources.
- [Validation Script](scripts/validate-config.sh): Validates configuration files.
- [Connection Settings Template](templates/connection-settings.json.template): Reusable template for DocumentDB connection settings.

## Orchestration

This skill supports spawning sub-agents for parallel execution when 3+ independent items need the same operation.

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

### Adversarial Verification Panel
For each significant integration issue, security vulnerability, or performance bottleneck produced by the parallel sub-agents:
1. Spawn 3 independent Refuter Agents per finding.
2. A finding is confirmed only if ≥2 refuters fail to refute it.
3. A finding is discarded if ≥2 refuters succeed.

### Cross-System Consistency Validator
Run one Consistency Validator Agent with all parallel outputs to flag contradictions and missing prerequisites.

### Synthesis Agent
The synthesis step actively resolves contradictions, re-orders items based on prerequisites, calibrates confidence, and notes blind spots.
