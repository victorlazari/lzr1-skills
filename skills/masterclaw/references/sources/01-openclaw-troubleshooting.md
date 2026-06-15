# OpenClaw (ZeroClaw) Deep Troubleshooting Guide: Production Operations and Worst-Case Scenarios

## 1. Introduction to OpenClaw Troubleshooting

Welcome to the definitive, deep-dive troubleshooting guide for OpenClaw (also known as ZeroClaw). OpenClaw is a highly advanced, open-source AI agent runtime designed to operate autonomously across a multitude of environments. With support for over 30 Large Language Model (LLM) providers and 14 distinct messaging channels, OpenClaw represents a paradigm shift in how autonomous agents interact with the world. However, this immense flexibility and power come with significant operational complexity. When you are running OpenClaw in a production environment, you are orchestrating a symphony of concurrent processes, network connections, memory synchronizations, and multi-agent communications. When things go wrong, they can go wrong in spectacular and deeply technical ways.

This guide is specifically engineered for production operations, Site Reliability Engineers (SREs), and advanced technical support personnel who are tasked with maintaining OpenClaw deployments at scale. We will not cover basic setup or introductory concepts here. Instead, we will plunge directly into the most severe, complex, and persistent issues that plague high-volume OpenClaw instances. We will dissect worst-case scenarios, analyze raw logs, and provide step-by-step, battle-tested resolution protocols. 

The configuration for OpenClaw is centralized in the `openclaw.json` file, which acts as the nervous system of the runtime. The agent's cognitive state and operational parameters are defined by a strict hierarchy of workspace files: `SOUL.md`, `IDENTITY.md`, `USER.md`, `AGENTS.md`, `BOOT.md`, `HEARTBEAT.md`, `MEMORY.md`, and `TOOLS.md`. Understanding the interplay between these files, the `openclaw.json` configuration, and the underlying infrastructure is paramount for effective troubleshooting.

## 2. Architectural Context and File Relationships

Before diving into specific error states, it is crucial to understand how this troubleshooting guide relates to the broader OpenClaw specialist documentation ecosystem. This file, `01-openclaw-troubleshooting.md`, serves as the operational bedrock for resolving acute system failures. It is intimately connected to the other six specialist files in the repository:

1.  **Architecture and Core (00-openclaw-architecture.md):** The troubleshooting steps detailed here rely heavily on the architectural principles defined in the core documentation. When we discuss lane congestion or memory layer failures, we are directly referencing the architectural constraints outlined in the core guide.
2.  **Memory Management (02-openclaw-memory.md):** OpenClaw utilizes a sophisticated 3-layer memory architecture (context window, workspace files, and a vector database powered by SQLite and Gemini embeddings). Troubleshooting memory corruption or sync issues requires a deep understanding of the memory management protocols.
3.  **Channel Integration (03-openclaw-channels.md):** The channel-specific troubleshooting sections (WhatsApp, Signal, Telegram) in this guide are the practical, reactive counterparts to the proactive integration strategies detailed in the channel documentation.
4.  **Multi-Agent Orchestration (04-openclaw-orchestration.md):** Resolving cross-context messaging blocks and lane congestion directly involves the multi-agent orchestration mechanisms, particularly the background workers like Codex, Claude Code, and Pi.
5.  **Extensions and Skills (05-openclaw-extensions.md):** When custom TypeScript plugins (extensions) or ClawdHub marketplace skills fail, the diagnostic procedures outlined here must be applied in conjunction with the extension development guidelines.
6.  **Security and Compliance (06-openclaw-security.md):** Many connectivity issues, such as RPC failures or messaging blocks, are rooted in security policies or compliance enforcement mechanisms. Troubleshooting must always align with the security postures defined in the security documentation.

Understanding these relationships ensures that when you apply a fix from this guide, you are not inadvertently violating architectural principles or security protocols defined elsewhere in the OpenClaw ecosystem.

## 3. WhatsApp (Baileys) 408 Request Timeout Disconnects

One of the most notorious and disruptive issues in OpenClaw production environments is the persistent WhatsApp 408 Request Timeout disconnect. OpenClaw utilizes the Baileys library for WhatsApp Web API integration. While Baileys is robust, the underlying WebSocket connection to WhatsApp's servers is highly sensitive to latency, packet loss, and state desynchronization.

