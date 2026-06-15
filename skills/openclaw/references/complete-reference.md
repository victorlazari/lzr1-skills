# OpenClaw (ZeroClaw) Complete Reference Guide

This document serves as the definitive, consolidated reference for OpenClaw (ZeroClaw) architecture, operations, security, and troubleshooting. It synthesizes all advanced knowledge required to deploy, manage, and debug OpenClaw in production environments.

## 1. Core Architecture & Configuration

OpenClaw is a high-availability, multi-modal, and multi-channel AI agent runtime. It supports over 30 LLM providers and integrates with 14 messaging channels.

### 1.1 `openclaw.json` Configuration
The `openclaw.json` file is the central nervous system of the runtime. It must be strictly version-controlled and validated against the official schema.

**Key Sections:**
-   `instance`: Global settings (ID, log level, workspace directory).
-   `providers`: LLM provider configurations (primary, fallback, API keys, models).
-   `channels`: Messaging channel settings (WhatsApp, Signal, Telegram).
-   `memory`: Vector DB path, context window limits, embedding models.
-   `plugins` / `extensions`: Custom TypeScript plugins and ClawdHub skills.
-   `orchestration`: Multi-agent routing rules and background worker definitions.

**Best Practices:**
-   Never hardcode secrets; use environment variables (e.g., `env:OPENAI_API_KEY`).
-   Utilize dynamic reloading for non-critical changes to minimize downtime.

### 1.2 Workspace Files Ecosystem
The workspace defines the agent's persona, state, and operational parameters via Markdown files:

-   **`SOUL.md`**: Core ethical boundaries, immutable directives, and fundamental purpose.
-   **`IDENTITY.md`**: Persona, tone of voice, and background story.
-   **`USER.md`**: Persistent user preferences and historical context.
-   **`AGENTS.md`**: Topology of the multi-agent network and communication protocols.
-   **`BOOT.md`**: Initialization scripts executed upon startup.
-   **`HEARTBEAT.md`**: Recurring internal checks and health status.
-   **`MEMORY.md`**: Scratchpad for short-term memory consolidation.
-   **`TOOLS.md`**: Manifest of available tools, extensions, and skills.

## 2. The 3-Layer Memory System

OpenClaw balances immediate context awareness with long-term recall using a 3-layer architecture.

### 2.1 Layer 1: Context Window (Short-Term)
-   **Function:** Holds recent conversational turns, tool results, and system prompts.
-   **Management:** Highly volatile; strictly bounded by LLM token limits. Uses a sliding window approach with automated summarization to prevent overflow.

### 2.2 Layer 2: Workspace Files (Mid-Term)
-   **Function:** Persistent, human-readable state (e.g., `USER.md`, `MEMORY.md`).
-   **Management:** Bridging the gap between ephemeral context and permanent databases. Agents explicitly read/write to these files.

### 2.3 Layer 3: Vector Database (Long-Term)
-   **Function:** Semantic recall of historical interactions and learned facts.
-   **Implementation:** Local SQLite database with vector search extensions (`sqlite-vss`) and Gemini embeddings.
-   **Management:** Requires periodic compaction (`VACUUM`) and WAL (Write-Ahead Logging) mode for high concurrency.

## 3. Session Management & JSONL Logs

All interactions are immutably logged in JSON Lines (JSONL) format.

-   **Structure:** Each line represents a discrete event (user message, tool call, error).
-   **Analysis:** Use `jq` for advanced log parsing (e.g., extracting errors, calculating latency).
-   **Compaction:** Automated processes summarize old messages and archive raw JSONL files to prevent disk exhaustion.

## 4. Multi-Agent Orchestration

OpenClaw delegates complex tasks to specialized background workers.

### 4.1 Background Workers
-   **Codex:** Code generation, debugging, and scripting.
-   **Claude Code:** System design, deep repository analysis, and complex logic.
-   **Pi:** User onboarding, emotional support, and sensitive communications.

