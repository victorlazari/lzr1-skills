---
name: hermes-agent
description: Advanced configuration, multi-model orchestration, and deep skill development for Hermes Agent v0.20.0, including voice mode, A2A communication, and grounded citations.
---

# Hermes Agent Skill

## Scope and Triggers

Use this skill when you need to configure, operate, or troubleshoot Hermes Agent v0.20.0 in production environments. This includes setting up advanced provider configurations (failover, credential pools, auxiliary models), orchestrating multiple models (Mixture of Agents), developing advanced skills with conditional activation and fallback mechanisms, managing the background review system, configuring context engine plugins (Honcho), and setting up advanced Docker backends. It is also essential for managing the Hermes Agent CLI, configuring the `config.yaml` file, handling complex integrations via the Gateway system and MCP servers, and utilizing v0.20.0 features like real-time conversational voice, Agent-to-Agent (A2A) communication, and grounded citations.

**Escalation Boundaries:** Do not use this skill for modifying the core Hermes Agent source code or performing actions that violate the Tirith Security Module's `DANGEROUS_PATTERNS` without explicit user confirmation.

## Preconditions

Before executing any configuration changes or advanced operations:
1. Verify the target environment and permissions.
2. Ensure the installed Hermes Agent version is v0.20.0 using the provided validation script.
3. Confirm the user's intent, especially for destructive or production-impacting actions.

## Source Freshness

Hermes Agent is a rapidly evolving tool. Volatile facts, such as supported versions, CLI commands, and configuration schemas, must be verified against the official documentation at runtime.
- **Primary Source:** [Hermes Agent Documentation](https://hermes-agent.nousresearch.com/docs/)
- **Repository:** [NousResearch/hermes-agent](https://github.com/nousresearch/hermes-agent)
- **Validation Script:** Run `scripts/verify-hermes-version.sh` to ensure the installed version matches the expected v0.20.0.

## Workflow

1. **Verify Installation:** Run `scripts/verify-hermes-version.sh` to confirm Hermes Agent v0.20.0 is installed and dependencies are met.
2. **Assess the Environment:** Determine the current state of the Hermes Agent deployment. Check the `config.yaml` file, environment variables, and the status of the terminal backend (e.g., Docker, SSH).
3. **Configure Providers:** Set up primary and failover mechanisms, credential pools, and auxiliary models.
4. **Develop and Deploy Skills:** Create or update `SKILL.md` files, incorporating v0.20.0 features like voice mode, A2A communication, and grounded citations.
5. **Orchestrate Models:** Utilize the Mixture of Agents (MoA) tool to delegate sub-tasks to different models and synthesize their outputs.
6. **Manage Context and Memory:** Configure the Honcho context engine plugin and manage the Bounded Curation Strategy for the `MEMORY.md` file.
7. **Ensure Security:** Enable the Tirith Security Module, configure the `DANGEROUS_PATTERNS` system, and set up the Command Approval Flow.
8. **Monitor and Troubleshoot:** Use the `hermes doctor` command and CLI power commands (`!command`, `/init`, `/diff`, `/context`, `/focus`) to diagnose issues. Analyze the error classification system and tool self-recovery mechanisms.
9. **Stop Condition:** The configuration is successfully applied, validated, and no further errors are reported.

## Safety

- **Read-Only Discovery:** Always assess the environment and configuration state before making any changes.
- **Confirmation Required:** Require explicit user confirmation before executing destructive commands, modifying production configurations, or bypassing the Tirith Security Module.
- **Dry Runs:** Implement dry-run options for configuration changes where possible.

## Validation

- **Syntax Checks:** Ensure all generated configuration files (e.g., `config.yaml`) are valid YAML.
- **Postcondition Verification:** After applying changes, run `hermes doctor` to verify the health of the installation.

## Failure Handling

- **Diagnosis:** Use `hermes doctor --debug` and analyze error logs to identify the root cause of failures.
- **Alternatives:** If a provider fails, rely on the configured failover mechanisms and credential pools.
- **Rollback:** Maintain backups of previous configurations and revert to them if a new configuration causes instability. Do not repeat a failed action unchanged.

## Output Contract

The result of using this skill must include:
- A summary of the actions taken and configurations applied.
- Evidence of successful validation (e.g., output of `hermes doctor`).
- Any warnings or non-critical errors encountered.
- Actionable next steps for the user, if applicable.

## Resources

- **[Complete Reference Guide](references/complete-reference.md):** Detailed technical material on advanced configurations, multi-model orchestration, and CLI commands.
- **[Version Verification Script](scripts/verify-hermes-version.sh):** Script to validate the installed Hermes Agent version.

## Orchestration

This skill supports spawning sub-agents for parallel execution when tasks can be decomposed (e.g., validating multiple provider configurations, developing multiple skills).
- **Spawning Rules:** Spawn when 3+ independent items need the same operation. Each sub-agent receives context, specific target, and success criteria.
- **Synthesis:** Results are aggregated and cross-referenced for conflicts using a Consistency Validator Agent and a Synthesis Agent.
