---
name: bot
description: Advanced Bot Engineering with OpenClaw, NemoClaw, and OpenShell
---

# Bot Specialist Skill

## When to Use

Use this skill when tasked with designing, developing, deploying, or auditing advanced autonomous AI agents and bots using the OpenClaw, NemoClaw, and OpenShell ecosystems. This includes:
- Building and managing native or bundle plugins for OpenClaw.
- Configuring advanced memory systems (QMD, Honcho, LanceDB) and dreaming processes.
- Setting up secure sandboxes with OpenShell, including network policies, credential injection, and L7 proxying.
- Designing multi-agent routing architectures and complexity-based model routing.
- Conducting comprehensive security audits for bot deployments.
- Troubleshooting bot lifecycles, session locking, and plugin hooks.

## Sub-Agent Spawning

This skill supports spawning sub-agents for parallel execution when tasks can be decomposed:

| Trigger Condition | Sub-Agent Type | Purpose |
|---|---|---|
| Multiple plugins to develop/audit | Plugin Engineer | Parallel development or review of native/bundle plugins |
| Multiple network policies to validate | Policy Validator | Parallel validation of OpenShell network policies |
| Multiple environments to deploy | Deployment Specialist | Parallel sandbox creation and configuration |
| Bulk security auditing | Security Auditor | Parallel security review of bot components (auth, data, network) |

### Spawning Rules
- Spawn when 3+ independent items need the same operation
- Each sub-agent receives: context, specific target, success criteria
- Results are aggregated and cross-referenced for conflicts
- Maximum concurrent sub-agents: 10

## Workflow

1. **Architecture & Design**: Define the bot's purpose, required plugins, memory engine, and multi-agent routing rules.
2. **Environment Setup**: Use OpenShell to create secure sandboxes (`openshell sandbox create`), configure network policies, and set up credential providers.
3. **Plugin Development**: Develop native or bundle plugins, utilizing OpenClaw lifecycle hooks (e.g., `before_model_resolve`, `before_agent_reply`).
4. **Memory Configuration**: Configure the appropriate memory engine (Builtin, QMD, Honcho, LanceDB) and set up dreaming/consolidation schedules.
5. **Deployment & Orchestration**: Deploy the bot using the `bot` CLI or OpenShell, managing scaling, persistent storage, and port forwarding.
6. **Security Audit**: Perform a comprehensive security audit covering authentication, data privacy, network segmentation, and input validation.
7. **Monitoring & Troubleshooting**: Utilize `bot status`, `bot logs`, and OpenShell diagnostics to monitor performance and resolve issues.

## Core Principles

- **Defense-in-Depth Security**: Always utilize Landlock, seccomp, and network namespace isolation via OpenShell. Never store credentials in the sandbox filesystem; use L7 proxy credential injection.
- **Modular Extensibility**: Leverage the plugin architecture and ClawHub ecosystem for capabilities rather than building monolithic agents.
- **State and Memory Management**: Ensure robust session locking to prevent race conditions. Use appropriate memory engines and background dreaming for long-term context retention.
- **Least Privilege**: Apply strict network policies (default deny) and operator approval flows for egress traffic.
- **Cost and Performance Optimization**: Utilize complexity-based model routing (e.g., NVIDIA LLM Router) to balance inference costs and latency.

## Key References

- [NemoClaw GitHub Repository](https://github.com/NVIDIA/NemoClaw)
- [OpenShell GitHub Repository](https://github.com/NVIDIA/OpenShell)
- [OpenClaw Documentation](https://docs.openclaw.ai)
- [VoltAgent Awesome NemoClaw](https://github.com/VoltAgent/awesome-nemoclaw)
- [VoltAgent Awesome OpenClaw Skills](https://github.com/VoltAgent/awesome-openclaw-skills)
