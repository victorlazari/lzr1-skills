# Specialist: 37-k8s-eks

## === FILE: 37-k8s-eks-advanced.md ===
# Advanced Kubernetes and EKS Operations: The Specialist Guide

## 1. Introduction to Advanced EKS Operations

The evolution of Kubernetes from a container orchestration platform to a universal control plane has fundamentally shifted the responsibilities of platform engineers and technical support specialists. In modern enterprise environments, particularly those leveraging Amazon Elastic Kubernetes Service (EKS), basic administration tasks such as deploying pods and configuring basic services are no longer sufficient. The modern EKS specialist must navigate a complex ecosystem of custom controllers, advanced networking paradigms, multi-cluster architectures, and declarative continuous delivery models.

This comprehensive guide is designed for technical support operations and platform engineering specialists who are responsible for maintaining, troubleshooting, and recovering advanced Kubernetes environments. It focuses on production operations, worst-case scenarios, and the deep technical knowledge required to resolve the most complex incidents. The topics covered herein—ranging from the Operator pattern and eBPF networking to Cluster Mesh, GitOps, and advanced scheduling—represent the pinnacle of Kubernetes operational maturity.

As a specialist, your role is not merely to keep the lights on, but to understand the intricate interactions between these advanced components. When an eBPF map is exhausted, when an Operator enters a crash loop and orphans resources, or when a GitOps controller syncs a destructive change across a fleet of clusters, you must possess the analytical skills and systemic understanding to diagnose and remediate the issue rapidly. This document serves as your definitive reference for these high-stakes scenarios.

## 2. Custom Controllers and the Operator Pattern

The Operator pattern is the cornerstone of Kubernetes extensibility. By combining Custom Resource Definitions (CRDs) with custom controllers, organizations can encode human operational knowledge into software, automating the lifecycle management of complex stateful applications. However, this power introduces significant operational risk.

### 2.1 Understanding the Control Loop and CRDs

At its core, a Kubernetes controller operates on a continuous reconciliation loop. It observes the desired state (defined in a Custom Resource), compares it to the actual state of the cluster, and takes action to align the two. This level-triggered architecture is robust but can fail in subtle ways.

When managing CRDs in a production EKS environment, specialists must be acutely aware of API versioning and conversion webhooks. A common failure mode occurs during cluster upgrades when deprecated API versions of CRDs are no longer served by the API server, causing the associated controllers to fail silently or crash.

### 2.2 Developing and Operating Operators

Operators are typically built using frameworks like Kubebuilder or the Operator SDK. These frameworks abstract away the boilerplate of client-go, informers, and workqueues. However, understanding these underlying mechanisms is critical for troubleshooting.

For instance, the informer cache is a local, eventually consistent view of the API server's state. If the controller's cache falls out of sync due to network partitions or API server throttling, the Operator may make incorrect decisions, such as creating duplicate resources or failing to recognize that a resource has been deleted.

### 2.3 Tech Support Scenarios: Operator Failures

**Scenario 1: The Crash-Looping Operator and Orphaned Resources**
When an Operator encounters an unhandled exception (e.g., a nil pointer dereference when parsing a malformed Custom Resource), it will crash and be restarted by the kubelet. If the Operator uses finalizers to manage external resources (such as AWS RDS instances or S3 buckets), a crash loop can prevent the finalizer from being removed. This results in the Custom Resource being stuck in a `Terminating` state indefinitely, blocking namespace deletion and potentially causing resource leaks.
*Resolution:* The specialist must inspect the Operator logs to identify the panic, patch the Custom Resource to remove the finalizer manually (using `kubectl patch`), and ensure the external resource is cleaned up out-of-band to prevent billing anomalies.

**Scenario 2: Stale Caches and Split-Brain Reconciliation**
If an Operator's RBAC permissions are misconfigured, it may fail to establish a watch on a specific resource type. The informer cache will not populate, and the Operator will assume the resources do not exist. It may then attempt to recreate them, leading to conflicts and API server thrashing.
*Resolution:* Audit the Operator's ServiceAccount permissions. Check the API server audit logs for `403 Forbidden` errors originating from the Operator's pod. Restart the Operator to force a full re-list and cache synchronization.

### 2.4 Worst-Case Scenario: Destructive Reconciliation

The most severe Operator failure occurs when a bug in the reconciliation logic causes the Operator to interpret a valid state as invalid and take destructive action. For example, an Operator managing a distributed database might incorrectly determine that all nodes are out of sync and initiate a cluster-wide wipe and restore operation.
*Mitigation and Recovery:* This scenario highlights the necessity of strict RBAC scoping, comprehensive testing, and implementing "dry-run" or "pause" annotations in the CRD design. Recovery requires immediately scaling the Operator deployment to zero to halt the destructive loop, restoring the stateful data from the most recent backup, and manually reconstructing the Custom Resources to match the restored state before re-enabling the Operator.

## 3. eBPF Networking and Cilium in EKS

Extended Berkeley Packet Filter (eBPF) has revolutionized Kubernetes networking. By allowing sandboxed programs to run within the Linux kernel without modifying kernel source code or loading kernel modules, eBPF provides unprecedented performance, security, and observability. In EKS, replacing the traditional `kube-proxy` (which relies on complex and inefficient `iptables` rules) with an eBPF-based CNI like Cilium is a common pattern for high-scale environments.

### 3.1 The Shift from iptables to eBPF

Traditional `iptables`-based routing becomes a significant bottleneck as the number of services and pods scales. Every packet must traverse a linear list of rules, leading to increased latency and CPU overhead. eBPF, conversely, uses hash tables and highly optimized kernel-level execution, ensuring O(1) complexity for routing decisions regardless of cluster size.

### 3.2 Cilium Architecture on EKS

Deploying Cilium on EKS involves running the Cilium agent as a DaemonSet on every node. The agent compiles eBPF programs and attaches them to various kernel hooks (e.g., XDP, TC, socket layer). Cilium also integrates with AWS ENI (Elastic Network Interfaces) to provide native VPC routing, eliminating the need for overlay networks (like VXLAN) and improving throughput.

### 3.3 Advanced Network Policies and Hubble

Cilium extends standard Kubernetes Network Policies with CiliumNetworkPolicies, which support Layer 7 (HTTP, gRPC, Kafka) filtering and DNS-based rules. Hubble, the observability component of Cilium, leverages eBPF to provide deep visibility into network flows, dropped packets, and latency metrics without requiring sidecar proxies.

### 3.4 Tech Support Scenarios: eBPF Networking

**Scenario 1: eBPF Map Exhaustion**
eBPF programs store state in data structures called maps. If a cluster experiences a massive surge in connections or endpoints, these maps can reach their capacity limits. When a map is full, new connections will be silently dropped at the kernel level, bypassing standard application logs and traditional network monitoring tools.
*Resolution:* The specialist must use `bpftool` or the Cilium CLI (`cilium bpf map list`) to inspect map utilization. Remediation involves increasing the map size limits in the Cilium configuration (e.g., `bpf-ct-global-tcp-max`) and performing a rolling restart of the Cilium DaemonSet.

**Scenario 2: Kernel Panics and Compatibility Issues**
eBPF programs are highly dependent on the underlying Linux kernel version. If an EKS node group is upgraded to an AMI with an incompatible kernel, or if a kernel bug is triggered by a specific eBPF instruction sequence, the node may experience a kernel panic and crash.
*Resolution:* Analyze the kernel crash dumps (vmcore) if available. Revert the node group to a known stable AMI. Ensure that the Cilium version is explicitly certified for the specific kernel version running on the EKS optimized AMIs.

### 3.5 Worst-Case Scenario: Complete Network Partition

A misconfigured cluster-wide CiliumNetworkPolicy (e.g., a default deny rule applied incorrectly) or a failure in the Cilium operator that corrupts the eBPF maps across all nodes can result in a complete network partition. Pods cannot communicate with the API server, DNS resolution fails, and the cluster becomes entirely unmanageable via standard `kubectl` commands.
*Mitigation and Recovery:* Because the API server is unreachable from within the cluster, recovery requires out-of-band access. The specialist must SSH directly into the EKS worker nodes (using SSM Session Manager or bastion hosts), manually bypass or delete the eBPF programs using `tc` and `bpftool`, or forcefully remove the Cilium DaemonSet manifests directly from the kubelet's static pod path (if applicable) to restore basic connectivity.


## 4. Multi-Cluster Architectures and Cluster Mesh

As organizations scale, a single Kubernetes cluster becomes a single point of failure and a bottleneck for API server performance. Multi-cluster architectures distribute workloads across multiple EKS clusters, often spanning different AWS regions for disaster recovery and high availability.

### 4.1 The Need for Cluster Mesh

Traditional multi-cluster communication relies on ingress controllers and external load balancers, which introduce latency, complexity, and security overhead. A Cluster Mesh connects multiple Kubernetes clusters at the network layer, allowing pods in Cluster A to communicate directly with pods in Cluster B using standard Kubernetes service discovery, without traversing the public internet or complex NAT gateways.

### 4.2 Implementing Cilium Cluster Mesh

Cilium provides a robust Cluster Mesh implementation. It establishes secure IPsec or WireGuard tunnels between the nodes of participating clusters. The Cilium agents synchronize Kubernetes Service and Endpoint data across clusters via an etcd-backed control plane, enabling global service load balancing.

### 4.3 Tech Support Scenarios: Cluster Mesh Operations

**Scenario 1: Overlapping Pod CIDRs**
A fundamental requirement for Cluster Mesh is that the Pod and Service CIDRs across all participating clusters must be non-overlapping. If two clusters are provisioned with the same CIDR block and joined to the mesh, routing loops and asymmetric routing will occur, causing intermittent connection timeouts and dropped packets.
*Resolution:* This is a severe architectural flaw. The specialist must immediately disconnect the offending cluster from the mesh. The only permanent solution is to rebuild one of the clusters with a unique CIDR block, as changing the Pod CIDR of an active EKS cluster is not supported.