### 3.1. Symptom Analysis and Log Signatures

When a 408 disconnect occurs, the OpenClaw channel worker will typically emit a cascade of errors. The primary indicator is a sudden cessation of incoming messages, followed by a specific log signature in the channel worker's standard output.

**Typical Log Signature:**
```json
{"level":"error","timestamp":"2026-05-20T14:32:10.123Z","module":"channel:whatsapp","message":"Connection closed with status code 408","details":{"reason":"Request Timeout","isReconnectable":true,"lastNode":"message_ack"}}
{"level":"warn","timestamp":"2026-05-20T14:32:10.125Z","module":"channel:whatsapp","message":"Initiating exponential backoff reconnection strategy. Attempt 1/5."}
```

The 408 error specifically indicates that the WhatsApp server expected a response or a heartbeat (ping) from the Baileys client within a specific timeframe, but did not receive it. This is rarely a problem with the WhatsApp servers themselves; it is almost always an issue with the OpenClaw host environment or the network path.

### 3.2. Root Cause Diagnostics

Several factors can trigger these timeouts in a high-throughput OpenClaw instance:

1.  **Event Loop Starvation:** Node.js, which underpins the Baileys integration, is single-threaded. If OpenClaw is executing heavy synchronous operations (e.g., parsing massive JSONL session files or performing complex local vector embeddings without offloading to a worker thread), the event loop can become blocked. When the event loop is blocked, the Baileys client cannot process incoming WebSocket frames or send required heartbeat pings, leading the WhatsApp server to terminate the connection with a 408.
2.  **Network Jitter and Buffer Bloat:** In containerized environments (like Kubernetes or Docker Swarm), aggressive traffic shaping or inadequate network resource limits can cause micro-stalls in packet delivery. WhatsApp's WebSocket protocol is unforgiving of these stalls.
3.  **Cryptographic State Desynchronization:** Baileys maintains a complex local state of cryptographic keys (Signal protocol sessions) to encrypt and decrypt messages. If the disk I/O is too slow when OpenClaw attempts to write these state updates to the session JSONL files, the client may fall behind the server's expected state, resulting in a timeout during the key negotiation phase of a message receipt.

### 3.3. Resolution Protocols

To permanently resolve WhatsApp 408 disconnects, you must address the underlying resource constraints and configuration bottlenecks.

**Step 1: Offload Synchronous Operations**
Ensure that all heavy computational tasks are offloaded from the main event loop. Review your `openclaw.json` and verify that vector database operations (SQLite + Gemini embeddings) are configured to use asynchronous drivers or dedicated worker threads.

**Step 2: Optimize Baileys Configuration in `openclaw.json`**
You must tune the Baileys connection parameters within the OpenClaw configuration. Increase the default timeout thresholds and adjust the keep-alive intervals.

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

**Step 3: Implement In-Memory State Management (with Async Flush)**
If disk I/O is the bottleneck for cryptographic state updates, configure OpenClaw to hold the Baileys state in memory and flush it to the JSONL session files asynchronously in batches, rather than synchronously on every message. This significantly reduces I/O wait times on the main thread.

**Step 4: Network QoS (Quality of Service)**
If running in Kubernetes, ensure that the OpenClaw pods have guaranteed network bandwidth and are not being throttled by overly restrictive CNI (Container Network Interface) policies. Apply QoS rules to prioritize WebSocket traffic on ports 443 and 5222.

## 4. Signal (signal-cli) RPC Failures

OpenClaw integrates with the Signal network using `signal-cli` via a JSON-RPC interface. This architecture separates the cryptographic heavy lifting of the Signal protocol (handled by the Java-based `signal-cli` daemon) from the OpenClaw Node.js runtime. While secure, this IPC (Inter-Process Communication) bridge is a frequent point of failure, manifesting as RPC timeouts or connection refused errors.

### 4.1. Symptom Analysis and Log Signatures

Signal RPC failures are typically catastrophic for the channel, resulting in a complete inability to send or receive messages. The OpenClaw logs will show IPC connection drops, while the `signal-cli` daemon logs (if available) might show memory exhaustion or database locks.

**Typical Log Signature (OpenClaw):**
```json
{"level":"error","timestamp":"2026-05-20T15:01:22.441Z","module":"channel:signal","message":"RPC call failed: send_message","details":{"error":"Error: connect ECONNREFUSED 127.0.0.1:7583","code":"ECONNREFUSED"}}
```

