# Lerian Studio Helm Deployments: Complete Reference

This document serves as the definitive, expert-level reference for managing, deploying, and troubleshooting Lerian Studio applications via Helm in enterprise-grade Kubernetes environments. It consolidates advanced operational strategies, CLI references, configuration schemas, security audit procedures, and deep-dive troubleshooting guides.

## 1. Advanced Lerian Helm Operations

In the realm of enterprise-grade Kubernetes deployments, mastering the Lerian Studio Helm charts is a critical competency for tech support operations and DevOps engineering teams. As organizations scale their infrastructure to handle massive datasets, high concurrency, and stringent uptime requirements, the default configurations provided by standard Helm charts are often insufficient.

### 1.1 Custom `values.yaml` Overrides for Production

The `values.yaml` file is the heart of any Helm chart. In production environments, relying on the default `values.yaml` is a recipe for disaster. Custom overrides are essential for tailoring the deployment to the specific needs of the infrastructure.

**Structuring Overrides for Maintainability:**
Best practices dictate splitting overrides into logical, environment-specific files:
- `values-base.yaml`: Contains common configurations applicable across all environments.
- `values-prod.yaml`: Contains production-specific settings such as resource limits, replica counts, and ingress configurations.
- `values-secrets.yaml`: Contains sensitive information managed via tools like Helm Secrets or SOPS.

**Resource Limits and Requests for Huge Datasets:**
Accurate configuration of resource requests and limits is critical. Failing to set appropriate limits can lead to CPU throttling, Out-Of-Memory (OOM) kills, and cascading failures.

```yaml
api:
  resources:
    requests:
      cpu: "2000m"
      memory: "4Gi"
    limits:
      cpu: "4000m"
      memory: "8Gi"
```

**Handling Timeouts and Aggressive Network Policies:**
In high-throughput environments, network timeouts and aggressive connection handling are common sources of instability. Custom overrides must address these issues by configuring appropriate timeout values for ingress controllers, internal service communication, and database connections.

### 1.2 Multi-Tenant Configurations

Lerian Studio is frequently deployed in multi-tenant environments. Implementing a robust multi-tenant architecture requires careful consideration of namespace isolation, resource allocation, and routing.

**Namespace Isolation and Security:**
Each tenant should be deployed into a dedicated namespace. To enforce security and prevent cross-tenant interference, NetworkPolicies must be implemented.

**Ingress and Routing Strategies:**
Host-Based Routing is the preferred approach for production environments, as it provides cleaner isolation and simplifies SSL/TLS certificate management.

### 1.3 Managing External Databases vs. Bitnami Subcharts

The Lerian Helm chart often relies on backend databases. Choosing between embedded Bitnami subcharts and external databases is crucial for production stability.

**The External Database Approach:**
For production environments handling massive datasets, connecting to an external database (e.g., Amazon RDS, Google Cloud SQL) is strongly recommended. It decouples the application lifecycle from the database lifecycle, allowing for safer Helm upgrades and independent scaling.

**Connection Pooling and Timeouts:**
When using external databases, managing connection pooling is critical. Tech support engineers must configure connection pooling tools (e.g., PgBouncer) and tune application-level connection timeouts to fail fast and retry gracefully.

### 1.4 Zero-Downtime Upgrades

Achieving zero-downtime upgrades requires a combination of Kubernetes deployment strategies, robust health checks, and careful handling of database schema changes.

**Rolling Updates Strategy:**
To optimize rolling updates, configure the `maxSurge` and `maxUnavailable` parameters in `values.yaml`. Setting `maxUnavailable: 0` ensures continuous availability.

**Readiness and Liveness Probes:**
Probes must be accurately configured to hit a dedicated health check endpoint (e.g., `/healthz`) that verifies the application's connection to critical dependencies.

**Handling Schema Changes During Upgrades:**
Schema changes must be backward compatible. This often requires a multi-step deployment process involving deploying a new version supporting both schemas, applying the migration, and then deploying a version exclusively using the new schema.

### 1.5 Custom Migration Strategies

When dealing with tables containing millions or billions of rows, simple `ALTER TABLE` statements can cause massive downtime.

**Pre-Install and Post-Install Hooks:**
Helm lifecycle hooks allow custom scripts or jobs to be executed at specific points. For database migrations, `pre-install` and `pre-upgrade` hooks are invaluable.

