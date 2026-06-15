# OpenClaw (ZeroClaw) Configuration Schemas and Architecture Guide

## 1. Introduction to OpenClaw

OpenClaw, also widely known in the community as ZeroClaw, is a highly advanced, open-source AI agent runtime designed for production-grade, multi-agent orchestration. Built to handle complex, long-running tasks across a variety of platforms, OpenClaw boasts native support for over 30 LLM providers (including OpenAI, Anthropic, Google, Groq, and local models via Ollama) and integrates seamlessly with 14 distinct messaging channels. 

This document serves as the definitive guide to the configuration schemas, workspace architecture, memory management, and troubleshooting protocols for OpenClaw. It is specifically tailored for production operations, worst-case scenario recovery, and advanced technical support.

### 1.1 Relation to Other Specialist Files
This configuration schema guide is the foundational document (Topic 6) in the OpenClaw specialist series. It directly informs:
- **Deployment & Scaling:** Understanding `openclaw.json` is critical for containerized deployments.
- **Memory Management:** The 3-layer memory architecture described here dictates how vector databases and workspace files are provisioned.
- **Channel Integration:** The channel block schemas are prerequisite knowledge for troubleshooting WhatsApp, Signal, and Telegram integrations.
- **Multi-Agent Orchestration:** Background worker configurations rely on the session JSONL structures detailed in this guide.

---

## 2. Core Configuration: `openclaw.json`

The heart of any OpenClaw instance is the `openclaw.json` file. This file dictates the runtime behavior, provider selection, channel activation, and plugin management. It must be strictly validated against the OpenClaw JSON schema to prevent catastrophic runtime failures.

