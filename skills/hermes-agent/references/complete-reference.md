# Hermes Agent: Complete Reference Guide

This document serves as the definitive, consolidated reference for operating Hermes Agent v0.20.0 in production environments. It covers advanced provider configurations, multi-model orchestration, deep skill development, background review systems, complex backend setups, and the comprehensive Command Line Interface (CLI).

*Verified against upstream: 2026-08-07*

## 1. Advanced Provider Configuration

In production environments, relying on a single model provider is a significant risk. Hermes Agent provides an advanced provider configuration system that supports automatic failover, credential pools, and auxiliary models to ensure high availability and optimal performance.

### Failover Mechanisms
The failover system seamlessly switches to alternative providers when the primary provider experiences downtime, rate limits, or other transient errors. This is configured in the `config.yaml` file under the `providers` section.

### Credential Pools
Managing API keys for multiple providers can be challenging. Hermes Agent introduces Credential Pools, allowing you to define multiple API keys for a single provider. The agent will round-robin through these keys or select them based on specific criteria.

### Auxiliary Models
Hermes Agent allows you to define auxiliary models for specific tasks, optimizing both cost and latency without sacrificing the quality of the primary agent loop.

## 2. Multi-Model Orchestration

Hermes Agent excels in environments where multiple models must collaborate to solve complex problems. The Mixture of Agents (MoA) tool allows Hermes Agent to delegate sub-tasks to different models and synthesize their outputs.

## 3. Advanced Skills Development

Skills in Hermes Agent are procedural memories that allow the agent to learn and improve over time. Advanced skill development involves configuring settings, environment variables, conditional activation, and fallback mechanisms.

### Grounded Citations Skill
The grounded-citations skill enables verifiable research and fact-checking, ensuring the agent's outputs are backed by credible sources.

## 4. Background Review System

Hermes Agent features a sophisticated background review system that operates asynchronously, analyzing the agent's performance and suggesting improvements through memory nudges and skill updates.

## 5. Context Engine Plugins and Memory Providers

Managing context is critical for long-running agent sessions. Hermes Agent supports context engine plugins and advanced memory providers, such as Honcho, to handle large volumes of information efficiently.

## 6. Iteration Budget System

To prevent runaway processes and manage costs, Hermes Agent implements an Iteration Budget System. The default tool-calling iteration limit has been increased to 500 in v0.20.0.

## 7. Error Classification and Retry Logic

Robust error handling is a hallmark of production-ready systems. Hermes Agent features an advanced error classifier and retry logic to handle transient failures gracefully. Tools now have self-recovery mechanisms to automatically handle common errors.

## 8. Advanced Docker Backend

For tasks requiring execution in an isolated environment, Hermes Agent provides an advanced Docker backend supporting GPU passthrough, persistent volumes, and fine-grained resource limits.

## 9. Gateway Hooks and Extension Points

The Gateway system is highly extensible, allowing developers to intercept and modify messages using Gateway Hooks.

### Outbound Webhooks
Hermes Agent v0.20.0 supports signed outbound webhooks for event pushing, enabling seamless integration with external systems.

## 10. Cross-Session Message Mirroring

Cross-Session Message Mirroring ensures the user's context is synchronized across all platforms, allowing seamless transitions without losing the conversation thread.

## 11. Credential Sources

Hermes Agent supports multiple Credential Sources, allowing retrieval of API keys from secure vaults such as AWS Secrets Manager or HashiCorp Vault.

## 12. Plugin System

The robust plugin system allows developers to extend functionality with third-party integrations.

## 13. Advanced Prompt Caching

Prompt caching reduces latency and costs. Hermes Agent supports advanced mechanisms, including Anthropic's Cache Control.

## 14. Codex Responses Adapter

For environments requiring strict adherence to specific output formats, the Codex Responses Adapter intercepts the agent's output and reformats it to match a predefined schema.

## 15. LSP Integration (Language Server Protocol)

Hermes Agent integrates with LSP to enhance coding capabilities, leveraging intelligent code completion, error checking, and refactoring tools.

## 16. Image Routing and Generation Backends

Hermes Agent supports multiple image generation backends (e.g., FAL, OpenAI DALL-E 3, xAI Grok Vision).

## 17. Real-Time Conversational Voice

Hermes Agent v0.20.0 introduces real-time conversational voice with streaming TTS, barge-in capabilities, and on-device wake words, enabling natural and fluid voice interactions.

## 18. Agent-to-Agent (A2A) Communication

The A2A v1.0 protocol allows Hermes Agent to communicate and collaborate with other autonomous agents, facilitating complex multi-agent workflows.

## 19. Desktop App Platform

The desktop app has evolved into a comprehensive platform featuring artifacts, a plugin SDK, and a quick-entry window for rapid access to agent capabilities.

## 20. The Tirith Security Module

The Tirith Security Module prevents malicious actions and protects the host environment using the `DANGEROUS_PATTERNS` system and Command Approval Flow.

## 21. Supply Chain Security

Hermes Agent uses exact-pinned dependencies to mitigate supply chain risks.

## 22. Hermes Agent CLI Reference

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

### Power Commands (v0.20.0)
- `!command`: Execute shell commands directly.
- `/init`: Initialize a new project or configuration.
- `/diff`: View differences between files or configurations.
- `/context`: Manage and view the current context.
- `/focus`: Focus the agent on a specific task or file.

*Note: The pip and Homebrew installation methods are deprecated. Use the official one-line installer.*