**Typical Log Signature (signal-cli daemon):**
```text
WARN  [Thread-4] org.whispersystems.signalservice.api.SignalServiceMessageSender - Failed to send message to +1234567890
java.io.IOException: SQLite database is locked
```

### 4.2. Root Cause Diagnostics

The JSON-RPC bridge between OpenClaw and `signal-cli` is fragile under high load. The primary culprits for RPC failures are:

1.  **Daemon Crash or OOM (Out of Memory):** The `signal-cli` daemon is a Java application. If it is not allocated sufficient heap space (`-Xmx`), it will crash under the memory pressure of maintaining thousands of secure sessions, leading to `ECONNREFUSED` errors in OpenClaw.
2.  **SQLite Database Locks:** `signal-cli` uses a local SQLite database to store account state, contacts, and group information. If OpenClaw sends a massive burst of concurrent RPC requests (e.g., broadcasting a message to many users), the SQLite database can become locked, causing subsequent RPC calls to time out and fail.
3.  **Socket Exhaustion:** In high-throughput scenarios, the rapid opening and closing of TCP sockets for the JSON-RPC communication can lead to ephemeral port exhaustion on the host system.

### 4.3. Resolution Protocols

Resolving Signal RPC failures requires tuning both the OpenClaw configuration and the underlying `signal-cli` daemon environment.

**Step 1: Tune `signal-cli` JVM Parameters**
You must ensure the `signal-cli` daemon has adequate resources. Modify the systemd service file or the Docker entrypoint for `signal-cli` to increase the Java heap size.

```bash
# Example modification for signal-cli startup
exec java -Xmx1024M -Xms512M -jar /opt/signal-cli/lib/signal-cli.jar daemon --rpc --tcp 127.0.0.1:7583
```

**Step 2: Implement RPC Request Queuing and Throttling**
OpenClaw must not overwhelm the `signal-cli` daemon. Configure the Signal channel in `openclaw.json` to implement a strict concurrency limit and a request queue for RPC calls. This prevents SQLite database locks by serializing the requests.

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

**Step 3: Persistent Connection (Keep-Alive)**
Ensure that OpenClaw maintains a persistent TCP connection to the `signal-cli` JSON-RPC server rather than opening a new socket for every request. This mitigates ephemeral port exhaustion and reduces the overhead of connection establishment.

## 5. Telegram Polling Timeouts and `getUpdates` Failures

While Telegram offers Webhooks, many OpenClaw deployments utilize long polling (`getUpdates`) for simplicity in environments behind strict NATs or firewalls. However, long polling is susceptible to timeouts, duplicate message processing, and API rate limiting, especially when the Telegram servers are under heavy load or the network connection is unstable.

### 5.1. Symptom Analysis and Log Signatures

Telegram polling issues usually manifest as a complete halt in message ingestion, often accompanied by repeated timeout errors in the logs. If the `offset` parameter is not managed correctly during these timeouts, OpenClaw may process the same messages multiple times upon reconnection.

**Typical Log Signature:**
```json
{"level":"error","timestamp":"2026-05-20T16:15:44.002Z","module":"channel:telegram","message":"Polling error during getUpdates","details":{"error":"ETIMEDOUT","code":"EFATAL","retryIn": 5000}}
{"level":"warn","timestamp":"2026-05-20T16:15:49.005Z","module":"channel:telegram","message":"Retrying getUpdates with offset 84759302"}
```

### 5.2. Root Cause Diagnostics

1.  **Network Partitioning:** The most common cause of `ETIMEDOUT` during `getUpdates` is a temporary network partition between the OpenClaw host and the Telegram API servers (`api.telegram.org`).
2.  **Aggressive Timeout Configuration:** If the HTTP client timeout in OpenClaw is set lower than the `timeout` parameter passed to the Telegram `getUpdates` API, the OpenClaw client will prematurely terminate the connection before Telegram has a chance to respond with new messages or an empty array.
3.  **Rate Limiting (HTTP 429):** If OpenClaw polls too aggressively (e.g., immediately retrying without a delay after an empty response), Telegram will temporarily ban the IP address, resulting in HTTP 429 Too Many Requests errors.

