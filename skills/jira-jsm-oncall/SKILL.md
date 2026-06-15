---
name: jira-jsm-oncall
description: Advanced guide and workflow for Jira Service Management (JSM) alerts, on-call management, SLA configurations, and automation.
---

# Jira Service Management (JSM) Alerts & On-Call

## When to Use

This skill should be utilized when managing, configuring, or troubleshooting Jira Service Management (JSM) environments, specifically focusing on advanced incident response, alerting, and on-call management. It is highly applicable when:
- Designing complex transition rules using custom scripting (e.g., ScriptRunner, Automation for Jira) or webhook triggers.
- Configuring sophisticated Service Level Agreements (SLAs) that differentiate between business hours and calendar hours, or involve multi-tiered escalation policies.
- Integrating Asset Management (CMDB) with incident workflows for automated impact analysis and dynamic routing.
- Implementing Jira Edge Connector (JEC) for secure, bi-directional synchronization with external monitoring or ITSM tools.
- Developing advanced JQL queries and custom dashboards for real-time operational metrics and SLA compliance reporting.
- Creating automation rules for auto-assigning tickets based on on-call schedules and auto-closing resolved incidents.

## Sub-Agent Spawning

This skill supports spawning sub-agents for parallel execution when tasks can be decomposed:

| Trigger Condition | Sub-Agent Type | Purpose |
|---|---|---|
| Multiple workflows to update | Workflow Configurator | Parallel implementation of custom transition scripts |
| Multiple SLAs to configure | SLA Manager | Parallel setup of business calendars and multi-tiered metrics |
| Multiple CMDB integrations | Asset Integrator | Parallel linking of external assets and impact analysis rules |
| Bulk JQL dashboard creation | Reporting Analyst | Parallel generation of custom reports and gadgets |

### Spawning Rules
- Spawn when 3+ independent items need the same operation.
- Each sub-agent receives: context, specific target, success criteria.
- Results are aggregated and cross-referenced for conflicts.
- Maximum concurrent sub-agents: 10.

## Workflow

1. **Assessment and Planning:** Evaluate the current JSM configuration, identifying gaps in alerting, SLA tracking, or automation. Determine the necessity of custom scripts versus native automation rules.
2. **Transition Rule Configuration:** Implement advanced transition rules. Utilize Groovy scripts for dynamic validations or configure webhooks to trigger external systems like PagerDuty or Opsgenie.
3. **SLA Definition:** Define business calendars and configure SLA metrics (e.g., Time to First Response, Time to Resolution). Establish multi-tiered policies for different priority levels.
4. **CMDB Integration:** Link Jira Assets or external CMDBs to incident workflows. Configure automation to perform impact analysis based on affected configuration items (CIs).
5. **Automation Implementation:** Set up rules for auto-assigning tickets to on-call engineers and auto-closing tickets after a period of inactivity post-resolution.
6. **Reporting and Monitoring:** Develop advanced JQL queries to track SLA breaches and on-call workload. Build custom dashboards to visualize these metrics.
7. **Testing and Validation:** Rigorously test all configurations in a staging environment to ensure scripts, webhooks, and SLAs perform as expected under various scenarios.

## Core Principles

- **Context-Aware Automation:** Ensure that automation rules and scripts utilize all available context, such as linked assets and priority, to make intelligent routing and transition decisions.
- **Accurate Measurement:** SLAs must reflect reality. Accurately distinguish between business and calendar hours to provide fair and meaningful metrics for support teams.
- **Seamless Integration:** Leverage webhooks and JEC to maintain a single source of truth across JSM and external alerting/monitoring platforms.
- **Proactive Impact Analysis:** Utilize CMDB data not just for documentation, but as an active component in incident prioritization and resolution strategies.
- **Scalability and Maintainability:** Prefer global transitions where standardization is needed, and reserve local transitions for highly specialized workflows to keep the system manageable.

## Key References

- [Jira Service Management Documentation](https://confluence.atlassian.com/servicedeskcloud)
- [Automation for Jira Reference](https://support.atlassian.com/cloud-automation/)
- [ScriptRunner for Jira Documentation](https://docs.adaptavist.com/sr4j/latest)
- [Jira Edge Connector (JEC) Guide](https://support.atlassian.com/opsgenie/docs/integrate-opsgenie-with-jira-edge-connector/)
- [Advanced JQL Functions](https://support.atlassian.com/jira-software-cloud/docs/advanced-search-reference-jql-functions/)
