---
name: lerian-helm
description: Comprehensive guide for Lerian Studio Helm deployments, advanced operations, security audits, and troubleshooting in production environments.
---

# Lerian Studio Helm Deployments

## When to Use

Use this skill when managing, deploying, or troubleshooting Lerian Studio applications via Helm in enterprise-grade Kubernetes environments. This includes:
- Configuring custom `values.yaml` overrides for production, including resource limits and multi-tenant configurations.
- Managing external databases versus Bitnami subcharts and handling connection pooling.
- Executing zero-downtime upgrades and complex database migrations using `golang-migrate` and Helm hooks.
- Troubleshooting deployment failures, CrashLoopBackOffs, network timeouts, and ingress issues.
- Performing security audits on Helm deployments, including secret management, Network Policies, and PodSecurityContext hardening.
- Handling massive datasets and worst-case scenarios like complete environment resets or disaster recovery.

## Sub-Agent Spawning

This skill supports spawning sub-agents for parallel execution when tasks can be decomposed:

| Trigger Condition | Sub-Agent Type | Purpose |
|---|---|---|
| Multiple environments to upgrade | Deployment Upgrader | Parallel zero-downtime upgrades across different namespaces or clusters |
| Multiple microservices to troubleshoot | Diagnostics Agent | Parallel log analysis and resource inspection for failing pods |
| Multiple databases to migrate | Migration Executor | Parallel execution of `golang-migrate` scripts for different services |
| Multiple namespaces to audit | Security Auditor | Parallel security review of Network Policies and secret management |

### Spawning Rules
- Spawn when 3+ independent items (environments, services, databases) need the same operation
- Each sub-agent receives: context, specific target (e.g., namespace, release name), success criteria
- Results are aggregated and cross-referenced for conflicts
- Maximum concurrent sub-agents: 10

## Workflow

1. **Pre-Deployment Assessment**: Review the target environment, existing Helm releases, and database states. Ensure backups are available before any upgrade or migration.
2. **Configuration Tuning**: Customize `values.yaml` for the specific environment. Focus on resource requests/limits, HPA settings, Pod Disruption Budgets, and timeout configurations.
3. **Security Hardening**: Audit the configuration for hardcoded secrets, enforce default-deny Network Policies, and ensure strict `PodSecurityContext` settings (e.g., `runAsNonRoot`).
4. **Execution**: Apply the Helm upgrade using `--wait` and `--timeout` flags. Monitor the execution of `pre-install` and `pre-upgrade` hooks, especially database migrations.
5. **Validation and Troubleshooting**: Verify pod readiness and service availability. If issues arise (e.g., CrashLoopBackOff, pending pods), utilize `kubectl` and `helm` CLI commands to diagnose logs, events, and resource constraints.
6. **Post-Deployment**: Confirm successful migration, monitor application metrics (latency, error rates), and document any manual interventions required during the process.

## Core Principles

- **Never Edit Resources Directly**: Always use `helm upgrade` to maintain the single source of truth. Avoid manual `kubectl edit` for persistent changes.
- **Master the Hooks**: Database migrations are the most dangerous part of any deployment. Monitor them closely and handle massive datasets with out-of-band migrations if necessary.
- **Zero-Trust Architecture**: Implement default-deny Network Policies and utilize external secret stores (e.g., ESO) to minimize the blast radius of a compromised pod.
- **Plan for Failure**: Assume network partitions will happen, databases will crash, and disks will fill up. Configure aggressive timeouts, exponential backoffs, and robust readiness/liveness probes.
- **Data Integrity First**: Always backup databases before migrations. Use transactional migrations and be prepared to manually resolve dirty states in `golang-migrate`.

## Key References

- `values-base.yaml`, `values-prod.yaml`, `values-secrets.yaml` for configuration layering.
- `_helpers.tpl` for understanding Helm template rendering and naming conventions.
- `golang-migrate` CLI for manual database schema management and dirty state resolution.
- Kubernetes Network Policies and PodSecurityContext documentation for security audits.
- Prometheus and Grafana dashboards for monitoring resource utilization and API latency.
