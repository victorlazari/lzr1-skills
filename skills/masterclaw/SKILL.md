---
name: masterclaw
description: The definitive expert skill for OpenClaw, NemoClaw, and Enterprise Prompt Engineering. Use when analyzing, implementing, debugging, fixing, troubleshooting, or architecting multi-agent systems, distributed stream-processing platforms, or complex prompt/RAG architectures. Covers the full lifecycle from architecture design through production operations, incident response, and disaster recovery. Includes sub-agent spawning intelligence for complex multi-domain tasks.
---
# Skill: MasterClaw — Unified OpenClaw, NemoClaw & Prompt Engineering Runtime Specialist

> **Core Purpose:** This super skill consolidates the entire technical, operational, architectural, and research-backed knowledge of OpenClaw (ZeroClaw), NemoClaw, and Enterprise Prompt Engineering into a single autonomous cognitive framework. It diagnoses, fixes, implements, analyzes, and troubleshoots complex multi-agent, distributed stream processing, and LLM-orchestrated systems in production environments — backed by 400+ academic papers, engineering articles, and official documentation sources.

---

## 1. Skill Architecture & Cognitive Mapping

The **MasterClaw** skill is a hierarchical, multi-domain expert system integrating three systems into a unified cognitive loop:

```
                  +---------------------------------------+
                  |       Enterprise Prompt Layer         |
                  |  (CoT, ToT, GoT, ReAct, DSPy, OPRO) |
                  +-------------------+-------------------+
                                      |
                                      v
                  +-------------------+-------------------+
                  |        OpenClaw Agent Runtime         |
                  | (3-Layer Memory, Multi-Agent Swarms,  |
                  |  Channel Workers, Extension System)   |
                  +-------------------+-------------------+
                                      |
                                      v
                  +-------------------+-------------------+
                  |       NemoClaw Distributed Engine     |
                  | (LSM-Tree/RocksDB, Stream Processing, |
                  |  Raft Consensus, Active-Active CRDT)  |
                  +-------------------+-------------------+
```

### 1.1 Reference Architecture Map

| Reference File | Domain | Key Topics | Deep-Dive Sources |
| :--- | :--- | :--- | :--- |
| **`01-openclaw-runtime.md`** | OpenClaw Agent Gateway | 8-Phase Startup, 3-Layer Memory (Working/Episodic/Semantic), Channel Workers (WhatsApp/Signal/Telegram), Multi-Agent Swarm Orchestration, Extension Security, Session Compaction | `01-openclaw-specialist.md`, `01-openclaw-deep-dive.md`, `01-openclaw-advanced.md`, `01-openclaw-config-schemas.md`, `01-openclaw-cli-reference.md`, `01-openclaw-troubleshooting.md`, `01-openclaw-security-audit.md` |
| **`02-nemoclaw-platform.md`** | NemoClaw Distributed Engine | LSM-Tree Storage (RocksDB), Exactly-Once Transactional Write Protocol, Stream Processing, Workflow Engine (Sagas/TCC), Active-Active Replication (CRDTs + HLC), Raft Consensus, Error Codes, Security Audit | `02-nemoclaw-specialist.md`, `02-nemoclaw-deep-dive.md`, `02-nemoclaw-advanced.md`, `02-nemoclaw-config-schemas.md`, `02-nemoclaw-cli-reference.md`, `02-nemoclaw-troubleshooting.md`, `02-nemoclaw-security-audit.md` |
| **`03-prompt-architecture.md`** | Enterprise Prompt Engineering | Reasoning Frameworks (CoT, ToT, GoT, ReAct, Self-Consistency), Context Window Management, Automated Optimization (DSPy, OPRO), Prompt Caching, Security (Injection/Jailbreak), RAG Integration, CLI Tools | `03-prompt-specialist.md`, `03-prompt-deep-dive.md`, `03-prompt-advanced.md`, `03-prompt-config-schemas.md`, `03-prompt-cli-reference.md`, `03-prompt-troubleshooting.md`, `03-prompt-security-audit.md` |
| **`04-troubleshooting-playbooks.md`** | Unified Diagnostics & Recovery | WhatsApp 408 Timeouts, Signal RPC Failures, Telegram Polling, Cross-Context Blocks, Lane Congestion, Nemo-KV Quorum Loss, RocksDB Compaction Debt, DNS Failures, Volume Issues, Disaster Recovery, Security Audit Checklists | `01-openclaw-troubleshooting.md`, `02-nemoclaw-troubleshooting.md`, `03-prompt-troubleshooting.md`, all `*-security-audit.md` |
| **`05-research-foundations.md`** | Academic & Industry Research | 400+ sources: AI Agent Frameworks, Multi-Agent Memory, Distributed Consensus, Stream Processing, RocksDB/LSM, Prompt Engineering, RAG, LLM Security, Observability, SRE, Event-Driven Architectures | All research files in `references/research/` |

