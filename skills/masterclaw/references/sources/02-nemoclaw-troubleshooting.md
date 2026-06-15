# Nemoclaw Troubleshooting & Diagnostics Guide

## 1. Introduction

Welcome to the comprehensive Troubleshooting and Diagnostics Guide for Nemoclaw. Nemoclaw is a highly distributed, fault-tolerant orchestration and execution engine designed for high-throughput data processing, microservices management, and complex stateful workloads. While Nemoclaw is built with resilience in mind, complex deployments inevitably encounter edge cases, network partitions, resource exhaustion, and configuration drifts.

This guide is intended for Site Reliability Engineers (SREs), DevOps professionals, system administrators, and platform engineers who are responsible for maintaining the health, performance, and reliability of Nemoclaw clusters. It provides deep technical insights into diagnosing issues, interpreting error codes, executing recovery strategies, performing routine health checks, and optimizing the system for peak performance. By mastering the concepts and procedures outlined in this document, you will be equipped to handle everything from minor transient errors to catastrophic cluster-wide failures.

## 2. Architecture Overview & Failure Domains

To effectively troubleshoot Nemoclaw, one must possess a deep understanding of its core architecture and the potential failure domains. Nemoclaw operates on a decoupled control-plane and data-plane model, ensuring that control plane failures do not immediately impact running workloads.

### 2.1 Control Plane
The Control Plane is the brain of the cluster, responsible for state management, scheduling, API serving, and controller loops.
- **Nemo-API Server:** The central entry point for all administrative, operational, and automated commands. It handles authentication, authorization, admission control, and API routing.
- **State Store (Nemo-KV):** A highly available, distributed key-value store (based on the Raft consensus algorithm) that maintains the entire cluster state, including configurations, secrets, and workload statuses.
- **Scheduler:** The component that evaluates resource requirements, node affinities, taints, and tolerations to assign pending workloads to the most appropriate worker nodes.
- **Controller Manager:** Runs various background control loops that regulate the state of the cluster, ensuring the actual state matches the desired state declared by the user.

*Failure Domains:* Split-brain scenarios in Nemo-KV leading to data corruption, API server rate-limiting causing control plane unresponsiveness, scheduler deadlocks due to complex constraints, and controller loop crashes.

### 2.2 Data Plane
The Data Plane consists of the worker nodes that execute the actual workloads and the networking infrastructure that connects them.
- **Nemolet:** The primary agent running on each worker node. It registers the node with the control plane, manages the lifecycle of tasks, and reports node health and resource utilization.
- **Execution Engine:** The runtime environment (e.g., container runtime, WebAssembly engine, or VM hypervisor) responsible for isolating and executing the tasks.
- **Network Proxy (Nemo-Proxy):** Handles inter-node communication, service discovery, load balancing, and network policy enforcement.

*Failure Domains:* Out-of-memory (OOM) kills by the Linux kernel, network partitions between workers or between workers and the control plane, disk I/O bottlenecks, and container runtime deadlocks.

## 3. Health Checks and Monitoring

Proactive monitoring is the first line of defense against system degradation. Nemoclaw exposes several endpoints, metrics, and logging mechanisms for comprehensive health verification.

### 3.1 Liveness, Readiness, and Startup Probes
Every Nemoclaw component and user workload supports configurable probes.
- **`/healthz` (Liveness):** Indicates if the process is running and healthy. A failure here indicates a deadlock or unrecoverable error, triggering an automatic restart of the component by the process manager.
- **`/readyz` (Readiness):** Indicates if the component is fully initialized and ready to accept traffic or workloads. A failure here removes the component from the active load balancing pool without restarting it, allowing it time to recover or initialize.
- **`/startupz` (Startup):** Used for legacy applications or components that require a long time to initialize. It disables liveness and readiness checks until it succeeds, preventing premature restarts.

