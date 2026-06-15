# NemoClaw Advanced Guide

> **Role:** NVIDIA NemoClaw Platform Specialist — Advanced Patterns
> **Domain:** Enterprise deployment, advanced security hardening, multi-sandbox orchestration, GPU inference optimization
> **Official Documentation:** [docs.nvidia.com/nemoclaw](https://docs.nvidia.com/nemoclaw/latest/) | [GitHub](https://github.com/NVIDIA/NemoClaw)

---

## 1. Advanced Blueprint Engineering

### 1.1 Blueprint Internals

The NemoClaw blueprint is a versioned Python artifact that encapsulates all orchestration logic for creating and configuring sandboxes. Understanding the blueprint internals is essential for advanced customization and troubleshooting [3].

The blueprint execution follows a deterministic pipeline. First, the plugin downloads the blueprint artifact from the configured registry. Second, the plugin verifies the artifact's SHA-256 digest against the expected value. Third, the plugin executes the blueprint as a Python subprocess, passing configuration parameters via environment variables and stdin. Fourth, the blueprint inspects the current state of OpenShell resources and determines which operations are needed (create, update, or skip). Fifth, the blueprint executes OpenShell CLI commands to apply the desired state [3].

### 1.2 Custom Blueprint Development

For organizations with specific security or compliance requirements, custom blueprints can be developed. A custom blueprint must implement the standard blueprint interface, which includes methods for sandbox creation, policy application, inference configuration, and state management. Custom blueprints are registered in the NemoClaw configuration and can be selected during onboarding [3].

### 1.3 Blueprint Versioning Strategy

Blueprint versions follow semantic versioning (MAJOR.MINOR.PATCH). Major version changes indicate breaking changes to the sandbox configuration format. Minor version changes add new features while maintaining backward compatibility. Patch version changes fix bugs without changing behavior. The blueprint version is locked at sandbox creation time, and upgrading to a new blueprint version requires explicit operator action [3].

### 1.4 Digest Verification Deep Dive

Every blueprint artifact includes a SHA-256 digest that is verified before execution. The verification process works as follows: the plugin computes the SHA-256 hash of the downloaded artifact, compares it against the expected digest stored in the NemoClaw configuration, and refuses to execute the blueprint if the digests do not match. This prevents supply chain attacks where a compromised registry could serve a malicious blueprint [3].

---

## 2. Advanced Security Hardening

### 2.1 Landlock Filesystem Policies

Landlock is a Linux security module that provides fine-grained filesystem access control without requiring root privileges. NemoClaw uses Landlock to restrict the sandbox's filesystem access to only the paths it needs [2].

The default Landlock policy allows read-write access to `/sandbox` (the agent's working directory) and `/tmp` (temporary files), read-only access to system libraries and binaries required for the agent to run, and blocks access to all other paths including `/etc`, `/home`, `/root`, and `/proc`.

For advanced use cases, the Landlock policy can be customized to grant additional read-only access (e.g., to a shared data directory) or to further restrict write access within the sandbox. Policy changes to filesystem rules are **locked at sandbox creation** and cannot be modified at runtime — this is by design to prevent privilege escalation [2] [3].

### 2.2 Seccomp Profiles

The seccomp profile defines which system calls the sandbox process is allowed to make. NemoClaw's default seccomp profile blocks system calls that could be used for privilege escalation (`setuid`, `setgid`, `mount`, `umount`), container escape (`unshare`, `clone` with new namespaces), kernel module loading (`init_module`, `finit_module`), raw network access (`socket` with `AF_PACKET`, `AF_NETLINK`), and debugging other processes (`ptrace`, `process_vm_readv`) [2].

Like filesystem policies, seccomp profiles are **locked at sandbox creation** and cannot be modified at runtime.

### 2.3 Capability Drops

Linux capabilities provide fine-grained control over privileged operations. NemoClaw drops all capabilities by default and only adds back the minimum set required for the agent to function. The dropped capabilities include `CAP_NET_RAW` (raw network access), `CAP_SYS_ADMIN` (broad system administration), `CAP_SYS_PTRACE` (debugging other processes), `CAP_DAC_OVERRIDE` (bypass file permissions), and `CAP_FOWNER` (bypass file ownership checks) [2].

### 2.4 MITRE ATLAS Threat Mitigation

NemoClaw's security model is designed to mitigate threats identified in the MITRE ATLAS framework for AI/ML systems [2]:

| MITRE ATLAS Technique | NemoClaw Mitigation |
|----------------------|---------------------|
| **Prompt Injection** | Content policies at gateway level, output filtering |
| **Model Manipulation** | Inference routing prevents direct model access |
| **Data Poisoning via Tools** | Tool allow/deny lists, sandboxed execution |
| **Session Hijacking** | Session isolation, authentication at gateway |
| **Credential Theft** | Credentials never enter sandbox, inference routing |
| **Privilege Escalation** | Seccomp, capability drops, Landlock |
| **Container Escape** | Namespace isolation, seccomp, capability drops |
| **Supply Chain Attack** | SHA-256 digest verification for all artifacts |

---

## 3. Multi-Sandbox Orchestration

### 3.1 Multiple Agent Deployment

For organizations running multiple AI agents with different roles, NemoClaw supports deploying multiple sandboxes on the same host. Each sandbox is independently configured with its own blueprint, policies, inference routing, and channel connections. Sandboxes are isolated from each other — they cannot communicate directly and share no state [2].

### 3.2 Resource Allocation

When running multiple sandboxes, resource allocation becomes critical. Each sandbox should be configured with explicit CPU and memory limits to prevent resource contention [2]:

| Deployment Pattern | CPU per Sandbox | RAM per Sandbox | Max Sandboxes (16 core / 64 GB) |
|-------------------|----------------|-----------------|--------------------------------|
| Lightweight (chat only) | 1 core | 2 GB | 16 |
| Standard (chat + tools) | 2 cores | 4 GB | 8 |
| Heavy (code execution) | 4 cores | 8 GB | 4 |

### 3.3 Shared Infrastructure

While sandboxes are isolated from each other, they can share infrastructure components such as the inference router (reducing the number of provider connections), the network policy engine (applying consistent policies across all sandboxes), and monitoring and logging infrastructure (centralizing observability) [2].

---

## 4. Remote GPU Deployment

### 4.1 Architecture for Remote GPU

For agents that require GPU-accelerated inference (e.g., running local models via Ollama or vLLM), NemoClaw supports a split deployment where the Gateway and sandbox run on a lightweight frontend instance while inference requests are routed to a remote GPU instance. This separation allows cost-effective scaling where GPU resources are only provisioned when needed [2].

### 4.2 DGX Spark Optimization

NemoClaw includes optimized configurations for NVIDIA DGX Spark workstations. The DGX Spark configuration enables direct GPU access from the sandbox for local inference, optimized Docker runtime settings for NVIDIA GPU passthrough, and pre-configured Ollama integration with recommended model configurations [1].

### 4.3 Cloud GPU Deployment

For cloud deployments, NemoClaw supports running on GPU-enabled cloud instances from AWS (p4d, p5), GCP (a2, a3), Azure (NC, ND series), and NVIDIA DGX Cloud. The deployment process involves provisioning a GPU instance, installing NemoClaw, configuring Ollama or vLLM for local inference, and running `nemoclaw onboard` with the local inference option [2].

---

## 5. Kubernetes Deployment

### 5.1 Kubernetes Architecture

For enterprise-scale deployments, NemoClaw can be deployed on Kubernetes clusters. The Kubernetes deployment includes a NemoClaw Operator that manages sandbox lifecycle, a Custom Resource Definition (CRD) for NemoClaw sandboxes, network policies that enforce the same isolation as the Docker deployment, and persistent volume claims for sandbox state [1].

### 5.2 Helm Chart Configuration

```yaml
# values.yaml
replicaCount: 1
image:
  repository: nvcr.io/nvidia/nemoclaw
  tag: latest
  pullPolicy: IfNotPresent

resources:
  limits:
    cpu: "4"
    memory: "8Gi"
  requests:
    cpu: "2"
    memory: "4Gi"

inference:
  provider: nvidia
  endpoint: "https://integrate.api.nvidia.com/v1"

security:
  networkPolicy:
    enabled: true
    egress:
      - host: "integrate.api.nvidia.com"
        port: 443
  seccomp:
    profile: runtime/default
  capabilities:
    drop: ["ALL"]

persistence:
  enabled: true
  size: 20Gi
  storageClass: gp3
```

### 5.3 Kubernetes Network Policies

In Kubernetes, NemoClaw's network isolation is enforced through Kubernetes NetworkPolicy resources:

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: nemoclaw-sandbox-egress
  namespace: nemoclaw
spec:
  podSelector:
    matchLabels:
      app: nemoclaw-sandbox
  policyTypes:
    - Egress
  egress:
    - to:
        - ipBlock:
            cidr: 0.0.0.0/0
      ports:
        - protocol: TCP
          port: 443
```

---

## 6. Monitoring and Observability

### 6.1 Health Checks

NemoClaw exposes health check endpoints that can be used by orchestrators (Docker, Kubernetes) to monitor sandbox health. The health check verifies that the OpenClaw agent is running, the OpenShell gateway is responsive, all configured channels are connected, and the inference router is functioning [2].

### 6.2 Key Metrics

| Metric | Description | Warning Threshold | Critical Threshold |
|--------|-------------|-------------------|-------------------|
| Inference latency (p95) | Time to receive model responses | > 5s | > 15s |
| Error rate | Percentage of failed requests | > 1% | > 5% |
| Memory utilization | Sandbox memory usage | > 80% | > 95% |
| Disk utilization | Sandbox disk usage | > 70% | > 90% |
| Channel disconnections | Channel reconnection events | > 1/hour | > 5/hour |
| Network policy violations | Blocked connection attempts | > 10/hour | > 50/hour |
| Active sessions | Concurrent conversations | > 80% capacity | > 95% capacity |
| Tool execution duration | Time spent in tool calls | > 10s | > 30s |

### 6.3 Structured Logging

All NemoClaw components emit structured JSON logs that can be collected by Fluentd, Filebeat, or similar log aggregators and shipped to Elasticsearch, Loki, or CloudWatch for centralized analysis. The `nemoclaw logs --follow` command streams real-time logs from all components [1].

---

## 7. State Management Advanced Patterns

### 7.1 Cross-Machine Migration

NemoClaw's state management system enables migrating a running agent from one machine to another. The migration process creates a state snapshot on the source machine, strips all credentials from the snapshot (API keys, tokens, certificates), verifies the snapshot integrity with SHA-256, transfers the snapshot to the target machine, restores the snapshot on the target machine, and re-injects credentials from the target machine's configuration [2] [3].

### 7.2 Disaster Recovery

For disaster recovery, NemoClaw supports automated snapshot scheduling. Snapshots can be created on a regular schedule (hourly, daily) and stored in durable storage (S3, NFS, GCS). In the event of a failure, the most recent snapshot can be restored on a new machine to resume operations with minimal data loss [2].

### 7.3 Blue-Green Deployment

NemoClaw supports blue-green deployment patterns where two sandboxes run simultaneously — the "blue" sandbox handles production traffic while the "green" sandbox is updated and tested. Once the green sandbox is verified, traffic is switched from blue to green, and the blue sandbox is decommissioned. This pattern enables zero-downtime upgrades [2].

---

## 8. Advanced Inference Patterns

### 8.1 Multi-Provider Failover

NemoClaw's inference router supports configuring multiple providers in a failover chain. If the primary provider is unavailable or returns errors, requests are automatically routed to the next provider in the chain. The failover configuration supports health checks, circuit breakers, and configurable retry policies [2].

### 8.2 Cost-Optimized Routing

For organizations managing inference costs, the routing layer can be configured to route requests based on cost. Simple queries can be directed to cheaper models (e.g., smaller local models via Ollama), while complex queries requiring higher capability are routed to more expensive cloud providers [2].

### 8.3 Privacy-Aware Routing

For organizations with data privacy requirements, the inference router can be configured to route requests containing sensitive data to local inference providers (Ollama, vLLM) while allowing non-sensitive requests to use cloud providers. This hybrid approach balances privacy requirements with the capability advantages of cloud-hosted models [2].

---

## 9. Integration with NVIDIA Ecosystem

NemoClaw integrates with the broader NVIDIA AI ecosystem [1] [2]:

| Component | Integration |
|-----------|-------------|
| **NeMo Framework** | Model training and fine-tuning for custom models |
| **NeMo Guardrails** | AI safety and content filtering at the inference level |
| **NVIDIA NIMs** | Optimized model serving with TensorRT-LLM |
| **NVIDIA AI Enterprise** | Commercial support and SLA guarantees |
| **DGX Spark** | Optimized local inference on NVIDIA workstations |
| **DGX Cloud** | Cloud-based GPU inference at scale |

---

## 10. Troubleshooting Guide

| Issue | Diagnosis | Resolution |
|-------|-----------|------------|
| Sandbox fails to start | Check `nemoclaw status` output | Verify Docker is running, check disk space, verify blueprint digest |
| Inference requests failing | Check inference router logs | Verify provider API keys, check network policy allows provider host |
| Channel not connecting | Check channel process logs | Verify bot token, check webhook URL, verify network policy |
| High memory usage | Check sandbox resource metrics | Configure session compaction, increase memory limit |
| Network policy blocking legitimate requests | Check TUI for blocked hosts | Approve host in TUI or add to network policy YAML |
| Blueprint verification failed | Check SHA-256 digest | Re-download blueprint, verify registry integrity |
| State migration failed | Check migration logs | Verify source and target NemoClaw versions match |
| Slow inference | Check provider latency metrics | Switch to closer provider region, enable local inference |

**Debug Mode:**

```bash
NEMOCLAW_DEBUG=1 nemoclaw onboard
```

Debug mode produces verbose logs including all OpenShell CLI commands executed, all network requests made by the blueprint, detailed timing information for each operation, and full error stack traces [1].

---

## 11. Production Deployment Checklist

| Item | Status | Notes |
|------|--------|-------|
| Hardware meets minimum requirements (4 vCPU, 8 GB RAM, 20 GB disk) | ☐ | Check with `nemoclaw status` |
| Node.js 22.16+ installed | ☐ | Use `node -v` to verify |
| Docker running and accessible | ☐ | Use `docker info` to verify |
| `nemoclaw onboard` completed successfully | ☐ | Creates sandbox with hardened defaults |
| Inference provider configured and tested | ☐ | Verify with test message |
| Network policy customized for production | ☐ | Pre-approve known-safe hosts |
| Channel connections verified | ☐ | Test each channel with a message |
| State snapshot created | ☐ | Initial backup for disaster recovery |
| Monitoring and alerting configured | ☐ | Set up health checks, metrics, alerts |
| Backup strategy documented | ☐ | Regular snapshots to durable storage |
| Disaster recovery tested | ☐ | Restore snapshot on separate machine |
| Security policies reviewed | ☐ | Verify Landlock, seccomp, capabilities |
| Blueprint digest verified | ☐ | Confirm SHA-256 matches expected value |
| Credential storage secured | ☐ | API keys in env vars, not in config files |
| MITRE ATLAS mitigations reviewed | ☐ | Address all identified threat vectors |

---

## References

[1]: [NVIDIA NemoClaw GitHub Repository](https://github.com/NVIDIA/NemoClaw)
[2]: [NVIDIA NemoClaw Official Documentation - Overview](https://docs.nvidia.com/nemoclaw/latest/about/overview.html)
[3]: [NVIDIA NemoClaw - How It Works](https://docs.nvidia.com/nemoclaw/latest/about/how-it-works.html)