**Scenario 2: Control Plane Synchronization Failures**
The Cluster Mesh relies on the synchronization of Endpoint data. If the etcd cluster managing the mesh state becomes degraded or if network connectivity between the control planes is interrupted, the global service endpoints will become stale. Traffic may be routed to pods that have been terminated in a remote cluster.
*Resolution:* Verify the health of the mesh etcd cluster. Check the Cilium agent logs for `clustermesh` synchronization errors. Restarting the `clustermesh-apiserver` pods can often force a state reconciliation.

### 4.4 Worst-Case Scenario: Cascading Failure via Global Services

In a tightly coupled Cluster Mesh, a failure in one cluster can cascade to others. If a critical service in Cluster A fails, the global load balancing mechanism will route all traffic for that service to the replicas in Cluster B. If Cluster B is not provisioned to handle the aggregate load, its pods will become overwhelmed, fail health checks, and crash, leading to a total global outage of the service.
*Mitigation and Recovery:* Implement strict rate limiting and circuit breaking at the application layer (e.g., using Envoy or an API gateway). During an incident, the specialist must quickly isolate the failing cluster by disabling the global service annotations or severing the mesh connection to prevent the failure from propagating, allowing the healthy cluster to shed load and recover.

## 5. GitOps with ArgoCD and Flux

GitOps is the paradigm of using Git as the single source of truth for declarative infrastructure and applications. In advanced EKS environments, tools like ArgoCD and Flux continuously monitor Git repositories and automatically synchronize the cluster state to match the repository state.

### 5.1 The Pull-Based Deployment Model

Unlike traditional CI/CD pipelines where a CI server pushes changes to the cluster (requiring cluster credentials to be stored externally), GitOps uses a pull-based model. The GitOps controller runs inside the EKS cluster, authenticates to the Git repository, and pulls the manifests. This significantly improves security and auditability.

### 5.2 Managing Complex Deployments

GitOps controllers handle complex deployment strategies, such as Helm chart rendering, Kustomize overlays, and progressive delivery (Canary/Blue-Green) when integrated with tools like Argo Rollouts or Flagger.

### 5.3 Tech Support Scenarios: GitOps Failures

**Scenario 1: The Sync Loop of Death**
If a resource in the cluster is continuously modified by an external process (e.g., a mutating admission webhook or a custom controller) in a way that conflicts with the state defined in Git, the GitOps controller will enter an infinite sync loop. It will continuously overwrite the cluster state, which is then immediately mutated again. This causes massive API server load and fills the etcd database with revision history.
*Resolution:* Identify the conflicting controller or webhook. The specialist must either configure the GitOps tool to ignore the specific fields being mutated (e.g., using `ignoreDifferences` in ArgoCD) or update the Git repository to match the mutated state.

**Scenario 2: Secret Management and Decryption Failures**
GitOps requires secrets to be stored in Git, which necessitates encryption (e.g., using Sealed Secrets or SOPS). If the decryption key (stored in AWS KMS or a cluster secret) is rotated incorrectly or becomes unavailable, the GitOps controller will fail to decrypt the secrets during synchronization. Applications will fail to start due to missing configuration.
*Resolution:* Verify the KMS key policies and the IAM roles for Service Accounts (IRSA) assigned to the GitOps controller. Ensure the decryption keys are valid and accessible. Manually trigger a sync after restoring access to the keys.

### 5.4 Worst-Case Scenario: The Accidental Cluster Wipe

The most terrifying GitOps scenario occurs when a user accidentally deletes the root application manifest or the entire directory structure in the Git repository. Because the GitOps controller ensures the cluster matches Git, it will dutifully execute a cascading deletion of all resources, namespaces, and applications in the EKS cluster.
*Mitigation and Recovery:* Preventative measures are critical: enable branch protection rules in Git, require pull request reviews, and configure the GitOps controller to prevent cascading deletions (e.g., disabling the `prune` option for critical applications). If a wipe occurs, recovery involves reverting the Git commit, ensuring the GitOps controller is running, and waiting for the massive synchronization process to rebuild the cluster. Stateful data must be recovered from backups if PersistentVolumes were deleted.

## 6. Advanced Scheduling and Resource Management

Efficiently utilizing compute resources in EKS requires moving beyond basic resource requests and limits. Advanced scheduling techniques ensure that critical workloads receive priority, nodes are optimally packed, and specialized hardware (like GPUs) is utilized effectively.

### 6.1 Taints, Tolerations, and Node Affinity

Specialists must master the use of taints and tolerations to dedicate specific node groups to specific workloads (e.g., isolating noisy neighbors or dedicating high-memory instances to database pods). Node affinity and anti-affinity rules dictate pod placement based on node labels, ensuring high availability across Availability Zones.

### 6.2 Pod Topology Spread Constraints

To achieve true high availability, pods must be distributed evenly across failure domains. Pod Topology Spread Constraints provide granular control over how pods are spread across regions, zones, or individual nodes, preventing a single node failure from taking down an entire application tier.

### 6.3 Custom Schedulers and Descheduler

In highly specialized environments, the default `kube-scheduler` may not suffice. Organizations may deploy custom schedulers to handle complex placement logic (e.g., gang scheduling for machine learning workloads). Furthermore, the Kubernetes Descheduler is critical for maintaining cluster health over time. As pods are created and destroyed, the cluster can become fragmented. The Descheduler evicts pods based on specific policies (e.g., removing pods from overutilized nodes) to allow the `kube-scheduler` to place them more optimally.

### 6.4 Tech Support Scenarios: Scheduling Nightmares

**Scenario 1: The Unschedulable Pod Backlog**
A massive influx of pods with strict affinity rules or resource requests that exceed the available capacity of any single node will result in a backlog of `Pending` pods. This can exhaust the API server's memory as it tracks the unschedulable pods and trigger aggressive scaling actions from the Cluster Autoscaler or Karpenter, potentially hitting AWS account limits.
*Resolution:* The specialist must analyze the scheduling events (`kubectl describe pod`). If the constraints are too strict, they must be relaxed. If capacity is genuinely exhausted, AWS limits must be increased, or the Cluster Autoscaler configuration must be adjusted to provision appropriate instance types.

**Scenario 2: Priority Inversion and Preemption Storms**
Kubernetes PriorityClasses allow critical pods to preempt (evict) lower-priority pods. If PriorityClasses are misconfigured, a deployment of high-priority pods can trigger a preemption storm, evicting essential system components (like logging daemonsets or ingress controllers) and causing widespread instability.
*Resolution:* Immediately scale down the deployment causing the preemption. Review and strictly govern the use of PriorityClasses. Ensure critical system components are protected with the `system-cluster-critical` or `system-node-critical` priority classes.

### 6.5 Worst-Case Scenario: Karpenter/Autoscaler Thrashing

When using advanced node provisioners like Karpenter, conflicting scheduling constraints or rapid fluctuations in workload demand can cause thrashing. Karpenter may provision a node, schedule pods, realize the node is underutilized, deprovision it, and immediately provision a new one. This continuous churn destabilizes the cluster, disrupts network connections, and incurs significant AWS costs.
*Mitigation and Recovery:* Pause the node provisioner. Analyze the Karpenter logs and the pod scheduling constraints. Adjust the consolidation policies and TTL settings in the Karpenter Provisioner configuration to introduce hysteresis and prevent rapid deprovisioning.

## 7. Conclusion

Operating an advanced EKS environment requires a deep, systemic understanding of Kubernetes internals. The specialist must be prepared to navigate the complexities of custom controllers, debug kernel-level networking issues with eBPF, manage the risks of GitOps automation, and optimize scheduling across massive fleets. By mastering these advanced topics and preparing for the worst-case scenarios outlined in this guide, technical support operations can ensure the resilience, performance, and security of mission-critical Kubernetes infrastructure.

## === FILE: 37-k8s-eks-cli-reference.md ===
# Kubernetes and EKS CLI Reference: Advanced Operations and Tech Support Guide

## 1. Introduction

In the high-stakes environment of production Kubernetes and Amazon Elastic Kubernetes Service (EKS), technical support engineers and site reliability engineers (SREs) require rapid, precise, and powerful tools to diagnose and remediate complex issues. This comprehensive CLI reference guide is designed specifically for tech support operations, focusing on advanced usage, worst-case scenarios, and practical one-liners. It covers the essential toolchain: `kubectl`, `eksctl`, `aws eks`, `helm`, and `k9s`.

This document serves as a definitive operational playbook. It moves beyond basic commands to provide deep diagnostic capabilities, state recovery procedures, and performance profiling techniques. Whether you are dealing with a widespread `NodeNotReady` incident, a subtle DNS resolution failure, or a complex Helm release rollback, this guide provides the exact commands needed to restore service stability.

---

## 2. `kubectl` Advanced Operations & One-Liners

The `kubectl` command-line tool is the primary interface for interacting with the Kubernetes API. For tech support, mastering `kubectl` means understanding how to extract precise state information, manipulate resources directly, and bypass standard abstractions when necessary.

### 2.1 Cluster & Node Diagnostics

When cluster stability is compromised, the first step is to assess the health of the underlying compute resources.

**Identify Nodes with High Resource Pressure:**
```bash
kubectl get nodes -o custom-columns="NAME:.metadata.name,CPU_ALLOCATABLE:.status.allocatable.cpu,MEMORY_ALLOCATABLE:.status.allocatable.memory,STATUS:.status.conditions[?(@.type=='Ready')].status"
```

**Find Nodes that are NotReady and Extract the Reason:**
```bash
kubectl get nodes --field-selector=status.phase!=Running -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.status.conditions[?(@.type=="Ready")].message}{"\n"}{end}'
```

**Drain a Node Aggressively (Ignoring DaemonSets and Local Data):**
In emergency situations where a node is failing and pods must be evicted immediately:
```bash
kubectl drain <node-name> --ignore-daemonsets --delete-emptydir-data --force --grace-period=0
```

**Check Kubelet Logs via Node Shell (Requires Privileged Access):**
When SSH access is unavailable, you can spawn a privileged pod on the node to inspect system logs.
```bash
kubectl debug node/<node-name> -it --image=ubuntu -- chroot /host journalctl -u kubelet -f
```

