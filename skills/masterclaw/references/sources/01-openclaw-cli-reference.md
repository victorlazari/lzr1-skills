# OpenClaw (ZeroClaw) CLI Reference and Operations Guide

## 1. Introduction to OpenClaw

OpenClaw, also widely known in the community as ZeroClaw, is a premier open-source AI agent runtime designed for high-performance, multi-channel, and multi-agent orchestration. Built for scale and resilience, OpenClaw supports over 30 Large Language Model (LLM) providers and integrates seamlessly with 14 distinct messaging channels. This comprehensive CLI reference and operations guide is tailored for system administrators, DevOps engineers, and technical support specialists who manage OpenClaw deployments in production environments.

The architecture of OpenClaw is fundamentally designed around a robust workspace model, a sophisticated 3-layer memory system, and a highly extensible plugin ecosystem. Whether you are debugging a complex multi-agent orchestration issue, recovering from a channel timeout, or simply performing routine maintenance, this guide provides the essential commands, scripts, and operational knowledge required to keep your OpenClaw instances running smoothly.

This document serves as the primary operational manual and is intrinsically linked to the other specialist files in the repository. While this file focuses on CLI operations, troubleshooting, and system administration, it relies on the architectural definitions provided in the core system documentation. The configuration structures discussed here directly impact the agent behaviors defined in the persona files, and the memory management techniques are essential for maintaining the state described in the memory architecture documents. Understanding this file is a prerequisite for effectively utilizing the advanced orchestration and extension development guides.

## 2. Core Architecture and Configuration

### 2.1 The `openclaw.json` Configuration File

The heart of any OpenClaw deployment is the `openclaw.json` configuration file. This file dictates the runtime behavior, channel bindings, LLM provider settings, and memory management parameters. It is crucial to maintain strict version control over this file, as even minor misconfigurations can lead to cascading failures across the agent network.

```json
{
  "runtime": {
    "name": "ZeroClaw-Prod-01",
    "version": "2.4.1",
    "log_level": "debug",
    "max_concurrent_tasks": 50,
    "worker_timeout_ms": 120000
  },
  "providers": {
    "primary": "openai",
    "fallback": "anthropic",
    "embeddings": "gemini",
    "retry_strategy": {
      "max_attempts": 3,
      "backoff_multiplier": 1.5
    }
  },
  "channels": {
    "whatsapp": {
      "enabled": true,
      "engine": "baileys",
      "timeout_ms": 30000,
      "session_dir": "/var/lib/openclaw/whatsapp_sessions"
    },
    "signal": {
      "enabled": true,
      "engine": "signal-cli",
      "rpc_port": 8080,
      "daemon_path": "/usr/local/bin/signal-cli"
    },
    "telegram": {
      "enabled": true,
      "engine": "polling",
      "poll_interval_ms": 1000,
      "webhook_url": null
    }
  },
  "memory": {
    "vector_db_path": "/var/lib/openclaw/memory.sqlite",
    "context_window_limit": 16000,
    "consolidation_interval_minutes": 60
  }
}
```

### 2.2 Workspace Files Structure

OpenClaw relies on a structured set of Markdown files within its workspace to define the agent's persona, operational boundaries, and state. These files are dynamically read and updated by the runtime.

| File Name | Purpose and Content Description |
| :--- | :--- |
| `SOUL.md` | Defines the core ethical boundaries, immutable directives, and fundamental purpose of the agent. This file is read-only during runtime and requires a full restart to apply changes. |
| `IDENTITY.md` | Contains the persona, tone of voice, background story, and stylistic guidelines for the agent's responses. It dictates how the agent presents itself across different channels. |
| `USER.md` | Stores persistent user preferences, historical context summaries, and relationship dynamics. This file is frequently updated as the agent learns more about its users. |
| `AGENTS.md` | Maps the topology of the multi-agent network, detailing the roles, capabilities, and communication protocols of background workers. |
| `BOOT.md` | Initialization scripts, startup sequences, and pre-flight checks executed when the runtime boots. Useful for setting up environment variables or verifying external API connectivity. |
| `HEARTBEAT.md` | A dynamic file updated periodically to reflect the current health, load, and operational status of the agent. Often monitored by external health-check systems. |
| `MEMORY.md` | A scratchpad for short-term memory consolidation before it is committed to the vector database. It acts as a buffer to reduce database write frequency. |
| `TOOLS.md` | Declarations of available tools, API endpoints, and execution permissions for the agent. It defines what actions the agent can take in the external world. |

