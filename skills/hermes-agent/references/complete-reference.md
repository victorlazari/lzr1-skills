# Hermes Agent: Complete Reference Guide

This document serves as the definitive, consolidated reference for operating Hermes Agent v0.14.0 in production environments. It covers advanced provider configurations, multi-model orchestration, deep skill development, background review systems, complex backend setups, and the comprehensive Command Line Interface (CLI).

## 1. Advanced Provider Configuration

In production environments, relying on a single model provider is a significant risk. Hermes Agent provides an advanced provider configuration system that supports automatic failover, credential pools, and auxiliary models to ensure high availability and optimal performance.

### Failover Mechanisms

The failover system seamlessly switches to alternative providers when the primary provider experiences downtime, rate limits, or other transient errors. This is configured in the `config.yaml` file under the `providers` section. When a request to the primary provider fails, the agent's error classifier evaluates the `FailoverReason`. If the error is deemed recoverable (e.g., a 502 Bad Gateway or a 429 Too Many Requests), the agent automatically routes the request to the first failover provider.

### Credential Pools

Managing API keys for multiple providers can be challenging. Hermes Agent introduces Credential Pools, allowing you to define multiple API keys for a single provider. The agent will round-robin through these keys or select them based on specific criteria, such as remaining quota or rate limit status. This ensures that if one API key hits a rate limit, the agent can immediately switch to another key within the pool.

### Auxiliary Models

Hermes Agent allows you to define auxiliary models for specific tasks. For example, you might use a large, capable model for complex reasoning and a smaller, faster model for simple text extraction or summarization. By routing specific tasks to auxiliary models, you can optimize both cost and latency without sacrificing the quality of the primary agent loop.

## 2. Multi-Model Orchestration

Hermes Agent excels in environments where multiple models must collaborate to solve complex problems. The Mixture of Agents (MoA) tool allows Hermes Agent to delegate sub-tasks to different models and synthesize their outputs. This is particularly useful for tasks that require diverse perspectives or specialized knowledge. The agent sends the task to multiple models simultaneously, and a `synthesizer` model reviews their outputs to generate a comprehensive, unified response.

## 3. Advanced Skills Development

Skills in Hermes Agent are procedural memories that allow the agent to learn and improve over time. Advanced skill development involves configuring settings, environment variables, conditional activation, and fallback mechanisms.

### Config Settings and Environment Variables

Skills can define their own configuration settings and required environment variables in their `SKILL.md` file. When the agent loads a skill, it verifies that the required environment variables are present and applies the configuration settings. If any requirements are missing, the skill is disabled, and a warning is logged.

### Conditional Activation and Fallback Skills

To optimize context window usage, skills can be conditionally activated based on the current task or available toolsets using the `requires_toolsets` and `fallback_for_toolsets` directives. Fallback skills are designed to handle situations where a primary skill fails or is unavailable, providing a safety net to ensure the agent can still accomplish its goals.

## 4. Background Review System

Hermes Agent features a sophisticated background review system that operates asynchronously, analyzing the agent's performance and suggesting improvements.

### Memory Nudges and Skill Improvement

The background review system continuously monitors the agent's interactions and updates its memory. If the agent repeatedly struggles with a specific type of task, the review system can inject a "memory nudge" into the `MEMORY.md` file to guide future behavior. Additionally, the system can analyze the execution of skills and suggest improvements, generating revised versions of skills for user approval.

## 5. Context Engine Plugins and Memory Providers

Managing context is critical for long-running agent sessions. Hermes Agent supports context engine plugins and advanced memory providers, such as Honcho, to handle large volumes of information efficiently. Honcho provides a static block of context that is injected into the prompt assembly pipeline, ensuring the agent always has access to essential information across multiple sessions and platforms.

## 6. Iteration Budget System

To prevent runaway processes and manage costs, Hermes Agent implements an Iteration Budget System. This system limits the number of iterations the agent can perform within a single conversation loop. If the agent reaches the maximum number of iterations without completing its task, it triggers a `budget_exceeded_action`, which can ask the user for permission to continue, terminate the task, or switch to a cheaper model.

## 7. Error Classification and Retry Logic

Robust error handling is a hallmark of production-ready systems. Hermes Agent features an advanced error classifier and retry logic to handle transient failures gracefully.

### Failover Reasons and Jittered Backoff

The error classifier categorizes API errors into specific `FailoverReason` enums (e.g., `RATE_LIMIT`, `CONTEXT_LENGTH_EXCEEDED`, `SERVER_ERROR`, `UNAUTHORIZED`). When a transient error occurs, the agent employs a jittered backoff strategy before retrying the request, preventing the "thundering herd" problem and ensuring resilience in the face of network instability.

### Handling Context Length Exceeded

When the error classifier identifies a `CONTEXT_LENGTH_EXCEEDED` error, it triggers the Context Compression engine. The agent attempts to compress the conversation history, summarize older messages, or drop less relevant context files before retrying the request. Only if compression fails will the agent failover to a provider with a larger context window.

## 8. Advanced Docker Backend

For tasks requiring execution in an isolated environment, Hermes Agent provides an advanced Docker backend supporting GPU passthrough, persistent volumes, and fine-grained resource limits.

### GPU Passthrough and Persistent Containers

The Docker backend can be configured to pass through GPUs to the container for hardware acceleration. It also supports persistent containers and volumes to maintain state across multiple executions, crucial for tasks involving compiling code or downloading large datasets. Resource limits (CPU, memory, disk) ensure the agent's activities do not impact other applications on the host.

## 9. Gateway Hooks and Extension Points

