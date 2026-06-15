# Unified Diagnostics, Troubleshooting, & Security Playbooks — Complete Reference

> **Official Sources:** [OpenClaw Operations - Troubleshooting](https://docs.openclaw.dev/operations/troubleshooting.html) | [NemoClaw Troubleshooting Guide](https://docs.nvidia.com/nemoclaw/latest/operations/troubleshooting.html) | [OWASP LLM Security Top 10](https://owasp.org/www-project-top-10-for-large-language-model-applications/)

---

## 1. OpenClaw Operational Troubleshooting Playbooks

### 1.1 Playbook: WhatsApp 408 Request Timeout Disconnects

**Symptom:** The Baileys engine repeatedly logs `Error: 408 Request Timeout` or flaps between `connecting` and `close`. Messages fail to send.

**Log Signature:**
```json
{"level":"error","timestamp":"2026-05-20T14:32:10.123Z","module":"channel:whatsapp","message":"Connection closed with status code 408","details":{"reason":"Request Timeout","isReconnectable":true,"lastNode":"message_ack"}}
{"level":"warn","timestamp":"2026-05-20T14:32:10.125Z","module":"channel:whatsapp","message":"Initiating exponential backoff reconnection strategy. Attempt 1/5."}
```

**Root Causes:**
1. **Event Loop Starvation:** Node.js is single-threaded. Heavy synchronous operations (parsing massive JSONL files, local vector embeddings) block the event loop, preventing Baileys from sending heartbeat pings.
2. **Network Jitter and Buffer Bloat:** In containerized environments, aggressive traffic shaping causes micro-stalls in packet delivery.
3. **Cryptographic State Desynchronization:** Slow disk I/O when writing Baileys Signal protocol session keys causes the client to fall behind the server's expected state.

**Step-by-Step Remediation:**

```bash
# Step 1: Gracefully stop the OpenClaw service
sudo systemctl stop openclaw

# Step 2: Check for orphaned node processes and terminate them
ps aux | grep node
# If processes exist: sudo kill -9 <pid>

# Step 3: Backup and clear the Baileys session directory (forces clean handshake)
mv /opt/openclaw/sessions/wa /opt/openclaw/sessions/wa_backup_$(date +%Y%m%d)
mkdir -p /opt/openclaw/sessions/wa

# Step 4: Restart the OpenClaw service
sudo systemctl start openclaw

# Step 5: Tail the runtime log to retrieve the new QR code for authentication
tail -f /var/log/openclaw/runtime.log
```

**Configuration Fix (openclaw.json):**
```json
{
  "channels": {
    "whatsapp": {
      "enabled": true,
      "provider": "baileys",
      "options": {
        "connectTimeoutMs": 60000,
        "keepAliveIntervalMs": 15000,
        "retryRequestDelayMs": 5000,
        "maxRetries": 10,
        "markOnlineOnConnect": true
      }
    }
  }
}
```

**Long-Term Fixes:**
- Offload synchronous operations from the main event loop to worker threads.
- Configure in-memory state management with async flush for Baileys cryptographic state.
- Apply QoS rules to prioritize WebSocket traffic on ports 443 and 5222 in Kubernetes.

---

### 1.2 Playbook: Signal (signal-cli) RPC Failures

**Symptom:** OpenClaw logs show `SignalRPCException: Connection refused` or `Timeout waiting for signal-cli response`.

**Log Signatures:**
```json
{"level":"error","timestamp":"2026-05-20T15:01:22.441Z","module":"channel:signal","message":"RPC call failed: send_message","details":{"error":"Error: connect ECONNREFUSED 127.0.0.1:7583","code":"ECONNREFUSED"}}
```

```text
WARN  [Thread-4] org.whispersystems.signalservice.api.SignalServiceMessageSender - Failed to send message
java.io.IOException: SQLite database is locked
```

**Root Causes:**
1. **Daemon Crash or OOM:** signal-cli (Java) crashes under memory pressure maintaining thousands of secure sessions.
2. **SQLite Database Locks:** Burst of concurrent RPC requests locks the signal-cli SQLite database.
3. **Socket Exhaustion:** Rapid TCP socket open/close for JSON-RPC causes ephemeral port exhaustion.

**Step-by-Step Remediation:**

```bash
# Step 1: Verify if signal-cli is running
ps aux | grep signal-cli

# Step 2: Check bound ports (default: 7583 or 8080)
sudo netstat -tulpn | grep -E "7583|8080"

# Step 3: Check for database locks
ls -la ~/.local/share/signal-cli/data/
# If lock files exist: rm ~/.local/share/signal-cli/data/*.lock

# Step 4: Restart signal-cli with increased heap
sudo systemctl restart signal-cli

# Step 5: Verify RPC connectivity
curl -X POST -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"listIdentities","id":1}' \
  http://localhost:7583/
```

**JVM Tuning (systemd service or Docker entrypoint):**
```bash
exec java -Xmx1024M -Xms512M -jar /opt/signal-cli/lib/signal-cli.jar daemon --rpc --tcp 127.0.0.1:7583
```

**Configuration Fix (openclaw.json):**
```json
{
  "channels": {
    "signal": {
      "enabled": true,
      "provider": "signal-cli",
      "options": {
        "rpcHost": "127.0.0.1",
        "rpcPort": 7583,
        "maxConcurrentRpcCalls": 5,
        "rpcTimeoutMs": 30000,
        "queueMaxCapacity": 1000
      }
    }
  }
}
```

---

### 1.3 Playbook: Telegram Polling Timeouts & getUpdates Failures

**Symptom:** Complete halt in message ingestion with repeated timeout errors. Potential duplicate message processing.

**Log Signature:**
```json
{"level":"error","timestamp":"2026-05-20T16:15:44.002Z","module":"channel:telegram","message":"Polling error during getUpdates","details":{"error":"ETIMEDOUT","code":"EFATAL","retryIn": 5000}}
```

**Root Causes:**
1. **Network Partitioning:** Temporary network partition between OpenClaw host and Telegram API.
2. **Aggressive Timeout Configuration:** HTTP client timeout set lower than Telegram's `timeout` parameter.
3. **Rate Limiting (HTTP 429):** Polling too aggressively triggers Telegram IP ban.

**Configuration Fix (openclaw.json):**
```json
{
  "channels": {
    "telegram": {
      "enabled": true,
      "provider": "polling",
      "options": {
        "pollingTimeoutSeconds": 50,
        "httpClientTimeoutMs": 60000,
        "limit": 100,
        "allowedUpdates": ["message", "callback_query"]
      }
    }
  }
}
```

**Key Rule:** `httpClientTimeoutMs` (60s) MUST be greater than `pollingTimeoutSeconds` (50s) to allow for network transit time.

**Additional Fixes:**
- Implement robust offset management: only increment `update_id` after message is committed to memory layer.
- Implement strict exponential backoff for HTTP 429 responses using the `Retry-After` header.

---

### 1.4 Playbook: Cross-Context Messaging Blocks

**Symptom:** Agent logs `Error: Cross-context messaging denied` when delegating tasks across agents.

**Log Signature:**
```json
{"level":"error","timestamp":"2026-05-20T17:05:11.882Z","module":"orchestration:router","message":"Cross-context messaging blocked","details":{"sourceAgent":"pi_worker","targetAgent":"codex_worker","reason":"Policy Violation: Attempted to pass PII context to unrestricted code execution environment","contextId":"ctx_9948a-bf42"}}
```

**Root Causes:**
1. **Misconfigured `AGENTS.md` Policies:** Trust matrix too restrictive for legitimate collaboration.
2. **Data Classification Failures:** Benign data falsely flagged as PII.
3. **Implicit Context Bleed:** Agent invokes a tool requiring a different security context.

**Remediation:**

1. Audit `AGENTS.md` and define clear data sharing agreements:
```markdown
## Agent: Codex Worker
- **Role:** Code generation and execution.
- **Clearance:** Public data only. No PII.
- **Allowed Inbound Channels:** Claude Code (sanitized data only).

## Agent: Pi Worker
- **Role:** User interaction and data collection.
- **Clearance:** PII authorized.
- **Allowed Outbound Channels:** Codex Worker (requires explicit data sanitization filter).
```

2. Configure sanitization middleware in `openclaw.json`:
```json
{
  "orchestration": {
    "routing": {
      "rules": [
        {
          "from": "pi_worker",
          "to": "codex_worker",
          "action": "allow",
          "middleware": ["pii_redactor", "context_minimizer"]
        }
      ]
    }
  }
}
```

3. Refine data classification prompts in `IDENTITY.md` or `SOUL.md`.

---

### 1.5 Playbook: Lane Congestion & Multi-Agent Orchestration Issues

**Symptom:** Severe latency; agent appears unresponsive for minutes.

**Log Signature:**
```json
{"level":"warn","timestamp":"2026-05-20T18:22:01.115Z","module":"orchestration:lanes","message":"Lane congestion detected","details":{"lane":"heavy_research","queueDepth": 450, "averageWaitTimeMs": 120500, "activeWorkers": 2}}
```

**Root Causes:**
1. Insufficient worker allocation for the "heavy" lane.
2. Poison pill tasks monopolizing workers.
3. LLM provider rate limits causing exponential backoff.

**Configuration Fix:**
```json
{
  "orchestration": {
    "lanes": {
      "heavy_research": {
        "minWorkers": 2,
        "maxWorkers": 10,
        "scaleUpThresholdQueueDepth": 50,
        "scaleDownThresholdQueueDepth": 10
      }
    }
  }
}
```

**Additional Fixes:**
- Implement task timeouts and preemption for poison pill prevention.
- Configure provider load balancing across multiple API keys/providers.

---

### 1.6 Playbook: Embedded Run Timeouts

**Symptom:** Tool execution fails with timeout error.

**Log Signature:**
```json
{"level":"error","timestamp":"2026-05-20T19:10:33.401Z","module":"sandbox:executor","message":"Embedded run timeout exceeded","details":{"tool":"data_analyzer_script","executionTimeMs": 30005, "limitMs": 30000, "pid": 4492}}
```

**Fixes:**
1. Increase sandbox timeouts in `openclaw.json` or `TOOLS.md` (with caution).
2. Optimize tool design: instruct agent to write efficient code, use pagination, implement internal timeouts.
3. Convert to asynchronous tool execution: initiate background job, return job ID, poll for status.

---

### 1.7 Playbook: Memory Layer Corruption & Sync Issues

**Symptom:** Agent fails to recall recent conversations or contradicts workspace file instructions.

**Log Signatures:**
```json
{"level":"error","timestamp":"2026-05-20T20:05:12.991Z","module":"memory:vector_db","message":"Failed to generate Gemini embedding for session chunk","details":{"error":"API Error: 503 Service Unavailable","chunkId":"chk_883a-99b"}}
{"level":"fatal","timestamp":"2026-05-20T20:05:13.001Z","module":"memory:sync","message":"Memory layer desynchronization detected. SQLite state does not match JSONL session log."}
```

**Root Causes:**
1. Embedding API failures (Gemini down or rate-limiting).
2. Concurrent write conflicts to SQLite without proper locking.
3. Disk space exhaustion preventing write operations.

**Configuration Fix (SQLite WAL mode):**
```json
{
  "memory": {
    "vectorDb": {
      "provider": "sqlite",
      "options": {
        "journalMode": "WAL",
        "synchronous": "NORMAL",
        "busyTimeoutMs": 10000,
        "maxConnections": 20
      }
    }
  }
}
```

**Additional Fixes:**
- Implement embedding fallbacks (queue for later or use local HuggingFace model).
- Schedule automated compaction (`VACUUM`) and archiving of old JSONL files to cold storage.

---

### 1.8 Playbook: Extension & ClawdHub Skill Failures

**Symptom:** Unhandled exception in extension crashes the agent process.

**Log Signature:**
```json
{"level":"error","timestamp":"2026-05-20T21:30:44.221Z","module":"extension_manager","message":"Unhandled exception in extension: clawdhub-salesforce-integration","details":{"error":"TypeError: Cannot read properties of undefined (reading 'data')","stack":"..."}}
```

**Immediate Fix:**
```json
{
  "extensions": {
    "clawdhub-salesforce-integration": {
      "enabled": false
    }
  }
}
```

**Long-Term Fixes:**
- Run extensions in isolated worker threads or separate processes.
- Enforce strict dependency pinning for all custom extensions.
- Audit `package.json` and run through staging before production deployment.

---

## 2. NemoClaw Operational Troubleshooting Playbooks

### 2.1 Playbook: Worker Node Disconnection (Ghost Nodes)

**Symptom:** Node appears as `NotReady` or `Unknown` but underlying server is accessible via SSH.

**Diagnosis:**
```bash
# Check network connectivity to control plane
curl -k https://<api-server-ip>:6443/version

# Inspect nemolet logs
journalctl -u nemolet -f

# Check for clock skew
timedatectl status

# Verify TLS certificate validity
openssl x509 -in /etc/nemoclaw/pki/nemolet.crt -noout -dates
```

**Resolution:**
- Clock skew: `chronyc makestep` or `systemctl restart systemd-timesyncd`
- Expired certs: `nemocli certs renew --node <node-name>` and restart nemolet
- Network partition: Resolve underlying routing/firewall issue; node auto-rejoins

---

### 2.2 Playbook: Scheduler Deadlock (Pending Tasks Accumulation)

**Symptom:** Tasks remain in `Pending` state indefinitely despite available resources.

**Diagnosis:**
```bash
# Check scheduler logs for constraint errors
nemocli logs -n nemoclaw-system -l component=scheduler --tail=100

# Verify node resources vs task requests
nemocli describe node <node-name> | grep -A 10 "Allocatable"

# Inspect for corrupted scheduling locks
nemocli admin cache clear --component scheduler
```

**Resolution:**
- Impossible constraints: Update task definition to request fewer resources or relax affinity rules.
- Corrupted lock: Restart scheduler (stateless; rebuilds from state store).
- Clear cache: `nemocli admin cache clear --component scheduler`

---

### 2.3 Playbook: Nemo-KV Quorum Loss

**Symptom:** Cluster becomes read-only or completely unresponsive. API returns 503.

**Diagnosis:**
```bash
# Check Nemo-KV cluster status
nemocli cluster status --component kv

# Identify offline control plane nodes
nemocli get pods -n nemo-system -l app=nemo-kv

# Inspect Raft membership
nemocli exec -it nemo-kv-0 -n nemo-system -- nemocli-raft member list

# Check disk space on KV nodes
df -h /var/lib/nemokv
```

**Resolution:**
- Temporary node outage: Wait for auto-recovery.
- Disk full: Expand volume or clear old snapshots/WAL.
- Permanent quorum loss: Execute disaster recovery from backup (see Section 3).

---

### 2.4 Playbook: RocksDB Compaction Stalls (Write Stalls)

**Symptom:** Stream processor throughput drops to zero; logs show `RocksDB: write stall` or `Too many L0 files`.

**Diagnosis:**
```bash
# Check compaction logs
nemocli exec -it stream-job-pod-xyz -- cat /var/log/nemoclaw/rocksdb.log | grep -i "compaction"

# Check L0 file count
nemocli exec -it stream-job-pod-xyz -- cat /var/log/nemoclaw/rocksdb.log | grep "L0"
```

**Configuration Fix:**
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

```bash
nemocli apply -f rocksdb-config.yaml
```

---

### 2.5 Playbook: High Disk I/O on Worker Nodes

**Symptom:** Task execution slows; node load average spikes; SSH becomes sluggish.

**Diagnosis:**
```bash
iostat -x 1        # Monitor disk utilization and await times
iotop              # Identify specific process causing high I/O
```

**Resolution:**
- Enforce strict ephemeral storage quotas via LimitRanges/ResourceQuotas.
- Evict offending tasks: `nemocli task evict <task-id>`
- Upgrade to NVMe SSDs for high-IOPS workloads.
- Separate disks for container runtime overlay and application data volumes.

---

### 2.6 Playbook: Volume Attachment Failures

**Symptom:** Task stuck in `ContainerCreating` with `Multi-Attach error for volume`.

**Diagnosis:**
```bash
nemocli get volumeattachments
```

**Resolution:**
- Wait for cloud provider API to complete detachment.
- If permanently stuck: manually detach via cloud console, then delete stuck VolumeAttachment object.

---

### 2.7 Playbook: Filesystem Corruption

**Symptom:** Application crashes with input/output errors (EIO) when reading/writing to volume.

**Diagnosis:**
```bash
dmesg -T | grep -i ext4  # or xfs
```

**Resolution:**
- Scale task to 0; mount volume to debug node.
- Run filesystem check: `fsck.ext4 -y /dev/sdX`
- If unrecoverable: restore from volume snapshot or application-level backup.

---

### 2.8 Playbook: DNS Resolution Failures

**Symptom:** Tasks cannot resolve internal service names.

**Diagnosis:**
```bash
# Check CoreDNS pods
nemocli get tasks -n kube-system -l k8s-app=kube-dns

# Test resolution from within cluster
nemocli task debug <task-id> --image=nicolaka/netshoot
nslookup my-service.default.svc.cluster.local

# Verify resolv.conf
cat /etc/resolv.conf
```

---

### 2.9 Playbook: Network Policy Violations

**Symptom:** Services cannot communicate despite being healthy.

**Diagnosis:**
```bash
# List network policies
nemocli get networkpolicies -n <namespace>

# Review ingress/egress rules
nemocli describe networkpolicy <policy-name> -n <namespace>

# Use nemo-net-trace to simulate traffic
nemo-net-trace --from <source-pod> --to <dest-pod> --port 8080
```

---

## 3. Disaster Recovery Procedures

### 3.1 NemoClaw: Control Plane Disaster Recovery (Restore from Backup)

**When:** Nemo-KV loses quorum permanently (multiple simultaneous disk failures).

**Procedure:**
```bash
# 1. Stop all API servers and Controller Managers
nemocli admin stop --component api-server,controller-manager

# 2. Stop Nemo-KV on all control plane nodes
sudo systemctl stop nemo-kv

# 3. Wipe corrupted data directories
sudo rm -rf /var/lib/nemokv/member

# 4. Initialize new cluster from snapshot (on single node)
nemocli kv restore --snapshot-path /backups/nemokv-latest.snap --data-dir /var/lib/nemokv

# 5. Start Nemo-KV on first node
sudo systemctl start nemo-kv

# 6. Join remaining control plane nodes one by one
nemocli kv member add --peer-urls=https://<node-ip>:2380

# 7. Restart API servers and Controller Managers
nemocli admin start --component api-server,controller-manager

# 8. Verify cluster state
nemocli cluster status
```

**Warning:** Tasks created after the snapshot was taken will be lost and must be resubmitted.

### 3.2 OpenClaw: `openclaw.json` Compromise Response

**Procedure:**
1. **Immediate Isolation:** Disconnect server from network.
2. **Credential Revocation:** Revoke all 30+ LLM provider API keys and channel bot tokens simultaneously.
3. **Session Termination:** Force-close all active user sessions across all 14 channels.
4. **Forensic Analysis:** Image the server for forensic analysis.
5. **Rebuild and Restore:** Rebuild from known good state, generate new credentials, restore from secure backups.

### 3.3 OpenClaw: Malicious Skill Execution Response

**Procedure:**
1. **Skill Deactivation:** Disable via `openclaw.json` or `TOOLS.md`.
2. **Sandbox Review:** Analyze sandbox logs for network connections and filesystem access attempts.
3. **Memory Purge:** Roll back vector database and session files to previous snapshot.
4. **Vulnerability Disclosure:** Report to ClawdHub maintainers.

---

## 4. Unified Security Audit & Hardening Playbooks

### 4.1 OpenClaw Security Audit Checklist

- [ ] Channel policies configured (Open/Allowlist/Pairing/Disabled) per channel.
- [ ] WhatsApp Baileys session state encrypted at rest.
- [ ] Signal-cli daemon running as non-root with restricted socket permissions.
- [ ] Telegram bot token injected via secrets manager (never hardcoded).
- [ ] Cross-context messaging isolation tested and verified.
- [ ] Credential directory permissions: directory=0700, files=0600.
- [ ] Encryption at rest for credential directory (KMS/HSM integration).
- [ ] File Integrity Monitoring (FIM) on all workspace files.
- [ ] JSONL session files encrypted at rest with data retention policy.
- [ ] PII redaction before Gemini embedding API calls.
- [ ] Extension sandboxing verified (no filesystem/process/network escape).
- [ ] ClawdHub skills verified (signature, static analysis, dependency audit).
- [ ] Multi-agent worker authentication (mTLS or JWT).
- [ ] Orchestration audit logs forwarded to SIEM.
- [ ] Incident response protocols documented and tested.

### 4.2 NemoClaw Security Audit Checklist

- [ ] MFA enforced for all administrative accounts.
- [ ] SSO integration via SAML 2.0 or OIDC validated.
- [ ] API keys rotated every 30-60 days; stored in secrets manager.
- [ ] Session timeouts configured (15 min inactivity).
- [ ] Principle of Least Privilege applied to all roles.
- [ ] VPC/Subnet isolation between Control and Data Planes.
- [ ] Zero Trust Architecture validated.
- [ ] TLS 1.2+ (preferably 1.3) for all communications.
- [ ] mTLS enforced for service-to-service communication.
- [ ] All data at rest encrypted (AES-256) with KMS.
- [ ] Backups encrypted with immutability (WORM).
- [ ] SAST/DAST/SCA integrated into CI/CD pipeline.
- [ ] Container images scanned before registry push.
- [ ] Containers run as non-root with read-only root filesystems.
- [ ] API rate limiting and throttling enforced.
- [ ] Comprehensive audit logging to centralized SIEM.
- [ ] Anomaly detection rules configured and tuned.
- [ ] Incident Response plan documented with tabletop exercises.

### 4.3 Prompt Security Hardening Checklist

- [ ] All user inputs isolated with unique delimiters.
- [ ] LLM-Guard gateway deployed for PII/injection scanning.
- [ ] Output sanitization regex filters active (API keys, secrets).
- [ ] System prompt never revealed in responses.
- [ ] RAG sources validated against injection attacks.
- [ ] Rate limiting on prompt API endpoints.
- [ ] Audit trails for all prompt executions.
- [ ] Compliance with GDPR/CCPA for processed data.

---

## 5. Advanced Debugging Techniques

### 5.1 Distributed Tracing (NemoClaw)

Use OpenTelemetry trace IDs from API response headers (`X-Nemoclaw-Trace-Id`) to follow request lifecycle across components.

### 5.2 Profiling (pprof)

```bash
# Port forward to debug port
nemocli port-forward svc/nemo-api -n nemoclaw-system 6060:6060

# Capture 30-second CPU profile
go tool pprof http://localhost:6060/debug/pprof/profile?seconds=30

# Capture heap profile
go tool pprof http://localhost:6060/debug/pprof/heap
```

### 5.3 Ephemeral Debug Containers

```bash
nemocli task debug <task-id> --image=nicolaka/netshoot --target=main-container
# Available tools: tcpdump, strace, curl, dig, nslookup
```

### 5.4 Dynamic Log Levels

```bash
nemocli admin log-level set --component scheduler --level debug
# Available: fatal, error, warn, info, debug, trace
# WARNING: debug/trace generate massive data; revert to info when done
```

### 5.5 Diagnostic Bundle Collection

```bash
nemocli admin inspect cluster --output-dir /tmp/nemo-diag
tar -czvf nemoclaw-diagnostics.tar.gz /tmp/nemo-diag
```

Bundle includes: component logs (last 10K lines), cluster state export (excluding Secrets), node health summaries, recent event history, anonymized configurations.

---

## 6. NemoClaw Error Codes Quick Reference

| Code | Name | Category | Action |
| :--- | :--- | :--- | :--- |
| ERR-1001 | API_RATE_LIMIT_EXCEEDED | Control Plane | Exponential backoff with jitter. |
| ERR-1002 | UNAUTHORIZED_ACCESS | Control Plane | Renew token; check IdP. |
| ERR-1003 | FORBIDDEN_ACTION | Control Plane | Update RBAC RoleBindings. |
| ERR-1004 | STATE_STORE_UNAVAILABLE | Control Plane | Check Nemo-KV health/quorum. |
| ERR-1005 | RESOURCE_QUOTA_EXCEEDED | Control Plane | Increase quota or free resources. |
| ERR-1006 | ADMISSION_WEBHOOK_DENIED | Control Plane | Check webhook service logs. |
| ERR-2001 | INSUFFICIENT_RESOURCES | Scheduling | Scale up or reduce requests. |
| ERR-2002 | AFFINITY_CONFLICT | Scheduling | Relax constraints; check labels. |
| ERR-2003 | TAINT_TOLERATION_MISMATCH | Scheduling | Add tolerations or remove taints. |
| ERR-2004 | VOLUME_BINDING_FAILED | Scheduling | Check storage class/availability. |
| ERR-3001 | IMAGE_PULL_BACKOFF | Execution | Verify registry creds/image path. |
| ERR-3002 | OOM_KILLED | Execution | Increase memory limit or optimize. |
| ERR-3003 | EXECUTION_TIMEOUT | Execution | Optimize or increase timeout. |
| ERR-3004 | LOCAL_STORAGE_EXHAUSTED | Execution | Clean /tmp or request more storage. |
| ERR-3005 | RUNTIME_SANDBOX_FAILURE | Execution | Check runtime logs; reboot node. |
| ERR-4001 | SERVICE_DISCOVERY_FAILURE | Network | Check CoreDNS; verify resolv.conf. |
| ERR-4002 | CONNECTION_REFUSED | Network | Verify target service health. |
| ERR-4003 | NETWORK_POLICY_VIOLATION | Network | Review/update network policies. |
| ERR-4004 | PORT_ALLOCATION_CONFLICT | Network | Use NodePorts/LoadBalancers. |

---

## 7. OpenClaw Error Signatures Quick Reference

| Error / Log Pattern | Component | Root Cause | Immediate Action |
| :--- | :--- | :--- | :--- |
| `Connection closed with status code 408` | WhatsApp/Baileys | Event loop starvation or network jitter. | Clear session; tune timeouts. |
| `ECONNREFUSED 127.0.0.1:7583` | Signal/signal-cli | Daemon crashed or OOM. | Restart daemon; increase JVM heap. |
| `ETIMEDOUT` during getUpdates | Telegram/Polling | Network partition or aggressive timeout. | Sync timeout parameters. |
| `Cross-context messaging blocked` | Orchestration | Policy violation in AGENTS.md. | Audit trust matrix; add middleware. |
| `Lane congestion detected` | Orchestration | Insufficient workers or poison pill task. | Scale workers; implement timeouts. |
| `Embedded run timeout exceeded` | Sandbox | Inefficient code or resource starvation. | Increase timeout; optimize code. |
| `Memory layer desynchronization` | Memory | Embedding API failure or SQLite corruption. | Enable WAL mode; implement fallbacks. |
| `Unhandled exception in extension` | Extensions | API changes or dependency conflicts. | Disable extension; isolate in worker. |

---

## References

- [1] [OpenClaw Operations - Troubleshooting](https://docs.openclaw.dev/operations/troubleshooting.html)
- [2] [NemoClaw Troubleshooting Guide](https://docs.nvidia.com/nemoclaw/latest/operations/troubleshooting.html)
- [3] [OpenClaw Security Audit Procedures](https://docs.openclaw.dev/security/audit-procedures.html)
- [4] [NemoClaw Security Audit Guide](https://docs.nvidia.com/nemoclaw/latest/security/audit.html)
- [5] [OWASP LLM Security Top 10](https://owasp.org/www-project-top-10-for-large-language-model-applications/)