### 3.2 Key Metrics to Monitor
Nemoclaw natively exports Prometheus-compatible metrics at the `/metrics` endpoint on all components. Key metrics that require alerting include:
- `nemoclaw_api_request_duration_seconds`: Latency of API requests. High latency (e.g., >500ms for reads, >2s for writes) indicates control plane overload or Nemo-KV degradation.
- `nemoclaw_scheduler_queue_length`: The number of pending tasks. A continuously growing queue indicates insufficient worker capacity, a stalled scheduler, or impossible scheduling constraints.
- `nemoclaw_worker_memory_usage_bytes` & `nemoclaw_worker_cpu_usage_seconds`: Resource consumption per worker. Crucial for predicting OOM events and CPU throttling.
- `nemoclaw_kv_consensus_latency_ms`: Time taken to achieve consensus in the state store. High values (>50ms) indicate network issues, disk latency on control nodes, or CPU starvation.
- `nemoclaw_network_transmit_errors_total`: Indicates dropped packets or network interface saturation on worker nodes.

### 3.3 Synthetic Transactions and Blackbox Monitoring
Relying solely on internal metrics is insufficient. Implement synthetic transactions (canary workloads) that periodically submit a lightweight, end-to-end task to the cluster. Measure the time to scheduling, execution, and completion. This provides a holistic health metric that catches issues isolated component metrics might miss, such as DNS resolution failures or subtle network policies blocking traffic.

## 4. Common Issues and Resolutions

### 4.1 Worker Node Disconnection (Ghost Nodes)
**Symptom:** A worker node appears as `NotReady` or `Unknown` in the cluster state, but the underlying virtual machine or physical server is still running and accessible via SSH.
**Diagnosis:**
1. Check the network connectivity between the worker node and the control plane API server using `curl -k https://<api-server-ip>:6443/version`.
2. Inspect the `nemolet` logs on the affected node: `journalctl -u nemolet -f`. Look for connection timeouts or TLS handshake errors.
3. Verify TLS certificate validity. Nemoclaw uses mutual TLS (mTLS) for all internal communication.
4. Check for clock skew. Nemoclaw requires strict time synchronization (NTP) across all nodes. A skew of more than a few seconds can invalidate authentication tokens.
**Resolution:**
- If clock skew is detected, force an NTP sync: `chronyc makestep` or `systemctl restart systemd-timesyncd`.
- If certificates are expired, trigger a manual certificate rotation: `nemocli certs renew --node <node-name>` and restart the `nemolet` service.
- If a network partition occurred, resolve the underlying network routing, firewall, or security group issue. The node should automatically rejoin and reconcile its state once connectivity is restored.

### 4.2 Scheduler Deadlock (Pending Tasks Accumulation)
**Symptom:** Tasks remain in the `Pending` state indefinitely, despite apparent available resources on worker nodes.
**Diagnosis:**
1. Check the scheduler logs for errors related to resource constraints, affinity/anti-affinity rules, or taint/toleration mismatches.
2. Verify that the requested resources (CPU, Memory, GPU, Ephemeral Storage) do not exceed the maximum allocatable resources on any single node in the cluster. A task requesting 10 CPUs cannot be scheduled if the largest node only has 8 CPUs.
3. Inspect the Nemo-KV state for corrupted scheduling locks or stale node resource reports.
**Resolution:**
- If tasks have impossible constraints, update the task definition to request fewer resources or relax affinity rules.
- If the scheduler is stuck on a corrupted lock, restart the scheduler component. Nemoclaw's scheduler is stateless and will rebuild its queue and internal cache from the state store upon restart.
- Clear the scheduling cache manually: `nemocli admin cache clear --component scheduler`.