---

## 2. When to Use This Skill

Invoke MasterClaw when the task involves ANY of the following:

- **Fixing bugs or errors** in OpenClaw, NemoClaw, or prompt-based systems
- **Implementing new features** (new channels, agents, workflows, stream processors, prompt patterns)
- **Analyzing existing projects** (architecture review, performance audit, security assessment)
- **Troubleshooting production incidents** (connection failures, memory issues, performance degradation)
- **Configuring or tuning** system parameters (openclaw.json, nemoclaw.yaml, RocksDB, prompt configs)
- **Security hardening** (audit checklists, credential rotation, injection defense, zero-trust)
- **Disaster recovery** (quorum loss, data corruption, credential compromise, split-brain)
- **Performance optimization** (compaction tuning, caching strategies, lane scaling, context budgeting)
- **Multi-agent orchestration** (swarm topology, agent specialization, task decomposition)
- **Prompt engineering** (CoT/ToT/GoT/ReAct patterns, DSPy optimization, RAG architecture)
- **Observability & monitoring** (OpenTelemetry integration, distributed tracing, alerting)

---

## 3. Sub-Agent Spawning Intelligence

When a task spans multiple domains or requires parallel expertise, MasterClaw spawns specialized sub-agents:

| Trigger Condition | Sub-Agent Spawned | Capabilities |
| :--- | :--- | :--- |
| OpenClaw channel connection failures | **Channel Recovery Agent** | Baileys session reset, signal-cli daemon restart, Telegram polling diagnostics |
| NemoClaw cluster degradation | **Distributed Systems Agent** | Raft quorum recovery, RocksDB compaction tuning, node drain/cordon |
| Prompt quality issues (hallucinations, injection) | **Prompt Security Agent** | Input isolation, output sanitization, DSPy re-optimization, guardrails |
| Multi-agent orchestration failures | **Swarm Orchestrator Agent** | Lane rebalancing, worker clearance audit, cross-context routing |
| Performance degradation | **Performance Profiling Agent** | pprof analysis, flame graphs, eBPF tracing, memory leak detection |
| Security incident detected | **Security Incident Agent** | Credential rotation, mTLS verification, audit log analysis, SIEM correlation |
| Disaster recovery needed | **DR Recovery Agent** | Snapshot restore, quorum bootstrap, data integrity verification |
| Observability gaps | **Telemetry Agent** | OTLP pipeline configuration, trace correlation, metric alerting |

### 3.1 Spawning Protocol

```
1. DETECT: Identify task complexity and domain overlap
2. CLASSIFY: Map to one or more failure domains (see §4.2)
3. SPAWN: Initialize sub-agent(s) with scoped context from relevant reference files
4. COORDINATE: Sub-agents report findings back to MasterClaw orchestrator
5. SYNTHESIZE: Merge sub-agent outputs into unified resolution plan
6. EXECUTE: Apply changes atomically with rollback strategy
7. VERIFY: Run synthetic transactions and confirm stability
```

---

## 4. Core Workflows & Execution Procedures

### 4.1 Primary Workflow Loop: Analyze → Plan → Implement → Verify