### 2.2 Pod & Container Troubleshooting

Pod failures are the most common support tickets. Rapidly identifying the root cause—whether it's an OOMKill, a readiness probe failure, or a crash loop—is critical.

**List All Pods in CrashLoopBackOff or Error State Across All Namespaces:**
```bash
kubectl get pods -A --field-selector=status.phase!=Running | grep -v 'Completed'
```

**Extract the Exit Code and Reason for the Last Terminated Container:**
This is essential for diagnosing OOMKilled (Exit Code 137) or segmentation faults.
```bash
kubectl get pod <pod-name> -n <namespace> -o jsonpath='{.status.containerStatuses[0].lastState.terminated.reason} - Exit Code: {.status.containerStatuses[0].lastState.terminated.exitCode}{"\n"}'
```

**Stream Logs from All Containers in a Deployment:**
```bash
kubectl logs -f deployment/<deployment-name> --all-containers=true --max-log-requests=10
```

**Execute a Network Troubleshooting Container in an Existing Pod's Network Namespace:**
If a pod lacks debugging tools (e.g., `curl`, `dig`, `ping`), attach an ephemeral debug container.
```bash
kubectl debug -it <pod-name> --image=nicolaka/netshoot --target=<container-name>
```

### 2.3 Networking & DNS Debugging

Networking issues in Kubernetes often manifest as intermittent timeouts or DNS resolution failures.

**Test DNS Resolution from within the Cluster:**
```bash
kubectl run -i --tty --rm debug-dns --image=busybox:1.28 --restart=Never -- nslookup kubernetes.default.svc.cluster.local
```

**Check CoreDNS Logs for Errors:**
```bash
kubectl logs -n kube-system -l k8s-app=kube-dns -c coredns --tail=100 | grep -i error
```

**List All Services Without Endpoints (Orphaned Services):**
A service without endpoints will drop traffic. This command identifies them.
```bash
kubectl get endpoints -A | awk '$3 == "<none>" {print $1, $2}'
```

**Capture Packet Trace on a Specific Pod (Requires Netshoot):**
```bash
kubectl exec -it <pod-name> -- tcpdump -i eth0 -nn -s0 -w /tmp/capture.pcap
```

### 2.4 Resource & Performance Profiling

Resource exhaustion leads to unpredictable behavior. Monitoring CPU and memory requests versus actual usage is a core support task.

**Sort Pods by Memory Usage (Requires Metrics Server):**
```bash
kubectl top pods -A --sort-by=memory
```

**Identify Pods Without Resource Limits Configured:**
```bash
kubectl get pods -A -o jsonpath='{range .items[*]}{.metadata.namespace}{"\t"}{.metadata.name}{"\t"}{.spec.containers[*].resources.limits}{"\n"}{end}' | grep -v "cpu"
```

### 2.5 RBAC & Security Auditing

Permissions issues often block deployments or operational tasks.

**Check if You (or a ServiceAccount) Can Perform an Action:**
```bash
kubectl auth can-i create deployments --namespace dev --as system:serviceaccount:dev:ci-cd
```

**List All ClusterRoleBindings Granting Cluster-Admin:**
```bash
kubectl get clusterrolebindings -o jsonpath='{range .items[?(@.roleRef.name=="cluster-admin")]}{.metadata.name}{"\t"}{.subjects[*].name}{"\n"}{end}'
```

---

## 3. `eksctl` Production Management

`eksctl` is the official CLI for Amazon EKS. In a support context, it is primarily used for cluster lifecycle management, node group scaling, and IAM integration.

### 3.1 Cluster Upgrades & Maintenance

Upgrading an EKS cluster requires careful orchestration of the control plane and data plane.

**Check Cluster Upgrade Readiness:**
```bash
eksctl utils update-cluster-logging --cluster <cluster-name> --region <region> --enable-types all
```

**Upgrade the Control Plane to a Specific Version:**
```bash
eksctl upgrade cluster --name <cluster-name> --version 1.28 --approve
```

### 3.2 Node Group Management

When nodes fail or require patching, node group management is necessary.

**Scale a Managed Node Group:**
```bash
eksctl scale nodegroup --cluster <cluster-name> --name <nodegroup-name> --nodes 5 --nodes-min 3 --nodes-max 10
```

**Drain and Delete a Node Group (Graceful Decommissioning):**
```bash
eksctl delete nodegroup --cluster <cluster-name> --name <old-nodegroup> --drain=true
```

### 3.3 IAM OIDC & Service Accounts

IRSA (IAM Roles for Service Accounts) is the standard for granting AWS permissions to pods. Misconfigurations here are a frequent source of support tickets.

**Create an IAM Role and Bind it to a Kubernetes ServiceAccount:**
```bash
eksctl create iamserviceaccount   --cluster=<cluster-name>   --namespace=<namespace>   --name=<service-account-name>   --attach-policy-arn=arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess   --approve   --override-existing-serviceaccounts
```

**Verify the OIDC Provider is Associated with the Cluster:**
```bash
eksctl utils associate-iam-oidc-provider --cluster <cluster-name> --approve
```

---

## 4. `aws eks` CLI for Control Plane

The AWS CLI (`aws eks`) is used for interacting with the AWS API regarding the EKS control plane infrastructure.

### 4.1 Cluster Authentication & Kubeconfig

**Generate or Update Kubeconfig for an EKS Cluster:**
```bash
aws eks update-kubeconfig --region <region> --name <cluster-name> --alias <custom-alias>
```

**Assume a Role Before Updating Kubeconfig (Cross-Account Access):**
```bash
aws eks update-kubeconfig --region <region> --name <cluster-name> --role-arn arn:aws:iam::<account-id>:role/<role-name>
```

### 4.2 Add-on Management

EKS Add-ons (VPC CNI, CoreDNS, kube-proxy) must be kept up to date.

**List Installed Add-ons and Their Status:**
```bash
aws eks list-addons --cluster-name <cluster-name> --region <region>
```

**Describe a Specific Add-on to Check for Degradation:**
```bash
aws eks describe-addon --cluster-name <cluster-name> --addon-name vpc-cni --region <region> --query 'addon.health.issues'
```

### 4.3 Control Plane Logging & Diagnostics

When the API server is unresponsive, control plane logs in CloudWatch are the only source of truth.

**Enable All Control Plane Logs (API, Audit, Authenticator, ControllerManager, Scheduler):**
```bash
aws eks update-cluster-config     --region <region>     --name <cluster-name>     --logging '{"clusterLogging":[{"types":["api","audit","authenticator","controllerManager","scheduler"],"enable":true}]}'
```

---

## 5. `helm` Advanced Release Management

Helm is the package manager for Kubernetes. Support operations often involve untangling failed deployments, recovering from stuck states, and verifying chart integrity.

### 5.1 Release Debugging & Rollbacks

**List All Failed or Pending Helm Releases Across All Namespaces:**
```bash
helm ls --all-namespaces -a | grep -E 'FAILED|pending'
```

**Rollback a Release to the Previous Successful Revision:**
```bash
helm rollback <release-name> 0 -n <namespace> --wait --timeout 10m
```

**Force a Rollback (Bypassing Hooks):**
If a pre-rollback hook is failing and blocking recovery:
```bash
helm rollback <release-name> <revision-number> -n <namespace> --no-hooks --force
```

### 5.2 Chart Verification & Templating

Before applying a chart, it is crucial to verify the exact manifests that will be generated.

**Render Chart Templates Locally for Inspection:**
```bash
helm template <release-name> <chart-path> -n <namespace> -f values-production.yaml > rendered-manifests.yaml
```

**Diff a Helm Upgrade Before Applying (Requires helm-diff plugin):**
```bash
helm diff upgrade <release-name> <chart-path> -n <namespace> -f values-production.yaml
```

### 5.3 State Recovery

Sometimes the Helm release secret becomes corrupted or out of sync with the actual cluster state.

**Get the Decoded Helm Release Secret (Advanced Debugging):**
```bash
kubectl get secret -n <namespace> sh.helm.release.v1.<release-name>.v1 -o jsonpath="{.data.release}" | base64 -d | base64 -d | gzip -d
```

---

## 6. `k9s` Power User Guide

`k9s` is a terminal-based UI to interact with your Kubernetes clusters. For tech support, it drastically reduces the time required to navigate resources, view logs, and execute commands.

### 6.1 Keyboard Shortcuts for Rapid Triage

- `:` : Enter command mode (e.g., `:pods`, `:deploy`, `:svc`).
- `/` : Filter the current view by regex.
- `l` : View logs for the selected pod or container.
- `w` : Toggle line wrap in log view.
- `s` : Open a shell inside the selected pod.
- `d` : Describe the selected resource.
- `e` : Edit the resource YAML directly.
- `ctrl-d` : Delete the selected resource.
- `shift-f` : Setup port-forwarding for the selected pod or service.

### 6.2 Custom Resource Views

`k9s` excels at managing Custom Resource Definitions (CRDs).

- Type `:crd` to view all Custom Resource Definitions.
- Select a CRD and press `Enter` to view all instances of that custom resource.
- This is invaluable for debugging operators (e.g., Prometheus Operator, Cert-Manager).

### 6.3 Plugins & Extensibility

`k9s` can be extended with custom plugins defined in `~/.config/k9s/plugins.yaml`.

**Example Plugin: Decode Secret**
This plugin allows you to press `x` on a Secret to view its decoded contents.
```yaml
plugins:
  decode-secret:
    shortCut: x
    confirm: false
    description: "Decode Secret"
    scopes:
      - secrets
    command: sh
    background: false
    args:
      - -c
      - "kubectl get secret $NAME -n $NAMESPACE -o json | jq '.data | map_values(@base64d)' | less"
```

---

## 7. Worst-Case Scenarios & Incident Response

Tech support operations are defined by how they handle worst-case scenarios. Below are playbooks for critical incidents.

### 7.1 API Server Unresponsive