## 3. The 3-Layer Memory System

OpenClaw employs a sophisticated 3-layer memory architecture to balance immediate context awareness with long-term recall and persistent state management.

### 3.1 Layer 1: Context Window

The immediate context window is the fastest but most volatile memory layer. It contains the recent conversational turns, immediate tool execution results, and the active system prompt derived from the workspace files. Managing the context window size is critical to prevent token limit exhaustion and maintain optimal response latency. When the context window approaches its limit, OpenClaw automatically triggers a summarization routine, moving older context into Layer 2 or Layer 3.

### 3.2 Layer 2: Workspace Files

As detailed in Section 2.2, the workspace files serve as the intermediate memory layer. They provide a persistent, human-readable state that survives runtime restarts. The agent actively reads from and writes to these files to maintain its identity and operational context over time. This layer is particularly useful for storing structured data that needs to be frequently accessed but doesn't fit well in a relational database.

### 3.3 Layer 3: Vector Database (SQLite + Gemini Embeddings)

For long-term, semantic recall, OpenClaw utilizes a local SQLite database coupled with Gemini embeddings. This layer allows the agent to retrieve relevant historical interactions, learned facts, and past tool executions based on semantic similarity rather than exact keyword matches. The use of SQLite ensures low overhead and easy portability, while Gemini embeddings provide state-of-the-art semantic understanding.

#### SQLite Operations and One-Liners

Operating the vector database directly is often necessary for debugging, manual data curation, or performance tuning. Below are essential `sqlite3` one-liners for managing the OpenClaw memory database (`memory.sqlite`).

**Check Database Integrity:**
```bash
sqlite3 /var/lib/openclaw/memory.sqlite "PRAGMA integrity_check;"
```

**List All Tables and Schema:**
```bash
sqlite3 /var/lib/openclaw/memory.sqlite ".tables"
sqlite3 /var/lib/openclaw/memory.sqlite ".schema memory_fragments"
```

**Count Total Memory Fragments:**
```bash
sqlite3 /var/lib/openclaw/memory.sqlite "SELECT COUNT(*) FROM memory_fragments;"
```

**Search for Specific Keywords in Memory Text:**
```bash
sqlite3 /var/lib/openclaw/memory.sqlite "SELECT id, timestamp, text FROM memory_fragments WHERE text LIKE '%error 408%' ORDER BY timestamp DESC LIMIT 10;"
```

**Delete Old Memory Fragments (Older than 30 days) to Free Space:**
```bash
sqlite3 /var/lib/openclaw/memory.sqlite "DELETE FROM memory_fragments WHERE timestamp < datetime('now', '-30 days');"
sqlite3 /var/lib/openclaw/memory.sqlite "VACUUM;"
```

**Export Memory Fragments to CSV for External Analysis:**
```bash
sqlite3 -header -csv /var/lib/openclaw/memory.sqlite "SELECT * FROM memory_fragments;" > /tmp/memory_export.csv
```

**Identify the Most Frequently Accessed Memories:**
```bash
sqlite3 /var/lib/openclaw/memory.sqlite "SELECT id, access_count, text FROM memory_fragments ORDER BY access_count DESC LIMIT 5;"
```

## 4. Session Management and JSONL Logs

OpenClaw stores active and historical sessions as JSON Lines (JSONL) files. This format is highly efficient for appending new events and allows for robust stream processing. Each line in a session file represents a discrete event, such as a user message, an agent response, a tool invocation, or a system error. The session files are typically stored in `/var/log/openclaw/sessions/`.

### 4.1 Parsing Sessions with `jq`

The `jq` command-line JSON processor is an indispensable tool for analyzing OpenClaw session logs. Below are advanced `jq` one-liners for extracting actionable intelligence from your session files.

**Extract All User Messages from a Specific Session:**
```bash
jq -r 'select(.role == "user") | "[\(.timestamp)] \(.content)"' /var/log/openclaw/sessions/session_12345.jsonl
```

**Count the Number of Tool Invocations by Tool Name:**
```bash
jq -r 'select(.event_type == "tool_call") | .tool_name' /var/log/openclaw/sessions/*.jsonl | sort | uniq -c | sort -nr
```

