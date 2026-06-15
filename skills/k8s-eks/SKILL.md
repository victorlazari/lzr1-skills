---
name: k8s-eks
description: Advanced Kubernetes and AWS EKS operations, troubleshooting, and architecture specialist.
---

# Kubernetes and AWS EKS Specialist

## When to Use

Use this skill when you need to:
- Diagnose and resolve complex Kubernetes production incidents (e.g., CrashLoopBackOff, OOMKilled, Node NotReady).
- Troubleshoot AWS EKS specific integrations like VPC CNI, IP exhaustion, and IAM Roles for Service Accounts (IRSA).
- Manage and debug advanced networking configurations including eBPF, Cilium, Cluster Mesh, and CoreDNS.
- Operate and recover Custom Controllers, the Operator pattern, and GitOps workflows (ArgoCD/Flux).
- Architect, provision, and scale EKS clusters using Infrastructure as Code (Terraform), Karpenter, and advanced compute options (Spot, Fargate).
- Perform deep system-level debugging using ephemeral containers, tcpdump, strace, and CloudWatch Logs Insights.

## Sub-Agent Spawning

This skill supports spawning sub-agents for parallel execution when tasks can be decomposed:

| Trigger Condition | Sub-Agent Type | Purpose |
|---|---|---|
| Multiple clusters to upgrade | Cluster Upgrader | Parallel execution of EKS control plane and node group upgrades |
| Fleet-wide security audit | Security Auditor | Parallel review of RBAC, IRSA, and Pod Security Standards across namespaces |
| Distributed network troubleshooting | Network Diagnostics Agent | Parallel packet capture and connectivity testing across multiple nodes/pods |
| Bulk log analysis | Log Analyzer | Parallel querying of CloudWatch Logs Insights for API server or application errors |
| Multi-region GitOps sync | GitOps Reconciler | Parallel verification of ArgoCD/Flux synchronization status across regions |

### Spawning Rules
- Spawn when 3+ independent items (clusters, namespaces, nodes, applications) need the same operation.
- Each sub-agent receives: context (cluster details, credentials), specific target (e.g., namespace or node ID), and success criteria.
- Results are aggregated and cross-referenced for conflicts or systemic issues.
- Maximum concurrent sub-agents: 10.

## Workflow

1. **Incident Triage & Identification:**
   - Gather symptoms (e.g., pods pending, network timeouts, API server unresponsive).
   - Identify the scope (single pod, node, namespace, or cluster-wide).
2. **Initial Diagnostics:**
   - Use `kubectl describe`, `kubectl logs`, and `kubectl get events` to pinpoint immediate errors.
   - Check node status and resource utilization (CPU/Memory/Disk).
3. **Deep Dive Analysis:**
   - **Networking:** Inspect VPC CNI logs, check IP availability, verify SNAT, and analyze CoreDNS performance.
   - **Compute/Scaling:** Review Karpenter provisioner logs, ASG status, and HPA/VPA configurations.
   - **Security/Access:** Validate IRSA annotations, trust policies, and RBAC permissions.
   - **Advanced Components:** Check Operator logs, eBPF map utilization, and GitOps sync status.
4. **Remediation & Recovery:**
   - Apply targeted fixes (e.g., restart DaemonSets, patch finalizers, adjust resource limits).
   - For severe issues, execute disaster recovery protocols (e.g., isolate clusters in a mesh, restore etcd, scale down destructive operators).
5. **Post-Incident Review:**
   - Document the root cause and remediation steps.
   - Implement preventative measures (e.g., adjust alerts, update Network Policies, refine resource requests).

## Core Principles

- **Declarative Infrastructure:** All cluster state and infrastructure must be defined as code (GitOps, Terraform) to ensure reproducibility and auditability.
- **Least Privilege:** Enforce strict RBAC, IRSA, and Network Policies to minimize the blast radius of security incidents.
- **Proactive Observability:** Rely on comprehensive metrics, logs, and traces (Prometheus, CloudWatch, Hubble) rather than reactive debugging.
- **Automated Scaling:** Utilize Karpenter and HPA to dynamically adjust resources based on actual workload demands, avoiding manual intervention.
- **Resilience by Design:** Architect for failure using multi-AZ deployments, Cluster Mesh for cross-region failover, and robust backup strategies.

## Key References

- [Complete Reference Guide](./references/complete-reference.md)
- [Reading List](./references/reading-list.md)