**Symptoms:** `kubectl` commands time out; nodes transition to `NotReady`; controllers stop functioning.
**EKS Context:** In EKS, the control plane is managed by AWS.
**Response:**
1. Verify network connectivity to the EKS endpoint.
2. Check AWS Service Health Dashboard for regional EKS outages.
3. Review CloudWatch metrics for the EKS control plane (if enabled).
4. Ensure the VPC and subnets associated with the cluster have available IP addresses.
5. If the issue persists, escalate to AWS Support immediately, as control plane recovery is their responsibility.

### 7.2 Widespread Node NotReady

**Symptoms:** Multiple nodes simultaneously report `NotReady` status. Pods are evicted or stuck in `Terminating`.
**Response:**
1. **Check Kubelet Status:** Use SSM Session Manager or SSH to access a failing node. Run `systemctl status kubelet` and `journalctl -u kubelet`.
2. **Verify VPC CNI:** If the VPC CNI plugin fails, nodes cannot assign IPs to pods, leading to readiness failures. Check the `aws-node` daemonset logs in the `kube-system` namespace.
3. **Check Disk Pressure:** Nodes will become `NotReady` if they run out of disk space. Run `df -h` on the node.
4. **Review Auto Scaling Group (ASG):** Check the AWS console for ASG health checks or EC2 instance status checks failing.

### 7.3 CoreDNS CrashLoopBackOff

**Symptoms:** Internal service discovery fails. Pods cannot resolve `kubernetes.default.svc` or external domains.
**Response:**
1. **Check CoreDNS Logs:** `kubectl logs -n kube-system -l k8s-app=kube-dns`. Look for configuration errors or connection refused messages.
2. **Verify Node Connectivity:** CoreDNS pods must be able to reach the API server. Check security groups and network ACLs.
3. **Restart CoreDNS:** `kubectl rollout restart deployment coredns -n kube-system`.
4. **Check Resource Limits:** Ensure CoreDNS is not being OOMKilled. Increase memory limits if necessary.

### 7.4 Exhaustion of VPC IP Addresses

**Symptoms:** Pods remain in `ContainerCreating` state. VPC CNI logs show `Failed to allocate IP address`.
**Response:**
1. **Check Subnet IP Availability:** Use the AWS CLI to check available IPs in the cluster subnets.
   ```bash
   aws ec2 describe-subnets --subnet-ids <subnet-ids> --query 'Subnets[*].[SubnetId, AvailableIpAddressCount]' --output table
   ```
2. **Enable Custom Networking:** If the primary subnets are exhausted, configure the VPC CNI to use secondary subnets for pod IPs.
3. **Reduce WARM_IP_TARGET:** Adjust the VPC CNI environment variables to hold fewer unused IPs in reserve.

---

## 8. Advanced Troubleshooting Scenarios

### 8.1 Persistent Volume (PV) and Persistent Volume Claim (PVC) Issues

Storage issues can cause pods to remain in a `Pending` state indefinitely.

**Identify Unbound PVCs:**
```bash
kubectl get pvc -A | grep -v Bound
```

**Check Events for a Specific PVC:**
```bash
kubectl describe pvc <pvc-name> -n <namespace> | grep -A 10 Events
```

**Force Delete a Stuck PV:**
Sometimes a PV gets stuck in a `Terminating` state due to finalizers.
```bash
kubectl patch pv <pv-name> -p '{"metadata":{"finalizers":null}}'
```

### 8.2 Ingress and Load Balancer Debugging

When external traffic fails to reach your services, the issue often lies with the Ingress controller or the cloud provider's load balancer.

**Check AWS Load Balancer Controller Logs:**
```bash
kubectl logs -n kube-system deployment/aws-load-balancer-controller
```

**Verify Ingress Resource Configuration:**
```bash
kubectl describe ingress <ingress-name> -n <namespace>
```

**Test Internal Service Reachability from the Ingress Controller Pod:**
```bash
kubectl exec -it <ingress-controller-pod> -n <ingress-namespace> -- curl -v http://<service-name>.<service-namespace>.svc.cluster.local:<port>
```

### 8.3 Certificate and Secret Management

Expired certificates or misconfigured secrets can cause widespread outages.

**Check Certificate Expiration (Requires cert-manager):**
```bash
kubectl get certificates -A -o custom-columns="NAMESPACE:.metadata.namespace,NAME:.metadata.name,READY:.status.conditions[?(@.type=='Ready')].status,EXPIRATION:.status.notAfter"
```

**Decode All Secrets in a Namespace (Use with Caution):**
```bash
kubectl get secrets -n <namespace> -o json | jq '.items[] | {name: .metadata.name, data: .data | map_values(@base64d)}'
```

---

## 9. Conclusion

Effective Kubernetes and EKS tech support requires a deep understanding of the underlying architecture and the ability to wield CLI tools with precision. This reference guide provides the foundational commands and advanced techniques necessary to diagnose, mitigate, and resolve complex production incidents. By mastering `kubectl`, `eksctl`, `aws eks`, `helm`, and `k9s`, support engineers can ensure the reliability, security, and performance of mission-critical containerized workloads.

Regularly practice these commands in a non-production environment to build muscle memory. In the heat of an incident, the ability to rapidly execute the correct diagnostic one-liner is the difference between a minor blip and a major outage.

## === FILE: 37-k8s-eks-specialist.md ===
# Kubernetes and AWS EKS Specialist: Comprehensive Operations Guide

## 1. Introduction and Executive Summary

The **Kubernetes and AWS Elastic Kubernetes Service (EKS) Specialist** is a critical role within the modern cloud-native engineering organization. As organizations increasingly adopt microservices architectures and containerized workloads, Kubernetes has emerged as the de facto standard for container orchestration. AWS EKS provides a managed Kubernetes control plane, alleviating some of the operational burdens of managing etcd and the API server, but it introduces its own set of complexities regarding AWS integration, networking, and security.

This document serves as the definitive guide for the Kubernetes/EKS Specialist, focusing heavily on production operations, worst-case scenarios, and advanced technical support. It is designed to equip the specialist with the deep technical knowledge required to architect, deploy, manage, and troubleshoot large-scale, highly available EKS clusters. The content herein transcends basic tutorials, delving into the intricate details of the AWS VPC CNI, IAM Roles for Service Accounts (IRSA), advanced scaling mechanisms like Karpenter, and rigorous disaster recovery protocols.

The specialist must not only understand Kubernetes primitives but also how they map to AWS infrastructure. This requires a dual expertise in both the open-source Kubernetes ecosystem and the proprietary AWS services that EKS relies upon. By mastering the concepts, architectures, and troubleshooting methodologies detailed in this guide, the specialist will be prepared to ensure the reliability, security, and performance of mission-critical applications running on EKS.

## 2. Role and Responsibilities of the K8s/EKS Specialist

The Kubernetes/EKS Specialist is responsible for the end-to-end lifecycle of the Kubernetes infrastructure. This role bridges the gap between infrastructure engineering, platform engineering, and application development. The core responsibilities are multifaceted and demand a proactive approach to system reliability.

### Core Responsibilities

*   **Architecture and Design:** Designing highly available, scalable, and secure EKS clusters tailored to specific workload requirements. This includes selecting the appropriate compute options (EC2, Fargate), designing the network topology (VPC, subnets, CNI configuration), and defining the security posture (RBAC, network policies).
*   **Cluster Provisioning and Lifecycle Management:** Utilizing Infrastructure as Code (IaC) tools such as Terraform or AWS CDK to provision and manage EKS clusters. A critical aspect of this responsibility is managing Kubernetes version upgrades, ensuring compatibility with add-ons, and minimizing downtime during the upgrade process.
*   **Compute and Scaling Management:** Configuring and optimizing node groups, leveraging Spot instances for cost efficiency, and implementing advanced autoscaling solutions like Karpenter or the Kubernetes Cluster Autoscaler. The specialist must ensure that the cluster can dynamically respond to fluctuating workload demands.
*   **Networking and Ingress:** Managing the AWS VPC CNI plugin, configuring Ingress controllers (e.g., AWS Load Balancer Controller, NGINX), and implementing service meshes (e.g., Istio) for advanced traffic management, observability, and security.
*   **Security and Compliance:** Implementing robust security controls, including IAM integration (IRSA), Kubernetes RBAC, Pod Security Standards, and network policies. The specialist must ensure that the cluster adheres to organizational compliance requirements and industry best practices.
*   **Observability and Monitoring:** Integrating EKS with observability platforms (e.g., Prometheus, Grafana, Datadog, AWS CloudWatch) to monitor cluster health, resource utilization, and application performance.
*   **Technical Support and Incident Response:** Serving as the highest level of escalation for Kubernetes-related issues. The specialist must possess deep troubleshooting skills to diagnose and resolve complex problems, ranging from pod scheduling failures to network connectivity issues and performance bottlenecks.

## 3. Architecture Deep Dive: Kubernetes and AWS EKS

Understanding the architectural nuances of EKS is fundamental to operating it effectively. EKS is a managed service, meaning AWS assumes responsibility for the control plane, while the customer manages the data plane (worker nodes).

### The EKS Control Plane

The EKS control plane consists of the Kubernetes API server, etcd (the distributed key-value store), the scheduler, and the controller manager. In EKS, these components run in an AWS-managed VPC. AWS automatically scales the control plane instances based on load and ensures high availability by deploying them across multiple Availability Zones (AZs).

*   **API Server Endpoint:** EKS provides an endpoint for the API server, which can be configured as public, private, or both. For production environments, a private-only endpoint or a public endpoint with strict CIDR restrictions is highly recommended to minimize the attack surface.
*   **etcd Management:** AWS manages the etcd cluster, including backups and scaling. While this removes a significant operational burden, it also means the specialist has limited visibility into etcd performance metrics.

### The Data Plane (Worker Nodes)

The data plane consists of the EC2 instances or Fargate profiles where the actual application pods run. These nodes reside in the customer's VPC.

*   **Kubelet:** The primary node agent that communicates with the control plane and manages the containers on the node.
*   **Kube-proxy:** Maintains network rules on the node, enabling communication to pods from inside or outside the cluster.
*   **Container Runtime:** EKS currently uses containerd as the default container runtime.

### AWS Integrations

