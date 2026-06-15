# Advanced Bot Engineering: Complete Reference Guide

This document consolidates and enhances the technical knowledge required for advanced bot engineering using the OpenClaw, NemoClaw, and OpenShell ecosystems. It covers architecture, configuration, security, CLI operations, and enterprise deployment patterns.

## 1. OpenClaw Agent Architecture

OpenClaw is the foundational self-hosted gateway and agent runtime. It connects communication channels to AI coding agents, enabling real-time, context-aware interactions.

### 1.1 Agent Loop and Lifecycle
The Agent Loop is an asynchronous process managing message intake, context resolution, model invocation, tool execution, and response generation.
- **Entry Points**: Gateway RPC (`agent`, `agent.wait`) and CLI (`agent`).
- **Stages**:
  1. Session and Parameter Validation (returns `runId`, `acceptedAt`).
  2. Model Resolution and Skill Loading.
  3. Run Serialization (per session key to prevent race conditions).
  4. Session Subscription (bridges Pi-agent core events to OpenClaw).
  5. Completion and Status Reporting.
- **Concurrency**: Uses a session write lock (default 60s timeout) to serialize runs.
- **Message Handling Modes**: `Collect` (aggregates), `Steer` (prioritizes/redirects), `Followup` (chains sequentially).

### 1.2 Plugin Architecture and Hooks
Plugins extend OpenClaw capabilities.
- **Native Plugins**: `openclaw.plugin.json` + JS/TS module. In-process execution. For complex integrations.
- **Bundle Plugins**: Directory layout. External/embedded execution. For rapid skill development.
- **Lifecycle Hooks**:
  - `before_model_resolve`, `before_prompt_build`, `before_agent_reply`, `agent_end`
  - `before_tool_call`, `after_tool_call`, `tool_result_persist`
  - `before_compaction`, `after_compaction`
  - `message_received`, `message_sending`, `message_sent`
  - `session_start`, `session_end`, `gateway_start`, `gateway_stop`

### 1.3 Workspace and State Management
- **Workspace**: `~/.openclaw/workspace` (skills, profiles, tools, personality).
- **State Directory**: `~/.openclaw/agents/<agentId>/agent` (runtime state, logs).
- **Sessions**: `~/.openclaw/agents/<agentId>/sessions` (conversational context).
- **Config Files**: `openclaw.json` (gateway), `SKILL.md` (skills), `USER.md` (profile), `TOOLS.md` (tools), `SOUL.md` (personality).

### 1.4 Memory System
- **Files**: `MEMORY.md` (long-term), `memory/YYYY-MM-DD.md` (episodic), `DREAMS.md` (consolidation summaries).
- **Engines**: Builtin (SQLite), QMD (high-performance sidecar), Honcho (cross-session AI-native), LanceDB (vector DB).
- **Dreaming**: Background consolidation based on score, recall frequency, diversity, and grounded backfill.
- **Memory Wiki Plugin**: Structured vault with claims, evidence, contradiction tracking, and freshness.

## 2. NemoClaw Sandbox Topology and Security

NemoClaw provides a hardened, sandboxed environment for AI agents.

### 2.1 Architecture
- **Topology**: Docker Daemon -> OpenShell Gateway Container (L7 Proxy) -> Embedded k3s Cluster -> Sandbox Pod (OpenClaw + NemoClaw Plugin).
- **Layered Security**:
  - **Landlock**: Restricts filesystem access.
  - **seccomp**: Filters system calls.
  - **Network Namespace Isolation**: Restricts outbound connections.

### 2.2 L7 Proxy and Credential Injection
The OpenShell Gateway acts as an L7 HTTP proxy.
- **Credential Injection**: Dynamically injects API keys into outbound requests (e.g., rewriting `Authorization` headers). Credentials are NEVER stored in the sandbox filesystem.
- **Policy Enforcement**: Restricts hosts, HTTP methods, and URL paths.
- **Operator Approval Flow**: Unknown hosts trigger manual review workflows.

## 3. OpenShell Orchestration

OpenShell manages the secure runtime environment.

### 3.1 Components
- **Gateway**: Control-plane API.
- **Sandbox**: Isolated runtime environment.
- **Policy Engine**: Enforces declarative YAML policies (Filesystem, Network, Process, Inference).
- **Privacy Router**: Securely routes inference requests.