**Find All Errors and Extract the Error Message and Stack Trace:**
```bash
jq -r 'select(.level == "error") | "[\(.timestamp)] \(.error_code): \(.message)
\(.stack_trace // "No stack trace")
---"' /var/log/openclaw/sessions/*.jsonl
```

**Calculate Average Response Time (Assuming `latency_ms` field exists):**
```bash
jq '[select(.role == "agent" and .latency_ms != null) | .latency_ms] | if length > 0 then add / length else 0 end' /var/log/openclaw/sessions/session_12345.jsonl
```

**Filter Events by a Specific Time Range and Event Type:**
```bash
jq -c 'select(.timestamp >= "2023-10-27T10:00:00Z" and .timestamp <= "2023-10-27T12:00:00Z" and .event_type == "message")' /var/log/openclaw/sessions/session_12345.jsonl
```

**Extract the Full Conversation History as Plain Text:**
```bash
jq -r 'select(.role == "user" or .role == "agent") | "\(.role | ascii_upcase): \(.content)"' /var/log/openclaw/sessions/session_12345.jsonl
```

## 5. Extensions and Skills Ecosystem

OpenClaw's functionality is heavily augmented by its extension and skills ecosystem, allowing it to adapt to a wide variety of use cases without modifying the core runtime.

### 5.1 Extensions (Custom TypeScript Plugins)

Extensions are custom TypeScript plugins that run directly within the OpenClaw Node.js runtime. They are typically used for deep integrations, custom channel implementations, or complex data processing tasks that require low-latency execution. Extensions must be compiled and placed in the `extensions/` directory.

**Managing Extensions:**
*   Extensions are loaded dynamically at startup.
*   If an extension crashes, it can bring down the entire runtime unless properly isolated using worker threads.
*   Always review the source code of third-party extensions before deploying them to production.

### 5.2 Skills (ClawdHub Marketplace)

Skills are higher-level capabilities downloaded from the ClawdHub marketplace. They are often declarative or script-based and provide the agent with new tools, APIs, or behavioral patterns. Skills are managed via the `openclaw` CLI.

**ClawdHub Operations:**

*   `openclaw skill search <keyword>`: Search the ClawdHub marketplace for new skills. Example: `openclaw skill search "calendar integration"`
*   `openclaw skill install <skill_id>`: Download and install a skill into the current workspace. Example: `openclaw skill install clawdhub/google-calendar-v2`
*   `openclaw skill update <skill_id>`: Update an installed skill to the latest version.
*   `openclaw skill list`: List all currently installed skills, their versions, and their active status.
*   `openclaw skill remove <skill_id>`: Uninstall a skill and remove its associated configuration from the workspace.

## 6. Multi-Agent Orchestration

OpenClaw excels in multi-agent orchestration, utilizing background workers to handle complex, parallel, or long-running tasks. The primary orchestration engine delegates tasks to specialized agents such as Codex (for code generation and analysis), Claude Code (for architectural reasoning), and Pi (for empathetic user engagement).

The orchestration topology is defined in the `AGENTS.md` file, and inter-agent communication is handled via a lightweight internal message bus (often backed by Redis in clustered deployments).

### 6.1 Debugging Inter-Agent Communication

When multi-agent workflows fail, the issue often lies in the message bus, permission boundaries, or worker timeouts. Use `grep` and `awk` to trace inter-agent messages in the runtime logs.

**Trace Messages Sent to the Codex Worker:**
```bash
grep "\[MessageBus\] Dispatching to worker: codex" /var/log/openclaw/runtime.log
```

**Identify Cross-Context Messaging Denied Errors:**
This error occurs when an agent attempts to send a message to another agent without the proper authorization defined in `AGENTS.md`.
```bash
grep "Cross-context messaging denied" /var/log/openclaw/runtime.log | awk '{print $1, $2, "Source:", $8, "Target:", $10}'
```

**Monitor Worker Timeouts:**
```bash
grep "Worker timeout exceeded" /var/log/openclaw/runtime.log
```

## 7. Channel Operations and Known Errors

OpenClaw supports 14 messaging channels, but the most commonly deployed are WhatsApp, Signal, and Telegram. Each channel has its own underlying engine and specific failure modes. Understanding these failure modes is critical for maintaining high availability.

### 7.1 WhatsApp (Baileys Engine)

The WhatsApp integration utilizes the Baileys library. It is highly capable but susceptible to network instability, session invalidation, and strict rate limiting by Meta.