EKS differentiates itself through deep integration with AWS services:

*   **AWS VPC CNI:** This plugin assigns native AWS Elastic Network Interfaces (ENIs) and secondary IP addresses directly to pods. This allows pods to have native VPC IP addresses, enabling seamless communication with other AWS services and on-premises networks.
*   **IAM Roles for Service Accounts (IRSA):** IRSA allows you to associate an AWS IAM role with a Kubernetes Service Account. This provides fine-grained, pod-level access control to AWS resources (e.g., S3, DynamoDB) without the need to manage AWS credentials within the pods or on the worker nodes.

## 4. Cluster Management and Provisioning

Effective cluster management relies heavily on automation and rigorous lifecycle management practices. Manual configuration is an anti-pattern in modern Kubernetes operations.

### Infrastructure as Code (IaC)

All EKS infrastructure must be defined and provisioned using IaC. Terraform is the industry standard, often utilized alongside the official AWS EKS Terraform module.

```hcl
# Example Terraform snippet for EKS Cluster
module "eks" {
  source  = "terraform-aws-modules/eks/aws"
  version = "~> 19.0"

  cluster_name    = "production-cluster"
  cluster_version = "1.28"

  vpc_id     = module.vpc.vpc_id
  subnet_ids = module.vpc.private_subnets

  eks_managed_node_groups = {
    general = {
      desired_size = 3
      min_size     = 3
      max_size     = 10

      instance_types = ["m6i.large"]
      capacity_type  = "ON_DEMAND"
    }
  }
}
```

### Upgrades and Version Management

Kubernetes releases new minor versions frequently, and AWS deprecates older versions accordingly. Upgrading an EKS cluster is a critical operation that requires careful planning.

1.  **Pre-Upgrade Checks:** Utilize tools like `pluto` or `kubent` to identify deprecated API versions in use within the cluster. Ensure all Helm charts and manifests are updated to use the supported API versions.
2.  **Control Plane Upgrade:** Initiate the control plane upgrade via the AWS Console, CLI, or Terraform. This process typically takes 10-20 minutes. The API server may experience brief periods of unavailability during this time.
3.  **Add-on Upgrades:** Upgrade critical add-ons such as the VPC CNI, CoreDNS, and kube-proxy to versions compatible with the new Kubernetes version.
4.  **Data Plane Upgrade:** Upgrade the worker nodes. For managed node groups, this involves updating the AMI release version. EKS handles the rolling update, cordoning and draining nodes to minimize disruption. For self-managed nodes or Karpenter, the process involves provisioning new nodes with the updated AMI and terminating the old ones.

## 5. Node Groups and Compute Options

Selecting the right compute strategy is essential for balancing performance, cost, and operational overhead.

### Managed Node Groups

EKS Managed Node Groups automate the provisioning and lifecycle management of EC2 instances. AWS handles the rolling updates and ensures that the nodes are running the optimized EKS AMI. This is the recommended approach for most general-purpose workloads.

### Self-Managed Node Groups

Self-managed node groups provide maximum control over the EC2 instances. This is necessary when using custom AMIs, specialized instance types not supported by managed node groups, or complex user data scripts. However, the operational burden of managing updates and scaling falls entirely on the specialist.

### AWS Fargate

Fargate is a serverless compute engine for containers. It eliminates the need to manage EC2 instances entirely. Pods run in isolated compute environments.

*   **Use Cases:** Ideal for batch processing, CI/CD jobs, and workloads with highly variable resource requirements.
*   **Limitations:** Fargate does not support DaemonSets, privileged containers, or host network mode. It also introduces a slight delay in pod startup time compared to EC2 instances.

### Spot Instances and Karpenter

Spot instances offer significant cost savings (up to 90%) compared to On-Demand instances, but they can be interrupted by AWS with a two-minute warning.

**Karpenter** is an open-source, flexible, high-performance Kubernetes cluster autoscaler built by AWS. It dramatically improves the efficiency and cost-effectiveness of running workloads on EKS.

*   **How Karpenter Works:** Unlike the traditional Cluster Autoscaler, which relies on Auto Scaling Groups (ASGs), Karpenter directly provisions EC2 instances based on the specific resource requests of pending pods. It bypasses ASGs entirely.
*   **Spot Integration:** Karpenter excels at managing Spot instances. It can intelligently select from a diverse pool of instance types and availability zones to minimize the risk of simultaneous interruptions. It also handles graceful termination of pods when a Spot interruption notice is received.

## 6. Scaling Strategies

Scaling in Kubernetes occurs at two levels: the application level (pods) and the infrastructure level (nodes).

### Application Scaling

*   **Horizontal Pod Autoscaler (HPA):** Scales the number of pod replicas based on observed CPU utilization, memory utilization, or custom metrics (e.g., queue length).
*   **Vertical Pod Autoscaler (VPA):** Automatically adjusts the CPU and memory requests and limits for containers in a pod. VPA is useful for workloads with unpredictable resource requirements, but it requires restarting the pods to apply the changes.

### Infrastructure Scaling

*   **Cluster Autoscaler (CA):** The traditional method for scaling nodes. It monitors for pending pods that cannot be scheduled due to resource constraints and increases the size of the corresponding ASG. It also scales down ASGs when nodes are underutilized.
*   **Karpenter:** As discussed, Karpenter provides a more dynamic and efficient approach to node scaling, directly provisioning instances tailored to the workload requirements.

**Best Practice:** Use HPA in conjunction with Karpenter. HPA scales the pods based on application metrics, and Karpenter rapidly provisions the necessary infrastructure to accommodate the new pods.

## 7. Networking and Traffic Management

Networking in EKS is complex and requires a deep understanding of both Kubernetes networking primitives and AWS VPC networking.

### AWS VPC CNI Deep Dive

The AWS VPC CNI plugin is the default networking solution for EKS. It allocates IP addresses from the VPC directly to pods.

*   **IP Address Exhaustion:** A common issue with the VPC CNI is IP address exhaustion in the subnets. Each EC2 instance has a maximum number of ENIs and secondary IP addresses it can support.
*   **Prefix Delegation:** To mitigate IP exhaustion and increase pod density per node, enable Prefix Delegation. This feature assigns /28 IPv4 prefixes to ENIs instead of individual secondary IP addresses, significantly increasing the number of pods that can run on a single instance.
*   **Custom Networking:** For environments with strict IP address constraints, custom networking allows pods to be placed in different subnets (with different CIDR ranges) than the worker nodes.

### Ingress Controllers

Ingress controllers manage external access to the services in a cluster, typically HTTP/HTTPS.

*   **AWS Load Balancer Controller:** This controller provisions AWS Application Load Balancers (ALBs) for Kubernetes Ingress resources and Network Load Balancers (NLBs) for Kubernetes Service resources of type `LoadBalancer`. It natively integrates with AWS WAF and ACM (AWS Certificate Manager).
*   **NGINX Ingress Controller:** A popular open-source alternative that provides advanced routing capabilities, rate limiting, and custom configuration options. It is typically exposed via an NLB.

### Service Mesh

For complex microservices architectures, a service mesh like Istio or Linkerd provides advanced traffic management (canary deployments, circuit breaking), mutual TLS (mTLS) for secure service-to-service communication, and deep observability.

## 8. Security and Compliance

Securing an EKS cluster requires a defense-in-depth approach, addressing security at the infrastructure, cluster, and application levels.

### RBAC and IAM Integration

*   **Kubernetes RBAC:** Use Role-Based Access Control to restrict what users and service accounts can do within the cluster. Adhere to the principle of least privilege.
*   **AWS IAM Authenticator:** EKS uses the AWS IAM Authenticator to map IAM users and roles to Kubernetes RBAC groups.
*   **IRSA:** As mentioned earlier, use IAM Roles for Service Accounts to grant pods access to AWS resources securely. Never use long-lived AWS credentials within pods.

### Network Policies

By default, all pods in a Kubernetes cluster can communicate with each other. Network Policies act as a firewall for pods, restricting ingress and egress traffic based on labels, namespaces, and IP blocks. Implementing default-deny network policies is a critical security best practice.

### Pod Security Standards and Admission Controllers

*   **Pod Security Admission (PSA):** Replaces the deprecated Pod Security Policies (PSP). PSA enforces the Pod Security Standards (Privileged, Baseline, Restricted) at the namespace level.
*   **OPA Gatekeeper / Kyverno:** For more granular and customizable policy enforcement, use admission controllers like OPA Gatekeeper or Kyverno. These tools can enforce policies such as requiring specific labels, restricting image registries, or preventing the deployment of privileged containers.

## 9. Tech Support Operations and Troubleshooting

The specialist must be adept at diagnosing and resolving complex issues in production environments. This section outlines common failure scenarios and troubleshooting methodologies.

### Common Pod Failures

*   **CrashLoopBackOff:** The pod starts, crashes, and Kubernetes repeatedly attempts to restart it.
    *   *Troubleshooting:* Inspect the pod logs (`kubectl logs <pod-name> --previous`). Check for application errors, missing configuration files, or incorrect environment variables.
*   **ImagePullBackOff / ErrImagePull:** The kubelet cannot pull the container image.
    *   *Troubleshooting:* Verify the image name and tag. Ensure the node has network access to the container registry. Check if image pull secrets are required and correctly configured.
*   **OOMKilled (Out of Memory):** The container exceeded its memory limit and was terminated by the Linux kernel.
    *   *Troubleshooting:* Inspect the pod description (`kubectl describe pod <pod-name>`). Analyze application memory usage. Increase the memory limit if necessary, or investigate the application for memory leaks.

### Node NotReady States

A node enters the `NotReady` state when the kubelet stops communicating with the control plane or reports an unhealthy status.

*   *Troubleshooting:*
    1.  Check the node status and events (`kubectl describe node <node-name>`).
    2.  Verify the underlying EC2 instance status in the AWS Console.
    3.  SSH into the node (if possible) and check the kubelet logs (`journalctl -u kubelet`).
    4.  Check for resource exhaustion (CPU, memory, disk space) on the node.
    5.  Verify network connectivity between the node and the EKS control plane.

