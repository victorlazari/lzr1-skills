---
name: masterclaw
description: Complete operational playbook for managing OpenClaw agent gateways, NemoClaw distributed engines, and enterprise prompt architectures. Triggers on requests to configure, troubleshoot, or deploy OpenClaw/NemoClaw systems.
---

# Masterclaw Operational Playbook

## Scope and Triggers
This skill provides the operational workflow for managing OpenClaw agent gateways, NemoClaw distributed engines, and enterprise prompt architectures.
**Triggers:** Activates when the user requests to configure, troubleshoot, deploy, or optimize OpenClaw, NemoClaw, or prompt engineering systems.
**Non-goals:** Does not cover general background execution or event-triggered execution outside of OpenClaw/NemoClaw (use `automation-and-scheduling`). Does not cover deploying OpenClaw/NemoClaw services on persistent VMs (use `persistent-computing`).

## Preconditions
1. Identify the target domain: OpenClaw, NemoClaw, or Prompt Engineering.
2. Detect the current environment, installed versions, and available permissions.
3. Verify the user's intent and constraints before proceeding.

## Source Freshness
Volatile facts such as supported versions, configuration schemas, and CLI flags must be verified against upstream documentation before executing production-impacting actions. See the reference files for authoritative sources and verification dates.

## Workflow
1. **Identify Domain:** Determine if the task involves OpenClaw, NemoClaw, or Prompt Engineering and load the corresponding reference file:
   - `references/openclaw-runtime.md`
   - `references/nemoclaw-engine.md`
   - `references/prompt-architecture.md`
2. **Verify Upstream:** Verify current versions and configuration schemas against upstream documentation.
3. **Diagnose/Plan:** Diagnose the issue or plan the implementation using the reference guidelines.
4. **Propose Change:** Propose the change or fix. **REQUIRE USER CONFIRMATION** for destructive or production-impacting actions.
5. **Execute & Validate:** Execute the change, validate syntax, and perform a dry-run if possible.
6. **Verify Postconditions:** Verify postconditions and provide a rollback plan if the change fails.
7. **Stop Condition:** Stop when the system is stable and the output contract is met.

## Safety
- **Read-only Discovery:** Separate read-only discovery (e.g., checking logs, viewing configs) from mutations.
- **Confirmation Required:** Explicit user confirmation is REQUIRED before applying destructive changes to production OpenClaw/NemoClaw clusters.
- **Dry-runs:** Perform dry-runs for configuration changes where supported.

## Validation
- Validate syntax of configuration files before deployment.
- Ensure rollback plans are documented for all state-mutating operations.

## Failure Handling
- If a change fails, diagnose the error using logs and reference guidelines.
- Do not repeat a failed action unchanged.
- Execute the documented rollback plan if necessary.

## Output Contract
The final output must include:
- A summary of the changes made or issues resolved.
- Evidence of successful validation (e.g., syntax check results, dry-run output).
- Any actionable next steps or remaining limitations.

## Resources
- [OpenClaw Runtime Reference](references/openclaw-runtime.md): Core operational reference for OpenClaw agent gateway, memory, and orchestration.
- [NemoClaw Engine Reference](references/nemoclaw-engine.md): Core operational reference for NemoClaw distributed engine and stream processing.
- [Prompt Architecture Reference](references/prompt-architecture.md): Core operational reference for enterprise prompt engineering patterns.