**Handling Massive Datasets During Migrations:**
Employ advanced migration strategies such as online schema change tools (e.g., `gh-ost`, `pg_repack`), batch processing, or shadow tables.

**Rollback Procedures and Worst-Case Scenarios:**
Have robust rollback procedures in place, including `helm rollback`, database restores (PITR), and disaster recovery (DR) failover plans.

## 2. Comprehensive CLI Reference

Operating complex microservices architectures requires a deep understanding of the underlying tools: Helm, kubectl, and golang-migrate.

### 2.1 Helm Advanced Operations

**Release Management and Rollbacks:**
- List all releases: `helm ls --all-namespaces --all`
- Rollback to previous revision: `helm rollback <release-name> 0 -n <namespace>`
- Rollback with timeout: `helm rollback <release-name> <revision-number> -n <namespace> --wait --timeout 10m`
- Force upgrade: `helm upgrade <release-name> <chart-path> -n <namespace> --force --wait --timeout 15m`

**Debugging and Dry Runs:**
- Render templates locally: `helm template <release-name> <chart-path> -n <namespace> --set key=value > rendered.yaml`
- Dry run upgrade: `helm upgrade <release-name> <chart-path> -n <namespace> --dry-run --debug`
- Get deployed manifest: `helm get manifest <release-name> -n <namespace>`

**Advanced Helm One-Liners:**
- Uninstall failed releases: `helm ls -n <namespace> --failed -q | xargs -I {} helm uninstall {} -n <namespace>`
- Extract deployed values: `helm get values <release-name> -n <namespace> -o yaml > current-values.yaml`

### 2.2 kubectl Mastery

**Resource Troubleshooting and Inspection:**
- Get all resources sorted by creation: `kubectl get all -n <namespace> --sort-by=.metadata.creationTimestamp`
- Extract pod events: `kubectl describe pod <pod-name> -n <namespace> | grep -A 20 "Events:"`
- Check resource usage: `kubectl top pods -n <namespace> --containers`

**Log Extraction and Analysis:**
- Tail logs for specific container: `kubectl logs -f <pod-name> -c <container-name> -n <namespace>`
- Get logs from crashed container: `kubectl logs <pod-name> -c <container-name> -n <namespace> --previous`
- Stream logs by label: `kubectl logs -f -l app=lerian-backend -n <namespace> --all-containers=true --max-log-requests=10`

**Network Troubleshooting:**
- Run debug pod: `kubectl run -i --tty --rm debug --image=nicolaka/netshoot --restart=Never -- sh`
- Port-forward service: `kubectl port-forward svc/<service-name> 8080:80 -n <namespace>`

**Advanced kubectl One-Liners:**
- Delete evicted pods: `kubectl get pods -n <namespace> | grep Evicted | awk '{print $1}' | xargs kubectl delete pod -n <namespace>`
- Scale deployments to zero (Emergency Stop): `kubectl get deployments -n <namespace> -o name | xargs -I {} kubectl scale {} --replicas=0 -n <namespace>`

### 2.3 golang-migrate Operations

**Migration Execution and Rollbacks:**
- Apply all pending up migrations: `migrate -path ./migrations -database "$DATABASE_URL" up`
- Rollback last applied migration: `migrate -path ./migrations -database "$DATABASE_URL" down 1`

**Handling Dirty States and Failures:**
- Force database version: `migrate -path ./migrations -database "$DATABASE_URL" force <version-number>`
- Check current version: `migrate -path ./migrations -database "$DATABASE_URL" version`

## 3. Configuration Schemas and Tuning

Properly configuring resource requests and limits is the foundation of a stable Kubernetes deployment.

### 3.1 Resource Requests and Limits Tuning

- **CPU Allocation:** Set CPU requests based on baseline usage. In modern environments, removing CPU limits entirely or setting them very high is preferred to avoid aggressive throttling.
- **Memory Allocation:** Set memory requests to average consumption plus a 20% buffer. Memory limits must be strictly enforced (1.5x to 2x the request) to prevent node starvation.

### 3.2 Horizontal Pod Autoscaling (HPA)

Configure HPA correctly to handle traffic spikes without over-provisioning resources. Use custom metrics (e.g., HTTP request rate, queue length) in addition to CPU utilization. Configure rapid scale-up policies and stabilization windows for scale-down events.

### 3.3 Pod Disruption Budgets (PDBs)