### 4.3 State Store (Nemo-KV) Quorum Loss
**Symptom:** The entire cluster becomes read-only or completely unresponsive. API requests time out or return 503 Service Unavailable.
**Diagnosis:**
1. Check the status of the Nemo-KV cluster: `nemocli cluster status --component kv`.
2. Identify how many control plane nodes are offline. Nemo-KV uses Raft and requires a strict majority (e.g., 3 out of 5 nodes) to maintain quorum and accept writes.
3. Check the disk space and I/O latency on the Nemo-KV nodes. A full disk or slow disk will cause the Raft leader to step down.
**Resolution:**
- If nodes are temporarily down (e.g., rebooting), wait for them to return. The cluster will automatically recover quorum.
- If disk space is full, expand the volume or clear old snapshots and Write-Ahead Logs (WAL).
- If nodes are permanently lost and quorum cannot be restored, you must perform a disaster recovery procedure from the last known good backup (see Section 6).

### 4.4 High Disk I/O on Worker Nodes
**Symptom:** Task execution slows down significantly. Node load average spikes. SSH access to the node becomes sluggish.
**Diagnosis:**
1. Use `iostat -x 1` or `dstat` to monitor disk utilization and await times.
2. Identify the specific process causing high I/O using `iotop`.
3. Check if tasks are writing excessive temporary data to the local disk instead of the designated distributed storage system.
**Resolution:**
- Enforce strict ephemeral storage quotas on all tasks via LimitRanges or ResourceQuotas.
- Evict offending tasks immediately: `nemocli task evict <task-id>`.
- Upgrade worker node storage to NVMe SSDs if the workload legitimately requires high IOPS.
- Configure separate physical disks for the container runtime overlay filesystem and the application data volumes.

## 5. Error Codes Reference

Nemoclaw standardizes its error reporting to facilitate automated remediation and easier debugging. Below is a comprehensive list of error codes, their meanings, and recommended actions.

### 5.1 Control Plane Errors (1xxx)
- **ERR-1001 (API_RATE_LIMIT_EXCEEDED):** The client is sending too many requests, triggering the API server's rate limiter. *Action:* Implement exponential backoff and jitter in the client application. Review automated scripts for aggressive polling.
- **ERR-1002 (UNAUTHORIZED_ACCESS):** Invalid, expired, or malformed authentication token. *Action:* Renew the token. Check the identity provider (OIDC/LDAP) integration.
- **ERR-1003 (FORBIDDEN_ACTION):** The authenticated user lacks the necessary Role-Based Access Control (RBAC) permissions. *Action:* Review and update the user's RoleBindings or ClusterRoleBindings.
- **ERR-1004 (STATE_STORE_UNAVAILABLE):** The API server cannot communicate with Nemo-KV. *Action:* Check Nemo-KV health, quorum status, and network connectivity between API and KV nodes.
- **ERR-1005 (RESOURCE_QUOTA_EXCEEDED):** The namespace has exhausted its allocated resources (CPU, memory, or object count). *Action:* Increase the namespace quota or delete unused resources.
- **ERR-1006 (ADMISSION_WEBHOOK_DENIED):** A mutating or validating admission webhook rejected the request. *Action:* Check the logs of the specific webhook service mentioned in the error message.

### 5.2 Scheduling Errors (2xxx)
- **ERR-2001 (INSUFFICIENT_RESOURCES):** No node has enough capacity to schedule the task. *Action:* Add more worker nodes (scale up the cluster) or reduce task resource requests.
- **ERR-2002 (AFFINITY_CONFLICT):** Node affinity, pod affinity, or anti-affinity rules cannot be satisfied. *Action:* Review and relax scheduling constraints. Ensure nodes have the correct labels.
- **ERR-2003 (TAINT_TOLERATION_MISMATCH):** The task does not tolerate the taints applied to the available nodes. *Action:* Add appropriate tolerations to the task specification or remove the taints from the nodes.
- **ERR-2004 (VOLUME_BINDING_FAILED):** The scheduler could not find a node that satisfies both the compute requirements and the persistent volume topology constraints. *Action:* Check storage class configurations and volume availability in the target zones.