### DNS Resolution Issues (CoreDNS)

DNS failures can cause widespread application disruption.

*   *Troubleshooting:*
    1.  Check the status of the CoreDNS pods (`kubectl get pods -n kube-system -l k8s-app=kube-dns`).
    2.  Inspect the CoreDNS logs for errors.
    3.  Verify that the CoreDNS service has endpoints.
    4.  Use a debug pod (e.g., `dnstools`) to test DNS resolution from within the cluster (`nslookup kubernetes.default`).
    5.  Check for node-level DNS issues or security group rules blocking UDP port 53.

### Network Connectivity Issues

*   *Troubleshooting:*
    1.  Verify Network Policies are not inadvertently blocking traffic.
    2.  Check the AWS Security Groups associated with the worker nodes and the control plane.
    3.  Inspect the VPC CNI logs on the nodes.
    4.  Use tools like `tcpdump` or VPC Flow Logs to analyze network traffic.

## 10. Worst-Case Scenarios and Disaster Recovery

Preparing for catastrophic failures is a core responsibility of the specialist.

### Control Plane Failure

While AWS manages the control plane and provides an SLA, outages can occur.

*   *Impact:* You cannot deploy new applications, scale existing ones, or manage the cluster. However, existing pods on worker nodes will continue to run and serve traffic, provided they do not rely on the API server for continuous operation.
*   *Mitigation:* Rely on AWS to restore the control plane. Ensure your applications are resilient and do not have hard dependencies on the API server for the data path.

### Complete Availability Zone (AZ) Outage

An entire AWS AZ goes offline.

*   *Impact:* All worker nodes and pods in that AZ are lost.
*   *Mitigation:*
    1.  Ensure node groups are distributed across multiple AZs.
    2.  Use pod anti-affinity rules to spread application replicas across different AZs.
    3.  Configure the Cluster Autoscaler or Karpenter to rapidly provision new nodes in the healthy AZs to replace the lost capacity.
    4.  Ensure persistent volumes (EBS) are snapshotted regularly, as EBS volumes are AZ-specific.

### Accidental Namespace or Cluster Deletion

*   *Mitigation:*
    1.  Implement strict RBAC to limit who can delete critical resources.
    2.  Use tools like Velero to perform regular backups of Kubernetes resources and persistent volumes.
    3.  In the event of deletion, use Velero to restore the namespace or the entire cluster state to a new cluster.
    4.  Maintain all infrastructure and Kubernetes manifests in version control (GitOps) to facilitate rapid redeployment.

## 11. Relationship to Other Specialist Files

The Kubernetes/EKS Specialist does not operate in a vacuum. This role is deeply interconnected with other specialized domains within the engineering organization. Understanding these relationships is crucial for building a cohesive and robust platform.

### 1. CI/CD and Automation Specialist
The EKS Specialist provides the target environment for the CI/CD pipelines. The CI/CD Specialist builds the pipelines that compile code, build container images, and deploy manifests (via Helm or Kustomize) to the EKS cluster. The EKS Specialist must ensure that the cluster has the necessary ingress controllers, service accounts, and RBAC permissions to allow the CI/CD tools (e.g., ArgoCD, GitHub Actions) to deploy applications securely. They collaborate closely on implementing GitOps methodologies, ensuring that the cluster state always reflects the source of truth in the Git repository.

### 2. Database and Storage Specialist
While EKS is excellent for stateless workloads, running stateful applications (databases) in Kubernetes requires careful coordination. The EKS Specialist works with the Database Specialist to provision and manage Persistent Volumes (PVs) and Persistent Volume Claims (PVCs) backed by AWS EBS or EFS. They collaborate on configuring StatefulSets, managing database operators, and ensuring that storage performance meets the database requirements. In many cases, the Database Specialist will manage RDS or DynamoDB instances outside the cluster, and the EKS Specialist will configure IRSA to allow pods to securely access those external databases.

### 3. Security and Compliance Specialist
Security is a shared responsibility. The Security Specialist defines the organizational security policies, and the EKS Specialist implements them within the cluster. This involves configuring Pod Security Standards, implementing OPA Gatekeeper policies, setting up network policies, and ensuring that the EKS cluster complies with frameworks like CIS Benchmarks or SOC 2. The EKS Specialist also works with the Security team to integrate vulnerability scanning for container images and to monitor the cluster for anomalous behavior using tools like Falco or AWS GuardDuty.

### 4. Cloud Networking Specialist
The EKS cluster resides within the broader AWS network architecture. The Cloud Networking Specialist designs the VPCs, Transit Gateways, and Direct Connect links. The EKS Specialist must understand this topology to configure the VPC CNI correctly, manage IP address allocation, and ensure that pods can communicate with on-premises resources or other VPCs. They collaborate heavily on configuring Ingress controllers, AWS Load Balancer Controllers, and ensuring that security groups allow the necessary traffic flow while maintaining a strong security posture.

### 5. Observability and Monitoring Specialist
An EKS cluster is a complex distributed system that requires comprehensive observability. The EKS Specialist works with the Observability Specialist to deploy and configure monitoring agents (e.g., Prometheus, Fluent Bit, Datadog agents) as DaemonSets within the cluster. They collaborate on defining critical alerts for cluster health (e.g., node CPU exhaustion, API server latency, pod crash loops) and creating dashboards that provide visibility into both infrastructure and application performance. The EKS Specialist relies on the tools managed by the Observability Specialist to troubleshoot production incidents effectively.

### 6. Cloud Architecture Specialist
The Cloud Architecture Specialist defines the overarching cloud strategy and architectural patterns. The EKS Specialist ensures that the Kubernetes platform aligns with this strategy. For example, if the Cloud Architect mandates a multi-region active-active architecture, the EKS Specialist must design and manage multiple EKS clusters across different regions, implementing global load balancing and cross-cluster communication mechanisms. They work together to evaluate new AWS services and determine how they can be integrated into the Kubernetes ecosystem to improve performance, reliability, or cost-efficiency.

---
**Document Version:** 1.0
**Author:** Manus AI
**Classification:** Internal / Highly Confidential

## === FILE: 37-k8s-eks-troubleshooting.md ===
# Kubernetes and EKS Deep Troubleshooting Guide: Production Operations & Tech Support

## 1. Introduction

In modern cloud-native architectures, Amazon Elastic Kubernetes Service (EKS) and Kubernetes serve as the backbone for mission-critical applications. However, the complexity of distributed systems introduces a myriad of failure modes that can disrupt production environments. This comprehensive guide is designed for tech support specialists, Site Reliability Engineers (SREs), and platform operators who are tasked with diagnosing and resolving the most severe and elusive issues in Kubernetes and EKS clusters. 

This document goes beyond basic `kubectl get pods` commands. It delves into the deep technical underpinnings of Kubernetes components, the AWS infrastructure that supports EKS, and the intricate interactions between them. We will explore worst-case scenarios, advanced diagnostic techniques, and battle-tested remediation strategies for CrashLoopBackOff, OOMKilled events, DNS resolution failures, Container Network Interface (CNI) problems, Node NotReady states, and IAM Roles for Service Accounts (IRSA) failures.

## 2. CrashLoopBackOff: Beyond the Basics

The `CrashLoopBackOff` state is one of the most common yet frustrating issues encountered in Kubernetes. It indicates that a pod is repeatedly crashing immediately after starting, and the kubelet is applying an exponential backoff delay before attempting to restart it. While the symptom is uniform, the root causes are highly diverse.

### 2.1. Diagnostic Workflow

When confronted with a `CrashLoopBackOff`, the initial step is to inspect the pod's logs and state. However, in production, logs might be missing if the container crashes too quickly.

1. **Inspect Previous Container Logs:**
   Use the `-p` (previous) flag to view the logs of the crashed container instance.
   ```bash
   kubectl logs <pod-name> -c <container-name> -p
   ```

2. **Analyze Pod Events:**
   The events associated with the pod often reveal issues related to scheduling, image pulling, or probe failures.
   ```bash
   kubectl describe pod <pod-name>
   ```

3. **Examine Exit Codes:**
   The exit code of the terminated container provides critical clues.
   - **Exit Code 1:** Application error (e.g., unhandled exception, missing configuration).
   - **Exit Code 137:** OOMKilled (Out of Memory) or forced termination via SIGKILL.
   - **Exit Code 143:** Graceful termination via SIGTERM.
   - **Exit Code 255:** Out of bounds exit code, often related to entrypoint script failures.

### 2.2. Common Root Causes and Deep Dives

#### 2.2.1. Misconfigured Liveness and Readiness Probes
Probes that are too aggressive or incorrectly configured can force the kubelet to repeatedly kill a perfectly healthy application.
- **Symptom:** The application starts, but the liveness probe fails before the application is fully initialized.
- **Deep Dive:** Analyze the `initialDelaySeconds`, `periodSeconds`, and `timeoutSeconds`. In slow-starting applications (e.g., legacy Java monoliths), the `initialDelaySeconds` must be sufficient. Alternatively, implement a `startupProbe` to defer liveness checks until the application has successfully started.

#### 2.2.2. Missing Dependencies and Configuration
Applications often crash if they cannot connect to a database, cache, or external API, or if required ConfigMaps/Secrets are missing.
- **Symptom:** Logs indicate connection timeouts or missing environment variables.
- **Deep Dive:** Verify the existence and contents of ConfigMaps and Secrets. Ensure that network policies or security groups are not blocking outbound traffic to required dependencies. Use ephemeral debug containers to test connectivity from within the pod's network namespace.
  ```bash
  kubectl debug -it <pod-name> --image=busybox:1.28 --target=<container-name>
  ```

#### 2.2.3. Entrypoint and Command Failures
Issues with the Dockerfile's `ENTRYPOINT` or `CMD`, or shell script syntax errors.
- **Symptom:** The container exits immediately with code 1 or 127 (command not found).
- **Deep Dive:** Override the command to keep the container alive for debugging.
  ```yaml
  command: ["sleep", "3600"]
  ```
  Once running, `exec` into the container and manually run the entrypoint script to observe the failure in real-time.