```
+---------------------------------------------------------------------------------+
|                                1. ANALYZE                                       |
| - Parse error signatures or feature requirements.                               |
| - Inspect configurations (openclaw.json, nemoclaw.yaml, prompt_config.json).    |
| - Query active system state (nemocli, sqlite3, jq, journalctl).                 |
| - Match error patterns against known signatures in reference docs.              |
| - Correlate with OpenTelemetry traces and metrics.                              |
+----------------------------------------------------+----------------------------+
                                                     |
                                                     v
+----------------------------------------------------+----------------------------+
|                                  2. PLAN                                        |
| - Identify failure domains (Control Plane vs Data Plane vs LLM Provider).       |
| - Select appropriate remediation or implementation playbook.                    |
| - Perform dry-runs (--dry-run) and schema validation.                           |
| - Assess blast radius and rollback strategy.                                    |
| - Determine if sub-agent spawning is needed for parallel resolution.            |
+----------------------------------------------------+----------------------------+
                                                     |
                                                     v
+----------------------------------------------------+----------------------------+
|                                3. IMPLEMENT                                     |
| - Apply declarative configurations (nemocli apply -f, openclaw hot-reload).    |
| - Modify code/prompts using atomic file editing.                                |
| - Execute migration scripts or rotate certificates/keys.                        |
| - Follow principle of least change.                                             |
| - Use canary deployments for high-risk changes.                                 |
+----------------------------------------------------+----------------------------+
                                                     |
                                                     v
+----------------------------------------------------+----------------------------+
|                                 4. VERIFY                                       |
| - Run synthetic transactions, integration tests, and prompt evaluations.       |
| - Monitor system metrics (latency, error rates, memory usage, CPU).             |
| - Confirm stability and document the resolution in session logs.                |
| - Validate no regression in adjacent systems.                                   |
| - Update runbooks with new patterns discovered.                                 |
+---------------------------------------------------------------------------------+
```

### 4.2 Failure Domain Classification

| Domain | Key Indicators | Primary Tools | Sub-Agent |
| :--- | :--- | :--- | :--- |
| **OpenClaw Channel Layer** | Connection timeouts, QR code failures, RPC errors | `journalctl`, `tail -f runtime.log`, `netstat` | Channel Recovery |
| **OpenClaw Memory Layer** | Recall failures, embedding errors, SQLite locks | `sqlite3`, `jq` on JSONL files, vector similarity checks | Performance Profiling |
| **OpenClaw Orchestration** | Cross-context blocks, lane congestion, worker crashes | `AGENTS.md` audit, lane metrics, swarm topology | Swarm Orchestrator |
| **NemoClaw Control Plane** | API 503s, quorum loss, scheduling failures | `nemocli cluster status`, Raft member list | Distributed Systems |
| **NemoClaw Data Plane** | Write stalls, OOM kills, node disconnections | `nemocli top pods`, RocksDB logs, `iostat` | Performance Profiling |
| **NemoClaw Network** | DNS failures, connection refused, policy violations | `nemocli task debug`, `nslookup`, network policies | Distributed Systems |
| **Prompt Layer** | Hallucinations, injection attacks, timeout errors | Prompt config validation, output sanitization, DSPy | Prompt Security |
| **Observability** | Missing traces, metric gaps, alert fatigue | OTLP collector logs, sampling config, dashboard review | Telemetry |

---

## 5. Operational Command Cheat Sheet

### 5.1 NemoClaw Administrative Commands

```bash
# === CLUSTER STATUS ===
nemocli get pods -A                                         # All pods across namespaces
nemocli describe node worker-01                             # Node resource utilization
nemocli top pods -n production --sort-by=memory             # Sort by memory consumption
nemocli cluster status --component kv                       # Nemo-KV cluster health

# === NODE MANAGEMENT ===
nemocli node drain <node-name> --ignore-daemonsets --force  # Drain for maintenance
nemocli node cordon <node-name>                             # Prevent new scheduling
nemocli node uncordon <node-name>                           # Resume scheduling

# === TASK MANAGEMENT ===
nemocli task debug <task-id> --image=nicolaka/netshoot      # Inject debug container
nemocli task delete <task-id> --force --grace-period=0      # Force delete stuck task
nemocli task evict <task-id>                                # Evict offending task

# === LOGGING & DEBUGGING ===
nemocli admin log-level set --component scheduler --level debug
nemocli port-forward svc/nemo-api -n nemoclaw-system 6060:6060

# === STATE STORE (NEMO-KV) ===
nemocli exec -it nemo-kv-0 -n nemo-system -- nemocli-raft member list
nemocli exec -it nemo-kv-0 -n nemo-system -- nemocli-raft member remove <dead-node-id>
nemocli exec -it nemo-kv-0 -n nemo-system -- nemocli-raft bootstrap --force

# === DISASTER RECOVERY ===
nemocli kv restore --snapshot-path /backups/nemokv-latest.snap --data-dir /var/lib/nemokv
nemocli admin inspect cluster --output-dir /tmp/nemo-diag
```