The Gateway system is highly extensible, allowing developers to intercept and modify messages using Gateway Hooks. Hooks can be registered to execute before a message is processed (`pre_message`) or after a response is generated (`post_message`), providing a mechanism for custom logging, content filtering, and message formatting.

## 10. Cross-Session Message Mirroring

In complex deployments, users may interact with Hermes Agent across multiple platforms (e.g., Slack, Telegram, CLI). Cross-Session Message Mirroring ensures the user's context is synchronized across all platforms, allowing seamless transitions without losing the conversation thread.

## 11. Credential Sources

Hermes Agent supports multiple Credential Sources, allowing retrieval of API keys from secure vaults such as AWS Secrets Manager or HashiCorp Vault. This ensures sensitive keys are never hardcoded in configuration files or exposed in plain text.

## 12. Plugin System

The robust plugin system allows developers to extend functionality with third-party integrations. For example, the Langfuse plugin provides detailed observability insights into token usage and latency, while the Spotify plugin allows the agent to control playback and manage playlists.

## 13. Advanced Prompt Caching

Prompt caching reduces latency and costs. Hermes Agent supports advanced mechanisms, including Anthropic's Cache Control, to cache specific parts of the prompt, such as system instructions or large context files, significantly reducing processed tokens for each request.

## 14. Codex Responses Adapter

For environments requiring strict adherence to specific output formats, the Codex Responses Adapter intercepts the agent's output and reformats it to match a predefined schema using prompt engineering and post-processing.

## 15. LSP Integration (Language Server Protocol)

Hermes Agent integrates with LSP to enhance coding capabilities, leveraging intelligent code completion, error checking, and refactoring tools. Features include Go to Definition, Find References, and real-time Diagnostics.

## 16. Image Routing and Generation Backends

Hermes Agent supports multiple image generation backends (e.g., FAL, OpenAI DALL-E 3, xAI Grok Vision). The Image Routing system intelligently selects the best backend based on the user's request and available resources.

## 17. The Anatomy of a Skill: Procedural Memory in Action

Skills represent the agent's procedural memory. A skill is defined by a directory containing a `SKILL.md` file, which includes metadata, configuration, and instructions. Hermes Agent tracks the provenance of every skill, verifying cryptographic signatures for skills downloaded from the Skills Hub and requiring user approval for self-generated skills.

## 18. Advanced Memory Management: The Bounded Curation Strategy

The `MEMORY.md` file has a strict character limit to ensure efficient caching. Hermes Agent employs a Bounded Curation Strategy, forcing the agent to curate its existing memory when adding new information that would exceed the limit. This involves rewriting memory, summarizing older points, and integrating new data.

## 19. The Kanban Orchestration System

For complex projects, Hermes Agent uses a Kanban Orchestration System to manage tasks across multiple sub-agents. The primary agent breaks down projects into tasks, adds them to a virtual Kanban board, and delegates them to sub-agents. The system is designed for resilience, automatically recovering from sub-agent crashes or timeouts.

## 20. Deep Dive into the Prompt Assembly Pipeline

The prompt assembly pipeline gathers context, formats it, and presents it to the model through 10 distinct layers:
1. Agent Identity (`SOUL.md`)
2. Tool-Aware Behavior Guidance
3. Honcho Static Block
4. Optional System Message
5. Frozen MEMORY Snapshot
6. Frozen USER Profile Snapshot
7. Skills Index
8. Context Files
9. Timestamp and Session ID
10. Platform Hint

## 21. The Tirith Security Module

The Tirith Security Module prevents malicious actions and protects the host environment. It uses the `DANGEROUS_PATTERNS` system to block potentially destructive commands and enforces a Command Approval Flow for sensitive commands. Tirith can bypass certain checks if running in a fully isolated container environment.

## 22. Supply Chain Security

Hermes Agent uses exact-pinned dependencies to mitigate supply chain risks. Every package is pinned to a specific, audited version, and automated tools monitor for vulnerabilities. Users are advised never to run `pip install --upgrade` to maintain this security.

## 23. Advanced Gateway Configuration

Advanced configuration of the Gateway system allows for complex routing and delivery behaviors. Home Channels can be configured where the agent is always active and listening. Delivery preferences can be set to handle platform-specific constraints on message size and formatting.

## 24. The Migration Path: From OpenClaw to Hermes

The `hermes claw migrate` tool provides a comprehensive migration path from OpenClaw to Hermes Agent, translating configurations, converting memory files, migrating session databases, and adapting custom tools.

## 25. Hermes Agent CLI Reference

The Hermes Agent CLI provides granular control over the agent's behavior. Core commands include:
- `hermes`: Initiates an interactive chat session.
- `hermes chat`: Explicitly starts an interactive session.
- `hermes model`: Manages language model configuration.
- `hermes tools`: Manages the agent's toolset.
- `hermes config`: Manages configuration settings.
- `hermes setup`: Launches the first-time setup wizard.
- `hermes doctor`: Diagnostic tool for checking installation health.
- `hermes cron`: Manages scheduled jobs.
- `hermes gateway`: Manages the messaging gateway.
- `hermes skills`: Manages the skills system.
- `hermes claw migrate`: Migrates from OpenClaw.

Interactive slash commands (e.g., `/new`, `/reset`, `/approve`, `/model`, `/memory`) provide quick control during chat sessions.

## 26. Environment Variables and Config.yaml Schema

Hermes Agent relies on environment variables for sensitive information and overriding settings. The `config.yaml` file is the central configuration repository, defining model settings, terminal backends, MCP servers, skills, memory, gateways, cron jobs, browsers, and toolsets. Advanced configurations allow for deep customization of execution environments, authentication, routing, and observability.
