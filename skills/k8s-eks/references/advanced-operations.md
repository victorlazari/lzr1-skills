# Advanced Kubernetes and EKS Operations

**Verified against upstream:** 2026-08-07

## Table of Contents
1. [Custom Controllers and the Operator Pattern](#1-custom-controllers-and-the-operator-pattern)
2. [eBPF Networking and Cilium in EKS](#2-ebpf-networking-and-cilium-in-eks)
3. [Multi-Cluster Architectures and Cluster Mesh](#3-multi-cluster-architectures-and-cluster-mesh)
4. [GitOps with ArgoCD and Flux](#4-gitops-with-argocd-and-flux)
5. [Advanced Scheduling and Resource Management](#5-advanced-scheduling-and-resource-management)
6. [CLI Reference and One-Liners](#6-cli-reference-and-one-liners)
7. [Worst-Case Scenarios and Incident Response](#7-worst-case-scenarios-and-incident-response)

## 1. Custom Controllers and the Operator Pattern

The Operator pattern is the cornerstone of Kubernetes extensibility. By combining Custom Resource Definitions (CRDs) with custom controllers, organizations can encode human operational knowledge into software.

### Tech Support Scenarios: Operator Failures

**Scenario 1: The Crash-Looping Operator and Orphaned Resources**
When an Operator encounters an unhandled exception, it will crash and be restarted by the kubelet. If the Operator uses finalizers to manage external resources, a crash loop can prevent the finalizer from being removed. This results in the Custom Resource being stuck in a `Terminating` state indefinitely.
*Resolution:* Inspect the Operator logs to identify the panic, patch the Custom Resource to remove the finalizer manually (using `kubectl patch`), and ensure the external resource is cleaned up out-of-band.

**Scenario 2: Stale Caches and Split-Brain Reconciliation**
If an Operator's RBAC permissions are misconfigured, it may fail to establish a watch on a specific resource type. The informer cache will not populate, and the Operator will assume the resources do not exist.
*Resolution:* Audit the Operator's ServiceAccount permissions. Check the API server audit logs for `403 Forbidden` errors. Restart the Operator to force a full re-list and cache synchronization.

## 2. eBPF Networking and Cilium in EKS

Extended Berkeley Packet Filter (eBPF) provides unprecedented performance, security, and observability. In EKS, replacing the traditional `kube-proxy` with an eBPF-based CNI like Cilium is a common pattern for high-scale environments.

### Tech Support Scenarios: eBPF Networking

**Scenario 1: eBPF Map Exhaustion**
eBPF programs store state in data structures called maps. If a cluster experiences a massive surge in connections, these maps can reach their capacity limits. New connections will be silently dropped at the kernel level.
*Resolution:* Use `bpftool` or the Cilium CLI (`cilium bpf map list`) to inspect map utilization. Increase the map size limits in the Cilium configuration and perform a rolling restart of the Cilium DaemonSet.

**Scenario 2: Complete Network Partition**
A misconfigured cluster-wide CiliumNetworkPolicy or a failure in the Cilium operator that corrupts the eBPF maps across all nodes can result in a complete network partition.
*Mitigation and Recovery:* Recovery requires out-of-band access. SSH directly into the EKS worker nodes, manually bypass or delete the eBPF programs using `tc` and `bpftool`, or forcefully remove the Cilium DaemonSet manifests directly from the kubelet's static pod path.

## 3. Multi-Cluster Architectures and Cluster Mesh

A Cluster Mesh connects multiple Kubernetes clusters at the network layer, allowing pods in Cluster A to communicate directly with pods in Cluster B.

### Tech Support Scenarios: Cluster Mesh Operations

**Scenario 1: Overlapping Pod CIDRs**
The Pod and Service CIDRs across all participating clusters must be non-overlapping. If two clusters are provisioned with the same CIDR block and joined to the mesh, routing loops and asymmetric routing will occur.
*Resolution:* Immediately disconnect the offending cluster from the mesh. Rebuild one of the clusters with a unique CIDR block.

**Scenario 2: Control Plane Synchronization Failures**
If the etcd cluster managing the mesh state becomes degraded, the global service endpoints will become stale.
*Resolution:* Verify the health of the mesh etcd cluster. Check the Cilium agent logs for `clustermesh` synchronization errors. Restarting the `clustermesh-apiserver` pods can often force a state reconciliation.

## 4. GitOps with ArgoCD and Flux

GitOps uses Git as the single source of truth for declarative infrastructure and applications.

### Tech Support Scenarios: GitOps Failures

**Scenario 1: The Sync Loop of Death**
If a resource in the cluster is continuously modified by an external process in a way that conflicts with the state defined in Git, the GitOps controller will enter an infinite sync loop.
*Resolution:* Identify the conflicting controller or webhook. Configure the GitOps tool to ignore the specific fields being mutated or update the Git repository to match the mutated state.

**Scenario 2: The Accidental Cluster Wipe**
If a user accidentally deletes the root application manifest in the Git repository, the GitOps controller will execute a cascading deletion of all resources in the EKS cluster.
*Mitigation and Recovery:* Enable branch protection rules in Git and configure the GitOps controller to prevent cascading deletions. If a wipe occurs, revert the Git commit and wait for the synchronization process to rebuild the cluster.

## 5. Advanced Scheduling and Resource Management

Efficiently utilizing compute resources in EKS requires moving beyond basic resource requests and limits.

### Tech Support Scenarios: Scheduling Nightmares

**Scenario 1: The Unschedulable Pod Backlog**
A massive influx of pods with strict affinity rules or resource requests that exceed the available capacity will result in a backlog of `Pending` pods.
*Resolution:* Analyze the scheduling events (`kubectl describe pod`). Relax constraints if they are too strict. If capacity is genuinely exhausted, increase AWS limits or adjust the Cluster Autoscaler configuration.

**Scenario 2: Karpenter/Autoscaler Thrashing**
Conflicting scheduling constraints or rapid fluctuations in workload demand can cause Karpenter to rapidly provision and deprovision nodes.
*Mitigation and Recovery:* Pause the node provisioner. Analyze the Karpenter logs and adjust the consolidation policies and TTL settings to introduce hysteresis.

## 6. CLI Reference and One-Liners

### `kubectl` Advanced Operations

**Identify Nodes with High Resource Pressure:**
```bash
kubectl get nodes -o custom-columns="NAME:.metadata.name,CPU_ALLOCATABLE:.status.allocatable.cpu,MEMORY_ALLOCATABLE:.status.allocatable.memory,STATUS:.status.conditions[?(@.type=='Ready')].status"
```

**Find Nodes that are NotReady and Extract the Reason:**
```bash
kubectl get nodes --field-selector=status.phase!=Running -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.status.conditions[?(@.type=="Ready")].message}{"\n"}{end}'
```

**Drain a Node Aggressively:**
```bash
kubectl drain <node-name> --ignore-daemonsets --delete-emptydir-data --force --grace-period=0
```

**List All Pods in CrashLoopBackOff or Error State:**
```bash
kubectl get pods -A --field-selector=status.phase!=Running | grep -v 'Completed'
```

### `eksctl` Production Management

**Upgrade the Control Plane to a Specific Version:**
```bash
eksctl upgrade cluster --name <cluster-name> --version 1.28 --approve
```

**Scale a Managed Node Group:**
```bash
eksctl scale nodegroup --cluster <cluster-name> --name <nodegroup-name> --nodes 5 --nodes-min 3 --nodes-max 10
```

### `aws eks` CLI for Control Plane

**Generate or Update Kubeconfig:**
```bash
aws eks update-kubeconfig --region <region> --name <cluster-name> --alias <custom-alias>
```

**Enable All Control Plane Logs:**
```bash
aws eks update-cluster-config --region <region> --name <cluster-name> --logging '{"clusterLogging":[{"types":["api","audit","authenticator","controllerManager","scheduler"],"enable":true}]}'
```

## 7. Worst-Case Scenarios and Incident Response

### API Server Unresponsive
1. Verify network connectivity to the EKS endpoint.
2. Check AWS Service Health Dashboard for regional EKS outages.
3. Review CloudWatch metrics for the EKS control plane.
4. Escalate to AWS Support immediately if the issue persists.

### Widespread Node NotReady
1. Check Kubelet Status using SSM Session Manager or SSH.
2. Verify VPC CNI logs (`aws-node` daemonset).
3. Check Disk Pressure on the nodes.
4. Review Auto Scaling Group (ASG) health checks.

### CoreDNS CrashLoopBackOff
1. Check CoreDNS Logs (`kubectl logs -n kube-system -l k8s-app=kube-dns`).
2. Verify Node Connectivity to the API server.
3. Restart CoreDNS (`kubectl rollout restart deployment coredns -n kube-system`).
4. Check Resource Limits to ensure CoreDNS is not being OOMKilled.

### Exhaustion of VPC IP Addresses
1. Check Subnet IP Availability using the AWS CLI.
2. Enable Custom Networking to use secondary subnets for pod IPs.
3. Reduce `WARM_IP_TARGET` in the VPC CNI environment variables.