### 5.2 OpenClaw Administrative Commands

```bash
# === SERVICE MANAGEMENT ===
sudo systemctl start openclaw
sudo systemctl stop openclaw
sudo systemctl restart openclaw
sudo systemctl status openclaw

# === LOG ANALYSIS ===
tail -f /var/log/openclaw/runtime.log
jq -r 'select(.level == "error") | .message' /var/log/openclaw/sessions/*.jsonl
jq -r 'select(.event_type == "tool_call") | .tool_name' sessions/*.jsonl | sort | uniq -c

# === MEMORY DIAGNOSTICS (SQLITE3) ===
sqlite3 /var/lib/openclaw/memory.sqlite "SELECT COUNT(*) FROM memory_fragments;"
sqlite3 /var/lib/openclaw/memory.sqlite "SELECT id, access_count, text FROM memory_fragments ORDER BY access_count DESC LIMIT 5;"
sqlite3 /var/lib/openclaw/memory.sqlite "PRAGMA journal_mode;"
sqlite3 /var/lib/openclaw/memory.sqlite "VACUUM;"

# === SESSION MANAGEMENT ===
mv /opt/openclaw/sessions/wa /opt/openclaw/sessions/wa_backup_$(date +%Y%m%d)
mkdir -p /opt/openclaw/sessions/wa

# === HEALTH CHECKS ===
curl -s http://localhost:3000/health | jq .
curl -s http://localhost:3000/metrics | grep openclaw_
```

### 5.3 Prompt CLI Commands

```bash
# === PROMPT MANAGEMENT ===
prompt init [--overwrite] [-d ~/my_prompts]
prompt run [-p user=admin] [-e ENV=production] [--dry-run] <script>
prompt list [-a] [-d ~/my_prompts]
prompt validate [--strict] [--format json] <script>
prompt convert [-f json] [-t yaml] [--backup] <source> <destination>
prompt config --set timeout=30
prompt config --get timeout
prompt config --list
```

---

## 6. Key Configuration Patterns

### 6.1 OpenClaw Channel Configuration (openclaw.json)

```json
{
  "channels": {
    "whatsapp": {
      "enabled": true,
      "engine": "baileys",
      "session_dir": "./sessions/wa",
      "reconnect_interval_ms": 5000,
      "max_retries": 10,
      "options": {
        "printQRInTerminal": true,
        "keepAliveIntervalMs": 30000,
        "retryRequestDelayMs": 500,
        "connectTimeoutMs": 60000
      }
    },
    "signal": {
      "enabled": true,
      "engine": "signal-cli",
      "rpc_port": 7583,
      "options": {
        "jvmHeap": "-Xmx1024M",
        "trustMode": "trust-new-identities"
      }
    },
    "telegram": {
      "enabled": true,
      "engine": "grammy",
      "options": {
        "pollingTimeoutSeconds": 30,
        "httpClientTimeoutMs": 35000,
        "allowedUpdates": ["message", "callback_query"]
      }
    }
  }
}
```

### 6.2 NemoClaw RocksDB Tuning (nemoclaw.yaml)

```yaml
storage:
  engine: rocksdb
  data_dir: /var/lib/nemoclaw/data
  wal_dir: /var/lib/nemoclaw/wal
  options:
    writeBufferSize: 268435456       # 256MB (optimize for write-heavy)
    maxWriteBufferNumber: 6          # More buffers before flush
    level0FileNumCompactionTrigger: 4
    delayedWriteRate: 104857600      # 100MB/s
    maxBackgroundJobs: 8             # Parallel compaction threads
    targetFileSizeBase: 67108864     # 64MB L1 files
    maxBytesForLevelBase: 536870912  # 512MB L1 total
    compressionType: lz4             # Fast compression for hot data
    bottomLevelCompression: zstd     # High ratio for cold data
    bloomFilterBitsPerKey: 10        # Optimal bloom filter
    blockSize: 16384                 # 16KB blocks
    blockCache: 2147483648           # 2GB block cache
    enablePipelinedWrite: true       # Pipeline WAL + memtable writes
```

### 6.3 NemoClaw Telemetry Configuration