**Known Error: WhatsApp 408 Timeouts**
*   **Symptom:** The agent fails to send or receive messages, and the logs show repeated `408 Request Timeout` errors from the Baileys engine. The connection state may flap between `connecting` and `close`.
*   **Root Cause:** Typically caused by a stale connection to the WhatsApp Web socket, a temporary IP ban from Meta's servers due to high message volume, or underlying network instability.
*   **Resolution:**
    1.  Restart the OpenClaw runtime to force a clean socket reconnection.
    2.  If the issue persists, clear the Baileys session state directory (`rm -rf /var/lib/openclaw/whatsapp_sessions/*`) and re-authenticate via QR code. This is a disruptive action and should be a last resort.
    3.  Check network egress rules to ensure outbound traffic to WhatsApp servers (TCP ports 443, 5222) is not being throttled or dropped.
    4.  Implement message queuing and rate limiting within OpenClaw to avoid triggering Meta's anti-spam filters.

### 7.2 Signal (signal-cli Engine)

The Signal integration relies on the `signal-cli` daemon running in the background, communicating with OpenClaw via RPC over a local socket or TCP port.

**Known Error: Signal RPC Failures**
*   **Symptom:** OpenClaw logs indicate `RPC connection refused`, `Timeout waiting for signal-cli response`, or `Broken pipe`. The agent cannot send or receive Signal messages.
*   **Root Cause:** The `signal-cli` daemon has crashed, is hung, the RPC port specified in `openclaw.json` is blocked or in use by another process, or the Java Virtual Machine (JVM) running `signal-cli` has run out of memory.
*   **Resolution:**
    1.  Verify the `signal-cli` process is running: `ps aux | grep signal-cli`.
    2.  If not running, restart the daemon: `systemctl restart signal-cli`.
    3.  Check the `signal-cli` logs (usually in `~/.local/share/signal-cli/data/`) for underlying errors such as database corruption or registration issues.
    4.  Ensure the RPC port (default 8080) matches the configuration in `openclaw.json` and is not blocked by a local firewall.
    5.  If the JVM is crashing, increase the heap size allocated to `signal-cli`.

### 7.3 Telegram (Polling Engine)

The Telegram integration uses a standard long-polling mechanism to retrieve updates from the Telegram Bot API. While simple to set up, it can be inefficient at high volumes.

**Known Error: Telegram getUpdates Timeout**
*   **Symptom:** The agent stops responding to Telegram messages, and logs show `getUpdates request timed out` or `NetworkError: read ECONNRESET`.
*   **Root Cause:** Network latency between the OpenClaw server and Telegram API endpoints, Telegram API rate limiting (HTTP 429 Too Many Requests), or transient DNS resolution failures.
*   **Resolution:**
    1.  Increase the `poll_interval_ms` in `openclaw.json` to reduce the frequency of requests and avoid rate limits.
    2.  Implement exponential backoff in the polling loop (this is a configuration setting in newer OpenClaw versions).
    3.  Verify the server's DNS resolution is functioning correctly and quickly. Consider using a local caching DNS resolver.
    4.  For high-volume deployments, switch from the polling engine to the webhook engine, which requires exposing a public HTTPS endpoint but is significantly more efficient and reliable.

## 8. Advanced Directory Operations with `grep`, `find`, and `awk`

Managing a large OpenClaw deployment requires efficient navigation and searching of the workspace directory structure. These one-liners are essential for rapid incident response and auditing.

**Find All Markdown Files Modified in the Last 24 Hours:**
```bash
find /opt/openclaw/workspace -name "*.md" -type f -mtime -1 -exec ls -l {} \;
```

**Search for a Specific API Key or Secret Across All Configuration Files:**
```bash
grep -rnw '/opt/openclaw/config' -e 'sk-[a-zA-Z0-9]\{48\}' --color=always
```

**Identify Large Session Files (Over 100MB) that May Need Archiving:**
```bash
find /var/log/openclaw/sessions -name "*.jsonl" -type f -size +100M -exec ls -lh {} \;
```

**Extract All Unique Error Codes and Their Frequencies from the Runtime Log:**
```bash
grep -oP 'Error Code: \K\d+' /var/log/openclaw/runtime.log | sort | uniq -c | sort -nr
```

**Find and Delete Empty Session Files to Clean Up the Directory:**
```bash
find /var/log/openclaw/sessions -name "*.jsonl" -type f -empty -delete
```