## 3. OOMKilled: Memory Management and Deep Diagnostics

An `OOMKilled` (Out of Memory) event occurs when a container exceeds its allocated memory limit, prompting the Linux kernel's OOM killer to terminate the process to protect the node's stability.

### 3.1. Understanding Kubernetes Memory Limits vs. Requests

- **Requests:** The guaranteed amount of memory allocated to the container. Used by the scheduler to place the pod on a suitable node.
- **Limits:** The absolute maximum amount of memory the container is allowed to use. Exceeding this triggers the OOM killer.

### 3.2. Diagnostic Workflow

1. **Identify OOMKilled Pods:**
   ```bash
   kubectl get pods -A | grep OOMKilled
   ```

2. **Verify the Exit Code:**
   Check the pod description for `Reason: OOMKilled` and `Exit Code: 137`.

3. **Analyze Node-Level OOM Events:**
   Sometimes, the entire node experiences memory pressure, leading to the eviction of pods. Check the node's kernel logs (dmesg) for OOM killer invocations.
   ```bash
   dmesg -T | grep -i oom
   ```

### 3.3. Deep Dive: Java and Memory Limits

Java applications are notorious for OOM issues in Kubernetes due to the JVM's default heap sizing behavior.
- **The Problem:** Older JVMs do not respect cgroup memory limits. They calculate the default heap size based on the host node's total memory, not the container's limit. This inevitably leads to the JVM attempting to allocate more memory than the container is allowed, resulting in an OOMKilled event.
- **The Solution:** Ensure the use of Java 10+ (or Java 8u191+) which includes `UseContainerSupport` (enabled by default). Explicitly set the heap size using `-XX:MaxRAMPercentage` (e.g., 75.0) rather than hardcoding `-Xmx`, allowing the JVM to scale dynamically with the container's memory limit.

### 3.4. Memory Leaks and Profiling

If an application's memory usage grows unbounded over time, it likely has a memory leak.
- **Diagnostic Action:** Capture a heap dump before the container is killed. This can be challenging if the container crashes unpredictably.
- **Advanced Technique:** Configure the application to automatically generate a heap dump on OOM and write it to a persistent volume.
  ```bash
  -XX:+HeapDumpOnOutOfMemoryError -XX:HeapDumpPath=/mnt/pv/heapdump.hprof
  ```
  Analyze the heap dump using tools like Eclipse MAT or VisualVM to identify the objects consuming the most memory.

## 4. DNS Resolution Issues: CoreDNS and VPC DNS

DNS resolution failures in Kubernetes manifest as applications being unable to communicate with other services or external endpoints. In EKS, DNS relies on CoreDNS running within the cluster and the AWS VPC DNS resolver.

### 4.1. Symptoms of DNS Failures

- Applications log `UnknownHostException` or `NXDOMAIN` errors.
- Intermittent connection timeouts to internal services (e.g., `my-svc.default.svc.cluster.local`).
- High latency in API calls due to DNS lookup delays.

### 4.2. Diagnostic Workflow

1. **Test DNS Resolution from a Pod:**
   Deploy a diagnostic pod (e.g., `dnsutils`) and test resolution using `nslookup` or `dig`.
   ```bash
   kubectl run -i --tty --rm debug --image=infoblox/dnstools --restart=Never -- sh
   # Inside the pod:
   nslookup kubernetes.default
   nslookup google.com
   ```

2. **Check CoreDNS Pods:**
   Ensure the CoreDNS pods are running and not in a CrashLoopBackOff state.
   ```bash
   kubectl get pods -n kube-system -l k8s-app=kube-dns
   ```

3. **Inspect CoreDNS Logs:**
   Look for errors, warnings, or high query rates.
   ```bash
   kubectl logs -n kube-system -l k8s-app=kube-dns
   ```

### 4.3. Deep Dive: ndots and DNS Search Domains

A common cause of DNS performance issues and intermittent failures in Kubernetes is the `ndots` configuration in the pod's `/etc/resolv.conf`.
- **The Problem:** By default, Kubernetes sets `ndots:5`. This means that for any domain name with fewer than 5 dots (e.g., `google.com`), the DNS resolver will append all the search domains (e.g., `default.svc.cluster.local`, `svc.cluster.local`, `cluster.local`, `ec2.internal`) and query them sequentially before finally querying the absolute name. This results in multiple unnecessary DNS queries, increasing latency and load on CoreDNS.
- **The Solution:** If an application frequently queries external domains, reduce the `ndots` value in the pod's `dnsConfig`.
  ```yaml
  dnsConfig:
    options:
      - name: ndots
        value: "2"
  ```

### 4.4. EKS Specifics: VPC DNS Throttling

AWS limits DNS queries to the VPC DNS resolver (the `.2` address) to 1024 packets per second per elastic network interface (ENI).
- **The Problem:** If CoreDNS pods are concentrated on a few nodes, they can easily exceed this limit, resulting in dropped DNS queries and intermittent resolution failures.
- **The Solution:** Implement NodeLocal DNSCache. This deploys a DNS caching agent as a DaemonSet on every node, significantly reducing the load on CoreDNS and avoiding VPC DNS throttling by caching responses locally on the node.

## 5. CNI Problems: VPC CNI, IP Exhaustion, and Routing

The Container Network Interface (CNI) is responsible for assigning IP addresses to pods and configuring network routing. In EKS, the default is the Amazon VPC CNI, which assigns native VPC IP addresses to pods.

### 5.1. Symptoms of CNI Failures

- Pods remain in the `ContainerCreating` state indefinitely.
- Events show `FailedCreatePodSandBox` with errors related to network plugin initialization or IP allocation.
- Pods cannot communicate with each other or external networks.

### 5.2. Deep Dive: VPC IP Exhaustion

The most common issue with the Amazon VPC CNI is IP address exhaustion.
- **The Mechanism:** The VPC CNI attaches secondary ENIs to the EC2 worker nodes and assigns secondary IP addresses from the VPC subnets to these ENIs. Each EC2 instance type has a hard limit on the number of ENIs and IPs per ENI it can support.
- **The Problem:** If the subnets are too small, or if the node is running many small pods, the CNI may run out of available IP addresses to assign to new pods.
- **Diagnostic Action:**
  Check the subnet's available IP addresses in the AWS VPC Console.
  Check the `aws-node` daemonset logs for IP allocation errors.
  ```bash
  kubectl logs -n kube-system -l k8s-app=aws-node
  ```
- **The Solution:**
  1. **Custom Networking:** Configure the VPC CNI to use a secondary CIDR block (e.g., 100.64.0.0/10 - CGNAT space) specifically for pods, freeing up the primary VPC CIDR for nodes and other AWS resources.
  2. **Prefix Delegation:** Enable Prefix Delegation in the VPC CNI. Instead of assigning individual IPs to ENIs, it assigns /28 prefixes, significantly increasing the number of pods that can run on a single node and reducing the frequency of AWS API calls.

### 5.3. SNAT and Outbound Connectivity

Pods need to communicate with the internet (e.g., to pull images or access external APIs).
- **The Problem:** By default, the VPC CNI translates the pod's IP address to the node's primary IP address (Source Network Address Translation - SNAT) for traffic destined outside the VPC. If `AWS_VPC_K8S_CNI_EXTERNALSNAT` is misconfigured, or if the node lacks a NAT Gateway/Public IP, outbound traffic will fail.
- **Diagnostic Action:** Verify the `aws-node` DaemonSet environment variables. Ensure the subnets have appropriate route tables pointing to a NAT Gateway (for private subnets) or an Internet Gateway (for public subnets).

## 6. Node NotReady: Kubelet, Container Runtime, and EC2 Health

A node entering the `NotReady` state means the Kubernetes control plane can no longer communicate with the kubelet running on that node, or the kubelet has reported that the node is unhealthy.

### 6.1. Diagnostic Workflow

1. **Check Node Status and Conditions:**
   ```bash
   kubectl describe node <node-name>
   ```
   Look at the `Conditions` section. Is `MemoryPressure`, `DiskPressure`, or `PIDPressure` set to True?

2. **Access the Node:**
   If possible, SSH into the node or use AWS Systems Manager (SSM) Session Manager.

3. **Inspect Kubelet Logs:**
   The kubelet is the primary agent on the node. Its logs are crucial.
   ```bash
   journalctl -u kubelet -f
   ```

### 6.2. Common Root Causes

#### 6.2.1. Resource Exhaustion (CPU/Memory/Disk)
- **Symptom:** The node becomes unresponsive, and the kubelet fails to send heartbeats to the API server.
- **Deep Dive:** If a node runs out of memory and the OOM killer terminates the kubelet or container runtime (containerd/Docker), the node will become `NotReady`. Similarly, if the root filesystem (`/`) or the container runtime filesystem (`/var/lib/containerd`) reaches 100% capacity, the kubelet will mark the node with `DiskPressure` and eventually transition to `NotReady`.
- **Solution:** Implement proper resource requests and limits for all pods. Configure kubelet eviction thresholds (`evictionHard`) to proactively evict pods before the node reaches a critical state.

#### 6.2.2. Container Runtime Failures
- **Symptom:** The kubelet logs show errors communicating with the container runtime (e.g., containerd socket timeouts).
- **Deep Dive:** The container runtime can hang due to deadlocks, storage driver issues, or kernel bugs. Restarting the runtime service (`systemctl restart containerd`) often resolves the immediate issue, but root cause analysis requires inspecting the runtime logs (`journalctl -u containerd`).

#### 6.2.3. AWS Infrastructure Issues
- **Symptom:** The node is `NotReady`, and SSH/SSM access fails.
- **Deep Dive:** The underlying EC2 instance may have failed a status check (System Status Check or Instance Status Check). Check the AWS EC2 Console. If the instance is impaired, terminate it and let the Auto Scaling Group (ASG) or Karpenter provision a replacement.

## 7. IAM Roles for Service Accounts (IRSA) Failures

IRSA allows you to assign AWS IAM roles directly to Kubernetes Service Accounts. This provides fine-grained, pod-level access control to AWS resources (e.g., S3, DynamoDB) without relying on node-level IAM roles or hardcoded credentials.