### 5.3. Resolution Protocols

**Step 1: Synchronize Timeout Parameters**
The most critical fix is to ensure that the OpenClaw HTTP client timeout is significantly larger than the long polling timeout requested from Telegram.

Update `openclaw.json`:
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
*Note: The `httpClientTimeoutMs` (60s) must be greater than `pollingTimeoutSeconds` (50s) to allow for network transit time.*

**Step 2: Implement Robust Offset Management**
Ensure that OpenClaw strictly manages the `update_id` offset. The offset must only be incremented *after* a message has been successfully committed to the OpenClaw memory layer (the JSONL session file and the vector DB). If a crash occurs during processing, the offset should not be advanced, ensuring the message is retrieved again on restart.

**Step 3: Exponential Backoff for 429s**
Implement a strict exponential backoff strategy specifically for HTTP 429 responses. If Telegram rate-limits the bot, OpenClaw must immediately cease polling and wait for the duration specified in the `Retry-After` header provided by Telegram.

## 6. Cross-Context Messaging Blocks and Security Violations

OpenClaw's multi-agent orchestration allows different background workers (e.g., Codex for coding, Claude Code for analysis, Pi for empathetic interaction) to collaborate. However, to prevent data leakage and maintain security boundaries, OpenClaw enforces strict context isolation. A "Cross-Context Messaging Block" occurs when an agent attempts to share information or pass a task to another agent across a restricted boundary.

### 6.1. Symptom Analysis and Log Signatures

These blocks are intentional security features, but they manifest as errors when workflows are misconfigured. The user will typically see a message indicating that the agent cannot complete the task, and the logs will show a security policy violation.

**Typical Log Signature:**
```json
{"level":"error","timestamp":"2026-05-20T17:05:11.882Z","module":"orchestration:router","message":"Cross-context messaging blocked","details":{"sourceAgent":"pi_worker","targetAgent":"codex_worker","reason":"Policy Violation: Attempted to pass PII context to unrestricted code execution environment","contextId":"ctx_9948a-bf42"}}
```

### 6.2. Root Cause Diagnostics

1.  **Misconfigured `AGENTS.md` Policies:** The `AGENTS.md` workspace file defines the permissions and boundaries for each background worker. If the policies are too restrictive, legitimate collaboration is blocked.
2.  **Data Classification Failures:** OpenClaw attempts to classify data in the context window. If a user provides benign data that is falsely flagged as PII (Personally Identifiable Information) or sensitive, the router will block its transfer to agents that are not cleared for sensitive data (like a generic coding worker).
3.  **Implicit Context Bleed:** An agent might attempt to invoke a tool or a skill from the ClawdHub marketplace that requires a different security context, triggering a block at the tool execution layer.

### 6.3. Resolution Protocols

**Step 1: Audit `AGENTS.md` and `openclaw.json`**
Review the `AGENTS.md` file to ensure that the intended communication pathways are explicitly authorized. You must define clear data sharing agreements between the workers.

Example `AGENTS.md` snippet:
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

**Step 2: Implement Data Sanitization Middleware**
If an agent like Pi needs to send a task to Codex, you must configure a sanitization middleware in `openclaw.json` that strips sensitive information before the message crosses the context boundary.

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

**Step 3: Refine Data Classification Prompts**
If false positives are causing blocks, you may need to adjust the system prompts in `IDENTITY.md` or `SOUL.md` to better instruct the primary routing agent on how to classify and handle user data accurately.

## 7. Lane Congestion and Multi-Agent Orchestration Issues

OpenClaw uses a "lane" system for multi-agent orchestration. Think of lanes as dedicated message queues or processing pipelines for different types of tasks (e.g., a "fast lane" for simple chat, a "heavy lane" for deep research using Claude Code). Lane congestion occurs when the volume of tasks assigned to a specific lane exceeds the processing capacity of the background workers assigned to that lane.

### 7.1. Symptom Analysis and Log Signatures

Lane congestion results in severe latency for the end-user. The agent may appear unresponsive for minutes at a time.

**Typical Log Signature:**
```json
{"level":"warn","timestamp":"2026-05-20T18:22:01.115Z","module":"orchestration:lanes","message":"Lane congestion detected","details":{"lane":"heavy_research","queueDepth": 450, "averageWaitTimeMs": 120500, "activeWorkers": 2}}
```

