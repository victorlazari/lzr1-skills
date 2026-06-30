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

---

## Adversarial Verification Panel

For each significant Helm deployment issue and security audit finding produced by the parallel sub-agents:

1. Spawn **3 independent Refuter Agents** per finding, each with:
   - The finding in full
   - Instruction: *"Assume this finding is wrong. Find the strongest argument against it."*
   - Default stance: `refuted=true` if evidence is insufficient or ambiguous
2. A finding is **confirmed** only if ≥2 refuters fail to refute it
3. A finding is **discarded** if ≥2 refuters succeed
4. When a confirmed finding had 1 successful refuter, include the dissenting argument in the output with a `CONTESTED` label

> This prevents plausible-but-wrong Helm deployment issues and security audit findings from reaching the final output. The 3-vote panel eliminates single-point hallucination without requiring unanimity.

## Cross-System Consistency Validator

After all parallel agents (Deployment Upgrader, Diagnostics Agent, Migration Executor, Security Auditor) complete, but **before** synthesis:

Run one **Consistency Validator Agent** with all parallel outputs that:
- Flags any pair of recommendations that logically contradict each other
  *(example: Security Auditor recommends removing a permissive Network Policy while Diagnostics Agent identifies that same policy as required for cross-namespace service communication)*
- Notes where one agent's output is a prerequisite for another agent's recommendation
- Passes contradictions to the Synthesis Agent as `MUST_RESOLVE` items
- Passes missing prerequisites as `SEQUENCING_REQUIRED` items

## Synthesis Agent (Upgraded)

The synthesis step actively resolves rather than aggregates:

1. **`MUST_RESOLVE` contradictions**: Pick the better recommendation, annotate the reasoning, preserve the dissenting view as a footnote
2. **`SEQUENCING_REQUIRED` items**: Re-order the unified deployment action plan so prerequisites appear before the steps that depend on them
3. **Confidence calibration**: Label each finding `HIGH` / `MEDIUM` / `LOW` confidence based on refuter panel outcomes
4. **Gap analysis**: Note any analysis dimension not covered by any of the parallel agents — these are blind spots, not confirmed negatives