### 7.1. How IRSA Works

IRSA relies on an OpenID Connect (OIDC) identity provider configured in the EKS cluster. When a pod uses a Service Account annotated with an IAM role, the EKS pod identity webhook injects AWS credentials (a web identity token file and environment variables) into the pod. The AWS SDKs within the pod use this token to assume the IAM role.

### 7.2. Symptoms of IRSA Failures

- Applications log `AccessDenied` errors when attempting to access AWS resources.
- The AWS SDK reports that it cannot find credentials.

### 7.3. Diagnostic Workflow and Deep Dive

1. **Verify the Service Account Annotation:**
   Ensure the Service Account has the correct annotation pointing to the IAM role ARN.
   ```bash
   kubectl describe sa <service-account-name> -n <namespace>
   # Look for: eks.amazonaws.com/role-arn: arn:aws:iam::123456789012:role/my-role
   ```

2. **Verify Pod Configuration:**
   Check if the pod is actually using the Service Account and if the webhook successfully injected the environment variables and volume mounts.
   ```bash
   kubectl describe pod <pod-name>
   # Look for environment variables: AWS_ROLE_ARN and AWS_WEB_IDENTITY_TOKEN_FILE
   # Look for volume mounts: aws-iam-token
   ```
   *Failure Point:* If these are missing, the pod identity webhook might be failing, or the pod was created before the Service Account was annotated. Delete the pod to force a recreation.

3. **Inspect the IAM Role Trust Policy:**
   This is the most common point of failure. The IAM role must have a trust policy that allows the OIDC provider to assume the role, specifically for the designated Service Account and namespace.
   ```json
   {
     "Version": "2012-10-17",
     "Statement": [
       {
         "Effect": "Allow",
         "Principal": {
           "Federated": "arn:aws:iam::123456789012:oidc-provider/oidc.eks.region.amazonaws.com/id/EXAMPLED539D4633E53DE1B71EXAMPLE"
         },
         "Action": "sts:AssumeRoleWithWebIdentity",
         "Condition": {
           "StringEquals": {
             "oidc.eks.region.amazonaws.com/id/EXAMPLED539D4633E53DE1B71EXAMPLE:sub": "system:serviceaccount:<namespace>:<service-account-name>",
             "oidc.eks.region.amazonaws.com/id/EXAMPLED539D4633E53DE1B71EXAMPLE:aud": "sts.amazonaws.com"
           }
         }
       }
     ]
   }
   ```
   *Failure Point:* Typos in the namespace or service account name in the `Condition` block will result in silent failures (AccessDenied).

4. **Verify AWS SDK Version:**
   Ensure the application is using an AWS SDK version that supports `AssumeRoleWithWebIdentity`. Older SDKs will ignore the injected environment variables and fall back to the node's IAM role (which should ideally have no permissions).

## 8. Worst-Case Scenarios and Disaster Recovery

In extreme situations, multiple failures can cascade, leading to a complete cluster outage.

### 8.1. Control Plane Exhaustion (API Server Overload)
- **Scenario:** A misconfigured controller or a massive surge in deployments floods the Kubernetes API server with requests, causing it to become unresponsive. `kubectl` commands time out.
- **Mitigation:** In EKS, the control plane is managed by AWS. However, you can still impact it. Identify the source of the API spam. If it's a specific deployment, scale it down. Utilize API Priority and Fairness (APF) to throttle abusive clients and protect critical system components.

### 8.2. Complete Network Partition
- **Scenario:** A misconfigured Network Policy or a failure in the CNI daemonset isolates all pods, preventing any internal or external communication.
- **Mitigation:** Temporarily disable enforcing Network Policies (if possible) to restore baseline connectivity. Roll back recent changes to the CNI configuration. If the CNI is completely broken, you may need to manually delete the CNI daemonset and reapply the manifest.

### 8.3. Etcd Data Corruption (Self-Managed Kubernetes)
- **Scenario:** The etcd database, which stores the entire cluster state, becomes corrupted or loses quorum.
- **Mitigation:** In EKS, AWS manages etcd backups and recovery. In self-managed clusters, this is a catastrophic event requiring a restore from the latest etcd snapshot.
  ```bash
  ETCDCTL_API=3 etcdctl snapshot restore snapshot.db     --name m1     --initial-cluster m1=http://host1:2380,m2=http://host2:2380,m3=http://host3:2380     --initial-cluster-token etcd-cluster-1     --initial-advertise-peer-urls http://host1:2380
  ```

## 8.4. Persistent Volume (PV) and Persistent Volume Claim (PVC) Failures
Storage issues can cause pods to hang in `ContainerCreating` or fail to start.
- **Scenario:** A pod requests a PVC, but the underlying EBS volume fails to attach to the EC2 node.
- **Deep Dive:** Check the PVC status (`kubectl get pvc`). If it's `Pending`, the storage class might be misconfigured or the AWS EBS CSI driver might be failing. Check the CSI driver logs.
- **EBS Limits:** EC2 instances have limits on the number of attached EBS volumes. If a node reaches this limit, new pods requiring storage will fail to schedule or start.

## 8.5. Ingress Controller and Load Balancer Bottlenecks
- **Scenario:** External traffic fails to reach services, or latency is extremely high.
- **Deep Dive:** In EKS, this often involves the AWS Load Balancer Controller. Check the controller logs for errors provisioning ALBs or NLBs. Verify that the subnets are correctly tagged (`kubernetes.io/role/elb` or `kubernetes.io/role/internal-elb`) so the controller can discover them.

## 8.6. Certificate Expiration and TLS Failures
- **Scenario:** Webhooks fail, or internal communication between components breaks down due to expired TLS certificates.
- **Deep Dive:** Kubernetes relies heavily on mutual TLS (mTLS). Check the expiration dates of certificates in the `kube-system` namespace. Use tools like `cert-manager` to automate certificate renewal and prevent these outages.

## 9. Advanced Debugging Tools and Techniques

### 9.1. Ephemeral Containers
Introduced as a stable feature in recent Kubernetes versions, ephemeral containers allow you to attach a debug container to a running pod without restarting it. This is invaluable for debugging distroless images or containers that lack basic shell utilities.
```bash
kubectl debug -it <pod-name> --image=nicolaka/netshoot --target=<container-name>
```

### 9.2. Network Packet Capture (tcpdump)
When diagnosing complex network issues (e.g., dropped packets, unexpected resets), capturing traffic at the node or pod level is necessary.
- **Node Level:** SSH into the node and run `tcpdump` on the `eni` or `cali` interfaces.
- **Pod Level:** Use an ephemeral container with `tcpdump` installed to capture traffic directly within the pod's network namespace.

### 9.3. Strace and Sysdig
For deep system-level debugging, tools like `strace` (to trace system calls) and `sysdig` (for comprehensive system exploration) can reveal exactly what a process is doing, which files it's trying to open, and where it's getting stuck.

## 9.4. EKS Control Plane Logging
EKS provides the ability to export control plane logs to Amazon CloudWatch. This is critical for auditing and troubleshooting API server, scheduler, and controller manager issues.
- **Enable Logging:** Ensure that API, audit, authenticator, controllerManager, and scheduler logs are enabled in the EKS cluster configuration.
- **Analysis:** Use CloudWatch Logs Insights to query the logs. For example, to find all failed API requests:
  ```
  fields @timestamp, @message
  | filter @logStream like /^kube-apiserver/
  | filter responseStatus.code >= 400
  | sort @timestamp desc
  ```

## 9.5. Karpenter vs. Cluster Autoscaler
Scaling issues often lead to pending pods. Understanding the autoscaling mechanism is crucial.
- **Cluster Autoscaler:** Relies on AWS Auto Scaling Groups (ASGs). It can be slow and requires careful configuration of node groups.
- **Karpenter:** A newer, high-performance autoscaler that bypasses ASGs and provisions EC2 instances directly based on pod requirements. Troubleshooting Karpenter involves checking its logs and the `Provisioner` custom resources.

## 10. Security and Compliance Troubleshooting

### 10.1. Pod Security Admission (PSA)
With the deprecation of Pod Security Policies (PSP), PSA is the standard for enforcing security standards.
- **Symptom:** Pods fail to create with errors related to security context (e.g., `violates PodSecurity "restricted"`).
- **Solution:** Review the namespace labels (`pod-security.kubernetes.io/enforce`) and adjust the pod's `securityContext` to comply with the required profile (Privileged, Baseline, or Restricted).

### 10.2. Network Policies
- **Symptom:** Pods can communicate with some services but not others.
- **Solution:** Network Policies act as firewalls for pods. Use tools like `cilium network-policy-editor` or carefully review the YAML definitions to ensure the `podSelector`, `ingress`, and `egress` rules are correctly configured. Remember that Network Policies are default-deny once applied to a pod.

## 11. Conclusion

Troubleshooting Kubernetes and EKS in production requires a deep understanding of both the Kubernetes architecture and the underlying AWS infrastructure. By mastering the diagnostic workflows for CrashLoopBackOff, OOMKilled, DNS, CNI, Node readiness, and IRSA, tech support specialists and SREs can rapidly identify root causes and implement robust solutions. 

The key to successful operations is not just fixing the immediate issue, but understanding *why* it happened and implementing preventative measures—such as proper resource limits, optimized DNS configurations, and robust IAM policies—to ensure the long-term stability and resilience of the cluster. Continuous monitoring, proactive alerting, and regular disaster recovery drills are essential components of a mature Kubernetes operational strategy.

---
**References:**
[1] Kubernetes Documentation: Debugging Pods - https://kubernetes.io/docs/tasks/debug/debug-application/debug-pods/
[2] AWS EKS Documentation: Troubleshooting IAM Roles for Service Accounts - https://docs.aws.amazon.com/eks/latest/userguide/troubleshooting-iam-roles-for-service-accounts.html
[3] Amazon VPC CNI Plugin for Kubernetes - https://github.com/aws/amazon-vpc-cni-k8s
[4] CoreDNS Performance and Scaling - https://coredns.io/manual/scaling/

