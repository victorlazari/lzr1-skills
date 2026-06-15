# OpenClaw (ZeroClaw) Agent Gateway Runtime — Complete Reference

> **Official Sources:** [OpenClaw Architecture & Core Engine](https://github.com/openclaw/openclaw) | [OpenClaw Specialist Documentation](https://docs.openclaw.dev/about/overview.html) | [OpenClaw CLI Reference](https://docs.openclaw.dev/cli/reference.html)

---

## 1. Architectural Blueprint & Gateway Sequence

OpenClaw is a highly extensible, open-source AI agent runtime designed for production-grade multi-agent orchestration. It supports high-throughput, multi-channel AI interactions while maintaining persistent state and context across long-running sessions. The system operates under a strict directory structure and configuration hierarchy.

### 1.1 Directory Structure & File Mapping

A standard OpenClaw production deployment utilizes the following file layout:

```
/opt/openclaw/
├── config/
│   └── openclaw.json           # Main system configuration (central nervous system)
├── workspace/                  # Dynamic workspace files (agent cognition layer)
│   ├── SOUL.md                 # Ethical boundaries & immutable core directives
│   ├── IDENTITY.md             # Persona, role, tone, and domain expertise
│   ├── USER.md                 # User profile, preferences & channel identity mappings
│   ├── AGENTS.md               # Swarm topology, worker clearances & trust matrix
│   ├── BOOT.md                 # Startup sequence commands & initialization scripts
│   ├── HEARTBEAT.md            # System health, cron tracking & recurring tasks
│   ├── MEMORY.md               # Scratchpad for active sessions & persistent notes
│   └── TOOLS.md                # Registered tools, JSON schemas & execution policies
├── sessions/
│   ├── wa/                     # Persistent WhatsApp (Baileys) cryptographic state
│   ├── signal/                 # Signal protocol session data
│   └── *.jsonl                 # Raw conversation transcripts (JSON Lines format)
├── extensions/                 # Custom TypeScript plugins
│   └── crm-sync/              # Example local extension
├── skills/                     # ClawdHub marketplace skills
└── data/
    └── vector.db               # SQLite memory database (sqlite-vss + Gemini embeddings)
```

### 1.2 The Gateway Startup Sequence (8 Phases)

```
[Phase 1: Config Parsing]  --> Validates /opt/openclaw/config/openclaw.json schema.
                                     |
                                     v
[Phase 2: Workspace Load]  --> Reads SOUL.md, IDENTITY.md, USER.md, etc., into RAM.
                                     |
                                     v
[Phase 3: Memory Boot]     --> Opens SQLite vector DB; tests Gemini embeddings API connectivity.
                                     |
                                     v
[Phase 4: Plugins/Skills]  --> Compiles TypeScript extensions; registers ClawdHub skills.
                                     |
                                     v
[Phase 5: Swarm Init]      --> Places Codex, Claude Code, and Pi workers in standby.
                                     |
                                     v
[Phase 6: Channel Binding] --> Opens WebSockets (Baileys) & binds RPC ports (signal-cli).
                                     |
                                     v
[Phase 7: BOOT.md Exec]    --> Executes custom startup scripts defined in BOOT.md.
                                     |
                                     v
[Phase 8: Ready State]     --> Starts accepting channel events; logs "Gateway Ready".
```

---

## 2. Configuration Schema: `openclaw.json` (Complete)

The central nervous system of any OpenClaw deployment. It defines providers, active channels, memory parameters, plugin mappings, and orchestration rules.

```json
{
  "$schema": "https://schema.openclaw.dev/v1/openclaw.schema.json",
  "version": "1.4.2",
  "instance_id": "prod-cluster-alpha-01",
  "llm_providers": {
    "primary": {
      "provider": "anthropic",
      "model": "claude-3-5-sonnet-20241022",
      "api_key": "${ANTHROPIC_API_KEY}",
      "max_tokens": 8192,
      "temperature": 0.7
    },
    "fallback": {
      "provider": "openai",
      "model": "gpt-4o",
      "api_key": "${OPENAI_API_KEY}",
      "max_tokens": 4096,
      "temperature": 0.5
    }
  },
  "channels": {
    "whatsapp": {
      "enabled": true,
      "engine": "baileys",
      "session_dir": "./sessions/wa",
      "reconnect_interval_ms": 5000,
      "max_retries": 10,
      "options": {
        "connectTimeoutMs": 60000,
        "keepAliveIntervalMs": 15000,
        "retryRequestDelayMs": 5000,
        "markOnlineOnConnect": true
      }
    },
    "signal": {
      "enabled": true,
      "engine": "signal-cli",
      "daemon_port": 8080,
      "phone_number": "+1234567890",
      "options": {
        "rpcHost": "127.0.0.1",
        "rpcPort": 7583,
        "maxConcurrentRpcCalls": 5,
        "rpcTimeoutMs": 30000,
        "queueMaxCapacity": 1000
      }
    },
    "telegram": {
      "enabled": true,
      "engine": "polling",
      "bot_token": "${TELEGRAM_BOT_TOKEN}",
      "poll_interval_ms": 1000,
      "options": {
        "pollingTimeoutSeconds": 50,
        "httpClientTimeoutMs": 60000,
        "limit": 100,
        "allowedUpdates": ["message", "callback_query"]
      }
    }
  },
  "memory": {
    "vector_db": {
      "engine": "sqlite",
      "path": "./data/vector.db",
      "embeddings": {
        "provider": "google",
        "model": "models/embedding-001"
      },
      "options": {
        "journalMode": "WAL",
        "synchronous": "NORMAL",
        "busyTimeoutMs": 10000,
        "maxConnections": 20
      }
    },
    "context_window_size": 128000
  },
  "plugins": [
    {
      "name": "clawdhub-weather",
      "version": "^2.1.0",
      "source": "marketplace"
    },
    {
      "name": "custom-crm-sync",
      "path": "./extensions/crm-sync",
      "source": "local"
    }
  ],
  "extensions": {
    "clawdhub-salesforce-integration": {
      "enabled": true
    }
  },
  "orchestration": {
    "background_workers": ["codex", "claude-code", "pi"],
    "max_concurrent_tasks": 50,
    "lanes": {
      "heavy_research": {
        "minWorkers": 2,
        "maxWorkers": 10,
        "scaleUpThresholdQueueDepth": 50,
        "scaleDownThresholdQueueDepth": 10
      }
    },
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

---

## 3. The 3-Layer Memory Architecture

OpenClaw coordinates memory across three distinct physical layers to balance immediate token efficiency with long-term semantic recall.

```
+---------------------------------------------------------------------------------+
|                         LAYER 1: CONTEXT WINDOW (RAM)                           |
| - Volatile, sliding-window conversation buffer.                                 |
| - Holds raw chat history, active system prompts, and immediate tool results.    |
| - Managed dynamically via token pruning algorithms.                             |
+----------------------------------------------------+----------------------------+
                                                     |
                                                     v
+----------------------------------------------------+----------------------------+
|                        LAYER 2: WORKSPACE FILES (DISK)                          |
| - Mid-term, structured Markdown database (SOUL.md, IDENTITY.md, USER.md, etc.).|
| - Explicitly read/written by the agent to persist key facts across sessions.    |
| - Mounted on persistent volumes in containerized clusters.                      |
+----------------------------------------------------+----------------------------+
                                                     |
                                                     v
+----------------------------------------------------+----------------------------+
|                     LAYER 3: VECTOR DATABASE (SQLITE-VSS)                       |
| - Long-term semantic recall store.                                              |
| - Uses Gemini models/embedding-001 for high-dimensional semantic search.        |
| - Stores conversation fragments and external knowledge bases.                   |
| - Configured with WAL mode for concurrent access safety.                        |
+---------------------------------------------------------------------------------+
```

### 3.1 Session Compaction Protocol

To prevent context window overflow, OpenClaw background threads execute a compaction loop:

1. **Threshold Trigger:** Triggered when active session tokens exceed `context_window_size` * 0.8.
2. **Asynchronous Summarization:** A background worker summarizes conversation segments older than N messages.
3. **Memory Append:** The summary is appended to `MEMORY.md` and embedded into the SQLite vector DB.
4. **Context Flush:** Raw older messages are pruned from Layer 1, and the summary is injected as a baseline context.

### 3.2 Memory Security Considerations

- **Vector DB Protection:** The SQLite database file must have strict filesystem permissions (0600). OpenClaw uses parameterized queries exclusively to prevent SQL injection.
- **Session Storage:** JSONL session files contain raw conversation transcripts and must be encrypted at rest. A strict data retention policy must automatically purge sessions older than a specified threshold.
- **Embedding Security:** Sensitive PII must be redacted before being sent to the Gemini embedding model to prevent accidental leakage to the LLM provider.

---

## 4. Multi-Agent Swarm Orchestration

OpenClaw coordinates specialized, asynchronous background workers via a central message broker and a lane-based routing system.

| Worker Agent | Core Capability | Security Clearance | Primary Use Case |
| :--- | :--- | :--- | :--- |
| **Codex** | Code generation, compilation, local sandbox script execution. | Restricted (no PII access, sandboxed filesystem). | Automating data analysis, writing scripts, running terminal utilities. |
| **Claude Code** | Deep repository analysis, structural refactoring, design patterns. | Intermediate (read-only code directory access). | Explaining codebase architectures, refactoring code, generating pull requests. |
| **Pi** | Empathetic conversational interaction, copywriting, human-in-the-loop chat. | Unrestricted (PII authorized). | Customer engagement, drafting delicate communications, user onboarding. |

### 4.1 Orchestration Flow

1. **Decompose:** The primary agent receives a complex user request and splits it into independent sub-tasks.
2. **Delegate:** It writes task definitions to a temporary workspace file and invokes the `delegate_task` tool, targeting a specific worker (e.g., `codex`).
3. **Isolate:** The worker boots in an isolated thread/sandbox, processes the task, and writes the output back to the workspace.
4. **Synthesize:** The primary agent reads the result, validates it against `SOUL.md` guidelines, and delivers the finalized response to the user.

### 4.2 Lane System & Congestion Management

OpenClaw uses a "lane" system for multi-agent orchestration. Lanes are dedicated message queues for different task types (e.g., a "fast lane" for simple chat, a "heavy lane" for deep research using Claude Code).

- **Dynamic Worker Scaling:** Configure OpenClaw to dynamically scale workers based on lane queue depth via Kubernetes HPA integration.
- **Task Timeouts & Preemption:** Enforce strict execution timeouts for all background workers to prevent "poison pill" tasks from blocking a lane indefinitely.
- **Provider Load Balancing:** Load balance requests across multiple API keys or providers within the same lane to avoid rate limit bottlenecks.

---

## 5. Channel Security Policies

OpenClaw supports four distinct channel policies:

| Policy | Description | Recommended Use |
| :--- | :--- | :--- |
| **Open** | Accepts incoming messages from any user. | Public-facing customer support bots (with rate limiting). |
| **Allowlist** | Only processes messages from explicitly approved identifiers. | Internal enterprise deployments. |
| **Pairing** | Requires cryptographic handshake or OTP exchange before session establishment. | High-security environments. |
| **Disabled** | Channel completely deactivated at runtime level. | Unused channels in production. |

### 5.1 Channel-Specific Security Checks

- **WhatsApp (Baileys):** Ensure session state is stored securely and encrypted at rest. Multi-device sync must not leak session keys to unauthorized nodes.
- **Signal (signal-cli):** Daemon must run with least privilege (not root). UNIX socket permissions must be strictly controlled.
- **Telegram (Polling):** Polling must use HTTPS exclusively. Bot token must never be hardcoded; inject via secure environment variables or secrets manager.

---

## 6. Workspace File Integrity & Security

### 6.1 Core Workspace Files

| File | Purpose | Security Risk if Compromised |
| :--- | :--- | :--- |
| `SOUL.md` | Ethical boundaries and immutable directives. | Attacker bypasses safety filters. |
| `IDENTITY.md` | Persona, tone, and background. | Agent impersonation or social engineering. |
| `USER.md` | User instructions and preferences. | Data manipulation or privilege escalation. |
| `AGENTS.md` | Multi-agent topology and trust matrix. | Unauthorized cross-context access. |
| `BOOT.md` | Initialization scripts and startup sequences. | Arbitrary code execution at startup. |
| `HEARTBEAT.md` | Recurring tasks and cron jobs. | Persistent backdoor via scheduled tasks. |
| `MEMORY.md` | Active session scratchpad. | Data exfiltration of session context. |
| `TOOLS.md` | Authorized extensions and skills. | Malicious tool execution. |

### 6.2 File Integrity Monitoring (FIM)

A FIM system must continuously hash workspace files and alert administrators immediately if unauthorized changes are detected. In high-security deployments, OpenClaw should refuse startup if cryptographic signatures of workspace files do not match expected values.

---

## 7. Extension & Skill Marketplace Security

### 7.1 Extension Sandboxing

Custom TypeScript extensions execute within the OpenClaw runtime. They must be sandboxed with strict limitations:
- No access to host filesystem outside designated temporary directories.
- No ability to spawn child processes.
- Network access restricted to explicitly approved domains.

### 7.2 ClawdHub Skill Verification

Skills from the ClawdHub marketplace must be treated as untrusted third-party code:
1. **Signature Verification:** Only install skills cryptographically signed by trusted developers.
2. **Static Analysis:** Run automated static analysis against skill source code before deployment.
3. **Dependency Auditing:** Check `package.json` for vulnerable dependencies using `npm audit`.

---

## 8. CLI Reference (Key Administrative Commands)

```bash
# === SERVICE MANAGEMENT ===
sudo systemctl start openclaw                    # Start the OpenClaw service
sudo systemctl stop openclaw                     # Gracefully stop the service
sudo systemctl restart openclaw                  # Restart the service
sudo systemctl status openclaw                   # Check service status

# === LOG ANALYSIS ===
tail -f /var/log/openclaw/runtime.log            # Stream main runtime logs
jq -r 'select(.level == "error") | .message' /var/log/openclaw/sessions/*.jsonl  # Find all errors
jq -r 'select(.event_type == "tool_call") | .tool_name' sessions/*.jsonl | sort | uniq -c  # Count tool calls

# === MEMORY DIAGNOSTICS (SQLITE3) ===
sqlite3 /var/lib/openclaw/memory.sqlite "SELECT COUNT(*) FROM memory_fragments;"
sqlite3 /var/lib/openclaw/memory.sqlite "SELECT id, access_count, text FROM memory_fragments ORDER BY access_count DESC LIMIT 5;"
sqlite3 /var/lib/openclaw/memory.sqlite "PRAGMA journal_mode;"  # Verify WAL mode
sqlite3 /var/lib/openclaw/memory.sqlite "VACUUM;"               # Compact the database

# === SESSION MANAGEMENT ===
mv /opt/openclaw/sessions/wa /opt/openclaw/sessions/wa_backup   # Backup WhatsApp session
mkdir -p /opt/openclaw/sessions/wa                               # Create fresh session directory

# === PROCESS MANAGEMENT ===
ps aux | grep node                               # Check for orphaned node processes
ps aux | grep signal-cli                         # Check signal-cli daemon status
sudo netstat -tulpn | grep 8080                  # Verify signal-cli port binding
```

---

## 9. Incident Response Protocols

### 9.1 Scenario: `openclaw.json` Compromise

If the central configuration file is compromised, the attacker gains full control over the runtime.

**Response Protocol:**
1. **Immediate Isolation:** Disconnect the OpenClaw server from the network.
2. **Credential Revocation:** Revoke all 30+ LLM provider API keys and channel bot tokens simultaneously.
3. **Session Termination:** Force-close all active user sessions across all 14 channels.
4. **Forensic Analysis:** Image the server for forensic analysis.
5. **Rebuild and Restore:** Rebuild from known good state, generate new credentials, restore from secure backups.

### 9.2 Scenario: Malicious Skill Execution

**Response Protocol:**
1. **Skill Deactivation:** Immediately disable the offending skill via `openclaw.json` or `TOOLS.md`.
2. **Sandbox Review:** Analyze sandbox logs to determine extent of skill's activities.
3. **Memory Purge:** If skill interacted with vector database or session files, roll back to previous snapshot.
4. **Vulnerability Disclosure:** Report the malicious skill to ClawdHub maintainers.

---

## References

- [1] [OpenClaw Specialist Documentation - Overview](https://docs.openclaw.dev/about/overview.html)
- [2] [OpenClaw Architecture & Core Engine](https://github.com/openclaw/openclaw)
- [3] [OpenClaw CLI Reference](https://docs.openclaw.dev/cli/reference.html)
- [4] [OpenClaw Security Audit Procedures](https://docs.openclaw.dev/security/audit-procedures.html)