### 7.2. Root Cause Diagnostics

1.  **Insufficient Worker Allocation:** The most common cause is simply not having enough background workers (e.g., Claude Code instances) provisioned for the "heavy" lane in `openclaw.json`.
2.  **Poison Pill Tasks:** A single, highly complex task (e.g., a request to analyze a massive dataset using a custom TypeScript extension) can monopolize a worker for an extended period, blocking the entire lane.
3.  **LLM Provider Rate Limits:** If the background workers are hitting rate limits with the upstream LLM providers (e.g., OpenAI or Anthropic), they will implement exponential backoff, drastically reducing the throughput of the lane and causing congestion.

### 7.3. Resolution Protocols

**Step 1: Dynamic Worker Scaling**
Configure OpenClaw to dynamically scale the number of background workers based on lane queue depth. This requires integration with your container orchestration platform (like Kubernetes HPA).

Update `openclaw.json` to define scaling thresholds:
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

**Step 2: Implement Task Timeouts and Preemption**
To prevent "poison pill" tasks from blocking a lane indefinitely, enforce strict execution timeouts for all background workers. If a task exceeds the timeout, it should be preempted, marked as failed, and the worker returned to the pool.

**Step 3: Provider Load Balancing**
If LLM provider rate limits are the bottleneck, configure OpenClaw to load balance requests across multiple API keys or even multiple providers (e.g., falling back from GPT-4 to Claude 3.5 Sonnet if OpenAI rate limits are hit) within the same lane.

## 8. Embedded Run Timeouts

OpenClaw allows for "embedded runs," where the agent executes custom code (often Python or TypeScript) in a sandboxed environment to perform data analysis, web scraping, or system administration tasks. Embedded run timeouts occur when this sandboxed code takes too long to execute.

### 8.1. Symptom Analysis and Log Signatures

The user will receive an error indicating that the tool execution failed.

**Typical Log Signature:**
```json
{"level":"error","timestamp":"2026-05-20T19:10:33.401Z","module":"sandbox:executor","message":"Embedded run timeout exceeded","details":{"tool":"data_analyzer_script","executionTimeMs": 30005, "limitMs": 30000, "pid": 4492}}
```

### 8.2. Root Cause Diagnostics

1.  **Inefficient Code:** The code generated by the agent or provided via a ClawdHub skill is poorly optimized (e.g., an infinite loop, or processing a large dataset in memory instead of streaming).
2.  **External Dependency Latency:** The embedded script is making network calls to a slow external API or database.
3.  **Resource Starvation:** The sandbox environment (e.g., a Docker container or a WebAssembly runtime) is not allocated enough CPU or memory, causing the script to execute artificially slowly.

### 8.3. Resolution Protocols

**Step 1: Increase Sandbox Timeouts (with Caution)**
If the task legitimately requires more time (e.g., training a small machine learning model), you can increase the timeout limit in `openclaw.json` or `TOOLS.md`. However, this should be done sparingly, as it ties up system resources.

**Step 2: Optimize Tool Design in `TOOLS.md`**
Ensure that the descriptions in `TOOLS.md` explicitly instruct the agent to write efficient code, use pagination for large datasets, and implement proper error handling and timeouts for external network requests within the embedded script itself.

**Step 3: Asynchronous Tool Execution**
For long-running tasks, modify the tool architecture so that the embedded run initiates a background job and immediately returns a job ID to the agent. The agent can then periodically poll the status of the job, rather than blocking and waiting for the execution to complete synchronously.

## 9. Memory Layer Corruption and Sync Issues

OpenClaw's 3-layer memory (context window, workspace files, vector DB) must remain perfectly synchronized. If the SQLite database becomes corrupted or the Gemini embeddings fail to generate, the agent will suffer from "amnesia" or hallucinate based on outdated information.

### 9.1. Symptom Analysis and Log Signatures

The agent will fail to recall recent conversations or will contradict instructions defined in `USER.md` or `IDENTITY.md`.

**Typical Log Signature:**
```json
{"level":"error","timestamp":"2026-05-20T20:05:12.991Z","module":"memory:vector_db","message":"Failed to generate Gemini embedding for session chunk","details":{"error":"API Error: 503 Service Unavailable","chunkId":"chk_883a-99b"}}
{"level":"fatal","timestamp":"2026-05-20T20:05:13.001Z","module":"memory:sync","message":"Memory layer desynchronization detected. SQLite state does not match JSONL session log."}
```

