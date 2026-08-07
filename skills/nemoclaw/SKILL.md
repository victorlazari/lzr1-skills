---
name: nemoclaw
description: NVIDIA NemoClaw Platform Specialist for enterprise deployment, guided onboarding, and secure credential handling.
---

# NemoClaw Guide

## Scope and Triggers

Use this skill when you need to:
- Deploy NemoClaw on supported environments (DGX Spark, DGX Station, Windows WSL, Linux/macOS).
- Configure supported agents (OpenClaw, Hermes, LangChain Deep Agents Code).
- Set up inference providers (vLLM, Ollama, NVIDIA Endpoints, OpenRouter, OpenAI, Anthropic, Gemini).
- Execute the guided onboarding workflow using the interactive terminal installer.
- Configure secure credential handling using the local helper script and form.

**Non-Goals:**
- Kubernetes Helm charts deployment.
- Complex multi-sandbox orchestration.
- Adversarial verification panels.

## Preconditions

Before proceeding, ensure:
- The target environment is one of: DGX Spark, DGX Station, Windows WSL, Linux/macOS.
- The required inference provider is supported.
- The agent type is supported.

## Source Freshness

Verify the latest supported agents, deployment environments, and inference providers against the official NVIDIA NemoClaw documentation and GitHub repository.
- [NVIDIA NemoClaw Official Documentation](https://docs.nvidia.com/nemoclaw/latest/)
- [NVIDIA NemoClaw GitHub Repository](https://github.com/NVIDIA/NemoClaw)

## Workflow

1. **Assess deployment requirements**: Determine the target environment (DGX Spark, DGX Station, Windows WSL, Linux/macOS).
2. **Verify supported agents**: Confirm the use of OpenClaw, Hermes, or LangChain Deep Agents Code, and select an inference provider.
3. **Execute guided onboarding**: Run the interactive terminal installer to deploy the sandbox.
4. **Configure secure credentials**: Use the local helper script and form to handle credentials securely.
5. **Validate deployment**: Verify the deployment and inference configuration.
6. **Stop**: Stop when the sandbox is successfully deployed and the agent is responsive.

## Safety

- **Read-only discovery**: Verify environment and requirements before making changes.
- **Mutation confirmation**: Require user confirmation before executing the interactive terminal installer or modifying credential configurations.
- **Secure credentials**: Ensure credentials are not exposed in configuration files; use the provided helper script and form.

## Validation

- Verify the sandbox is running and responsive.
- Confirm the agent can communicate with the selected inference provider.
- Ensure credentials are securely stored and not hardcoded.

## Failure Handling

- If the deployment fails, check the installer logs for errors.
- If the agent is unresponsive, verify the inference provider configuration and network connectivity.
- Do not repeat a failed installation step without addressing the underlying error.

## Output Contract

The result must include:
- A summary of the deployment environment and configured agent.
- Confirmation of successful onboarding and credential configuration.
- Any actionable next steps or warnings.

## Resources

- [Complete Reference](references/complete-reference.md)
- [Local Credential Helper Script](scripts/local-credential-helper.mts)
- [Local Credential Form](docs/resources/local-credential-form.html)

## Orchestration

Parallel work is not required for standard NemoClaw deployment. Execute the workflow sequentially.