**Summarize the Total Size of the Workspace Directory:**
```bash
du -sh /opt/openclaw/workspace
```

## 9. Production Deployment Best Practices

To ensure maximum uptime, security, and reliability for your OpenClaw instances, adhere to the following production best practices:

1.  **Log Rotation and Management:** Implement aggressive log rotation for both runtime logs and session JSONL files to prevent disk exhaustion. Use `logrotate` with compression enabled. Forward logs to a centralized logging system (e.g., ELK stack, Splunk) for long-term retention and analysis.
2.  **Process Supervision and Auto-Restart:** Never run OpenClaw directly in a detached `tmux` or `screen` session in production. Use a robust process supervisor like `systemd`, `pm2`, or Docker restart policies to ensure automatic restarts on failure.
3.  **Database Backups and Integrity Checks:** Schedule regular, automated backups of the `memory.sqlite` database. A corrupted vector database can severely degrade the agent's long-term recall capabilities. Run periodic integrity checks using the `sqlite3` commands provided in Section 3.3.
4.  **Monitoring and Alerting:** Integrate OpenClaw with a comprehensive monitoring system (e.g., Prometheus/Grafana, Datadog, or New Relic). Monitor key metrics such as API latency, LLM token usage, tool execution failure rates, and channel connection status. Set up proactive alerts for known errors like WhatsApp 408 timeouts or Signal RPC failures.
5.  **Staged Rollouts and Testing:** When updating extensions, changing core configuration, or installing new skills from ClawdHub, always test in a staging environment first. The dynamic nature of the workspace files means that a poorly written skill can corrupt the agent's `IDENTITY.md` or `SOUL.md`, leading to unpredictable behavior.
6.  **Security and Access Control:** Secure the `openclaw.json` file and the workspace directory with strict file system permissions. Ensure that API keys and secrets are injected via environment variables rather than hardcoded in configuration files. Regularly audit the `TOOLS.md` file to ensure the agent does not have excessive permissions.
7.  **Resource Limits:** Configure resource limits (CPU, memory) for the OpenClaw process using `systemd` or Docker to prevent a runaway agent or memory leak from impacting other services on the host machine.

## 10. Troubleshooting Workflows

When an issue arises, follow these structured workflows to identify and resolve the root cause efficiently.

### 10.1 Agent Unresponsive on All Channels

1.  **Check Process Status:** Verify the OpenClaw runtime is active (`systemctl status openclaw`).
2.  **Review Runtime Logs:** Tail the runtime logs (`tail -f /var/log/openclaw/runtime.log`) and look for fatal errors, LLM provider API failures, or out-of-memory exceptions.
3.  **Verify LLM Connectivity:** Ensure the primary LLM provider is reachable and the API key is valid. Check for rate limiting or quota exhaustion.
4.  **Inspect `HEARTBEAT.md`:** Check the heartbeat file for the last recorded status and load metrics.

### 10.2 Agent Hallucinating or Ignoring Instructions

1.  **Review Context Window:** Use `jq` to extract the recent conversation history from the active session file and verify that the context window is not overflowing or containing corrupted data.
2.  **Inspect Workspace Files:** Check `SOUL.md` and `IDENTITY.md` for unauthorized modifications or conflicting instructions.
3.  **Check Memory Retrieval:** Query the vector database to see if irrelevant or incorrect memories are being retrieved and injected into the prompt.

### 10.3 Tool Execution Failures

1.  **Verify Tool Definition:** Check `TOOLS.md` to ensure the tool is correctly defined and the API endpoint is accurate.
2.  **Review Tool Logs:** Filter the session logs for `tool_call` events and examine the input parameters and the resulting error messages.
3.  **Test Tool Manually:** Attempt to execute the tool's underlying API or script manually from the command line to isolate the issue from the OpenClaw runtime.

## 11. Conclusion

Operating an OpenClaw (ZeroClaw) deployment requires a deep understanding of its architecture, memory systems, and channel integrations. By mastering the CLI commands, `jq` parsing techniques, and `sqlite3` operations detailed in this guide, administrators can effectively troubleshoot complex issues, optimize performance, and ensure the reliable operation of their multi-agent orchestration networks. Continuous monitoring, proactive maintenance, and a rigorous approach to configuration management are the keys to a successful OpenClaw production environment. This document should be treated as a living resource, updated as new extensions are deployed and new operational patterns emerge.