### 5.3 Execution Errors (3xxx)
- **ERR-3001 (IMAGE_PULL_BACKOFF):** The worker cannot download the required container image. *Action:* Verify image registry credentials (ImagePullSecrets), image path, tag existence, and network access to the registry.
- **ERR-3002 (OOM_KILLED):** The task exceeded its memory limit and was terminated by the Linux kernel OOM killer. *Action:* Increase the memory limit for the task or profile and optimize the application's memory usage.
- **ERR-3003 (EXECUTION_TIMEOUT):** The task ran longer than its configured `max_duration` or `activeDeadlineSeconds`. *Action:* Optimize the task execution time or increase the timeout value.
- **ERR-3004 (LOCAL_STORAGE_EXHAUSTED):** The task filled up its ephemeral storage allocation. *Action:* Clean up temporary files (`/tmp`) during execution or request more ephemeral storage in the task spec.
- **ERR-3005 (RUNTIME_SANDBOX_FAILURE):** The container runtime failed to create the isolation sandbox (cgroups, namespaces). *Action:* Check the container runtime (containerd/CRI-O) logs on the worker node. Reboot the node if the kernel state is corrupted.

### 5.4 Network Errors (4xxx)
- **ERR-4001 (SERVICE_DISCOVERY_FAILURE):** The task cannot resolve the internal DNS name of a dependency. *Action:* Check the cluster DNS provider (e.g., CoreDNS) logs. Verify the `resolv.conf` inside the task.
- **ERR-4002 (CONNECTION_REFUSED):** The target service is not accepting connections. *Action:* Verify the target service is running, passing its readiness probes, and listening on the correct port.
- **ERR-4003 (NETWORK_POLICY_VIOLATION):** Traffic was blocked by a cluster network policy. *Action:* Review and update network policies to allow the required ingress/egress traffic flow. Use a network policy logging tool to identify dropped packets.
- **ERR-4004 (PORT_ALLOCATION_CONFLICT):** The task requested a host port that is already in use on the scheduled node. *Action:* Avoid using host ports; use NodePorts or LoadBalancers instead.

## 6. Recovery Strategies

When standard troubleshooting fails, you may need to employ advanced recovery strategies to restore service.

### 6.1 Graceful Node Drain and Maintenance
Before performing OS patching, hardware upgrades, or deep debugging on a worker node, it must be drained to safely evict running tasks.
```bash
nemocli node drain <node-name> --ignore-daemonsets --delete-local-data --force
```
This command cordons the node (preventing new tasks from being scheduled) and gracefully terminates existing tasks, allowing the scheduler to place them elsewhere. The `--delete-local-data` flag acknowledges that any local ephemeral data will be lost.

### 6.2 Control Plane Disaster Recovery (Restore from Backup)
If Nemo-KV loses quorum permanently (e.g., multiple simultaneous disk failures), you must restore from a snapshot. This is a destructive operation and will result in the loss of any state changes made after the snapshot was taken.
1. Stop all API servers and Controller Managers to prevent split-brain writes and erratic behavior.
2. Stop the Nemo-KV service on all control plane nodes.
3. Wipe the corrupted Nemo-KV data directories.
4. Initialize a new Nemo-KV cluster on a single node using the restore command:
   ```bash
   nemocli kv restore --snapshot-path /backups/nemokv-latest.snap --data-dir /var/lib/nemokv
   ```
5. Start the Nemo-KV service on the first node.
6. Join the remaining control plane nodes to the new Nemo-KV cluster one by one.
7. Restart the API servers and Controller Managers.
8. Verify cluster state. Tasks created after the snapshot was taken will be lost and must be resubmitted by the users or CI/CD pipelines.

### 6.3 Forcing Task Deletion
Sometimes a task gets stuck in a `Terminating` state indefinitely due to an unresponsive worker node, a deadlocked container runtime, or an unreachable storage backend. You can force delete it, but this bypasses graceful shutdown procedures.
```bash
nemocli task delete <task-id> --force --grace-period=0
```
*Warning:* This removes the task object from the control plane immediately. However, it can leave orphaned resources (like attached block volumes, running processes, or network interfaces) on the worker node. You may need to manually clean up the worker node later.

## 7. Advanced Debugging and Tracing