```yaml
telemetry:
  tracing:
    enabled: true
    provider: otlp
    endpoint: "http://otel-collector:4317"
    sampling_rate: 0.1
    propagation: ["tracecontext", "baggage"]
  metrics:
    enabled: true
    provider: prometheus
    port: 9090
    path: /metrics
  logging:
    level: info
    format: json
    output: stdout
```

---

## 7. Critical Error Patterns & Quick Fixes

### 7.1 OpenClaw Error Quick Reference

| Error Pattern | Component | Root Cause | Quick Fix |
| :--- | :--- | :--- | :--- |
| `408 Request Timeout` | WhatsApp/Baileys | Session state corruption or network instability | Clear session dir; tune `keepAliveIntervalMs`; check NAT timeout |
| `ECONNREFUSED 127.0.0.1:7583` | Signal/signal-cli | JVM daemon crashed or port conflict | Restart daemon; increase JVM heap (`-Xmx1024M`); check port |
| `ETIMEDOUT` getUpdates | Telegram | HTTP client timeout < polling timeout | Ensure `httpClientTimeoutMs` > `pollingTimeoutSeconds` × 1000 + 5000 |
| `Cross-context messaging blocked` | Orchestration | Agent clearance mismatch in AGENTS.md | Audit `AGENTS.md`; add sanitization middleware; check trust matrix |
| `Lane congestion detected` | Orchestration | Worker pool exhaustion | Scale workers; implement task timeouts; check for deadlocks |
| `Embedded run timeout exceeded` | Sandbox | Tool execution exceeding limits | Increase timeout; optimize tool code; add circuit breaker |
| `Memory layer desynchronization` | Memory | WAL mode disabled or embedding API failure | Enable SQLite WAL mode; implement embedding fallbacks |
| `Unhandled exception in extension` | Extensions | Third-party code failure | Disable extension; isolate in worker thread; check permissions |

### 7.2 NemoClaw Error Quick Reference

| Error Code | Name | Root Cause | Quick Fix |
| :--- | :--- | :--- | :--- |
| ERR-1001 | API_RATE_LIMIT_EXCEEDED | Burst traffic exceeding quotas | Exponential backoff with jitter; increase rate limits |
| ERR-1004 | STATE_STORE_UNAVAILABLE | Nemo-KV quorum loss | Check Nemo-KV health; restore from snapshot if needed |
| ERR-2001 | INSUFFICIENT_RESOURCES | Cluster capacity exhausted | Scale up cluster; implement resource quotas |
| ERR-3001 | IMAGE_PULL_BACKOFF | Registry auth failure or image not found | Verify registry credentials and image path |
| ERR-3002 | OOM_KILLED | Memory limit exceeded | Increase memory limit; profile for leaks; tune GC |
| ERR-4001 | SERVICE_DISCOVERY_FAILURE | CoreDNS degradation | Check CoreDNS logs; verify resolv.conf; restart DNS pods |
| ERR-4003 | NETWORK_POLICY_VIOLATION | Firewall rules blocking traffic | Review and update network policies; check mTLS certs |

---

## 8. Security Hardening Summary

### 8.1 Critical Security Controls (Zero-Trust Model)

1. **Credential Management:** All API keys, tokens, and secrets injected via environment variables or secrets manager (HashiCorp Vault / AWS Secrets Manager). Never hardcode. Rotate every 90 days.
2. **mTLS Everywhere:** Enforce mutual TLS for all service-to-service communication using SPIFFE/SPIRE identity framework. Certificate rotation every 24 hours.
3. **Least Privilege:** Apply principle of least privilege to all roles, service accounts, and agent clearances. Use RBAC with deny-by-default.
4. **Input Isolation:** All user inputs to prompts isolated with unique delimiters (`<<<USER_INPUT_START>>>...<<<USER_INPUT_END>>>`) and treated as untrusted data.
5. **Output Sanitization:** Apply regex-based sanitization + LLM-based content filtering to all outputs before delivery.
6. **Audit Logging:** Forward all administrative actions and prompt executions to centralized SIEM. Immutable audit trail.
7. **File Integrity Monitoring:** Hash workspace files (SOUL.md, IDENTITY.md, AGENTS.md) and alert on unauthorized modifications.
8. **Extension Sandboxing:** Run third-party extensions in isolated V8 isolates with restricted permissions and resource limits.
9. **Supply Chain Security:** Sign all container images with Sigstore/cosign. Verify SBOM before deployment.
10. **Network Segmentation:** Enforce network policies isolating control plane, data plane, and agent workloads.