### 9.2. Root Cause Diagnostics

1.  **Embedding API Failures:** If the Gemini API is down or rate-limiting the OpenClaw instance, new memories cannot be vectorized and stored in the SQLite database.
2.  **Concurrent Write Conflicts:** If multiple background workers attempt to write to the SQLite database simultaneously without proper locking mechanisms, the database file can become corrupted.
3.  **Disk Space Exhaustion:** The JSONL session files and the SQLite database can grow rapidly. If the host runs out of disk space, write operations will fail, leading to immediate corruption.

### 9.3. Resolution Protocols

**Step 1: Implement Embedding Fallbacks and Queues**
If the primary embedding provider (Gemini) fails, OpenClaw must queue the memory chunks for later processing or fall back to a local embedding model (e.g., a small HuggingFace model running via an extension) to maintain synchronization.

**Step 2: SQLite WAL Mode and Connection Pooling**
Ensure that the SQLite database is configured to use Write-Ahead Logging (WAL) mode. This significantly improves concurrency and reduces the risk of database locks and corruption during high-volume write operations. Configure a robust connection pool in `openclaw.json`.

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

**Step 3: Automated Compaction and Archiving**
Implement a scheduled task (defined in `BOOT.md` or via a system cron job) to periodically compact the SQLite database (`VACUUM`) and archive old JSONL session files to cold storage (e.g., AWS S3) to prevent disk space exhaustion.

## 10. Extension and ClawdHub Skill Failures

Extensions (custom TypeScript plugins) and Skills (downloaded from the ClawdHub marketplace) execute within the OpenClaw runtime. A poorly written extension can crash the entire agent process.

### 10.1. Symptom Analysis and Log Signatures

Errors will typically originate from the `extension_manager` module, often accompanied by stack traces pointing to specific TypeScript files within the extension directory.

**Typical Log Signature:**
```json
{"level":"error","timestamp":"2026-05-20T21:30:44.221Z","module":"extension_manager","message":"Unhandled exception in extension: clawdhub-salesforce-integration","details":{"error":"TypeError: Cannot read properties of undefined (reading 'data')","stack":"..."}}
```

### 10.2. Root Cause Diagnostics

1.  **API Changes:** The external service the skill interacts with (e.g., Salesforce, Jira) has changed its API, breaking the skill's logic.
2.  **Dependency Conflicts:** The extension relies on a specific version of an npm package that conflicts with a package used by the core OpenClaw runtime or another extension.
3.  **Memory Leaks:** The TypeScript extension does not properly garbage collect resources, leading to a gradual increase in memory usage until the OpenClaw process OOMs.

### 10.3. Resolution Protocols

**Step 1: Isolate and Disable**
The immediate response to a failing extension is to disable it in `openclaw.json` to restore core functionality.

```json
{
  "extensions": {
    "clawdhub-salesforce-integration": {
      "enabled": false
    }
  }
}
```

**Step 2: Sandbox Extension Execution**
To prevent a single extension from crashing the main process, configure OpenClaw to run extensions in isolated worker threads or separate processes (e.g., using Node.js `worker_threads` or child processes). This ensures that an unhandled exception in an extension only crashes that specific worker, not the entire agent.

**Step 3: Dependency Pinning and Auditing**
Enforce strict dependency pinning for all custom extensions. Before deploying a ClawdHub skill to production, audit its `package.json` and run it through a staging environment to identify potential conflicts with the core runtime.

## 11. Conclusion

Troubleshooting OpenClaw in a production environment requires a holistic understanding of its architecture, from the low-level WebSocket connections of the messaging channels to the high-level cognitive routing of the multi-agent orchestrator. By systematically analyzing log signatures, understanding the root causes of resource starvation and state desynchronization, and applying the resolution protocols detailed in this guide, SREs and operations teams can maintain highly available, resilient, and performant autonomous agent deployments. Remember that the `openclaw.json` configuration and the workspace files (`SOUL.md`, `MEMORY.md`, etc.) are your primary levers for tuning and stabilizing the system. Always test configuration changes in a staging environment before applying them to production traffic.
