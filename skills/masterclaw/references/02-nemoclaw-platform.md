# NemoClaw Distributed Orchestration & Execution Platform — Complete Reference

> **Official Sources:** [NVIDIA NemoClaw GitHub Repository](https://github.com/NVIDIA/NemoClaw) | [NVIDIA NemoClaw Official Documentation](https://docs.nvidia.com/nemoclaw/latest/about/overview.html) | [NemoClaw CLI Reference](https://docs.nvidia.com/nemoclaw/latest/cli/reference.html)

---

## 1. System Architecture & Failure Domains

NemoClaw is a distributed, multi-tenant, event-native platform designed to run stateful, low-latency workloads at enterprise scale. It operates on a strictly decoupled control-plane and data-plane model.

```
                             +-----------------------------------+
                             |           CONTROL PLANE           |
                             |  - Nemo-API Server (SPIFFE/SPIRE) |
                             |  - State Store (Nemo-KV / Raft)   |
                             |  - Scheduler & Controller Manager |
                             +-----------------+-----------------+
                                               |
                                               v (mTLS / gRPC)
                             +-----------------+-----------------+
                             |            DATA PLANE             |
                             |  - Nemolet (Worker Node Agent)    |
                             |  - RocksDB State Store (LSM)      |
                             |  - Nemo-Proxy (Network Mesh)      |
                             +-----------------------------------+
```

### 1.1 Control Plane Components

- **Nemo-API Server:** Central entry point for all administrative, operational, and automated commands. Handles authentication, authorization, admission control, and API routing.
- **State Store (Nemo-KV):** Highly available, distributed key-value store based on the Raft consensus algorithm. Maintains entire cluster state including configurations, secrets, and workload statuses.
- **Scheduler:** Evaluates resource requirements, node affinities, taints, and tolerations to assign pending workloads to the most appropriate worker nodes.
- **Controller Manager:** Runs background control loops that regulate cluster state, ensuring actual state matches desired state.

### 1.2 Data Plane Components

- **Nemolet:** Primary agent on each worker node. Registers with control plane, manages task lifecycle, reports node health and resource utilization.
- **Execution Engine:** Runtime environment (container runtime, WebAssembly engine, or VM hypervisor) for isolating and executing tasks.
- **Network Proxy (Nemo-Proxy):** Handles inter-node communication, service discovery, load balancing, and network policy enforcement.

### 1.3 Failure Domains & Risk Analysis

| Subsystem | Component | Core Failure Mode | Operational Mitigation |
| :--- | :--- | :--- | :--- |
| **Control Plane** | Nemo-KV (Raft) | Quorum loss due to network partition or disk exhaustion. | Deploy across odd-numbered AZs; aggressive WAL pruning. |
| **Control Plane** | Nemo-API Server | Rate-limiting degradation under high automation load. | Enable gRPC/HTTP backpressure; configure upstream Envoy LBs. |
| **Control Plane** | Scheduler | Deadlocks due to complex constraints or corrupted locks. | Restart scheduler (stateless); clear scheduling cache. |
| **Data Plane** | Nemolet | Node disconnection (Ghost Node status). | Enforce strict NTP sync; automated mTLS cert rotation. |
| **Data Plane** | RocksDB | Write stalls due to high compaction debt. | Increase background compaction threads; off-heap block caching. |
| **Data Plane** | Network | Overlay network failures (CNI issues). | Verify encapsulation ports; inspect routing tables. |

---

## 2. Configuration Schema: `nemoclaw.yaml` (Complete)

### 2.1 Core Configuration Files

| File | Purpose |
| :--- | :--- |
| `nemoclaw.yaml` | Primary global configuration (system-wide defaults, essential parameters). |
| `modules.yaml` | Module configurations and dependencies with fine-grained control. |
| `security.yaml` | Security settings including access controls and encryption mechanisms. |
| `network.yaml` | Network configurations (IP ranges, subnets, load balancer settings). |
| `scheduler.yaml` | Scheduling functionality (job priorities, resource allocation). |

### 2.2 Schema Definition Example

```yaml
type: object
properties:
  version:
    type: string
    description: "Specifies the version of the configuration schema."
  logging:
    type: object
    properties:
      level:
        type: string
        enum: ["DEBUG", "INFO", "WARN", "ERROR"]
        default: "INFO"
      format:
        type: string
        default: "json"
    required: ["level"]
  performance:
    type: object
    properties:
      maxThreads:
        type: integer
        default: 100
      timeout:
        type: integer
        default: 3000
    required: ["maxThreads"]
required: ["version", "logging"]
```

### 2.3 Advanced Configuration Patterns

**Modular Configurations:**
```yaml
modules:
  - name: "user_management"
    enabled: true
    config:
      maxUsers: 1000
      accessLevel: "admin"
```

**Environment Overlays:**
```yaml
overlays:
  - environment: "production"
    logging:
      level: "ERROR"
  - environment: "development"
    logging:
      level: "DEBUG"
```

**YAML Reference Patterns:**
```yaml
ref: &default_logging
  level: "INFO"
  format: "text"

logging:
  <<: *default_logging
  level: "DEBUG" # Override default
```

### 2.4 Telemetry Configuration

```yaml
telemetry:
  tracing:
    enabled: true
    provider: otlp
    endpoint: "http://otel-collector:4317"
    sampling_rate: 0.1 # Sample 10% of requests
```

---

## 3. Storage & Transactional Write Architecture

NemoClaw achieves high-throughput event processing through an LSM-tree backed storage engine (RocksDB) with an exactly-once transactional write protocol.

### 3.1 LSM-Tree Compaction and Memory Settings

NemoClaw partitions state across specialized RocksDB column families:

- **Memtable Configuration:** Set `write_buffer_size` to `128MB - 512MB` per column family, with a maximum of `3 - 6` buffers to absorb high-throughput write bursts.
- **Compaction Style:** Utilize leveled compaction (L0 to L6) with dynamic level sizing to keep write amplification under strict bounds.
- **Block Cache:** Allocate `25% - 50%` of node memory to an off-heap block cache. Pin hot index and bloom filter blocks in memory.

**RocksDB Custom Resource for Optimized Compaction:**
```yaml
apiVersion: nemoclaw.io/v1
kind: RocksDBConfig
metadata:
  name: optimized-compaction
spec:
  maxBackgroundJobs: 8
  writeBufferSize: 268435456 # 256MB
  maxWriteBufferNumber: 6
  level0FileNumCompactionTrigger: 4
  delayedWriteRate: 104857600 # 100MB/s rate limiter
```

### 3.2 Exactly-Once Transactional Write Protocol

Two-phase commit protocol for exactly-once processing:

```
[Phase 1: Consume & Prepare] --> Reads event offset; writes state mutations to local RocksDB WAL.
                                 Reserves idempotent sequence numbers for downstream topics.
                                       |
                                       v
[Phase 2: Atomic Commit]     --> Flushes state mutations; appends output events with committed offset.
                                 On restart, uncommitted transactions are rolled back or re-evaluated.
```

---

## 4. Stream Processing & Workflow Orchestration

### 4.1 Time Semantics and Watermarking

Watermarks are derived dynamically from event timestamps. Late events outside the `allowedLateness` window are routed to Dead Letter Queues or processed using decremental aggregation logic.

$$\text{Watermark}_{\text{operator}} = \min(W_k) - \text{allowedLateness}$$

### 4.2 Workflow Engine: Sagas & TCC

- **Saga Pattern:** Each forward activity has a corresponding compensation activity. On failure, the engine executes compensations in reverse order.
- **TCC (Try-Confirm/Cancel) Pattern:** Reserves resources in "Try" phase, commits in "Confirm" phase, or releases in "Cancel" phase if any participant fails.

---

## 5. Multi-Region Replication & Edge Architecture

### 5.1 Active-Active Replication

NemoClaw supports active-active multi-region deployments using log-shipping and CRDTs.

- **Hybrid Logical Clocks (HLC):** Preserves causal ordering across regions without perfectly synchronized physical clocks. $HLC = (ts, counter, nodeID)$
- **CRDT Merge Semantics:** For set-like structures, uses Observed-Removed Sets (OR-Set); for scalar values, Last-Write-Wins Registers (LWW-Register) keyed by HLC.

---

## 6. Health Checks & Monitoring

### 6.1 Probe Endpoints

| Endpoint | Type | Behavior on Failure |
| :--- | :--- | :--- |
| `/healthz` | Liveness | Triggers automatic restart of the component. |
| `/readyz` | Readiness | Removes component from active load balancing pool. |
| `/startupz` | Startup | Disables liveness/readiness checks until success. |

### 6.2 Key Prometheus Metrics

| Metric | Alert Threshold | Indicates |
| :--- | :--- | :--- |
| `nemoclaw_api_request_duration_seconds` | >500ms reads, >2s writes | Control plane overload or Nemo-KV degradation. |
| `nemoclaw_scheduler_queue_length` | Continuously growing | Insufficient worker capacity or stalled scheduler. |
| `nemoclaw_worker_memory_usage_bytes` | >85% of limit | Imminent OOM event. |
| `nemoclaw_kv_consensus_latency_ms` | >50ms | Network issues, disk latency, or CPU starvation. |
| `nemoclaw_network_transmit_errors_total` | Increasing rate | Dropped packets or network interface saturation. |

### 6.3 Synthetic Transactions

Implement canary workloads that periodically submit lightweight end-to-end tasks to catch issues that isolated component metrics might miss (DNS failures, subtle network policies blocking traffic).

---

## 7. CLI Reference (Key Administrative Commands)

```bash
# === CLUSTER STATUS & NODE MANAGEMENT ===
nemocli get pods -A                                         # List all pods across namespaces
nemocli describe node worker-01                             # Check resource utilization & conditions
nemocli top pods -n production --sort-by=memory             # Sort pods by memory consumption
nemocli get nodes -o wide                                   # Wide output with IPs and kernel versions
nemocli cluster status --component kv                       # Check Nemo-KV cluster status

# === NODE MAINTENANCE ===
nemocli node drain <node-name> --ignore-daemonsets --force  # Drain node for maintenance
nemocli node cordon <node-name>                             # Prevent new scheduling
nemocli node uncordon <node-name>                           # Resume scheduling

# === TASK MANAGEMENT ===
nemocli task debug <task-id> --image=nicolaka/netshoot --target=main-container  # Inject debug container
nemocli task evict <task-id>                                # Evict offending task
nemocli task delete <task-id> --force --grace-period=0      # Force delete stuck task
nemocli get tasks -n <namespace> -l app=<label>             # Filter tasks by label

# === LOGGING & DEBUGGING ===
nemocli admin log-level set --component scheduler --level debug  # Dynamic log level adjustment
nemocli admin log-level set --component scheduler --level info   # Revert to normal
nemocli port-forward svc/nemo-api -n nemoclaw-system 6060:6060   # Port forward for profiling

# === STATE STORE (NEMO-KV) OPERATIONS ===
nemocli exec -it nemo-kv-0 -n nemo-system -- nemocli-raft member list    # List Raft members
nemocli exec -it nemo-kv-0 -n nemo-system -- nemocli-raft member remove <dead-node-id>  # Remove dead node
nemocli exec -it nemo-kv-0 -n nemo-system -- nemocli-raft bootstrap --force  # Force bootstrap

# === DISASTER RECOVERY ===
nemocli kv restore --snapshot-path /backups/nemokv-latest.snap --data-dir /var/lib/nemokv  # Restore from snapshot
nemocli admin inspect cluster --output-dir /tmp/nemo-diag   # Gather diagnostic bundle
nemocli admin cache clear --component scheduler             # Clear scheduling cache

# === CERTIFICATE MANAGEMENT ===
nemocli certs renew --node <node-name>                      # Rotate node certificates

# === CONFIGURATION VALIDATION ===
nemoclaw-validate config/schema/nemoclaw.yaml               # Validate config against schema
nemocli apply -f rocksdb-config.yaml                        # Apply RocksDB configuration
```

---

## 8. Security Audit Checklist

### 8.1 Identity & Access Management

- [ ] MFA enforced for all administrative accounts accessing the Control Plane.
- [ ] SSO integration via SAML 2.0 or OIDC with JIT provisioning.
- [ ] API keys rotated every 30-60 days; stored in secrets manager.
- [ ] Session timeouts configured (15 min inactivity); secure cookie attributes set.
- [ ] Principle of Least Privilege applied to all roles and service accounts.
- [ ] Periodic access reviews (quarterly minimum).

### 8.2 Network Security

- [ ] VPC/Subnet isolation between Control Plane and Data Plane.
- [ ] Only necessary ports open (443 HTTPS, Message Broker ports).
- [ ] Zero Trust Architecture validated (all requests authenticated regardless of origin).
- [ ] WAF deployed in front of Control Plane; DDoS mitigation active.
- [ ] TLS 1.2+ (preferably 1.3) for all internal and external communications.
- [ ] mTLS enforced for service-to-service communication.

### 8.3 Data Security

- [ ] All data at rest encrypted (AES-256).
- [ ] KMS integration with annual key rotation.
- [ ] Backups encrypted and stored with immutability (WORM).
- [ ] Secrets managed via external secrets manager (never plaintext).
- [ ] Dynamic, short-lived secrets for database access where possible.

### 8.4 Application Security

- [ ] SAST integrated into CI/CD pipeline.
- [ ] Regular DAST scans against Control Plane APIs.
- [ ] SCA monitoring for CVEs in open-source dependencies.
- [ ] Container images scanned before registry push.
- [ ] Critical patches applied within 48-hour SLA.

### 8.5 Hardening

- [ ] Containers run as non-root with read-only root filesystems.
- [ ] Unnecessary Linux capabilities dropped; seccomp profiles enforced.
- [ ] Host OS hardened per CIS Benchmarks.
- [ ] API rate limiting and throttling enforced.
- [ ] Plugin sandboxing with restricted network and filesystem access.

---

## 9. Error Codes Reference

### 9.1 Control Plane Errors (1xxx)

| Code | Name | Cause | Action |
| :--- | :--- | :--- | :--- |
| ERR-1001 | API_RATE_LIMIT_EXCEEDED | Too many requests. | Implement exponential backoff with jitter. |
| ERR-1002 | UNAUTHORIZED_ACCESS | Invalid/expired auth token. | Renew token; check IdP integration. |
| ERR-1003 | FORBIDDEN_ACTION | Insufficient RBAC permissions. | Update RoleBindings/ClusterRoleBindings. |
| ERR-1004 | STATE_STORE_UNAVAILABLE | API cannot reach Nemo-KV. | Check KV health, quorum, network. |
| ERR-1005 | RESOURCE_QUOTA_EXCEEDED | Namespace quota exhausted. | Increase quota or delete unused resources. |
| ERR-1006 | ADMISSION_WEBHOOK_DENIED | Webhook rejected request. | Check webhook service logs. |

### 9.2 Scheduling Errors (2xxx)

| Code | Name | Cause | Action |
| :--- | :--- | :--- | :--- |
| ERR-2001 | INSUFFICIENT_RESOURCES | No node has enough capacity. | Scale up cluster or reduce resource requests. |
| ERR-2002 | AFFINITY_CONFLICT | Affinity rules unsatisfiable. | Relax constraints; verify node labels. |
| ERR-2003 | TAINT_TOLERATION_MISMATCH | Task doesn't tolerate node taints. | Add tolerations or remove taints. |
| ERR-2004 | VOLUME_BINDING_FAILED | Storage topology constraints unmet. | Check storage class and volume availability. |

### 9.3 Execution Errors (3xxx)

| Code | Name | Cause | Action |
| :--- | :--- | :--- | :--- |
| ERR-3001 | IMAGE_PULL_BACKOFF | Cannot download container image. | Verify registry credentials, image path, network. |
| ERR-3002 | OOM_KILLED | Memory limit exceeded. | Increase limit or optimize memory usage. |
| ERR-3003 | EXECUTION_TIMEOUT | Task exceeded max_duration. | Optimize execution or increase timeout. |
| ERR-3004 | LOCAL_STORAGE_EXHAUSTED | Ephemeral storage full. | Clean /tmp or request more storage. |
| ERR-3005 | RUNTIME_SANDBOX_FAILURE | Container runtime failed to create sandbox. | Check runtime logs; reboot node if needed. |

### 9.4 Network Errors (4xxx)

| Code | Name | Cause | Action |
| :--- | :--- | :--- | :--- |
| ERR-4001 | SERVICE_DISCOVERY_FAILURE | DNS resolution failed. | Check CoreDNS logs; verify resolv.conf. |
| ERR-4002 | CONNECTION_REFUSED | Target service not accepting connections. | Verify service running and passing readiness probes. |
| ERR-4003 | NETWORK_POLICY_VIOLATION | Traffic blocked by network policy. | Review and update network policies. |
| ERR-4004 | PORT_ALLOCATION_CONFLICT | Host port already in use. | Use NodePorts or LoadBalancers instead. |

---

## References

- [1] [NemoClaw Troubleshooting and Diagnostics Guide](https://docs.nvidia.com/nemoclaw/latest/operations/troubleshooting.html)
- [2] [NVIDIA NemoClaw Official Documentation](https://docs.nvidia.com/nemoclaw/latest/about/overview.html)
- [3] [NVIDIA NemoClaw GitHub Repository](https://github.com/NVIDIA/NemoClaw)
- [4] [NemoClaw Security Audit Guide](https://docs.nvidia.com/nemoclaw/latest/security/audit.html)