### 8.2 Prompt Security Framework (OWASP LLM Top 10 Aligned)

| Threat | Defense | Implementation |
| :--- | :--- | :--- |
| Prompt Injection (LLM01) | Input isolation + instruction hierarchy | Delimiter-based separation; system prompt immutability |
| Sensitive Data Disclosure (LLM06) | Output filtering + PII detection | Regex patterns + NER-based PII scrubbing |
| Insecure Plugin Design (LLM07) | Extension sandboxing + permission model | V8 isolates; capability-based access control |
| Excessive Agency (LLM08) | Tool approval workflows + human-in-the-loop | Clearance levels in AGENTS.md; confirmation gates |
| Model Denial of Service (LLM04) | Rate limiting + circuit breakers | Token budgets; exponential backoff; fallback providers |

---

## 9. Research Foundations & Academic Backing

This skill is backed by extensive research across 20 domains. Key references:

### 9.1 AI Agent Frameworks & Multi-Agent Systems
- Park et al. (2023) "Generative Agents: Interactive Simulacra of Human Behavior" — Stanford
- Yao et al. (2023) "ReAct: Synergizing Reasoning and Acting in Language Models" — Princeton/Google
- Wu et al. (2023) "AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation" — Microsoft
- Hong et al. (2024) "MetaGPT: Meta Programming for Multi-Agent Collaborative Framework" — DeepWisdom
- Anthropic (2025) "Building Effective Agents" — Workflow patterns for production agents

### 9.2 Distributed Systems & Consensus
- Ongaro & Ousterhout (2014) "In Search of an Understandable Consensus Algorithm (Raft)" — Stanford
- Shapiro et al. (2011) "Conflict-Free Replicated Data Types" — INRIA
- Kulkarni et al. (2020) "CockroachDB: The Resilient Geo-Distributed SQL Database" — CockroachDB Labs
- Dong et al. (2023) "RocksDB: Evolution of Development Priorities" — Meta

### 9.3 Prompt Engineering & LLM Optimization
- Wei et al. (2022) "Chain-of-Thought Prompting Elicits Reasoning in LLMs" — Google Brain
- Yao et al. (2023) "Tree of Thoughts: Deliberate Problem Solving with LLMs" — Princeton
- Khattab et al. (2024) "DSPy: Compiling Declarative Language Model Calls" — Stanford
- Yang et al. (2024) "OPRO: Large Language Models as Optimizers" — Google DeepMind

### 9.4 Security & Observability
- OWASP (2025) "Top 10 for Large Language Model Applications v2.0"
- Google (2024) "BeyondProd: A Cloud-Native Security Architecture"
- CNCF OpenTelemetry Project (2024-2026) — Collector, OTTL, Operator documentation
- Beyer et al. (2016-2024) "Site Reliability Engineering" series — Google

> **Full research bibliography:** See `references/05-research-foundations.md` for complete 400+ source listing.

---

## 10. Reference Documentation

For detailed architectural schemas, advanced configurations, complete error code tables, and step-by-step troubleshooting playbooks:

- **[01-openclaw-runtime.md](./references/01-openclaw-runtime.md)**: OpenClaw architecture, 3-layer memory, session compaction, channel worker configurations, extension security, CLI commands, incident response protocols.
- **[02-nemoclaw-platform.md](./references/02-nemoclaw-platform.md)**: NemoClaw distributed platform, LSM-tree tuning, stream execution, active-active replication, complete error codes, security audit checklist, CLI reference.
- **[03-prompt-architecture.md](./references/03-prompt-architecture.md)**: Enterprise prompt patterns, DSPy optimization, context budgeting, prompt caching, security hardening, CLI tools, configuration schemas.
- **[04-troubleshooting-playbooks.md](./references/04-troubleshooting-playbooks.md)**: Unified step-by-step recovery playbooks for all components, disaster recovery procedures, security audit checklists, advanced debugging techniques.
- **[05-research-foundations.md](./references/05-research-foundations.md)**: Complete academic and industry research bibliography (400+ sources) organized by domain.