For complex, intermittent issues, or performance bottlenecks, deeper introspection is required.

### 7.1 Distributed Tracing
Nemoclaw natively supports OpenTelemetry for distributed tracing. Ensure tracing is enabled in the cluster configuration:
```yaml
telemetry:
  tracing:
    enabled: true
    provider: otlp
    endpoint: "http://otel-collector:4317"
    sampling_rate: 0.1 # Sample 10% of requests
```
Use the trace ID returned in the API response headers (`X-Nemoclaw-Trace-Id`) to follow the request lifecycle across the API server, admission webhooks, scheduler, and worker nodes. This is invaluable for diagnosing latency spikes and identifying exactly which component is slowing down a request.

### 7.2 Profiling Components (pprof)
If a control plane component (like the API server or scheduler) is consuming excessive CPU or memory, you can capture a Go pprof profile to identify the root cause in the code.
```bash
# Port forward to the component's debug port (requires admin privileges)
nemocli port-forward svc/nemo-api -n nemoclaw-system 6060:6060

# Capture a 30-second CPU profile
go tool pprof http://localhost:6060/debug/pprof/profile?seconds=30

# Capture a heap (memory) profile
go tool pprof http://localhost:6060/debug/pprof/heap
```
Analyze the profile using the interactive prompt or export it to a web UI to identify hot paths, lock contention, or memory leaks.

### 7.3 Ephemeral Debug Containers
If a task is failing but the application logs are insufficient, and the container image lacks debugging tools (e.g., a distroless image), you can inject an ephemeral debug container into the task's namespace.
```bash
nemocli task debug <task-id> --image=nicolaka/netshoot --target=main-container
```
This command drops you into an interactive shell sharing the same network, process, and IPC namespace as the failing task. You can now run tools like `tcpdump`, `strace`, `curl`, `dig`, and `nslookup` to diagnose the environment exactly as the application sees it.

## 8. Network Troubleshooting Deep Dive

Networking in Nemoclaw is often the most complex area to troubleshoot. Nemoclaw uses a Container Network Interface (CNI) plugin to manage pod-to-pod communication.

### 8.1 Diagnosing DNS Issues
DNS resolution failures are a common cause of application errors.
1. Check if the CoreDNS pods are running and healthy: `nemocli get tasks -n kube-system -l k8s-app=kube-dns`.
2. Check the CoreDNS logs for errors or upstream server timeouts.
3. Use a debug container to test resolution from within the cluster:
   ```bash
   nslookup my-service.default.svc.cluster.local
   ```
4. Verify that the node's `/etc/resolv.conf` is correctly configured and that the upstream DNS servers are reachable.

### 8.2 Diagnosing Network Policies
If services cannot communicate, a NetworkPolicy might be dropping the traffic.
1. List all network policies in the namespace: `nemocli get networkpolicies -n <namespace>`.
2. Review the ingress and egress rules. Ensure that the labels match the intended source and destination tasks.
3. Use a tool like `nemo-net-trace` (if installed) to simulate traffic and see which policy is dropping the packets.

### 8.3 Overlay Network Issues
If tasks on different nodes cannot communicate, but tasks on the same node can, the overlay network (e.g., Calico, Flannel, Cilium) might be broken.
1. Check the logs of the CNI agent daemonset running on the worker nodes.
2. Verify that the nodes can communicate over the encapsulation protocol port (e.g., UDP 8472 for VXLAN, IP protocol 4 for IPIP). Check firewalls and security groups.
3. Inspect the routing tables on the worker nodes: `ip route`. Ensure routes to the pod CIDRs of other nodes exist and point to the correct tunnel interface.

## 9. Storage and Volume Diagnostics

Stateful workloads rely on Persistent Volumes (PVs) and the Container Storage Interface (CSI).

