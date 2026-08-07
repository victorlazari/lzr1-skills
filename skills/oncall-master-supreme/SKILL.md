---
name: oncall-master-supreme
description: Operational playbook for managing on-call systems, incidents, ChatOps, runbooks, and SLOs. Triggers on incident response, schedule management, or on-call configuration tasks.
---

# On-Call Master Supreme

## Scope and Triggers

**Triggers:**
- Designing or auditing high availability (HA) and disaster recovery (DR) architectures for on-call systems.
- Integrating ChatOps (Slack, Microsoft Teams) for incident war rooms and automated notifications.
- Conducting blameless post-incident reviews (postmortems) and integrating with tools like Jeli.
- Automating runbooks and implementing auto-remediation workflows to reduce MTTR.
- Defining, tracking, and reporting on Service Level Objectives (SLOs) and Service Level Indicators (SLIs).
- Implementing and managing follow-the-sun multi-region on-call schedules and handoffs.
- Utilizing the `oncall-master-supreme` CLI for incident management, scheduling, and configuration.
- Managing JSON-based configuration schemas for notifications, escalations, users, integrations, and security.

**Non-Goals & Escalation Boundaries:**
- Does not handle general system administration outside of on-call/incident context.
- Does not perform arbitrary code execution or infrastructure provisioning without explicit runbook definitions.
- Escalate to `automation-and-scheduling` when setting up recurring schedules or background processes.
- Escalate to `post-mortem-master` when writing customer-facing incident post-mortems.

## Preconditions

1.  **Environment:** Ensure access to the target on-call platform (e.g., PagerDuty, Opsgenie, incident.io).
2.  **Permissions:** Verify sufficient privileges to modify schedules, trigger incidents, or update configurations.
3.  **Inputs:** Gather necessary details (e.g., service IDs, user IDs, incident severity, configuration JSON).

## Source Freshness

Volatile facts (e.g., API endpoints, supported versions) must be verified against official documentation at runtime.
-   [PagerDuty API Documentation](https://developer.pagerduty.com/api-reference/)
-   [incident.io API Documentation](https://api-docs.incident.io/)
-   [Datadog API Documentation](https://docs.datadoghq.com/api/latest/)

## Workflow

1.  **Assess and Define:** Assess current architecture and define SLOs/SLIs. Consult [SLO/SLI Tracking](references/slo-sli.md) and [HA/DR](references/ha-dr.md).
2.  **Configure:** Configure global settings, schedules, and notifications using validated JSON schemas. Consult [Configuration Schemas](references/config-schemas.md) and [Follow-the-Sun](references/follow-the-sun.md).
    -   *Validation:* Run `scripts/validate-config.sh <config.json>` before applying.
3.  **Integrate:** Set up integrations with monitoring and ChatOps tools. Consult [ChatOps Integration](references/chatops.md).
4.  **Automate:** Implement and test runbook automations with dry-runs. Consult [Runbook Automation](references/runbooks.md).
5.  **Respond:** Respond to incidents using CLI and ChatOps. Consult [CLI Reference](references/cli-reference.md).
6.  **Review:** Conduct postmortems and track remediation actions. Consult [Postmortems](references/postmortems.md).
7.  **Stop Condition:** Stop when SLOs are met, incidents are resolved, and postmortems are completed.

## Safety

-   **Read-Only First:** Always perform read-only discovery (e.g., listing schedules, viewing incidents) before making changes.
-   **Confirmation Required:** Require explicit user confirmation for destructive actions (e.g., resolving incidents, overriding schedules, deleting configurations).
-   **Dry-Runs:** Use dry-run support for configuration changes where available.

## Validation

-   **Syntax Checks:** Validate JSON configuration schemas using `scripts/validate-config.sh`.
-   **Postcondition Verification:** Verify that changes (e.g., schedule updates, incident resolution) are reflected in the target system.

## Failure Handling

-   **Diagnosis:** Check API response codes and error messages.
-   **Rollback:** Revert to the previous configuration or schedule state if an update fails.
-   **Retry:** Do not repeat a failed action unchanged. Adjust inputs or configuration based on error diagnostics.

## Output Contract

-   **Structure:** Provide a structured summary of actions taken, including IDs of created/modified resources.
-   **Evidence:** Include relevant logs, API responses, or CLI output.
-   **Next Steps:** Suggest actionable next steps (e.g., reviewing a generated postmortem, verifying a schedule change).

## Resources

-   [High Availability and Disaster Recovery](references/ha-dr.md)
-   [ChatOps Integration](references/chatops.md)
-   [Postmortems](references/postmortems.md)
-   [Runbook Automation](references/runbooks.md)
-   [SLO/SLI Tracking](references/slo-sli.md)
-   [Follow-the-Sun Models](references/follow-the-sun.md)
-   [CLI Reference](references/cli-reference.md)
-   [Configuration Schemas](references/config-schemas.md)
-   [Validate Config Script](scripts/validate-config.sh)

## Orchestration

When parallel execution is required (e.g., configuring multiple services):
1.  **Input List:** Define an explicit list of target services or configurations.
2.  **Bounded Concurrency:** Limit concurrent operations to avoid rate limits.
3.  **Evidence:** Collect success/failure status for each operation.
4.  **Synthesis:** Provide a consolidated report of all parallel operations.