### 4.2 Routing & Cross-Context Messaging
-   The primary agent acts as a router, dispatching tasks via an internal message bus.
-   **Cross-Context Messaging Denied:** A strict security feature preventing unauthorized data leakage between agents. Ensure explicit pathways are defined in `AGENTS.md` and `openclaw.json`.

## 5. Channel Integrations & Troubleshooting

OpenClaw integrates with 14 channels, each with specific failure modes.

### 5.1 WhatsApp (Baileys Engine)
-   **Known Error:** `408 Request Timeout`.
-   **Root Cause:** Stale WebSocket connection, network instability, or event loop starvation.
-   **Resolution:** Implement aggressive reconnection, offload synchronous operations, and clear corrupted session states if necessary.

### 5.2 Signal (signal-cli Engine)
-   **Known Error:** `RPC Failures` (Connection refused, timeout).
-   **Root Cause:** `signal-cli` daemon crash, OOM (Out of Memory), or SQLite database locks.
-   **Resolution:** Increase Java heap size (`-Xmx`), implement RPC request queuing, and run the daemon under a process manager (`systemd`).

### 5.3 Telegram (Polling Engine)
-   **Known Error:** `getUpdates Timeout` or `HTTP 429 Too Many Requests`.
-   **Root Cause:** Network latency, aggressive polling intervals, or API rate limiting.
-   **Resolution:** Ensure HTTP client timeout > polling timeout, implement exponential backoff, and consider migrating to Webhooks for production.

## 6. Extensions & ClawdHub Skills

OpenClaw's functionality is extended via custom code and marketplace skills.

### 6.1 Custom TypeScript Extensions
-   Run directly within the Node.js runtime.
-   **Risks:** Memory leaks and unhandled exceptions can crash the entire agent.
-   **Mitigation:** Run in isolated worker threads, enforce strict dependency pinning, and profile memory usage.

### 6.2 ClawdHub Skills
-   Pre-packaged capabilities downloaded from the marketplace.
-   **Risks:** Supply chain attacks and breaking changes.
-   **Mitigation:** Pin exact version hashes, use local mirrors for air-gapped deployments, and verify cryptographic signatures.

## 7. Security Audit Procedures

Securing OpenClaw requires rigorous auditing of its complex attack surface.

### 7.1 Credential Directory Protection
-   Enforce strict filesystem permissions (`0700` for directories, `0600` for files).
-   Encrypt the credential directory and session JSONL files at rest.

### 7.2 Workspace Integrity
-   Implement File Integrity Monitoring (FIM) to detect unauthorized changes to `SOUL.md`, `TOOLS.md`, etc.

### 7.3 Extension Sandboxing
-   Execute custom extensions in restricted environments (e.g., V8 isolates) with no access to the host filesystem or unauthorized networks.

## 8. Advanced CLI Operations

Essential command-line operations for managing OpenClaw:

-   **Check SQLite Integrity:** `sqlite3 /var/lib/openclaw/memory.sqlite "PRAGMA integrity_check;"`
-   **Parse JSONL Errors:** `jq -r 'select(.level == "error") | "[\(.timestamp)] \(.message)"' /var/log/openclaw/sessions/*.jsonl`
-   **Trace Inter-Agent Messages:** `grep "\[MessageBus\] Dispatching to worker" /var/log/openclaw/runtime.log`
-   **Find Modified Workspace Files:** `find /opt/openclaw/workspace -name "*.md" -type f -mtime -1`

## 9. Production Best Practices

-   **Log Rotation:** Implement aggressive log rotation and forward logs to a centralized SIEM.
-   **Process Supervision:** Use `systemd` or Docker restart policies to ensure automatic recovery.
-   **Database Backups:** Schedule automated backups of the SQLite vector database.
-   **Monitoring:** Integrate with Prometheus/Grafana to monitor API latency, token usage, and channel status.
-   **Resource Limits:** Configure CPU and memory limits to prevent runaway extensions from impacting the host.
