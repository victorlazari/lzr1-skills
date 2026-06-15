---
name: jira-status-workflows
description: Advanced Jira workflow configuration, complex state management, ITSM integration, and troubleshooting.
---

# Jira Status & Workflows

## When to Use

Use this skill when you need to:
- Design or audit complex Jira workflows and state machines.
- Implement advanced transition rules using custom scripting (e.g., ScriptRunner) or Jira Automation.
- Configure global, local, and loop transitions for specific business logic.
- Enforce Separation of Duties (SoD), sub-task blocking, and complex permission checks.
- Set up advanced post-functions like webhook triggers, cross-project syncing, or Jira Edge Connector (JEC).
- Design ITSM workflows (Service Requests, Incidents, Problems, Changes) in Jira Service Management.
- Migrate workflows between company-managed and team-managed projects.
- Troubleshoot workflow transition failures, permission issues, or script errors.
- Audit Jira workflow security, permission models, and data exposure.

## Sub-Agent Spawning

This skill supports spawning sub-agents for parallel execution when tasks can be decomposed:

| Trigger Condition | Sub-Agent Type | Purpose |
|---|---|---|
| Multiple workflows to audit | Workflow Auditor | Parallel review of workflow configurations and schemas |
| Multiple projects to migrate | Migration Specialist | Parallel migration of workflows between project types |
| Bulk transition failures | Diagnostics Agent | Parallel troubleshooting of transition errors |
| Multiple scripts to review | Script Reviewer | Parallel security and performance review of custom scripts |

### Spawning Rules
- Spawn when 3+ independent items (workflows, projects, scripts) need the same operation.
- Each sub-agent receives: context, specific target workflow/project/script, success criteria.
- Results are aggregated and cross-referenced for conflicts.
- Maximum concurrent sub-agents: 10.

## Workflow

1. **Requirement Analysis**: Understand the business process, issue types, and required states. Determine if it's a standard Jira Software project or an ITSM project (JSM).
2. **State Machine Design**: Map out statuses, categories (To Do, In Progress, Done), and transitions. Define local, global, and loop transitions.
3. **Rule Configuration**: Define conditions (e.g., permissions, SoD), validators (e.g., required fields), and post-functions (e.g., setting Resolution, webhooks).
4. **Scripting & Automation**: Implement complex logic using ScriptRunner or Jira Automation if standard rules are insufficient.
5. **Security & Governance**: Audit permission schemes, group memberships, and field-level security to ensure data protection and authorized access.
6. **Testing & Validation**: Test transitions with different user roles, verify edge cases (e.g., concurrent transitions), and check performance.
7. **Deployment & Monitoring**: Deploy the workflow scheme, monitor transition logs, and set up alerts for failures.

## Core Principles

- **State Machine Mindset**: Treat workflows as finite state machines with clear states, transitions, guards (conditions/validators), and actions (post-functions).
- **Status Categories**: Always map custom statuses to the correct category (To Do, In Progress, Done) to ensure accurate reporting and SLA tracking.
- **Resolution vs. Status**: Remember that an issue is "open" if Resolution is empty, and "closed" if Resolution is set. Always set Resolution via post-functions on transitions to "Done" statuses.
- **Principle of Least Privilege**: Restrict transition permissions and administrative access to authorized roles only.
- **Simplicity & Modularity**: Avoid over-engineering. Use modular workflow design and shared workflows where possible.
- **Performance**: Minimize complex scripted conditions and validators that could slow down transitions.

## Key References

- **Atlassian Jira Software Documentation**: Official guide on configuring workflows.
- **ScriptRunner for Jira Documentation**: Guide for Groovy scripting in workflows.
- **Jira Automation Documentation**: Guide for no-code/low-code automation rules.
- **ITIL Foundation**: Best practices for ITSM processes.
- **Jira Service Management Documentation**: Guides on request types, queues, and ITSM categories.