### 9.1 Volume Attachment Failures
**Symptom:** A task is stuck in `ContainerCreating` with an error like `Multi-Attach error for volume`.
**Diagnosis:**
1. This usually happens when a task is rescheduled to a new node, but the cloud provider hasn't detached the block storage volume from the old node yet.
2. Check the `VolumeAttachment` objects: `nemocli get volumeattachments`.
**Resolution:**
- Wait for the cloud provider's API to complete the detachment.
- If it's permanently stuck, you may need to manually detach the volume via the cloud provider's console (AWS EC2, GCP Compute, etc.) and then delete the stuck `VolumeAttachment` object.

### 9.2 Filesystem Corruption
**Symptom:** The task starts, but the application crashes with input/output errors (EIO) when reading or writing to the volume.
**Diagnosis:**
1. Check the kernel logs on the worker node where the task is running: `dmesg -T | grep -i ext4` (or xfs). Look for filesystem corruption messages.
**Resolution:**
- Scale the task down to 0.
- Mount the volume to a debug node or use a debug pod.
- Run a filesystem check: `fsck.ext4 -y /dev/sdX`.
- If the corruption is unrecoverable, restore the data from a volume snapshot or application-level backup.

## 10. Log Analysis and Telemetry

Effective log analysis is critical for rapid root cause identification.

### 10.1 Dynamic Log Levels
Nemoclaw components support dynamic log level adjustment without requiring a restart, which is crucial for debugging production issues without causing downtime.
```bash
nemocli admin log-level set --component scheduler --level debug
```
Available levels: `fatal`, `error`, `warn`, `info`, `debug`, `trace`. Use `debug` or `trace` only temporarily, as they generate massive amounts of data and can impact performance. Remember to revert to `info` when debugging is complete.

### 10.2 Structured Logging
All Nemoclaw control plane logs are output in JSON format. When querying logs in your centralized logging system (e.g., Elasticsearch, Splunk, Datadog), filter by specific structured fields:
- `component`: The subsystem generating the log (e.g., `nemolet`, `scheduler`, `api-server`).
- `task_id`: The unique identifier of the workload.
- `node_name`: The worker node where the event occurred.
- `error_code`: The specific ERR-XXXX code.
- `trace_id`: For correlating logs with distributed traces.

### 10.3 Audit Logs
For security, compliance, and post-mortem troubleshooting, consult the API audit logs. These logs record every mutating request (POST, PUT, PATCH, DELETE) made to the cluster, including the user identity, timestamp, source IP, and the exact payload. Audit logs are typically written to a secure, append-only storage system and are essential for answering "who changed what and when."

## 11. Support and Escalation

If you have exhausted all troubleshooting steps in this guide, consulted the internal knowledge base, and the issue persists, it is time to escalate to Nemoclaw Enterprise Support.

### 11.1 Gathering Diagnostic Data (Nemo-Inspect)
Before opening a support ticket, gather a comprehensive diagnostic bundle. Nemoclaw provides a built-in tool for this purpose, which safely collects logs and state without exposing sensitive secrets.
```bash
nemocli admin inspect cluster --output-dir /tmp/nemo-diag
tar -czvf nemoclaw-diagnostics.tar.gz /tmp/nemo-diag
```
This archive includes:
- Component logs (last 10,000 lines for each control plane component).
- Current cluster state export (excluding Secrets).
- Node health summaries and resource utilization.
- Recent event history.
- Anonymized configuration files and feature gate statuses.

### 11.2 Engaging Enterprise Support
When contacting Nemoclaw Enterprise Support, provide the following information to ensure rapid triage and resolution:
1. The `nemoclaw-diagnostics.tar.gz` bundle.
2. A detailed description of the symptom, the business impact, and the urgency.
3. The exact steps to reproduce the issue (if known and reproducible).
4. A timeline of events leading up to the failure.
5. Any recent changes to the cluster configuration, application deployments, or underlying infrastructure (e.g., network changes, OS upgrades).
6. The Nemoclaw version and the underlying OS/Kernel versions.

By following this structured, methodical approach to troubleshooting, you can minimize downtime, maintain cluster stability, and ensure the reliable execution of your critical workloads on the Nemoclaw platform.