### 2.1 Schema Definition

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
      "max_retries": 10
    },
    "signal": {
      "enabled": true,
      "engine": "signal-cli",
      "daemon_port": 8080,
      "phone_number": "+1234567890"
    },
    "telegram": {
      "enabled": true,
      "engine": "polling",
      "bot_token": "${TELEGRAM_BOT_TOKEN}",
      "poll_interval_ms": 1000
    }
  },
  "memory": {
    "vector_db": {
      "engine": "sqlite",
      "path": "./data/vector.db",
      "embeddings": {
        "provider": "google",
        "model": "models/embedding-001"
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
  "orchestration": {
    "background_workers": ["codex", "claude-code", "pi"],
    "max_concurrent_tasks": 50
  }
}
```

### 2.2 Configuration Deep Dive

#### 2.2.1 LLM Providers
OpenClaw supports a primary and fallback provider system. If the primary provider experiences a rate limit (HTTP 429) or server error (HTTP 500+), the runtime automatically seamlessly switches to the fallback provider. Environment variables (e.g., `${ANTHROPIC_API_KEY}`) are interpolated at startup.

#### 2.2.2 Channels Block
The `channels` block defines how the agent interacts with the outside world. 
- **WhatsApp:** Utilizes the Baileys library. The `session_dir` must be persistent across container restarts to avoid requiring re-authentication via QR code.
- **Signal:** Relies on `signal-cli` running in daemon mode. The `daemon_port` must match the exposed port of the `signal-cli` service.
- **Telegram:** Uses long polling by default. Webhooks can be configured by changing the `engine` to `webhook` and providing a `webhook_url`.

#### 2.2.3 Plugins and Extensions
OpenClaw extends its capabilities through two primary mechanisms:
1. **Extensions:** Custom TypeScript plugins developed locally and referenced via the `path` attribute. These are compiled at runtime.
2. **Skills:** Pre-packaged capabilities downloaded from the ClawdHub marketplace.

---

## 3. Workspace Architecture

OpenClaw utilizes a file-based workspace architecture to define the agent's persona, rules, and state. These files are typically stored in a `.workspace` directory and are continuously monitored for changes.

### 3.1 Core Workspace Files

- **`SOUL.md`**: The core essence of the agent. Defines the fundamental personality, ethical boundaries, and immutable directives. This file is loaded into the system prompt with the highest priority.
- **`IDENTITY.md`**: Defines the agent's current role, name, background story, and specific domain expertise.
- **`USER.md`**: Contains information about the user(s) interacting with the agent. This is dynamically updated by the agent to build long-term user profiles.
- **`AGENTS.md`**: In multi-agent setups, this file lists the available background workers (e.g., Codex, Claude Code, Pi) and their specific capabilities, allowing the primary agent to delegate tasks effectively.
- **`BOOT.md`**: Initialization instructions. Contains scripts or commands that the agent must execute upon startup (e.g., "Check the weather API and summarize the day").
- **`HEARTBEAT.md`**: A system-managed file that records the last successful cycle of the agent loop. Used by external watchdogs to detect stalled agents.
- **`MEMORY.md`**: A scratchpad for the agent to write down short-term notes, intermediate reasoning steps, or temporary state that doesn't belong in the vector database.
- **`TOOLS.md`**: A dynamically generated file listing all currently available tools, extensions, and ClawdHub skills, along with their JSON schemas.

### 3.2 Workspace File Management in Production
In production environments, these files should be mounted as a persistent volume. Changes to `SOUL.md` or `IDENTITY.md` trigger a hot-reload of the agent's context window, which may cause a brief latency spike (typically 200-500ms) as the LLM processes the new system prompt.

---

## 4. The 3-Layer Memory Architecture

OpenClaw's ability to maintain coherence over long-running sessions is driven by its sophisticated 3-layer memory architecture.

### 4.1 Layer 1: The Context Window
The immediate, short-term memory. This contains the system prompt (derived from workspace files), the recent conversation history, and the outputs of recently executed tools. OpenClaw dynamically prunes this window to stay within the configured `context_window_size` (e.g., 128k tokens), prioritizing recent messages and critical system instructions.

### 4.2 Layer 2: Workspace Files
The mid-term, structured memory. Files like `USER.md` and `MEMORY.md` act as a bridge between the ephemeral context window and the permanent database. The agent is explicitly instructed to read and write to these files to maintain state across context window resets.

### 4.3 Layer 3: Vector Database
The long-term, semantic memory. OpenClaw uses SQLite with the `sqlite-vss` extension for lightweight, embedded vector search. 
- **Embeddings:** By default, it utilizes Gemini embeddings (`models/embedding-001`) to convert text into high-dimensional vectors.
- **Retrieval:** When the user asks a question, OpenClaw queries the SQLite database for semantically similar past interactions and injects them into the context window.

---

## 5. Session Management: JSONL Files

All interactions, tool calls, and state changes are immutably logged in JSONL (JSON Lines) format. This is crucial for auditing, debugging, and fine-tuning future models.

### 5.1 Session JSONL Schema

Each line in a session file (e.g., `session_20260520_143022.jsonl`) represents a single event.

```json
{"timestamp": "2026-05-20T14:30:22.105Z", "type": "user_message", "channel": "whatsapp", "sender_id": "1234567890@s.whatsapp.net", "content": "Can you analyze the Q3 report?"}
{"timestamp": "2026-05-20T14:30:22.500Z", "type": "agent_thought", "content": "I need to retrieve the Q3 report from the vector DB and then use the data analysis tool."}
{"timestamp": "2026-05-20T14:30:23.012Z", "type": "tool_call", "tool_name": "query_vector_db", "arguments": {"query": "Q3 financial report 2025"}}
{"timestamp": "2026-05-20T14:30:24.550Z", "type": "tool_result", "tool_name": "query_vector_db", "result": "Found 3 matching documents..."}
{"timestamp": "2026-05-20T14:30:28.100Z", "type": "agent_message", "channel": "whatsapp", "recipient_id": "1234567890@s.whatsapp.net", "content": "Based on the Q3 report, revenue increased by 15%..."}
```

### 5.2 Log Rotation and Archival
In production, session JSONL files can grow rapidly. It is recommended to configure a cron job to compress and archive files older than 7 days to an S3-compatible object store.

---

## 6. Multi-Agent Orchestration

OpenClaw excels at complex task delegation using background workers. The primary agent acts as a router and synthesizer, while specialized workers handle heavy lifting.

### 6.1 Background Workers
- **Codex:** Specialized in code generation, debugging, and executing scripts in isolated sandboxes.
- **Claude Code:** Optimized for deep repository analysis, refactoring, and architectural planning.
- **Pi:** Focused on empathetic user interaction, emotional intelligence, and drafting sensitive communications.

### 6.2 Orchestration Flow
1. The primary agent receives a complex request (e.g., "Build a React dashboard for the Q3 data").
2. The primary agent writes a task definition to a temporary workspace file.
3. The primary agent invokes the `delegate_task` tool, assigning the task to the **Codex** worker.
4. The Codex worker spins up in a separate thread, executes the task, and writes the result back to the workspace.
5. The primary agent reads the result and communicates the final output to the user.

---

## 7. Troubleshooting and Known Errors

Operating OpenClaw in production requires familiarity with common failure modes across its various integrations.

### 7.1 WhatsApp 408 Timeouts
**Symptom:** The Baileys engine repeatedly logs `Error: 408 Request Timeout` and messages fail to send.
**Root Cause:** The connection to the WhatsApp Web socket has become stale, often due to network instability or the host device (phone) losing connectivity.
**Resolution:** 
1. Force a reconnection by restarting the OpenClaw process.
2. If the issue persists, delete the `session_dir` (e.g., `./sessions/wa`) and re-authenticate via QR code.
3. Ensure the host phone has a stable internet connection and battery optimization is disabled for WhatsApp.

### 7.2 Signal RPC Failures
**Symptom:** Logs show `SignalRPCException: Connection refused` or `Method not found`.
**Root Cause:** The `signal-cli` daemon has crashed, or the OpenClaw instance is attempting to communicate on the wrong port.
**Resolution:**
1. Verify that `signal-cli` is running: `ps aux | grep signal-cli`.
2. Check the `signal-cli` logs for database locks or registration issues.
3. Ensure the `daemon_port` in `openclaw.json` matches the port `signal-cli` is bound to.

### 7.3 Cross-Context Messaging Denied
**Symptom:** The agent attempts to send a message to a user on Telegram based on a trigger from WhatsApp, but the action is blocked with `Error: Cross-context messaging denied`.
**Root Cause:** OpenClaw enforces strict context isolation by default to prevent privacy leaks. An agent cannot spontaneously message a user on Channel B using context gathered from Channel A unless explicitly authorized.
**Resolution:**
1. Update the `SOUL.md` to explicitly grant cross-channel messaging permissions.
2. Ensure the `USER.md` file correctly links the user's identities across different channels (e.g., mapping their WhatsApp number to their Telegram ID).

### 7.4 Telegram getUpdates Timeout
**Symptom:** The Telegram polling engine logs `ETIMEDOUT` or `ESOCKETTIMEDOUT` during `getUpdates` calls.
**Root Cause:** The Telegram API servers are unreachable, or the polling interval is too aggressive, leading to rate limiting.
**Resolution:**
1. Increase the `poll_interval_ms` in `openclaw.json` to at least 2000ms.
2. Consider switching from the `polling` engine to the `webhook` engine for production deployments, as webhooks are significantly more stable and resource-efficient.

---

## 8. Cron Jobs and Scheduled Tasks

OpenClaw supports scheduled tasks via a `cron_jobs.json` configuration file. This allows the agent to perform proactive actions without user prompting.

### 8.1 `cron_jobs.json` Schema

```json
{
  "jobs": [
    {
      "id": "daily_summary",
      "schedule": "0 9 * * *",
      "timezone": "UTC",
      "action": "execute_prompt",
      "payload": {
        "prompt": "Summarize the key events from yesterday and send them to the admin channel.",
        "target_channel": "telegram",
        "target_id": "-100123456789"
      }
    },
    {
      "id": "vector_db_cleanup",
      "schedule": "0 0 * * 0",
      "timezone": "UTC",
      "action": "system_command",
      "payload": {
        "command": "vacuum_database"
      }
    }
  ]
}
```

### 8.2 Best Practices for Cron Jobs
- Always specify a `timezone` to avoid unexpected execution times across different server environments.
- Use the `system_command` action for maintenance tasks (like vacuuming the SQLite database) to keep the agent's context window clean.
- Monitor the `HEARTBEAT.md` file to ensure the cron scheduler thread hasn't silently crashed.

---

## 9. Conclusion

Mastering the OpenClaw configuration schemas and architecture is essential for deploying resilient, highly capable AI agents. By understanding the interplay between `openclaw.json`, the workspace files, the 3-layer memory system, and the various channel integrations, operators can build robust systems capable of handling complex, real-world tasks while gracefully recovering from inevitable network and API failures. Always refer back to this document when troubleshooting production issues or scaling your OpenClaw infrastructure.
