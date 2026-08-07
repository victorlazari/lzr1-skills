---
name: lerian-helm
description: Execute Helm deployments, database migrations, and security validation enforcing Kubernetes Restricted Pod Security Standards.
---

# Lerian Studio Helm Deployments

## Scope and Triggers
Use this skill to deploy, upgrade, or troubleshoot Lerian Studio applications via Helm. It activates when managing `values.yaml` overrides, executing database migrations with `golang-migrate`, or enforcing Kubernetes Restricted Pod Security Standards.
**Non-goals:** This skill does not perform deep container image vulnerability scanning (use `trivy-scanner`) or comprehensive application code security reviews (use `security-review`).

## Preconditions
Before executing any Helm commands, verify:
1. Target Kubernetes environment and namespace access.
2. Existing Helm releases (`helm list -n <namespace>`).
3. Current database states and connection details.
4. Tool versions: Helm (v3+) and `golang-migrate` (v4+).

## Source Freshness
Volatile facts such as supported Helm versions, Kubernetes API deprecations, and `golang-migrate` syntax must be verified against official documentation before execution. See `references/complete-reference.md` for authoritative sources (Verified: 2026-08-07).

## Workflow
1. **Pre-Deployment Assessment:** Verify target environment, existing releases, and database states; check tool versions (Helm, golang-migrate v4).
2. **Configuration Tuning:** Customize `values.yaml`, ensuring compliance with Restricted Pod Security Standards.
3. **Security Validation:** Run `scripts/validate-security.sh` to enforce `allowPrivilegeEscalation: false` and `seccompProfile: RuntimeDefault`. Stop if validation fails.
4. **Dry Run:** Execute `helm upgrade --dry-run` and review output.
5. **Execution:** Apply Helm upgrade with `--wait` and `--timeout`. Monitor hooks.
6. **Validation:** Verify pod readiness and service availability.
7. **Post-Deployment:** Confirm migration success and document interventions.

## Safety
- **Read-only discovery:** Always inspect the environment (`helm get values`, `kubectl get pods`) before making changes.
- **Confirmation required:** Explicit user confirmation is required before applying database migrations, executing destructive actions (e.g., `helm uninstall`), or modifying production resources.
- **Dry-run mandate:** `helm upgrade --dry-run` must be executed and reviewed before any mutating Helm command.

## Validation
- Syntax checks: Run `scripts/validate-security.sh` on `values.yaml` before deployment.
- Postcondition verification: Ensure all pods are `Running` or `Completed` and services are reachable.

## Failure Handling
- If a deployment fails, inspect pod logs (`kubectl logs`) and events (`kubectl describe pod`).
- Do not repeat a failed `helm upgrade` without modifying the configuration or addressing the underlying issue.
- Rollback using `helm rollback <release> <revision>` if a deployment cannot be fixed promptly.

## Output Contract
The result must include:
- A summary of actions taken (e.g., upgraded release X to version Y).
- Evidence of successful deployment (e.g., pod status, service endpoints).
- Any warnings or manual interventions required.

## Resources
- [Complete Reference](references/complete-reference.md): Authoritative sources, Bitnami OCI artifact transition, and golang-migrate v4 specifics.
- [Security Validation Script](scripts/validate-security.sh): Automates PodSecurityContext checks against the Restricted profile.

## Orchestration
Parallel execution is supported for independent environments or namespaces. Ensure inputs are clearly defined and conflicts (e.g., concurrent database migrations) are avoided. Synthesize results into a single deployment report.
