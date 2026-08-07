---
name: manus-workflows
description: Advanced guide for n8n Workflow & Integration Specialists to architect, implement, and troubleshoot sophisticated workflows using n8n's AI agent architecture.
---

# n8n Workflows

## Scope and Triggers

Use this skill when you need to:
- Design and implement complex, multi-step workflows in n8n.
- Integrate diverse tools, APIs, and services into a cohesive automation pipeline using n8n nodes.
- Configure advanced scheduling, including cron expressions, timezone management, and recurrence rules in n8n.
- Handle robust file operations, including cloud storage integration and secure transfers.
- Implement inter-workflow messaging patterns (Pub/Sub, Request/Reply, Event Streaming).
- Optimize workflow performance, manage state, and configure retry/recovery policies.
- Troubleshoot and diagnose workflow execution failures, data integration issues, and performance bottlenecks.

## Preconditions

Before acting, verify:
- The target environment is an n8n instance.
- You have access to the n8n credential manager.
- `N8N_ENCRYPTION_KEY` is set.
- Execution logs are enabled.

## Source Freshness

Volatile facts such as execution modes and security configurations must be verified against official n8n documentation.
- Verified against upstream: 2026-08-07

## n8n AI Agent Architecture

This skill utilizes n8n's AI agent architecture for workflow execution:
- **Supervisor**: Orchestrates the overall workflow and delegates tasks.
- **Discovery**: Identifies available tools and APIs.
- **Builder**: Constructs the workflow logic.
- **Planner**: Determines the sequence of execution.
- **Responder**: Formats and delivers the final output.
- **Parameter Updater**: Dynamically adjusts parameters during execution.

## Workflow

1. **Requirement Analysis**: Analyze requirements and determine if n8n is the appropriate tool.
2. **Architecture Design**: Design the workflow architecture, breaking complex processes into sub-workflows.
3. **Integration Setup**: Configure credentials securely using n8n's credential manager.
4. **Implementation**: Implement the workflow using n8n's visual builder or JSON definition.
5. **Scheduling & Triggers**: Configure triggers (webhooks, cron, events) with appropriate authentication.
6. **Testing & Validation**: Test the workflow in main mode before deploying to queue mode for distributed execution.
7. **Monitoring & Maintenance**: Monitor execution logs and handle errors using n8n's error handling nodes.

## Safety

- **Read-only discovery**: Always perform read-only discovery before making mutations.
- **Confirmation**: Require confirmation for destructive, external, privileged, financial, legal, or production-impacting actions.
- **Credential Management**: Explicitly mandate the use of n8n's credential manager and the `N8N_ENCRYPTION_KEY`.

## Validation

- Verify credentials are in the credential manager.
- Ensure webhooks have authentication.
- Validate `N8N_ENCRYPTION_KEY` is set.
- Confirm execution logs are enabled.

## Failure Handling

- Diagnose errors using n8n's execution logs.
- Choose alternative nodes or configurations if a step fails.
- Roll back changes if a workflow deployment causes issues.
- Avoid repeating a failed action unchanged.

## Output Contract

The result must include:
- A structured workflow definition (JSON).
- Evidence of successful execution or validation.
- Severity/confidence levels for any findings.
- Actionable next steps.

## Resources

- [Complete Reference](references/complete-reference.md): Details n8n's execution modes (main vs queue) and internal architecture.
- [Security Best Practices](references/security-best-practices.md): Details n8n security best practices, including credential management and webhook authentication.
- [Modular Design](references/modular-design.md): Details modular workflow design using sub-workflows in n8n.
- [Validation Script](scripts/validate-workflow.sh): Script to validate n8n workflow JSON.

## Orchestration

Use parallel work only for independent dimensions. Define inputs, schemas, conflict handling, synthesis, and termination conditions.

## Authoritative sources

- [Authoritative source map](references/source-map.md) — consult this before relying on volatile upstream behavior.

## Package resource index

| Resource | Purpose |
|---|---|
| [references/source-map.md](references/source-map.md) | Supporting package resource; inspect before use and apply the workflow’s safety and validation gates. |