### 3.2 Policy Management
Policies are defined in YAML and can be hot-reloaded (for network/inference).
```yaml
network:
  outbound:
    - host: api.github.com
      methods: [GET]
      paths: ["/**"]
```
- **Presets**: Official presets exist for Discord, Docker, HuggingFace, Jira, NPM, Slack, Telegram, etc.

### 3.3 Credential Providers
Providers bundle API keys and inject them as environment variables.
- Supported: NVIDIA, OpenAI, Anthropic, Google Gemini, Local Ollama.

## 4. Multi-Agent Routing and Inference

### 4.1 Multi-Agent Routing
- **Rules**: Based on Channel, Account ID, Peer, Guild/Team IDs. Configured in `openclaw.json`.
- **Cross-Agent Memory**: Uses QMD extraCollections for shared context.
- **Skill Allowlisting**: Per-agent restriction of skills. Priority: Workspace > Local > Bundled.

### 4.2 Inference Routing
- **NVIDIA LLM Router v3**: Dynamically selects models based on query complexity and cost.
- **Model Pool Config**: Defines routing method (e.g., prefill), checkpoint, tolerance, and available models with cost metrics.

## 5. Bot CLI Reference

The `bot` CLI manages deployments, scheduling, and monitoring.

### 5.1 Core Commands
- `bot init [name] [--template]`: Initialize project.
- `bot deploy [--environment] [--dry-run]`: Deploy bot.
- `bot start <id> [--detach] [--scale]`: Start instance.
- `bot stop <id> [--force] [--timeout]`: Stop instance.
- `bot status [id] [--watch]`: View metrics.
- `bot logs <id> [--tail] [--follow] [--level]`: View logs.

### 5.2 Advanced Commands
- `bot config <get|set|delete|list>`: Manage CLI config.
- `bot secret <add|get|list|remove>`: Manage sensitive data.
- `bot schedule <add|list|remove>`: Manage cron executions.
- `bot network <create-vpc|list-vpcs|add-route|diagnose>`: Manage network isolation.
- `bot storage <provision|attach|detach|snapshot>`: Manage persistent volumes.
- `bot metrics <id> [--timeframe] [--export]`: Extract performance data.
- `bot audit [--compliance-standard]`: Generate security reports.

## 6. Bot Configuration Schemas

### 6.1 `bot-config.yml`
Global settings: `botName`, `prefix`, `language`, `loggingLevel`, `autoReconnect`, `server`, `port`, `useSSL`, `username`, `password`.

### 6.2 `commands.json`
Command definitions: `description`, `usage`, `cooldown`, `enabled`.

### 6.3 `permissions.json`
Role-based access: `commands` list, `accessLevel`.

### 6.4 `responses.yml`
Customizable interaction strings (e.g., greetings, farewells).

## 7. Advanced Architecture and Enterprise Patterns

### 7.1 Design Patterns
- **Event-Driven**: Producers, Consumers, Brokers (RabbitMQ/Kafka) for scalability.
- **Microservices**: Independent deployment, fault isolation, polyglot persistence.
- **State Management**: Stateless vs. Stateful, session management, persistent storage (Redis/DynamoDB).

### 7.2 Handling Edge Cases
- **NLP**: Ambiguity resolution, handling variability (slang/idioms), graceful error handling.
- **Concurrency**: Managing race conditions with locks/semaphores, async programming.

### 7.3 Enterprise Patterns
- **Legacy Integration**: APIs, webhooks, middleware, data transformation.
- **Multi-Tenancy**: Data isolation, resource allocation, tenant customization.
- **Compliance**: GDPR/HIPAA adherence, audit trails, incident response plans.

## 8. Security Audit Checklist

1. **Initial Assessment**: Define scope, inventory assets, assess risks.
2. **Authentication/Authorization**: MFA, strong passwords, least privilege, RBAC/ABAC.
3. **Data Handling**: Classification, encryption (rest/transit), anonymization, privacy compliance.
4. **Network Security**: TLS/SSL, VPNs, firewalls, network segmentation (VLANs).
5. **Input Validation**: Whitelisting, server-side validation, output encoding (XSS prevention).
6. **Error Handling/Logging**: Generic user errors, detailed admin logs, SIEM integration.
7. **Dependencies**: Regular updates, vulnerability scanning, vendor security assurance.
8. **Configuration/Hardening**: Config management, disable unnecessary services, patch management.
9. **Incident Response**: Documented plan, regular drills, continuous monitoring.
10. **Compliance/Legal**: Regulatory audits, legal risk assessment (TOS/liability).
