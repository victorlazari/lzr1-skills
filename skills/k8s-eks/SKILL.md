---
name: k8s-eks
description: Advanced Kubernetes and AWS EKS operations, troubleshooting, and architecture specialist. Triggers on complex EKS incidents, networking issues, and cluster management tasks.
---

# Kubernetes and AWS EKS Specialist

## Scope and Triggers

Use this skill when you need to:
- Diagnose and resolve complex Kubernetes production incidents (e.g., CrashLoopBackOff, OOMKilled, Node NotReady).
- Troubleshoot AWS EKS specific integrations like VPC CNI, IP exhaustion, and IAM Roles for Service Accounts (IRSA).
- Manage and debug advanced networking configurations including eBPF, Cilium, Cluster Mesh, and CoreDNS.
- Operate and recover Custom Controllers, the Operator pattern, and GitOps workflows (ArgoCD/Flux).
- Architect, provision, and scale EKS clusters using Infrastructure as Code (Terraform), Karpenter, and advanced compute options (Spot, Fargate).
- Perform deep system-level debugging using ephemeral containers, tcpdump, strace, and CloudWatch Logs Insights.

**Explicit Non-Goals:**
- Do not use for basic application deployment or simple `kubectl` commands that do not require deep EKS knowledge.
- Do not use for managing AWS resources outside the context of EKS (e.g., general EC2 or VPC management).

## Preconditions

Before acting, detect the target cluster, environment, versions, permissions, inputs, constraints, and user intent:
1. Verify `kubectl` and `aws` CLI are installed and configured.
2. Check the current context and cluster access (`kubectl config current-context`).
3. Verify the EKS cluster version and supported features.
4. Confirm the user's intent and the specific issue or operation required.

## Source Freshness

Volatile facts (e.g., supported versions, specific command flags) must be verified against current upstream documentation before applying destructive or production-impacting actions.
- **Verified against upstream:** 2026-08-07
- **Authoritative Sources:**
  - Amazon EKS User Guide: https://docs.aws.amazon.com/eks/latest/userguide/what-is-eks.html
  - Kubernetes Documentation: https://kubernetes.io/docs/home/
  - Cilium Documentation: https://docs.cilium.io/en/stable/
  - Karpenter Documentation: https://karpenter.sh/
  - Argo CD Documentation: https://argo-cd.readthedocs.io/en/stable/

## Workflow

1. **Detect Target and Intent:** Identify the target cluster, environment, and user intent.
2. **Baseline Validation:** Run `scripts/verify-cluster-health.sh` to establish the baseline state of the cluster.
3. **Identify Issue:** Pinpoint the specific issue or operation (e.g., Operator failure, eBPF exhaustion, Node NotReady).
4. **Consult References:** Consult `references/advanced-operations.md` for specific troubleshooting steps and deep technical details if needed.
5. **Propose Remediation:** Propose remediation actions to the user. **Require explicit confirmation for any destructive changes** (e.g., deleting namespaces, scaling operators to zero).
6. **Execute Actions:** Execute the approved actions, using dry-run or preview modes where feasible.
7. **Post-Validation:** Re-run `scripts/verify-cluster-health.sh` to validate the fix and ensure the cluster has returned to a healthy state.
8. **Stop Condition:** Stop when the cluster returns to a healthy state or escalate if the issue persists.

## Safety

- **Read-only discovery must precede any mutation.**
- **Destructive actions require explicit user confirmation.** This includes deleting namespaces, scaling operators to zero, or modifying critical cluster configurations.
- All scripts and commands must support a dry-run mode or equivalent preview whenever feasible.
- Provide explicit rollback instructions for failed operations.

## Validation

- Define syntax checks, dry runs, tests, evidence capture, and postcondition verification.
- Verify cluster health before and after any significant change using `scripts/verify-cluster-health.sh`.

## Failure Handling

- If an operation fails, diagnose the error using logs and events.
- Choose alternative remediation steps based on the diagnosis.
- Roll back any partial changes to restore the previous state.
- Do not repeat a failed action unchanged.

## Output Contract

The result must include:
- A structured summary of the issue and the actions taken.
- Evidence of the cluster state before and after the operation (e.g., output from `verify-cluster-health.sh`).
- Severity/confidence level of the findings.
- Actionable next steps or recommendations for preventing future occurrences.

## Resources

- [Advanced Operations Guide](./references/advanced-operations.md): Deep technical details, troubleshooting scenarios, and advanced CLI reference.
- [Verify Cluster Health Script](./scripts/verify-cluster-health.sh): Deterministic script to perform read-only discovery and validation of cluster state.

## Orchestration (Sub-Agent Spawning)

This skill supports spawning sub-agents for parallel execution when tasks can be decomposed (e.g., multiple clusters to upgrade, fleet-wide security audit).
- **Cross-skill routing:**
  - Route to `trivy-scanner` when scanning container images or Kubernetes manifests for vulnerabilities.
  - Route to `security-review` when performing a comprehensive security audit of the cluster architecture or RBAC policies.
- **Adversarial Verification Panel:** For each significant finding, spawn 3 independent Refuter Agents to challenge the finding. A finding is confirmed only if ≥2 refuters fail to refute it.
- **Cross-System Consistency Validator:** Run a Consistency Validator Agent to flag contradictions and missing prerequisites before synthesis.
- **Synthesis Agent:** Actively resolve contradictions, re-order recommendations based on prerequisites, calibrate confidence, and perform gap analysis.