---

## References

- [1] [OpenClaw Architecture & Core Engine](https://github.com/openclaw/openclaw)
- [2] [OpenClaw Specialist Documentation](https://docs.openclaw.dev/about/overview.html)
- [3] [NVIDIA NemoClaw GitHub Repository](https://github.com/NVIDIA/NemoClaw)
- [4] [NVIDIA NemoClaw Official Documentation](https://docs.nvidia.com/nemoclaw/latest/about/overview.html)
- [5] [OpenAI Prompt Engineering Guide](https://platform.openai.com/docs/guides/prompt-engineering)
- [6] [Anthropic Prompt Engineering Documentation](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering)
- [7] [Anthropic Building Effective Agents](https://www.anthropic.com/engineering/building-effective-agents)
- [8] [DSPy Framework Documentation](https://dspy-docs.vercel.app/)
- [9] [OWASP LLM Security Top 10](https://owasp.org/www-project-top-10-for-large-language-model-applications/)
- [10] [OpenTelemetry Collector Documentation](https://opentelemetry.io/docs/collector/)
- [11] [RocksDB Tuning Guide](https://github.com/facebook/rocksdb/wiki/RocksDB-Tuning-Guide)
- [12] [Raft Consensus Algorithm](https://raft.github.io/)
- [13] [CNCF Cloud Native Security Whitepaper](https://github.com/cncf/tag-security/blob/main/security-whitepaper/v2/cloud-native-security-whitepaper.md)
- [14] [Google SRE Books](https://sre.google/books/)
- [15] [Model Context Protocol (MCP)](https://modelcontextprotocol.io/)
- [16] [LangGraph Documentation](https://github.com/langchain-ai/langgraph)
- [17] [CrewAI Documentation](https://docs.crewai.com/)
- [18] [SPIFFE/SPIRE Identity Framework](https://spiffe.io/)
- [19] [Sigstore Container Signing](https://www.sigstore.dev/)
- [20] [HashiCorp Vault Secrets Management](https://www.vaultproject.io/)

---

## Adversarial Verification Panel

For each significant architecture finding, failure diagnosis, and remediation recommendation produced by the parallel sub-agents:

1. Spawn **3 independent Refuter Agents** per finding, each with:
   - The finding in full
   - Instruction: *"Assume this finding is wrong. Find the strongest argument against it."*
   - Default stance: `refuted=true` if evidence is insufficient or ambiguous
2. A finding is **confirmed** only if ≥2 refuters fail to refute it
3. A finding is **discarded** if ≥2 refuters succeed
4. When a confirmed finding had 1 successful refuter, include the dissenting argument in the output with a `CONTESTED` label

> This prevents plausible-but-wrong architecture findings, failure diagnoses, and remediation recommendations from reaching the final output. The 3-vote panel eliminates single-point hallucination without requiring unanimity.

## Cross-System Consistency Validator

After all parallel agents (Channel Recovery Agent, Distributed Systems Agent, Prompt Security Agent, Swarm Orchestrator Agent, Performance Profiling Agent, Security Incident Agent, DR Recovery Agent, Telemetry Agent) complete, but **before** synthesis:

Run one **Consistency Validator Agent** with all parallel outputs that:
- Flags any pair of recommendations that logically contradict each other
  *(example: the Performance Profiling Agent recommends increasing RocksDB write buffers while the Distributed Systems Agent recommends reducing memory allocation on the same node)*
- Notes where one agent's output is a prerequisite for another agent's recommendation
- Passes contradictions to the Synthesis Agent as `MUST_RESOLVE` items
- Passes missing prerequisites as `SEQUENCING_REQUIRED` items

## Synthesis Agent (Upgraded)

The synthesis step actively resolves rather than aggregates:

1. **`MUST_RESOLVE` contradictions**: Pick the better recommendation, annotate the reasoning, preserve the dissenting view as a footnote
2. **`SEQUENCING_REQUIRED` items**: Re-order the unified resolution plan so prerequisites appear before the steps that depend on them
3. **Confidence calibration**: Label each finding `HIGH` / `MEDIUM` / `LOW` confidence based on refuter panel outcomes
4. **Gap analysis**: Note any analysis dimension not covered by any of the parallel agents — these are blind spots, not confirmed negatives
