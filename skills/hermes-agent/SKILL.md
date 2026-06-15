---
name: hermes-agent
description: Advanced configuration, multi-model orchestration, and deep skill development for Hermes Agent v0.14.0.
---

# Hermes Agent Skill

## When to Use

Use this skill when you need to configure, operate, or troubleshoot Hermes Agent v0.14.0 in production environments. This includes setting up advanced provider configurations (failover, credential pools, auxiliary models), orchestrating multiple models (Mixture of Agents), developing advanced skills with conditional activation and fallback mechanisms, managing the background review system, configuring context engine plugins (Honcho), and setting up advanced Docker backends. It is also essential for managing the Hermes Agent CLI, configuring the `config.yaml` file, and handling complex integrations via the Gateway system and MCP servers.

## Sub-Agent Spawning

This skill supports spawning sub-agents for parallel execution when tasks can be decomposed:

| Trigger Condition | Sub-Agent Type | Purpose |
|---|---|---|
| Multiple provider configurations to validate | Config Validator | Parallel validation of provider API keys and endpoints |
| Multiple skills to develop or review | Skill Developer | Parallel creation or auditing of `SKILL.md` files |
| Multiple environments to deploy | Deployment Agent | Parallel setup of Docker backends and persistent volumes |
| Bulk log analysis for troubleshooting | Diagnostics Agent | Parallel investigation of error logs and failover events |

### Spawning Rules
- Spawn when 3+ independent items need the same operation
- Each sub-agent receives: context, specific target, success criteria
- Results are aggregated and cross-referenced for conflicts
- Maximum concurrent sub-agents: 10

## Workflow

1. **Assess the Environment**: Determine the current state of the Hermes Agent deployment. Check the `config.yaml` file, environment variables, and the status of the terminal backend (e.g., Docker, SSH).
2. **Configure Providers**: Set up primary and failover providers, configure credential pools, and define auxiliary models for specific tasks to ensure high availability and optimal performance.
3. **Develop and Deploy Skills**: Create or update `SKILL.md` files with required environment variables, configuration settings, conditional activation rules, and fallback mechanisms.
4. **Orchestrate Models**: Utilize the Mixture of Agents (MoA) tool to delegate sub-tasks to different models and synthesize their outputs for complex problem-solving.
5. **Manage Context and Memory**: Configure the Honcho context engine plugin and manage the Bounded Curation Strategy for the `MEMORY.md` file to optimize context window usage.
6. **Ensure Security**: Enable the Tirith Security Module, configure the `DANGEROUS_PATTERNS` system, and set up the Command Approval Flow to protect the host environment.
7. **Monitor and Troubleshoot**: Use the `hermes doctor` command and the `--debug` flag to diagnose issues. Analyze the error classification system and retry logic to handle transient failures gracefully.

## Core Principles

- **Resilience**: Always configure failover mechanisms and credential pools to ensure continuous operation in the face of provider outages or rate limits.
- **Security First**: Strictly enforce the Tirith Security Module and exact-pinned dependencies to mitigate supply chain risks and prevent malicious actions.
- **Efficiency**: Leverage advanced prompt caching, context compression, and auxiliary models to optimize token usage and reduce latency.
- **Extensibility**: Utilize Gateway Hooks, the Plugin System, and MCP servers to integrate Hermes Agent with external tools and platforms seamlessly.
- **Continuous Improvement**: Rely on the background review system and memory nudges to allow the agent to learn and adapt over time.

## Key References

- **Advanced Provider Configuration**: Details on failover mechanisms, credential pools, and auxiliary models.
- **Multi-Model Orchestration**: Guide to using the Mixture of Agents (MoA) tool.
- **Advanced Skills Development**: Instructions for creating robust `SKILL.md` files with conditional activation and fallbacks.
- **Error Classification System**: Deep dive into the normalization pipeline and handling `CONTEXT_LENGTH_EXCEEDED` errors.
- **Tirith Security Module**: Overview of the `DANGEROUS_PATTERNS` system and Command Approval Flow.
- **Hermes Agent CLI Reference**: Comprehensive guide to the `hermes` command, subcommands, and interactive slash commands.
- **Config.yaml Schema**: Complete breakdown of the configuration file, including advanced settings for models, terminals, memory, and gateways.
