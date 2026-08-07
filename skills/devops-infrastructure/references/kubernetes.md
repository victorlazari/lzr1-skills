# Kubernetes

**Verified against upstream: 2026-08-07**

## Table of Contents
1. Cluster Architecture
2. Workload Management
3. Networking
4. Storage
5. Security & Policy-as-Code
6. AIOps & Self-Healing

---

## 1. Cluster Architecture

- Control Plane: API Server, etcd, Scheduler, Controller Manager
- Worker Nodes: Kubelet, Kube-proxy, Container Runtime

## 2. Workload Management

- Deployments, StatefulSets, DaemonSets, Jobs, CronJobs
- Horizontal Pod Autoscaler (HPA), Vertical Pod Autoscaler (VPA)

## 3. Networking

- Services (ClusterIP, NodePort, LoadBalancer)
- Ingress Controllers, Gateway API
- Network Policies

## 4. Storage

- Persistent Volumes (PV), Persistent Volume Claims (PVC)
- Storage Classes, CSI Drivers

## 5. Security & Policy-as-Code

- RBAC (Roles, RoleBindings, ClusterRoles, ClusterRoleBindings)
- Pod Security Standards
- **Policy-as-Code**: Kyverno, OPA Gatekeeper for enforcing organizational policies.

## 6. AIOps & Self-Healing

- Implement self-healing clusters using operators and automated remediation tools.
- Leverage AIOps for predictive scaling and anomaly detection.