Define PDBs to guarantee a minimum number of available pods (`minAvailable`) or a maximum number of unavailable pods (`maxUnavailable`) during voluntary disruptions.

### 3.4 Timeout Configurations

Configure strict timeouts for HTTP clients, database connection pools, and ingress controllers to prevent cascading failures.

## 4. Security Audit Procedures

Security is the foundational pillar upon which all production operations rest.

### 4.1 Auditing `values.yaml` and Secret Management

- **Identify Hardcoded Secrets:** Scan `values.yaml` and chart templates for plaintext sensitive data.
- **Transition to External Secret Stores:** Mandate the use of external secret management solutions (e.g., HashiCorp Vault, AWS Secrets Manager) integrated via the External Secrets Operator (ESO).
- **Handling Secrets During Migrations:** Ensure migration jobs use ephemeral credentials or IAM roles for service accounts (IRSA).

### 4.2 Enforcing Network Policies

- **Default Deny Policy:** Implement a "default deny" policy blocking all ingress and egress traffic to all pods in the namespace.
- **Explicit Ingress and Egress Rules:** Explicitly define allowed communication paths for application pods, restricting access to authorized sources and required external services.

### 4.3 Hardening `PodSecurityContext`

- **Run as Non-Root:** Ensure containers do not run as the root user (`runAsNonRoot: true`).
- **Restrict Capabilities:** Drop all capabilities by default (`capabilities: drop: ["ALL"]`) and prevent privilege escalation (`allowPrivilegeEscalation: false`).
- **Read-Only Root Filesystem:** Enforce `readOnlyRootFilesystem: true` wherever possible.

### 4.4 Securing External Database Connections

- **Enforce TLS/SSL Encryption:** Ensure all data in transit between the application and the external database is encrypted.
- **Authentication and Authorization:** Use strong passwords or IAM-based authentication and enforce least-privilege authorization for database users.

## 5. Deep Dive into Helm Internals

Understanding the deep internals of Lerian Helm charts is an absolute requirement for diagnosing production incidents.

### 5.1 Helm Chart Structure and `_helpers.tpl`

The Lerian Helm chart is structured as an umbrella chart with multiple subcharts. The `_helpers.tpl` file contains reusable Go template functions that generate standard labels and names. Be aware of silent truncation issues if release names combined with subchart names exceed 63 characters.

### 5.2 Dependency Management and Initialization Ordering

Lerian uses init containers to poll dependencies before allowing the main application container to start. This ensures proper startup order and helps prevent cascading failures (e.g., the "Thundering Herd" problem).

### 5.3 Managing Secrets and Certificates

Lerian uses `cert-manager` and `external-secrets` integrated into the Helm charts. Monitor `Certificate` and `CertificateRequest` resources to prevent outages caused by expired certificates.

## 6. Deep Troubleshooting Guide

Develop a methodical troubleshooting approach rooted in layered investigation and correlation of logs, metrics, and event histories.

### 6.1 Scenario: Midaz Pod CrashLoopBackOff Immediately After Upgrade

**Investigation:**
- Check pod-level events and container logs.
- Confirm resource requests and limits.
- Check recent Helm `pre-upgrade` hooks for DB schema locks.
- Validate ConfigMaps and Secrets.
- Check Init Containers status.

**Remediation:**
- Rollback Helm release to last known good version.
- Adjust resource limits.
- Correct ConfigMap or Secret values.
- Fix or disable failing plugins.

### 6.2 Scenario: Fetcher Job Hangs on Massive Dataset Import

**Investigation:**
- Inspect Fetcher pod logs for retries or timeouts.
- Confirm resource allocation and check for throttling.
- Check network policies and connectivity.
- Review Helm values overrides for batch size and parallelism.

**Remediation:**
- Tune `fetcher.batchSize` and `fetcher.parallelWorkers`.
- Implement HPA or controlled parallelism.
- Coordinate with network team.
- Use `initContainers` for environment pre-checks.

### 6.3 Advanced Database Migration Recovery

**Recovery Procedure:**
1. Identify the failed migration phase.
2. Confirm if schema changes were partially applied.
3. Restore database from backup if necessary.
4. Manually run pending migrations step-by-step.
5. Update Helm Chart version and embedded scripts.
6. Re-deploy Helm chart with `--force`.
7. Monitor application connectivity.
