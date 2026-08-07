---
name: jira-jsm-oncall
description: Advanced guide and workflow for Jira Service Management (JSM) alerts, on-call management, SLA configurations, and automation.
---

# Jira Service Management (JSM) Alerts & On-Call

## Scope and Triggers

This skill handles advanced incident response, alerting, and on-call management in Jira Service Management (JSM). It activates when:
- Designing complex transition rules using custom scripting or webhook triggers.
- Configuring sophisticated Service Level Agreements (SLAs) (business vs. calendar hours, multi-tiered policies).
- Integrating Asset Management (CMDB) with incident workflows for automated impact analysis.
- Implementing Jira Edge Connector (JEC) for secure synchronization.
- Developing advanced JQL queries and custom dashboards.
- Creating automation rules for auto-assigning and auto-closing tickets.

**Escalation Boundaries:**
- For general automation, recurring execution, or external API integrations outside of JSM-specific workflows, route to `automation-and-scheduling`.

## Preconditions

Before acting, verify:
- Target JSM environment (Cloud vs. Data Center).
- Necessary administrative permissions to modify workflows, SLAs, or automation rules.
- User intent and constraints (e.g., staging vs. production).

## Source Freshness

JSM features and APIs evolve. Always verify current capabilities against official Atlassian documentation before applying changes. See the focused references for canonical links and `Verified against upstream` dates.

## Workflow

1. **Assess Current Configuration:** Evaluate the current JSM setup, identifying gaps in alerting, SLA tracking, or automation.
2. **Consult Focused References:** Review the relevant reference guide for the specific task:
   - `references/sla-config.md` for SLA configurations.
   - `references/cmdb-integration.md` for Asset/CMDB integration.
   - `references/jql-reporting.md` for advanced JQL and reporting.
3. **Validate Proposed Changes:**
   - Use `scripts/validate-jql.sh` to validate JQL syntax before saving filters.
   - Use `scripts/test-webhook.sh` in dry-run mode to test webhook payloads.
4. **Apply in Staging:** Implement configurations in a staging environment first.
5. **Request Confirmation:** Require explicit user confirmation before deploying to production.
6. **Stop Condition:** Stop when all configurations are applied, validated, and confirmed by the user.

## Safety

- **Read-only Discovery:** Always assess the current state before proposing changes.
- **Confirmation Required:** Require explicit user confirmation before modifying production SLAs, transition rules, or automation rules.
- **Dry-run Mode:** Use dry-run mode for webhook testing where feasible.

## Validation

- **Syntax Checks:** Validate JQL syntax using the provided script.
- **Smoke Tests:** Test webhook payloads using the provided script.
- **Postcondition Verification:** Ensure CMDB integrations are tested in a staging environment.

## Failure Handling

- If a JQL query fails validation, review the syntax against the Atlassian documentation and adjust.
- If a webhook test fails, verify the payload format and endpoint URL.
- Do not repeat a failed action unchanged. Diagnose the error and propose an alternative.

## Output Contract

The result must include:
- A summary of the configurations applied.
- Evidence of successful validation (e.g., JQL validation output, webhook test results).
- Any required next steps or manual verifications.

## Resources

- [SLA Configuration Guide](references/sla-config.md)
- [CMDB Integration Guide](references/cmdb-integration.md)
- [JQL Reporting Guide](references/jql-reporting.md)
- [Validate JQL Script](scripts/validate-jql.sh)
- [Test Webhook Script](scripts/test-webhook.sh)
